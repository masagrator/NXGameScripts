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
				entry["DIALOG"]["STRINGS"].append('CMD12_ARG: %d' % int.from_bytes(file.read(4), byteorder="little"))
				entry["DIALOG"]["STRINGS"].append(readStringDialog(file))
			
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
	passing = [2, 3, 4, 5, 6, 7, 8, 9, 0xA, 0xB, 0xC, 0xD, 0xE, 0x10, 0x11, 0x12, 0x13, 0x17, 0x22]
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
		

def GenerateCommand(cmd, file, end):
	entry = {}
	entry["LABEL"] = "0x%x" % (file.tell() - 1)
	#print("0x%x" % cmd)
	match(cmd):
		case 0:
			if ((end - file.tell()) < 4):
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
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
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
				case 0:
					entry["UNK"] = file.read(9).hex().upper()
				
				case 1:
					entry["UNK"] = file.read(5).hex().upper()
				
				case 2:
					entry["UNK"] = file.read(4).hex().upper()

				case 5:
					entry["UNK"] = file.read(9).hex().upper()
				
				case _:
					print("UNKNOWN 0x19 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x1A:
			entry["TYPE"] = "MESSAGE"
			entry["NAME_ID"] = int.from_bytes(file.read(2), byteorder="little", signed=True)
			ReadDialog(file, entry)

		case 0x1B:
			entry["TYPE"] = "0x1B"
			
		case 0x1C:
			entry["TYPE"] = "REMOVE_TEXT_BOX"
		
		case 0x1D:
			entry["TYPE"] = "OVERRIDE_DIALOG_SPEAKER"
			entry["NAME"] = [readString(file)]
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x1E:
			entry["TYPE"] = "JUMP_TO_ID"
			entry["STRINGS"] = [readString(file), readString(file)]

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
					entry["UNK"] = file.read(5).hex().upper()
				
				case 3:
					pass
				
				case 4:
					entry["UNK"] = file.read(1).hex().upper()
				
				case 5:
					entry["UNK"] = file.read(4).hex().upper()
				
				case 6:
					entry["UNK"] = file.read(2).hex().upper()
				
				case 7:
					entry["UNK"] = file.read(2).hex().upper()
				
				case 0xC:
					entry["UNK"] = file.read(2).hex().upper()
				
				case _:
					print("UNKNOWN 0x19 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 1))
					sys.exit()

		case 0x20:
			entry["TYPE"] = "0x20"
			entry["SIZE_CHECK"] = int.from_bytes(file.read(1), byteorder="little")
			assert(entry["SIZE_CHECK"] <= 2)
			entry["UNK0"] = file.read(2).hex().upper()
			if (entry["SIZE_CHECK"] > 0):
				entry["UNK0"] += file.read(entry["SIZE_CHECK"]).hex().upper()
			entry["STRINGS"] = [readString(file), readString(file)]
			entry["UNK1"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
		case 0x21:
			entry["TYPE"] = "0x21"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			entry["UNK"] = file.read(6).hex().upper()
			if (entry["CONTROL"] == 1):
				entry["UNK"] += file.read(8).hex().upper()
		
		case 0x22:
			entry["TYPE"] = "0x22"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
			entry["UNK1"] = file.read(21).hex().upper()
		
		case 0x23:
			entry["TYPE"] = "0x23"
			entry["UNK"] = file.read(6).hex().upper()

		case 0x24:
			entry["TYPE"] = "0x24"
			entry["UNK"] = file.read(3).hex().upper()
			entry["STRINGS"] = [readString(file), readString(file)]

		case 0x25:
			entry["TYPE"] = "0x25"
			entry["UNK0"] = file.read(3).hex().upper()
			entry["STRINGS"] = [readString(file), readString(file)]
			entry["UNK1"] = file.read(36).hex().upper()

		case 0x26:
			entry["TYPE"] = "0x26"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
		
		case 0x27:
			entry["TYPE"] = "0x27"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0xA:
					entry["UNK"] = file.read(3).hex().upper()
					entry["STRINGS"] = [readString(file)]
				case 0xC:
					entry["UNK0"] = file.read(8).hex().upper()
					entry["STRINGS"] = [readString(file)]
					entry["UNK1"] = file.read(37).hex().upper()
				case 0x12:
					entry["UNK"] = file.read(5).hex().upper()
				case 0x15:
					entry["UNK"] = file.read(1).hex().upper()
					entry["STRINGS"] = [readString(file)]
				case _:
					if (entry["CONTROL"] in [0x11, 0x10, 0xF, 0xB, 0xD, 0xE]):
						entry["UNK"] = file.read(3).hex().upper()
					elif (entry["CONTROL"] in [0x13, 0x14]):
						entry["UNK"] = file.read(19).hex().upper()
					else:
						print("UNKNOWN 0x27 CONTROL: 0x%x" % entry["CONTROL"])
						print("OFFSET: 0x%x" % (file.tell() - 2))
						sys.exit()
		
		case 0x28:
			entry["TYPE"] = "0x28"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)

			match(entry["CONTROL"]):
				case 0:
					entry["UNK"] = file.read(5).hex().upper()
				case 1:
					entry["UNK"] = file.read(10).hex().upper()
				case 0xE:
					entry["UNK"] = file.read(8).hex().upper()
				case 0x12:
					entry["UNK"] = ""
					for x in range(0, 9):
						entry["UNK"] += file.read(2).hex().upper()
				case 0x13:
					entry["UNK"] = file.read(18).hex().upper()
				case 0x15:
					entry["UNK"] = file.read(22).hex().upper()
				case 0x32:
					entry["UNK"] = file.read(22).hex().upper()
				case 0x35:
					entry["UNK"] = file.read(18).hex().upper()
				case 0x36:
					entry["UNK"] = file.read(10).hex().upper()
				case 0x37:
					entry["UNK"] = file.read(25).hex().upper()
				case ord("<"):
					entry["UNK"] = file.read(12).hex().upper()
				case ord("F"):
					entry["UNK"] = file.read(12).hex().upper()
				case ord("P"):
					entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
					entry["STRING1"] = [readString(file)]
					entry["UNK1"] = file.read(20).hex().upper()
					entry["STRING2"] = [readString(file)]
				case ord("["):
					entry["UNK"] = file.read(5).hex().upper()
				case ord("\\"):
					entry["UNK"] = file.read(1).hex().upper()
				case ord("a"):
					entry["UNK"] = file.read(7).hex().upper()
				case ord("d"):
					entry["STRINGS"] = [readString(file)]
				case ord("n"):
					entry["UNK"] = file.read(16).hex().upper()
				case ord("r"):
					entry["UNK"] = file.read(11).hex().upper()
				case ord("{"):
					entry["UNK"] = file.read(4).hex().upper()
				case ord("i"):
					entry["UNK"] = file.read(2).hex().upper()
					entry["STRINGS"] = [readString(file), readString(file)]
				case ord("j"):
					entry["UNK"] = file.read(2).hex().upper()
				case _:
					if (entry["CONTROL"] in [ord("\b"), 6, 4, 2]):
						entry["UNK"] = file.read(1).hex().upper()
					elif (entry["CONTROL"] in [ord("\a"), 5]):
						entry["UNK"] = file.read(1).hex().upper()
						entry["STRINGS"] = [readString(file)]
					elif (entry["CONTROL"] in [ord("m"), ord("l"), ord("k"), ord("f"), ord("e"), ord("c"), 0x1C, 0x1A, 0x17, 0x19, 0x14, ord("\r"), 0x10, ord("H"), ord("]"), ord("\t"), ord("^"), ord("_"), ord("`"), ord("s"), ord("t"), ord("u"), ord("y")]):
						entry["UNK"] = file.read(2).hex().upper()
					elif (entry["CONTROL"] in [ord("\n"), 0xF]):
						entry["UNK"] = file.read(4).hex().upper()
					elif (entry["CONTROL"] in [ord("\f"), 4, ord("Z"), ord("\v")]):
						entry["UNK"] = file.read(6).hex().upper()
					elif (entry["CONTROL"] in [ord("b"), 0x11, ord("z")]):
						entry["UNK"] = file.read(3).hex().upper()
					elif (entry["CONTROL"] in [ord("~"), ord("q")]):
						entry["UNK"] = file.read(7).hex().upper()
					else:
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
		
		case 0x2D:
			entry["TYPE"] = "0x2D"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] in [0, 0x10]):
				return entry
			match(entry["CONTROL"]):
				case 2:
					entry["UNK0"] = file.read(15).hex().upper()
				
				case 3:
					entry["UNK0"] = file.read(3).hex().upper()
					entry["STRINGS"] = [readString(file)]
					entry["UNK1"] = file.read(14).hex().upper()

				case 0x14:
					entry["UNK0"] = file.read(3).hex().upper()
					entry["STRINGS"] = [readString(file)]
					entry["UNK1"] = file.read(14).hex().upper()
				
				case 4:
					entry["UNK0"] = file.read(16).hex().upper()
				
				case 5:
					entry["UNK0"] = file.read(7).hex().upper()
				
				case 7:
					entry["UNK0"] = file.read(2).hex().upper()
				
				case 8:
					entry["UNK0"] = file.read(3).hex().upper()
				
				case 9:
					entry["UNK0"] = file.read(12).hex().upper()
				
				case 0xB:
					entry["UNK0"] = file.read(7).hex().upper()
				
				case 0xC:
					entry["UNK0"] = file.read(15).hex().upper()
				
				case 0xD:
					entry["UNK0"] = file.read(15).hex().upper()

				case 0xE:
					entry["UNK0"] = file.read(11).hex().upper()
				
				case 0xF:
					entry["UNK0"] = file.read(14).hex().upper()
				
				case 0x11:
					entry["UNK0"] = file.read(16).hex().upper()
				
				case 0x12:
					entry["UNK0"] = file.read(2).hex().upper()
				
				case 0x13:
					entry["UNK0"] = file.read(18).hex().upper()
				
				case 0x15:
					entry["UNK0"] = file.read(10).hex().upper()
				
				case 0x16:
					entry["UNK0"] = file.read(7).hex().upper()
				
				case 0x17:
					entry["UNK0"] = file.read(2).hex().upper()
				
				case 0x1B:
					entry["UNK0"] = file.read(8).hex().upper()

				case _:
					print("UNKNOWN 0x2D CONTROL BYTE: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x2E:
			entry["TYPE"] = "0x2E"
			entry["UNK"] = file.read(18).hex().upper()
		
		case 0x2F:
			entry["TYPE"] = "0x2F"
			entry["UNK"] = file.read(3).hex().upper()
			entry["STRINGS"] = [readString(file)]
		
		case 0x30:
			entry["TYPE"] = "0x30"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			check = [7]
			if (entry["CONTROL"] in check):
				return entry
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
				
				case _:
					print("UNKNOWN 0x30 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()

		
		case 0x31:
			entry["TYPE"] = "0x31"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			match(entry["CONTROL"]):
				case 0xFE:
					entry["UNK"] = file.read(2).hex().upper()
					return entry
				case 0xFF:
					entry["UNK"] = file.read(12).hex().upper()
					return entry
			if (entry["CONTROL"] == 0):
				entry["UNK"] = file.read(36).hex().upper()
				entry["STRINGS"] = [readString(file)]
			elif (entry["CONTROL"] == 0x32):
				entry["VOICE_FILE_ID"] = int.from_bytes(file.read(2), byteorder="little")
				entry["UNK"] = file.read(34).hex().upper()
				entry["STRINGS"] = [readString(file)]
			elif (entry["CONTROL"] == 0x34):
				entry["VOICE_FILE_ID"] = int.from_bytes(file.read(2), byteorder="little")
			elif (entry["CONTROL"]  in [1, 0x33]):
				entry["UNK"] = file.read(4).hex().upper()
			
			elif (entry["CONTROL"] in [0x96, 0x39, 6, 0x38, 5, 0x37, 2]):
				entry["UNK"] = file.read(2).hex().upper()
			
			elif(entry["CONTROL"] in [0x35, 3]):
				entry["UNK"] = file.read(8).hex().upper()
			
			elif(entry["CONTROL"] == 0x3A):
				entry["UNK"] = file.read(10).hex().upper()
			
			elif(entry["CONTROL"] == 100):
				entry["UNK"] = file.read(6).hex().upper()
			
			elif(entry["CONTROL"] == 0x65):
				entry["UNK"] = file.read(56).hex().upper()
			
			elif(entry["CONTROL"] == 0xFD):
				entry["UNK"] = file.read(1).hex().upper()
			
			else:
				print("UNKNOWN 0x31 CONTROL: 0x%x" % entry["CONTROL"])
				print("OFFSET: 0x%x" % (file.tell() - 2))
				sys.exit()


		case 0x32:
			entry["TYPE"] = "SET_NAME_ID"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			entry["NAME_ID"] = int.from_bytes(file.read(2), byteorder="little")
			match(entry["CONTROL"]):
				case 1:
					entry["STRINGS"] = [readString(file), readString(file)]
				
				case 2:
					entry["UNK"] = file.read(4).hex().upper()
				
				case 3:
					entry["STRINGS"] = [readString(file), readString(file), readString(file), readString(file)]
				
				case 4:
					entry["STRINGS"] = [readString(file)]
				
				case 0xA:
					pass
				
				case 0xB:
					pass
				
				case _:
					print("UNKNOWN 0x32 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x33:
			entry["TYPE"] = "0x33"
			entry["UNK"] = file.read(11).hex().upper()
		
		case 0x34:
			entry["TYPE"] = "0x34"
			entry["NAME_ID"] = int.from_bytes(file.read(2), byteorder="little")
			entry["UNK"] = file.read(7).hex().upper()
		
		case 0x35:
			entry["TYPE"] = "0x35"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			
		case 0x36:
			entry["TYPE"] = "0x36"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["CONTROL"] = int.from_bytes(file.read(2), byteorder="little", signed=True)
			entry["UNK1"] = file.read(12).hex().upper()
			if (-0x1ff < entry["CONTROL"] < -0x1fc):
				entry["UNK1"] += file.read(4).hex().upper()
			entry["UNK1"] += file.read(7).hex().upper()

		case 0x37:
			entry["TYPE"] = "0x37"
			entry["NAME_ID"] = int.from_bytes(file.read(2), byteorder="little", signed=True)
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little")]
		
		case 0x38:
			entry["TYPE"] = "0x38"
			entry["UNK"] = file.read(22).hex().upper()
		
		case 0x39:
			entry["TYPE"] = "0x39"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			entry["UNK"] = file.read(2).hex().upper()
			check = [0xC, 0x5, 0x69, 0xA, 0xB, 0xFF, 0xFE]
			if (entry["CONTROL"] not in check):
				entry["UNK"] += file.read(4).hex().upper()
		
		case 0x3A:
			entry["TYPE"] = "0x3A"
			entry["UNK"] = file.read(9).hex().upper()
		
		case 0x3B:
			entry["TYPE"] = "0x3B"
			entry["UNK"] = file.read(18).hex().upper()
		
		case 0x3C:
			entry["TYPE"] = "0x3C"
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
		
		case 0x3D:
			entry["TYPE"] = "0x3D"
			entry["UNK0"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
			entry["UNK1"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]

		case 0x3E:
			entry["TYPE"] = "0x3E"
			entry["UNK"] = file.read(7).hex().upper()

		case 0x3F:
			entry["TYPE"] = "0x3F"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			type1 = [9, 10, 11, 1, 6, 5, 4, 0, 8]
			if (entry["CONTROL"] in type1):
				entry["UNK"] = file.read(2).hex().upper()
			if (entry["CONTROL"] == 8):
				entry["UNK"] += file.read(4).hex().upper()
		
		case 0x40:
			entry["TYPE"] = "0x40"
			entry["UNK"] = file.read(19).hex().upper()
		
		case 0x41:
			entry["TYPE"] = "0x41"
			entry["UNK"] = file.read(21).hex().upper()

		case 0x42:
			entry["TYPE"] = "0x42"
			entry["UNK"] = file.read(3).hex().upper()
		
		case 0x43:
			entry["TYPE"] = "0x43"
			entry["UNK"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]
		
		case 0x44:
			entry["TYPE"] = "0x44"
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
				
				case 4:
					entry["UNK"] += file.read(2).hex().upper()
				
				case 5:
					entry["UNK"] += file.read(2).hex().upper()
				
				case _:
					print("UNKNOWN 0x44 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x45:
			entry["TYPE"] = "0x45"
			entry["STRINGS"] = [readString(file), readString(file)]
		
		case 0x46:
			entry["TYPE"] = "0x46"
			entry["UNK"] = file.read(22).hex().upper()
		
		case 0x47:
			entry["TYPE"] = "0x47"
			entry["UNK"] = file.read(3).hex().upper()

		case 0x48:
			entry["TYPE"] = "0x48"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]

		case 0x49:
			entry["TYPE"] = "0x49"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			if (entry["CONTROL"] in [0xB, 0xE, 0xF, 0x10, 0x11, 0x12, 0x16, 0x1D, 0x1E, 0x20, 0x25]):
				return entry
			first_type = [10, 4, 3, 2, 1, 0]
			if (entry["CONTROL"] in first_type):
				entry["UNK"] = file.read(32).hex().upper()
				return entry
			match(entry["CONTROL"]):
				case 0xD:
					entry["STRINGS"] = [readString(file), readString(file)]
					entry["UNK"] = file.read(4).hex().upper()
				
				case 0x14:
					entry["STRINGS"] = [readString(file), readString(file)]
					entry["UNK"] = file.read(10).hex().upper()
				
				case 0x15:
					entry["STRINGS"] = [readString(file)]
				
				case 0x17:
					entry["UNK"] = file.read(5).hex().upper()

				case 0x18:
					entry["UNK"] = file.read(3).hex().upper()
				
				case 0x19:
					entry["STRINGS"] = [readString(file), readString(file)]
				
				case 0x1C:
					entry["STRINGS"] = [readString(file)]
					entry["UNK"] = file.read(4).hex().upper()
				
				case 0x21:
					entry["UNK"] = file.read(4).hex().upper()
				
				case 0x23:
					entry["UNK"] = file.read(2).hex().upper()
				case 0x24:
					entry["UNK"] = file.read(2).hex().upper()
				
				case 0x26:
					entry["UNK"] = file.read(9).hex().upper()
					entry["STRINGS"] = [readString(file)]

				case 0x28:
					entry["UNK"] = file.read(2).hex().upper()
				
				case 0x29:
					entry["UNK"] = file.read(3).hex().upper()
				
				case _:
					print("UNKNOWN 0x49 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()

		case 0x4A:
			entry["TYPE"] = "0x4A"
			entry["UNK"] = file.read(38).hex().upper()
			entry["STRINGS"] = [readString(file)]
		
		case 0x4B:
			entry["TYPE"] = "0x4B"
			entry["UNK"] = file.read(23).hex().upper()
		
		case 0x4C:
			entry["TYPE"] = "0x4C"
			entry["UNK"] = file.read(2).hex().upper()
		
		case 0x4D:
			entry["TYPE"] = "0x4D"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
		case 0x4F:
			entry["TYPE"] = "0x4F"
			entry["UNK0"] = file.read(4).hex().upper()
			entry["STRINGS"] = [readString(file)]
			entry["UNK1"] = file.read(3).hex().upper()
		
		case 0x51:
			entry["TYPE"] = "0x51"
			entry["UNK"] = file.read(3).hex().upper()
			entry["STRINGS"] = [readString(file)]
		
		case 0x52:
			entry["TYPE"] = "0x52"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
			entry["UNK1"] = file.read(36).hex().upper()
		
		case 0x53:
			entry["TYPE"] = "0x53"
			entry["UNK"] = file.read(9).hex().upper()
		
		case 0x55:
			entry["TYPE"] = "0x55"
			entry["UNK"] = file.read(3).hex().upper()
			entry["STRINGS"] = [readString(file)]
		
		case 0x56:
			entry["TYPE"] = "0x56"
			entry["STRINGS"] = [readString(file)]
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x57:
			entry["TYPE"] = "0x57"
		
		case 0x58:
			entry["TYPE"] = "0x58"
			entry["UNK"] = file.read(3).hex().upper()
		
		case 0x59:
			entry["TYPE"] = "0x59"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x5A:
			entry["TYPE"] = "0x5A"
			entry["UNK0"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
			entry["UNK1"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x5B:
			entry["TYPE"] = "0x5B"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			entry["UNK"] = file.read(2).hex().upper()
			if (entry["CONTROL"] in [0, 1, 4]):
				entry["UNK"] += file.read(2).hex().upper()
		
		case 0x5C:
			entry["TYPE"] = "0x5C"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			entry["UNK"] = file.read(2).hex().upper()
			if (entry["CONTROL"] in [0, 1]):
				entry["UNK"] += file.read(2).hex().upper()
		
		case 0x5D:
			entry["TYPE"] = "0x5D"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			entry["STRINGS"] = [readString(file)]
			if (entry["CONTROL"] in [5, 6, 9]):
				return entry
			match(entry["CONTROL"]):
				case 0:
					entry["UNK"] = file.read(2).hex().upper()
				case 1:
					entry["UNK"] = file.read(2).hex().upper()
				case 2:
					entry["UNK"] = file.read(12).hex().upper()
				case 3:
					entry["UNK"] = file.read(12).hex().upper()
				case 4:
					entry["UNK"] = file.read(12).hex().upper()

				case 7:
					entry["UNK"] = file.read(19).hex().upper()
				case 8:
					entry["UNK"] = file.read(15).hex().upper()
				case _:
					print("UNKNOWN 0x5D CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x5E:
			entry["TYPE"] = "0x5E"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0:
					entry["UNK"] = file.read(8).hex().upper()
				case 6:
					entry["UNK"] = file.read(10).hex().upper()
				case 0xA:
					entry["UNK"] = file.read(5).hex().upper()
				case _:
					if (entry["CONTROL"] in [0xB, 9, 7, 8, 4, 1]):
						entry["UNK"] = file.read(2).hex().upper()
					elif (entry["CONTROL"] in [5, 3, 2]):
						entry["UNK"] = file.read(6).hex().upper()
					elif (entry["CONTROL"] in [0xD, 0xC]):
						entry["UNK"] = file.read(4).hex().upper()
					else:
						print("UNKNOWN 0x5E CONTROL: 0x%x" % entry["CONTROL"])
						print("OFFSET: 0x%x" % (file.tell() - 2))
						sys.exit()
		
		case 0x5F:
			entry["TYPE"] = "0x5F"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0:
					entry["UNK1"] = file.read(7).hex().upper()
				
				case 1:
					pass

				case 2:
					entry["UNK1"] = file.read(12).hex().upper()
				
				case 3:
					entry["UNK1"] = file.read(7).hex().upper()
				
				case _:
					print("UNKNOWN 0x5F CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x60:
			entry["TYPE"] = "0x60"
			entry["UNK"] = file.read(17).hex().upper()
		
		case 0x61:
			entry["TYPE"] = "0x61"
			entry["UNK"] = file.read(6).hex().upper()
		
		case 0x62:
			entry["TYPE"] = "0x62"
			entry["STRINGS"] = [readString(file)]
			entry["UNK"] = file.read(6).hex().upper()
		
		case 0x63:
			entry["TYPE"] = "0x63"
			entry["UNK"] = file.read(19).hex().upper()

		case 0x64:
			entry["TYPE"] = "0x64"
			entry["UNK"] = file.read(7).hex().upper()
		
		case 0x65:
			entry["TYPE"] = "0x65"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			match(entry["CONTROL"]):
				case 6:
					entry["UNK"] = file.read(4).hex().upper()
				case 2:
					entry["UNK"] = file.read(4).hex().upper()
				case 8:
					entry["UNK"] = file.read(6).hex().upper()
				case _:
					if (entry["CONTROL"] in [5, 3, 0]):
						entry["UNK"] = file.read(5).hex().upper()
					elif (entry["CONTROL"] in [9, 7, 4, 1]):
						entry["UNK"] = file.read(3).hex().upper()
					else:
						print("UNKNOWN 0x65 CONTROL: 0x%x" % entry["CONTROL"])
						print("OFFSET: 0x%x" % (file.tell() - 2))
						sys.exit()
		case 0x66:
			entry["TYPE"] = "0x66"
			entry["UNK"] = file.read(6).hex().upper()
		
		case 0x67:
			entry["TYPE"] = "0x67"
			entry["CONTROLS"] = [int.from_bytes(file.read(2), byteorder="little")]
			entry["CONTROLS"].append(int.from_bytes(file.read(1), byteorder="little"))
			entry["UNK"] = ""
			if (entry["CONTROLS"][1] in [2, 1]):
				entry["UNK"] += file.read(2).hex().upper()
			elif (entry["CONTROLS"][1] in [3, 4]):
				entry["UNK"] += file.read(1).hex().upper()
			
			if ((entry["CONTROLS"][0] <= 0x96) and (entry["CONTROLS"][1] == 6)):
				entry["UNK"] += file.read(2).hex().upper()
		
		case 0x68:
			entry["TYPE"] = "0x68"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 1:
					entry["UNK1"] = file.read(2).hex().upper()
				case 0:
					entry["UNK1"] = file.read(1).hex().upper()
				case _:
					print("UNKNOWN 0x68 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()

		case 0x69:
			entry["TYPE"] = "0x69"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0:
					entry["UNK1"] = file.read(4).hex().upper()
				
				case 2:
					entry["UNK1"] = file.read(10).hex().upper()
					entry["STRINGS"] = [readString(file)]
				
				case 3:
					entry["STRINGS1"] = [readString(file)]
					entry["UNK1"] = file.read(8).hex().upper()
					entry["STRINGS2"] = [readString(file)]
				
				case 5:
					entry["UNK1"] = file.read(4).hex().upper()
				
				case _:
					print("UNKNOWN 0x69 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2 ))
					sys.exit()

		case 0x6A:
			entry["TYPE"] = "0x6A"
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
						entry["UNK"] = file.read(5).hex().upper()
					case 3:
						pass
					case 4:
						entry["UNK"] = file.read(1).hex().upper()
					case 5:
						entry["UNK"] = file.read(4).hex().upper()
					case 6:
						entry["UNK"] = file.read(2).hex().upper()
					case 7:
						entry["UNK"] = file.read(2).hex().upper()
					case _:
						print("UNKNOWN 0x6A CONTROL: 0x%x" % entry["CONTROLS"][0])
						print("OFFSET: 0x%x" % (file.tell() - 3))
						sys.exit()
		
		case 0x6B:
			entry["TYPE"] = "0x6B"
			entry["UNK0"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file), readString(file)]
			entry["UNK1"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
		case 0x6C:
			entry["TYPE"] = "0x6C"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x6D:
			entry["TYPE"] = "0x6D"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
		
		case 0x6E:
			entry["TYPE"] = "0x6E"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			entry["UNK"] = file.read(2).hex().upper()
			if (entry["CONTROL"] == 5):
				entry["UNK"] += file.read(6).hex().upper()
		
		case 0x6F:
			entry["TYPE"] = "0x6F"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			if (entry["CONTROL"] == 0):
				entry["STRINGS"] = [readString(file)]
			elif (entry["CONTROL"] in [1, 2]):
				entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
				entry["STRINGS"] = [readString(file)]
			else:
				print("UNKNOWN 0x6F CONTROL: 0x%x" % entry["CONTROL"])
				print("OFFSET: 0x%x" % (file.tell() - 2))
				sys.exit()

		case 0x70:
			entry["TYPE"] = "0x70"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			if (entry["CONTROL"] == 1):
				entry["STRINGS"] = [readString(file)]
				entry["UNK"] = file.read(3).hex().upper()
		
		case 0x71:
			entry["TYPE"] = "0x71"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			if (entry["CONTROL"] == 0):
				entry["UNK"] = file.read(10).hex().upper()
		
		case 0x72:
			entry["TYPE"] = "0x72"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x73:
			entry["TYPE"] = "0x73"
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
						print("UNKNOWN 0x73 CONTROL: 0x%x" % entry["CONTROL"])
						print("OFFSET: 0x%x" % (file.tell() - 2))
						sys.exit()

		case 0x74:
			entry["TYPE"] = "0x74"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
		case 0x77:
			entry["TYPE"] = "0x77"
			entry["UNK"] = file.read(30).hex().upper()
		
		case 0x78:
			entry["TYPE"] = "0x78"
			entry["UNK"] = file.read(8).hex().upper()

		case 0x79:
			entry["TYPE"] = "0x79"
			entry["UNK"] = file.read(17).hex().upper()
		
		case 0x7A:
			entry["TYPE"] = "0x7A"
			entry["UNK"] = file.read(2).hex().upper()
		
		case 0x7B:
			entry["TYPE"] = "0x7B"
			entry["UNK"] = file.read(23).hex().upper()
			entry["STRINGS"] = [readString(file)]
		
		case 0x7D:
			entry["TYPE"] = "0x7D"
			entry["UNK"] = file.read(4).hex().upper()
		
		case 0x7E:
			entry["TYPE"] = "0x7E"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x7F:
			entry["TYPE"] = "0x7F"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] in [-1, -2]):
				entry["UNK0"] = file.read(2).hex().upper()
				entry["STRINGS"] = [readString(file)]
				entry["UNK1"] = file.read(4).hex().upper()
			elif (entry["CONTROL"] in [0, 1]):
				entry["UNK0"] = file.read(4).hex().upper()
				entry["STRINGS"] = [readString(file), readString(file)]
			else:
				entry["UNK0"] = file.read(2).hex().upper()
				entry["STRINGS"] = [readString(file)]
				entry["UNK1"] = file.read(4).hex().upper()
		
		case 0x81:
			entry["TYPE"] = "0x81"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] in [0, 3, 4]):
				entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x82:
			entry["TYPE"] = "0x82"
			entry["UNK"] = file.read(6).hex().upper()
		
		case 0x83:
			entry["TYPE"] = "0x83"
			entry["UNK"] = file.read(14).hex().upper()
		
		case 0x84:
			entry["TYPE"] = "0x84"
		
		case 0x85:
			entry["TYPE"] = "0x85"
			entry["STRINGS"] = [readString(file)]
			entry["UNK"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]
		
		case 0x86:
			entry["TYPE"] = "0x86"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] in [0, 1]):
				entry["UNK"] = file.read(4).hex().upper()
		
		case 0x87:
			entry["TYPE"] = "0x87"
			entry["UNK"] = file.read(3).hex().upper()
		
		case 0x88:
			entry["TYPE"] = "0x88"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] == 0):
				entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x89:
			entry["TYPE"] = "0x89"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] == 0):
				entry["UNK"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]
		
		case 0x8A:
			entry["TYPE"] = "0x8A"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] == 0):
				entry["STRINGS"] = [readString(file), readString(file)]
		
		case 0x8B:
			entry["TYPE"] = "0x8B"
			entry["UNK"] = file.read(3).hex().upper()
		
		case 0x8C:
			entry["TYPE"] = "0x8C"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x8D:
			entry["TYPE"] = "0x8D"
			entry["UNK"] = file.read(6).hex().upper()
		
		case 0x8E:
			entry["TYPE"] = "0x8E"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x90:
			entry["TYPE"] = "0x90"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] == 0):
				entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x91:
			entry["TYPE"] = "0x91"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			if (entry["CONTROL"] == 0):
				entry["UNK"] = file.read(9).hex().upper()
			
		case 0x92:
			entry["TYPE"] = "0x92"
			entry["UNK"] = file.read(2).hex().upper()
		
		case 0x93:
			entry["TYPE"] = "0x93"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
		case 0x94:
			entry["TYPE"] = "0x94"
			entry["UNK"] = file.read(16).hex().upper()
			
		case 0x95:
			entry["TYPE"] = "0x95"

		case 0x96:
			entry["TYPE"] = "0x96"
			entry["UNK"] = file.read(16).hex().upper()
		
		case 0x97:
			entry["TYPE"] = "0x97"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0x98:
			entry["TYPE"] = "0x98"
			entry["UNK"] = file.read(4).hex().upper()
		
		case 0x99:
			entry["TYPE"] = "0x99"
		
		case 0x9A:
			entry["TYPE"] = "0x9A"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			if (entry["CONTROL"] in [1, 2]):
				entry["UNK"] = file.read(8).hex().upper()
			elif (entry["CONTROL"] in [3, 4]):
				entry["UNK"] = file.read(18).hex().upper()
			else:
				print("UNKNOWN 0x9A CONTROL: 0x%x" % entry["CONTROL"])
				print("OFFSET: 0x%x" % (file.tell() - 2))
				sys.exit()
		
		case 0x9B:
			entry["TYPE"] = "0x9B"
			entry["UNK"] = file.read(14).hex().upper()
		
		case 0x9E:
			entry["TYPE"] = "0x9E"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
		case 0x9F:
			entry["TYPE"] = "0x9F"
			entry["UNK"] = file.read(38).hex().upper()
			entry["STRINGS"] = [readString(file), readString(file)]
		
		case 0xA1:
			entry["TYPE"] = "0xA1"
			entry["UNK"] = file.read(6).hex().upper()
		
		case 0xA2:
			entry["TYPE"] = "0xA2"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]

		case 0xA3:
			entry["TYPE"] = "0xA3"
			entry["UNK"] = file.read(6).hex().upper()
		
		case 0xA4:
			entry["TYPE"] = "0xA4"
			entry["UNK"] = file.read(3).hex().upper()
		
		case 0xA5:
			entry["TYPE"] = "0xA5"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
		
		case 0xA6:
			entry["TYPE"] = "0xA6"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0x32:
					entry["UNK"] = file.read(3).hex().upper()
					entry["STRINGS"] = [readString(file)]
				case 0x3A:
					entry["UNK"] = file.read(9).hex().upper()
				case 0x3C:
					entry["UNK"] = file.read(6).hex().upper()
				case _:
					print("UNKNOWN 0xA6 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0xFF:
			entry["TYPE"] = "0xFF"
			test = file.read(3).hex().upper()
			if (test == "FFFFFF"):
				entry["UNK"] = file.read(24).hex().upper()
			else:
				print("UNKNOWN 0xFF PATTERN: %s" % test)
				print("OFFSET: 0x%x" % (file.tell() - 2))
				sys.exit() 

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
	while(True):
		entry2 = {}
		entry2["UNK0"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]
		entry2["STRINGS1"] = []
		for i in range(0, 8):
			string = readString(file)
			entry2["STRINGS1"].append(string)
			file.seek(0x10 - (len(string) + 1), 1)
		entry2["UNK1"] = file.read(8).hex().upper()
		check = int.from_bytes(file.read(4), byteorder="little", signed=True)
		file.seek(-4, 1)
		if (check == 0):
			entry2["UNK1"] += file.read(8).hex().upper()
		else:
			entry2["STRINGS2"] = [readString(file)]
			file.seek(12 - (len(entry2["STRINGS2"][0]) + 1), 1)

		check = file.read(1)
		file.seek(-1, 1)
		entry["TABLE"].append(entry2)
		if (check == b"\xFF"): break
		if (file.tell() == (until_offset - 4)): break
	
	if (file.tell() == (until_offset - 4)):
		check = int.from_bytes(file.read(4), byteorder="little")
		if (check != 1):
			print("UNEXPECTED MONSTERS ENDING: 0x%x" % check)
			print("OFFSET: 0x%x" % (file.tell() - 4))
			sys.exit()
	else:
		entry["UNK1"] = file.read(0x1C).hex().upper()
	return entry


files = glob.glob("nx/*.dat")
os.makedirs("jsons", exist_ok=True)

for y in range(0, len(files)):
	print(files[y])
	if (files[y] == "nx\\a1700.dat"):
		print("For some reason script stucks at this file.")
		print("When you see that script doesn't continue, in cmd press 'Ctrl+C'.")
		print("This won't cease process, script will continue working.")
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
			if (FUNCTIONS_NAMES[i] != ""):
				cmd = int.from_bytes(file.read(1), byteorder="little")
				CMD_ENTRY = GenerateCommand(cmd, file, end)
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
					if ((len(string) == 6) and (ord(string[0]) >= 0x20)):
						DUMP["FUNCTIONS"]["%04d" % i].append(GenerateMonsters(file, end))
					else:
						cmd = int.from_bytes(file.read(1), byteorder="little")
						CMD_ENTRY = GenerateCommand(cmd, file, end)
						if ((CMD_ENTRY == None) and cmd != 0):
							print("CMD: 0x%x returned None!")
							sys.exit()
						elif CMD_ENTRY != None:
							DUMP["FUNCTIONS"]["%04d" % i].append(CMD_ENTRY)

	file.close()

	file = open("jsons/%s.json" % files[y][3:-4], "w", encoding="UTF-8")
	json.dump(DUMP, file, indent="\t", ensure_ascii=False)
	file.close()