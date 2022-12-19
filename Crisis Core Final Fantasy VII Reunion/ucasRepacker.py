# Script for repacking ucas/utoc files, WIP
# It is required to use ucasUnpack.py first since umodel doesn't support unpacking all files, and UnrealPakViewer is unpacking them without class imports
# It is required to have Oodle.exe that can be compiled with Oodle.cpp from repo
# Script must be in the same folder as utoc and ucas files, generate json file with UnrealPakViewer and put it to the same folder with the same name as ucas/utoc file
# Edited uncompressed asset file cannot have different count of 256kB blocks than original (so if you file has for example 384 kB, making it bigger than 512 kB or smaller than/equal to 256 kB will return error)
# As Argument provide filename of ucas file without any type (so for example `python ucasRepacker.py pakchunk5-Switch``)
# It will create new folder Paks with utoc and ucas files
# File generated in Paks are not compatible with any unpacking tool because they are going on shortcuts instead of using proper chunk table
# It was not tested with original game

import sys
import json
import shutil
import os
import math
import subprocess

def Sort(key):
	return key["Offset"]

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("UTF-8"))
		chars.append(c)

os.makedirs("Paks", exist_ok=True)
shutil.copy(f"{sys.argv[1]}.utoc", f"Paks/{sys.argv[1]}.utoc")
utoc_file = open(f"Paks/{sys.argv[1]}.utoc", "rb+")

if (utoc_file.read(16) != b"-==--==--==--==-"):
	print("Wrong MAGIC!")
	sys.exit(1)

version = int.from_bytes(utoc_file.read(4), "little")
if (version != 3):
	print("Unsupported version: %d" % version)

header_size = int.from_bytes(utoc_file.read(4), "little")
file_count = int.from_bytes(utoc_file.read(4), "little")
all_block_count = int.from_bytes(utoc_file.read(4), "little")
block_entry_size = int.from_bytes(utoc_file.read(4), "little")
compression_method_string_id = int.from_bytes(utoc_file.read(4), "little")
compression_method_string_len = int.from_bytes(utoc_file.read(4), "little")
block_size = int.from_bytes(utoc_file.read(4), "little")
DirectoryIndexSize = int.from_bytes(utoc_file.read(4), "little")
valid_container = int.from_bytes(utoc_file.read(4), "little")
containerID = int.from_bytes(utoc_file.read(8), "little")
encryptionkeyGUID = int.from_bytes(utoc_file.read(16), "little")
flags = int.from_bytes(utoc_file.read(4), "little")
Compressed = bool(flags & (1 << 0))
Encrypted = bool(flags & (1 << 1))
Signed = bool(flags & (1 << 2))
Indexed = bool(flags & (1 << 3))

if (Encrypted == True):
	print("Tool doesn't support encrypted utoc!")
	sys.exit(1)

utoc_file.seek(header_size)

DATA1 = []
for i in range(file_count):
	entry = {}
	entry["file_hash"] = int.from_bytes(utoc_file.read(8), "big")
	entry["flags"] = int.from_bytes(utoc_file.read(4), "big")
	DATA1.append(entry)

print("0x%X" % utoc_file.tell())
#print(DATA1)

DATA2 = []
for i in range(file_count):
	entry = {}
	entry["ID"] = int(int.from_bytes(utoc_file.read(5), "big") / 0x40000)
	entry["dec_size"] = int.from_bytes(utoc_file.read(5), "big")
	DATA2.append(entry)

print("0x%X" % utoc_file.tell())
#print(DATA2)

DATA3 = {}
for i in range(all_block_count):
	data_ptr = utoc_file.tell()
	offset = int.from_bytes(utoc_file.read(5), "little") 
	DATA3[offset] = {}
	DATA3[offset]["data_ptr"] = data_ptr
	DATA3[offset]["com_size"] = int.from_bytes(utoc_file.read(3), "little")
	DATA3[offset]["unc_size"] = int.from_bytes(utoc_file.read(3), "little")
	DATA3[offset]["com_method"] = int.from_bytes(utoc_file.read(1), "little")

#print(DATA3)

pos = utoc_file.tell()

CompressionMethod = readString(utoc_file)

utoc_file.seek(pos + compression_method_string_len)

mount_point_string_size = int.from_bytes(utoc_file.read(4), "little")

mount_point = readString(utoc_file)

json_file = open(f"{sys.argv[1]}.json", "r", encoding="UTF-8")
DUMP = json.load(json_file)["Files"]
json_file.close()

DUMP.sort(key=Sort)

FilteredList = []

all_dec_size = 0

offset = 0
for i in range(len(DUMP)):
	entry = {}
	entry["filepath"] = DUMP[i]["Path"]
	entry["offset"] = offset
	entry["com_size"] = DUMP[i]["Compressed Size"]
	offset += DUMP[i]["Compressed Size"]
	entry["dec_size"] = DUMP[i]["Size"]
	all_dec_size += DUMP[i]["Size"]
	entry["block_count"] = DUMP[i]["Compressed Block Count"]
	FilteredList.append(entry)

DUMP = []
shutil.copy(f"{sys.argv[1]}.ucas", f"Paks/{sys.argv[1]}.ucas")

ucas_file = open(f"Paks/{sys.argv[1]}.ucas", "ab")

for i in range(len(FilteredList)):
	if (os.path.isfile(FilteredList[i]["filepath"]) == False):
		continue
	print("Detected file:\n%s" % FilteredList[i]["filepath"])
	filesize = os.stat(FilteredList[i]["filepath"]).st_size
	temp_file = open(FilteredList[i]["filepath"], "rb")
	block_count = math.ceil(os.stat(FilteredList[i]["filepath"]).st_size / 0x40000)
	if (block_count != FilteredList[i]["block_count"]):
		print("Exptected that file will have %d block(s)" % FilteredList[i]["block_count"])
		print("It had %d block(s)." % block_count)
		sys.exit(1)
	utoc_file.seek(DATA3[FilteredList[i]["offset"]]["data_ptr"])
	for i in range(block_count):
		buffer = temp_file.read(0x40000)
		if (len(buffer) == 0):
			print("Buffer is empty!")
			sys.exit(1)
		catch = subprocess.run(["Oodle.exe", "-c", "9", "stdin=%d" % len(buffer), "stdout"], input=buffer, capture_output=True, text=False)
		if (catch.stderr != b""):
			print("Compressing files failed!")
			print("stderr:")
			print(catch.stderr.decode("ascii"))
			sys.exit(1)
		utoc_file.write(ucas_file.tell().to_bytes(5, "little"))
		utoc_file.write((len(catch.stdout)).to_bytes(3, "little"))
		if (i+1 < block_count):
			utoc_file.write(0x40000.to_bytes(3, "little"))
		else:
			utoc_file.write((filesize - (0x40000*i)).to_bytes(3, "little"))
		utoc_file.write(0x1.to_bytes(1, "little"))
		ucas_file.write(catch.stdout)
		if (ucas_file.tell() % 0x10 != 0):
			ucas_file.write(catch.stdout[:(0x10 - (ucas_file.tell() % 0x10))])

ucas_file.close()
utoc_file.close()

	