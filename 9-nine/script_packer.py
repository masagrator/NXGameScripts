#It automatically patches "keywait" commands to get correct IDs and 00_info.bin to put correct jump offsets

import sys
import glob
from pathlib import Path

files = glob.glob("%s/*" % sys.argv[1])

new_file = open("script_new.arc", "wb")

header_size = (len(files) * 0x48) + 8

new_file.write(header_size.to_bytes(4, "little"))
new_file.write(len(files).to_bytes(4, "little"))
itr = 0

for i in range(0, len(files)):
	print(files[i])
	if (files[i].find("00_info.bin") == -1):
		file = open(files[i], "r", encoding="shift_jis_2004")
		lines = file.readlines()
		file.close()
		DUMP = []
		entry = []
		for x in range(0, len(lines)):
			lines[x] = lines[x].rstrip()
			if (lines[x][0:9] == "<keywait "):
				lines[x] = "<keywait %d>" % itr
				itr += 1

		new_txtfile = open(files[i], "w", encoding="shift_jis_2004")
		for x in range(0, len(lines)):
			try:
				new_txtfile.write(lines[x])
			except:
				print("Error when writing this line:")
				print(lines[x])
				sys.exit()
			new_txtfile.write("\n")
		new_txtfile.close()

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

for i in range(0, len(files)):
	file = open(files[i], "rb")

	new_file.write(file.read())
	if (new_file.tell() % 8 != 0):
		new_file.write(b"\x00" * (8 - (new_file.tell() % 8)))
	if (new_file.tell() % 16 == 0):
		new_file.write(b"\x00" * 8)

new_file.close()

info_bin = open("%s/00_info.bin" % sys.argv[1], "rb")
entry_count = int.from_bytes(info_bin.read(8), "little")
info_dump = {}
for i in range(entry_count):
	pos = info_bin.tell()
	temp = []
	while(True):
		c = info_bin.read(1)
		if (c != b"\x00"):
			temp.append(c)
			continue
		Label = b"".join(temp).decode("ascii")
		temp = []
		break
	info_bin.seek(pos+0x40)
	while(True):
		c = info_bin.read(1)
		if (c != b"\x00"):
			temp.append(c)
			continue
		Filename = b"".join(temp).decode("ascii")
		break
	info_bin.seek(pos+0x80)
	Offset = int.from_bytes(info_bin.read(8), "little")
	try:
		info_dump[Filename]
	except:
		info_dump[Filename] = {}
	info_dump[Filename][Label] = Offset

for i in range(0, len(files)):
	file = open(files[i], "rb")
	if (Path(files[i]).stem not in ["00_info", "99_all_clear", "99_special", "99_special2"]):
		file.seek(0)
		data = file.read()
		label_list = list(info_dump["%s.txt" % Path(files[i]).stem].keys())
		for x in range(0, len(label_list)):
			index = data.find(b"<label %s" % label_list[x].encode("ascii"))
			if (index == -1):
				print("Index have not been found!")
				sys.exit()
			info_dump["%s.txt" % Path(files[i]).stem][label_list[x]] = index
	file.close()

infobin_data = []
infobin_data.append(entry_count.to_bytes(8, "little"))
filename_list = list(info_dump.keys())

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

info_bin = open("%s/00_info.bin" % sys.argv[1], "wb")
info_bin.write(b"".join(infobin_data))
info_bin.close()