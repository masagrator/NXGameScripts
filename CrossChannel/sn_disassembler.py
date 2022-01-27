import json
import os
import sys
import glob

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("shift_jis_2004"))
		chars.append(c)

files = glob.glob("sn/*.bin")

os.makedirs("jsons", exist_ok=True)

for i in range(len(files)):
	if (files[i][3:7] == "0316"):
		print("0316 is not a valid script file. Ignoring...")
		continue
	print(files[i])
	file = open(files[i], "rb")

	file.seek(0, 2)
	size = file.tell()
	file.seek(0, 0)

	OUTPUT = []

	header_size = int.from_bytes(file.read(0x4), byteorder="little")
	file.seek(header_size)
	while (file.tell() < size):
		entry = {}
		entry["LABEL"] = "0x%X" % file.tell()
		cmd = int.from_bytes(file.read(0x1), byteorder="little")
		match(cmd):
			case 0:
				entry["CMD"] = "%X" % cmd
				while(file.tell() < size):
					test = file.read(0x1)
					if ((test != b"\x00") and (test != b"\xFF")):
						print("DETECTED WRONG NOP AT 0x%X" % (file.tell() - 1))
						print(test)
						sys.exit()
				continue
			case 1:
				entry["CMD"] = "JZ_TO_LABEL"
				entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
			case 2:
				entry["TYPE"] = "JMP_TO_ID"
				entry["ID"] = int.from_bytes(file.read(0x4), byteorder="little")
			# case 3:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
			case 4:
				entry["TYPE"] = "JMP_TO_ID2"
				entry["DATA"] = file.read(0x2).hex()
				entry["ID2"] = int.from_bytes(file.read(0x2), byteorder="little")
			case 5:
				entry["CMD"] = "RETURN"
				if (file.read(0x1) == b"\x05"):
					file.seek(-1, 1)
					entry["DATA"] = file.read().hex()
				else:
					file.seek(-1, 1)
			case 6:
				entry["CMD"] = "IF_EQ_JMP_TO_LABEL"
				entry["DATA"] = file.read(0x4).hex()
				entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
			case 7:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x8).hex()
			case 8:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x8).hex()
			# case 9:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x8).hex()
			case 0xA:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x8).hex()
			case 0xB:
				entry["CMD"] = "IF_TRUE_JMP_TO_LABEL"
				entry["DATA"] = file.read(0x4).hex()
				entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
			case 0xC:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x6).hex()
			case 0xD:
				entry["CMD"] = "JMP_TO_LABEL2"
				entry["DATA"] = file.read(0x2).hex()
				entry["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
				if (file.read(0x1) != b"\x00"):
					file.seek(-1, 1)
			case 0xE:
				entry["CMD"] = "IF_EQ_JMP_TO_LABEL2"
				entry["DATA"] = file.read(0x2).hex()
				count = int.from_bytes(file.read(0x2), byteorder="little")
				new_list = []
				for x in range(0, count):
					entry2 = {}
					entry2["VALUE"] = int.from_bytes(file.read(0x2), byteorder="little")
					entry2["TO_LABEL"] = "0x%X" % int.from_bytes(file.read(0x4), byteorder="little")
					new_list.append(entry2)
				entry["LIST"] = new_list
			case 0xF:
				entry["CMD"] = "%X" % cmd
				print("0xF is a nullsub! Disassembling failed!")
				print("Offset: 0x%X" % file.tell())
				sys.exit()
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
			# case 0x15:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
			# case 0x16:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
			# case 0x17:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
			# case 0x18:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x2).hex()
			# case 0x19:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x8).hex()
			case 0x1A:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x4).hex()
			case 0x1B:
				entry["CMD"] = "%X" % cmd
				pass
			case 0x1C:
				entry["CMD"] = "%X" % cmd
				pass
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
			case 0x24:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x6).hex()
			case 0x25:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x4).hex()
			# case 0x26:
			# 	entry["CMD"] = "%X" % cmd
			# 	pass
			# case 0x27:
			# 	entry["CMD"] = "%X" % cmd
			# 	pass
			# case 0x28:
			# 	entry["CMD"] = "%X" % cmd
			# 	print("DETECTED 0x28")
			# 	input()
			# 	entry["DATA"] = file.read(0x2).hex()
			# case 0x29:
			# 	entry["CMD"] = "%X" % cmd
			# 	print("DETECTED 0x29")
			# 	input()
			# 	entry["DATA"] = file.read(0x2).hex()
			# case 0x2A:
			# 	entry["CMD"] = "%X" % cmd
			# 	pass
			# case 0x2B:
			# 	entry["CMD"] = "%X" % cmd
			# 	pass
			# case 0x2C:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x2).hex()
			case 0x2D:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x4).hex()
			case 0x2E:
				entry["CMD"] = "%X" % cmd
				pass
			case 0x2F:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x2).hex()
			case 0x30:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0xA).hex()
			case 0x31:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x2).hex()
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
			case 0x32:
				entry["CMD"] = "SELECT"
				entry["DATA"] = file.read(0x2).hex()
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
			case 0x33:
				entry["CMD"] = "%X" % cmd
				pass
			case 0x34:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0xA).hex()
			# case 0x35:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
			case 0x36:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x3).hex()
			# case 0x37:
			# 	entry["CMD"] = "%X" % cmd
			# 	pass
			# case 0x38:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x2).hex()
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
			# 	pass
			# case 0x3E:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
			case 0x3F:
				entry["CMD"] = "%X" % cmd
				print("0x3F is a nullsub! Disassembling failed!")
				print("Offset: 0x%X" % file.tell())
				sys.exit()
			case 0x40:
				entry["CMD"] = "%X" % cmd
				print("0x40 is a nullsub! Disassembling failed!")
				print("Offset: 0x%X" % file.tell())
				sys.exit()
			# case 0x41:
			# 	entry["CMD"] = "%X" % cmd
			#	pass
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
					entry["TYPE"] = "WITH_TEXT"
					entry["VOICE_ID"] = int.from_bytes(file.read(0x2), byteorder="little")
					entry["DATA"] = file.read(0x2).hex()
					check = file.read(0x2)
					if (check == b"\xFF\xFF"):
						ID = int.from_bytes(file.read(0x2), byteorder="little")
						entry["STRING"] = readString(file)
					else:
						file.seek(-2, 1)
						entry["TYPE"] = "WITHOUT_TEXT"
						entry["DATA"] += file.read(0x4).hex()
				else:
					print("UNKNOWN 0x44 type!")
					print("0x%X" % file.tell())
					sys.exit()
			case 0x45:
				entry["CMD"] = "MC_TEXT"
				type = int.from_bytes(file.read(0x2), byteorder="little", signed=True)
				if (type == -1):
					entry["TYPE"] = "MESSAGE"
					ID = int.from_bytes(file.read(0x2), byteorder="little")
					entry["STRING"] = readString(file)
				else:
					print("UNKNOWN 0x45 TYPE! %X" % type)
					print("0x%X" % file.tell())
					sys.exit()
			# case 0x46:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x2).hex()
			# 	type = int.from_bytes(file.read(0x2), byteorder="little", signed=True)
			# 	if (type == -1):
			# 		entry["TYPE"] = "MESSAGE"
			# 		ID = int.from_bytes(file.read(0x2), byteorder="little")
			# 		entry["STRING"] = readString(file)
			# 	else:
			# 		print("UNKNOWN 0x46 TYPE! %X" % type)
			# 		print("0x%X" % file.tell())
			# 		sys.exit()
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
				entry["DATA"] = file.read(0x2).hex()
			case 0x49:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x4).hex()
			case 0x4A:
				entry["CMD"] = "KEY_WAIT"
				entry["DATA"] = file.read(0x2).hex()
			case 0x4B:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x4).hex()
			case 0x4C:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x6).hex()
			# case 0x4D:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0xA).hex()
			# case 0x4E:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
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
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
			# case 0x56:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x2).hex()
			# case 0x57:
			# 	entry["CMD"] = "%X" % cmd
			# 	pass
			# case 0x58:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x2).hex()
			# case 0x59:
			# 	entry["CMD"] = "%X" % cmd
			# 	pass
			case 0x5A:
				entry["CMD"] = "%X" % cmd
				pass
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
			case 0x5F:
				entry["CMD"] = "%X" % cmd
				pass
			# case 0x60:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
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
			case 0x67:
				entry["CMD"] = "%X" % cmd
				print("0x67 is a nullsub! Disassembling failed!")
				print("Offset: 0x%X" % file.tell())
				sys.exit()
			case 0x68:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0xA).hex()
			case 0x69:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x2).hex()
			case 0x6A:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x4).hex()
			# case 0x6B:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x2).hex()
			case 0x6C:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x10).hex()
			# case 0x6D:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x2).hex()
			case 0x6E:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x4).hex()
			# case 0x6F:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x6).hex()
			# case 0x70:
			# 	entry["CMD"] = "%X" % cmd
			# 	pass
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
			case 0x76:
				entry["CMD"] = "%X" % cmd
				print("0x76 is a nullsub! Disassembling failed!")
				print("Offset: 0x%X" % file.tell())
				sys.exit()
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
			# 	entry["DATA"] = file.read(0x6).hex()
			case 0x7B:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x4).hex()
			# case 0x7C:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
			# case 0x7D:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x2).hex()
			# case 0x7E:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x2).hex()
			# case 0x7F:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
			# case 0x80:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
			case 0x81:
				entry["CMD"] = "%X" % cmd
				print("0x81 is a nullsub! Disassembling failed!")
				print("Offset: 0x%X" % file.tell())
				sys.exit()
			case 0x82:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x2).hex()
			case 0x83:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x4).hex()
			case 0x84:
				entry["CMD"] = "%X" % cmd
				print("0x84 is a nullsub! Disassembling failed!")
				print("Offset: 0x%X" % file.tell())
				sys.exit()
			case 0x85:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x4).hex()
				entry["STRING"] = readString(file)
			case 0x86:
				entry["CMD"] = "%X" % cmd
				entry["DATA"] = file.read(0x4).hex()
				entry["STRING"] = readString(file)
			case 0x87:
				entry["CMD"] = "%X" % cmd
				print("0x87 is a nullsub! Disassembling failed!")
				print("Offset: 0x%X" % file.tell())
				sys.exit()
			case 0x88:
				entry["CMD"] = "%X" % cmd
				print("0x88 is a nullsub! Disassembling failed!")
				print("Offset: 0x%X" % file.tell())
				sys.exit()
			case 0x89:
				entry["CMD"] = "%X" % cmd
				print("0x89 is a nullsub! Disassembling failed!")
				print("Offset: 0x%X" % file.tell())
				sys.exit()
			# case 0x8A:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x2).hex()
			# case 0x8B:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
			# case 0x8C:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
			# case 0x8D:
			# 	entry["CMD"] = "%X" % cmd
			# 	pass
			case 0x8E:
				entry["CMD"] = "%X" % cmd
				print("0x8E is a nullsub! Disassembling failed!")
				print("Offset: 0x%X" % file.tell())
				sys.exit()
			case 0x8F:
				entry["CMD"] = "%X" % cmd
				print("0x90is a nullsub! Disassembling failed!")
				print("Offset: 0x%X" % file.tell())
				sys.exit()
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
			# case 0x93:
			# 	entry["CMD"] = "%X" % cmd
			# 	entry["DATA"] = file.read(0x4).hex()
			# 	entry["STRING"] = readString(file)
			case _:
				entry["CMD"] = "%X" % cmd
				print("UNKNOWN COMMAND: 0x%X" % cmd)
				print("OFFSET: 0x%X" % (file.tell() - 1))
				sys.exit()
		OUTPUT.append(entry)

	file_new = open("jsons/%s.json" % files[i][3:-4], "w", encoding="UTF-8")
	json.dump(OUTPUT, file_new, indent="\t", ensure_ascii=False)
	file_new.close()