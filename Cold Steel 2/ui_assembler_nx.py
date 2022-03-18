import glob
import os
import json
import sys
import numpy

def WriteDialog(dialog):
	entry = []
	for i in range(0, len(dialog["STRINGS"])):
		size = len(dialog["STRINGS"][i])
		if (size < 5):
			entry.append(dialog["STRINGS"][i].encode("UTF-8").replace(b"\n", b"\x01"))
			continue
		match(dialog["STRINGS"][i][0:5]):
			case "NEW_L":
				entry.append(numpy.uint8(1))
			case "CMD: ":
				entry.append(numpy.uint8(int(dialog["STRINGS"][i].replace("CMD: ", ""))))
			case "KEY_W":
				entry.append(numpy.uint8(2))
			case "CLEAR":
				entry.append(numpy.uint8(3))
			case "SHOW_":
				entry.append(numpy.uint8(6))
			case "SET_C":
				entry.append(numpy.uint8(7))
			case "ITEM_":
				entry.append(numpy.uint8(0x10))
				entry.append(numpy.uint16(int(dialog["STRINGS"][i].replace("ITEM_ID: ", ""))))
			case "VOICE":
				entry.append(numpy.uint8(0x11))
				entry.append(numpy.uint32(int(dialog["STRINGS"][i].replace("VOICE_FILE_ID: ", ""))))
			case "CMD12":
				entry.append(numpy.uint32(int(dialog["STRINGS"][i].replace("CMD12_ARG: ", ""))))
			case _:
				entry.append(dialog["STRINGS"][i].encode("UTF-8").replace(b"\n", b"\x01"))
	entry.append(b"\x00")
	return b"".join(entry)
			

def CalcGoto(table):
	entry = []
	for i in range(0, len(table)):
		entry.append(numpy.uint8(table[i]["CONTROL"]))
		if (table[i]["CONTROL"] in [2, 3, 4, 5, 6, 7, 8, 9, 0xA, 0xB, 0xC, 0xD, 0xE, 0x10, 0x11, 0x12, 0x13, 0x17, 0x22]):
			continue
		match(table[i]["CONTROL"]):
			case 0:
				entry.append(numpy.int32(table[i]["UNK"][0]))
			case 0x1E:
				entry.append(numpy.int16(table[i]["UNK"][0]))
			case 0x1F:
				entry.append(numpy.int8(table[i]["UNK"][0]))
			case 0x20:
				entry.append(numpy.int8(table[i]["UNK"][0]))
			case 0x21:
				entry.append(bytes.fromhex(table[i]["UNK"]))
			case 0x23:
				entry.append(numpy.int8(table[i]["UNK"][0]))
			case 0x24:
				entry.append(numpy.int32(table[i]["UNK"][0]))
			case 0x25:
				entry.append(numpy.int16(table[i]["UNK"][0]))
			case 0x1C:
				entry.append(GenerateCommand(table[i]["INSTRUCTION"]))
	entry.append(numpy.uint8(1))
	return b"".join(entry)

