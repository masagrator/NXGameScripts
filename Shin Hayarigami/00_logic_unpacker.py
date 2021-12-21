import os
import numpy
import sys

file = open("database\\00_logic.dat", "rb")

os.makedirs("00_logic", exist_ok=True)

file_count = int.from_bytes(file.read(0x4), byteorder="little")

Offsets = []
for i in range(0, file_count):
    buffer = numpy.fromfile(file, dtype=numpy.uint32, count=2)
    if (buffer[0] != i):
        print("Something is wrong with offset table. Aborting...")
        sys.exit()
    else:
        Offsets.append(buffer[1])

for i in range(0, len(Offsets)):
    file.seek(Offsets[i])
    new_file = open("00_logic\\%d.dat" % i, "wb")
    if (i < (len(Offsets) - 1)):
        new_file.write(file.read(Offsets[i+1] - Offsets[i]))
    else:
        new_file.write(file.read())
    new_file.close()