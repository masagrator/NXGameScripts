# Script for repacking ucas/utoc files, WIP
# It is required to use ucasUnpack.py first since umodel doesn't support unpacking all files, and UnrealPakViewer is unpacking them without class imports
# It is required to have Oodle.exe that can be compiled with project linked below:
# https://github.com/masagrator/UnrealOodleWrapper
# Script must be in the same folder as utoc and ucas files, generate json file with UnrealPakViewer and put it to the same folder with the same name as ucas/utoc file
# Edited uncompressed asset file cannot have different count of blocks (in case of CCFF7R one block is 256kB) than original (so for CCFF7R if your file has for example 384 kB, making it bigger than 512 kB or smaller than/equal to 256 kB will return error)
# As Argument provide filename of ucas file without any type (so for example `python ucasRepacker.py pakchunk5-Switch`)
# It will create new folder Paks with utoc and ucas files
# File generated in Paks are not compatible with UnrealPakViewer and umodel (because of how they use shortcuts for generating file tree)
# It was not tested with original game
# If you have PC, you can provide encryption key in format 0x 64 byte long as next argument (so f.e. `python ucasRepacker.py pakchunk5-WindowsNoEditor 0x1234567890123456789012345678901234567890123456789012345678901234`)

import sys
import json
import shutil
import os
import math
import subprocess
from Crypto.Cipher import AES # pip install pycryptodome

class _AES:
	Key = b""

class TOC:
	MAGIC = b"-==--==--==--==-"
	version = 3
	headerSize = 0x90
	fileCount = 1
	allBlockCount = 1
	blockEntrySize = 12
	compressionMethod = ""
	compressionMethodStringId = 1
	compressionMethodStringLen = 32
	blockSize = 0x40000
	directoryIndexSize = 0
	validContainer = 0
	containerID = 0
	encryptionKeyGUID = 0
	compressed = False
	encrypted = False
	signed = False
	indexed = False
	TABLE1 = []
	TABLE2 = []
	TABLE3 = []

class _JSON:
	DUMP = []
	FILTEREDLIST = []

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

if (utoc_file.read(16) != TOC.MAGIC):
	print("Wrong MAGIC!")
	sys.exit(1)

version = int.from_bytes(utoc_file.read(4), "little")
if (version != TOC.version):
	print("Unsupported version: %d" % version)

TOC.headerSize = int.from_bytes(utoc_file.read(4), "little")
TOC.fileCount = int.from_bytes(utoc_file.read(4), "little")
TOC.allBlockCount = int.from_bytes(utoc_file.read(4), "little")
TOC.blockEntrySize = int.from_bytes(utoc_file.read(4), "little")
TOC.compressionMethodStringId = int.from_bytes(utoc_file.read(4), "little")
TOC.compressionMethodStringLen = int.from_bytes(utoc_file.read(4), "little")
TOC.blockSize = int.from_bytes(utoc_file.read(4), "little")
TOC.directoryIndexSize = int.from_bytes(utoc_file.read(4), "little")
TOC.validContainer = int.from_bytes(utoc_file.read(4), "little")
TOC.containerID = int.from_bytes(utoc_file.read(8), "little")
TOC.encryptionKeyGUID = int.from_bytes(utoc_file.read(16), "little")
flags = int.from_bytes(utoc_file.read(4), "little")
TOC.compressed = bool(flags & (1 << 0))
TOC.encrypted = bool(flags & (1 << 1))
TOC.signed = bool(flags & (1 << 2))
TOC.indexed = bool(flags & (1 << 3))

utoc_file.seek(TOC.headerSize)

for i in range(TOC.fileCount):
	entry = {}
	entry["file_hash"] = int.from_bytes(utoc_file.read(8), "big")
	entry["flags"] = int.from_bytes(utoc_file.read(4), "big")
	TOC.TABLE1.append(entry)

for i in range(TOC.fileCount):
	entry = {}
	entry["data_ptr"] = utoc_file.tell()
	entry["block_start_id"] = int(int.from_bytes(utoc_file.read(5), "big") / TOC.blockSize)
	entry["full_dec_size"] = int.from_bytes(utoc_file.read(5), "big")
	TOC.TABLE2.append(entry)

for i in range(TOC.allBlockCount):
	entry = {}
	data_ptr = utoc_file.tell()
	offset = int.from_bytes(utoc_file.read(5), "little")
	entry["data_ptr"] = data_ptr
	entry["offset"] = offset 
	entry["com_size"] = int.from_bytes(utoc_file.read(3), "little")
	entry["unc_size"] = int.from_bytes(utoc_file.read(3), "little")
	entry["com_method"] = int.from_bytes(utoc_file.read(1), "little")
	TOC.TABLE3.append(entry)

