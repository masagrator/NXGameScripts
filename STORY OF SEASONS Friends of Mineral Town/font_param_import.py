# STORY OF SEASONS: Friends of Mineral Town font's character table data generator from *.tsv file (use font_param_extract.py to generate tsv example file)
# It generates file with filename based on `mainfile` string that adds "_new" to name
# Python 3 script
# Author: MasaGratoR @ 2020

import numpy
import platform

mainfile = 'SHORHB___param.bin'

paramnew = open("%s_new.bin" % (mainfile[:-4]), "wb")

with open("%s.tsv" % (mainfile), 'r', encoding='utf-16-le') as f:
    IDs = [line.split("\t", -1)[0] for line in f]
    f.seek(0,0)
    UTF16chars = [line.split("\t", -1)[2] for line in f]
    f.seek(0,0)
    posx = [line.split("\t", -1)[3] for line in f]
    f.seek(0,0)
    posy = [line.split("\t", -1)[4] for line in f]
    f.seek(0,0)
    width = [line.split("\t", -1)[5] for line in f]
    f.seek(0,0)
    height = [line.split("\t", -1)[6] for line in f]
    f.seek(0,0)
    unk1 = [line.split("\t", -1)[7] for line in f]
    f.seek(0,0)
    y_shift = [line.split("\t", -1)[8] for line in f]
    f.seek(0,0)
    right_margin = [line.split("\t", -1)[9].strip("\r\n").strip("\n") for line in f]
    f.close()

offset = 1
ID_count = len(IDs) - 3
ID_now = 0

for i in range (0, 0x10000):
    
    if (offset != len(IDs)):
        if (i == int(UTF16chars[offset], 16)): 
            paramnew.write(numpy.uint16(IDs[offset]))
            offset = offset + 1
        else: paramnew.write(b'\xFF\xFF')
    else: paramnew.write(b'\xFF\xFF')

for i in range (1, len(IDs)):
    if (int(UTF16chars[i], 16) == 0x0): 
        i = i + 1
        continue
    for x in range(1, len(IDs)):
        if (int(IDs[x]) == ID_now):
            paramnew.write(numpy.uint16(int(UTF16chars[x], 16)))
            paramnew.write(numpy.uint16(posx[x]))
            paramnew.write(numpy.uint16(posy[x]))
            paramnew.write(numpy.uint8(width[x]))
            paramnew.write(numpy.uint8(height[x]))
            paramnew.write(numpy.int8(unk1[x]))
            paramnew.write(numpy.uint8(y_shift[x]))
            paramnew.write(numpy.uint16(right_margin[x]))
            ID_now = ID_now + 1

paramnew.close()
