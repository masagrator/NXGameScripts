import os
import numpy

file = open("story.dat", "rb")

buffer = numpy.fromfile(file, dtype=numpy.uint32, count=2)
header_size = buffer[0]
table_entries = buffer[1]

offsets = []
IDs = []
for i in range(0, table_entries):
    buffer = numpy.fromfile(file, dtype=numpy.uint32, count=2)
    offsets.append(buffer[1])
    IDs.append(buffer[0])

os.makedirs("extracted", exist_ok=True)

for i in range(0, table_entries):
    new_file = open("extracted\%s.dat" % IDs[i], "wb")
    file.seek(offsets[i])
    if (i != table_entries - 1):
        new_file.write(file.read(offsets[i+1]-offsets[i]))
    else:
        new_file.write(file.read())
    new_file.close()