#include <iostream>
#include <fstream>
#include <filesystem>
#include <sstream>
#include <string>
#include <map>
#include <algorithm>
#include <vector>
#include <cmath>

unsigned int read4(char* buf, int at) {
	return (unsigned char)buf[at]
		+ ((unsigned char)buf[at + 1] << 8)
		+ ((unsigned char)buf[at + 2] << 16)
		+ ((unsigned char)buf[at + 3] << 24);
}

void write4(char* buf, int at, unsigned int val) {
	buf[at] = val & 0xFF;
	buf[at + 1] = (val & 0xFF00) >> 8;
	buf[at + 2] = (val & 0xFF0000) >> 16;
	buf[at + 3] = (val & 0xFF000000) >> 24;
}

unsigned int read4(std::ifstream& in) {
	unsigned char c1 = in.get();
	unsigned char c2 = in.get();
	unsigned char c3 = in.get();
	unsigned char c4 = in.get();
	return c1 + (c2 << 8) + (c3 << 16) + (c4 << 24);
}

void write4(std::ofstream& out, unsigned int val) {
	out.put(val & 0xFF);
	out.put((val & 0xFF00) >> 8);
	out.put((val & 0xFF0000) >> 16);
	out.put((val & 0xFF000000) >> 24);
}

int countLSBZeros(int value) {
	unsigned int c = 0;
	while (((value >> c) & 1) == 0) {
		c++;
	}
	return c;
}

class Swizzler {
public:
	Swizzler() {}
	Swizzler(unsigned int width, unsigned int bpp, unsigned int blockHeight) {
		bhMask = (blockHeight * 8) - 1;

		bhShift = countLSBZeros(blockHeight * 8);
		bppShift = countLSBZeros(bpp);

		unsigned int widthInGobs = (unsigned int)ceil(width * bpp / 64.);

		gobStride = 512 * blockHeight * widthInGobs;
		xShift = countLSBZeros(blockHeight * 512);
	}

	unsigned int getOffset(unsigned int x, unsigned int y) {
		x <<= bppShift;

		unsigned int off = (y >> bhShift) * gobStride;
		off += (x >> 6) << xShift;
		off += ((y & bhMask) >> 3) << 9;
		off += ((x & 0x3F) >> 5) << 8;
		off += ((y & 0x07) >> 1) << 6;
		off += ((x & 0x1F) >> 4) << 5;
		off += ((y & 0x01) >> 0) << 4;
		off += ((x & 0x0F) >> 0) << 0;

		return off;
	}

	unsigned int bhMask;
	unsigned int bhShift;
	unsigned int bppShift;
	unsigned int gobStride;
	unsigned int xShift;
};

struct Texture {
	std::filesystem::path path;
	int format;
	int swizzleType;
	int swizzleExpandSize;
	char* ykcmp = NULL;
	int zsz = 0;
};

int ykCompress(char* src, int srcSz, char*& dest) {
	dest = new char[0x14 + srcSz + srcSz / 0x7E + 1];
	const char header[] = "YKCMP_V1\x04\0\0\0";
	std::copy(header, header + 0xC, dest);
	write4(dest, 0x10, srcSz);

	int cp = 0x14, dp = 0;
	int copyHeader = -1;

	while (dp < srcSz) {
		int sz = 0, offset = 0, saved = 0;
		for (int i = dp - 0x1000; i < dp; i++) {
			if (i < 0) {
				i = -1;
				continue;
			}

			int j = 0;
			for (; dp + j < srcSz && src[i + j] == src[dp + j] && i + j < dp && j < 0x202; j++) {}

			int s = j - 3;
			if (s > saved) {
				sz = j;
				offset = dp - i;
				saved = s;
			}
		}
		for (int i = dp - 0x100; i < dp; i++) {
			if (i < 0) {
				i = -1;
				continue;
			}

			int j = 0;
			for (; dp + j < srcSz && src[i + j] == src[dp + j] && i + j < dp && j < 0x21; j++) {}

			int s = j - 2;
			if (s > saved) {
				sz = j;
				offset = dp - i;
				saved = s;
			}
		}
		for (int i = dp - 0x10; i < dp; i++) {
			if (i < 0) {
				i = -1;
				continue;
			}

			int j = 0;
			for (; dp + j < srcSz && src[i + j] == src[dp + j] && i + j < dp && j < 0x4; j++) {}

			int s = j - 1;
			if (s > saved) {
				sz = j;
				offset = dp - i;
				saved = s;
			}
		}

		if (copyHeader != -1) {
			if (saved <= 0) {
				if (dest[copyHeader] >= 0x7E) {
					copyHeader = cp;
					dest[cp++] = 0;
				}
				dest[cp++] = src[dp++];
				dest[copyHeader]++;
				continue;
			}
			else {
				copyHeader = -1;
			}
		}

		if (saved <= 0) {
			copyHeader = cp;
			dest[cp++] = 1;
			dest[cp++] = src[dp++];
			continue;
		}

		if (sz <= 0x4 && offset <= 0x10) {
			dest[cp++] = (sz << 4) + 0x70 + (offset - 1);
		}
		else if (sz <= 0x21 && offset <= 0x100) {
			dest[cp++] = sz + 0xBE;
			dest[cp++] = offset - 1;
		}
		else {
			int tmp = sz + 0xE00 - 3;
			dest[cp++] = (tmp >> 4);
			dest[cp++] = ((tmp & 0xF) << 4) + ((offset - 1) >> 8);
			dest[cp++] = ((offset - 1) & 0xFF);
		}
		dp += sz;
	}
	write4(dest, 0xC, cp);
	return cp;
}

