import json
import sys
import os

file = open(sys.argv[1], "r", encoding="UTF-8")
DUMP = json.load(file)
file.close()

header = []
header.append(len(DUMP).to_bytes(4, "little"))
for i in range(len(DUMP)):
    if (DUMP[i]["type"] == "STRING"):
        header.append(0x1.to_bytes(4, "little"))
    elif (DUMP[i]["type"] == "VALUE"):
        header.append(0x2.to_bytes(4, "little"))
    else:
        print("UNKNOWN TYPE: %s!" % DUMP[i]["type"])
        sys.exit()

entries = []
for i in range(len(DUMP)):
    if (DUMP[i]["type"] == "STRING"):
        entries.append((len(DUMP[i]["string"].encode("UTF-8"))+1).to_bytes(4, "little"))
        entries.append(DUMP[i]["string"].encode("UTF-8") + b"\x00")
    elif (DUMP[i]["type"] == "VALUE"):
        entries.append(DUMP[i]["value"].to_bytes(4, "little", signed=True))

os.makedirs("new", exist_ok=True)
new_file = open("new/system.datu8", "wb")
new_file.write(b"".join(header))
new_file.write(b"".join(entries))
new_file.close()