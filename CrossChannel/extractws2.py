# Script for extracting texts from .ws2 files
# That you can find in rio.arc of Steam release.
# For unpacking rio.arc use GarBro

import json
import os
import glob

def GetFileSize(file):
    pos = file.tell()
    file.seek(0, 2)
    size = file.tell()
    file.seek(pos)
    return size

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("shift_jis_2004"))
        chars.append(c)

def SearchInFile(file, size):
    dump = []
    name = ""
    while (file.tell() < size):
        check = file.read(1)
        entry = {}
        if (check == b"c"):
            if (file.read(4) == b"har\x00"):
                entry["TYPE"] = "MESSAGE"
                entry["STRING"] = readString(file).replace("¥d", "").replace("%K", "").replace("%P", "").replace("¥n", "%N")
                dump.append(entry)
            else:
                file.seek(-4, 1)
        elif (check == b"%"):
            if (file.read(2) == b"LC"):
                entry["TYPE"] = "NAME"
                entry["STRING"] = readString(file)
                dump.append(entry)
            else:
                file.seek(-2, 1)
        elif (check == b"\x0E"):
            if (file.read(2) == b"\x0B\x00"):
                entry["TYPE"] = "SELECT2"
                count = int.from_bytes(file.read(2), byteorder="little")
                file.seek(-5, 1)
                entry2 = []
                for x in range(0, count):
                    file.seek(10, 1)
                    entry2.append(readString(file))
                entry["STRINGS"] = entry2
                dump.append(entry)
            else:
                file.seek(-2, 1)
    return dump

files = glob.glob("rio/*.ws2")

os.makedirs("rio_txt", exist_ok=True)

for i in range(0, len(files)):
    file = open(files[i], "rb")
    data = file.read()
    file.seek(0, 0)
    if (data.find(b"char\x00") == -1):
        file.close()
        print("NO STRING IN %s" % files[i])
        continue
    else:
        print(files[i])
        dump = SearchInFile(file, GetFileSize(file))
        file_new = open("rio_txt/%s.json" % files[i][4:-7], "w", encoding="UTF-8")
        json.dump(dump, file_new, indent="\t", ensure_ascii=False)
        file_new.close()