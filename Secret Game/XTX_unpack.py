import sys
from PIL import Image
import astc_decomp

file = open(sys.argv[1], "rb")
header_size = int.from_bytes(file.read(4), "little")
file_size = int.from_bytes(file.read(4), "little")
file.seek(header_size)

if (file.read(4) != b"xtx\x00"):
    print("WRONG MAGIC!")
    sys.exit()

format_type = int.from_bytes(file.read(4), "little")
aligned_width = int.from_bytes(file.read(4), "big")
aligned_height = int.from_bytes(file.read(4), "big")
width = int.from_bytes(file.read(4), "big")
height = int.from_bytes(file.read(4), "big")
pos_x = int.from_bytes(file.read(4), "big")
pos_y = int.from_bytes(file.read(4), "big")

if (format_type != 9):
    print("UNKNOWN format_type!")
    sys.exit()

astc_data = file.read()
file.close()
block_width = 4
block_height = 4
is_srgb : bool = False

img = Image.frombytes('RGBA', (width, height), astc_data, 'astc', (block_width, block_height, is_srgb))
img.save(sys.argv[2])