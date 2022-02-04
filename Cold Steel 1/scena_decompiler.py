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
	entry["CONTROLS"] = []
	entry["STRINGS"] = []
	while(True):
		entry["CONTROLS"].append(int.from_bytes(file.read(1), byteorder="little"))
		match(entry["CONTROLS"][len(entry["CONTROLS"]) - 1]):
			case 0:
				return
			
			case 2:
				pass

			case 0xB:
				entry["STRINGS"].append(readStringDialog(file))
			
			case 0x23:
				file.seek(-1, 1)
				entry["STRINGS"].append(readStringDialog(file))
			
			case _:
				print("UNKNOWN DIALOG COMMAND: 0x%x" % entry["CONTROLS"][len(entry["CONTROLS"]) - 1])
				print("OFFSET: 0x%x" % (file.tell() - 1))
				sys.exit()

def CalcGoto(file, entry):
	entry["CONTROLS"] = []
	control = int.from_bytes(file.read(1), byteorder="little")
	entry["CONTROLS"].append(control)
	passing = [5, 0x13]
	while (control != 1):
		if (control in passing):
			control = int.from_bytes(file.read(1), byteorder="little")
			entry["CONTROLS"].append(control)
			continue
		match(control):
			case 0:
				entry["UNK"] = [int.from_bytes(file.read(4), byteorder="little")]
			
			case 0x1E:
				entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little")]

			case 0x1F:
				entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little")]

			case 0x20:
				entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little")]
			
			case 0x21:
				entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little")]
				entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little")]

			case 0x23:
				entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little")]
			
			case 0x24:
				entry["UNK"] = [int.from_bytes(file.read(4), byteorder="little")]

			case 0x25:
				entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little")]
			
			case _:
				print("UNKNOWN GOTO COMMAND: 0x%x" % control)
				print("OFFSET: 0x%x" % (file.tell() - 1))
				sys.exit()
			
		control = int.from_bytes(file.read(1), byteorder="little")
		entry["CONTROLS"].append(control)
		

