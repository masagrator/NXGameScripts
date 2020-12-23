# Python 3 script

import numpy

text = open("extract.txt", "w", encoding='utf-16')
og = open("patch.dat", "rb")

text_offset = 0x410B6C
table_offset = 0x3C2B20

og.seek(table_offset, 0)

table_array = numpy.fromfile(og, dtype=numpy.uint32, count=0x13813)

exception = 0
exception2 = 0
exceptionoffset = 0

for i in range(0, 0x9C09):
    relative_offset = table_array[i*2]
    hard_offset = text_offset + relative_offset
    size = table_array[i*2+1]
    og.seek(hard_offset, 0)
    text.write(og.read(size).decode('utf-16'))
    text.write("\n\n>-NEW LINE-<\n\n")

text.close()
