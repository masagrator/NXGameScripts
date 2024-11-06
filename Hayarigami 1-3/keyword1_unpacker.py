import sys
import json

file = open(sys.argv[1], "rb")

entry_count = int.from_bytes(file.read(4), "little")

entries = []

for i in range(entry_count):
    entry = {}
    entry["ID"] = int.from_bytes(file.read(2), "little")
    string1_size = int.from_bytes(file.read(2), "little")
    offset = int.from_bytes(file.read(4), "little")
    pos = file.tell()
    file.seek(offset)
    entry["STRING1"] = file.read(string1_size).decode("shift_jis_2004")
    file.seek(pos)
    entry["DATA1"] = file.read(4).hex()
    string2_size = int.from_bytes(file.read(2), "little")
    string3_size = int.from_bytes(file.read(2), "little")
    offset = int.from_bytes(file.read(4), "little")
    pos = file.tell()
    file.seek(offset)
    entry["STRING2"] = file.read(string2_size).decode("shift_jis_2004")
    file.seek(pos)
    offset = int.from_bytes(file.read(4), "little")
    pos = file.tell()
    file.seek(offset)
    entry["STRING3"] = file.read(string3_size).decode("shift_jis_2004")
    file.seek(pos)
    entry["DATA2"] = file.read(4).hex()
    entries.append(entry)

file.close()

new_file = open("keyword1_dump.json", "w", encoding="UTF-8")
json.dump(entries, new_file, indent="\t", ensure_ascii=False)
new_file.close()