def GenerateCommand(cmd, file):
	entry = {}
	entry["LABEL"] = "0x%x" % (file.tell() - 1)
	print("0x%x" % cmd)
	match(cmd):
		case 1:
			entry["TYPE"] = "RETURN"
			while(file.tell() % 4 != 0):
				file.seek(1, 1)
		
		case 2:
			entry["TYPE"] = "0x2"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["STRINGS"] = readString(file)
		
		case 3:
			entry["TYPE"] = "GOTO3"
			entry["TO_LABEL"] = "0x%x" % int.from_bytes(file.read(4), byteorder="little")

		case 5:
			entry["TYPE"] = "GOTO5"
			CalcGoto(file, entry)
			entry["TO_LABEL"] = "0x%x" % int.from_bytes(file.read(4), byteorder="little")
		
		case 6:
			entry["TYPE"] = "GOTO5"
			CalcGoto(file, entry)
			count = int.from_bytes(file.read(1), byteorder="little")
			entry["TO_LABELS"] = []
			for i in range(0, count):
				entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little"))
				entry["TO_LABELS"].append("0x%x" % int.from_bytes(file.read(4), byteorder="little"))
			entry["TO_LABELS"].append("0x%x" % int.from_bytes(file.read(4), byteorder="little"))
		
		case 8:
			entry["TYPE"] = "0x8"
			CalcGoto(file, entry)
		
		case 0xE:
			entry["TYPE"] = "0xE"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
		
		case 0xF:
			entry["TYPE"] = "0xF"
			entry["UNK"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]
		
		case 0x10:
			entry["TYPE"] = "0x10"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]

		case 0x12:
			entry["TYPE"] = "0x12"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			CalcGoto(file, entry)
		
		case 0x13:
			entry["TYPE"] = "0x13"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file), readString(file)]
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["STRINGS"].append(readString(file))
			entry["STRINGS"].append(readString(file))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
		
		case 0x14:
			entry["TYPE"] = "0x14"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
			entry["STRINGS"] = [readString(file)]
		
		case 0x16:
			entry["TYPE"] = "0x16"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
		
		case 0x17:
			entry["TYPE"] = "0x17"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]

		case 0x18:
			entry["TYPE"] = "0x18"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			ReadDialog(file, entry)

		case 0x19:
			entry["TYPE"] = "0x19"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			entry["UNK"] = []
			match(entry["CONTROL"]):
				case 0:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
				
				case 1:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
				
				case 2:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))

				case 5:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
				
				case _:
					print("UNKNOWN 0x19 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell - 2))
		
		case 0x1A:
			entry["TYPE"] = "0x1A"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			ReadDialog(file, entry)

		case 0x1B:
			entry["TYPE"] = "0x1B"
			
		case 0x1C:
			entry["TYPE"] = "0x1C"

		case 0x1F:
			entry["TYPE"] = "0x1F"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			entry["CONTROL2"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			assert(entry["CONTROL2"] < 4)
			entry["UNK"] = []
			match(entry["CONTROL"]):
				case 0:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
				
				case 1:
					entry["STRINGS"] = [readString(file)]
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 2:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 3:
					pass
				
				case 4:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
				
				case 5:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 6:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 7:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case _:
					print("UNKNOWN 0x19 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 1))
					sys.exit()

		case 0x20:
			entry["TYPE"] = "0x20"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			assert(entry["CONTROL"] <= 2)
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			if (entry["CONTROL"] > 0):
				entry["UNK"].append(int.from_bytes(file.read(entry["CONTROL"]), byteorder="little", signed=True))
			entry["STRINGS"] = [readString(file), readString(file)]
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
		
		case 0x22:
			entry["TYPE"] = "0x22"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
		
		case 0x23:
			entry["TYPE"] = "0x23"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))

		case 0x24:
			entry["TYPE"] = "0x24"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["STRINGS"] = [readString(file), readString(file)]

		case 0x25:
			entry["TYPE"] = "0x25"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["STRINGS"] = [readString(file), readString(file)]
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])

		case 0x26:
			entry["TYPE"] = "0x26"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["STRINGS"] = [readString(file)]
		
		case 0x2B:
			entry["TYPE"] = "0x2B"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
		
		case 0x2C:
			entry["TYPE"] = "0x2C"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
		
		case 0x2D:
			entry["TYPE"] = "0x2D"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			entry["UNK"] = []
			match(entry["CONTROL"]):
				case 2:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 3:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["STRINGS"] = [readString(file)]
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))

				case 0x14:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["STRINGS"] = [readString(file)]
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 4:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
				
				case 5:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 7:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 8:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 9:
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
				
				case 0xB:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 0xC:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 0xD:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))

				case 0xE:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 0xF:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
				
				case 0x11:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
				
				case 0x12:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 0x13:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
				
				case 0x15:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
				
				case 0x16:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 0x17:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case _:
					print("UNKNOWN 2D CONTROL BYTE: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x32:
			entry["TYPE"] = "0x32"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			match(entry["CONTROL"]):
				case 1:
					entry["STRINGS"] = [readString(file), readString(file)]
				
				case 2:
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
				
				case 3:
					entry["STRINGS"] = [readString(file), readString(file), readString(file), readString(file)]
				
				case 4:
					entry["STRINGS"] = [readString(file)]
				
				case _:
					print("UNKNOWN 0x32 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x33:
			entry["TYPE"] = "0x33"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
		
		case 0x35:
			entry["TYPE"] = "0x35"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			
		case 0x36:
			entry["TYPE"] = "0x36"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["CONTROL"] = int.from_bytes(file.read(2), byteorder="little", signed=True)
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			if (-0x1ff < entry["CONTROL"] < -0x1fc):
				entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))

		case 0x37:
			entry["TYPE"] = "0x37"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
		
		case 0x39:
			entry["TYPE"] = "0x39"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			check = [0xC, 0x5, 0x69, 0xA, 0xB, 0xFF, 0xFE]
			if (entry["CONTROL"] not in check):
				entry["UNK"].append(struct.unpack("<f", file.read(4))[0])

		case 0x3F:
			entry["TYPE"] = "0x3F"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			type1 = [9, 10, 11, 1, 6, 5, 4, 0, 8]
			entry["UNK"] = []
			if (entry["CONTROL"] in type1):
				entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			if (entry["CONTROL"] == 8):
				entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
				entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
				entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
		
		case 0x42:
			entry["TYPE"] = "0x42"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
		
		case 0x44:
			entry["TYPE"] = "0x44"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			match(entry["CONTROL"]):
				case 0:
					entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
				
				case 1:
					pass
				
				case 2:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
				
				case 3:
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
				
				case 4:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 5:
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case _:
					print("UNKNOWN 0x44 CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()

		case 0x4A:
			entry["TYPE"] = "0x4A"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
			entry["STRINGS"] = [readString(file)]
		
		case 0x5F:
			entry["TYPE"] = "0x5F"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little", signed=True)
			match(entry["CONTROL"]):
				case 0:
					entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case 1:
					pass

				case 2:
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
					entry["UNK"].append(struct.unpack("<f", file.read(4))[0])
				
				case 3:
					entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
					entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
				
				case _:
					print("UNKNOWN 0x5F CONTROL: 0x%x" % entry["CONTROL"])
					print("OFFSET: 0x%x" % (file.tell() - 2))
					sys.exit()
		
		case 0x60:
			entry["TYPE"] = "0x60"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
		
		case 0x62:
			entry["TYPE"] = "0x62"
			entry["STRINGS"] = [readString(file)]
			entry["UNK"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
		
		case 0x66:
			entry["TYPE"] = "0x66"
			entry["UNK"] = [struct.unpack("<f", file.read(4))[0]]
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
		
		case 0x70:
			entry["TYPE"] = "0x70"
			entry["CONTROL"] = int.from_bytes(file.read(1), byteorder="little")
			if (entry["CONTROL"] == 1):
				entry["STRINGS"] = [readString(file)]
				entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
				entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))
				entry["UNK"].append(int.from_bytes(file.read(1), byteorder="little", signed=True))

		case 0x79:
			entry["TYPE"] = "0x79"
			entry["UNK"] = [int.from_bytes(file.read(1), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
		
		case 0x82:
			entry["TYPE"] = "0x82"
			entry["UNK"] = [int.from_bytes(file.read(2), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
		
		case 0x96:
			entry["TYPE"] = "0x96"
			entry["UNK"] = [int.from_bytes(file.read(4), byteorder="little", signed=True)]
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(4), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
			entry["UNK"].append(int.from_bytes(file.read(2), byteorder="little", signed=True))
		
		case _:
			print("UNKNOWN COMMAND: 0x%x" % cmd)
			print("Offset: 0x%x" % (file.tell() - 1))
			sys.exit()
		
	return entry

file = open(sys.argv[1], "rb")

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
	DUMP["FUNCTIONS"]["%s" % FUNCTIONS_NAMES[i] if (FUNCTIONS_NAMES[i] != "") else "DUMMY_%d" % i] = []
	file.seek(FUNCTIONS_POINTERS[i])
	if (i < (function_names_count - 1)):
		end = FUNCTIONS_POINTERS[i + 1]
	else:
		end = file_size
	while(file.tell() < end):
		cmd = int.from_bytes(file.read(1), byteorder="little")
		DUMP["FUNCTIONS"]["%s" % FUNCTIONS_NAMES[i] if (FUNCTIONS_NAMES[i] != "") else "DUMMY_%d" % i].append(GenerateCommand(cmd, file))

file.close()

file = open("%s.json" % sys.argv[1][:-4], "w", encoding="UTF-8")
json.dump(DUMP, file, indent="\t", ensure_ascii=False)
file.close()