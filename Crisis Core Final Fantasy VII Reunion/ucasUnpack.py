# Script decompressing ucas archives.
# It was made just to understand how archives are storing data. It's slow in comparison to fully C-like tools, but it unpacks all files whole in comparison to UnrealPakViewer/umodel
# It requires Oodle.exe in the same folder for Oodle compression, source code is available here (read readme):
# https://github.com/masagrator/UnrealOodleWrapper
# Confirmed that it's unpacking fully without issues all Switch pakchunks, including also Little Hope game
# It does support PC encrypted ucas, though multiblock files like in pakchunk0, 7 and 8 are not tested.

import subprocess
import json
import sys
import os
import zlib
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
	compressionMethod = ["None"]
	compressionMethodStringCount = 1
	compressionMethodStringLen = 32
	blockSize = 0x40000
	fileTreeIndexSize = 0
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
	mount_point = "../../../"
	FilePaths = []

class _JSON:
	DUMP = []
	FILTEREDLIST = []


def Sort(key):
	return key["UserData"]

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("UTF-8"))
		chars.append(c)

def recursiveDirExplorer(parentPath: str, pDir: int, strTable: list, dirs: list, files: list):
	dirIdx = dirs[pDir]["FirstChildEntry"]
	fileIdx = dirs[pDir]["FirstFileEntry"]

	if (dirIdx == -1 and fileIdx == -1):
		return

	while (dirIdx != -1):
		dirEntry = dirs[dirIdx]
		newdirName = parentPath + "/" + strTable[dirEntry["Name"]]
		recursiveDirExplorer(newdirName, dirIdx, strTable, dirs, files)
		dirIdx = dirEntry["NextSiblingEntry"]
	
	while (fileIdx != -1):
		fileEntry = files[fileIdx]
		entry = {}
		entry["Filepath"] = parentPath + "/" + strTable[fileEntry["Name"]]
		entry["UserData"] = fileEntry["UserData"]
		TOC.FilePaths.append(entry)
		fileIdx = fileEntry["NextFileEntry"]


utoc_file = open(f"{sys.argv[1]}.utoc", "rb")

if (utoc_file.read(16) != TOC.MAGIC):
	print("Wrong MAGIC!")
	sys.exit(1)

version = int.from_bytes(utoc_file.read(4), "little")
if (version != TOC.version):
	print("Unsupported version: %d" % version)

TOC.headerSize = int.from_bytes(utoc_file.read(4), "little")
TOC.fileCount = int.from_bytes(utoc_file.read(4), "little")
if (TOC.fileCount <= 1):
	print("This package has no files!")
	utoc_file.close()
	sys.exit()

TOC.allBlockCount = int.from_bytes(utoc_file.read(4), "little")
TOC.blockEntrySize = int.from_bytes(utoc_file.read(4), "little")
TOC.compressionMethodStringCount = int.from_bytes(utoc_file.read(4), "little")
TOC.compressionMethodStringLen = int.from_bytes(utoc_file.read(4), "little")
TOC.blockSize = int.from_bytes(utoc_file.read(4), "little")
TOC.fileTreeIndexSize = int.from_bytes(utoc_file.read(4), "little")
TOC.validContainer = int.from_bytes(utoc_file.read(4), "little")
TOC.containerID = int.from_bytes(utoc_file.read(8), "little", signed=True)
if (TOC.containerID == -1):
	print("Global doesn't store any file!")
	utoc_file.close()
	sys.exit()

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
	flags = int.from_bytes(utoc_file.read(4), "big")
	TOC.TABLE1.append(entry)

for i in range(TOC.fileCount):
	entry = {}
	entry["block_start_id"] = int(int.from_bytes(utoc_file.read(5), "big") / TOC.blockSize)
	entry["full_dec_size"] = int.from_bytes(utoc_file.read(5), "big")
	TOC.TABLE2.append(entry)

