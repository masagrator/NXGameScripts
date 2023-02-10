# It requires *.mrg, *.nam and *.hed
# As argument provide filename without any type

import zlib
import sys
import os
from pathlib import Path

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("UTF-8"))
		chars.append(c)

file = open(f"{sys.argv[1]}.nam", "rb")
offset = 0
FILENAMES = []

while(True):
	file.seek(offset)
	string = readString(file)
	if (string != ""):
		FILENAMES.append(string)
		offset += 32
	else:
		break

file.close()

file = open(f"{sys.argv[1]}.hed", "rb")
offset = 0
HEADER = []

for i in range(len(FILENAMES)):
	entry = {}
	entry["offset"] = int.from_bytes(file.read(4), "little") * 0x800
	entry["com_size"] = int.from_bytes(file.read(2), "little") * 0x800
	entry["dec_size"] = int.from_bytes(file.read(2), "little") * 0x800 #This is rounded to 0x800, so don't use it for asserts
	HEADER.append(entry)

file.close()

file = open(f"{sys.argv[1]}.mrg", "rb")
os.makedirs(f"{sys.argv[1]}/Decompressed", exist_ok=True)

for i in range(len(FILENAMES)):
	print(FILENAMES[i])
	file.seek(HEADER[i]["offset"])
	new_file = open(f"{sys.argv[1]}/{FILENAMES[i]}", "wb")
	BLOB = file.read(HEADER[i]["com_size"])
	new_file.write(BLOB)
	new_file.close()
	filetype = BLOB[:4].decode("ascii")
	if (HEADER[i]["com_size"] != HEADER[i]["dec_size"] and filetype == "NXCX"):
		DATA = zlib.decompress(BLOB[16:])
		filetype = DATA[:4].decode("ascii")
		print(f"Decompressed to {Path(FILENAMES[i]).stem}.{filetype}")
		try:
			assert(len(DATA) == int.from_bytes(BLOB[4:8], "little"))
		except:
			print("Size didn't match!")
			print("Expected: %dB, got: %dB" % (int.from_bytes(BLOB[4:8], "little"), len(DATA)))
		new_file = open(f"{sys.argv[1]}/Decompressed/{Path(FILENAMES[i]).stem}.{filetype}", "wb")
		new_file.write(DATA)
		new_file.close()
