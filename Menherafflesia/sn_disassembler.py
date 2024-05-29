import json
import os
import sys
import glob
import puyo_lz01
from pathlib import Path

def Sort(key):
	return key

class Utils:
	CMDS = []
	JUMP_POINTS = []
	string_counter = 0

Filenames = [
	"0000",
	"0001",
	"purorogu",
	"maturi",
	"mihomi",
	"ayume",
	"moeko",
	"nenene",
	"grandroot",
	"ex1",
	"ex2",
	"ex3",
	"ex4",
	"ex5",
	"ex6",
	"ex7"
]

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("shift_jis_2004"))
		chars.append(c)

def ProcessMessage(entry, file):
	entry["MESSAGE_TYPE_ID"] = int.from_bytes(file.read(0x2), byteorder="little", signed=True)
	if (entry["MESSAGE_TYPE_ID"] in [-1, 10]):
		ID = int.from_bytes(file.read(0x2), byteorder="little", signed=True)
		if (ID < 0):
			entry["ID"] = ID
		else: Utils.string_counter += 1
	entry["STRING"] = readString(file)
	return entry

# 0x1677D0 - Command array
def ProcessCMD(cmd: int, file, size):
	entry = {}
	entry["LABEL"] = "0x%X" % (file.tell() - 1)
	match(cmd):
		case 0:
			entry["CMD"] = "%X" % cmd
		case 1:
			entry["CMD"] = "IFGOTO"
			entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		case 2:
			entry["CMD"] = "JMP"
			entry["ID"] = int.from_bytes(file.read(0x4), byteorder="little")
		# case 3:
		# 	entry["CMD"] = "%X" % cmd
		# 	pos = file.tell()
		# 	label = int.from_bytes(file.read(0x4), byteorder="little")
		# 	assert(label == pos)
		# 	Utils.JUMP_POINTS.append(label)
		# 	entry["ID"] = int.from_bytes(file.read(2), "little")
		# 	entry["VALUE"] = int.from_bytes(file.read(2), "little")
		# 	label = int.from_bytes(file.read(0x4), byteorder="little")
		# 	entry["TO_LABEL"] = "0x%X" % label
		# case 4:
		# 	entry["CMD"] = "%X" % cmd
		# 	pos = file.tell()
		# 	label = int.from_bytes(file.read(0x4), byteorder="little")
		# 	assert(label == pos)
		# 	Utils.JUMP_POINTS.append(label)
		# 	pos = file.tell()
		# 	entry["ID1"] = int.from_bytes(file.read(2), "little")
		# 	entry["VALUE1"] = int.from_bytes(file.read(2), "little")
		# 	entry["ID2"] = int.from_bytes(file.read(2), "little")
		# 	entry["VALUE2"] = int.from_bytes(file.read(2), "little")
		case 5:
			entry["CMD"] = "RETURN"
		case 6:
			entry["CMD"] = "IFGOTO6"
			entry["DATA"] = file.read(0x4).hex()
			entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		case 7:
			entry["CMD"] = "IFGOTO7"
			entry["DATA"] = file.read(0x4).hex()
			entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		case 8:
			entry["CMD"] = "IFGOTO8"
			entry["DATA"] = file.read(0x4).hex()
			entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		# case 9:
		# 	entry["CMD"] = "IFGOTO9"
		# 	entry["DATA"] = file.read(0x4).hex()
		# 	entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		# case 0xA:
		# 	entry["CMD"] = "IFGOTOA"
		# 	entry["DATA"] = file.read(0x4).hex()
		# 	entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		# case 0xB:
		# 	entry["CMD"] = "IFGOTOB"
		# 	entry["DATA"] = file.read(0x4).hex()
		# 	entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		# case 0xC:
		# 	entry["CMD"] = "IFGOTOC"
		# 	entry["DATA"] = file.read(0x2).hex()
		# 	entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		case 0xD:
			entry["CMD"] = "GOTO"
			entry["ID"] = int.from_bytes(file.read(0x2), byteorder="little")
			entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		case 0xE:
			entry["CMD"] = "IFGOTOE"
			entry["DATA"] = file.read(0x2).hex()
			count = int.from_bytes(file.read(0x2), byteorder="little")
			new_list = []
			for x in range(count):
				entry2 = {}
				entry2["VALUE"] = int.from_bytes(file.read(0x2), byteorder="little")
				entry2["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
				new_list.append(entry2)
			entry["LIST"] = new_list
		# case 0xF:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		case 0x10:
			entry["CMD"] = "MOV"
			entry["ID"] = int.from_bytes(file.read(0x2), "little")
			entry["VALUE"] = int.from_bytes(file.read(0x2), "little")
		# case 0x11:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		case 0x12:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		# case 0x13:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x14:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x15:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		case 0x16:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		# case 0x17:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x18:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x19:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x8).hex()
		case 0x1A:
			entry["CMD"] = "ATTACH_BG"
			entry["ID"] = int.from_bytes(file.read(0x2), byteorder="little")
			entry["BGID"] = int.from_bytes(file.read(0x2), byteorder="little")
		case 0x1B:
			entry["CMD"] = "%X" % cmd
		case 0x1C:
			entry["CMD"] = "%X" % cmd
		case 0x1D:
			entry["CMD"] = "%X" % cmd
			entry["ID"] = int.from_bytes(file.read(0x2), byteorder="little")
			entry["DATA"] = file.read(0x4).hex()
		case 0x1E:
			entry["CMD"] = "%X" % cmd
			entry["ID"] = int.from_bytes(file.read(0x2), byteorder="little")
			entry["DATA"] = file.read(0x8).hex()
		case 0x1F:
			entry["CMD"] = "%X" % cmd
			entry["ID"] = int.from_bytes(file.read(0x2), byteorder="little")
			entry["DATA"] = file.read(0xA).hex()
		# case 0x20:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x6).hex()
		case 0x21:
			entry["CMD"] = "%X" % cmd
			entry["ID"] = int.from_bytes(file.read(0x2), byteorder="little")
			entry["DATA"] = file.read(0x4).hex()
		case 0x22:
			entry["CMD"] = "%X" % cmd
			entry["ID"] = int.from_bytes(file.read(0x2), byteorder="little")
			entry["DATA"] = file.read(0x2).hex()
		# case 0x23:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x8).hex()
		# case 0x24:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x6).hex()
		case 0x25:
			entry["CMD"] = "%X" % cmd
			entry["ID"] = int.from_bytes(file.read(0x2), byteorder="little")
			entry["DATA"] = file.read(0x2).hex()
		# case 0x26:
		# 	entry["CMD"] = "%X" % cmd
		# case 0x27:
		# 	entry["CMD"] = "%X" % cmd
		# case 0x28:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x29:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x2A:
		# 	entry["CMD"] = "%X" % cmd
		# case 0x2B:
		# 	entry["CMD"] = "%X" % cmd
		# case 0x2C:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		case 0x2D:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x2E:
			entry["CMD"] = "%X" % cmd
		# case 0x2F:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x30:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0xA).hex()
		case 0x31:
			entry["CMD"] = "SELECT2"
			assert(file.read(0x2) == b"\x80\x80")
			count = int.from_bytes(file.read(0x2), byteorder="little")
			entry["COUNT_TYPE"] = count // 100
			count %= 100
			assert(file.read(0x2) == b"\x00\x00")
			new_list = []
			for x in range(0, count):
				entry2 = {}
				entry2["UNK0"] = int.from_bytes(file.read(0x2), byteorder="little")
				entry2["ID"] = int.from_bytes(file.read(0x2), byteorder="little")
				entry2["UNK1"] = int.from_bytes(file.read(0x2), byteorder="little")
				entry2["JUMP_TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
				entry2["STRING"] = readString(file)
				new_list.append(entry2)
			entry["LIST"] = new_list
		case 0x32:
			entry["CMD"] = "SELECT"
			assert(file.read(0x2) == b"\x80\x80")
			count = int.from_bytes(file.read(0x2), byteorder="little")
			entry["UNK0"] = int.from_bytes(file.read(0x2), byteorder="little")
			new_list = []
			for x in range(0, count):
				entry2 = {}
				entry2["UNK0"] = int.from_bytes(file.read(0x2), byteorder="little")
				entry2["ID"] = int.from_bytes(file.read(0x2), byteorder="little")
				entry2["UNK1"] = int.from_bytes(file.read(0x2), byteorder="little")
				entry2["JUMP_TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
				entry2["STRING"] = readString(file)
				new_list.append(entry2)
			entry["LIST"] = new_list
		# case 0x33:
		# 	entry["CMD"] = "%X" % cmd
		case 0x34:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0xA).hex()
		# case 0x35:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		case 0x36:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		case 0x37:
			entry["CMD"] = "%X" % cmd
		# case 0x38:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		case 0x39:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
			entry["ID"] = int.from_bytes(file.read(0x2), "little")
		# case 0x3A:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		case 0x3B:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		case 0x3C:
			entry["CMD"] = "WAIT"
			entry["VALUE"] = int.from_bytes(file.read(0x2), "little")
		# case 0x3D:
		# 	entry["CMD"] = "%X" % cmd
		# case 0x3E:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x3F:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x40:
		# 	entry["CMD"] = "%X" % cmd
		# case 0x41:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x1).hex()
		# case 0x42:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x8).hex()
		case 0x43:
			entry["CMD"] = "%X" % cmd
			entry["ID"] = int.from_bytes(file.read(0x2), byteorder="little")
			entry["DATA"] = file.read(0x2).hex()
		case 0x44:
			entry["CMD"] = "VOICE"
			entry["MESSAGE_TYPE_ID"] = int.from_bytes(file.read(0x2), byteorder="little")
			entry["VOICE_ID"] = int.from_bytes(file.read(0x2), byteorder="little")
		case 0x45:
			entry["CMD"] = "TEXT2"
			entry = ProcessMessage(entry, file)
		# case 0x46:
		# 	entry["CMD"] = "TEXT3"
		# 	entry = ProcessMessage(entry, file)
		case 0x47:
			entry["CMD"] = "TEXT"
			entry = ProcessMessage(entry, file)
		# case 0x48:
		# 	entry["CMD"] = "NEW_LINE"
		# 	entry["MESSAGE_TYPE_ID"] = int.from_bytes(file.read(0x2), "little", signed=True)
		case 0x49:
			entry["CMD"] = "NEW_PAGE"
			assert(file.read(4) == b"\xFF\xFF\xFF\xFF")
		case 0x4A:
			entry["CMD"] = "KEY_WAIT"
			entry["MESSAGE_TYPE_ID"] = int.from_bytes(file.read(0x2), "little", signed=True) #It's ignored in code
		case 0x4B:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x4C:
			entry["CMD"] = "TEXT_BOX_TEXTURE_POS"
			entry["MESSAGE_TYPE_ID"] = int.from_bytes(file.read(0x2), "little", signed=True)
			entry["POS_X"] = int.from_bytes(file.read(0x2), "little", signed=True)
			entry["POS_Y"] = int.from_bytes(file.read(0x2), "little", signed=True)
		# case 0x4D:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0xA).hex()
		case 0x4E:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x4F:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		# case 0x50:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		case 0x51:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x6).hex()
		# case 0x52:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0xA).hex()
		# case 0x53:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x54:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x8).hex()
		# case 0x55:
		# 	entry["CMD"] = "TITLE"
		# 	string_offset = int.from_bytes(file.read(4), "little")
		# 	pos = file.tell()
		# 	file.seek(string_offset)
		# 	entry["STRING"] = readString(file)
		# 	file.seek(pos)
		# case 0x56:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x57:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		# case 0x58:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		case 0x59:
			entry["CMD"] = "%X" % cmd
		case 0x5A:
			entry["CMD"] = "%X" % cmd
		# case 0x5B:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0xA).hex()
		# case 0x5C:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x6).hex()
		# case 0x5D:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x5E:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x5F:
		# 	entry["CMD"] = "%X" % cmd
		# 	pos = file.tell()
		# 	label = int.from_bytes(file.read(0x4), byteorder="little")
		# 	assert(label == pos)
		# 	Utils.JUMP_POINTS.append(label)
		# 	entry["ID"] = int.from_bytes(file.read(2), "little")
		# 	entry["VALUE"] = int.from_bytes(file.read(2), "little")
		# case 0x60:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x6).hex()
		# case 0x61:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x6).hex()
		# case 0x62:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x63:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0xA).hex()
		# case 0x64:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x6).hex()
		# case 0x65:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x66:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x67:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		case 0x68:
			entry["CMD"] = "TEXT_BOX"
			entry["MESSAGE_TYPE_ID"] = int.from_bytes(file.read(2), "little", signed=True)
			entry["TEXT_POS_X"] = int.from_bytes(file.read(2), "little", signed=True)
			entry["TEXT_POS_Y"] = int.from_bytes(file.read(2), "little", signed=True)
			entry["SIZE_X"] = int.from_bytes(file.read(2), "little", signed=True)
			entry["SIZE_Y"] = int.from_bytes(file.read(2), "little", signed=True)
		case 0x69:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		case 0x6A:
			entry["CMD"] = "%X" % cmd
			assert(file.read(0x4) == b"\xFF\xFF\xFF\xFF")
		case 0x6B:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		case 0x6C:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x10).hex()
		# case 0x6D:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		case 0x6E:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x6F:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x6).hex()
		# case 0x70:
		# 	entry["CMD"] = "%X" % cmd
		case 0x71:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x6).hex()
		case 0x72:
			entry["CMD"] = "%X" % cmd
			entry["ID"] = int.from_bytes(file.read(0x2), byteorder="little")
			entry["DATA"] = file.read(0x2).hex()
		# case 0x73:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0xA).hex()
		case 0x74:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x6).hex()
		case 0x75:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		# case 0x76:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		# case 0x77:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x78:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x79:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x7A:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0xA).hex()
		case 0x7B:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		# case 0x7C:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x7D:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex() #It's ignored by code
		# case 0x7E:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x7F:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x80:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x3).hex()
		# case 0x81:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		case 0x82:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		case 0x83:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		# case 0x84:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		case 0x85:
			entry["CMD"] = "%X" % cmd
			entry = ProcessMessage(entry, file)
		# case 0x86:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x87:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		# case 0x88:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		# case 0x89:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		# case 0x8A:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x8B:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x8C:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		case 0x8D:
			entry["CMD"] = "%X" % cmd
		# case 0x8E:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		# case 0x8F:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		# case 0x90:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x91:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		case 0x92:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0xE).hex()
		case 0x93:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x8).hex()
		# case 0x94:
		# 	entry["CMD"] = "TEXT4"
		# 	entry = ProcessMessage(entry, file)
		# case 0x95:
		# 	entry["CMD"] = "TEXT5"
		# 	entry = ProcessMessage(entry, file)
		# case 0x96:
		# 	entry["CMD"] = "TEXT6"
		# 	entry = ProcessMessage(entry, file)
		# case 0x97:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		# case 0x98:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		# case 0x99:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		# case 0x9A:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x9B:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x6).hex()
		# case 0x9C:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x8).hex()
		case 0x9D:
			entry["CMD"] = "%X" % cmd
			entry["ID"] = int.from_bytes(file.read(0x2), byteorder="little")
			entry["DATA"] = file.read(0x4).hex()
		# case 0x9E:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		# case 0x9F:
		# 	entry["CMD"] = "TEXT7"
		# 	entry = ProcessMessage(entry, file)
		# case 0xA0:
		# 	print("0x%x is a nullsub!" % cmd)
		# 	print("Offset: 0x%X" % (file.tell() - 1))
		# 	sys.exit()
		case _:
			entry["CMD"] = "%X" % cmd
			print("UNKNOWN COMMAND: 0x%X" % cmd)
			print("OFFSET: 0x%X" % (file.tell() - 1))
			sys.exit()
	return entry

