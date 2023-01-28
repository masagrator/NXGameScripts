import json
import sys
from pathlib import Path

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("shift_jis_2004"))
        chars.append(c)

file = open(sys.argv[1], "rb")

if (file.read(0x4) != b"TRE2"):
    print("WRONG MAGIC!")
    sys.exit()

entries_count = int.from_bytes(file.read(0x4), byteorder="little")
header_size = int.from_bytes(file.read(0x8), byteorder="little")
file.seek(4, 1)

Offsets = []
for i in range(0, entries_count):
    Offsets.append(int.from_bytes(file.read(0x4), byteorder="little"))

DUMP = {}
for i in range(0, len(Offsets)):
    file.seek(Offsets[i])
    file.seek(0x24, 1)
    ID = int.from_bytes(file.read(0x4), byteorder="little")
    file.seek(4, 1)
    entry = []
    entry.append(readString(file))
    file.seek(Offsets[i] + 0x6C)
    entry.append(readString(file))
    file.seek(Offsets[i] + 0xAC)
    entry.append(readString(file))
    file.seek(Offsets[i] + 0xEC)
    entry.append(readString(file))
    file.seek(Offsets[i] + 0x12C)
    entry.append(readString(file))
    try:
        DUMP["%d" % ID]
    except:
        DUMP["%d" % ID] = entry
    else:
        if (DUMP["%d" % ID] != entry):
            DUMP["%d-%d" % (ID, i)] = entry

new_dict = dict(sorted(DUMP.items()))
file_new = open(f"{Path(sys.argv[1]).stem}_dump.json", "w", encoding="UTF-8")
json.dump(new_dict, file_new, indent="\t", ensure_ascii=False)
