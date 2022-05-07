import json
import glob
import os
import sys
import struct

def GetFileSize(file):
	pos = file.tell()
	file.seek(0, 2)
	size = file.tell()
	file.seek(pos)
	return size

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("UTF-8"))
		chars.append(c)

def readStringDialog(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		test = int.from_bytes(c, byteorder="little")
		if (0xE0 > test >= 0xC0):
			chars.append(c)
			chars.append(myfile.read(1))
		elif (0xE0 <= test <= 0xF7):
			chars.append(c)
			chars.append(myfile.read(1))
			chars.append(myfile.read(1))
		elif (test > 0xF7):
			chars.append(c)
		elif (test >= 0x20):
			chars.append(c)
		elif test < 0x20:
			myfile.seek(-1, 1)
			return str(b"".join(chars).decode("UTF-8"))

def ReadDialog(file, entry):
	entry["DIALOG"] = {}
	entry["DIALOG"]["STRINGS"] = []
	while(True):
		control = int.from_bytes(file.read(1), byteorder="little")
		type_check = [8, 9, 0xB, 0xC, 0xF]
		if (control in type_check):
			entry["DIALOG"]["STRINGS"].append('CMD: %d' % control)
			entry["DIALOG"]["STRINGS"].append(readStringDialog(file))
			continue
		match(control):
			case 0:
				return
			
			case 1:
				entry["DIALOG"]["STRINGS"].append("NEW_LINE")
			
			case 2:
				entry["DIALOG"]["STRINGS"].append("KEY_WAIT")
			
			case 3:
				entry["DIALOG"]["STRINGS"].append("CLEAR_TEXT")
				entry["DIALOG"]["STRINGS"].append(readStringDialog(file))
			
			case 6:
				entry["DIALOG"]["STRINGS"].append("SHOW_ALL")
				entry["DIALOG"]["STRINGS"].append(readStringDialog(file))
			
			case 7:
				entry["DIALOG"]["STRINGS"].append("SET_COLOR")
				entry["DIALOG"]["STRINGS"].append(readStringDialog(file))

			case 0x10:
				entry["DIALOG"]["STRINGS"].append("ITEM_ID: %d" % int.from_bytes(file.read(2), byteorder="little"))

			case 0x11:
				entry["DIALOG"]["STRINGS"].append("VOICE_FILE_ID: %d" % int.from_bytes(file.read(4), byteorder="little"))
				entry["DIALOG"]["STRINGS"].append(readStringDialog(file))
			
			case 0x12:
				entry["DIALOG"]["STRINGS"].append('CMD: %d' % control)
				entry["DIALOG"]["STRINGS"].append('CMD18_ARG: %d' % int.from_bytes(file.read(4), byteorder="little"))
				entry["DIALOG"]["STRINGS"].append(readStringDialog(file))

			case 0x13:
				entry["DIALOG"]["STRINGS"].append('CMD: %d' % control)
			
			case 0x23:
				file.seek(-1, 1)
				entry["DIALOG"]["STRINGS"].append(readStringDialog(file))
			
			case _:
				if (control  >= 0x20):
					file.seek(-1, 1)
					entry["DIALOG"]["STRINGS"].append(readStringDialog(file))
				else:
					print("UNKNOWN DIALOG COMMAND: 0x%x" % control)
					print("OFFSET: 0x%x" % (file.tell() - 1))
					sys.exit()

def CalcGoto(file, entry, end):
	entry["TABLE"] = []
	entry2 = {}
	control = int.from_bytes(file.read(1), byteorder="little")
	passing = [2, 3, 4, 5, 6, 7, 8, 9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0x10, 0x11, 0x12, 0x13, 0x17, 0x18, 0x22, 0x1D]
	while (control != 1):
		entry2 = {}
		entry2["CONTROL"] = control
		if (control in passing):
			entry["TABLE"].append(entry2)
			control = int.from_bytes(file.read(1), byteorder="little")
			continue
		match(control):
			case 0:
				entry2["UNK"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]
			
			case 0x1E:
				entry2["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]

			case 0x1F:
				entry2["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]

			case 0x20:
				entry2["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			
			case 0x21:
				entry2["UNK"] = file.read(3).hex().upper()

			case 0x23:
				entry2["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			
			case 0x24:
				entry2["UNK"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]

			case 0x25:
				entry2["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			
			case 0x1C:
				cmd = int.from_bytes(file.read(1), byteorder="little")
				entry2["INSTRUCTION"] = GenerateCommand(cmd, file, end)
			
			case _:
				print("UNKNOWN GOTO COMMAND: 0x%x" % control)
				print("OFFSET: 0x%x" % (file.tell() - 1))
				sys.exit()
		
		entry["TABLE"].append(entry2)
		control = int.from_bytes(file.read(1), byteorder="little")
		

def GenerateTable(cmd, file, end):
	entry = {}
	entry["LABEL"] = "0x%x" % (file.tell() - 1)
	entry["TYPE"] = cmd
	match(cmd):
		case 3 | 1 | 8 | 2 | 9:
			entry["UNK"] = file.read(7).hex().upper()
			temp = file.tell()
			entry["STRINGS"] = [readString(file)]
			file.seek(temp + 0x20)
		case 4 | 7 | 5:
			entry["UNK"] = file.read(0x27).hex().upper()
		case 0:
			entry["UNK"] = file.read(end - file.tell()).hex().upper()
		case _:
			print("UNKNOWN TABLE TYPE. DISASSEMBLING FAILED")
			print("TYPE: %d" % cmd)
			print("OFFSET: 0x%x" % (file.tell() - 1))
			sys.exit()
	return entry

def AnimeClipTable(cmd, file, end):
	entry = {}
	entry["LABEL"] = "0x%x" % (file.tell() - 1)
	match(cmd):
		case 0:
			test = int.from_bytes(file.read(3), byteorder="little")
			match(test):
				case 0:
					if ((end - file.tell()) < 16):
						entry["TYPE"] = "0x0"
						entry["SUBTYPE"] = "0x0"
						entry["DATA"] = file.read(end - file.tell()).hex().upper()
						file.seek(end)
						return entry
					else:
						print("NOP DETECTED. DISASSEMBLING FAILED")
						print("OFFSET: 0x%x" % (file.tell() - 1))
						sys.exit()
				case _:
					entry["TYPE"] = "0x0"
					entry["SUBTYPE"] = "0x%x" % test
					new_offset = file.tell() + 0x20
					entry["STRINGS"] = [readString(file)]
					file.seek(new_offset)
					entry["STRINGS"].append(readString(file))
					file.seek(new_offset + 0x20)

		case _:
			test = int.from_bytes(file.read(3), byteorder="little")
			assert(test == 0)
			entry["TYPE"] = "0x%x" % cmd
			new_offset = file.tell() + 0x20
			entry["STRINGS"] = [readString(file)]
			file.seek(new_offset)
			entry["STRINGS"].append(readString(file))
			file.seek(new_offset + 0x20)
		
	return entry

def GenerateCommand(cmd, file, end):
	entry = {}
	entry["LABEL"] = "0x%x" % (file.tell() - 1)
	#print("0x%x" % cmd)
	#print("0x%x" % file.tell())
	match(cmd):
		case 0:
			if ((end - file.tell()) < 16):
				file.seek(end)
				return None
			else:
				print("NOP DETECTED. DISASSEMBLING FAILED")
				print("OFFSET: 0x%x" % (file.tell() - 1))
				sys.exit()
		case 1:
			entry["TYPE"] = "RETURN"
		
		case 2:
			entry["TYPE"] = "JUMP_TO_FUNCTION"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
		
		case 3:
			entry["TYPE"] = "GOTO3"
			entry["TO_LABEL"] = "0x%x" % int.from_bytes(file.read(4), byteorder="little")
		
		case 4:
			entry["TYPE"] = "0x4"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]

		case 5:
			entry["TYPE"] = "GOTO5"
			CalcGoto(file, entry, end)
			entry["TO_LABEL"] = "0x%x" % int.from_bytes(file.read(4), byteorder="little")
		
		case 6:
			entry["TYPE"] = "GOTO6"
			CalcGoto(file, entry, end)
			count = int.from_bytes(file.read(1), byteorder="little")
			entry["TO_LABELS"] = []
			for i in range(0, count):
				entry2 = {}
				entry2["UNK"] = [int.from_bytes(file.read(2), byteorder="little")]
				entry2["TO_LABEL"] = "0x%x" % int.from_bytes(file.read(4), byteorder="little")
				entry["TO_LABELS"].append(entry2)
			entry["TO_LABEL"] = "0x%x" % int.from_bytes(file.read(4), byteorder="little")
		
		case 7:
			entry["TYPE"] = "0x7"
			entry["UNK"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]
		
		case 8:
			entry["TYPE"] = "0x8"
			CalcGoto(file, entry, end)
		
		case 0xA:
			entry["TYPE"] = "0xA"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			CalcGoto(file, entry, end)
		
		case 0xC:
			entry["TYPE"] = "0xC"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0xD:
			entry["TYPE"] = "0xD"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0xE:
			entry["TYPE"] = "0xE"
			entry["UNK"] = file.read(4).hex().upper()
		
		case 0xF:
			entry["TYPE"] = "0xF"
			entry["UNK"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]
		
		case 0x10:
			entry["TYPE"] = "0x10"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x11:
			entry["TYPE"] = "0x11"
			entry["UNK"] = file.read(4).hex().upper()

		case 0x12:
			entry["TYPE"] = "0x12"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			CalcGoto(file, entry, end)
		
		case 0x13:
			entry["TYPE"] = "0x13"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["STRINGS1"] = [readString(file), readString(file), readString(file)]
			entry["UNK1"] = file.read(33).hex().upper()
			entry["STRINGS2"] = [readString(file), readString(file)]
			entry["UNK2"] = file.read(15).hex().upper()
		
		case 0x14:
			entry["TYPE"] = "0x14"
			entry["UNK"] = file.read(4).hex().upper()
			entry["STRINGS"] = [readString(file)]
		
		case 0x15:
			entry["TYPE"] = "0x15"
			entry["UNK"] = file.read(3).hex().upper()
		
		case 0x16:
			entry["TYPE"] = "0x16"
			entry["UNK"] = file.read(3).hex().upper()
		
		case 0x17:
			entry["TYPE"] = "0x17"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]

		case 0x18:
			entry["TYPE"] = "TEXT18"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			ReadDialog(file, entry)

		case 0x19:
			entry["TYPE"] = "0x19"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0 | 5:
					entry["UNK"] = file.read(9).hex().upper()
				
				case 1:
					entry["UNK"] = file.read(5).hex().upper()
				
				case 2:
					entry["UNK"] = file.read(4).hex().upper()
				
				case _:
					print("UNKNOWN 0x19 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x1A:
			entry["TYPE"] = "MESSAGE"
			entry["NAME_ID"] = int.from_bytes(file.read(2), byteorder="little", signed=True)
			ReadDialog(file, entry)

		#Changed
		case 0x1B:
			entry["TYPE"] = "0x1B"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			
		case 0x1C:
			entry["TYPE"] = "CLEAN_TEXT_BOX"
		
		case 0x1D:
			entry["TYPE"] = "OVERRIDE_DIALOG_SPEAKER"
			entry["NAME"] = [readString(file)]
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		#Changed
		case 0x1E:
			entry["TYPE"] = "JUMP_TO_ID"
			entry["STRINGS"] = [readString(file), readString(file)]
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]

		#Changed
		case 0x1F:
			entry["TYPE"] = "0x1F"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			entry["CONTROL2"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			assert(entry["CONTROL2"] < 4)
			match(entry["CONTROL"]):
				case 0:
					entry["UNK"] = file.read(6).hex().upper()
				
				case 1:
					entry["STRINGS"] = [readString(file)]
					entry["UNK"] = file.read(2).hex().upper()
				
				case 2:
					entry["UNK"] = file.read(6).hex().upper()
				
				case 3 | 0xA:
					pass
				
				case 4:
					entry["UNK"] = file.read(1).hex().upper()
				
				case 5:
					entry["UNK"] = file.read(4).hex().upper()
				
				case 6 | 7:
					entry["UNK"] = file.read(2).hex().upper()
				
				case 8:
					entry["STRINGS"] = [readString(file)]
					entry["UNK"] = file.read(10).hex().upper()
				
				case 9:
					entry["STRINGS"] = [readString(file)]
					entry["UNK"] = file.read(4).hex().upper()
				
				case 0xB:
					entry["UNK"] = file.read(2).hex().upper()
				
				case 0xC:
					entry["UNK"] = file.read(2).hex().upper()
				
				case _:
					print("UNKNOWN 0x1F CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 1))
					sys.exit()

		#Changed
		case 0x20:
			entry["TYPE"] = "0x20"
			entry["SIZE_CHECK"] = int.from_bytes(file.read(1), byteorder="little")
			assert(entry["SIZE_CHECK"] <= 3)
			entry["UNK0"] = file.read(2).hex().upper()
			entry["STRINGS"] = [readString(file), readString(file)]
			entry["UNK1"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
		#Changed
		case 0x21:
			entry["TYPE"] = "0x21"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			entry["UNK"] = file.read(6).hex().upper()
			match(entry["CONTROL"]):
				case 0:
					entry["UNK"] += file.read(10).hex().upper()
				case 1:
					entry["UNK"] += file.read(8).hex().upper()
				case _:
					print("UNKNOWN 0x21 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 1))
					sys.exit()
		
		#Changed
		case 0x22:
			entry["TYPE"] = "0x22"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
			entry["UNK1"] = file.read(22).hex().upper()
		
		#Changed
		case 0x23:
			entry["TYPE"] = "0x23"
			entry["UNK"] = file.read(7).hex().upper()

		#Changed
		case 0x24:
			entry["TYPE"] = "0x24"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			entry["UNK"] = file.read(2).hex().upper()
			match(entry["CONTROL"]):
				case 0 | 1 | 2 | 4 | 5 | 0xA | 0xB:
					entry["STRINGS"] = [readString(file), readString(file)]
				case 6 | 7:
					entry["UNK"] += file.read(4).hex().upper()
				case 8:
					entry["UNK"] += file.read(1).hex().upper()
					entry["STRINGS"] = [readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file)]
				case 9:
					entry["UNK"] += file.read(1).hex().upper()
				case 0xD:
					pass
				case 0xE:
					entry["UNK"] += file.read(4).hex().upper()
					entry["STRINGS"] = [readString(file), readString(file)]
				case _:
					print("UNKNOWN 0x24 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 3))
					sys.exit()					

		case 0x25:
			entry["TYPE"] = "0x25"
			entry["UNK0"] = file.read(3).hex().upper()
			entry["STRINGS"] = [readString(file), readString(file)]
			entry["UNK1"] = file.read(36).hex().upper()

		case 0x26:
			entry["TYPE"] = "0x26"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
		
		#Changed
		case 0x27:
			entry["TYPE"] = "0x27"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0xA:
					entry["UNK"] = file.read(3).hex().upper()
					entry["STRINGS"] = [readString(file)]
				case 0xB | 0xD | 0xE | 0xF:
					entry["UNK"] = file.read(3).hex().upper()
				case 0xC:
					entry["UNK0"] = file.read(10).hex().upper()
					entry["STRINGS"] = [readString(file)]
					entry["UNK1"] = file.read(37).hex().upper()
				case 0x10 | 0x11:
					entry["UNK"] = file.read(4).hex().upper()
				case 0x12 | 0x17:
					entry["UNK"] = file.read(5).hex().upper()
				case 0x13 | 0x14:
					entry["UNK"] = file.read(19).hex().upper()
				case 0x15:
					entry["UNK"] = file.read(1).hex().upper()
					entry["STRINGS"] = [readString(file)]
				case 0x16:
					entry["UNK"] = file.read(7).hex().upper()
				case 0x18:
					entry["UNK"] = file.read(11).hex().upper()
				case 0x19:
					entry["STRINGS"] = [readString(file)]
				case 0x1A:
					entry["UNK"] = file.read(2).hex().upper()
				case _:
					print("UNKNOWN 0x27 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		#Changed
		case 0x28:
			entry["TYPE"] = "0x28"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")

			match(entry["CONTROL"]):
				case 0 | 91:
					entry["UNK"] = file.read(5).hex().upper()
				case 1 | 0x1D | 0x36 | 0x20:
					entry["UNK"] = file.read(10).hex().upper()
				case 0x7D | 0x80 | 0x99 | 8 | 6 | 4 | 92 | 0x97 | 0x9D:
					entry["UNK"] = file.read(1).hex().upper()
				case 7 | 5:
					entry["UNK"] = file.read(1).hex().upper()
					entry["STRINGS"] = [readString(file)]
				case 0x81 | 0x9B | 0x8F | 3 | 0x2C | 0x2D | 0x1F | 0x89 | 0x93 | 0x98 | 109 | 108 | 107 | 102 | 101 | 99 | 0x1C | 0x14 | 13 | 0x10 | 72 | 93 | 9 | 94 | 95 | 96 | 115 | 116 | 117 | 121:
					entry["UNK"] = file.read(2).hex().upper()
				case 0x49 | 0xF | 0x8E | 10 | 123 | 0x91 | 0x1A | 0x19 | 0x83 | 0x2E:
					entry["UNK"] = file.read(4).hex().upper()
				case 0x9C | 0x17 | 12 | 0x34 | 90 | 11 | 0x96 | 0x95 | 0xA0 | 0xA1 | 0xA2 | 0xA3 | 0xA4 | 0xA5:
					entry["UNK"] = file.read(6).hex().upper()
				case 0xE | 0x92:
					entry["UNK"] = file.read(8).hex().upper()
				case 0x11 | 122 | 98 | 2 | 0x52:
					entry["UNK"] = file.read(3).hex().upper()
				case 0x12 | 0x13 | 0x35:
					entry["UNK"] = file.read(18).hex().upper()
				case 0x15 | 0x32:
					entry["UNK"] = file.read(22).hex().upper()
				case 0x37:
					entry["UNK"] = file.read(25).hex().upper()
				case 60 | 70:
					entry["UNK"] = file.read(12).hex().upper()
				case 80:
					entry["UNK0"] = file.read(2).hex().upper()
					entry["STRINGS1"] = [readString(file)]
					entry["UNK1"] = file.read(18).hex().upper()
					entry["STRINGS2"] = [readString(file)]
				case 97 | 0x26:
					entry["UNK"] = file.read(19).hex().upper()
				case 100 | 0x53:
					entry["STRINGS"] = [readString(file)]
				case 110:
					entry["UNK"] = file.read(20).hex().upper()
				case 126 | 113:
					entry["UNK"] = file.read(7).hex().upper()
				case 114:
					entry["UNK"] = file.read(11).hex().upper()
				case 0x9F | 0x88 | 0x22 | 0x24 | 0x25 | 0x23 | 0x21 | 0x18 | 105 | 106 | 0x27 | 0x28 | 0x29 | 0x2A | 0x76 | 0x8D | 0x8C | 0x8B | 0x47 | 0x68 | 0x87 | 0x2B | 0x9A | 0x33 | 0x67 | 0x6F | 0x70 | 0x85 | 0x86 | 0x1B | 0x16 | 0x7F | 0x8A:
					pass
				case 0x1E:
					entry["UNK"] = file.read(4).hex().upper()
					entry["STRINGS"] = [readString(file), readString(file)]
				case 0x51:
					entry["STRINGS"] = [readString(file)]
					entry["UNK"] = file.read(2).hex().upper()
				case 0x9E | 0x82:
					entry["UNK"] = file.read(2).hex().upper()
					entry["STRINGS"] = [readString(file)]
				
				case _:
					print("UNKNOWN 0x28 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()

		case 0x29:
			entry["TYPE"] = "0x29"
			entry["UNK"] = file.read(17).hex().upper()
		
		case 0x2A:
			entry["TYPE"] = "0x2A"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x2B:
			entry["TYPE"] = "0x2B"
			entry["UNK"] = file.read(6).hex().upper()
		
		case 0x2C:
			entry["TYPE"] = "0x2C"
			entry["UNK"] = file.read(6).hex().upper()
		
		#Changed
		case 0x2D:
			entry["TYPE"] = "0x2D"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0 | 0x10 | 0x1C | 0x1D:
					pass
				case 2:
					entry["UNK"] = file.read(15).hex().upper()
				
				case 3 | 0x14:
					entry["UNK0"] = file.read(3).hex().upper()
					entry["STRINGS"] = [readString(file)]
					entry["UNK1"] = file.read(14).hex().upper()
				
				case 4:
					entry["UNK"] = file.read(16).hex().upper()
				
				case 5:
					entry["UNK"] = file.read(7).hex().upper()
				
				case 7:
					entry["UNK"] = file.read(2).hex().upper()
				
				case 8:
					entry["UNK"] = file.read(3).hex().upper()
				
				case 9:
					entry["UNK"] = file.read(12).hex().upper()
				
				case 0xB:
					entry["UNK"] = file.read(7).hex().upper()
				
				case 0xC | 0xD:
					entry["UNK"] = file.read(15).hex().upper()

				case 0xE:
					entry["UNK"] = file.read(11).hex().upper()
				
				case 0xF:
					entry["UNK"] = file.read(14).hex().upper()
				
				case 0x11:
					entry["UNK"] = file.read(16).hex().upper()
				
				case 0x12:
					entry["UNK"] = file.read(2).hex().upper()
				
				case 0x13:
					entry["UNK"] = file.read(18).hex().upper()
				
				case 0x15:
					entry["UNK"] = file.read(10).hex().upper()
				
				case 0x16:
					entry["UNK"] = file.read(7).hex().upper()
				
				case 0x17:
					entry["UNK"] = file.read(2).hex().upper()
				
				case 0x18 | 0x19:
					entry["UNK0"] = file.read(1).hex().upper()
					entry["STRINGS"] = [readString(file)]
					entry["UNK1"] = file.read(14).hex().upper()
				
				case 0x1A:
					entry["STRINGS"] = [readString(file)]
					entry["UNK"] = file.read(16).hex().upper()

				case 0x1B:
					entry["UNK"] = file.read(8).hex().upper()
				
				case 0x1E:
					entry["UNK"] = file.read(10).hex().upper()

				case _:
					print("UNKNOWN 0x2D CONTROL BYTE: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x2E:
			entry["TYPE"] = "0x2E"
			entry["UNK"] = file.read(18).hex().upper()
		
		case 0x2F:
			entry["TYPE"] = "0x2F"
			entry["UNK"] = file.read(4).hex().upper()
			entry["STRINGS"] = [readString(file)]
		
		#New
		case 0x30:
			entry["TYPE"] = "0x30"
			entry["UNK0"] = file.read(3).hex().upper()
			entry["STRINGS"] = [readString(file)]
			entry["UNK1"] = file.read(12).hex().upper()

		#Moved by 1
		case 0x31:
			entry["TYPE"] = "0x31"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			match(entry["CONTROL"]):
				case 0:
					entry["UNK"] = file.read(13).hex().upper()
				case 1:
					entry["UNK"] = file.read(3).hex().upper()
				case 2:
					entry["UNK"] = file.read(1).hex().upper()
				case 3:
					entry["UNK"] = file.read(7).hex().upper()
				case 4:
					entry["UNK"] = file.read(13).hex().upper()
				case 5:
					entry["UNK"] = file.read(4).hex().upper()
				case 6:
					entry["UNK"] = file.read(2).hex().upper()
				case 7:
					pass
				case _:
					print("UNKNOWN 0x31 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
			return entry

		#Changed
		case 0x32:
			entry["TYPE"] = "0x32"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			match(entry["CONTROL"]):
				case 0xFE | 0x96 | 0x39 | 5 | 0x37 | 0x34 | 2:
					entry["UNK"] = file.read(2).hex().upper()
				case 0xFF:
					entry["UNK"] = file.read(12).hex().upper()
				case 0 | 0x32:
					entry["UNK"] = file.read(36).hex().upper()
					entry["STRINGS"] = [readString(file)]
				
				case 1 | 0x33:
					entry["UNK"] = file.read(4).hex().upper()
				
				case 4 | 6 | 7 | 8 | 9 | 10 | 0xb | 0xc | 0xd | 0xe | 0xf | 0x10 | 0x11 | 0x12 | 0x13 | 0x14 | 0x15 | 0x16 | 0x17 | 0x18 | 0x19 | 0x1a | 0x1b | 0x1c | 0x1d | 0x1e | 0x1f | 0x20 | 0x21 | 0x22 | 0x23 | 0x24 | 0x25 | 0x26 | 0x27 | 0x28 | 0x29 | 0x2a | 0x2b | 0x2c | 0x2d | 0x2e | 0x2f | 0x30 | 0x31 | 0x36 | 0x38 | 0x3b | 0x3c | 0x3d | 0x3e | 0x3f | 0x40 | 0x41 | 0x42 | 0x43 | 0x44 | 0x45 | 0x46 | 0x47 | 0x48 | 0x49 | 0x4a | 0x4b | 0x4c | 0x4d | 0x4e | 0x4f | 0x50 | 0x51 | 0x52 | 0x53 | 0x54 | 0x55 | 0x56 | 0x57 | 0x58 | 0x59 | 0x5a | 0x5b | 0x5c | 0x5d | 0x5e | 0x5f | 0x60 | 0x61 | 0x62 | 99 | 0x66 | 0x67 | 0x68 | 0x69 | 0x6a | 0x6b | 0x6c | 0x6d | 0x6e | 0x6f | 0x70 | 0x71 | 0x72 | 0x73 | 0x74 | 0x75 | 0x76 | 0x77 | 0x78 | 0x79 | 0x7a | 0x7b | 0x7c | 0x7d | 0x7e | 0x7f | 0x80 | 0x81 | 0x82 | 0x83 | 0x84 | 0x85 | 0x86 | 0x87 | 0x88 | 0x89 | 0x8a | 0x8b | 0x8c | 0x8d | 0x8e | 0x8f | 0x90 | 0x91 | 0x92 | 0x93 | 0x94 | 0x95:
					pass
				
				case 3 | 0x35:
					entry["UNK"] = file.read(8).hex().upper()
				
				case 0x3A:
					entry["UNK"] = file.read(10).hex().upper()
				
				case 0x64:
					entry["UNK"] = file.read(6).hex().upper()
				
				case 0x65:
					entry["UNK"] = file.read(56).hex().upper()
				
				case _:
					print("UNKNOWN 0x32 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					print("Possible 2 bytes")
					sys.exit()
		
		#NChanged
		case 0x33:
			entry["TYPE"] = "SET_NAME_ID"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			entry["NAME_ID"] = int.from_bytes(file.read(2), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 1:
					entry["STRINGS"] = [readString(file), readString(file)]
				case 2:
					entry["UNK"] = file.read(4).hex().upper()
				case 3:
					entry["STRINGS"] = [readString(file), readString(file), readString(file), readString(file)]
				case 4:
					entry["STRINGS"] = [readString(file)]
				case 0xA | 0xB:
					pass
				case _:
					print("UNKNOWN 0x33 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 4))
					sys.exit()
		case 0x34:
			entry["TYPE"] = "0x34"
			entry["UNK"] = file.read(11).hex().upper()
		
		case 0x35:
			entry["TYPE"] = "0x35"
			entry["NAME_ID"] = int.from_bytes(file.read(2), byteorder="little")
			entry["UNK"] = file.read(7).hex().upper()
		
		case 0x36:
			entry["TYPE"] = "0x36"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		#Changed
		case 0x37:
			entry["TYPE"] = "0x37"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["CONTROL"] = int.from_bytes(file.read(2), byteorder="little", signed=True)
			entry["UNK1"] = file.read(12).hex().upper()
			if (-0x1ff < entry["CONTROL"] < -0x1fc):
				entry["UNK1"] += file.read(4).hex().upper()
			entry["UNK1"] += file.read(7).hex().upper()
			if (entry["CONTROL"] == -0x1fc):
				entry["STRINGS"] = [readString(file)]

		case 0x38:
			entry["TYPE"] = "0x38"
			entry["NAME_ID"] = int.from_bytes(file.read(2), byteorder="little", signed=True)
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little")]
		
		#Changed
		case 0x39:
			entry["TYPE"] = "0x39"
			entry["UNK"] = file.read(26).hex().upper()
		
		case 0x3A:
			entry["TYPE"] = "0x3A"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			entry["UNK"] = file.read(2).hex().upper()
			check = [0xC, 0x5, 0x69, 0xA, 0xB, 0xFF, 0xFE]
			if (entry["CONTROL"] not in check):
				entry["UNK"] += file.read(4).hex().upper()

		case 0x3B:
			entry["TYPE"] = "0x3B"
			entry["UNK"] = file.read(9).hex().upper()
		
		case 0x3C:
			entry["TYPE"] = "0x3C"
			entry["UNK"] = file.read(18).hex().upper()
		
		case 0x3D:
			entry["TYPE"] = "0x3D"
			entry["NAME_ID"] = int.from_bytes(file.read(2), byteorder="little", signed=True)
			entry["CONTROLS"] = [int.from_bytes(file.read(2), byteorder="little")]
			entry["CONTROLS"].append(int.from_bytes(file.read(2), byteorder="little"))
			flag1 = False
			flag2 = False

			if ((entry["NAME_ID"] >= 0x10) and(entry["NAME_ID"] != 0xFFFD)):
				flag1 = True
			if ((entry["CONTROLS"][0] >= 0x10) and(entry["CONTROLS"][0] != 0xFFFD)):
				flag2 = True

			if ((flag1 == False) or (flag2 == False) or (flag1 == flag2)):
				if (entry["CONTROLS"][0] == 0xFFFF):
					entry["UNK"] = file.read(12).hex().upper()
		
		case 0x3E:
			entry["TYPE"] = "0x3E"
			entry["UNK0"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
			entry["UNK1"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]

		case 0x3F:
			entry["TYPE"] = "0x3F"
			entry["UNK"] = file.read(7).hex().upper()

		#Changed
		case 0x40:
			entry["TYPE"] = "0x40"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 9 | 10 | 11 | 1 | 6 | 5 | 4 | 0x10 | 0x13 | 0:
					entry["UNK"] = file.read(2).hex().upper()
				case 8:
					entry["UNK"] = file.read(6).hex().upper()
				case 0xD:
					entry["UNK"] = file.read(0x30).hex().upper()
				case 0x15 | 0x11:
					entry["UNK"] = file.read(1).hex().upper()
				case 2 | 3 | 7 | 0x14 | 0xE | 0x12:
					pass
				case _:
					print("UNKNOWN 0x40 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x41:
			entry["TYPE"] = "0x41"
			entry["UNK"] = file.read(19).hex().upper()
		
		case 0x42:
			entry["TYPE"] = "0x42"
			entry["UNK"] = file.read(21).hex().upper()

		case 0x43:
			entry["TYPE"] = "0x43"
			entry["UNK"] = file.read(3).hex().upper()
		
		#Changed
		case 0x44:
			entry["TYPE"] = "0x44"
			entry["UNK"] = file.read(4).hex().upper()
		
		case 0x45:
			entry["TYPE"] = "0x45"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			entry["UNK"] = file.read(2).hex().upper()
			match(entry["CONTROL"]):
				case 0:
					entry["UNK"] += file.read(16).hex().upper()
				
				case 1:
					pass
				
				case 2:
					entry["UNK"] += file.read(7).hex().upper()
				
				case 3:
					entry["UNK"] += file.read(19).hex().upper()
				
				case 4 | 5:
					entry["UNK"] += file.read(2).hex().upper()
				
				case _:
					print("UNKNOWN 0x45 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x46:
			entry["TYPE"] = "0x46"
			entry["STRINGS"] = [readString(file), readString(file)]
		
		case 0x47:
			entry["TYPE"] = "0x47"
			entry["UNK"] = file.read(22).hex().upper()
		
		case 0x48:
			entry["TYPE"] = "0x48"
			entry["UNK"] = file.read(3).hex().upper()

		case 0x49:
			entry["TYPE"] = "0x49"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]

		#Changed
		case 0x4A:
			entry["TYPE"] = "0x4A"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			if (entry["CONTROL"] in [0x2E, 0x36, 0x43, 0x41, 0x12, 0x2D, 0x10, 0x11, 0x2F, 0x13, 0x1E, 0x31, 0x2A, 0x25, 0xF, 0x1D, 0x3F, 0x27, 0x1F, 0x1B, 0x1A]):
				return entry
			first_type = [10, 6, 5, 4, 3, 2, 1, 0]
			if (entry["CONTROL"] in first_type):
				entry["UNK"] = file.read(32).hex().upper()
				return entry
			match(entry["CONTROL"]):
				case 0xD:
					entry["STRINGS"] = [readString(file), readString(file)]
					entry["UNK"] = file.read(4).hex().upper()
				
				case 0xE:
					entry["UNK"] = file.read(1).hex().upper()
				
				case 0x14:
					entry["STRINGS"] = [readString(file), readString(file)]
					entry["UNK"] = file.read(10).hex().upper()
				
				case 0x15:
					entry["STRINGS"] = [readString(file)]
				
				case 0x17 | 0x38:
					entry["UNK"] = file.read(5).hex().upper()

				case 0x18 | 0x29:
					entry["UNK"] = file.read(3).hex().upper()
				
				case 0x19:
					entry["STRINGS"] = [readString(file), readString(file)]
				
				case 0x1C:
					entry["STRINGS"] = [readString(file)]
					entry["UNK"] = file.read(4).hex().upper()
				
				case 0x21 | 0x37:
					entry["UNK"] = file.read(6).hex().upper()
				
				case 0x23 | 0x24 | 0x28 | 0xB | 0x33 | 0x39 | 0x40 | 0x42 | 0x44:
					entry["UNK"] = file.read(2).hex().upper()
				
				case 0x26:
					entry["UNK"] = file.read(9).hex().upper()
					entry["STRINGS"] = [readString(file)]
				
				case 0x2B:
					entry["UNK0"] = file.read(1).hex().upper()
					entry["STRINGS"] = [readString(file)]
					entry["UNK1"] = file.read(2).hex().upper()
				
				case 0x30 | 0x34 | 0x2C | 0x3D:
					entry["UNK"] = file.read(4).hex().upper()
				
				case 0x35:
					entry["UNK"] = file.read(6).hex().upper()
					entry["STRINGS"] = [readString(file), readString(file), readString(file)]
				
				case 0x3A:
					entry["UNK"] = file.read(20).hex().upper()
				
				case 0x3B:
					entry["UNK"] = file.read(12).hex().upper()
				
				case 0x3C:
					entry["UNK"] = file.read(10).hex().upper()
				
				case 0x3E:
					entry["UNK0"] = file.read(1).hex().upper()
					entry["STRINGS"] = [readString(file)]
					entry["UNK1"] = file.read(4).hex().upper()

				case _:
					print("UNKNOWN 0x4A CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()

		case 0x4B:
			entry["TYPE"] = "0x4B"
			entry["UNK"] = file.read(38).hex().upper()
			entry["STRINGS"] = [readString(file)]
		
		case 0x4C:
			entry["TYPE"] = "0x4C"
			entry["UNK"] = file.read(23).hex().upper()
		
		case 0x4D:
			entry["TYPE"] = "0x4D"
			entry["UNK"] = file.read(2).hex().upper()
		
		case 0x4E:
			entry["TYPE"] = "0x4E"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
		#New
		case 0x4F:
			entry["TYPE"] = "0x4F"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
		case 0x50:
			entry["TYPE"] = "0x50"
			entry["UNK0"] = file.read(4).hex().upper()
			entry["STRINGS"] = [readString(file)]
			entry["UNK1"] = file.read(3).hex().upper()
		
		#New
		case 0x51:
			entry["TYPE"] = "GOTO51"
			entry["UNK"] = file.read(3).hex().upper()
			CalcGoto(file, entry, end)

		case 0x52:
			entry["TYPE"] = "0x52"
			entry["UNK"] = file.read(3).hex().upper()
			entry["STRINGS"] = [readString(file)]

		#Changed
		case 0x53:
			entry["TYPE"] = "0x53"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
			entry["UNK1"] = file.read(38).hex().upper()
		
		case 0x54:
			entry["TYPE"] = "0x54"
			entry["UNK"] = file.read(9).hex().upper()
		
		case 0x56:
			entry["TYPE"] = "0x56"
			entry["UNK"] = file.read(3).hex().upper()
			entry["STRINGS"] = [readString(file)]
		
		#Changed
		case 0x57:
			entry["TYPE"] = "0x57"
			entry["STRINGS"] = [readString(file)]
			entry["UNK"] = file.read(33).hex().upper()
		
		case 0x58:
			entry["TYPE"] = "0x58"
		
		case 0x59:
			entry["TYPE"] = "0x59"
			entry["UNK"] = file.read(3).hex().upper()
		
		case 0x5A:
			entry["TYPE"] = "0x5A"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x5B:
			entry["TYPE"] = "0x5B"
			entry["UNK0"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
			entry["UNK1"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		#Changed
		case 0x5C:
			entry["TYPE"] = "0x5C"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			entry["UNK"] = file.read(2).hex().upper()
			if (entry["CONTROL"] in [0, 1, 4, 6]):
				entry["UNK"] += file.read(2).hex().upper()
			elif (entry["CONTROL"] == 2):
				entry["UNK"] += file.read(4).hex().upper()
		
		case 0x5D:
			entry["TYPE"] = "0x5D"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			entry["UNK"] = file.read(2).hex().upper()
			if (entry["CONTROL"] in [0, 1]):
				entry["UNK"] += file.read(2).hex().upper()
		
		#Changed
		case 0x5E:
			entry["TYPE"] = "0x5E"
			temp = file.tell() - 1
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			entry["STRINGS"] = [readString(file)]
			match(entry["CONTROL"]):
				case 0 | 1 | 0xB:
					entry["UNK"] = file.read(2).hex().upper()
				case 2 | 3 | 4:
					entry["UNK"] = file.read(12).hex().upper()
				case 7:
					entry["UNK"] = file.read(19).hex().upper()
				case 8:
					entry["UNK"] = file.read(15).hex().upper()
				case 5 | 0xA | 6:
					pass
				case _:
					print("UNKNOWN 0x5E CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % temp)
					sys.exit()
		
		#Changed
		case 0x5F:
			entry["TYPE"] = "0x5F"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0:
					entry["UNK"] = file.read(9).hex().upper()
				case 0xE:
					entry["UNK"] = file.read(8).hex().upper()
				case 6:
					entry["UNK"] = file.read(10).hex().upper()
				case 0xA:
					entry["UNK"] = file.read(5).hex().upper()
				case 0xB | 9 | 7 | 8 | 4 | 1 | 0x13:
					entry["UNK"] = file.read(2).hex().upper()
				case 5 | 3 | 2:
					entry["UNK"] = file.read(6).hex().upper()
				case 0xD | 0xC | 0xF | 0x12 | 0x10 | 0x11:
					entry["UNK"] = file.read(4).hex().upper()
				case _:
					print("UNKNOWN 0x5F CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		#Changed
		case 0x60:
			entry["TYPE"] = "0x60"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0 | 3:
					entry["UNK1"] = file.read(7).hex().upper()
				
				case 1:
					pass

				case 2:
					entry["UNK1"] = file.read(12).hex().upper()
				
				case 4:
					entry["UNK1"] = file.read(23).hex().upper()
				
				case 5:
					entry["UNK1"] = file.read(28).hex().upper()
				
				case _:
					print("UNKNOWN 0x60 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x61:
			entry["TYPE"] = "0x61"
			entry["UNK"] = file.read(17).hex().upper()
		
		case 0x62:
			entry["TYPE"] = "0x62"
			entry["UNK"] = file.read(6).hex().upper()
		
		case 0x63:
			entry["TYPE"] = "0x63"
			entry["STRINGS"] = [readString(file)]
			entry["UNK"] = file.read(6).hex().upper()
		
		case 0x64:
			entry["TYPE"] = "0x64"
			entry["UNK"] = file.read(19).hex().upper()

		case 0x65:
			entry["TYPE"] = "0x65"
			entry["UNK"] = file.read(7).hex().upper()
		
		#Changed
		case 0x66:
			entry["TYPE"] = "0x66"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			match(entry["CONTROL"]):
				case 6 | 0:
					entry["UNK"] = file.read(5).hex().upper()
				case 2 | 9 | 4 | 0xC:
					entry["UNK"] = file.read(4).hex().upper()
				case 8 | 5 | 3:
					entry["UNK"] = file.read(6).hex().upper()
				case 7 | 1 | 0xB:
					entry["UNK"] = file.read(3).hex().upper()
				case 0xA:
					entry["UNK"] = file.read(10).hex().upper()
				case _:
					print("UNKNOWN 0x66 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()

		case 0x67:
			entry["TYPE"] = "0x67"
			entry["UNK"] = file.read(6).hex().upper()
		
		#Changed
		case 0x68:
			entry["TYPE"] = "0x68"
			entry["CONTROLS"] = [int.from_bytes(file.read(2), byteorder="little")]
			entry["CONTROLS"].append(int.from_bytes(file.read(1), byteorder="little"))
			entry["UNK"] = ""
			if (entry["CONTROLS"][1] in [2, 1]):
				entry["UNK"] += file.read(2).hex().upper()
			elif (entry["CONTROLS"][1] in [3, 4]):
				entry["UNK"] += file.read(1).hex().upper()
			
			if ((entry["CONTROLS"][0] <= 0x101) and (entry["CONTROLS"][1] == 6)):
				entry["UNK"] += file.read(2).hex().upper()
		
		#Changed
		case 0x69:
			entry["TYPE"] = "0x69"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 1:
					entry["UNK1"] = file.read(3).hex().upper()
				case 0:
					entry["UNK1"] = file.read(2).hex().upper()
				case _:
					print("UNKNOWN 0x69 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()

		#Changed
		case 0x6A:
			entry["TYPE"] = "0x6A"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0:
					entry["UNK1"] = file.read(4).hex().upper()
				
				case 2:
					entry["UNK1"] = file.read(10).hex().upper()
					entry["STRINGS"] = [readString(file)]
					entry["UNK2"] = file.read(4).hex().upper()
				
				case 3:
					entry["STRINGS1"] = [readString(file)]
					entry["UNK1"] = file.read(8).hex().upper()
					entry["STRINGS2"] = [readString(file)]
					entry["UNK2"] = file.read(4).hex().upper()
				
				case 5 | 0x14:
					entry["UNK1"] = file.read(4).hex().upper()
				
				case 0x15 | 1:
					pass
				
				case _:
					print("UNKNOWN 0x6A CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2 ))
					sys.exit()
		
		#Changed
		case 0x6B:
			entry["TYPE"] = "0x6B"
			entry["CONTROLS"] = [int.from_bytes(file.read(1), byteorder="little")]
			entry["CONTROLS"].append(int.from_bytes(file.read(1), byteorder="little"))
			if (entry["CONTROLS"][1] < 4):
				match(entry["CONTROLS"][0]):
					case 0:
						entry["UNK"] = file.read(6).hex().upper()
					case 1:
						entry["STRINGS"] = [readString(file)]
						entry["UNK"] = file.read(2).hex().upper()
					case 2:
						entry["UNK"] = file.read(6).hex().upper()
					case 3:
						pass
					case 4:
						entry["UNK"] = file.read(1).hex().upper()
					case 5:
						entry["UNK"] = file.read(4).hex().upper()
					case 6 | 7:
						entry["UNK"] = file.read(2).hex().upper()
					case _:
						print("UNKNOWN 0x6B CONTROL: 0x%x" % entry["CONTROLS"][0])
						print("OFFSET: 0x%x" % (file.tell() - 3))
						sys.exit()
		
		case 0x6C:
			entry["TYPE"] = "0x6C"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file), readString(file)]
			entry["UNK1"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
		case 0x6D:
			entry["TYPE"] = "0x6D"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x6E:
			entry["TYPE"] = "0x6E"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
		
		case 0x6F:
			entry["TYPE"] = "0x6F"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			entry["UNK"] = file.read(2).hex().upper()
			if (entry["CONTROL"] == 5):
				entry["UNK"] += file.read(6).hex().upper()
		
		case 0x70:
			entry["TYPE"] = "0x70"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			if (entry["CONTROL"] == 0):
				entry["STRINGS"] = [readString(file)]
			elif (entry["CONTROL"] in [1, 2]):
				entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
				entry["STRINGS"] = [readString(file)]
			else:
				print("UNKNOWN 0x70 CONTROL: 0x%x" % entry["CONTROL"])
				print("OFFSET: 0x%x" % (file.tell() - 2))
				sys.exit()

		case 0x71:
			entry["TYPE"] = "0x71"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			if (entry["CONTROL"] == 1):
				entry["STRINGS"] = [readString(file)]
				entry["UNK"] = file.read(3).hex().upper()
		
		#Changed
		case 0x72:
			entry["TYPE"] = "0x72"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			if (entry["CONTROL"] == 0):
				entry["UNK"] = file.read(15).hex().upper()
		
		#Changed
		case 0x73:
			entry["TYPE"] = "0x73"
			entry["UNK"] = file.read(8).hex().upper()
		
		case 0x74:
			entry["TYPE"] = "0x74"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			check = [0, 1]
			if (entry["CONTROL"] in check):
				return entry
			match(entry["CONTROL"]):
				case 3:
					entry["UNK"] = file.read(12).hex().upper()
				case 5:
					entry["UNK"] = file.read(4).hex().upper()
				case _:
					if (entry["CONTROL"] in [6, 2, 4]):
						entry["UNK"] = file.read(2).hex().upper()
					else:
						print("UNKNOWN 0x74 CONTROL: 0x%x" % entry["CONTROL"])
						print("OFFSET: 0x%x" % (file.tell() - 2))
						sys.exit()

		#Changed
		case 0x75:
			entry["TYPE"] = "0x75"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			if (entry["CONTROL"] == 0):
				entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
		#NEW
		case 0x76:
			entry["TYPE"] = "0x76"
			entry["UNK"] = file.read(4).hex().upper()
		
		case 0x78:
			entry["TYPE"] = "0x78"
			entry["UNK"] = file.read(30).hex().upper()
		
		case 0x79:
			entry["TYPE"] = "0x79"
			entry["UNK"] = file.read(8).hex().upper()

		case 0x7A:
			entry["TYPE"] = "0x7A"
			entry["UNK"] = file.read(17).hex().upper()
		
		case 0x7B:
			entry["TYPE"] = "0x7B"
			entry["UNK"] = file.read(2).hex().upper()
		
		#Changed
		case 0x7C:
			entry["TYPE"] = "0x7C"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			entry["UNK"] = file.read(24).hex().upper()
			entry["STRINGS"] = [readString(file)]
		
		case 0x7E:
			entry["TYPE"] = "0x7E"
			entry["UNK"] = file.read(4).hex().upper()
		
		case 0x7F:
			entry["TYPE"] = "0x7F"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x80:
			entry["TYPE"] = "0x80"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0 | 1:
					entry["UNK0"] = file.read(4).hex().upper()
					entry["STRINGS"] = [readString(file), readString(file)]
				case 2:
					entry["UNK0"] = file.read(2).hex().upper()
				case _:
					entry["UNK0"] = file.read(2).hex().upper()
					entry["STRINGS"] = [readString(file)]
					entry["UNK1"] = file.read(4).hex().upper()
		
		#New
		case 0x81:
			entry["TYPE"] = "0x81"
			entry["UNK"] = file.read(21).hex().upper()

		case 0x82:
			entry["TYPE"] = "0x82"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] in [0, 3, 4]):
				entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		#Changed
		case 0x83:
			entry["TYPE"] = "0x83"
			entry["UNK"] = file.read(18).hex().upper()
		
		case 0x84:
			entry["TYPE"] = "0x84"
			entry["UNK"] = file.read(14).hex().upper()
		
		case 0x85:
			entry["TYPE"] = "0x85"
		
		case 0x86:
			entry["TYPE"] = "0x86"
			entry["STRINGS"] = [readString(file)]
			entry["UNK"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]
		
		case 0x87:
			entry["TYPE"] = "0x87"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] in [0, 1]):
				entry["UNK"] = file.read(4).hex().upper()
		
		case 0x88:
			entry["TYPE"] = "0x88"
			entry["UNK"] = file.read(3).hex().upper()
		
		#Changed
		case 0x89:
			entry["TYPE"] = "0x89"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] == 0):
				entry["UNK"] = file.read(1).hex().upper()
			elif (entry["CONTROL"] in [6, 7, 8]):
				entry["UNK"] = file.read(4).hex().upper()
		
		case 0x8A:
			entry["TYPE"] = "0x8A"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] == 0):
				entry["UNK"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]
		#Changed
		case 0x8B:
			entry["TYPE"] = "0x8B"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] == 0):
				entry["STRINGS"] = [readString(file), readString(file)]
				entry["UNK"] = file.read(3).hex().upper()
		
		case 0x8C:
			entry["TYPE"] = "0x8C"
			entry["UNK"] = file.read(3).hex().upper()
		
		case 0x8D:
			entry["TYPE"] = "0x8D"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		#Changed
		case 0x8E:
			entry["TYPE"] = "0x8E"
			entry["CONTROL"] = int.from_bytes(file.read(2), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 2 | 1:
					entry["UNK"] = file.read(4).hex().upper()
				case 3:
					entry["UNK"] = file.read(3).hex().upper()
				case 4 | 5:
					pass
				case _:
					print("UNKNOWN 0x8E CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 3))
					sys.exit()
		
		case 0x8F:
			entry["TYPE"] = "0x8F"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]

		#New
		case 0x90:
			entry["TYPE"] = "0x90"
			entry["UNK"] = file.read(14).hex().upper()

		case 0x91:
			entry["TYPE"] = "0x91"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] == 0):
				entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		#Changed
		case 0x92:
			entry["TYPE"] = "0x92"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0:
					entry["UNK"] = file.read(11).hex().upper()
				case 2:
					entry["UNK"] = file.read(2).hex().upper()
				case 1:
					pass
				case _:
					print("UNKNOWN 0x92 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
			
		case 0x93:
			entry["TYPE"] = "0x93"
			entry["UNK"] = file.read(2).hex().upper()
		
		#Changed
		case 0x94:
			entry["TYPE"] = "0x94"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0xA:
					entry["UNK"] = file.read(2).hex().upper()
				case 0xE | 0xD | 0xC:
					entry["UNK"] = file.read(8).hex().upper()
				case 1 | 0 | 0xB:
					pass
				case _:
					print("UNKNOWN 0x94 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x95:
			entry["TYPE"] = "0x95"
			entry["UNK"] = file.read(16).hex().upper()
			
		case 0x96:
			entry["TYPE"] = "0x96"

		case 0x97:
			entry["TYPE"] = "0x97"
			entry["UNK"] = file.read(16).hex().upper()
		
		case 0x98:
			entry["TYPE"] = "0x98"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		#Changed
		case 0x99:
			entry["TYPE"] = "0x99"
		
		#Changed
		case 0x9A:
			entry["TYPE"] = "0x9A"
			entry["UNK"] = file.read(34).hex().upper()
		
		#Changed
		case 0x9B:
			entry["TYPE"] = "0x9B"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			if (entry["CONTROL"] in [1, 2]):
				entry["UNK"] = file.read(8).hex().upper()
			elif (entry["CONTROL"] in [3, 4]):
				entry["UNK"] = file.read(20).hex().upper()
			else:
				print("UNKNOWN 0x9A CONTROL: 0x%x" % entry["CONTROL"])
				print("OFFSET: 0x%x" % (file.tell() - 2))
				sys.exit()
		
		case 0x9C:
			entry["TYPE"] = "0x9C"
			entry["UNK"] = file.read(14).hex().upper()
		
		#New
		case 0x9E:
			entry["TYPE"] = "0x9E"
			entry["UNK"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]

		case 0x9F:
			entry["TYPE"] = "0x9F"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
		case 0xA0:
			entry["TYPE"] = "0xA0"
			entry["UNK"] = file.read(38).hex().upper()
			entry["STRINGS"] = [readString(file), readString(file)]
		
		#New
		case 0xA1:
			entry["TYPE"] = "0xA1"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			match(entry["CONTROL"]):
				case 0 | 4:
					entry["UNK"] = file.read(18).hex().upper()
				case 2 | 5:
					entry["UNK"] = file.read(31).hex().upper()
				case 3:
					entry["UNK"] = file.read(12).hex().upper()
				case 1:
					pass
				case _:
					print("UNKNOWN 0xA1 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		#Changed
		case 0xA2:
			entry["TYPE"] = "0xA2"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			match(entry["CONTROL"]):
				case 0:
					entry["UNK"] = file.read(1).hex().upper()
				case 1 | 2 | 3 | 4:
					entry["UNK"] = file.read(2).hex().upper()
				case _:
					print("UNKNOWN 0xA2 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0xA3:
			entry["TYPE"] = "0xA3"
			entry["UNK"] = file.read(2).hex().upper()

		#Changed
		case 0xA4:
			entry["TYPE"] = "0xA4"
			entry["STRINGS"] = [readString(file)]
			entry["UNK"] = file.read(2).hex().upper()
		
		#Changed
		case 0xA5:
			entry["TYPE"] = "0xA5"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
		case 0xA6:
			entry["TYPE"] = "0xA6"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 1 | 3 | 4 | 0xE:
					entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
				case 0xF | 2 | 9 | 7 | 6 | 0xA | 0xC | 0x11 | 0x10 | 0xD | 0xB:
					pass
				case _:
					print("UNKNOWN 0xA6 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		#Changed
		case 0xA7:
			entry["TYPE"] = "0xA7"
			entry["UNK"] = file.read(7).hex().upper()

		#New
		case 0xA8:
			entry["TYPE"] = "0xA8"
			entry["UNK"] = file.read(3).hex().upper()

		#New
		case 0xA9:
			entry["TYPE"] = "0xA9"
			entry["UNK"] = file.read(20).hex().upper()

		#New
		case 0xAA:
			entry["TYPE"] = "0xAA"

		#New
		case 0xAB:
			entry["TYPE"] = "0xAB"
			entry["UNK"] = file.read(15).hex().upper()
		
		#New
		case 0xAC:
			entry["TYPE"] = "0xAC"
			entry["UNK"] = file.read(3).hex().upper()
			
		case 0xAD:
			entry["TYPE"] = "0xAD"
			entry["UNK"] = file.read(3).hex().upper()

		case 0xAE:
			entry["TYPE"] = "0xAE"
			entry["UNK"] = file.read(9).hex().upper()
			
		case 0xAF:
			entry["TYPE"] = "0xAF"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			entry["UNK"] = file.read(4).hex().upper()
			match(entry["CONTROL"]):
				case 0:
					entry["UNK"] += file.read(2).hex().upper()
					entry["STRINGS"] = [readString(file), readString(file)]
					entry["UNK1"] = file.read(4).hex().upper()
				case 1:
					entry["UNK"] += file.read(28).hex().upper()
				case 2:
					entry["UNK"] += file.read(12).hex().upper()
				case 3 | 4:
					pass
				case _:
					print("UNKNOWN 0xAF CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 6))
					sys.exit()
		
		case 0xB0:
			entry["TYPE"] = "0xB0"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 2:
					entry["UNK"] = file.read(2).hex().upper()
				case 0xA | 0xB | 0 | 1:
					pass
				case _:
					print("UNKNOWN 0xB0 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0xB1:
			entry["TYPE"] = "0xB1"
			entry["UNK"] = file.read(2).hex().upper()
		
		case 0xB2:
			entry["TYPE"] = "0xB2"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			entry["UNK"] = file.read(1).hex().upper()
			match(entry["CONTROL"]):
				case 0 | 6:
					entry["UNK"] += file.read(25).hex().upper()
				case 1:
					entry["UNK"] += file.read(30).hex().upper()
				case 3 | 4:
					entry["UNK"] += file.read(4).hex().upper()
				case 5 | 2:
					pass
				case _:
					print("UNKNOWN 0xB2 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0xB3:
			entry["TYPE"] = "0xB3"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0:
					entry["STRINGS"] = [readString(file)]
				case 1:
					entry["UNK"] = file.read(2).hex().upper()
				case 3 | 0xA:
					entry["UNK"] = file.read(4).hex().upper()
				case 0xD | 0xC | 0xB:
					pass
				case _:
					print("UNKNOWN 0xB3 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0xB4:
			entry["TYPE"] = "0xB4"
			entry["UNK"] = file.read(11).hex().upper()
		
		case 0xB5:
			entry["TYPE"] = "0xB5"
			entry["UNK"] = file.read(13).hex().upper()
			
		case 0xB7:
			entry["TYPE"] = "0xB7"
			entry["UNK"] = file.read(4).hex().upper()
		
		case 0xB8:
			entry["TYPE"] = "0xB8"
			entry["UNK"] = file.read(6).hex().upper()
		
		case 0xB9:
			entry["TYPE"] = "0xB9"
			entry["UNK"] = file.read(2).hex().upper()
		
		case 0xBA:
			entry["TYPE"] = "0xBA"
			entry["UNK"] = file.read(6).hex().upper()
		
		case 0xBB:
			entry["TYPE"] = "0xBB"
			entry["UNK"] = file.read(2).hex().upper()

		case 0xBC:
			entry["TYPE"] = "0xBC"

		case 0xBD:
			entry["TYPE"] = "0xBD"
			entry["UNK"] = file.read(2).hex().upper()

		case 0xBE:
			entry["TYPE"] = "0xBE"
			entry["UNK"] = file.read(2).hex().upper()

		case 0xBF:
			entry["TYPE"] = "0xBF"

		case 0xC0:
			entry["TYPE"] = "0xC0"

		case _:
			print("UNKNOWN COMMAND: 0x%x" % cmd)
			print("Offset: 0x%x" % (file.tell() - 1))
			sys.exit()
		
	return entry

def GenerateMonsters(file, until_offset = None):
	#print("READING MONSTERS")
	#print("OFFSET: 0x%x" % file.tell())
	entry = {}
	entry["TYPE"] = "CREATE_MONSTERS"
	firstByte = file.read(1)
	file.seek(-1, 1)
	if (firstByte == b"\xFF"):
		entry["UNK0"] = file.read(0x1C).hex().upper()
		return entry
	entry["MAP"] = readString(file)
	file.seek(0x10 - (len(entry["MAP"]) + 1), 1)
	entry["UNK0"] = file.read(16).hex().upper()
	entry["TABLE"] = []
	map_monsters = 8
	while(True):
		entry2 = {}
		entry2["UNK0"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]
		entry2["STRINGS1"] = []
		for i in range(0, map_monsters):
			string = readString(file)
			entry2["STRINGS1"].append(string)
			file.seek(0x10 - (len(string) + 1), 1)
		entry2["UNK1"] = file.read(8).hex().upper()
		check = int.from_bytes(file.read(4), byteorder="little", signed=True)
		file.seek(-4, 1)
		if (check == 0):
			entry2["UNK1"] += file.read(8).hex().upper()
		elif (map_monsters != 4):
			entry2["STRINGS2"] = [readString(file)]
			file.seek(12 - (len(entry2["STRINGS2"][0]) + 1), 1)

		check = file.read(1)
		file.seek(-1, 1)
		entry["TABLE"].append(entry2)
		if (check == b"\xFF"): break
		if (check == b"\xFE"):
			file.seek(4, 1)
			map_monsters = 4
			continue
		if (file.tell() == (until_offset - 4)): break
		map_monsters = 8
	
	if (file.tell() == (until_offset - 4)):
		check = int.from_bytes(file.read(4), byteorder="little")
		if (check != 1):
			print("UNEXPECTED MONSTERS ENDING: 0x%x" % check)
			print("OFFSET: 0x%x" % (file.tell() - 4))
			sys.exit()
	else:
		entry["UNK1"] = file.read(0x1C).hex().upper()
	return entry


files = glob.glob("nx/npc*.dat")
os.makedirs("jsons", exist_ok=True)

for y in range(0, len(files)):
	print(files[y])
	file = open(files[y], "rb")

	DUMP = {}

	file_size = GetFileSize(file)
	header_size = int.from_bytes(file.read(4), byteorder="little")
	string_id_offset = int.from_bytes(file.read(4), byteorder="little")
	functions_pointer_table_offset = int.from_bytes(file.read(4), byteorder="little")
	size_of_functions_pointer_table = int.from_bytes(file.read(4), byteorder="little")
	function_names_pointer_table_offset = int.from_bytes(file.read(4), byteorder="little")
	function_names_count = int.from_bytes(file.read(4), byteorder="little")
	end_of_function_names_table = int.from_bytes(file.read(4), byteorder="little")

	DUMP["HEADER"] = {}
	DUMP["HEADER"]["TYPE"] = "%X" % int.from_bytes(file.read(4), byteorder="little")
	DUMP["HEADER"]["ID"] = readString(file)

	FUNCTIONS_POINTERS = []
	FUNCTIONS_NAMES = []

	pos = file.tell()

	assert(pos == functions_pointer_table_offset)

	while(file.tell() < pos + size_of_functions_pointer_table):
		FUNCTIONS_POINTERS.append(int.from_bytes(file.read(4), byteorder="little"))

	pos = file.tell()

	assert(pos == function_names_pointer_table_offset)

	for i in range(0, function_names_count):
		ptr = int.from_bytes(file.read(2), byteorder="little")
		cur_pos = file.tell()
		file.seek(ptr)
		FUNCTIONS_NAMES.append(readString(file))
		file.seek(cur_pos)

	DUMP["FUNCTIONS"] = {}

	for i in range(0, function_names_count):
		DUMP["FUNCTIONS"]["%s" % FUNCTIONS_NAMES[i] if (FUNCTIONS_NAMES[i] != "") else "%04d" % i] = []
		file.seek(FUNCTIONS_POINTERS[i])
		if (i < (function_names_count - 1)):
			end = FUNCTIONS_POINTERS[i + 1]
		else:
			end = file_size
		while(file.tell() < end):
			if (FUNCTIONS_NAMES[i] == "AnimeClipTable"):
				cmd = int.from_bytes(file.read(1), byteorder="little")
				CMD_ENTRY = AnimeClipTable(cmd, file, end)
				DUMP["FUNCTIONS"]["%s" % FUNCTIONS_NAMES[i]].append(CMD_ENTRY)

			elif (FUNCTIONS_NAMES[i] in ["FieldMonsterData", "FieldFollowData"]):
				data = file.read(end - file.tell()).hex().upper()
				DUMP["FUNCTIONS"]["%s" % FUNCTIONS_NAMES[i]].append(data)
			elif ((FUNCTIONS_NAMES[i] != "") and (FUNCTIONS_NAMES[i] != "ShinigPomBtlset")):
				cmd = int.from_bytes(file.read(1), byteorder="little")
				if FUNCTIONS_NAMES[i][0:1] == "_":
					CMD_ENTRY = GenerateTable(cmd, file, end)
				else: CMD_ENTRY = GenerateCommand(cmd, file, end)
				if ((CMD_ENTRY == None) and cmd != 0):
					print("CMD: 0x%x returned None!")
					sys.exit()
				elif CMD_ENTRY != None:
					DUMP["FUNCTIONS"]["%s" % FUNCTIONS_NAMES[i]].append(CMD_ENTRY)
			else:
				tell_pos = file.tell()
				try:
					string = readString(file)
				except:
					file.seek(tell_pos)
					cmd = int.from_bytes(file.read(1), byteorder="little")
					CMD_ENTRY = GenerateCommand(cmd, file, end)
					if ((CMD_ENTRY == None) and cmd != 0):
						print("CMD: 0x%x returned None!")
						sys.exit()
					elif CMD_ENTRY != None:
						DUMP["FUNCTIONS"]["%04d" % i].append(CMD_ENTRY)
				else:
					file.seek(tell_pos)
					if (FUNCTIONS_NAMES[i] == "ShinigPomBtlset"):
						DUMP["FUNCTIONS"]["ShinigPomBtlset"].append(GenerateMonsters(file, end))
					elif ((len(string) == 6) and (ord(string[0]) >= 0x20)):
						DUMP["FUNCTIONS"]["%04d" % i].append(GenerateMonsters(file, end))
					else:
						cmd = int.from_bytes(file.read(1), byteorder="little")
						if ((cmd == 0) and (DUMP["HEADER"]["ID"] == "infsys")):
							file.seek(-1, 1)
							entry = {}
							entry["LABEL"] = "0x%x" % (file.tell() - 1)
							entry["TYPE"] = "DUMP"
							entry["DUMP"] = file.read(end - file.tell()).hex().upper()
							CMD_ENTRY = entry
						else: CMD_ENTRY = GenerateCommand(cmd, file, end)
						if ((CMD_ENTRY == None) and cmd != 0):
							print("CMD: 0x%x returned None!")
							sys.exit()
						elif CMD_ENTRY != None:
							DUMP["FUNCTIONS"]["%04d" % i].append(CMD_ENTRY)

	file.close()

	file = open("jsons/%s.json" % files[y][3:-4], "w", encoding="UTF-8")
	json.dump(DUMP, file, indent="\t", ensure_ascii=False)
	file.close()