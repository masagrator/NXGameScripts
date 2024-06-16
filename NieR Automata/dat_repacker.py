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

align = 256

file.seek(pointer_table)
for i in range(file_count):
    pointers.append(int.from_bytes(file.read(4), "little"))
    if align == 256:
        if pointers[i] % 256 != 0:
            align = 16

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

new_file = open("%s/%s" % (Path(sys.argv[1]).stem, sys.argv[1]), "wb")
file.seek(0)
new_file.write(file.read(pointers[0]))
pos = new_file.tell()
if (pos < 0x200):
    new_file.write(b"\x00" * (0x200 - pos))

for i in range(file_count):
    print(names[i])
    try:
        temp = open("%s/%s" % (Path(sys.argv[1]).stem, names[i]), "rb")
    except:
        print("Not detected file, ignoring...")
        pos = new_file.tell()
        file.seek(pointers[i])
        new_file.write(file.read(sizes[i]))
        if (new_file.tell() % align != 0):
            new_file.write(b"\x00" * (align - (new_file.tell() % align)))
        new_file.seek(pointer_table + (4 * i))
        new_file.write(pos.to_bytes(4, "little"))
        new_file.seek(0, 2)
        continue
    pos = new_file.tell()
    new_file.write(temp.read())
    if (new_file.tell() % align != 0):
        new_file.write(b"\x00" * (align - (new_file.tell() % align)))
    new_file.seek(pointer_table + (4 * i))
    new_file.write(pos.to_bytes(4, "little"))
    new_file.seek(sizes_table + (4 * i))
    new_file.write(temp.tell().to_bytes(4, "little"))
    new_file.seek(0, 2)
    temp.close()
new_file.close()
