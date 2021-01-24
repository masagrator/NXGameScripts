# Requirements: DDS must be RGBA8 and not have more than 256 different colors.

import sys
import numpy

f = open(sys.argv[1], 'rb')

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

if (len(Pallette) > 0x400): raise ValueError("Pallette too big")


write = open("result_indexed.dat", "wb")
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
