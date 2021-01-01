import numpy
import os

if (os.path.isdir("output") == False):
    os.makedirs("output")

text = open("Localizedint.lbf", "rb")

for i in range(0,99):
    size = numpy.fromfile(text, dtype=numpy.uint8, count=1)
    buffer = text.read((size[0] * 2)-2)
    output = open("output/%s" % (buffer.decode('utf-16')), "wb")
    offset = text.tell() + 2
    text.seek(offset, 0)
    size2 = numpy.fromfile(text, dtype=numpy.uint32, count=1)
    output.write(text.read(size2[0]))
    output.close()

text.close()