import json
import glob
import os
import sys
from turtle import bye

def ProcessOpcode(opcode):
    assert(opcode <= 0x48)
    data = {}
    match(opcode): #opcode 0 seems to be responisble for loading strings (and more)
        case 7:
            data["0x7"] = file.read(4).hex().upper()
        case _:
            data["0x%x" % opcode] = int.from_bytes(file.read(4), byteorder="little", signed=True)
    return data

os.makedirs("Script_disassembled", exist_ok=True)

files = glob.glob("Script/*.binu8")

for i in range(0, len(files)):
    DUMP = {}
    DUMP["INSTRUCTIONS"] = []
    print(files[i])
    file = open(files[i], "rb")
    file.seek(0, 2)
    filesize = file.tell()
    file.seek(0, 0)
    assert(file.read(4) == b"\x00\x00\x00\x00")
    string_registration_offset = int.from_bytes(file.read(4), byteorder="little") * 8
    if (string_registration_offset == 0): 
        print("STRINGS NOT DETECTED!")
        continue
    while (file.tell() < (string_registration_offset + 8)):
        opcode = int.from_bytes(file.read(4), byteorder="little")
        DUMP["INSTRUCTIONS"].append(ProcessOpcode(opcode))
    assert(file.tell() == (string_registration_offset + 8))
    DUMP["STRINGS"] = []
    string_count = int.from_bytes(file.read(4), byteorder="little")
    if (string_count == 0): string_count = -1
    while(string_count != 0):
        if (string_count == -1):
            string_count = int.from_bytes(file.read(4), byteorder="little")
            continue
        entry = []
        for x in range(0, string_count):
            string_size = int.from_bytes(file.read(4), byteorder="little")
            entry.append(file.read(string_size).decode("UTF-8")[:-1])
        DUMP["STRINGS"].append(entry)
        string_count = int.from_bytes(file.read(4), byteorder="little")
    if (os.path.basename(files[i]) not in ["eventmode.binu8", "replaymode.binu8", "system.binu8", "title.binu8"]):
        file.seek(4, 1)

    flag_count = int.from_bytes(file.read(4), byteorder="little")
    DUMP["FLAGS"] = {}
    for x in range(0, flag_count):
        ID = int.from_bytes(file.read(4), byteorder="little")
        DUMP["FLAGS"][ID] = file.read(0x40).hex().upper()
    DUMP["SPECIAL"] = []
    while(file.tell() < filesize):
        entry = {}
        entry["METADATA"] = file.read(8).hex().upper()
        instruction_block_size = int.from_bytes(file.read(4), byteorder="little") * 8
        temp_pos = file.tell()
        entry["INSTRUCTIONS"] = []
        while(file.tell() < (temp_pos + instruction_block_size)):
            entry["INSTRUCTIONS"].append(ProcessOpcode(int.from_bytes(file.read(4), byteorder="little")))
        entry["STRINGS"] = []
        strings_count = int.from_bytes(file.read(4), byteorder="little")
        if (strings_count == 0): strings_count = -1
        while(strings_count != 0):
            if (strings_count == -1):
                strings_count = int.from_bytes(file.read(4), byteorder="little")
                continue
            entry2 = []
            for x in range(0, strings_count):
                string_size = int.from_bytes(file.read(4), byteorder="little")
                entry2.append(file.read(string_size).decode("UTF-8")[:-1])
            entry["STRINGS"].append(entry2)
            strings_count = int.from_bytes(file.read(4), byteorder="little")
        file.seek(4, 1)
        DUMP["SPECIAL"].append(entry)
    file.close()
    new_file = open("Script_disassembled/%s.json" % files[i][7:-6], "w", encoding="UTF-8")
    json.dump(DUMP, new_file, indent="\t", ensure_ascii=False)
    new_file.close()    