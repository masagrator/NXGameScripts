//Original work by iltrof
//Fixed texture type reading by MasaGratoR

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <filesystem>
#include <cmath>
#include <vector>

namespace fs = std::filesystem;

fs::path outputFolder;
fs::path currentFad;

const char ddsHeader0[] = "DDS |\0\0\0\x07\x10\0\0";
const char ddsHeaderRGBA[] = "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x20\0\0\0\x41\0\0\0\0\0\0\0\x20\0\0\0"
"\xff\0\0\0\0\xff\0\0\0\0\xff\0\0\0\0\xff\0\x10\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0";
const char ddsHeaderDXT1[] = "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x20\0\0\0\x4\0\0\0DXT1\0\0\0\0"
"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x10\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0";
const char ddsHeaderDXT5[] = "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x20\0\0\0\x4\0\0\0DXT5\0\0\0\0"
"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x10\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0";
const char ddsHeaderDXT3[] = "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x20\0\0\0\x4\0\0\0DXT3\0\0\0"
"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x10\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0";
const char ddsHeaderBC7[] = "\0\0\0\x1\x1\0\0\0\x01\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x20\0\0\0\x4\0\0\0DX10\0\0\0\0\0\0\0\0\0"
"\0\0\0\0\0\0\0\0\0\0\0\0\x10\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x62\0\0\0\x3\0\0\0\0\0\0\0\x1\0\0\0\0\0\0\0";

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

unsigned int read4(std::ifstream& in) {
	unsigned char c1 = in.get();
	unsigned char c2 = in.get();
	unsigned char c3 = in.get();
	unsigned char c4 = in.get();
	return c1 + (c2 << 8) + (c3 << 16) + (c4 << 24);
}

unsigned int read2(std::ifstream& in) {
	unsigned char c1 = in.get();
	unsigned char c2 = in.get();
	return c1 + (c2 << 8);
}

void write4(std::ofstream& out, unsigned int n) {
	out.put(n & 0xFF);
	out.put((n & 0xFF00) >> 8);
	out.put((n & 0xFF0000) >> 16);
	out.put((n & 0xFF000000) >> 24);
}

bool isMagic(std::ifstream& in) {
	if (in.peek() != 0x59) {
		return false;
	}
	auto oldOffset = in.tellg();
	char magic[9];
	in.get(magic, 9);
	in.seekg(oldOffset);
	return std::string(magic) == "YKCMP_V1";
}

