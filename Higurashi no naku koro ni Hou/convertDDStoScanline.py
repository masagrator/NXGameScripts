# Requirements: DDS must be RGBA8 and header must have size 0x80

import sys
import numpy

def adjust_scanline(data, w, scanlines):
    scanlines_size = scanlines * 4
    for i in range(0, scanlines):
        block_scanline.append(numpy.uint8(0xFF))
        block_scanline.append(numpy.uint8(0xFF))
        block_scanline.append(numpy.uint8(0xFF))
        block_scanline.append(numpy.uint8(0x0))

    for i in range(scanlines_size, len(data)):
        block_scanline.append(numpy.uint8(data[i]))
    
    for i in range(scanlines_size, len(data)):   
        temp = numpy.uint8((numpy.int16(block_scanline[i]) - numpy.int16(block_scanline[i - scanlines_size])) % 256)
        new.append(numpy.uint8(temp))

f = open(sys.argv[1], 'rb')

f.seek(0x10, 0)
width = numpy.fromfile(f, dtype=numpy.uint32, count=1)[0]
f.seek(0x80, 0)
buffer = bytearray(f.read())
f.close()

scanlines = (((width)+3)&0xfffc)
new = []
block_scanline = []

adjust_scanline(buffer, width, scanlines)

f = open("output.raw", 'wb')
for i in range(0, scanlines*4):
    f.write(block_scanline[i])

for i in range(0, len(new)):
    f.write(numpy.uint8(new[i]))
f.close()