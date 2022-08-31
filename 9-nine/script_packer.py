#It automatically patches "keywait" commands to get correct IDs and creates new 00_info.bin to put correct label jump offsets

import sys
import glob
from pathlib import Path

files = glob.glob("%s/*" % sys.argv[1])

new_file = open("script_new.arc", "wb")

header_size = (len(files) * 0x48) + 8

new_file.write(header_size.to_bytes(4, "little"))
new_file.write(len(files).to_bytes(4, "little"))
itr = 0

print("Phase 1: fixing keywaits")
for i in range(0, len(files)):
	print("%s                " % files[i], end="\r")
	if (files[i].find("00_info.bin") == -1):
		file = open(files[i], "r", encoding="shift_jis_2004", newline="\r\n")
		lines = file.readlines()
		file.close()
		DUMP = []
		entry = []
		for x in range(0, len(lines)):
			lines[x] = lines[x].rstrip()
			if (lines[x][0:9] == "<keywait "):
				lines[x] = "<keywait %d>" % itr
				itr += 1

		new_txtfile = open(files[i], "w", encoding="shift_jis_2004", newline="\r\n")
		for x in range(0, len(lines)):
			try:
				new_txtfile.write(lines[x])
			except:
				print("Error when writing this line:")
				print(lines[x])
				sys.exit()
			new_txtfile.write("\n")
		new_txtfile.close()

info_dump = {}

print("Phase 2: creating jump table")
for i in range(0, len(files)):
	file = open(files[i], "rb")
	if (Path(files[i]).stem != "00_info"):
		print("%s                " % files[i], end="\r")
		data = file.read()
		info_dump["%s.txt" % Path(files[i]).stem] = {}
		index = 0
		while(True):
			index = data.find(b"<label ", index)
			if (index == -1):
				break
			else:
				chars = []
				orig_index = index
				index += 7
				while(True):
					c = data[index:index+1]
					if (c == b"\r"):
						c = data[index+1:index+2]
						if (c != b"\n"):
							print("Expected \"\\n\" after \"\\r\" at offset: 0x%X!" % index+1)
							sys.exit()
						else:
							info_dump["%s.txt" % Path(files[i]).stem][b"".join(chars[:-1]).decode("ascii")] = orig_index
							break
					elif (c == b","):
							info_dump["%s.txt" % Path(files[i]).stem][b"".join(chars).decode("ascii")] = orig_index
							break
					else:
						chars.append(c)
						index += 1

infobin_data = []
filename_list = list(info_dump.keys())
entry_count = 0

for x in range(0, len(filename_list)):
	labels_list = list(info_dump[filename_list[x]].keys())
	for y in range(0, len(labels_list)):
		entry = []
		entry.append(labels_list[y].encode("ascii"))
		entry.append(b"\x00")
		entry.append(b"\xFE" * (0x40 - (len(b"".join(entry)) % 0x40)))
		entry.append(filename_list[x].encode("ascii"))
		entry.append(b"\x00")
		entry.append(b"\xFE" * (0x40 - (len(b"".join(entry)) % 0x40)))
		entry.append(info_dump[filename_list[x]][labels_list[y]].to_bytes(8, "little"))
		infobin_data.append(b"".join(entry))
		entry_count += 1

info_bin = open("%s/00_info.bin" % sys.argv[1], "wb")
info_bin.write(entry_count.to_bytes(8, "little"))
info_bin.write(b"".join(infobin_data))
info_bin.close()

for i in range(0, len(files)):

	file = open(files[i], "rb")
	file.seek(0, 2)
	size = file.tell()
	
	file.close()

	entry = []
	entry.append(files[i].removeprefix(sys.argv[1])[1:].encode("shift_jis_2004"))
	entry.append(b"\x00")
	while (len(b"".join(entry)) < 0x40):
		entry.append(b"\xFE")
	new_file.write(b"".join(entry))
	new_file.write(size.to_bytes(4, "little"))
	new_file.write(header_size.to_bytes(4, "little"))
	header_size += size
	if (header_size % 8 != 0):
		header_size += 8 - (header_size % 8)
	if (header_size % 16 == 0):
		header_size += 8

print("Writing script_new.arc...")

for i in range(0, len(files)):

	file = open(files[i], "rb")

	new_file.write(file.read())
	if (new_file.tell() % 8 != 0):
		new_file.write(b"\x00" * (8 - (new_file.tell() % 8)))
	if (new_file.tell() % 16 == 0):
		new_file.write(b"\x00" * 8)
	
	file.close()

new_file.close()

print("Finished executing script.")