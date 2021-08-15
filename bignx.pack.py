import os
import shutil
import numpy
import platform

mainfile = "dlc.dlc9.big.nx"

if (os.path.isdir("output") == False):
    os.makedirs("output")
cases = open("output/%s" % (mainfile), "wb")

with open("%s.offsets.txt" % (mainfile), 'r') as f:
    if (platform.system() == "Linux"):
        filenames = [line.replace("\r\n","\n").replace(".nx :  ",".nx/").replace(" :  :  "," : ").replace(" : "," :  :  ").split(" :  :  ", -1)[1].strip("\n") for line in f]
    elif (platform.system() == "Windows"): 
        filenames = [line.replace(".nx :  ",".nx/").replace(" :  :  "," : ").replace(" : "," :  :  ").split(" :  :  ", -1)[1].strip("\n") for line in f]
    f.close()

size = []
iterationraw = []
sizeraw = []
file_offset = []
iterationread = 0

for i in range(0,len(filenames)):
    chunk = open(filenames[i], "rb")
    if (os.path.isfile("%s.raw" % (filenames[i])) == True):
        raw = open("%s.raw" % (filenames[i]))
        iterationraw.append(i)
    else: iterationraw.append(0xFFFFFFFF)
    file_offset.append(cases.tell() / 0x10)
    cases.write(chunk.read())
    if (os.path.isfile("%s.raw" % (filenames[i])) == True):
        cases.write(raw.read())
        sizeraw.append(raw.tell())
    else: sizeraw.append(0xFFFFFFFF)
    size.append(chunk.tell())
    chunk.close()
    if (os.path.isfile("%s.raw" % (filenames[i])) == True):
        raw.close()
    offset = cases.tell()
    if (os.path.isfile("%s.raw" % (filenames[i])) == True):
        print("filename: %s, size: %s, offset: %s + RAW size: %d" % (filenames[i], size[i], file_offset[i], sizeraw[iterationread]))
        iterationread = iterationread + 1
    else: print("filename: %s, size: %s, offset: %s" % (filenames[i], size[i], file_offset[i]))
    if (i != len(filenames)-1):
        if (offset & 0xF != 0):
            offset = offset & 0xF
            for x in range(0, (0x10 - offset)):
                cases.write("X")

cases_org = open(mainfile, "rb")
cases_org.seek(-4, 2)
table_offset = numpy.fromfile(cases_org, dtype=numpy.uint32, count=1)
cases_org.seek(0,2)
filetable_offset = cases_org.tell() - table_offset[0]
cases_org.seek(filetable_offset, 0)
cases.write(cases_org.read())
cases_org.close()
cases.seek(0,2)
file_offset_og = cases.tell() - table_offset[0] + 0xC

iteration = 0

for x in range (0,len(filenames)):
    cases.seek(file_offset_og, 0)
    cases.write(numpy.uint32(file_offset[x]))
    cases.write(numpy.uint32(size[x]))
    if (iterationraw[x] != 0xFFFFFFFF):
        cases.write(numpy.uint32(sizeraw[x]))
    file_offset_og = file_offset_og + 0x14

cases.close()