for i in range(TOC.allBlockCount):
	entry = {}
	offset = int.from_bytes(utoc_file.read(5), "little") 
	entry["offset"] = offset 
	entry["com_size"] = int.from_bytes(utoc_file.read(3), "little")
	entry["unc_size"] = int.from_bytes(utoc_file.read(3), "little")
	entry["com_method"] = int.from_bytes(utoc_file.read(1), "little")
	TOC.TABLE3.append(entry)

pos = utoc_file.tell()

for i in range(TOC.compressionMethodStringCount):
	TOC.compressionMethod.append(readString(utoc_file))

for i in range(1, TOC.compressionMethodStringCount):
	if (TOC.compressionMethod[i] not in ["Oodle", "Zlib"]):
		print("This tool doesn't support other compression methods than Oodle and Zlib!")
		sys.exit()

utoc_file.seek(pos + TOC.compressionMethodStringLen)

fileTree_pos = utoc_file.tell()

string_len = int.from_bytes(utoc_file.read(4), "little")
TOC.mount_point = readString(utoc_file)

assert(string_len == (len(TOC.mount_point) + 1))

print("Offset: 0x%x" % utoc_file.tell())

dirnameCount = int.from_bytes(utoc_file.read(4), "little")

Dirs = []
for i in range(dirnameCount):
	entry = {}
	entry["Name"] = int.from_bytes(utoc_file.read(4), "little", signed=True)
	entry["FirstChildEntry"] = int.from_bytes(utoc_file.read(4), "little", signed=True)
	entry["NextSiblingEntry"] = int.from_bytes(utoc_file.read(4), "little", signed=True)
	entry["FirstFileEntry"] = int.from_bytes(utoc_file.read(4), "little", signed=True)
	Dirs.append(entry)

filenameCount = int.from_bytes(utoc_file.read(4), "little")
Files = []

for i in range(filenameCount):
	entry = {}
	entry["Name"] = int.from_bytes(utoc_file.read(4), "little", signed=True)
	entry["NextFileEntry"] = int.from_bytes(utoc_file.read(4), "little", signed=True)
	entry["UserData"] = int.from_bytes(utoc_file.read(4), "little", signed=True)
	Files.append(entry)

stringCount = int.from_bytes(utoc_file.read(4), "little")
Strings = []
for i in range(stringCount):
	strsize = int.from_bytes(utoc_file.read(4), "little")
	Strings.append(utoc_file.read(strsize)[:-1].decode("ascii"))

assert (Dirs[0]["Name"] == -1)

recursiveDirExplorer("", 0, Strings, Dirs, Files)

TOC.FilePaths.sort(key=Sort)

all_dec_size = 0

for i in range(TOC.fileCount):
	entry = {}
	block_start_id = TOC.TABLE2[i]["block_start_id"]
	if (i + 1 < TOC.fileCount):
		block_end_id = TOC.TABLE2[i+1]["block_start_id"]
	else:
		block_end_id = TOC.allBlockCount
	entry["filepath"] = "%08X.dat" % TOC.TABLE3[block_start_id]["offset"]
	entry["com_size"] = 0
	for x in range(block_start_id, block_end_id):
		entry["com_size"] += TOC.TABLE3[x]["com_size"]
	entry["dec_size"] = 0
	for x in range(block_start_id, block_end_id):
		entry["dec_size"] += TOC.TABLE3[x]["unc_size"]
	all_dec_size += entry["dec_size"]
	entry["block_count"] = block_end_id - block_start_id
	entry["Encrypted"] = False
	_JSON.FILTEREDLIST.append(entry)

if (TOC.encrypted == True):
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

fileCount = len(TOC.FilePaths)

print("Unpacked files will take space of: %d B, %.2f MB" % (all_dec_size, all_dec_size/1024/1024))
print("Count of files: %d" % fileCount)
print("To continue, press ENTER")
input()

utoc_file.close()
	
ucas_file = open(f"{sys.argv[1]}.ucas", "rb")

os.makedirs("Unpacked", exist_ok=True)

