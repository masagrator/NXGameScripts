import sys
import glob
from pathlib import Path

files = glob.glob("%s/*" % sys.argv[1])

new_file = open("%s.arc" % Path(sys.argv[1]).stem, "wb")

header_size = (len(files) * 0x48) + 8

if (header_size % 0x80 != 0):
	header_size += 0x80 - (header_size % 0x80)

new_file.write(header_size.to_bytes(4, "little"))
new_file.write(len(files).to_bytes(4, "little"))
itr = 0

print("Writing %s.arc header..." % Path(sys.argv[1]).stem)

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
		header_size += 256

if (new_file.tell() % 0x80 != 0):
	tell = new_file.tell()
	new_file.write(b"\x00" * (0x80 - (tell % 0x80)))

print("Writing %s.arc data..." % Path(sys.argv[1]).stem)

for i in range(0, len(files)):

	file = open(files[i], "rb")

	new_file.write(file.read())
	if (new_file.tell() % 8 != 0):
		new_file.write(b"\x00" * (8 - (new_file.tell() % 8)))
	if (new_file.tell() % 16 == 0):
		new_file.write(b"\x00" * 256)
	
	file.close()

new_file.close()

print("Finished executing script.")
