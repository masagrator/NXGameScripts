from pydoc import tempfilepager
import sys
import json

DUMP = {}
file = open(sys.argv[1], "rb")
file.seek(0, 2)
filesize = file.tell()
file.seek(0)

table_entries_count = int.from_bytes(file.read(4), "little")
if (table_entries_count != 15):
	print("Wrong file!")
	sys.exit()
data = []
for i in range(table_entries_count):
	data.append(int.from_bytes(file.read(4), "little"))

DUMP["TABLE"] = data
DUMP["ENTRIES"] = []

while(file.tell() < filesize):
	flag1 = int.from_bytes(file.read(4), "little")
	entry = {}
	entry["STRINGS"] = []
	for i in range(4):
		string_length = int.from_bytes(file.read(4), "little")
		temp = file.read(string_length)
		entry["STRINGS"].append(temp[:-1].decode("UTF-8"))
	flag2 = int.from_bytes(file.read(4), "little")
	end2 = int.from_bytes(file.read(4), "little")
	if (end2 != 3):
		print("Wrong end2 data!")
		sys.exit()
	ID = int.from_bytes(file.read(32), "little", signed=True)
	entry["ID"] = ID
	entry["FLAG1"] = flag1
	entry["FLAG2"] = flag2
	DUMP["ENTRIES"].append(entry)

new_file = open("event.json", "w", encoding="UTF-8")
json.dump(DUMP, new_file, indent="\t", ensure_ascii=False)
new_file.close()