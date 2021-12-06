import glob
import json
import os
import numpy

def invertBitsU8(b1):
    number = numpy.uint8(b1)
    return ~number

def InvertString(bytes):
    chars = []
    for i in range(0, len(bytes)):
        chars.append(invertBitsU8(bytes[i]))
    return b"".join(chars)

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if ((c == b'\x00') or (c == b'\xFF')):
            myfile.seek(-1, 1)
            while (myfile.tell() % 4 != 0):
                myfile.seek(1, 1)
            return str(InvertString(b"".join(chars)).decode("shift_jis_2004"))
        chars.append(c)

def TakeID(F):
    pos = F.tell()
    F.seek(0x8)
    ID = numpy.fromfile(F, dtype=numpy.uint32, count=1)[0]
    F.seek(pos)
    return ID

def GetFileSize(F):
    pos = F.tell()
    F.seek(0, 2)
    size = F.tell()
    F.seek(pos)
    return size

files = glob.glob("extracted/*.dat")

os.makedirs("json", exist_ok=True)
for i in range(0, len(files)):
    file = open(files[i], "rb")
    ID = TakeID(file)
    print(ID)
    size = GetFileSize(file)
    file_new = open("json\%s.json" % ID, "w", encoding="UTF-8")
    Dump = []
    while (file.tell() < size):
        entry = {}
        if (file.read(0x1) == b"\xFF"):
            command_size = numpy.fromfile(file, dtype=numpy.uint8, count=1)[0] - 3
            command_ID = numpy.fromfile(file, dtype=numpy.uint8, count=1)[0]
            args = file.read(command_size)
            while (file.tell() % 4 != 0):
                file.seek(1, 1)

            entry["CMD_ID"] = int(command_ID)
            entry["ARGS"] = args.hex()
            Dump.append(entry)
        else:
            file.seek(-1, 1)
            entry["STRING"] = readString(file)
            Dump.append(entry)
    json.dump(Dump, file_new, indent="\t", ensure_ascii=False)