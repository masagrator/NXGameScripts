import sys
import json

DUMP = []
file = open(sys.argv[1], "rb")
file.seek(0, 2)
filesize = file.tell()
file.seek(0)

table_entries_count = int.from_bytes(file.read(4), "little")
if (table_entries_count != 0x401):
	print("Wrong file!")
	sys.exit()
data = []
for i in range(table_entries_count):
	data.append(int.from_bytes(file.read(4), "little"))

for i in range(len(data)):
	entry = {}
	if (data[i] == 1):
		entry["type"] = "STRING"
		string_length = int.from_bytes(file.read(4), "little")
		temp = file.read(string_length)
		entry["string"] = temp[:-1].decode("UTF-8")
		DUMP.append(entry)
	elif (data[i] == 2):
		entry["type"] = "VALUE"
		entry["value"] = int.from_bytes(file.read(4), "little", signed=True)
		DUMP.append(entry)
	else:
		print(f"UNKNOWN TYPE: {data[i]}!")
		print("OFFSET: 0x%x" % (file.tell() - 4))
		sys.exit()

new_file = open("system.json", "w", encoding="UTF-8")
json.dump(DUMP, new_file, indent="\t", ensure_ascii=False)
new_file.close()