import sys
import numpy

f = open(sys.argv[1], 'rb')

Pallette = numpy.fromfile(f, dtype=numpy.uint32, count=256)

buffer = f.read()

output = open("%s.rgba" % (sys.argv[1][:-4]), "wb")

print(len(buffer))

for i in range(0, len(buffer)):
    output.write(Pallette[buffer[i]])

f.close()
output.close()