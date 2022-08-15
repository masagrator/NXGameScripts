import gzip
import sys
from PIL import Image
from pathlib import Path

file = gzip.open(sys.argv[1])

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
if (BPP != 32):
    print("Unsupported BPP: %d" % BPP)
    sys.exit()

file.seek(0x100)

img = Image.frombuffer("RGBA", (real_texture_width, real_texture_height), file.read(), "raw", "BGRA", 0, 1)
img.save("%s.png" % Path(sys.argv[1]).stem)
