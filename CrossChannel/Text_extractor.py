import glob
import os
import json

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("shift_jis_2004"))
        chars.append(c)

def ProcessText(file, command, messagenumber):
    entry = {}
    entry["TYPE"] = command
    entry["SUBTYPE"] = "STRING"
    entry["ID"] = messagenumber
    entry["STRING"] = readString(file)
    return entry

def ProcessName(file, command):
    entry = {}
    entry["TYPE"] = command
    entry["SUBTYPE"] = "NAME"
    entry["STRING"] = readString(file)
    return entry

def SearchInFile(file, size):
    entry = []
    while(file.tell() < size):
        byte = int.from_bytes(file.read(0x1), byteorder="little")
        if (0x45 <= byte <= 0x47):
            check = file.read(0x2)
            match(check):
                case b"\xFF\xFF":
                    messagenumber = int.from_bytes(file.read(0x2), byteorder="little")
                    entry.append(ProcessText(file, byte, messagenumber))
                case b"\x0D\x00":
                    if (byte == 0x47):
                        entry.append(ProcessName(file, byte))

    return entry


def GetFileSize(file):
    pos = file.tell()
    file.seek(0, 2)
    size = file.tell()
    file.seek(pos)
    return size

files = glob.glob("sn/*.bin")

os.makedirs("Text_dump", exist_ok=True)

for i in range(0, len(files)):
    file = open(files[i], "rb")
    dump = SearchInFile(file, GetFileSize(file))
    file.close()
    file = open("Text_dump/%s.json" % files[i][3:-4], "w", encoding="UTF-8")
    json.dump(dump, file, indent="\t", ensure_ascii=False)
    file.close()