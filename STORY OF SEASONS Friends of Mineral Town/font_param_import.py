# STORY OF SEASONS: Friends of Mineral Town font's character table data generator from *.tsv file (use font_param_extract.py to generate tsv example file)
# It generates file with filename based on `mainfile` string that adds "_new" to name
# Python 3 script

import numpy
import platform

mainfile = 'FOT-UDMarugo_LargePro-B_param.bin'

paramnew = open("%s_new.bin" % (mainfile[:-4]), "wb")

with open("%s.tsv" % (mainfile), 'r', encoding='utf-16-le') as f:
    if (platform.system() == "Linux"):
        IDs = [line.replace("\r\n","\n").split("\t", -1)[0].strip("\n") for line in f]
        f.seek(0,0)
        UTF16chars = [line.replace("\r\n","\n").split("\t", -1)[2].strip("\n") for line in f]
        f.seek(0,0)
        posx = [line.replace("\r\n","\n").split("\t", -1)[3].strip("\n") for line in f]
        f.seek(0,0)
        posy = [line.replace("\r\n","\n").split("\t", -1)[4].strip("\n") for line in f]
        f.seek(0,0)
        width = [line.replace("\r\n","\n").split("\t", -1)[5].strip("\n") for line in f]
        f.seek(0,0)
        height = [line.replace("\r\n","\n").split("\t", -1)[6].strip("\n") for line in f]
        f.seek(0,0)
        unk1 = [line.replace("\r\n","\n").split("\t", -1)[7].strip("\n") for line in f]
        f.seek(0,0)
        unk2 = [line.replace("\r\n","\n").split("\t", -1)[8].strip("\n") for line in f]
        f.seek(0,0)
        unk3 = [line.replace("\r\n","\n").split("\t", -1)[9].strip("\n") for line in f]
        f.seek(0,0)
        unk4 = [line.replace("\r\n","\n").split("\t", -1)[10].strip("\n") for line in f]
    elif (platform.system() == "Windows"): 
        IDs = [line.split("\t", -1)[0].strip("\n") for line in f]
        f.seek(0,0)
        UTF16chars = [line.split("\t", -1)[2].strip("\n") for line in f]
        f.seek(0,0)
        posx = [line.split("\t", -1)[3].strip("\n") for line in f]
        f.seek(0,0)
        posy = [line.split("\t", -1)[4].strip("\n") for line in f]
        f.seek(0,0)
        width = [line.split("\t", -1)[5].strip("\n") for line in f]
        f.seek(0,0)
        height = [line.split("\t", -1)[6].strip("\n") for line in f]
        f.seek(0,0)
        unk1 = [line.split("\t", -1)[7].strip("\n") for line in f]
        f.seek(0,0)
        unk2 = [line.split("\t", -1)[8].strip("\n") for line in f]
        f.seek(0,0)
        unk3 = [line.split("\t", -1)[9].strip("\n") for line in f]
        f.seek(0,0)
        unk4 = [line.split("\t", -1)[10].strip("\n") for line in f]
    f.close()

offset = 1
line_count = len(IDs)

for i in range (0, 0x10000):
    
    if (offset != line_count):
        if (i == int(UTF16chars[offset], 16)): 
            paramnew.write(numpy.uint16(IDs[offset]))
            offset = offset + 1
        else: paramnew.write(b'\xFF\xFF')
    else: paramnew.write(b'\xFF\xFF')

offset = 1

for i in range (0, line_count-1):
    if (int(UTF16chars[offset], 16) == 0x0): 
        offset = offset + 1
        continue
    paramnew.write(numpy.uint16(int(UTF16chars[offset], 16)))
    paramnew.write(numpy.uint16(posx[offset]))
    paramnew.write(numpy.uint16(posy[offset]))
    paramnew.write(numpy.uint8(width[offset]))
    paramnew.write(numpy.uint8(height[offset]))
    paramnew.write(numpy.int8(unk1[offset]))
    paramnew.write(numpy.uint8(unk2[offset]))
    paramnew.write(numpy.uint8(unk3[offset]))
    paramnew.write(numpy.uint8(unk4[offset]))
    offset = offset + 1

paramnew.close()