for i in range(fileCount):
	new_filepath = os.path.normpath(TOC.mount_point[8:] + TOC.FilePaths[i]["Filepath"])

	if (os.path.dirname(new_filepath) != ""):
		os.makedirs("Unpacked/%s" % os.path.dirname(new_filepath), exist_ok=True)
	file_pos = ucas_file.tell()
	print("File: %6d/%d  %s, size: %.2f MB" % (i+1, fileCount, new_filepath, _JSON.FILTEREDLIST[i]["dec_size"]/1024/1024))
	chunks = []
	for x in range(_JSON.FILTEREDLIST[i]["block_count"]):
		print("Chunk: %d/%d" % (x+1, _JSON.FILTEREDLIST[i]["block_count"]), end="\r")
		blockID = TOC.TABLE2[i]["block_start_id"] + x
		ucas_file.seek(TOC.TABLE3[blockID]["offset"])
		chunk_pos = ucas_file.tell()
		if (_JSON.FILTEREDLIST[i]["Encrypted"] == True):
			cipher = AES.new(_AES.Key, AES.MODE_ECB)
			if (TOC.TABLE3[blockID]["com_size"] % 0x10 != 0):
				size = TOC.TABLE3[blockID]["com_size"] + (0x10 - (TOC.TABLE3[blockID]["com_size"] % 0x10))
			else:
				size = TOC.TABLE3[blockID]["com_size"]
			buffer = cipher.decrypt(ucas_file.read(size))
		else:
			buffer = ucas_file.read(TOC.TABLE3[blockID]["com_size"])
		if TOC.TABLE3[blockID]["com_method"] == "None":
			if (x+1 < _JSON.FILTEREDLIST[i]["block_count"]):
				chunks.append(ucas_file.read(TOC.blockSize))
			else:
				chunks.append(ucas_file.read(_JSON.FILTEREDLIST[i]["dec_size"] - (x * TOC.blockSize)))
			continue
		if (x+1 < _JSON.FILTEREDLIST[i]["block_count"]):
			if (TOC.compressionMethod[TOC.TABLE3[blockID]["com_method"]] == "Zlib"):
				catch = zlib.decompress(buffer, bufsize = TOC.blockSize)
			else:
				catch = subprocess.run(["Oodle.exe", "-d", "%d" % TOC.blockSize, "stdin=%d" % len(buffer), "stdout"], input=buffer, capture_output=True, text=False)
		else:  
			if (TOC.compressionMethod[TOC.TABLE3[blockID]["com_method"]] == "Zlib"):
				catch = zlib.decompress(buffer, bufsize = _JSON.FILTEREDLIST[i]["dec_size"] - (x * TOC.blockSize))
			else:
				catch = subprocess.run(["Oodle.exe", "-d", "%d" % (_JSON.FILTEREDLIST[i]["dec_size"] - (x * TOC.blockSize)), "stdin=%d" % len(buffer), "stdout"], input=buffer, capture_output=True, text=False)
		if (TOC.compressionMethod[TOC.TABLE3[blockID]["com_method"]] == "Oodle"):
			if (catch.stderr != b""):
				print(catch.stderr.decode("ascii"))
				print("Chunk: %d/%d" % (x+1, _JSON.FILTEREDLIST[i]["block_count"]))
				print("Error while decompressing chunk at offset: 0x%X!" % chunk_pos)
				print("File offset: 0x%X" % file_pos)
				sys.exit(1)
			chunks.append(catch.stdout)
		else:
			chunks.append(catch)
	conc_file = open("Unpacked/%s" % new_filepath, "wb")
	conc_file.write(b"".join(chunks))
	end_size = conc_file.tell()
	conc_file.close()
	if (end_size != _JSON.FILTEREDLIST[i]["dec_size"]):
		print("Decompressed file has wrong size!")
		print("Expected: %dB" % _JSON.FILTEREDLIST[i]["dec_size"])
		print("Got: %dB" % end_size)
		os.remove(new_filepath)
		sys.exit(1)

ucas_file.close()