file = open("sn.bin", "rb")
DecompressedSize = int.from_bytes(file.read(4), "little")
CompressedData = file.read()
file.close()

DecompressedData = puyo_lz01.Decompress(CompressedData, DecompressedSize)
new_file = open("sn_dec.bin", "wb")
new_file.write(DecompressedData)
new_file.close()

os.makedirs("sn", exist_ok=True)

file = open("sn_dec.bin", "rb")

Offsets = []
Sizes = []

header_size = int.from_bytes(file.read(0x4), byteorder="little")
file.seek(0)

while(file.tell() < header_size):
    Offsets.append(int.from_bytes(file.read(0x4), byteorder="little"))
    Sizes.append(int.from_bytes(file.read(0x4), byteorder="little"))
    file.seek(8, 1)

for i in range(0, len(Offsets)):
    file.seek(Offsets[i])
    file_new = open("sn/%04d.bin" % (i), "wb")
    file_new.write(file.read(Sizes[i]))
    file_new.close()

files = glob.glob("sn/*.bin")

os.makedirs("jsons", exist_ok=True)

ERROR_COUNT = []

EOF_file = open(files[len(files) - 1], "rb")
temp = EOF_file.read()
EOF_filesize = EOF_file.tell()
EOF_file.seek(0)
EOF_bases = []
EOF_bases2 = []
for i in range(len(files) - 1):
	EOF_bases.append(EOF_file.read(16))
