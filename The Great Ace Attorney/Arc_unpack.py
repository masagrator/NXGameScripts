# Python 3
# First argument is a filename

import sys
import zlib
import numpy
import os
import json

header_factor = 0x8000
file_entry_size = 0x90
filename_max_size = 0x80

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("ascii"))
        chars.append(c)

file = open(sys.argv[1], "rb")

if (file.read(4) != b"ARC\x00"): 
    print("Wrong MAGIC!")
    input("Press ENTER")
    exit()

version = numpy.fromfile(file, dtype=numpy.uint16, count=1)[0]
if (version != 7):
    print("Wrong version!")
    input("Press ENTER")
    exit()

file_count = numpy.fromfile(file, dtype=numpy.uint16, count=1)[0]
Dict = {}
Dict['Main'] = []

for i in range(0, file_count):
    entry = {}
    offset = file.tell()
    entry['Filename'] = readString(file)
    file.seek(offset + filename_max_size, 0)
    entry['MAGIC'] = "%s" % (file.read(4))
    entry['compressed_size'] = int(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0])
    entry['uncompressed_size'] = int(numpy.uint32(numpy.fromfile(file, dtype=numpy.uint16, count=1)[0]))
    entry['uncompressed_size'] = entry['uncompressed_size'] + int(numpy.fromfile(file, dtype=numpy.uint8, count=1)[0] * 0x10000)
    entry['unk4'] = int(numpy.fromfile(file, dtype=numpy.uint8, count=1)[0])
    entry['file_offset'] = int(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0])
    Dict['Main'].append(entry)

for i in range(0, file_count):
    os.makedirs(os.path.dirname("%s\%s.dat" % (sys.argv[1][:-4], Dict['Main'][i]['Filename'])), exist_ok=True)
    file.seek(Dict['Main'][i]['file_offset'], 0)
    Data = file.read(Dict['Main'][i]['compressed_size'])
    decompressed_data = zlib.decompress(Data)
    if (len(decompressed_data) != Dict['Main'][i]['uncompressed_size']):
        print("Wrong uncompressed size!")
        input("Press ENTER")
        exit()
    file2 = open("%s\%s.%s" % (sys.argv[1][:-4], Dict['Main'][i]['Filename'], decompressed_data[0:3].decode("ascii")), "wb")
    file2.write(decompressed_data)
    file2.close()

file2 = open("%s\%s.json" % (sys.argv[1][:-4], sys.argv[1][:-4]), "w", encoding="UTF-8")
json.dump(Dict, file2, indent=4, ensure_ascii=False)
file2.close()
