import glob
import os
import sys
import numpy
from PIL import Image, ImageOps
import subprocess

files = glob.glob("*\*.dds.phyre")
PNGs = glob.glob("*\*.png.phyre")

files += PNGs
os.makedirs("UNPACKED", exist_ok=True)

for i in range(0, len(files)):
	print(files[i])
	file = open(files[i], "rb")
	dump = file.read()
	file.seek(0)

	offset = dump.find(b".dds")

	if (offset == -1):
		offset = dump.find(b".DDS")

	if (offset == -1):
		offset = dump.find(b".png")
	
	if (offset == -1):
		print("WRONG TYPE casted!")
		sys.exit()

	proper_offset = dump.find(b"PTexture2D", offset)

	proper_offset += 11

	del dump

	file.seek(proper_offset)

	type = file.read(0x4)
	if (type[0:3] == b"L8\x00"):
		print("Detected L8 texture. Ignoring...")
		continue
	type = type.decode("ASCII")
	if (type in ["ARGB", "RGBA"]):
		start_image = file.tell() + 0x2D
	elif (type in ["RGB5"]):
		start_image = file.tell() + 0x2E
	else:
		start_image = file.tell() + 0x2C

	offset += 3
	offset = offset & 0xFFF8
	offset += 0x17
	file.seek(offset)

	width = int.from_bytes(file.read(4), byteorder="little")
	height = int.from_bytes(file.read(4), byteorder="little")
	orig_height = height
	orig_width = width
	if (height < 64):
		height = 64
	elif (height % 0x10 != 0):
		height += 0x10 - (height % 0x10)
	if (width < 64):
		width = 64
	elif (width % 0x10 != 0):
		width += 0x10 - (width % 0x10)

	file.seek(0)
	header = file.read(start_image)

	match(type):
		case "DXT1":
			size = int((width * height) / 2)
			data = file.read(size)
			file.close()
			os.makedirs(os.path.dirname("UNPACKED/%s" % files[i]), exist_ok=True)
			file_new = open("UNPACKED/%s.ds" % files[i][:-11], "wb")
			file_new.write(data)
			file_new.close()
			print(subprocess.run(["RawtexCmd_PS4.exe", "UNPACKED/%s.ds" % files[i][:-11], "DXT1", "0", "%d" % width, "%d" % height], capture_output=True))
		case "DXT3":
			size = int(width * height)
			data = file.read(size)
			file.close()
			os.makedirs(os.path.dirname("UNPACKED/%s" % files[i]), exist_ok=True)
			file_new = open("UNPACKED/%s.ds" % files[i][:-11], "wb")
			file_new.write(data)
			file_new.close()
			print(subprocess.run(["RawtexCmd_PS4.exe", "UNPACKED/%s.ds" % files[i][:-11], "DXT3", "0", "%d" % width, "%d" % height], capture_output=True))
		case "DXT5":
			size = int(width * height)
			data = file.read(size)
			file.close()
			os.makedirs(os.path.dirname("UNPACKED/%s" % files[i]), exist_ok=True)
			file_new = open("UNPACKED/%s.ds" % files[i][:-11], "wb")
			file_new.write(data)
			file_new.close()
			print(subprocess.run(["RawtexCmd_PS4.exe", "UNPACKED/%s.ds" % files[i][:-11], "DXT5", "0", "%d" % width, "%d" % height], capture_output=True))
		case "RGBA":
			size = int(width * height * 4)
			data = file.read(size)
			file.close()
			os.makedirs(os.path.dirname("UNPACKED/%s" % files[i]), exist_ok=True)
			file_new = open("UNPACKED/%s.ds" % files[i][:-11], "wb")
			file_new.write(data)
			file_new.close()
			print(subprocess.run(["RawtexCmd_PS4.exe", "UNPACKED/%s.ds" % files[i][:-11], "28", "0", "%d" % width, "%d" % height], capture_output=True))
		case "RGB5":
			size = int(width * height * 2)
			data = file.read(size)
			file.close()
			os.makedirs(os.path.dirname("UNPACKED/%s" % files[i]), exist_ok=True)
			file_new = open("UNPACKED/%s.ds" % files[i][:-11], "wb")
			file_new.write(data)
			file_new.close()
			print("Width: %d" % width)
			print("Height: %d" % height)
			print("rawtexcmd_PS4 doesn't support RGB565 type.")
			print("Use now rawtex.exe to convert file UNPACKED/%s.ds" % files[i][:-11])
			print("Check PS4 Swizzle, uncheck autodetect size, set Offset to 0")
			print("and set dimensions provided above, set type to b5g6r5_unorm")
			print("Press ENTER after converting texture or write \"n\" to skip it..")
			if (input() == "n"):
				os.remove("UNPACKED/%s.ds" % files[i][:-11])
				continue
		case "ARGB":
			size = int(width * height * 4)
			data = file.read(size)
			file.close()
			os.makedirs(os.path.dirname("UNPACKED/%s" % files[i]), exist_ok=True)
			file_new = open("UNPACKED/%s.ds" % files[i][:-11], "wb")
			file_new.write(data)
			file_new.close()
			print("Width: %d" % width)
			print("Height: %d" % height)
			print("rawtexcmd_PS4 doesn't support ARGB8 type.")
			print("Use now rawtex.exe to convert file UNPACKED/%s.ds" % files[i][:-11])
			print("Check PS4 Swizzle, uncheck autodetect size, set Offset to 0")
			print("and set dimensions provided above, set type to b8g8r8a8_unorm")
			print("Press ENTER after converting texture or write \"n\" to skip it..")
			if (input() == "n"):
				os.remove("UNPACKED/%s.ds" % files[i][:-11])
				continue
		case _:
			print("%s not implemented" % type)
			sys.exit()
	header_file = open("UNPACKED/%s.header" % files[i][:-6], "wb")
	header_file.write(header)
	header_file.close()
	try:
		img_raw = Image.open("UNPACKED/%s.png" % files[i][:-11])
	except:
		img_raw = Image.open("UNPACKED/%s.dds" % files[i][:-11])
	img = img_raw.crop((0, 0, orig_width, orig_height))
	img = ImageOps.flip(img)
	img.save("UNPACKED/%s.png" % files[i][:-10], "PNG")
	img.close()
	try:
		os.remove("UNPACKED/%s.dds" % files[i][:-11])
	except:
		pass
	try:
		os.remove("UNPACKED/%s.png" % files[i][:-11])
	except:
		pass
	os.remove("UNPACKED/%s.ds" % files[i][:-11])
