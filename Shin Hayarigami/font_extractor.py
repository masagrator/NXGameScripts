import sys
import json
import numpy
import os

file = open(sys.argv[1], "rb")
os.makedirs(sys.argv[1][:-4], exist_ok=True)
buffer = numpy.fromfile(file, dtype=numpy.uint16, count=4)
texture_width = buffer[0]
texture_height = buffer[1]
block_width = buffer[2]
block_height = buffer[3]
file.seek(0x4, 1)
table_character_size = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
file.seek(8, 1)
character_count = numpy.fromfile(file, dtype=numpy.uint64, count=1)[0]
file.seek(8, 1)
DUMP = {}
for i in range(0, character_count):
    entry = {}
    entry["OFFSET"] = "0x%x" % file.tell()
    entry["ID"] = int(numpy.fromfile(file, dtype=numpy.uint64, count=1)[0])
    string = file.read(0x8)
    string = int.from_bytes(string, byteorder="little")
    if (string < 256): size = 1
    elif (string < 65536): size = 2
    else: size = 3
    string = string.to_bytes(size, byteorder="big")
    entry["CHARACTER"] = string.decode("UTF-8")
    buffer = numpy.fromfile(file, dtype=numpy.int8, count=2)
    entry["ANCHOR"] = int(buffer[0])
    entry["WIDTH"] = int(buffer[1])
    entry["UNK2"] = int(numpy.fromfile(file, dtype=numpy.int16, count=1)[0])
    buffer = numpy.fromfile(file, dtype=numpy.int8, count=2)
    entry["UNK3"] = int(buffer[0])
    entry["UNK4"] = int(buffer[1])
    file.seek(2, 1)
    DUMP["0x%x" % int.from_bytes(string, byteorder="big")] = entry
new_file = open("%s/index.json" % sys.argv[1][:-4], "w", encoding="UTF-8")
json.dump(DUMP, new_file, indent="\t", ensure_ascii=False)
new_file.close()

file.seek(4, 1)
texture_size = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
file.seek(8, 1)

new_file = open("%s/font_texture.nltx" % sys.argv[1][:-4], "wb")
new_file.write(file.read(texture_size))
