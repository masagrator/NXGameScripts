# Provide folder created with Coalesced_unpacker.py as argument, it will create a .bin file with the same name in "new" folder
# example: python Coalesced_packer.py COALESCED_INT

import sys
import os
import json

with open(f"{sys.argv[1]}/fileorder.json", "r", encoding="UTF-8") as file:
	files = json.load(file)

DUMP = [len(files).to_bytes(4, "little")]

for i in range(len(files)):
	null_terminator = 1
	try:
		string = files[i].encode("iso-8859-1")
	except:
		string = files[i].encode("UTF-16-LE")
		null_terminator = -2
	string_len = int(len(string) / null_terminator) + 1
	DUMP.append(string_len.to_bytes(4, "little", signed=True))
	DUMP.append(string)
	DUMP.append(b"\x00" * abs(null_terminator))
	filepath = files[i]
	while (filepath[:3] in ["../", "..\\"]):
		filepath = filepath[3:]
	file = open("%s/%s.json" % (sys.argv[1], filepath), "r", encoding="UTF-8")
	config = json.load(file)
	file.close()
	DUMP.append(len(config.keys()).to_bytes(4, "little"))
	sections = list(config.keys())
	for x in range(len(sections)):
		null_terminator = 1
		try:
			string = sections[x].encode("iso-8859-1")
		except:
			string = sections[x].encode("UTF-16-LE")
			null_terminator = -2
		string_len = 1
		for i in range(0, len(string), abs(null_terminator)):
			string_len += 1
		if (null_terminator == -2):
			string_len = ~string_len + 1
		DUMP.append(string_len.to_bytes(4, "little", signed=True))
		DUMP.append(string)
		DUMP.append(b"\x00" * abs(null_terminator))
		pairs_count = len(config[sections[x]])
		DUMP.append(pairs_count.to_bytes(4, "little"))	
		for entry in config[sections[x]]:
			null_terminator = 1
			try:
				string = entry["key"].encode("iso-8859-1")
			except:
				string = entry["key"].encode("UTF-16-LE")
				null_terminator = -2
			key_len = 1
			for i in range(0, len(string), abs(null_terminator)):
				key_len += 1
			if (null_terminator == -2):
				key_len = ~key_len + 1
			DUMP.append(key_len.to_bytes(4, "little", signed=True))
			DUMP.append(string)
			DUMP.append(b"\x00" * abs(null_terminator))
			null_terminator = 1
			try:
				string = entry["value"].encode("iso-8859-1")
			except:
				string = entry["value"].encode("UTF-16-LE")
				null_terminator = -2
			value_len = 1
			for i in range(0, len(string), abs(null_terminator)):
				value_len += 1	
			if (value_len == 1):
				value_len = 0
				null_terminator = 0
			if (null_terminator == -2):
				value_len = ~value_len + 1
			DUMP.append(value_len.to_bytes(4, "little", signed=True))
			DUMP.append(string)
			DUMP.append(b"\x00" * abs(null_terminator))			


os.makedirs("new", exist_ok=True)
new_file = open("new/%s.bin" % (sys.argv[1]), "wb")
new_file.write(b"".join(DUMP))
new_file.close()