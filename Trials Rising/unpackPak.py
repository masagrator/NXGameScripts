import zlib
import sys
import os
from pathlib import Path

file = open(sys.argv[1], "rb")
if (int.from_bytes(file.read(4), "little") != 0x12345678):
	print("Unsupported PAK file!")
	sys.exit()

header_size = int.from_bytes(file.read(4), "little")
file_count = int.from_bytes(file.read(4), "little")

DUMP = []
for i in range(file_count):
	entry = {}
	entry["hash"] = int.from_bytes(file.read(4), "little")
	entry["com_size"] = int.from_bytes(file.read(4), "little")
	entry["unc_size"] = int.from_bytes(file.read(4), "little")
	entry["flag"] = int.from_bytes(file.read(1), "little")
	entry["offset"] = int.from_bytes(file.read(4), "little")
	DUMP.append(entry)

if DUMP[-1]["flag"] != 0:
	print("Unexpected data! 1")
	sys.exit()

Filenames = []

file.seek(DUMP[-1]["offset"])
file.seek(4, 1)
for i in range(file_count - 1):
	length = int.from_bytes(file.read(2), "little")
	Filenames.append(file.read(length).decode("UTF-8"))

print(Filenames)

os.makedirs(Path(sys.argv[1]).stem, exist_ok=True)
for i in range(file_count - 1):
	file.seek(DUMP[i]["offset"])
	if (DUMP[i]["flag"] == 1):
		dump = zlib.decompress(file.read(DUMP[i]["com_size"]))
	elif (DUMP[i]["flag"] == 0):
		assert(DUMP[i]["com_size"] == DUMP[i]["unc_size"])
		dump = file.read(DUMP[i]["unc_size"])
	assert(len(dump) == DUMP[i]["unc_size"])
	os.makedirs(os.path.dirname(os.path.normpath(f"{Path(sys.argv[1]).stem}/{Filenames[i]}")), exist_ok=True)
	new_file = open(os.path.normpath(f"{Path(sys.argv[1]).stem}/{Filenames[i]}"), "wb")
	new_file.write(dump)
	new_file.close()

file.close()