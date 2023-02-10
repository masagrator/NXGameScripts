# This script injects text into English scenario file. Everything else is just copied
# Expect Chinese languages to be broken after injecting custom text 

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

file = open("Dump.json", "r", encoding="UTF-8")
DUMP = json.load(file)
file.close()

offsets_table = []
strings_blob = []

offset = 0

for i in range(len(DUMP[1])):
    if len(DUMP[1][i]) == 0:
        offsets_table.append(len(b"".join(strings_blob)).to_bytes(4, "big"))
        continue
    offsets_table.append(offset.to_bytes(4, "big"))
    string = DUMP[1][i].encode("UTF-8") + b"\x0D\x0A"
    strings_blob.append(string)
    offset += len(string)

offsets_table.append(int(-1).to_bytes(4, "big", signed=True))
offsets_table.append(int(-1).to_bytes(4, "big", signed=True))
strings_blob.append(int(-1).to_bytes(4, "big", signed=True))

file = open("script_text.mrg", "rb")
filesize = GetFileSize(file)

FILE_OFFSETS = []

for i in range(2):
    STRINGS = []
    offsets = 0
    offset_check = False
    while(True):
        offset = int.from_bytes(file.read(4), "big", signed=True)
        if (offset == -1):
            if offset_check == True:
                break
            else:
                offset_check = True
        else:
            offsets = offset
    temp_pos = file.tell()
    file.seek(temp_pos + offsets)
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
    FILE_OFFSETS.append(file.tell())

new_file = open("script_text2.mrg", "wb")
file.seek(0)
new_file.write(file.read(FILE_OFFSETS[0]))
new_file.write(b"".join(offsets_table))
new_file.write(b"".join(strings_blob))
if (new_file.tell() % 4 != 0):
    new_file.write(b"\xFF" * (4 - (new_file.tell() % 4)))
file.seek(FILE_OFFSETS[1])
new_file.write(file.read())
new_file.close()
file.close()
