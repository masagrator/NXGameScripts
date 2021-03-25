# Dedicated only to DDS RGBA8 with header size 0x80 and <= 256 colors
# PIC cannot be bigger than 30 000 000 B, otherwise game won't show it.

import sys
import numpy
import os
import secrets

f = open(sys.argv[1], 'rb')

f.seek(0xC, 0)
height = numpy.fromfile(f, dtype=numpy.uint32, count=1)[0]
width = numpy.fromfile(f, dtype=numpy.uint32, count=1)[0]

f.seek(0x80, 0)

buffer = numpy.fromfile(f, dtype=numpy.uint32)

f.close()

Pallette = []

flag = 0

offset = 1

print(len(buffer))
for i in range(0, len(buffer)):
    if (i == 0): Pallette.append(numpy.uint32(buffer[i]))
    else:
        for x in range(0, len(Pallette)):
            if (buffer[i] == Pallette[x]): break
            elif (x == len(Pallette) - 1): Pallette.append(buffer[i])

if (len(Pallette) * 4 > 0x400): raise ValueError("Pallette too big")


write = open("temp.dat", "wb")
for i in range(0, len(Pallette)):
    write.write(Pallette[i])

if ((len(Pallette) * 4) < 0x400):
    print("Not complete pallette. Filling nulls")
    for i in range(0, (0x400 - (len(Pallette) * 4))):
        write.write(numpy.uint8(0x0))

for i in range(0, len(buffer)):
    for x in range(0, len(Pallette)):
        if (buffer[i] == Pallette[x]): 
            write.write(numpy.uint8(x))
            break
    
write.close()

temp = open("temp.dat", "rb")
temp.seek(0, 2)
temp_size = temp.tell()
temp.seek(0, 0)
buffer_temp = temp.read()
temp.close()
os.remove("temp.dat")

type = 3
mask = 0
transparent_mask = 1
random_ID = secrets.token_bytes(4)

output = open("output.pic", "wb")
output.write(b"PIC4")
output.write(numpy.uint32(2))
output.write(numpy.uint32(temp_size + 0x4C))
output.write(numpy.uint16(width/2))
output.write(numpy.uint16(height))
output.write(numpy.uint16(width))
output.write(numpy.uint16(height))
output.write(numpy.uint32(1))
output.write(numpy.uint32(1))
output.write(random_ID)
output.write(numpy.uint32(0))
output.write(numpy.uint32(0x2C))
output.write(numpy.uint32(temp_size + 0x20))
output.write(numpy.uint16(type))
output.write(numpy.uint16(mask))
output.write(numpy.uint16(transparent_mask))
output.write(numpy.uint16(2))
output.write(numpy.uint32(0))
output.write(numpy.uint16(width))
output.write(numpy.uint16(height))
output.write(numpy.uint64(0))
output.write(numpy.uint16(width))
output.write(numpy.uint16(height))
output.write(numpy.uint32(0))
output.write(buffer_temp)
