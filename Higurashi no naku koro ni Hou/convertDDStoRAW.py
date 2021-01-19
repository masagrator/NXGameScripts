import sys
import numpy

f = open(sys.argv[1], 'rb')

f.seek(0x80, 0)

Pixels = numpy.fromfile(f, dtype=numpy.uint32)

RAW = open("%s.raw" % (sys.argv[1][:-4]), "rb")

Pallette = numpy.fromfile(RAW, dtype=numpy.uint32, count=256)

transparent_index = 0

for i in range(0, len(Pallette)):
    if (Pallette[i] < 0x1000000):
        print("Transparent_index = %d" % (i))
        transparent_index = i
        break

output = open("new.raw", "wb")

output.write(Pallette)

number = 257

for i in range(0, len(Pixels)):
    for x in range(0, len(Pallette)):
        if (Pixels[i] == Pallette[x]): 
            number = x
            break
        elif (Pixels[i] < 0xFFFFFF):
            number = transparent_index
            break
    if (number < 257): 
        output.write(numpy.uint8(number))
        number = 257
    else: print("Wrong color. %x" % (Pixels[i]))

f.close()
RAW.close()
output.close()