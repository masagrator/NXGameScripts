import os
import sys

file = open(sys.argv[1], "rb")

os.makedirs("logic1", exist_ok=True)

file_count = int.from_bytes(file.read(0x4), byteorder="little")

Offsets = []
IDs = []
last = 1

for i in range(0, file_count):
    IDs.append(int.from_bytes(file.read(4), "little"))
    Offsets.append(int.from_bytes(file.read(4), "little"))

for i in range(0, len(Offsets)):
    file.seek(Offsets[i])
    new_file = open("logic1\\%04d.dat" % IDs[i], "wb")
    if (i < (len(Offsets) - 1)):
        new_file.write(file.read(Offsets[i+1] - Offsets[i]))
    else:
        new_file.write(file.read())
    new_file.close()