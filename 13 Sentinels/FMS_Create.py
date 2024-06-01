import json
import sys

file = open(sys.argv[1], "r", encoding="UTF-8")
dump = json.load(file)
file.close()

if (len(dump) != 24030):
    print("This file has different string count than this script was originally made for.")
    print("No support for other strings count than 24030. Got: %d" % len(dump))
    sys.exit()

DUMP1 = b"\x00" * (8 * len(dump))
DUMP2 = []

for i in range(len(dump)):
    DUMP2.append(dump[i].encode("UTF-8") + b"\x00")

NEW_DUMP = []
NEW_DUMP.append(DUMP1)
NEW_DUMP.append(b"".join(DUMP2))

if (len(DUMP1) + len(b"".join(DUMP2))) % 16 != 0:
    NEW_DUMP.append(b"\x00" * (16 - (((len(DUMP1) + len(b"".join(DUMP2))) % 16))))

new_file = open("ScriptTextNew.fms", "wb")
new_file.write(b"FMSB")
new_file.write(len(b"".join(NEW_DUMP)).to_bytes(4, "little"))
new_file.write(0x20.to_bytes(8, "little"))
new_file.write(0x0.to_bytes(4, "little"))
new_file.write(len(dump).to_bytes(4, "little"))
new_file.write(0x3.to_bytes(8, "little"))
new_file.write(b"".join(NEW_DUMP))
new_file.write(b"FEOC")
new_file.write(b"\x00" * 4)
new_file.write(0x10.to_bytes(8, "little"))
new_file.close()
