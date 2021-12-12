//Original work by iltrof
//Fixed texture type reading by MasaGratoR

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <filesystem>
#include <cmath>
#include <vector>
#include <map>

namespace fs = std::filesystem;

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
	fs::path path;
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

	int percentSize = srcSz / 100;
	int percent = 0, percentPrev = 0;
	std::cout << ".........|.........|.........|.........|.........|.........|.........|.........|.........|.........|\n";

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

		percent = dp / percentSize;
		if (percent > 100) percent = 100;
		for (int i = 0; i < percent - percentPrev; i++) {
			std::cout << '#';
		}
		percentPrev = percent;
	}
	std::cout << std::endl;
	write4(dest, 0xC, cp);
	return cp;
}

void compress(Texture& tex) {
	std::ifstream in(tex.path, std::ios::binary);
	in.ignore(0xC);

	unsigned int height = read4(in);
	unsigned int width = read4(in);
	in.ignore(0x6C);

	unsigned int swWidth = width, swHeight = height;
	int blockSize = tex.swizzleExpandSize * 64;
	if (tex.swizzleType >= 3 && blockSize != 0) {
		swWidth = blockSize * (unsigned int)ceil(swWidth / (double)blockSize);
		swHeight = blockSize * (unsigned int)ceil(swHeight / (double)blockSize);
	}
	if (tex.format == 0x4 || tex.format == 0x8) {
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

	sw = Swizzler(swWidth, bpp, pow(2, tex.swizzleType));

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
}

int main(int argc, char** argv) {
	if (argc < 3) {
		std::cout << "Usage: \"" << argv[0] << " 12345.fad -a\" to import all files from the folder 12345/ into 12345.fad,\n";
		std::cout << "\"" << argv[0] << " 12345.fad texture.dds\" to import one .dds into 12345.fad.\n";
		return 0;
	}

	std::map<int, Texture> textures;

	if (std::string(argv[2]) == "-a") {
		fs::path inputFolder = fs::path(argv[1]).parent_path() / fs::path(argv[1]).stem();
		if (!fs::exists(inputFolder)) {
			std::cout << "Please create a folder named \"" << fs::path(argv[1]).stem()
				<< "\" and put the .dds files you want to import in it.\n";
			return 0;
		}

		int f = 0;
		for (auto& p : fs::directory_iterator(inputFolder)) {
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

		if (f == 0) {
			std::cout << "The input folder contains no .dds files, or they have improper filenames.\n";
			std::cout << "Please use the same filenames as generated by fadEx.exe.\n";
			return 0;
		}
	}
	else {
		std::stringstream fname(fs::path(argv[2]).stem().generic_string());
		int id = -1, format = -1, swizzleType = -1, swizzleExpandSize = -1;
		std::string origOffset; char underscore;
		fname >> id >> underscore >> format >> underscore >> swizzleType >> underscore >> swizzleExpandSize;

		if (id == -1 || format == -1 || swizzleType == -1 || swizzleExpandSize == -1) {
			std::cout << "The input file has an improper filename.\n";
			std::cout << "Please use the same filenames as generated by fadEx.exe.\n";
			return 0;
		}

		textures[id] = Texture{ fs::path(argv[2]), format, swizzleType, swizzleExpandSize };

		std::cout << "Compressing " << argv[2] << std::endl;
		compress(textures[id]);
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

	unsigned int metadataSize = read4(buffer, 0x20);
	char* metadata = new char[metadataSize];
	std::copy(buffer, buffer + metadataSize, metadata);

	unsigned int files = read4(buffer, 0x8) + read4(buffer, 0xC) + read4(buffer, 0x10) + read4(buffer, 0x14);
	unsigned int tid = 0, toff = metadataSize;
	std::vector<unsigned int> oldOffsets, oldSizes;
	for (unsigned int i = 0; i < files; i++) {
		unsigned int type = read4(buffer, 0x3C + 0x20 * i);
		if (type == 0) {
			oldOffsets.push_back(read4(buffer, 0x40 + 0x20 * i));
			oldSizes.push_back(read4(buffer, 0x38 + 0x20 * i));
			unsigned int sz = oldSizes.back();
			if (textures.find(tid) != textures.end()) {
				sz = textures[tid].zsz + 0x30;
				sz = 16 * (unsigned int)ceil(sz / 16.);
			}
			write4(metadata, 0x40 + 0x20 * i, toff);
			write4(metadata, 0x38 + 0x20 * i, sz);
			toff += sz;
			tid++;
		}
	}

	std::ofstream out(argv[1], std::ios::binary);
	out.write(metadata, metadataSize);
	for (unsigned int i = 0; i < tid; i++) {
		if (textures.find(i) == textures.end()) {
			out.write(buffer + oldOffsets[i], oldSizes[i]);
		}
		else {
			std::cout << "Importing " << textures[i].path << std::endl;
			unsigned int sz = textures[i].zsz + 0x30;
			sz = 16 * (unsigned int)ceil(sz / 16.);
			out.write(buffer + oldOffsets[i], 0x8);
			write4(out, sz);
			out.write(buffer + oldOffsets[i] + 0xC, 0x4);
			write4(out, textures[i].zsz);
			out.write(buffer + oldOffsets[i] + 0x14, 0x1C);
			out.write(textures[i].ykcmp, textures[i].zsz);
			for (unsigned int j = 0; j < sz - textures[i].zsz - 0x30; j++) {
				out.put('\0');
			}
		}
	}

	delete[] metadata;
	for (auto& tex : textures) {
		delete[] tex.second.ykcmp;
	}
	std::cout << "Done\n";
	return 0;
}