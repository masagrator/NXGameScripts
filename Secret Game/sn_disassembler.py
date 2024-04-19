import json
import os
import sys
import glob
import puyo_lz01
from pathlib import Path

#0x11CFF8 - function array

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("shift_jis_2004"))
		chars.append(c)

def ProcessCMD(cmd: int, file, size):
	entry = {}
	entry["LABEL"] = "0x%X" % (file.tell() - 1)
	match(cmd):
		case 0:
			entry["CMD"] = "%X" % cmd
		case 1:
			entry["CMD"] = "IFGOTO"
			entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		# case 2:
		# 	entry["CMD"] = "JMP"
		# 	entry["ID"] = int.from_bytes(file.read(0x4), byteorder="little")
		# case 3:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		case 4:
			entry["CMD"] = "JMP4"
			entry["ID"] = int.from_bytes(file.read(0x4), byteorder="little")
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
		case 9:
			entry["CMD"] = "IFGOTO9"
			entry["DATA"] = file.read(0x4).hex()
			entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		case 0xA:
			entry["CMD"] = "IFGOTOA"
			entry["DATA"] = file.read(0x4).hex()
			entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		case 0xB:
			entry["CMD"] = "IFGOTOB"
			entry["DATA"] = file.read(0x4).hex()
			entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		case 0xC:
			entry["CMD"] = "IFGOTOC"
			entry["DATA"] = file.read(0x2).hex()
			entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		case 0xD:
			entry["CMD"] = "GOTO"
			entry["DATA"] = file.read(0x2).hex()
			entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
			if (file.read(0x1) != b"\x00"):
				file.seek(-1, 1)
			else:
				entry["DATA2"] = 0
		case 0xE:
			entry["CMD"] = "IFGOTOE"
			entry["DATA"] = file.read(0x2).hex()
			count = int.from_bytes(file.read(0x2), byteorder="little")
			new_list = []
			for x in range(0, count):
				entry2 = {}
				entry2["VALUE"] = int.from_bytes(file.read(0x2), byteorder="little")
				entry2["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
				new_list.append(entry2)
			entry["LIST"] = new_list
		# case 0xF:
		# 	entry["CMD"] = "%X" % cmd
		# 	print("0xF is a nullsub!")
		# 	print("Offset: 0x%X" % file.tell())
		case 0x10:
			entry["CMD"] = "CMP"
			entry["DATA"] = file.read(0x4).hex()
		case 0x11:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x12:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x13:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x14:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x15:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x16:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		# case 0x17:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		case 0x18:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		# case 0x19:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x8).hex()
		case 0x1A:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x1B:
			entry["CMD"] = "%X" % cmd
		case 0x1C:
			entry["CMD"] = "%X" % cmd
		case 0x1D:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x6).hex()
		case 0x1E:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0xA).hex()
		case 0x1F:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0xC).hex()
		case 0x20:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x6).hex()
		case 0x21:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x6).hex()
		case 0x22:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x23:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x8).hex()
		# case 0x24:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x6).hex()
		case 0x25:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		# case 0x26:
		# 	entry["CMD"] = "%X" % cmd
		# case 0x27:
		# 	entry["CMD"] = "%X" % cmd
		# case 0x28:
		# 	entry["CMD"] = "%X" % cmd
		# 	print("DETECTED 0x28")
		# 	entry["DATA"] = file.read(0x3).hex()
		# case 0x29:
		# 	entry["CMD"] = "%X" % cmd
		# 	print("DETECTED 0x29")
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x2A:
		# 	entry["CMD"] = "%X" % cmd
		# case 0x2B:
		# 	entry["CMD"] = "%X" % cmd
		case 0x2C:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		case 0x2D:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x2E:
			entry["CMD"] = "%X" % cmd
		case 0x2F:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		case 0x30:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0xA).hex()
		# case 0x31:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex() # Always "8080"
		# 	count = int.from_bytes(file.read(0x2), byteorder="little")
		# 	entry["UNK0"] = int.from_bytes(file.read(0x2), byteorder="little")
		# 	new_list = []
		# 	for x in range(0, count):
		# 		entry2 = {}
		# 		entry2["ID"] = int.from_bytes(file.read(0x1), byteorder="little")
		# 		entry2["DATA"] = file.read(0x5).hex()
		# 		entry2["JUMP_TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
		# 		entry2["STRING"] = readString(file)
		# 		new_list.append(entry2)
		# 	entry["LIST"] = new_list
		case 0x32:
			entry["CMD"] = "SELECT"
			entry["DATA"] = file.read(0x2).hex() # Always "8080"
			count = int.from_bytes(file.read(0x2), byteorder="little")
			entry["UNK0"] = int.from_bytes(file.read(0x2), byteorder="little")
			new_list = []
			for x in range(0, count):
				entry2 = {}
				entry2["ID"] = int.from_bytes(file.read(0x1), byteorder="little")
				entry2["DATA"] = file.read(0x5).hex()
				entry2["JUMP_TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
				entry2["STRING"] = readString(file)
				new_list.append(entry2)
			entry["LIST"] = new_list
		# case 0x33:
		# 	entry["CMD"] = "%X" % cmd
		case 0x34:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0xA).hex()
		case 0x35:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x36:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x3).hex()
		# case 0x37:
		# 	entry["CMD"] = "%X" % cmd
		# 	print("0x37 is a nullsub!")
		case 0x38:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x3).hex()
		case 0x39:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x3A:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x3B:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		case 0x3C:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		# case 0x3D:
		# 	entry["CMD"] = "%X" % cmd
		# case 0x3E:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x3F:
		# 	entry["CMD"] = "%X" % cmd
		# 	print("0x3F is a nullsub!")
		# case 0x40:
		# 	entry["CMD"] = "%X" % cmd
		# 	print("0x40 is a nullsub!")
		# case 0x41:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x1).hex()
		case 0x42:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x8).hex()
		case 0x43:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x44:
			entry["CMD"] = "VOICE"
			type = int.from_bytes(file.read(0x2), byteorder="little")
			if (type == 10):
				entry["VOICE_ID"] = int.from_bytes(file.read(0x2), byteorder="little")
			else:
				print("UNKNOWN 0x44 type!")
				print("0x%X" % file.tell())
				sys.exit()
		case 0x45:
			entry["CMD"] = "TEXT2"
			type = int.from_bytes(file.read(0x2), byteorder="little", signed=True)
			if (type == -1):
				ID = int.from_bytes(file.read(0x2), byteorder="little", signed=True)
				if (ID < 0):
					entry["ID"] = ID
				entry["STRING"] = readString(file)
			else:
				print("UNKNOWN 0x45 TYPE! %X" % type)
				print("0x%X" % file.tell())
				sys.exit()
		case 0x46:
			entry["CMD"] = "TEXT3"
			type = int.from_bytes(file.read(0x2), byteorder="little", signed=True)
			if (type == -1):
				ID = int.from_bytes(file.read(0x2), byteorder="little")
				entry["STRING"] = readString(file)
			else:
				print("UNKNOWN 0x46 TYPE! %X" % type)
				print("0x%X" % file.tell())
				sys.exit()
		case 0x47:
			entry["CMD"] = "TEXT"
			type = int.from_bytes(file.read(0x2), byteorder="little", signed=True)
			if (type == -1):
				entry["TYPE"] = "MESSAGE"
				ID = int.from_bytes(file.read(0x2), byteorder="little")
				entry["STRING"] = readString(file)
			elif (type == 13):
				entry["TYPE"] = "NAME"
				entry["STRING"] = readString(file)
			else:
				print("UNKNOWN 0x47 TYPE! %X" % type)
				print("0x%X" % file.tell())
				sys.exit()
		case 0x48:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex() # Always "FFFF"
		case 0x49:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex() # Always "FFFFFFFF"
		case 0x4A:
			entry["CMD"] = "KEY_WAIT"
			entry["DATA"] = file.read(0x2).hex() # Always "FFFF"
		case 0x4B:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x4C:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x6).hex()
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
		# case 0x51:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x6).hex()
		# case 0x52:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0xA).hex()
		# case 0x53:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x54:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x8).hex()
		case 0x55:
			entry["CMD"] = "TITLE"
			string_offset = int.from_bytes(file.read(4), "little")
			entry["NEXT"] = {}
			next_cmd = int.from_bytes(file.read(1), "little")
			entry["NEXT"]["CMD"] = "%X" % next_cmd
			match(next_cmd):
				case 1:
					entry["NEXT"]["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
				case _:
					print("UNEXPECTED NEXTCMD IN 0x55!")
					print(entry["NEXT"]["CMD"])
					sys.exit()
			file.seek(string_offset)
			entry["STRING"] = readString(file)
		# case 0x56:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x57:
		# 	entry["CMD"] = "%X" % cmd
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
		case 0x5E:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		case 0x5F:
			entry["CMD"] = "%X" % cmd
			flag = int.from_bytes(file.read(1), "little")
			entry["FLAG"] = flag
			if (flag > 0):
				match(flag):
					case 1:
						entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
					case _:
						print("UNKNOWN 0x5F flag!")
						sys.exit()
			entry["DATA"] = file.read(0xF).hex()
		case 0x60:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x6).hex()
		# case 0x61:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x6).hex()
		case 0x62:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x63:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0xA).hex()
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
		# 	entry["CMD"] = "%X" % cmd
		# 	print("0x67 is a nullsub!")
		case 0x68:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0xA).hex()
		case 0x69:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		# case 0x6A:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex() # Always "FFFFFFFF"
		case 0x6B:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		case 0x6C:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x10).hex()
		# case 0x6D:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x6E:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x6F:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x6).hex()
		# case 0x70:
		# 	entry["CMD"] = "%X" % cmd
		case 0x71:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x6).hex()
		case 0x72:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
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
		# 	entry["CMD"] = "%X" % cmd
		# 	print("0x76 is a nullsub!")
		# case 0x77:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x78:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		case 0x79:
			entry["CMD"] = "%X" % cmd
			string_offset = int.from_bytes(file.read(4), "little")
			entry["NEXT"] = {}
			next_cmd = int.from_bytes(file.read(1), "little")
			entry["NEXT"]["CMD"] = "%X" % next_cmd
			match(next_cmd):
				case 1:
					entry["NEXT"]["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
				case _:
					print("UNEXPECTED NEXTCMD IN 0x79!")
					print(entry["NEXT"]["CMD"])
					sys.exit()
			file.seek(string_offset)
			entry["STRING"] = readString(file)
		case 0x7A:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x7B:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex() # Always "00002c01"
		# case 0x7C:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x7D:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		case 0x7E:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		case 0x7F:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x80:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		case 0x81:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		case 0x82:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		case 0x83:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex() # Always "ff800300"
			new_entries = int.from_bytes(file.read(2), "little")
			entry["NEW_CMDS"] = []
			for i in range(new_entries+1):
				flag = int.from_bytes(file.read(1), "little")
				entry["NEW_CMDS"].append(ProcessCMD(flag, file, size))
			entry["STRING"] = readString(file)
		case 0x84:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x2).hex()
		case 0x85:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex() # Always "FFFFFFFF"
			entry["STRING"] = readString(file)
		case 0x86:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
			entry["STRING"] = readString(file)
		# case 0x87:
		# 	entry["CMD"] = "%X" % cmd
		# 	print("0x87 is a nullsub!")
		# case 0x88:
		# 	entry["CMD"] = "%X" % cmd
		# 	print("0x88 is a nullsub!")
		# case 0x89:
		# 	entry["CMD"] = "%X" % cmd
		# 	print("0x89 is a nullsub!")
		# case 0x8A:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x2).hex()
		# case 0x8B:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		case 0x8C:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
		# case 0x8D:
		# 	entry["CMD"] = "%X" % cmd
		# case 0x8E:
		# 	entry["CMD"] = "%X" % cmd
		# 	print("0x8E is a nullsub!")
		# case 0x8F:
		# 	entry["CMD"] = "%X" % cmd
		# 	print("0x8F is a nullsub!")
		# case 0x90:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# case 0x91:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# 	entry["STRING"] = readString(file)
		# case 0x92:
		# 	entry["CMD"] = "%X" % cmd
		# 	entry["DATA"] = file.read(0x4).hex()
		# 	entry["STRING"] = readString(file)
		case 0x93:
			entry["CMD"] = "%X" % cmd
			entry["DATA"] = file.read(0x4).hex()
			entry["STRING"] = readString(file)
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
os.makedirs("Decompressed", exist_ok=True)
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

