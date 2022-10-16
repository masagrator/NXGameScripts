# Based on work of Cabalex and Woewulf from Nier:Modding discord

from tegrax1swizzle import *
import sys

formats = {
	# DDS
	0x25: "R8G8B8A8_UNORM",
	0x42: "BC1_UNORM",
	0x43: "BC2_UNORM",
	0x44: "BC3_UNORM",
	0x45: "BC4_UNORM",
	0x46: "BC1_UNORM_SRGB",
	0x47: "BC2_UNORM_SRGB",
	0x48: "BC3_UNORM_SRGB",
	0x49: "BC4_SNORM",
	0x50: "BC6H_UF16",
	# ASTC (weird texture formats ??)
	0x2D: "ASTC_4x4_UNORM",
	0x38: "ASTC_8x8_UNORM",
	0x3A: "ASTC_12x12_UNORM",
	# ASTC
	0x79: "ASTC_4x4_UNORM",
	0x80: "ASTC_8x8_UNORM",
	0x87: "ASTC_4x4_SRGB",
	0x8E: "ASTC_8x8_SRGB",

	# Unknown NieR switch formats
	0x79: "ASTC_4x4_UNORM",
	0x7D: "ASTC_6x6_UNORM",
	0x8B: "ASTC_6x6_SRGB",
}

class NieRSwitchTexture:
	def __init__(self, extracted, width, height, size):
		self.size = size
		self.flags = 3
		self.id = 1
		self.extracted = extracted
		self.identifier = "%08x" % 1

		self.magic = 0
		self.format = 0x79
		self._format = formats[self.format]
		self.version = 1
		self.width = width
		self.height = height
		self.depth = 1
		self.mipCount = 1
		self.unknown1 = 0
		self.unknown2 = 0
		self.unknown3 = 0

		self.textureLayout = 4  # A COMPLETE GUESS
		self.arrayCount = 1
	
	def convert(self):
		textureData = self.extracted

		blockHeightLog2 = self.textureLayout & 7
		texture = compressImageData(self, textureData, 0, 0, 0, blockHeightLog2, 1)
		print(f"Loaded texture {self.identifier} ({self._format})")

		if self._format.startswith("ASTC"): # Texture is ASTC
			formatInfo = returnFormatTable(self._format)
			outBuffer = b''.join([
						b'\x13\xAB\xA1\x5C', formatInfo[1].to_bytes(1, "little"),
						formatInfo[2].to_bytes(1, "little"), b'\0',
						self.width.to_bytes(3, "little"),
						self.height.to_bytes(3, "little"), b'\1\0\0',
						texture,
					])
			return outBuffer, True
		

file = open(sys.argv[1], "rb")
if (file.read(4) != b'\x13\xAB\xA1\x5C'):
	print('WRONG MAGIC!')
	sys.exit()
if (file.read(3) != b"\4\4\1"):
	print("Unsupported ASTC format! Only supported one is 4x4!")
	sys.exit()
width = int.from_bytes(file.read(3), "little")
height = int.from_bytes(file.read(3), "little")
depth = int.from_bytes(file.read(3), "little")

if (depth > 1):
	print("Tool doesn't support 3D Textures!")
	sys.exit()

file.seek(0, 2)
size = file.tell() - 0x10
file.seek(0x10, 0)
new_file = open("output.astc", "wb")
new_file.write(NieRSwitchTexture(file.read(), width, height, size).convert()[0][0x10:])
new_file.close()
file.close()
