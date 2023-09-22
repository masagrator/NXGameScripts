import sys
import os
from pathlib import Path
import puyo_lz01

file = open(sys.argv[1], "rb")
DecompressedSize = int.from_bytes(file.read(4), "little")
CompressedData = file.read()
file.close()

DecompressedData = puyo_lz01.Decompress(CompressedData, DecompressedSize)
os.makedirs("Decompressed", exist_ok=True)
new_file = open("Decompressed/%s" % Path(sys.argv[1]).name, "wb")
new_file.write(DecompressedData)
new_file.close()