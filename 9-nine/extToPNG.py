import gzip
import sys
from PIL import Image
from pathlib import Path
import numpy

if (Path(sys.argv[1]).suffix == ".gz"):
    file = gzip.open(sys.argv[1])
else:
    file = open(sys.argv[1], "rb")

if (file.read(4) != b"EXT0"):
    print("WRONG MAGIC!")
    sys.exit()

file.seek(8, 1)

real_texture_width = int.from_bytes(file.read(4), "little", signed=False)
real_texture_height = int.from_bytes(file.read(4), "little", signed=False)
texture_width = int.from_bytes(file.read(4), "little", signed=False)
texture_height = int.from_bytes(file.read(4), "little", signed=False)

file.seek(8, 1)

BPP = int.from_bytes(file.read(4), "little", signed=False)
if (BPP not in [32, 8]):
    print("Unsupported BPP: %d" % BPP)
    sys.exit()

file.seek(0x100)

if (BPP == 32):
    img = Image.frombuffer("RGBA", (real_texture_width, real_texture_height), file.read(), "raw", "BGRA", 0, 1)
else:
    pallette = numpy.fromfile(file, dtype=numpy.uint32, count=256)
    buffer = []
    temp = numpy.fromfile(file, dtype=numpy.uint8, count=(real_texture_width * real_texture_height))
    for i in range(real_texture_width * real_texture_height):
        buffer.append(pallette[temp[i]])
    img = Image.frombuffer("RGBA", (real_texture_width, real_texture_height), b"".join(buffer), "raw", "BGRA", 0, 1)
img.save("%s.png" % Path(sys.argv[1]).stem)
