import os
import shutil
import numpy
import platform

mainfile = "dlc.dlc9.big.nx"

cases = open(mainfile, "rb")

with open("%s.offsets.txt" % (mainfile), 'r') as f:
    if (platform.system() == "Linux"):
        filenames = [line.replace("\r\n","\n").replace(".nx :  ",".nx/").replace(" :  :  "," : ").replace(" : "," :  :  ").split(" :  :  ", -1)[1].strip("\n") for line in f]
    elif (platform.system() == "Windows"): 
        filenames = [line.replace(".nx :  ",".nx/").replace(" :  :  "," : ").replace(" : "," :  :  ").split(" :  :  ", -1)[1].strip("\n") for line in f]
    f.close()

cases.seek(-4, 2)
table_offset = numpy.fromfile(cases, dtype=numpy.uint32, count=1)
table_offset = table_offset[0]
file_offset = table_offset - 0xC
size_offset = table_offset - 0x10

for i in range(0,len(filenames)):
    directory = os.path.dirname(filenames[i])
    if (os.path.exists(directory) == False):
        os.makedirs(directory)
    chunk = open(filenames[i], "wb")
    cases.seek(-size_offset, 2)
    size = numpy.fromfile(cases, dtype=numpy.uint32, count=1)
    cases.seek(-size_offset+4, 2)
    sizeraw = numpy.fromfile(cases, dtype=numpy.uint32, count=1)
    cases.seek(-file_offset, 2)
    offset = numpy.fromfile(cases, dtype=numpy.uint32, count=1)
    offset[0] = offset[0] * 0x10
    cases.seek(offset[0])
    chunk.write(cases.read(size[0]))
    if (sizeraw[0] != 0):
        raw = open("%s.raw" % (filenames[i]), "wb")
        raw.write(cases.read(sizeraw[0]))
        raw.close()
        print("Filename: %s, offset: 0x%x, size: %d + RAW size: %d" % (filenames[i], offset[0], size[0], sizeraw[0]))
    else:
        print("Filename: %s, offset: 0x%x, size: %d" % (filenames[i], offset[0], size[0]))
    chunk.close()
    file_offset = file_offset - 0x14
    size_offset = size_offset - 0x14

cases.close()
