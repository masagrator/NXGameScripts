# Python 3
# First argument is a filename

import sys
import zlib
import numpy
import os

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
    entry['MAGIC'] = file.read(4)
    entry['compressed_size'] = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
    entry['uncompressed_size'] = numpy.uint32(numpy.fromfile(file, dtype=numpy.uint16, count=1)[0])
    entry['uncompressed_size'] = entry['uncompressed_size'] + (numpy.fromfile(file, dtype=numpy.uint8, count=1)[0] * 0x10000)
    entry['unk4'] = numpy.fromfile(file, dtype=numpy.uint8, count=1)[0]
    entry['file_offset'] = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
    Dict['Main'].append(entry)

for i in range(0, file_count):
    os.makedirs(os.path.dirname("unpacked\%s.dat" % (Dict['Main'][i]['Filename'])), exist_ok=True)
    file.seek(Dict['Main'][i]['file_offset'], 0)
    Data = file.read(Dict['Main'][i]['compressed_size'])
    decompressed_data = zlib.decompress(Data)
    if (len(decompressed_data) != Dict['Main'][i]['uncompressed_size']):
        print("Wrong uncompressed size!")
        input("Press ENTER")
        exit()
    file2 = open("unpacked\%s.%s" % (Dict['Main'][i]['Filename'], decompressed_data[0:3].decode("ascii")), "wb")
    file2.write(decompressed_data)
    file2.close()