void extract(std::ifstream& in, unsigned int offset, unsigned int id) {
	auto oldOffset = in.tellg();
	in.seekg(offset);
	in.ignore(24);
	unsigned int width = read2(in);
	unsigned int height = read2(in);
	in.ignore(2);
	unsigned char pixeltype = in.get();
	if (pixeltype != 0x4 && pixeltype != 0x8 && pixeltype != 0x20) {
		std::cout << "Unknown pixeltype in " << currentFad << " @0x" << std::hex << (offset + 0x1E) << std::dec << std::endl;
		std::cout << "Should be 0x4 (DXT1), 0x8 (DXT3, DXT5, BC7) or 0x20 (RGBA). Skipping...\n";
		in.seekg(oldOffset);
		return;
	}
	in.ignore(1);
	unsigned char textureType = in.get();
	if (textureType != 0x0 && textureType != 0x4 && textureType != 0x5 && textureType != 0x6 && textureType != 0x7) {
		std::cout << "Unknown textureType in " << currentFad << " @0x" << std::hex << (offset + 0x20) << std::dec << std::endl;
		std::cout << "Should be 0x0 (RGBA8), 0x4 (DXT1), 0x5 (DXT3), 0x6 (DXT5) or 0x7 (BC7). Skipping...\n";
		in.seekg(oldOffset);
		return;
	}
	in.ignore(7);
	unsigned char swizzleType = in.get();
	if (swizzleType < 1 || swizzleType > 4) {
		std::cout << "Unknown swizzle type in " << currentFad << " @0x" << std::hex << (offset + 0x28) << std::dec << std::endl;
		std::cout << "Should be 1, 2, 3 or 4. Skipping...";
		in.seekg(oldOffset);
		return;
	}
	unsigned char swizzleExpandSize = in.get();
	unsigned int blockSize = swizzleExpandSize * 64;
	in.ignore(6);

	if (!isMagic(in)) {
		std::cout << "Expected a YKCMP archive in " << currentFad << " @0x" << std::hex << (offset + 0x30) << std::dec << std::endl;
		std::cout << "There wasn't one though. Skipping...\n";
		in.seekg(oldOffset);
		return;
	}

	in.ignore(16);
	unsigned int size = read4(in);

	std::stringstream sname;
	sname << id << "_" << (unsigned int)(pixeltype) << "_"
		<< (unsigned int)swizzleType << "_" << (unsigned int)swizzleExpandSize << ".dds";
	fs::path name = outputFolder / fs::path(sname.str());
	std::cout << "Extracting " << name << std::endl;

	char* decomp = new char[size];
	unsigned int op = 0;
	while (op < size) {
		unsigned char tmp = in.get();
		if (tmp < 0x80) {
			for (int j = 0; j < tmp; j++) {
				decomp[op++] = in.get();
			}
		}
		else {
			int sz, behind;
			if (tmp < 0xC0) {
				sz = (tmp >> 4) - 7;
				behind = (tmp & 0x0F) + 1;
			}
			else if (tmp < 0xE0) {
				sz = tmp - 0xBE;
				behind = (unsigned char)in.get() + 1;
			}
			else {
				unsigned char tmp2 = in.get();
				unsigned char tmp3 = in.get();
				sz = (tmp << 4) + (tmp2 >> 4) - 0xDFD;
				behind = ((tmp2 & 0x0F) << 8) + tmp3 + 1;
			}
			unsigned int opt = op - behind;
			for (int j = 0; j < sz; j++) {
				decomp[op++] = decomp[opt++];
			}
		}
	}

	std::ofstream outDDS(name, std::ios::binary);

	outDDS.write(ddsHeader0, 12);
	write4(outDDS, height);
	write4(outDDS, width);
	if (textureType == 0x0) {
		outDDS.write(ddsHeaderRGBA, 108);
	} 
	else if (textureType == 0x4) {
		outDDS.write(ddsHeaderDXT1, 108);
	}
	else if (textureType == 0x5) {
		outDDS.write(ddsHeaderDXT3, 108);
	}
	else if (textureType == 0x6) {
		outDDS.write(ddsHeaderDXT5, 108);
	}
	else {
		outDDS.write(ddsHeaderBC7, 128);
	}

	unsigned int swWidth = width, swHeight = height;
	if (swizzleType >= 3 && blockSize != 0 && pixeltype != 0x20) {
		swWidth = blockSize * (unsigned int)ceil(swWidth / (double)blockSize);
		swHeight = blockSize * (unsigned int)ceil(swHeight / (double)blockSize);
	}
	if (pixeltype == 0x4 || pixeltype == 0x8) {
		width /= 4; swWidth /= 4;
		height /= 4; swHeight /= 4;
	}
	
	Swizzler sw;
	unsigned int bpp;

	switch (pixeltype) {
	case 0x4: bpp = 8; break;
	case 0x20: bpp = 4; break;
	default: bpp = 16; break;
	}

	sw = Swizzler(swWidth, bpp, pow(2, (int)swizzleType));

	for (unsigned int y = 0; y < height; y++) {
		for (unsigned int x = 0; x < width; x++) {
			unsigned int off = sw.getOffset(x, y);
			outDDS.write(decomp + off, bpp);
		}
	}

	outDDS.close();

	delete[] decomp;
	in.seekg(oldOffset);
}

int main(int argc, char** argv)
{
	std::vector<fs::path> fads;
	if (argc > 1) {
		fads.push_back(fs::path(argv[1]));
	}
	else {
		for (auto& p : fs::directory_iterator(".")) {
			if (p.path().extension() == ".fad") {
				fads.push_back(p.path());
			}
		}
	}

	int w = 0;
	for (fs::path& p : fads) {
		currentFad = p;
		outputFolder = fs::path(p).parent_path() / fs::path(p).stem() / "";
		fs::create_directories(outputFolder);

		std::ifstream in(p, std::ios::binary);
		in.ignore(8);
		unsigned int nFiles = read4(in) + read4(in) + read4(in) + read4(in);
		in.ignore(24);

		int id = 0;
		for (unsigned int i = 0; i < nFiles; i++) {
			in.ignore(12);
			unsigned int type = read4(in);
			if (type != 0) {
				in.ignore(16);
				continue;
			}
			unsigned int offset = read4(in);
			in.ignore(12);

			extract(in, offset, id++);
			w++;
		}
	}

	std::cout << "Done extracting " << w << " file(s)." << std::endl;

	return 0;
}