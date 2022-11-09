import sys
import os
from pathlib import Path

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("ascii"))
		chars.append(c)

file = open(sys.argv[1], "rb")

if (file.read(4) != b"DAT\x00"):
    print("WRONG MAGIC!")
    sys.exit()

file_count = int.from_bytes(file.read(4), "little")
pointer_table = int.from_bytes(file.read(4), "little")
formats_table = int.from_bytes(file.read(4), "little")
names_table = int.from_bytes(file.read(4), "little")
sizes_table = int.from_bytes(file.read(4), "little")
name_hashes_table = int.from_bytes(file.read(4), "little")

pointers = []
sizes = []
names = []

file.seek(pointer_table)
for i in range(file_count):
    pointers.append(int.from_bytes(file.read(4), "little"))

file.seek(sizes_table)
for i in range(file_count):
    sizes.append(int.from_bytes(file.read(4), "little"))

file.seek(names_table)
string_size_check = int.from_bytes(file.read(4), "little")
print("0x%x" % file.tell())
pos = file.tell()
for i in range(file_count):
    file.seek(pos + (string_size_check * i))
    names.append(readString(file))

os.makedirs(Path(sys.argv[1]).stem, exist_ok=True)
for i in range(file_count):
    file.seek(pointers[i])
    new_file = open("%s/%s" % (Path(sys.argv[1]).stem, names[i]), "wb")
    new_file.write(file.read(sizes[i]))
    new_file.close()
