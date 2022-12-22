# Not tested

import glob
import sys
import os
from pathlib import Path

files = glob.glob(f"{sys.argv[1]}/*.*")

def sanitizeFilenames(fileList):
	for i in range(len(fileList)):
		if (Path(fileList[i]).stem.isnumeric() == False):
			print("Files must use numerical names!")
			print("File %s has wrong name!" % Path(fileList[i]).stem)
			sys.exit()

sanitizeFilenames(files)

HEADER = []
BLOB = []
HEADER.append(len(files).to_bytes(4, "little"))
offset = 0
for i in range(len(files)):
	HEADER.append(offset.to_bytes(4, "little"))
	filesize = os.stat(files[i]).st_size
	HEADER.append(filesize.to_bytes(4, "little"))
	temp_file = open(files[i], "rb")
	BLOB.append(temp_file.read())
	temp_file.close()
	offset += filesize
	if offset % 0x40 != 0:
		BLOB.append(b"\x00" * (0x40 - (offset % 0x40)))
		offset += 0x40 - (offset % 0x40)
HEADER.append(0x94.to_bytes(4, "little"))

os.makedirs("Discimg", exist_ok=True)

file = open(f"Discimg/system_jefigs.bin", "wb")
file.write(b"".join(HEADER))
file.write(b"".join(BLOB))
file.close()