import os
import json
import numpy
import sys

class Utils:
	text_counter = 0

def GetFileSize(file):
	pos = file.tell()
	file.seek(0, 2)
	size = file.tell()
	file.seek(pos)
	return size

def ProcessCommands(dict, precalcs = None):
	entry = []
	match(dict["CMD"]):
		case "0":
			entry.append(numpy.uint8(0))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "IFGOTO":
			entry.append(numpy.uint8(1))
			if (precalcs == None):
				entry.append(numpy.uint32(0))
			else:
				entry.append(numpy.uint32(precalcs[dict["TO_LABEL"]]))
		case "JMP":
			entry.append(numpy.uint8(2))
			entry.append(numpy.uint32(dict["ID"]))
		case "JMP4":
			entry.append(numpy.uint8(4))
			entry.append(numpy.uint32(dict["ID"]))
		case "RETURN":
			entry.append(numpy.uint8(5))
			try:
				dict["DATA"]
			except:
				pass
			else:
				entry.append(bytes.fromhex(dict["DATA"]))
		case "IFGOTO6":
			entry.append(numpy.uint8(6))
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(numpy.uint32(0))
			else:
				entry.append(numpy.uint32(precalcs[dict["TO_LABEL"]]))
		case "IFGOTO7":
			entry.append(numpy.uint8(7))
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(numpy.uint32(0))
			else:
				entry.append(numpy.uint32(precalcs[dict["TO_LABEL"]]))
		case "IFGOTO8":
			entry.append(numpy.uint8(8))
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(numpy.uint32(0))
			else:
				entry.append(numpy.uint32(precalcs[dict["TO_LABEL"]]))
		case "IFGOTOA":
			entry.append(numpy.uint8(0xA))
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(numpy.uint32(0))
			else:
				entry.append(numpy.uint32(precalcs[dict["TO_LABEL"]]))
		case "IFGOTOB":
			entry.append(numpy.uint8(0xB))
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(numpy.uint32(0))
			else:
				entry.append(numpy.uint32(precalcs[dict["TO_LABEL"]]))
		case "IFGOTOC":
			entry.append(numpy.uint8(0xC))
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(numpy.uint32(0))
			else:
				entry.append(numpy.uint32(precalcs[dict["TO_LABEL"]]))
		case "GOTO":
			entry.append(numpy.uint8(0xD))
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(numpy.uint32(0))
			else:
				entry.append(numpy.uint32(precalcs[dict["TO_LABEL"]]))
			try:
				dict["DATA2"]
			except:
				pass
			else:
				entry.append(numpy.uint8(0))
		case "IFGOTOE":
			entry.append(numpy.uint8(0xE))
			entry.append(bytes.fromhex(dict["DATA"]))
			entry.append(numpy.uint16(len(dict["LIST"])))
			for s in range(0, len(dict["LIST"])):
				entry.append(numpy.uint16(dict["LIST"][s]["VALUE"]))
				if (precalcs == None):
					entry.append(numpy.uint32(0))
				else:
					entry.append(numpy.uint32(precalcs[dict["LIST"][s]["TO_LABEL"]]))
		case "CMP":
			entry.append(numpy.uint8(0x10))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "11":
			entry.append(numpy.uint8(0x11))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "12":
			entry.append(numpy.uint8(0x12))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "13":
			entry.append(numpy.uint8(0x13))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "14":
			entry.append(numpy.uint8(0x14))
			entry.append(bytes.fromhex("98800200"))
		case "1A":
			entry.append(numpy.uint8(0x1A))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "1B":
			entry.append(numpy.uint8(0x1B))
		case "1C":
			entry.append(numpy.uint8(0x1C))
		case "1D":
			entry.append(numpy.uint8(0x1D))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "1E":
			entry.append(numpy.uint8(0x1E))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "1F":
			entry.append(numpy.uint8(0x1F))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "20":
			entry.append(numpy.uint8(0x20))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "21":
			entry.append(numpy.uint8(0x21))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "22":
			entry.append(numpy.uint8(0x22))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "23":
			entry.append(numpy.uint8(0x23))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "24":
			entry.append(numpy.uint8(0x24))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "25":
			entry.append(numpy.uint8(0x25))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "2D":
			entry.append(numpy.uint8(0x2D))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "2E":
			entry.append(numpy.uint8(0x2E))
		case "2F":
			entry.append(numpy.uint8(0x2F))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "30":
			entry.append(numpy.uint8(0x30))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "31":
			entry.append(numpy.uint8(0x31))
			entry.append(bytes.fromhex("8080"))
			entry.append(numpy.uint16(len(dict["LIST"])))
			entry.append(numpy.uint16(dict["UNK0"]))
			for s in range(0, len(dict["LIST"])):
				entry.append(numpy.uint8(dict["LIST"][s]["ID"]))
				entry.append(bytes.fromhex(dict["LIST"][s]["DATA"]))
				if (precalcs == None):
					entry.append(numpy.uint32(0))
				else:
					entry.append(numpy.uint32(precalcs[dict["LIST"][s]["JUMP_TO_LABEL"]]))
				entry.append(dict["LIST"][s]["STRING"].encode("shift_jis_2004") + b"\x00")
		case "SELECT":
			entry.append(numpy.uint8(0x32))
			entry.append(bytes.fromhex("8080"))
			entry.append(numpy.uint16(len(dict["LIST"])))
			entry.append(numpy.uint16(dict["UNK0"]))
			for s in range(0, len(dict["LIST"])):
				entry.append(numpy.uint8(dict["LIST"][s]["ID"]))
				entry.append(bytes.fromhex(dict["LIST"][s]["DATA"]))
				if ((precalcs == None) or (dict["LIST"][s]["JUMP_TO_LABEL"] == "0x0")):
					entry.append(numpy.uint32(0))
				else:
					entry.append(numpy.uint32(precalcs[dict["LIST"][s]["JUMP_TO_LABEL"]]))
				entry.append(dict["LIST"][s]["STRING"].encode("shift_jis_2004") + b"\x00")
		case "33":
			entry.append(numpy.uint8(0x33))
		case "34":
			entry.append(numpy.uint8(0x34))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "36":
			entry.append(numpy.uint8(0x36))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "39":
			entry.append(numpy.uint8(0x39))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "3A":
			entry.append(numpy.uint8(0x3A))
			entry.append(numpy.uint32(0))
		case "3B":
			entry.append(numpy.uint8(0x3B))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "3C":
			entry.append(numpy.uint8(0x3C))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "42":
			entry.append(numpy.uint8(0x42))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "43":
			entry.append(numpy.uint8(0x43))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "VOICE":
			entry.append(numpy.uint8(0x44))
			entry.append(numpy.uint16(0xA))
			entry.append(numpy.uint16(dict["VOICE_ID"]))
			if (dict["TYPE"] == "WITH_TEXT"):
				entry.append(bytes.fromhex("5945FFFF"))
				entry.append(numpy.uint16(Utils.text_counter))
				Utils.text_counter += 1
				entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
			elif (dict["TYPE"] == "WITHOUT_TEXT"):
				entry.append(bytes.fromhex("592d06000000"))
			else:
				print("UNKNOWN VOICE TYPE!")
				print(dict["TYPE"])
				sys.exit()
		case "TEXT2":
			entry.append(numpy.uint8(0x45))
			entry.append(numpy.int16(-1))
			try:
				dict["ID"]
			except:
				entry.append(numpy.uint16(Utils.text_counter))
				Utils.text_counter += 1
			else:
				entry.append(numpy.int16(dict["ID"]))
			entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
		case "TEXT":
			entry.append(numpy.uint8(0x47))
			if (dict["TYPE"] == "MESSAGE"):
				entry.append(numpy.int16(-1))
				entry.append(numpy.uint16(Utils.text_counter))
				Utils.text_counter += 1
				entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
			elif (dict["TYPE"] == "NAME"):
				entry.append(numpy.int16(13))
				entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
			else:
				print("UNKNOWN TEXT TYPE!")
				print(dict["TYPE"])
				sys.exit()
		case "48":
			entry.append(numpy.uint8(0x48))
			entry.append(numpy.int16(-1))
		case "49":
			entry.append(numpy.uint8(0x49))
			entry.append(numpy.int32(-1))
		case "KEY_WAIT":
			entry.append(numpy.uint8(0x4A))
			entry.append(numpy.int16(-1))
		case "4B":
			entry.append(numpy.uint8(0x4B))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "4C":
			entry.append(numpy.uint8(0x4C))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "4F":
			entry.append(numpy.uint8(0x4F))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "51":
			entry.append(numpy.uint8(0x51))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "5A":
			entry.append(numpy.uint8(0x5A))
		case "5F":
			entry.append(numpy.uint8(0x5F))
		case "68":
			entry.append(numpy.uint8(0x68))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "69":
			entry.append(numpy.uint8(0x69))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "6A":
			entry.append(numpy.uint8(0x6A))
			entry.append(numpy.int32(-1))
		case "6C":
			entry.append(numpy.uint8(0x6C))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "6E":
			entry.append(numpy.uint8(0x6E))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "71":
			entry.append(numpy.uint8(0x71))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "72":
			entry.append(numpy.uint8(0x72))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "74":
			entry.append(numpy.uint8(0x74))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "75":
			entry.append(numpy.uint8(0x75))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "7B":
			entry.append(numpy.uint8(0x7B))
			entry.append(bytes.fromhex("00002c01"))
		case "82":
			entry.append(numpy.uint8(0x82))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "83":
			entry.append(numpy.uint8(0x83))
			entry.append(bytes.fromhex("ff800300"))
		case "85":
			entry.append(numpy.uint8(0x85))
			entry.append(numpy.int32(-1))
			entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
		case "86":
			entry.append(numpy.uint8(0x86))
			entry.append(bytes.fromhex(dict["DATA"]))
			entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
		case _:
			print("UNKNOWN COMMAND!")
			print(dict["CMD"])
			sys.exit()

	return b"".join(entry)

