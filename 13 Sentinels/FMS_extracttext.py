import json
import sys

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("UTF-8"))
        chars.append(c)

MESSAGES = []

file = open(sys.argv[1], "rb")
file.seek(0x14)
string_count = int.from_bytes(file.read(4), byteorder="little")
file.seek(0x20)
file.seek(string_count * 8, 1)
for i in range(0, string_count):
    MESSAGES.append(readString(file))

new_file = open("dump.json", "w", encoding="UTF-8")
json.dump(MESSAGES, new_file, indent="\t", ensure_ascii=False)
new_file.close()