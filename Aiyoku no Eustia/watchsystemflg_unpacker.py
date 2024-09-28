import sys
import json

DUMP = {}
file = open(sys.argv[1], "rb")
file.seek(0, 2)
filesize = file.tell()
file.seek(0)

table_entries_count = int.from_bytes(file.read(4), "little")
if (table_entries_count != 2):
	print("Wrong file!")
	sys.exit()
data = []
for i in range(table_entries_count):
	data.append(int.from_bytes(file.read(4), "little"))

DUMP["TABLE"] = data
DUMP["ENTRIES"] = []

while(file.tell() < filesize):
	entry = {}
	entry["DATA"] = int.from_bytes(file.read(4), "little")
	string_length = int.from_bytes(file.read(4), "little")
	temp = file.read(string_length)
	entry["STRING"] = temp[:-1].decode("UTF-8")
	DUMP["ENTRIES"].append(entry)

new_file = open("watchsystemflg.json", "w", encoding="UTF-8")
json.dump(DUMP, new_file, indent="\t", ensure_ascii=False)
new_file.close()