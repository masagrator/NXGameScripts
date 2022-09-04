import os 
import sys
from pathlib import Path

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("shift_jis_2004"))
		chars.append(c)

path = Path(sys.argv[1]).stem
os.makedirs(path, exist_ok=True)

file = open(sys.argv[1], "rb")

header_size = int.from_bytes(file.read(4), "little", signed=False)
file_count = int.from_bytes(file.read(4), "little", signed=False)
string_max_size = 0x40

table = []

for i in range(0, file_count):
    entry = {}
    ptr = file.tell()
    entry["filename"] = readString(file)
    file.seek(ptr+string_max_size)
    entry["file_size"] = int.from_bytes(file.read(4), "little", signed=False)
    entry["offset"] = int.from_bytes(file.read(4), "little", signed=False)
    table.append(entry)

for i in range(0, file_count):
    file.seek(table[i]["offset"])
    print("%s/%s" % (path, table[i]["filename"]))
    new_file = open("%s/%s" % (path, table[i]["filename"]), "wb")
    new_file.write(file.read(table[i]["file_size"]))
    new_file.close()

file.close()
