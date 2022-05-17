import json
import glob
import os
import numpy

files = glob.glob("Script_disassembled/*.json")

for i in range(0, len(files)):
    print(files[i])
    file = open(files[i], "r", encoding="UTF-8")
    DUMP = json.load(file)
    file.close()

    os.makedirs("new_Script", exist_ok=True)
    new_file = open("new_Script/%s.binu8" % os.path.basename(files[i])[:-5], "wb")
    new_file.write(b"\x00" * 8)
    for x in range(0, len(DUMP["INSTRUCTIONS"])):
        key = list(DUMP["INSTRUCTIONS"][x].keys())[0]
        new_file.write(numpy.uint32(int(key, base=16)))
        match(key):
            case "0x7":
                new_file.write(bytes.fromhex(DUMP["INSTRUCTIONS"][x][key]))
            case _:
                new_file.write(numpy.int32(DUMP["INSTRUCTIONS"][x][key]))
    temp_pos = new_file.tell()
    new_file.seek(4, 0)
    new_file.write(numpy.uint32((temp_pos - 8) / 8))
    new_file.seek(0, 2)
    strings_blocks_count = len(DUMP["STRINGS"])
    for x in range(0, strings_blocks_count):
        new_file.write(numpy.uint32(len(DUMP["STRINGS"][x])))
        for y in range(0, len(DUMP["STRINGS"][x])):
            string = DUMP["STRINGS"][x][y].encode("UTF-8") + b"\x00"
            new_file.write(numpy.uint32(len(string)))
            new_file.write(string)
    if (os.path.basename(files[i])[:-5] in ["eventmode", "replaymode", "system", "title"]):
        new_file.write(b"\x00" * 4)
    else:
        new_file.write(b"\x00" * 8)
    flags = list(DUMP["FLAGS"].keys())
    new_file.write(numpy.uint32(len(flags)))
    for x in range(0, len(flags)):
        new_file.write(numpy.uint32(int(flags[x])))
        new_file.write(bytes.fromhex(DUMP["FLAGS"][flags[x]]))
    try:
        bytes.fromhex(DUMP["SPECIAL"][0]["METADATA"])
    except:
        new_file.close()
        continue
    else:
        for x in range(0, len(DUMP["SPECIAL"])):
            new_file.write(bytes.fromhex(DUMP["SPECIAL"][x]["METADATA"]))
            temp_pos = new_file.tell()
            new_file.write(b"\x00" * 4)
            for y in range(0, len(DUMP["SPECIAL"][x]["INSTRUCTIONS"])):
                key = list(DUMP["SPECIAL"][x]["INSTRUCTIONS"][y])[0]
                new_file.write(numpy.uint32(int(key, base=16)))
                match(key):
                    case "0x7":
                        new_file.write(bytes.fromhex(DUMP["SPECIAL"][x]["INSTRUCTIONS"][y][key]))
                    case _:
                        new_file.write(numpy.int32(DUMP["SPECIAL"][x]["INSTRUCTIONS"][y][key]))
            size = int((new_file.tell() - temp_pos) / 8)
            new_file.seek(temp_pos)
            new_file.write(numpy.uint32(size))
            new_file.seek(0, 2)
            for y in range(0, len(DUMP["SPECIAL"][x]["STRINGS"])):
                new_file.write(numpy.uint32(len(DUMP["SPECIAL"][x]["STRINGS"][y])))
                for z in range(0, len(DUMP["SPECIAL"][x]["STRINGS"][y])):
                    string = DUMP["SPECIAL"][x]["STRINGS"][y][z].encode("UTF-8") + b"\x00"
                    new_file.write(numpy.uint32(len(string)))
                    new_file.write(string)
            new_file.write(b"\x00" * 8)