void compress(Texture& tex) {
	std::ifstream in(tex.path, std::ios::binary);
	in.ignore(0xC);

	unsigned int height = read4(in);
	unsigned int width = read4(in);
	in.ignore(0x6C);
	if (tex.format == 0x6) 
		in.ignore(0x4);

	unsigned int swWidth = width, swHeight = height;
	int blockSize = tex.swizzleExpandSize * 64;
	if (tex.swizzleType == 3 && blockSize != 0) {
		swWidth = blockSize * (unsigned int)ceil(swWidth / (double)blockSize);
		swHeight = blockSize * (unsigned int)ceil(swHeight / (double)blockSize);
	}
	if (tex.format == 0x2 || tex.format == 0x6) {
		width /= 4; swWidth /= 4;
		height /= 4; swHeight /= 4;
	}

	Swizzler sw;
	unsigned int bpp;

	switch (tex.format) {
	case 0x4: bpp = 8; break;
	case 0x20: bpp = 4; break;
	default: bpp = 16; break;
	}

	switch (tex.swizzleType) {
	case 1: sw = Swizzler(swWidth, bpp, 2); break;
	case 2: sw = Swizzler(swWidth, bpp, 4); break;
	default: sw = Swizzler(swWidth, bpp, 8); break;
	}

	char* swizzled = new char[swWidth * swHeight * bpp];
	for (unsigned int i = 0; i < swWidth*swHeight*bpp; i++) {
		swizzled[i] = 0;
	}
	char* buffer = new char[bpp];
	for (unsigned int y = 0; y < height; y++) {
		for (unsigned int x = 0; x < width; x++) {
			unsigned int off = sw.getOffset(x, y);
			in.read(buffer, bpp);
			std::copy(buffer, buffer + bpp, swizzled + off);
		}
	}
	delete[] buffer;
	in.close();

	//std::ofstream out(tex.path.stem().generic_string() + ".raw", std::ios::binary);
	//out.write(swizzled, swWidth*swHeight*bpp);
	//out.close();

	tex.zsz = ykCompress(swizzled, swWidth*swHeight*bpp, tex.ykcmp);
	//std::ofstream outyk(tex.path.stem().generic_string() + ".yk", std::ios::binary);
	//outyk.write(tex.ykcmp, tex.zsz);
	//outyk.close();

	delete[] swizzled;
	std::cout << "catch";
}

int main(int argc, char** argv) {
	if (argc != 2) {
		std::cout << "Usage: \"" << argv[0] << " 12345.nltx\" to import texture from the folder 12345/ into 12345.nltx,\n";
		return 0;
	}

	std::map<int, Texture> textures;

	std::filesystem::path inputFolder = std::filesystem::path(argv[1]).parent_path() / std::filesystem::path(argv[1]).stem();
	if (!std::filesystem::exists(inputFolder)) {
		std::cout << "Please create a folder named \"" << std::filesystem::path(argv[1]).stem()
			<< "\" and put the .dds files you want to import in it.\n";
		return 0;
	}

	int f = 0;
	for (auto& p : std::filesystem::directory_iterator(inputFolder)) {
		if (p.path().extension() != ".dds") {
			continue;
		}

		std::stringstream fname(p.path().stem().generic_string());
		int id = -1, format = -1, swizzleType = -1, swizzleExpandSize = -1;
		std::string origOffset; char underscore;
		fname >> id >> underscore >> format >> underscore >> swizzleType >> underscore >> swizzleExpandSize;
		if (id == -1 || format == -1 || swizzleType == -1 || swizzleExpandSize == -1) {
			continue;
		}

		f++;
		textures[id] = Texture{ p.path(), format, swizzleType, swizzleExpandSize };
		std::cout << "Compressing " << p << std::endl;
		compress(textures[id]);
	}

	if (f != 1) {
		std::cout << "The input folder should contain only one .dds file, or it has improper filenames.\n";
		std::cout << "Please use the same filename as generated by nltxEx.exe.\n";
		return 0;
	}

	std::ifstream fad(argv[1], std::ios::binary | std::ios::ate);
	int fadSize = (int)fad.tellg();
	fad.seekg(0);
	char* buffer = new char[fadSize];
	fad.read(buffer, fadSize);
	fad.close();

	std::ofstream backup(std::string(argv[1]) + ".bak", std::ios::binary);
	backup.write(buffer, fadSize);
	backup.close();

	std::ofstream out(argv[1], std::ios::binary);
	for (unsigned int i = 0; i < 1; i++) {
		std::cout << "Importing " << textures[i].path << std::endl;
		unsigned int sz = textures[i].zsz + 0x30;
		sz = 16 * (unsigned int)ceil(sz / 16.);
		out.write(buffer, 0x80);
		out.write(textures[i].ykcmp, textures[i].zsz);
	}

	for (auto& tex : textures) {
		delete[] tex.second.ykcmp;
	}
	std::cout << "Done\n";
	return 0;
}