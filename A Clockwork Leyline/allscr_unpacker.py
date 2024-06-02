import sys
import os
from pathlib import Path

def readStringWide(myfile):
    chars = []
    while True:
        c = myfile.read(2)
        if c == b'\x0D\x0A':
            return str(b"".join(chars).decode("UTF-8"))
        else:
            myfile.seek(-2, 1)
            c = myfile.read(1)
            if (c == b"\xFF"):
                return str(b"".join(chars).decode("UTF-8"))
        chars.append(c)

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("shift_jis_2004"))
        chars.append(c)

def GetFileSize(file):
    pos = file.tell()
    file.seek(0, 2)
    size = file.tell()
    file.seek(pos)
    return size

file = open(sys.argv[1], "rb")

filesize = GetFileSize(file)

if (file.read(6) != b"mrgd00"):
    print("WRONG MAGIC!")
    sys.exit()

file_count = int.from_bytes(file.read(2), "little")

DATA = []

for i in range(file_count):
    entry = {}
    sector_offset = int.from_bytes(file.read(2), "little")
    entry["offset"] = sector_offset * 0x800 + int.from_bytes(file.read(2), "little")
    entry["sector_size_upper_boundary"] = int.from_bytes(file.read(2), "little")
    entry["size"] = int.from_bytes(file.read(2), "little")
    DATA.append(entry)

base_pos = file.tell()

FILENAMES = []

FILENAMES = ["DUMMY"]

for i in range(file_count-1):
    file.seek(base_pos+(i*0x20))
    if (i < file_count-3):
        FILENAMES.append(readString(file))

os.makedirs(Path(sys.argv[1]).stem, exist_ok=True)

for i in range(1, file_count-1):
    print(FILENAMES[i-1])
    file.seek(base_pos + DATA[i]["offset"])
    new_file = open(f"{Path(sys.argv[1]).stem}/{FILENAMES[i-1]}.dat", "wb")
    new_file.write(file.read(DATA[i]["size"]))
    new_file.close()

file.close()