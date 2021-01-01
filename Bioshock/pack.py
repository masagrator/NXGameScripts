import numpy
import platform

with open("dir.txt", 'r') as f:
    if (platform.system() == "Linux"):
        filenames = [line.replace("\r\n","\n").split("\n", -1)[0].strip("\n") for line in f]
    elif (platform.system() == "Windows"): 
        filenames = [line.split("\r\n", -1)[0].strip("\r\n") for line in f]
    f.close()

output = open("output.lbf", "wb")

for i in range(0, 101):
    size1 = len(filenames[i])
    text = open("output/%s" % (filenames[i]), 'rb')
    text.seek(0, 2)
    size2 = text.tell()
    text.seek(0, 0)
    buffer = text.read()
    text.close()
    output.write(numpy.uint8(size1+1))
    output.write(filenames[i].encode('utf-16')[2:])
    output.write(numpy.uint16(0x0))
    output.write(numpy.uint32(size2))
    output.write(buffer)
    
output.close()
