#Script to unpack texts from str.bytes that you can find inside file "str" in "Data\StreamingAssets\scratchpad"

import json
import sys

def readString(myfile, size_check = None):
	chars = []
	while True:
		if (size_check != None) and (size_check == len(chars)):
			c = myfile.read(1)
			return str(b"".join(chars).decode("shift_jis_2004"))
		c = myfile.read(1)
		if c == b'\x00':
			if (size_check != None) and (size_check != len(chars)):
				print("string size check failed!")
				sys.exit()
			return str(b"".join(chars).decode("shift_jis_2004"))
		chars.append(c)

with open(sys.argv[1], "rb") as file:
	magic_size = int.from_bytes(file.read(4), "little")
	if (magic_size != 3):
		print("Wrong magic size!")
		sys.exit()
	MAGIC = readString(file)
	if MAGIC != "str":
		print("Wrong MAGIC")
		sys.exit()
	data_size = int.from_bytes(file.read(4), "little")
	pos = file.tell()
	file.seek(0, 2)
	size = file.tell()
	file.seek(pos)
	if (size - pos) != data_size:
		print("Wrong file size!")
		sys.exit()
	strings_count = int.from_bytes(file.read(2), "big")
	file.seek(1,1)
	DUMP = []
	for i in range(strings_count):
		string_size_check = int.from_bytes(file.read(1), "little")
		DUMP.append(readString(file, string_size_check))

with open("str.json", "w", encoding="UTF-8") as json_file:
	json.dump(DUMP, json_file, indent="\t", ensure_ascii=False)
	
