import sys
import glob
import json
import os

files = glob.glob("*.pac", root_dir=sys.argv[1])
os.makedirs(sys.argv[1] + "/" + "dumped", exist_ok=True)

for x in range(len(files)):
    path = sys.argv[1] + "/" + files[x]
    print(path)
    file = open(path, "rb")
    offset_addon = int.from_bytes(file.read(4), "little")
    if (file.read(4) != b"ARC\x00"):
        print("WRONG MAGIC!")
        sys.exit()
    endianness = int.from_bytes(file.read(2), "big")
    if (endianness != 1):
        print("WRONG ENDIANNESS!")
        sys.exit()
    text_count1 = int.from_bytes(file.read(2), "little")
    text_count2 = int.from_bytes(file.read(2), "little")
    assert(text_count1 == text_count2)
    file.seek(0x14, 0)
    file_name = b""
    while(True):
        char = file.read(1)
        if (char != b"\x00"):
            file_name += char
        else: break
    file_name = file_name.decode("ascii")
    print(file_name)
    file.seek(0x34, 0)
    offsets = []
    for i in range(text_count1):
        offsets.append(int.from_bytes(file.read(4), "little") + offset_addon)
    if ((file.tell() - offset_addon) % 0x20 != 0):
        file.seek(0x20 - ((file.tell() - offset_addon) % 0x20), 1)
    text_metadata = []
    for i in range(text_count1):
        assert(file.read(4) == b"bin\x00")
        global_id = int.from_bytes(file.read(2), "little")
        internal_id = int.from_bytes(file.read(2), "little")
        assert(int.from_bytes(file.read(4), "little") == 0)
        assert(int.from_bytes(file.read(4), "little") == 0x10000)
        assert(int.from_bytes(file.read(0x10), "little") == 0)
        entry = {}
        entry["global_id"] = global_id
        entry["internal_id"] = internal_id
        text_metadata.append(entry)
    TEXT_DUMPS = []
    for i in range(len(offsets)):
        file.seek(offsets[i])
        entry_size = int.from_bytes(file.read(4), "little")
        data_type = int.from_bytes(file.read(4), "little")
        assert(data_type == 4)
        assert(int.from_bytes(file.read(4), "little") == 0)
        assert(int.from_bytes(file.read(4), "little") == 0x10)
        chara_count = int.from_bytes(file.read(2), "little")
        text_len = int.from_bytes(file.read(2), "little")
        assert(int.from_bytes(file.read(4), "little") == 0)
        text = file.read(text_len).decode("UTF-8")
        text_metadata[i]["TEXT"] = text
        text_metadata[i]["ORIGINAL_TEXT"] = text

    DUMP = {}
    DUMP["ENTRY"] = x
    DUMP["TEXTS"] = text_metadata
    
    new_path = sys.argv[1] + "/" + "dumped/" + file_name + ".json"
    new_file = open(new_path, "w", encoding="UTF-8")
    json.dump(DUMP, new_file, indent="\t", ensure_ascii=False)
    new_file.close()