EOF_file.close()
x = 0
while (x < EOF_filesize):
	entry = {}
	entry["STRING_COUNT"] = int.from_bytes(temp[x:x+4], "little", signed=True)
	entry["VALUE2"] = int.from_bytes(temp[x+4:x+8], "little", signed=True)
	entry["VALUE3"] = int.from_bytes(temp[x+8:x+12], "little", signed=True)
	entry["ID"] = int.from_bytes(temp[x+12:x+16], "little", signed=True)
	EOF_bases2.append(entry)
	x += 16

if (len(Filenames) != len(files) - 1):
	print("Hardcoded filename list doesn't match count of files.")
	print("Only 0000 and %04d file will be disassembled. You can fill out filename list based on 0000." % (len(files) - 1))
	files = [files[0], files[len(files) - 1]]

for i in range(0, len(files) - 1):
	print(files[i])
	file = open(files[i], "rb")
	Utils.string_counter = 0

	temp_buffer = file.read()
	size = file.tell()
	file.seek(0, 0)
	end_pos = temp_buffer.rfind(EOF_bases[i])

	OUTPUT = {}
	OUTPUT["HEADER"] = []
	OUTPUT["COMMANDS"] = []
	header_size = int.from_bytes(file.read(0x4), byteorder="little")
	assert(header_size % 4 == 0)
	while(file.tell() < header_size):
		OUTPUT["HEADER"].append("0x%X" % int.from_bytes(file.read(0x4), byteorder="little", signed=True))
	while (file.tell() < end_pos):
		cmd = int.from_bytes(file.read(0x1), byteorder="little")
		try:
			OUTPUT["COMMANDS"].append(ProcessCMD(cmd, file, end_pos))
		except:
			entry = {}
			entry["ERROR"] = "ERROR"
			OUTPUT["COMMANDS"].append(entry)
			ERROR_COUNT.append(Path(files[i]).stem)
			break
	OUTPUT["FOOTER"] = {}
	OUTPUT["FOOTER"]["STRING_COUNT"] = int.from_bytes(EOF_bases[i][0:4], "little")
	OUTPUT["FOOTER"]["CHOICES_COUNT"] = int.from_bytes(EOF_bases[i][4:8], "little")
	OUTPUT["FOOTER"]["JUMP_POINTS"] = int.from_bytes(EOF_bases[i][8:12], "little")
	OUTPUT["FOOTER"]["ID"] = int.from_bytes(EOF_bases[i][12:16], "little", signed=True)

	os.makedirs(os.path.dirname("jsons/%s.json" % Filenames[i]), exist_ok=True)
	file_new = open("jsons/%s.json" % Filenames[i], "w", encoding="UTF-8")
	json.dump(OUTPUT, file_new, indent="\t", ensure_ascii=False)
	file_new.close()

	if (OUTPUT["FOOTER"]["JUMP_POINTS"] == 0):
		assert(OUTPUT["FOOTER"]["JUMP_POINTS"] == len(Utils.JUMP_POINTS))
		Utils.JUMP_POINTS.append(header_size)
		OUTPUT["FOOTER"]["JUMP_POINTS"] = 1
	
	if (Utils.string_counter != OUTPUT["FOOTER"]["STRING_COUNT"]):
		print("Expected string count with ID: %d, got: %d" % (OUTPUT["FOOTER"]["STRING_COUNT"], Utils.string_counter))
		sys.exit()

	Utils.JUMP_POINTS = []

if (len(ERROR_COUNT) > 0):
	print("Files that failed disassembling:")
	for i in range(len(ERROR_COUNT)):
		print("%s - %s" % (ERROR_COUNT[i], Filenames[int(ERROR_COUNT[i], base=10)]))