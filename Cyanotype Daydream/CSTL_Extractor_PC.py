import os
import sys
import json
import glob
from pathlib import Path

def GetSerializedInt(file):
	Int = 0
	while(True):
		value = int.from_bytes(file.read(1), "little")
		Int += value
		if (value != 255):
			return Int

def GetFileSize(file):
	pos = file.tell()
	file.seek(0, 2)
	size = file.tell()
	file.seek(pos)
	return size

def readCSTL(file):
	if (file.read(8) != b"CSTL\x00\x00\x00\x00"):
		print("UNKNOWN MAGIC!")
		sys.exit()
	language_count = GetSerializedInt(file)
	languages = []
	for x in range(language_count):
		string_size = GetSerializedInt(file)
		languages.append(file.read(string_size).decode("ascii"))
	string_count = GetSerializedInt(file)
	STRINGS = []
	for x in range(string_count):
		entry = {}
		for y in range(language_count):
			entry[languages[y]] = {}
			string_size = GetSerializedInt(file)
			if (string_size > 0):
				entry[languages[y]]["Name"] = file.read(string_size).decode("UTF-8")
			string_size = GetSerializedInt(file)
			entry[languages[y]]["String"] = file.read(string_size).decode("UTF-8")
		STRINGS.append(entry)
	file.close()
	return STRINGS
	

files = glob.glob(f"{sys.argv[1]}/*.cstl")

os.makedirs("Unpacked", exist_ok=True)

for i in range(len(files)):
	print(files[i])
	BLOB = readCSTL(open(files[i], "rb"))
	json_file = open("Unpacked/%s.json" % Path(files[i]).stem, "w", encoding="UTF-8")
	json.dump(BLOB, json_file, indent="\t", ensure_ascii=False)
	json_file.close()
