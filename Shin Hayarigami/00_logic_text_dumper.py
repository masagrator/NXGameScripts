import json
from collections import Counter

file = open("00_logic.dat", "rb")

file_count = int.from_bytes(file.read(0x4), byteorder="little")

Offsets = []
IDs = []

for i in range(0, file_count):
    IDs.append(int.from_bytes(file.read(4), "little"))
    Offsets.append(int.from_bytes(file.read(4), "little"))

DUMP = {}

for i in range(file_count):
    ENTRY = {}
    ENTRY["KEYWORDS_DESCRIPTIONS"] = []
    ENTRY["CHARA_DESCRIPTIONS"] = {}
    file.seek(Offsets[i])
    file.seek(0x10, 1) #Unknown bytes
    string_count = 0
    pos = file.tell()
    value = int.from_bytes(file.read(4), "little")
    entries = (value - pos) // 4
    nodes_offset = [value]
    for x in range(1, entries):
        nodes_offset.append(int.from_bytes(file.read(4), "little"))
    x = 0
    while (x < len(nodes_offset)):
        file.seek(nodes_offset[x])
        section_type = int.from_bytes(file.read(2), "little")
        print("0x%x, section_type: %d" % (nodes_offset[x], section_type))
        if (section_type == 0):
            file.seek(-2, 1)
            break
        x += 1
    StringIDs = []
    StringIDs2 = []
    while(True):
        file.seek(nodes_offset[x])
        x += 1
        section_type = int.from_bytes(file.read(2), "little")
        if (section_type != 0): break
        file.seek(10, 1)
        stringId = int.from_bytes(file.read(1), "little")
        StringIDs.append(stringId)
        print("0x%x: StringId: %d" % (nodes_offset[x-1], stringId))
    for x in range(x, len(nodes_offset)):
        if (Counter(StringIDs) == Counter(StringIDs2)): 
            print("Printed strings: %d" % string_count)
            break
        print("0x%x" % nodes_offset[x])
        file.seek(nodes_offset[x])
        ID = int.from_bytes(file.read(2), "little")
        count = int.from_bytes(file.read(2), "little")
        test = int.from_bytes(file.read(2), "little")
        file.seek(-2, 1)
        if (test == 0):
            # Keyword descriptions
            if (ID not in StringIDs): continue
            StringIDs2.append(ID)
            print("Array ID: %d, count: %d" % (ID, count))
            pos = file.tell()
            M_ENTRY = []
            for y in range(count):
                file.seek(pos + (y * 0x64))
                ID = int.from_bytes(file.read(4), "little")
                str = b""
                while(True):
                    char = file.read(1)
                    if (char[0] == 0):
                        break
                    char = char[0] ^ 0xFF
                    str += char.to_bytes(1, "little")
                string = str.decode("shift_jis_2004")
                print(string)
                M_ENTRY.append(string)
                string_count += 1
            ENTRY["KEYWORDS_DESCRIPTIONS"].append(M_ENTRY)
        else:
            # Character descriptions
            name = ""
            for y in range(count):
                str = b""
                while(True):
                    char = file.read(1)
                    if (char[0] == 0):
                        break
                    char = char[0] ^ 0xFF
                    str += char.to_bytes(1, "little")
                if (len(str) > 0): 
                    string = str.decode("shift_jis_2004")
                    print(string)
                    if (y == 0):
                        name = string
                        if (name not in ENTRY["CHARA_DESCRIPTIONS"].keys()):
                            ENTRY["CHARA_DESCRIPTIONS"][name] = []
                    else:
                        if (string not in ENTRY["CHARA_DESCRIPTIONS"][name]):
                            ENTRY["CHARA_DESCRIPTIONS"][name].append(string)
                    string_count += 1
    DUMP["SECTION_%d" % i] = ENTRY

file = open("Dump.json", "w", encoding="UTF-8")
json.dump(DUMP, file, indent="\t", ensure_ascii=False)
file.close()