import os 

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("shift_jis_2004"))
		chars.append(c)

os.makedirs("script", exist_ok=True)

file = open('script.arc', "rb")

header_size = int.from_bytes(file.read(4), "little", signed=False)
file_count = int.from_bytes(file.read(4), "little", signed=False)
string_max_size = 0x40

table = []

for i in range(0, file_count):
    entry = {}
    ptr = file.tell()
    entry["filename"] = readString(file)
    file.seek(ptr+string_max_size)
    entry["file_size"] = int.from_bytes(file.read(4), "little", signed=False)
    entry["offset"] = int.from_bytes(file.read(4), "little", signed=False)
    table.append(entry)

for i in range(0, file_count):
    file.seek(table[i]["offset"])
    new_file = open("script/%s" % table[i]["filename"], "wb")
    new_file.write(file.read(table[i]["file_size"]))
    new_file.close()

file.close()