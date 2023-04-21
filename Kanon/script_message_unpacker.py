import json
import os
import sys
from enum import Enum

Dump = {}
Dump['Main'] = []

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("shift_jis_2004"))
		chars.append(c)

def readString16(myfile):
	chars = []
	while True:
		c = myfile.read(2)
		if c == b'\x00\x00':
			return str(b"".join(chars).decode("UTF-16-LE"))
		chars.append(c)

def taskDecompile(file, filesize):
	while (file.tell() < filesize):
		Dump["Main"].append(readString(file))


os.makedirs("%s/json" % os.path.basename(sys.argv[1])[:-4], exist_ok=True)
os.makedirs("%s/new" % os.path.basename(sys.argv[1])[:-4], exist_ok=True)

file = open(sys.argv[1], "rb")

header_size = int.from_bytes(file.read(4), "little")
if (header_size % 0x2000 == 0): raise ValueError("This script is dedicated only to script packages. Detected not correct one")

file_count = int.from_bytes(file.read(4), "little")
unk2_int32 = int.from_bytes(file.read(4), "little")
round_to = int.from_bytes(file.read(4), "little")
reserved0 = file.read(0x10)
flag0 = int.from_bytes(file.read(1), "little")
flag1 = int.from_bytes(file.read(1), "little")
flag2 = int.from_bytes(file.read(1), "little")
flag3 = int.from_bytes(file.read(1), "little")
offset_start_file_names = int.from_bytes(file.read(4), "little")

file_table = {}
file_table['offset'] = []
file_table['size'] = []

for i in range(0, file_count):
	file_table['offset'].append(int.from_bytes(file.read(4), "little")*4)
	file_table['size'].append(int.from_bytes(file.read(4), "little"))

Filenames = []

for i in range(0, file_count):
	Filenames.append(readString(file))

os.makedirs("%s" % os.path.basename(sys.argv[1])[:-4], exist_ok=True)

with open("%s/chapternames.json" % os.path.basename(sys.argv[1])[:-4], "w", encoding="UTF-8") as chapter_names:
	json.dump(Filenames, chapter_names, indent="\t", ensure_ascii=False)

for i in range(0, file_count):
	file.seek(file_table['offset'][i], 0)
	file_new = open("%s/new/%s.dat" % (os.path.basename(sys.argv[1])[:-4], Filenames[i]), "wb")
	file_new.write(file.read(file_table['size'][i]))
	file_new.close()

for i in range(0, len(Filenames)):
	print(Filenames[i])
	file = open("%s/new/%s.dat" % (os.path.basename(sys.argv[1])[:-4], Filenames[i]), "rb")
	if (Filenames[i] == "_varstr"):
		file.seek(0, 2)
		filesize = file.tell()
		file.seek(0)
		DUMP = []
		while (file.tell() < filesize):
			cmd_size = int.from_bytes(file.read(2), "little")
			CMD = int.from_bytes(file.read(1), "little")
			entry = {}
			match(CMD):
				case 0x1C:
					entry["TYPE"] = "VARSTR_SET"
					entry["SUBCMD"] = int.from_bytes(file.read(1), "little")
					entry["Args"] = file.read(4).hex()
					string_size = int.from_bytes(file.read(2), "little")
					if (string_size > 0):
						entry["String"] = file.read(string_size * 2).decode("UTF-16-LE")
						file.seek(2, 1)
					elif (string_size < 0):
						entry["String"] = file.read(string_size*-1).decode("UTF-8")
						file.seek(1, 1)
					DUMP.append(entry)
				case _:
					print("UNKNOWN _varstr command: 0x%x" % CMD)
					sys.exit()
		file.close()
		json_file = open("%s/json/%s.json" % (os.path.basename(sys.argv[1])[:-4], Filenames[i]), "w", encoding="UTF-8")
		json.dump(DUMP, json_file, indent="\t", ensure_ascii=False)
		json_file.close()
		continue

	strings_count = int.from_bytes(file.read(4), "little")
	offsets = []
	for x in range(strings_count):
		offsets.append(int.from_bytes(file.read(8), "little"))
	
	STRINGS = []
	for x in range(int(strings_count / 2)):
		entry = {}
		file.seek(offsets[x*2])
		strings_size = int.from_bytes(file.read(2), "little", signed=True)
		if (strings_size > 0):
			string1 = file.read(strings_size * 2).decode("UTF-16-LE")
		elif (strings_size < 0):
			string1 = file.read(strings_size*-1).decode("UTF-8")
		file.seek(offsets[(x*2)+1])
		strings_size = int.from_bytes(file.read(2), "little", signed=True)
		if (strings_size > 0):
			string2 = file.read(strings_size * 2).decode("UTF-16-LE")
		elif (strings_size < 0):
			string2 = file.read(strings_size*-1).decode("UTF-8")
		assert(string1 == string2) #WTF they are including each string twice?!
		y = 0
		if (string1[0:1] == "@"):
			y = 1
			array = []
			while(True):
				c = string1[y:y+1]
				if (c != "@"):
					array.append(c)
					y += 1
				else:
					entry["NAME"] = "".join(array)
					print(entry["NAME"])
					y += 1
					break
		entry["String"] = string1[y:]
		STRINGS.append(entry)
	file.close()
	json_file = open("%s/json/%s.json" % (os.path.basename(sys.argv[1])[:-4], Filenames[i]), "w", encoding="UTF-8")
	json.dump(STRINGS, json_file, indent="\t", ensure_ascii=False)
	json_file.close()