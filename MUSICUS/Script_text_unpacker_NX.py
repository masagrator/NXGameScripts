import json
import glob
import os

os.makedirs("Script_TEXTS", exist_ok=True)

files = glob.glob("Script/*.binu8")

for i in range(0, len(files)):
    print(files[i])
    file = open(files[i], "rb")
    assert(file.read(4) == b"\x00\x00\x00\x00")
    string_registration_offset = int.from_bytes(file.read(4), byteorder="little") * 8
    if (string_registration_offset == 0): 
        print("STRINGS NOT DETECTED!")
        continue
    file.seek(string_registration_offset, 1)
    string_count = int.from_bytes(file.read(4), byteorder="little")
    UNK = int.from_bytes(file.read(4), byteorder="little")
    file.seek(1, 1)
    STRINGS = []
    for x in range(0, string_count):
        string_size = int.from_bytes(file.read(4), byteorder="little")
        STRINGS.append(file.read(string_size).decode("UTF-8")[:-1])
    file.close()
    new_file = open("Script_TEXTS/%s.json" % files[i][7:-6], "w", encoding="UTF-8")
    json.dump(STRINGS, new_file, indent="\t", ensure_ascii=False)
    new_file.close()    