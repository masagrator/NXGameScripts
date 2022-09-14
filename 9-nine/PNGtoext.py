import gzip
import sys
from PIL import Image
from pathlib import Path

file = open(sys.argv[1], "rb")

if (file.read(4) != b"\x89PNG"):
    print("WRONG MAGIC!")
    sys.exit()

file.close()

image = Image.open(sys.argv[1])
buffer = image.convert("RGBA").tobytes('raw', 'BGRA', 0, 1)

temp = open("backup.ext", "rb")
header = temp.read(0x100)
temp.close()

file = open("%s.ext" % Path(sys.argv[1]).stem, "wb")
file.write(header)
file.write(buffer)
file.close()

file = gzip.open("%s.ext.gz" % Path(sys.argv[1]).stem, "wb")
file.write(header+buffer)
file.close()