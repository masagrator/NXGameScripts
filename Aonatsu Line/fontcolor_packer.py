import json
import sys
import os

file = open(sys.argv[1], "r", encoding="UTF-8")
DUMP = json.load(file)
file.close()

header = []
header.append(len(DUMP["TABLE"]).to_bytes(4, "little"))
for i in range(len(DUMP["TABLE"])):
    header.append(DUMP["TABLE"][i].to_bytes(4, "little"))

entries = []
for i in range(len(DUMP["ENTRIES"])):
    for x in range(len(DUMP["ENTRIES"][i]["STRINGS"])):
        entries.append((len(DUMP["ENTRIES"][i]["STRINGS"][x].encode("UTF-8")) + 1).to_bytes(4, "little"))
        entries.append(DUMP["ENTRIES"][i]["STRINGS"][x].encode("UTF-8"))
        entries.append(b"\x00")
    for x in range(len(DUMP["ENTRIES"][i]["FLAGS"])):
        entries.append(DUMP["ENTRIES"][i]["FLAGS"][x].to_bytes(4, "little"))

os.makedirs("new", exist_ok=True)
new_file = open("new/fontcolor.datu8", "wb")
new_file.write(b"".join(header))
new_file.write(b"".join(entries))
new_file.close()