os.makedirs("sn_new", exist_ok=True)

for i in range(0, 316):
	OUTPUT = []
	PrecalculateOffsets = {}
	print(i)
	try:
		file = open("jsons_new/%04d.json" % i, "r", encoding="UTF-8")
	except:
		file = open("jsons/%04d.json" % i, "r", encoding="UTF-8")
	dump = json.load(file)
	file.close()

	file_new = open("sn_new/%04d.bin" % i, "wb")
	file_new.write(numpy.uint32(len(dump["HEADER"]) * 2 + 4))

	for x in range(0, len(dump["HEADER"])):
		file_new.write(numpy.int16(dump["HEADER"][x]))
	
	offset = len(dump["HEADER"]) * 2 + 4

	for x in range(0, len(dump["COMMANDS"])):
		PrecalculateOffsets[dump["COMMANDS"][x]["LABEL"]] = offset
		offset += len(ProcessCommands(dump["COMMANDS"][x]))

	Utils.text_counter = 0
	for x in range(0, len(dump["COMMANDS"])):
		OUTPUT.append(ProcessCommands(dump["COMMANDS"][x], PrecalculateOffsets))
	
	file_new.write(b"".join(OUTPUT))
	file_new.close()

print(316)
OUTPUT = []

file = open("jsons/0316.json", "r", encoding="UTF-8")
dump = json.load(file)
file.close()

file_new = open("sn_new/0316.bin", "wb")
for i in range(0, len(dump)):
	for x in range(0, len(dump[i])):
		OUTPUT.append(numpy.int32(dump[i][x]))

file_new.write(b"".join(OUTPUT))
file_new.close()

header = []
sn_newfile = open("sn_new_dec.bin", "wb")
offset = 0x13D0

for i in range(0, 317):
	file = open("sn_new/%04d.bin" % i, "rb")
	header.append(numpy.uint32(offset))
	header.append(numpy.uint32(GetFileSize(file)))
	offset += GetFileSize(file)
	file.close()
	header.append(numpy.uint64(0))

sn_newfile.write(b"".join(header))

for i in range(0, 317):
	file = open("sn_new/%04d.bin" % i, "rb")
	sn_newfile.write(file.read())
	file.close()