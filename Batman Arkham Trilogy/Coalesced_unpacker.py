# Provide .bin file as argument, it will create a folder with the same name
# example: python Coalesced_unpacker.py COALESCED_INT.bin

import sys
import os
from pathlib import Path
import json

file = open(sys.argv[1], "rb")

file_count = int.from_bytes(file.read(4), "little")

filelist = []

for i in range(file_count):
    path_length = int.from_bytes(file.read(4), "little", signed=True)
    if (path_length < 0):
        path_length *= -2
        path_name = file.read(path_length)[:-2].decode("UTF-16-LE")
    else:
        path_name = file.read(path_length)[:-1].decode("iso-8859-1")
    filelist.append(path_name)
    while (path_name[:3] in ["../", "..\\"]):
        path_name = path_name[3:]
    section_count = int.from_bytes(file.read(4), "little")
    SECTIONS = {}
    for x in range(section_count):
        section_name_length = int.from_bytes(file.read(4), "little", signed=True)
        if (section_name_length < 0):
            section_name_length *= -2
            section_name = file.read(section_name_length)[:-2].decode("UTF-16-LE")
        else:
            section_name = file.read(section_name_length)[:-1].decode("iso-8859-1")
        SECTIONS[section_name] = []
        key_value_pair_count = int.from_bytes(file.read(4), "little")
        for y in range(key_value_pair_count):
            key_name_length = int.from_bytes(file.read(4), "little", signed=True)
            if (key_name_length < 0):
                key_name_length *= -2
                key_name = file.read(key_name_length)[:-2].decode("UTF-16-LE")
            else:
                key_name = file.read(key_name_length)[:-1].decode("iso-8859-1")
            value_length = int.from_bytes(file.read(4), "little", signed=True)
            if (value_length < 0):
                value_length *= -2
                value_string = file.read(value_length)[:-2].decode("UTF-16-LE")
            else:  
                value_string = file.read(value_length)[:-1].decode("iso-8859-1")
            SECTIONS[section_name].append({"key": key_name, "value": value_string})
    os.makedirs("%s/%s" % (Path(sys.argv[1]).stem, Path(path_name).parent), exist_ok=True)

    with open("%s/%s.json" % (Path(sys.argv[1]).stem, path_name), "w", encoding="UTF-8") as new_file:
        json.dump(SECTIONS, new_file, indent="\t", ensure_ascii=False)

with open("%s/fileorder.json" % Path(sys.argv[1]).stem, "w", encoding="UTF-8") as new_file:
    json.dump(filelist, new_file, indent="\t", ensure_ascii=False)