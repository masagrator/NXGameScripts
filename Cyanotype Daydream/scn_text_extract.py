import sys
import os
from pathlib import Path
import json

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("UTF-8"))
        chars.append(c)

file = open(sys.argv[1], "rb")

if (file.read(4) != b"PSB\x00"):
    print("WRONG MAGIC!")
    sys.exit()

if (int.from_bytes(file.read(4), "little") != 3):
    print("Wrong version!")
    sys.exit()

unk0 = int.from_bytes(file.read(4), "little")
unk1 = int.from_bytes(file.read(4), "little")

string_table_offset = int.from_bytes(file.read(4), "little")

file.seek(string_table_offset)

if (int.from_bytes(file.read(1), "little") != 0xE):
    print("Wrong table start!")
    sys.exit()

string_count = int.from_bytes(file.read(2), "little")

if (file.read(1) != b"\x0F"):
    print("Wrong table separator!")
    sys.exit()

string_blob_offsets = []

for i in range(string_count):
    string_blob_offsets.append(int.from_bytes(file.read(3), "little"))

STRINGS = []

base_pos = file.tell()

for i in range(string_count):
    file.seek(base_pos + string_blob_offsets[i])
    STRINGS.append(readString(file))

os.makedirs("Dumped", exist_ok=True)

json_file = open("Dumped/%s.json" % Path(sys.argv[1]).stem, "w", encoding="UTF-8")
json.dump(STRINGS, json_file, indent="\t", ensure_ascii=False)
json_file.close()