file_new = open("jsons/%s.json" % Path(files[len(files) - 1]).stem, "w", encoding="UTF-8")
json.dump(EOF_bases2, file_new, indent="\t", ensure_ascii=False)
file_new.close()

for i in range(len(files) - 1):
	print(files[i])
	file = open(files[i], "rb")

	temp_buffer = file.read()
	size = file.tell()
	file.seek(0, 0)
	end_pos = temp_buffer.rfind(EOF_bases[i])

	OUTPUT = {}
	OUTPUT["HEADER"] = []
	OUTPUT["COMMANDS"] = []
	header_size = int.from_bytes(file.read(0x4), byteorder="little")
	while(file.tell() < header_size):
		OUTPUT["HEADER"].append(int.from_bytes(file.read(0x4), byteorder="little", signed=True))
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
	
	OUTPUT["FOOTER"] = EOF_bases[i].hex()

	if (34 >= i >= 3):
		file_new = open("jsons/KQA%02d.json" % (i - 2), "w", encoding="UTF-8")
	elif (70 >= i >= 35):
		file_new = open("jsons/KQB%02d.json" % (i - 34), "w", encoding="UTF-8")
	elif (97 >= i >= 71):
		file_new = open("jsons/KQC%02d.json" % (i - 70), "w", encoding="UTF-8")
	elif (143 >= i >= 98):
		file_new = open("jsons/KQD%02d.json" % (i - 97), "w", encoding="UTF-8")
	else:
		file_new = open("jsons/%s.json" % Path(files[i]).stem, "w", encoding="UTF-8")
	json.dump(OUTPUT, file_new, indent="\t", ensure_ascii=False)
	file_new.close()

if (len(ERROR_COUNT) > 0):
	print("Files that failed disassembling:")
	print(ERROR_COUNT)