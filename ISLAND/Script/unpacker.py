import sys
import numpy
import os

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("ascii"))
        chars.append(c)

try:
    os.mkdir("new")
except:
    pass

file = open(sys.argv[1], "rb")

header_size = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
if (header_size == 0x2000): raise ValueError("This script is dedicated only to script packages. Detected not correct one")

file_count = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
unk2_int32 = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
round_to = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
reserved0 = file.read(0x10)
flag0 = numpy.fromfile(file, dtype=numpy.int8, count=1)[0]
flag1 = numpy.fromfile(file, dtype=numpy.int8, count=1)[0]
flag2 = numpy.fromfile(file, dtype=numpy.int8, count=1)[0]
flag3 = numpy.fromfile(file, dtype=numpy.int8, count=1)[0]
offset_start_file_names = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]

file_table = {}
file_table['offset'] = []
file_table['size'] = []

for i in range(0, file_count):
    file_table['offset'].append(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]*4)
    file_table['size'].append(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0])

filename_table = []

for i in range(0, file_count):
    filename_table.append(readString(file))

chapter_names = open("chapternames.txt", "w", encoding="ascii")

for i in range(0, file_count):
    file.seek(file_table['offset'][i], 0)
    file_new = open("new\%s.dat" % (filename_table[i]), "wb")
    file_new.write(file.read(file_table['size'][i]))
    chapter_names.write("%s\n" % (filename_table[i]))
    file_new.close()