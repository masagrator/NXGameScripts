import zlib
import os
import json
import sys
from pathlib import Path
import png

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("shift_jis_2004"))
		chars.append(c)

def DecompressTable(file, font_name=None):
	if (font_name == None):
		font_name = Path(file.name).stem
	table_unc_size =  int.from_bytes(file.read(4), "little")
	table_com_size =  int.from_bytes(file.read(4), "little")

	table =  zlib.decompress(file.read(table_com_size))

	assert (len(table) == table_unc_size)
	return table

def ProcessOldType(file):
	offset1 = int.from_bytes(file.read(4), "little")
	offset2 = int.from_bytes(file.read(4), "little")    
	table = DecompressTable(file)

	tex_blob_offset = file.tell()

	FONT_TABLE = {}
	FONT_TABLE["NAME"] = Path(file.name).stem
	FONT_TABLE["DATA"] = []

	OFFSETS = []

	x1 = 0
	x2 = 2

	entries_count = int(len(table) / 12)
	for i in range(entries_count):
		entry = {}
		entry["X"] = int.from_bytes(table[x1:x2], "little")
		entry["Y"] = int.from_bytes(table[x1+2:x2+2], "little")
		entry["width"] = int.from_bytes(table[x1+4:x2+4], "little")
		entry["height"] = int.from_bytes(table[x1+6:x2+6], "little")
		FONT_TABLE["DATA"].append(entry)
		OFFSETS.append(int.from_bytes(table[x1+8:x2+10], "little"))
		x1 += 12
		x2 += 12

	os.makedirs(Path(sys.argv[1]).stem, exist_ok=True)

	file_fontTable = open(f"{Path(sys.argv[1]).stem}/index.json", "w", encoding="UTF-8")
	json.dump(FONT_TABLE, file_fontTable, indent="\t", ensure_ascii=False)
	file_fontTable.close()

	print(f"Extracting {len(OFFSETS)} glyphs...")
	for i in range(len(OFFSETS)):
		if (FONT_TABLE["DATA"][i]["height"] + FONT_TABLE["DATA"][i]["width"] == 0):
			continue
		file.seek(tex_blob_offset + OFFSETS[i])
		img = []
		for x in range(FONT_TABLE["DATA"][i]["height"]):
			entry = []
			for y in range(FONT_TABLE["DATA"][i]["width"]):
				color = file.read(1)[0]
				entry.append(color)
				entry.append(color)
				entry.append(color)
				entry.append(file.read(1)[0])
			img.append(entry)
		
		image = open("%s/%06d.png" % (Path(sys.argv[1]).stem, i), "wb")
		w = png.Writer(width=FONT_TABLE["DATA"][i]["width"], height=FONT_TABLE["DATA"][i]["height"], greyscale=False, alpha=True)
		w.write(image, img)
		image.close()
	print("Extracing finished!")

def ProcessNewType(file):
	if (file.read(2) != b"\1\0"):
		print("Unknown New Type version!")
		sys.exit()
	if (file.read(2) != b"\x03\x01"):
		print("UNSUPPORTED FLAGS!")
		sys.exit()

	font_name = readString(file)
	offset1 = int.from_bytes(file.read(4), "little")
	offset2 = int.from_bytes(file.read(4), "little")

	assert(file.read(4) == b"\0\xFF\xFF\0")
	file.seek(9, 1)
	table = DecompressTable(file)

	tex_blob_offset = file.tell()

	FONT_TABLE = {}
	FONT_TABLE["NAME"] = font_name
	FONT_TABLE["DATA"] = []

	OFFSETS = []

	x1 = 0
	x2 = 2

	entries_count = int(len(table) / 16)
	for i in range(entries_count):
		entry = {}
		entry["X"] = int.from_bytes(table[x1:x2], "little")
		entry["Y"] = int.from_bytes(table[x1+2:x2+2], "little")
		entry["width"] = int.from_bytes(table[x1+4:x2+4], "little")
		entry["height"] = int.from_bytes(table[x1+6:x2+6], "little")
		entry["ceil"] = int.from_bytes(table[x1+8:x2+8], "little")
		FONT_TABLE["DATA"].append(entry)
		OFFSETS.append(int.from_bytes(table[x1+12:x2+14], "little"))
		x1 += 16
		x2 += 16

	os.makedirs(Path(sys.argv[1]).stem, exist_ok=True)

	file_fontTable = open(f"{Path(sys.argv[1]).stem}/index.json", "w", encoding="UTF-8")
	json.dump(FONT_TABLE, file_fontTable, indent="\t", ensure_ascii=False)
	file_fontTable.close()

	print(f"Extracting {len(OFFSETS)} glyphs...")
	for i in range(len(OFFSETS)):
		if (FONT_TABLE["DATA"][i]["height"] + FONT_TABLE["DATA"][i]["width"] == 0):
			continue
		file.seek(tex_blob_offset + OFFSETS[i])
		img = []
		for x in range(FONT_TABLE["DATA"][i]["height"]):
			entry = []
			for y in range(FONT_TABLE["DATA"][i]["width"]):
				color = file.read(1)[0]
				entry.append(color)
				entry.append(color)
				entry.append(color)
				entry.append(file.read(1)[0])
			img.append(entry)
		
		image = open("%s/%06d.png" % (Path(sys.argv[1]).stem, i), "wb")
		w = png.Writer(width=FONT_TABLE["DATA"][i]["width"], height=FONT_TABLE["DATA"][i]["height"], greyscale=False, alpha=True)
		w.write(image, img)
		image.close()
	print("Extracing finished!")

file = open(sys.argv[1], "rb")
if (file.read(4) != b"FNT\0"):
	print("WRONG MAGIC!")
	sys.exit()

if (file.read(9) != b"DATA VER-"):
	file.seek(-9, 1)
	ProcessOldType(file)
else:
	ProcessNewType(file)