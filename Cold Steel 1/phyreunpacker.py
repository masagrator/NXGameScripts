import glob
import os
import sys
import numpy
from PIL import Image, ImageOps

files = glob.glob("*\*.dds.phyre")
os.makedirs("UNPACKED", exist_ok=True)

DXT1 = b"\x44\x44\x53\x20\x7C\x00\x00\x00\x07\x10\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x00\x00\x00\x04\x00\x00\x00\x44\x58\x54\x31\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
DXT5 = b"\x44\x44\x53\x20\x7C\x00\x00\x00\x07\x10\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x00\x00\x00\x04\x00\x00\x00\x44\x58\x54\x35\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

for i in range(0, len(files)):
	print(files[i])
	file = open(files[i], "rb")
	dump = file.read()
	file.seek(0)

	offset = dump.find(b".dds")

	proper_offset = dump.find(b"PTexture2D", offset)

	proper_offset += 11

	start_image = dump.find(b"\x02\x08\x01\x00", proper_offset)

	del dump

	file.seek(proper_offset)

	type = file.read(0x4).decode("ASCII")

	file.seek(-28, 1)

	height = int.from_bytes(file.read(4), byteorder="little")
	width = int.from_bytes(file.read(4), byteorder="little")

	file.seek(0)
	header = file.read(start_image + 4)

	match(type):
		case "DXT1":
			size = int((width * height) / 2)
			data = file.read(size)
			file.close()
			os.makedirs(os.path.dirname("UNPACKED/%s" % files[i]), exist_ok=True)
			file_new = open("UNPACKED/%s" % files[i][:-6], "wb")
			file_new.write(DXT1)
		case "DXT5":
			size = int(width * height)
			data = file.read(size)
			file.close()
			os.makedirs(os.path.dirname("UNPACKED/%s" % files[i]), exist_ok=True)
			file_new = open("UNPACKED/%s" % files[i][:-6], "wb")
			file_new.write(DXT5)
		case _:
			print("%s not implemented" % type)
			sys.exit()
	
	file_new.write(data)
	file_new.seek(0xC)
	file_new.write(numpy.uint32(width))
	file_new.write(numpy.uint32(height))
	file_new.close()
	header_file = open("UNPACKED/%s.header" % files[i][:-6], "wb")
	header_file.write(header)
	header_file.close()
	img_raw = Image.open("UNPACKED/%s" % files[i][:-6])
	img = ImageOps.flip(img_raw)
	img.save("UNPACKED/%s.png" % files[i][:-10], "PNG")
	img.close()
	os.remove("UNPACKED/%s" % files[i][:-6])