def GenerateCommand(entry, Offset_dict = None):
	ret_entry = []
	match(entry["TYPE"]):
		case "RETURN":
			ret_entry.append(numpy.uint8(1))
		case "JUMP_TO_FUNCTION":
			ret_entry.append(numpy.uint8(2))
			ret_entry.append(numpy.int8(entry["UNK"][0]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "GOTO3":
			ret_entry.append(numpy.uint8(3))
			if (Offset_dict == None):
				ret_entry.append(numpy.uint32(0))
			else:
				ret_entry.append(numpy.uint32(Offset_dict[entry["TO_LABEL"]]))
		case "0x4":
			ret_entry.append(numpy.uint8(4))
			ret_entry.append(numpy.int8(entry["UNK"][0]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "GOTO5":
			ret_entry.append(numpy.uint8(5))
			ret_entry.append(CalcGoto(entry["TABLE"]))
			if (Offset_dict == None):
				ret_entry.append(numpy.uint32(0))
			else:
				ret_entry.append(numpy.uint32(Offset_dict[entry["TO_LABEL"]]))
			
		case "GOTO6":
			ret_entry.append(numpy.uint8(6))
			ret_entry.append(CalcGoto(entry["TABLE"]))
			ret_entry.append(numpy.uint8(len(entry["TO_LABELS"])))
			for i in range(0, len(entry["TO_LABELS"])):
				ret_entry.append(numpy.uint16(entry["TO_LABELS"][i]["UNK"][0]))
				if (Offset_dict == None):
					ret_entry.append(numpy.uint32(0))
				else:
					ret_entry.append(numpy.uint32(Offset_dict[entry["TO_LABELS"][i]["TO_LABEL"]]))
			if (Offset_dict == None):
				ret_entry.append(numpy.uint32(0))
			else:
				ret_entry.append(numpy.uint32(Offset_dict[entry["TO_LABEL"]]))
		case "0x7":
			ret_entry.append(numpy.uint8(7))
			ret_entry.append(numpy.int32(entry["UNK"][0]))
		case "0x8":
			ret_entry.append(numpy.uint8(8))
			ret_entry.append(CalcGoto(entry["TABLE"]))
		case "0xA":
			ret_entry.append(numpy.uint8(0xA))
			ret_entry.append(numpy.int8(entry["UNK"][0]))
			ret_entry.append(CalcGoto(entry["TABLE"]))
		case "0xC":
			ret_entry.append(numpy.uint8(0xC))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0xD":
			ret_entry.append(numpy.uint8(0xD))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0xE":
			ret_entry.append(numpy.uint8(0xE))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0xF":
			ret_entry.append(numpy.uint8(0xF))
			ret_entry.append(numpy.int32(entry["UNK"][0]))
		case "0x10":
			ret_entry.append(numpy.uint8(0x10))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0x11":
			ret_entry.append(numpy.uint8(0x11))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x12":
			ret_entry.append(numpy.uint8(0x12))
			ret_entry.append(numpy.int8(entry["UNK"][0]))
			ret_entry.append(CalcGoto(entry["TABLE"]))
		case "0x13":
			ret_entry.append(numpy.uint8(0x13))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK0"]))
			if (entry["CONTROL"] == 0):
				ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
				ret_entry.append(entry["STRINGS"][1].encode("UTF-8") + b"\x00")
			elif (entry["CONTROL"] in [0xB, 0x22, 0x2B, 0x33, 0x38, 0x3B]):
				ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			if (entry["CONTROL"] in [0xB, 0x22, 0x2B, 0x33]):
				ret_entry.append(bytes.fromhex(entry["UNK1"]))
		case "0x14":
			ret_entry.append(numpy.uint8(0x14))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "0x15":
			ret_entry.append(numpy.uint8(0x15))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x16":
			ret_entry.append(numpy.uint8(0x16))
			ret_entry.append(numpy.int8(entry["UNK"][0]))
		case "0x17":
			ret_entry.append(numpy.uint8(0x17))
			ret_entry.append(numpy.int8(entry["UNK"][0]))
		case "TEXT18":
			ret_entry.append(numpy.uint8(0x18))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
			ret_entry.append(WriteDialog(entry["DIALOG"]))
		case "0x19":
			ret_entry.append(numpy.uint8(0x19))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "MESSAGE":
			ret_entry.append(numpy.uint8(0x1A))
			ret_entry.append(numpy.int16(entry["NAME_ID"]))
			ret_entry.append(WriteDialog(entry["DIALOG"]))
		case "0x1B":
			ret_entry.append(numpy.uint8(0x1B))
		case "REMOVE_TEXT_BOX":
			ret_entry.append(numpy.uint8(0x1C))
		case "OVERRIDE_DIALOG_SPEAKER":
			ret_entry.append(numpy.uint8(0x1D))
			ret_entry.append(entry["NAME"][0].encode("UTF-8") + b"\x00")
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "JUMP_TO_ID":
			ret_entry.append(numpy.uint8(0x1E))
			for i in range(0, 2):
				ret_entry.append(entry["STRINGS"][i].encode("UTF-8") + b"\x00")
		case "0x1F":
			ret_entry.append(numpy.uint8(0x1F))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			ret_entry.append(numpy.int8(entry["CONTROL2"]))
			if (entry["CONTROL"] != 3):
				if (entry["CONTROL"] == 1):
					ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
				ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x20":
			ret_entry.append(numpy.uint8(0x20))
			ret_entry.append(numpy.uint8(entry["SIZE_CHECK"]))
			ret_entry.append(bytes.fromhex(entry["UNK0"]))
			for i in range(0, 2):
				ret_entry.append(entry["STRINGS"][i].encode("UTF-8") + b"\x00")
			ret_entry.append(numpy.int8(entry["UNK1"][0]))
		case "0x21":
			ret_entry.append(numpy.uint8(0x21))
			ret_entry.append(numpy.uint8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x22":
			ret_entry.append(numpy.uint8(0x22))
			ret_entry.append(numpy.int16(entry["UNK0"][0]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			ret_entry.append(bytes.fromhex(entry["UNK1"]))
		case "0x23":
			ret_entry.append(numpy.uint8(0x23))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x24":
			ret_entry.append(numpy.uint8(0x24))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
			for i in range(0, 2):
				ret_entry.append(entry["STRINGS"][i].encode("UTF-8") + b"\x00")
		case "0x25":
			ret_entry.append(numpy.uint8(0x25))
			ret_entry.append(bytes.fromhex(entry["UNK0"]))
			for i in range(0, 2):
				ret_entry.append(entry["STRINGS"][i].encode("UTF-8") + b"\x00")
			ret_entry.append(bytes.fromhex(entry["UNK1"]))
		case "0x26":
			ret_entry.append(numpy.uint8(0x26))
			ret_entry.append(numpy.int8(entry["UNK"][0]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "0x27":
			ret_entry.append(numpy.uint8(0x27))
			ret_entry.append(numpy.uint8(entry["CONTROL"]))
			if (entry["CONTROL"] in [0x11, 0x10, 0xF, 0xB, 0xD, 0xE, 0x12, 0x13, 0x14, 0xA, 0x15]):
				ret_entry.append(bytes.fromhex(entry["UNK"]))
			elif (entry["CONTROL"] == 0xC):
				ret_entry.append(bytes.fromhex(entry["UNK0"]))
			if (entry["CONTROL"] in [0xA, 0xC, 0x15]):
				ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			if (entry["CONTROL"] == 0xC):
				ret_entry.append(bytes.fromhex(entry["UNK1"]))
		case "0x28":
			ret_entry.append(numpy.uint8(0x28))
			ret_entry.append(numpy.uint8(entry["CONTROL"]))
			match(entry["CONTROL"]):
				case 80:
					ret_entry.append(numpy.int16(entry["UNK0"][0]))
					ret_entry.append(entry["STRINGS1"][0].encode("UTF-8") + b"\x00")
					ret_entry.append(bytes.fromhex(entry["UNK1"]))
					ret_entry.append(entry["STRINGS2"][0].encode("UTF-8") + b"\x00")
				case 100:
					ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
				case _:
					ret_entry.append(bytes.fromhex(entry["UNK"]))
					if (entry["CONTROL"] == ord("i")):
						for i in range(0, 2):
							ret_entry.append(entry["STRINGS"][i].encode("UTF-8") + b"\x00")
					elif (entry["CONTROL"] in [ord("\a"), 5]):
						ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "0x29":
			ret_entry.append(numpy.uint8(0x29))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x2A":
			ret_entry.append(numpy.uint8(0x2A))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0x2B":
			ret_entry.append(numpy.uint8(0x2B))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x2C":
			ret_entry.append(numpy.uint8(0x2C))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x2D":
			ret_entry.append(numpy.uint8(0x2D))
			ret_entry.append(numpy.uint8(entry["CONTROL"]))
			if (entry["CONTROL"] in [3, 0x14]):
				ret_entry.append(bytes.fromhex(entry["UNK0"]))
				ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
				ret_entry.append(bytes.fromhex(entry["UNK1"]))
			elif (entry["CONTROL"] in [0, 0x10]):
				pass
			else:
				ret_entry.append(bytes.fromhex(entry["UNK0"]))
		case "0x2E":
			ret_entry.append(numpy.uint8(0x2E))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x2F":
			ret_entry.append(numpy.uint8(0x2F))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "0x30":
			ret_entry.append(numpy.uint8(0x30))
			ret_entry.append(numpy.uint8(entry["CONTROL"]))
			if (entry["CONTROL"] != 7):
				ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x31":
			ret_entry.append(numpy.uint8(0x31))
			ret_entry.append(numpy.uint8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
			if (entry["CONTROL"] in [0, 0x32]):
				ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "0x32":
			ret_entry.append(numpy.uint8(0x32))
			ret_entry.append(numpy.uint8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
			if (entry["CONTROL"] in [1, 3, 4]):
				for i in range(0, len(entry["STRINGS"])):
					ret_entry.append(entry["STRINGS"][i].encode("UTF-8") + b"\x00")
		case "0x33":
			ret_entry.append(numpy.uint8(0x33))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x34":
			ret_entry.append(numpy.uint8(0x34))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x35":
			ret_entry.append(numpy.uint8(0x35))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0x36":
			ret_entry.append(numpy.uint8(0x36))
			ret_entry.append(numpy.int16(entry["UNK0"][0]))
			ret_entry.append(numpy.int16(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK1"]))
		case "0x37":
			ret_entry.append(numpy.uint8(0x37))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x38":
			ret_entry.append(numpy.uint8(0x38))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x39":
			ret_entry.append(numpy.uint8(0x39))
			ret_entry.append(numpy.uint8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x3A":
			ret_entry.append(numpy.uint8(0x3A))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x3B":
			ret_entry.append(numpy.uint8(0x3B))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x3C":
			ret_entry.append(numpy.uint8(0x3C))
			for i in range(0, 3):
				ret_entry.append(numpy.uint16(entry["CONTROLS"][i]))
			try:
				ret_entry.append(bytes.fromhex(entry["UNK"]))
			except:
				pass
		case "0x3D":
			ret_entry.append(numpy.uint8(0x3D))
			ret_entry.append(numpy.int8(entry["UNK0"][0]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			ret_entry.append(numpy.int16(entry["UNK1"][0]))
		case "0x3E":
			ret_entry.append(numpy.uint8(0x3E))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x3F":
			ret_entry.append(numpy.uint8(0x3F))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			try:
				ret_entry.append(bytes.fromhex(entry["UNK"]))
			except:
				pass
		case "0x40":
			ret_entry.append(numpy.uint8(0x40))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x41":
			ret_entry.append(numpy.uint8(0x41))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x42":
			ret_entry.append(numpy.uint8(0x42))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x43":
			ret_entry.append(numpy.uint8(0x43))
			ret_entry.append(numpy.int32(entry["UNK"][0]))
		case "0x44":
			ret_entry.append(numpy.uint8(0x44))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x45":
			ret_entry.append(numpy.uint8(0x45))
			for i in range(0, 2):
				ret_entry.append(entry["STRINGS"][i].encode("UTF-8") + b"\x00")
		case "0x46":
			ret_entry.append(numpy.uint8(0x46))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x47":
			ret_entry.append(numpy.uint8(0x47))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x48":
			ret_entry.append(numpy.uint8(0x48))
			ret_entry.append(numpy.int8(entry["UNK"][0]))
		case "0x49":
			ret_entry.append(numpy.uint8(0x49))
			ret_entry.append(numpy.uint8(entry["CONTROL"]))
			if (entry["CONTROL"] in [0xB, 0xE, 0xF, 0x10, 0x11, 0x12, 0x16, 0x1D, 0x1E, 0x20, 0x25]):
				pass
			elif (entry["CONTROL"] in [10, 4, 3, 2, 1, 0]):
				ret_entry.append(bytes.fromhex(entry["UNK"]))
			else:
				if (entry["CONTROL"] in [0xD, 0x14, 0x15, 0x19, 0x1C]):
					for i in range(0, len(entry["STRINGS"])):
						ret_entry.append(entry["STRINGS"][i].encode("UTF-8") + b"\x00")
				if (entry["CONTROL"] in [0xD, 0x14, 0x17, 0x18, 0x1C, 0x21, 0x23, 0x24, 0x26, 0x28, 0x29]):
					ret_entry.append(bytes.fromhex(entry["UNK"]))
				if (entry["CONTROL"] == 0x26):
					ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "0x4A":
			ret_entry.append(numpy.uint8(0x4A))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "0x4B":
			ret_entry.append(numpy.uint8(0x4B))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x4C":
			ret_entry.append(numpy.uint8(0x4C))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x4D":
			ret_entry.append(numpy.uint8(0x4D))
			ret_entry.append(numpy.int8(entry["UNK"][0]))
		case "0x4F":
			ret_entry.append(numpy.uint8(0x4F))
			ret_entry.append(bytes.fromhex(entry["UNK0"]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			ret_entry.append(bytes.fromhex(entry["UNK1"]))
		case "0x51":
			ret_entry.append(numpy.uint8(0x51))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "0x52":
			ret_entry.append(numpy.uint8(0x52))
			ret_entry.append(numpy.int16(entry["UNK0"][0]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			ret_entry.append(bytes.fromhex(entry["UNK1"]))
		case "0x53":
			ret_entry.append(numpy.uint8(0x53))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x55":
			ret_entry.append(numpy.uint8(0x55))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "0x56":
			ret_entry.append(numpy.uint8(0x56))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0x57":
			ret_entry.append(numpy.uint8(0x57))
		case "0x58":
			ret_entry.append(numpy.uint8(0x58))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x59":
			ret_entry.append(numpy.uint8(0x59))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0x5A":
			ret_entry.append(numpy.uint8(0x5A))
			ret_entry.append(numpy.int8(entry["UNK0"][0]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			ret_entry.append(numpy.int16(entry["UNK1"][0]))
		case "0x5B":
			ret_entry.append(numpy.uint8(0x5B))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x5C":
			ret_entry.append(numpy.uint8(0x5C))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x5D":
			ret_entry.append(numpy.uint8(0x5D))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			try:
				ret_entry.append(bytes.fromhex(entry["UNK"]))
			except:
				pass
		case "0x5E":
			ret_entry.append(numpy.uint8(0x5E))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x5F":
			ret_entry.append(numpy.uint8(0x5F))
			ret_entry.append(numpy.int16(entry["UNK0"]))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			if (entry["CONTROL"] != 1):
				ret_entry.append(bytes.fromhex(entry["UNK1"]))
		case "0x60":
			ret_entry.append(numpy.uint8(0x60))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x61":
			ret_entry.append(numpy.uint8(0x61))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x62":
			ret_entry.append(numpy.uint8(0x62))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x63":
			ret_entry.append(numpy.uint8(0x63))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x64":
			ret_entry.append(numpy.uint8(0x64))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x65":
			ret_entry.append(numpy.uint8(0x65))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x66":
			ret_entry.append(numpy.uint8(0x66))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x67":
			ret_entry.append(numpy.uint8(0x67))
			ret_entry.append(numpy.uint16(entry["CONTROLS"][0]))
			ret_entry.append(numpy.uint8(entry["CONTROLS"][1]))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x68":
			ret_entry.append(numpy.uint8(0x68))
			ret_entry.append(numpy.int16(entry["UNK0"][0]))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK1"]))
		case "0x69":
			ret_entry.append(numpy.uint8(0x69))
			ret_entry.append(numpy.int16(entry["UNK0"][0]))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			match(entry["CONTROL"]):
				case 0:
					ret_entry.append(bytes.fromhex(entry["UNK1"]))
				case 2:
					ret_entry.append(bytes.fromhex(entry["UNK1"]))
					ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
				case 3:
					ret_entry.append(entry["STRINGS1"][0].encode("UTF-8") + b"\x00")
					ret_entry.append(bytes.fromhex(entry["UNK1"]))
					ret_entry.append(entry["STRINGS2"][0].encode("UTF-8") + b"\x00")
				case 5:
					ret_entry.append(bytes.fromhex(entry["UNK1"]))
		case "0x6A":
			ret_entry.append(numpy.uint8(0x6A))
			ret_entry.append(numpy.int8(entry["CONTROLS"][0]))
			ret_entry.append(numpy.int8(entry["CONTROLS"][1]))
			if(entry["CONTROLS"][0] == 1):
				ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			if(entry["CONTROLS"][0] != 3):
				ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x6B":
			ret_entry.append(numpy.uint8(0x6B))
			ret_entry.append(numpy.int16(entry["UNK0"][0]))
			for i in range(0, 2):
				ret_entry.append(entry["STRINGS"][i].encode("UTF-8") + b"\x00")
			ret_entry.append(numpy.int8(entry["UNK1"][0]))
		case "0x6C":
			ret_entry.append(numpy.uint8(0x6C))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0x6D":
			ret_entry.append(numpy.uint8(0x6D))
			ret_entry.append(numpy.int8(entry["UNK"][0]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "0x6E":
			ret_entry.append(numpy.uint8(0x6E))
			ret_entry.append(numpy.uint8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x6F":
			ret_entry.append(numpy.uint8(0x6F))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			if (entry["CONTROL"] in [1, 2]):
				ret_entry.append(numpy.int16(entry["UNK"][0]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "0x70":
			ret_entry.append(numpy.uint8(0x70))
			ret_entry.append(numpy.uint8(entry["CONTROL"]))
			if (entry["CONTROL"] == 1):
				ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
				ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x71":
			ret_entry.append(numpy.uint8(0x71))
			ret_entry.append(numpy.uint8(entry["CONTROL"]))
			if (entry["CONTROL"] == 0):
				ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x72":
			ret_entry.append(numpy.uint8(0x72))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0x73":
			ret_entry.append(numpy.uint8(0x73))
			ret_entry.append(numpy.uint8(entry["CONTROL"]))
			if (entry["CONTROL"] > 1):
				ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x74":
			ret_entry.append(numpy.uint8(0x74))
			ret_entry.append(numpy.int8(entry["UNK"][0]))
		case "0x77":
			ret_entry.append(numpy.uint8(0x77))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x78":
			ret_entry.append(numpy.uint8(0x78))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x79":
			ret_entry.append(numpy.uint8(0x79))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x7A":
			ret_entry.append(numpy.uint8(0x7A))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x7B":
			ret_entry.append(numpy.uint8(0x7B))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "0x7D":
			ret_entry.append(numpy.uint8(0x7D))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x7E":
			ret_entry.append(numpy.uint8(0x7E))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0x7F":
			ret_entry.append(numpy.uint8(0x7F))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK0"]))
			for i in range(0, len(entry["STRINGS"])):
				ret_entry.append(entry["STRINGS"][i].encode("UTF-8") + b"\x00")
			if (entry["CONTROL"] not in [0, 1]):
				ret_entry.append(bytes.fromhex(entry["UNK1"]))
		case "0x81":
			ret_entry.append(numpy.uint8(0x81))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			if (entry["CONTROL"] in [0, 3, 4]):
				ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0x82":
			ret_entry.append(numpy.uint8(0x82))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x83":
			ret_entry.append(numpy.uint8(0x83))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x84":
			ret_entry.append(numpy.uint8(0x84))
		case "0x85":
			ret_entry.append(numpy.uint8(0x85))
			ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			ret_entry.append(numpy.int32(entry["UNK"][0]))
		case "0x86":
			ret_entry.append(numpy.uint8(0x86))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			try:
				ret_entry.append(bytes.fromhex(entry["UNK"]))
			except:
				pass
		case "0x87":
			ret_entry.append(numpy.uint8(0x87))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x88":
			ret_entry.append(numpy.uint8(0x88))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			if (entry["CONTROL"] == 0):
				ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0x89":
			ret_entry.append(numpy.uint8(0x89))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			if (entry["CONTROL"] == 0):
				ret_entry.append(numpy.int32(entry["UNK"][0]))
		case "0x8A":
			ret_entry.append(numpy.uint8(0x8A))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			if (entry["CONTROL"] == 0):
				for i in range(0, 2):
					ret_entry.append(entry["STRINGS"][i].encode("UTF-8") + b"\x00")
		case "0x8B":
			ret_entry.append(numpy.uint8(0x8B))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x8C":
			ret_entry.append(numpy.uint8(0x8C))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0x8D":
			ret_entry.append(numpy.uint8(0x8D))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x8E":
			ret_entry.append(numpy.uint8(0x8E))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0x90":
			ret_entry.append(numpy.uint8(0x90))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			if (entry["CONTROL"] == 0):
				ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0x91":
			ret_entry.append(numpy.uint8(0x91))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			if (entry["CONTROL"] == 0):
				ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x92":
			ret_entry.append(numpy.uint8(0x92))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x93":
			ret_entry.append(numpy.uint8(0x93))
			ret_entry.append(numpy.int8(entry["UNK"][0]))
		case "0x94":
			ret_entry.append(numpy.uint8(0x94))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x95":
			ret_entry.append(numpy.uint8(0x95))
		case "0x96":
			ret_entry.append(numpy.uint8(0x96))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x97":
			ret_entry.append(numpy.uint8(0x97))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0x98":
			ret_entry.append(numpy.uint8(0x98))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x99":
			ret_entry.append(numpy.uint8(0x99))
		case "0x9A":
			ret_entry.append(numpy.uint8(0x9A))
			ret_entry.append(numpy.uint8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x9B":
			ret_entry.append(numpy.uint8(0x9B))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0x9E":
			ret_entry.append(numpy.uint8(0x9E))
			ret_entry.append(numpy.int8(entry["UNK"][0]))
		case "0x9F":
			ret_entry.append(numpy.uint8(0x9F))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
			for i in range(0, 2):
				ret_entry.append(entry["STRINGS"][i].encode("UTF-8") + b"\x00")
		case "0xA1":
			ret_entry.append(numpy.uint8(0xA1))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0xA2":
			ret_entry.append(numpy.uint8(0xA2))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0xA3":
			ret_entry.append(numpy.uint8(0xA3))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0xA4":
			ret_entry.append(numpy.uint8(0xA4))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "0xA5":
			ret_entry.append(numpy.uint8(0xA5))
			ret_entry.append(numpy.int16(entry["UNK"][0]))
		case "0xA6":
			ret_entry.append(numpy.uint8(0xA6))
			ret_entry.append(numpy.int8(entry["CONTROL"]))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
			if (entry["CONTROL"] == 0x32):
				ret_entry.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
		case "0xFF":
			ret_entry.append(numpy.int32(-1))
			ret_entry.append(bytes.fromhex(entry["UNK"]))
		case "CREATE_MONSTERS":
			try:
				ret_entry.append(entry["MAP"].encode("UTF-8") + b"\x00")
			except:
				ret_entry.append(bytes.fromhex(entry["UNK0"]))
			else:
				ret_entry.append(b"\x00" * (0x10 - len(entry["MAP"].encode("UTF-8") + b"\x00")))
				ret_entry.append(bytes.fromhex(entry["UNK0"]))
				table = entry["TABLE"]
				for i in range(0, len(table)):
					ret_entry.append(numpy.int32(table[i]["UNK0"][0]))
					for x in range(0, 8):
						ret_entry.append(table[i]['STRINGS1'][x].encode("UTF-8") + b"\x00")
						ret_entry.append(b"\x00" * (0x10 - len(table[i]['STRINGS1'][x].encode("UTF-8") + b"\x00")))
					ret_entry.append(bytes.fromhex(table[i]["UNK1"]))
					try:
						ret_entry.append(table[i]['STRINGS2'][0].encode("UTF-8") + b"\x00")
					except:
						pass
					else:
						ret_entry.append(b"\x00" * (12 - len(table[i]['STRINGS1'][x].encode("UTF-8") + b"\x00")))
				try:
					ret_entry.append(bytes.fromhex(entry["UNK1"]))
				except:
					ret_entry.append(numpy.uint32(1))
		case _:
			print("UNKNOWN COMMAND: %s" % entry["TYPE"])
			sys.exit()

	return b"".join(ret_entry)

files = glob.glob("jsons/*.json")

os.makedirs("new_nx", exist_ok=True)
for i in range(0, len(files)):
	print(files[i])
	file = open(files[i], "r", encoding="UTF-8")
	DUMP = json.load(file)
	file.close()

	# Write Header
	file_new = open("new_nx/%s.dat" % files[i][6:-5], "wb")
	file_new.write(numpy.uint32(0x20)) #0x0 always starting with 0x20
	file_new.write(numpy.uint32(0x20)) #0x4 always starting with 0x20
	functions_pointer = 0x20 + len(DUMP["HEADER"]["ID"]) + 1
	file_new.write(numpy.uint32(functions_pointer)) #0x08
	size_of_functions_pointer_table = len(DUMP["FUNCTIONS"]) * 4
	file_new.write(numpy.uint32(size_of_functions_pointer_table)) #0x0C
	file_new.write(numpy.uint32(functions_pointer + size_of_functions_pointer_table)) #0x10
	file_new.write(numpy.uint32(len(DUMP["FUNCTIONS"]))) #0x14
	keys = list(DUMP["FUNCTIONS"].keys())
	rekeys = []
	for x in range(0, len(keys)):
		try:
			int(keys[x])
		except:
			rekeys.append(keys[x].encode("ASCII"))
		else:
			if (int(keys[x]) == x):
				rekeys.append(b"")
			else:
				rekeys.append(keys[x].encode("ASCII"))
	file_new.seek(4, 1)
	file_new.write(numpy.uint32(int(DUMP["HEADER"]["TYPE"], base=16))) #0x1C
	file_new.write(DUMP["HEADER"]["ID"].encode("ASCII") + b"\x00")
	functions_pointer_table_ptr = file_new.tell()
	file_new.seek(size_of_functions_pointer_table, 1)
	functions_strings_table_ptr = file_new.tell()
	functions_string_pointers = []
	entry = []
	for x in range(0, len(rekeys)):
		file_new.write(numpy.uint16(functions_pointer + size_of_functions_pointer_table + (len(DUMP["FUNCTIONS"]) * 2) + len(b"".join(entry))))
		entry.append(rekeys[x] + b"\x00")
	file_new.write(b"".join(entry))
	pos = file_new.tell()
	file_new.seek(0x18)
	file_new.write(numpy.uint32(pos))
	file_new.seek(pos)
	while (file_new.tell() % 4 != 0):
		file_new.write(b"\x00")

	#Write Commands
	offset = file_new.tell()
	Label_offsets = {}
	for x in range(0, len(keys)):
		COMMAND_BLOCK = []
		pos = file_new.tell()
		file_new.seek(functions_pointer + (4 * x))
		file_new.write(numpy.uint32(pos))
		file_new.seek(pos)
		temp = []
		for y in range(0, len(DUMP["FUNCTIONS"][keys[x]])):
			entry = DUMP["FUNCTIONS"][keys[x]][y]
			if (entry["TYPE"] != "CREATE_MONSTERS"):
				Label_offsets[entry["LABEL"]] = offset
			offset += len(GenerateCommand(entry))
		if (x != (len(keys) - 1)):
			if (offset % 4 != 0):
				offset += (4 - (offset % 4))
		for y in range(0, len(DUMP["FUNCTIONS"][keys[x]])):
			entry = DUMP["FUNCTIONS"][keys[x]][y]
			COMMAND_BLOCK.append(GenerateCommand(entry, Label_offsets))
		file_new.write(b"".join(COMMAND_BLOCK))
		if (x != (len(keys) - 1)):
			while (file_new.tell() % 4 != 0):
				file_new.write(b"\x00")
	#print(Label_offsets)
	file_new.close()