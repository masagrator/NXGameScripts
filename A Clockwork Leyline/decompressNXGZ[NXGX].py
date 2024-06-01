import sys
from pathlib import Path
import os
import zlib

file = open(sys.argv[1], "rb")
if (file.read(4) != b"NXGX"):
    print("WRONG MAGIC!")
    file.close()
    sys.exit()
unc_size = int.from_bytes(file.read(4), "little")
size = int.from_bytes(file.read(4), "little")
padding = int.from_bytes(file.read(4), "little")
obj = zlib.decompressobj(31)
data = obj.decompress(file.read(size))
file.close()

assert(len(data) == unc_size)

if data[0:4] in [b"BNTX"]:
    print(os.path.dirname(os.path.abspath(sys.argv[1])) + os.path.sep + Path(sys.argv[1]).stem + "." + data[0:4].decode("ascii").lower())
    new_file = open(os.path.dirname(os.path.abspath(sys.argv[1])) + os.path.sep + Path(sys.argv[1]).stem + "." + data[0:4].decode("ascii").lower(), "wb")
else:
    new_file = open(sys.argv[1] + ".unc", "wb")
new_file.write(data)
new_file.close()