import sys
from PIL import Image
import astc_decomp
from pathlib import Path
import os

isFont = False

file = open(sys.argv[1], "rb")
if (file.name.find("font") != -1):
    isFont = True
if (file.read(4) != b"xtx\x00"):
    file.seek(0)
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

if (format_type not in [5, 9]):
    print("UNKNOWN format_type!")
    sys.exit()

data = file.read()
file.close()

match(format_type):
        # case 1
        # Secret Game executable doesn't support case 1, info was extracted from Root Double
    case 5:
        # BGRA4
        if (isFont == True):
            # Font stores each of 4 layers using one of BGRA channels
            new_data1 = []
            new_data2 = []
            new_data3 = []
            new_data4 = []
            for i in range(0, len(data), 2):
                R = (data[i] & 0b00001111) << 4
                new_data1.append(b"\x00" * 3)
                new_data1.append(R.to_bytes(1, "little"))
                G = data[i] & 0b11110000
                new_data2.append(b"\x00" * 3)
                new_data2.append(G.to_bytes(1, "little"))
                B = (data[i+1] & 0b00001111) << 4
                new_data3.append(b"\x00" * 3)
                new_data3.append(B.to_bytes(1, "little"))
                A = data[i+1] & 0b11110000
                new_data4.append(b"\x00" * 3)
                new_data4.append(A.to_bytes(1, "little"))
            img = Image.frombytes('RGBA', (width, height), b"".join(new_data1))
            img.save("0.png")
            img = Image.frombytes('RGBA', (width, height), b"".join(new_data2))
            img.save("3.png")
            img = Image.frombytes('RGBA', (width, height), b"".join(new_data3))
            img.save("2.png")
            img = Image.frombytes('RGBA', (width, height), b"".join(new_data4))
            img.save("1.png")
        else:
            print("SUPPORTED ONLY FOR FILES WITH \"font\" IN FILENAME!")
            sys.exit()
    case 9:
        # ASTC 4x4
        block_width = 4
        block_height = 4
        is_srgb : bool = False
        img = Image.frombytes('RGBA', (width, height), data, "astc", (block_width, block_height, is_srgb))
        img.save(sys.argv[2])