pos = utoc_file.tell()

TOC.compressionMethod = readString(utoc_file)

if (TOC.compressionMethod != "Oodle"):
	print("This tool doesn't support other compression methods than Oodle!")
	sys.exit()

json_file = open(f"{sys.argv[1]}.json", "r", encoding="UTF-8")
_JSON.DUMP = json.load(json_file)["Files"]
json_file.close()

_JSON.DUMP.sort(key=Sort)

for i in range(len(_JSON.DUMP)):
	entry = {}
	entry["filepath"] = _JSON.DUMP[i]["Path"]
	entry["com_size"] = _JSON.DUMP[i]["Compressed Size"]
	entry["dec_size"] = _JSON.DUMP[i]["Size"]
	entry["block_count"] = _JSON.DUMP[i]["Compressed Block Count"]
	_JSON.FILTEREDLIST.append(entry)

DUMP = []

if (TOC.encrypted == True):
	if (len(sys.argv) > 2):
		_AES.Key = sys.argv[2]
	else:
		print("ucas is encrypted.")
		print("Provide AES key in 0x form to unpack encrypted files:")
		_AES.Key = input()
	if (_AES.Key[:2] != "0x"):
		print("Provided key in wrong format!")
		sys.exit(1)
	if len(_AES.Key) != 66:
		print("Key has wrong length!")
		sys.exit(1)
	try:
		_AES.Key = bytes.fromhex(_AES.Key[2:])
	except:
		print("Provided key in wrong format!")
		sys.exit(1)
shutil.copy(f"{sys.argv[1]}.ucas", f"Paks/{sys.argv[1]}.ucas")

ucas_file = open(f"Paks/{sys.argv[1]}.ucas", "rb+")

for i in range(len(_JSON.FILTEREDLIST)):
	if (os.path.isfile(_JSON.FILTEREDLIST[i]["filepath"]) == False):
		continue
	print("Detected file:\n%s" % _JSON.FILTEREDLIST[i]["filepath"])
	filesize = os.stat(_JSON.FILTEREDLIST[i]["filepath"]).st_size
	block_count = math.ceil(os.stat(_JSON.FILTEREDLIST[i]["filepath"]).st_size / TOC.blockSize)
	if (block_count != _JSON.FILTEREDLIST[i]["block_count"]):
		print("Exptected that file will have %d block(s)" % _JSON.FILTEREDLIST[i]["block_count"])
		print("It had %d %dkB block(s)." % (block_count, int(TOC.blockSize/1024)))
		sys.exit(1)

	temp_file = open(_JSON.FILTEREDLIST[i]["filepath"], "rb")
	blockID = TOC.TABLE2[i]["block_start_id"]
	for x in range(_JSON.FILTEREDLIST[i]["block_count"]):
		if (x+1 < _JSON.FILTEREDLIST[i]["block_count"]):
			temp_buffer = temp_file.read(TOC.blockSize)
		else:
			temp_buffer = temp_file.read()
		catch = subprocess.run(["Oodle.exe", "-c", "9", "3", "stdin=%d" % len(temp_buffer), "stdout"], input=temp_buffer, capture_output=True, text=False)
		if (catch.stderr != b""):
			print("Error while compressing file!")
			sys.exit(1)
		buffer = catch.stdout
		buffer_size = len(buffer)
		if (len(buffer) % 0x10 != 0):
			buffer += buffer[:0x10 - (len(buffer) % 0x10)]
		if (TOC.encrypted == True):
			cipher = AES.new(_AES.Key, AES.MODE_ECB)
			buffer = cipher.encrypt(buffer)
		size_check = TOC.TABLE3[blockID + x]["com_size"]
		if (size_check % 0x10 != 0):
			size_check += 0x10 - (size_check % 0x10)
		if (len(buffer) <= size_check):
			ucas_file.seek(TOC.TABLE3[blockID + x]["offset"])
		else:
			ucas_file.seek(0, 2)
		ucas_pos = ucas_file.tell()
		ucas_file.write(buffer)
		utoc_file.seek(TOC.TABLE3[blockID + x]["data_ptr"])
		utoc_file.write(ucas_pos.to_bytes(5, "little"))
		utoc_file.write(buffer_size.to_bytes(3, "little"))
		utoc_file.write(len(temp_buffer).to_bytes(3, "little"))
		utoc_file.write(0x1.to_bytes(1, "little"))
	utoc_file.seek(TOC.TABLE2[i]["data_ptr"] + 5)
	utoc_file.write(filesize.to_bytes(5, "big"))

ucas_file.close()
utoc_file.close()