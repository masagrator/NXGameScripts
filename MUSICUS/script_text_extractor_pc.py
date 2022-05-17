# This script is dedicated to Steam version using YOX ADV+++ engine
# Use GARBro to unpack script.dat and script_en.dat

import json
import glob
import os
import sys

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("shift_jis_2004"))
        chars.append(c)

def ReformatString(string: str):
    chars = []
    i = 0
    while(i < len(string)):
        if (string[i] == "@"):
            if (string[i+1] == "L"):
                chars.append("\n")
            i += 2
        else:
            chars.append(string[i])
            i += 1
    return "".join(chars)

def ReformatString2(string: str):
    return string.split("\n")

header_size = 0x30
files = glob.glob("script_en/*.dat")

for i in range(0, len(files)):
    print(files[i])
    file = open(files[i], "rb")
    assert(file.read(4) == b"YOX\x00")
    dummy = file.read(4)
    strings_offset = int.from_bytes(file.read(4), byteorder="little") + header_size
    strings_table_offset = strings_offset + int.from_bytes(file.read(4), byteorder="little")
    strings_count = int(int.from_bytes(file.read(4), byteorder="little") / 4)
    file.seek(strings_table_offset)
    STRINGS_OFFSETS = []
    for x in range(0, strings_count):
        STRINGS_OFFSETS.append(int.from_bytes(file.read(4), byteorder="little"))
    file.seek(strings_offset)
    STRINGS = []
    offset = 0
    start = file.tell()
    for x in range(0, strings_count):
        assert((file.tell() - start) == offset)
        string = readString(file)
        offset += len(string.encode("shift_jis_2004")) + 1
        string = ReformatString(string)
        STRINGS.append(string.split("\n"))

    file.close()
    os.makedirs("unpacked_en", exist_ok=True)
    dump = open("unpacked_en/%s.json" % files[i][10:-4], "w", encoding="UTF-8")
    json.dump(STRINGS, dump, indent="\t", ensure_ascii=False)
    dump.close()
    CLEANEDUP = []
    for x in range(0, len(STRINGS)):
        if (STRINGS[x] not in [[""], ["music.dat"]]):
            CLEANEDUP.append(STRINGS[x])
    if (CLEANEDUP != []):
        os.makedirs("cleaned_en", exist_ok=True)
        dump = open("cleaned_en/%s.json" % files[i][10:-4], "w", encoding="UTF-8")
        json.dump(CLEANEDUP, dump, indent="\t", ensure_ascii=False)
        dump.close()

files = glob.glob("script/*.dat")

for i in range(0, len(files)):
    print(files[i])
    file = open(files[i], "rb")
    assert(file.read(4) == b"YOX\x00")
    dummy = file.read(4)
    strings_offset = int.from_bytes(file.read(4), byteorder="little") + header_size
    strings_table_offset = strings_offset + int.from_bytes(file.read(4), byteorder="little")
    strings_count = int(int.from_bytes(file.read(4), byteorder="little") / 4)
    file.seek(strings_table_offset)
    STRINGS_OFFSETS = []
    for x in range(0, strings_count):
        STRINGS_OFFSETS.append(int.from_bytes(file.read(4), byteorder="little"))
    file.seek(strings_offset)
    STRINGS = []
    offset = 0
    start = file.tell()
    for x in range(0, strings_count):
        assert((file.tell() - start) == offset)
        string = readString(file)
        offset += len(string.encode("shift_jis_2004")) + 1
        string = ReformatString(string)
        STRINGS.append(string.split("\n"))

    file.close()
    os.makedirs("unpacked", exist_ok=True)
    dump = open("unpacked/%s.json" % files[i][10:-4], "w", encoding="UTF-8")
    json.dump(STRINGS, dump, indent="\t", ensure_ascii=False)
    dump.close()
    CLEANEDUP = []
    for x in range(0, len(STRINGS)):
        if (STRINGS[x] not in [[""], ["music.dat"]]):
            CLEANEDUP.append(STRINGS[x])
    if (CLEANEDUP != []):
        os.makedirs("cleaned", exist_ok=True)
        dump = open("cleaned/%s.json" % files[i][10:-4], "w", encoding="UTF-8")
        json.dump(CLEANEDUP, dump, indent="\t", ensure_ascii=False)
        dump.close()