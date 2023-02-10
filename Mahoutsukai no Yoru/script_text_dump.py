import sys
import json

def readString(myfile):
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

def GetFileSize(file):
    pos = file.tell()
    file.seek(0, 2)
    size = file.tell()
    file.seek(pos)
    return size

file = open("script_text.mrg", "rb")

filesize = GetFileSize(file)

if (file.read(4) != b"mrgd"):
    print("WRONG MAGIC!")
    sys.exit()

if (file.read(4) != b"00\n\0"):
    print("Wrong type!")
    sys.exit()

file.seek(0x58)

DUMP = []

while(file.tell() < filesize):
    print("0x%x" % file.tell())
    STRINGS = []
    offsets = []
    offset_check = False
    while(True):
        offset = int.from_bytes(file.read(4), "big", signed=True)
        if (offset == -1):
            if offset_check == True:
                break
            else:
                offset_check = True
        else:
            offsets.append(offset)
    temp_pos = file.tell()
    print("0x%x" % file.tell())
    print(f"Dumping {len(offsets)} strings...")
    for i in range(len(offsets)):
        file.seek(temp_pos + offsets[i])
        string = readString(file)
        STRINGS.append(string)
    DUMP.append(STRINGS)
    c = file.read(1)
    if c == b"\xFF":
        while(True):
            c = file.read(1)
            if c == b"":
                break
            if c != b"\xFF":
                file.seek(-1, 1)
                break
    else:
        file.seek(-1, 1)

file.close()
new_file = open("Dump.json", "w", encoding="UTF-8")
json.dump(DUMP, new_file, indent="\t", ensure_ascii=False)
new_file.close()