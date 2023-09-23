import os
import json
import sys
import shutil

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
			entry.append(b"\x00")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "IFGOTO":
			entry.append(b"\x01")
			if (precalcs == None):
				entry.append(0x0.to_bytes(4, "little"))
			else:
				entry.append(precalcs[dict["TO_LABEL"]].to_bytes(4, "little"))
		case "JMP4":
			entry.append(b"\x04")
			entry.append(dict["ID"].to_bytes(4, "little"))
		case "RETURN":
			entry.append(b"\x05")
			try:
				dict["DATA"]
			except:
				pass
			else:
				entry.append(bytes.fromhex(dict["DATA"]))
		case "IFGOTO6":
			entry.append(b"\x06")
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(0x0.to_bytes(4, "little"))
			else:
				entry.append(precalcs[dict["TO_LABEL"]].to_bytes(4, "little"))
		case "IFGOTO7":
			entry.append(b"\x07")
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(0x0.to_bytes(4, "little"))
			else:
				entry.append(precalcs[dict["TO_LABEL"]].to_bytes(4, "little"))
		case "IFGOTO8":
			entry.append(b"\x08")
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(0x0.to_bytes(4, "little"))
			else:
				entry.append(precalcs[dict["TO_LABEL"]].to_bytes(4, "little"))
		case "IFGOTO9":
			entry.append(b"\x09")
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(0x0.to_bytes(4, "little"))
			else:
				entry.append(precalcs[dict["TO_LABEL"]].to_bytes(4, "little"))
		case "IFGOTOA":
			entry.append(b"\x0A")
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(0x0.to_bytes(4, "little"))
			else:
				entry.append(precalcs[dict["TO_LABEL"]].to_bytes(4, "little"))
		case "IFGOTOB":
			entry.append(b"\x0B")
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(0x0.to_bytes(4, "little"))
			else:
				entry.append(precalcs[dict["TO_LABEL"]].to_bytes(4, "little"))
		case "IFGOTOC":
			entry.append(b"\x0C")
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(0x0.to_bytes(4, "little"))
			else:
				entry.append(precalcs[dict["TO_LABEL"]].to_bytes(4, "little"))
		case "GOTO":
			entry.append(b"\x0D")
			entry.append(bytes.fromhex(dict["DATA"]))
			if (precalcs == None):
				entry.append(0x0.to_bytes(4, "little"))
			else:
				entry.append(precalcs[dict["TO_LABEL"]].to_bytes(4, "little"))
			try:
				dict["DATA2"]
			except:
				pass
			else:
				entry.append(b"\x00")
		case "IFGOTOE":
			entry.append(b"\x0E")
			entry.append(bytes.fromhex(dict["DATA"]))
			entry.append(len(dict["LIST"]).to_bytes(2, "little"))
			for s in range(0, len(dict["LIST"])):
				entry.append(dict["LIST"][s]["VALUE"].to_bytes(2, "little"))
				if (precalcs == None):
					entry.append(0x0.to_bytes(4, "little"))
				else:
					entry.append(precalcs[dict["LIST"][s]["TO_LABEL"]].to_bytes(4, "little"))
		case "CMP":
			entry.append(b"\x10")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "11":
			entry.append(b"\x11")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "12":
			entry.append(b"\x12")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "13":
			entry.append(b"\x13")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "14":
			entry.append(b"\x14")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "15":
			entry.append(b"\x15")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "16":
			entry.append(b"\x16")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "18":
			entry.append(b"\x18")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "1A":
			entry.append(b"\x1A")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "1B":
			entry.append(b"\x1B")
		case "1C":
			entry.append(b"\x1C")
		case "1D":
			entry.append(b"\x1D")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "1E":
			entry.append(b"\x1E")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "1F":
			entry.append(b"\x1F")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "20":
			entry.append(b"\x20")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "21":
			entry.append(b"\x21")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "22":
			entry.append(b"\x22")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "23":
			entry.append(b"\x23")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "25":
			entry.append(b"\x25")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "2C":
			entry.append(b"\x2C")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "2D":
			entry.append(b"\x2D")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "2E":
			entry.append(b"\x2E")
		case "2F":
			entry.append(b"\x2F")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "30":
			entry.append(b"\x30")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "SELECT":
			entry.append(b"\x32")
			entry.append(bytes.fromhex(dict["DATA"]))
			entry.append(len(dict["LIST"]).to_bytes(2, "little"))
			entry.append(dict["UNK0"].to_bytes(2, "little"))
			for s in range(0, len(dict["LIST"])):
				entry.append(dict["LIST"][s]["ID"].to_bytes(1, "little"))
				entry.append(bytes.fromhex(dict["LIST"][s]["DATA"]))
				if ((precalcs == None) or (dict["LIST"][s]["JUMP_TO_LABEL"] == "0x0")):
					entry.append(0x0.to_bytes(4, "little"))
				else:
					entry.append(precalcs[dict["LIST"][s]["JUMP_TO_LABEL"]].to_bytes(4, "little"))
				entry.append(dict["LIST"][s]["STRING"].encode("shift_jis_2004") + b"\x00")
		case "34":
			entry.append(b"\x34")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "35":
			entry.append(b"\x35")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "36":
			entry.append(b"\x36")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "38":
			entry.append(b"\x38")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "39":
			entry.append(b"\x39")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "3A":
			entry.append(b"\x3A")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "3B":
			entry.append(b"\x3B")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "3C":
			entry.append(b"\x3C")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "42":
			entry.append(b"\x42")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "43":
			entry.append(b"\x43")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "VOICE":
			entry.append(b"\x44")
			entry.append(0xA.to_bytes(2, "little"))
			entry.append(dict["VOICE_ID"].to_bytes(2, "little"))
		case "TEXT2":
			entry.append(b"\x45")
			entry.append(b"\xFF\xFF")
			try:
				dict["ID"]
			except:
				entry.append(Utils.text_counter.to_bytes(2, "little"))
				Utils.text_counter += 1
			else:
				entry.append(dict["ID"].to_bytes(2, "little"))
			entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
		case "TEXT3":
			entry.append(b"\x46")
			entry.append(b"\xFF\xFF")
			try:
				dict["ID"]
			except:
				entry.append(Utils.text_counter.to_bytes(2, "little"))
				Utils.text_counter += 1
			else:
				entry.append(dict["ID"].to_bytes(2, "little"))
			entry.append(bytes.fromhex(dict["DATA"]))
			entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
		case "TEXT":
			entry.append(b"\x47")
			if (dict["TYPE"] == "MESSAGE"):
				entry.append(b"\xFF\xFF")
				entry.append(Utils.text_counter.to_bytes(2, "little"))
				Utils.text_counter += 1
				entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
			elif (dict["TYPE"] == "NAME"):
				entry.append(0xD.to_bytes(2, "little"))
				entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
			else:
				print("UNKNOWN TEXT TYPE!")
				print(dict["TYPE"])
				sys.exit()
		case "48":
			entry.append(b"\x48")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "49":
			entry.append(b"\x49")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "KEY_WAIT":
			entry.append(b"\x4A")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "4B":
			entry.append(b"\x4B")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "4C":
			entry.append(b"\x4C")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "4E":
			entry.append(b"\x4E")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "4F":
			entry.append(b"\x4F")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "55":
			entry.append(b"\x55")
			if (precalcs == None):
				offset = 0
			else:
				offset = precalcs[dict["LABEL"]] + 10
			entry.append(offset.to_bytes(4, "little"))
			entry.append(b"\x01")
			if (precalcs == None):
				entry.append(0x0.to_bytes(4, "little"))
			else:
				entry.append(precalcs[dict["NEXT"]["TO_LABEL"]].to_bytes(4, "little"))
			entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
		case "59":
			entry.append(b"\x59")
		case "5A":
			entry.append(b"\x5A")
		case "5E":
			entry.append(b"\x5E")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "5F":
			entry.append(b"\x5F")
			entry.append(dict["FLAG"].to_bytes(1, "little"))
			if (dict["FLAG"] > 0):
				match(dict["FLAG"]):
					case 1:
						if (precalcs == None):
							entry.append(0x0.to_bytes(4, "little"))
						else:
							entry.append(precalcs[dict["TO_LABEL"]].to_bytes(4, "little"))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "60":
			entry.append(b"\x60")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "62":
			entry.append(b"\x62")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "63":
			entry.append(b"\x63")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "68":
			entry.append(b"\x68")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "69":
			entry.append(b"\x69")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "6B":
			entry.append(b"\x6B")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "6C":
			entry.append(b"\x6C")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "71":
			entry.append(b"\x71")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "72":
			entry.append(b"\x72")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "74":
			entry.append(b"\x74")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "75":
			entry.append(b"\x75")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "79":
			entry.append(b"\x79")
			if (precalcs == None):
				offset = 0
			else:
				offset = precalcs[dict["LABEL"]] + 10
			entry.append(offset.to_bytes(4, "little"))
			entry.append(b"\x01")
			if (precalcs == None):
				entry.append(0x0.to_bytes(4, "little"))
			else:
				entry.append(precalcs[dict["NEXT"]["TO_LABEL"]].to_bytes(4, "little"))
			entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
		case "7A":
			entry.append(b"\x7A")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "7B":
			entry.append(b"\x7B")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "7E":
			entry.append(b"\x7E")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "7F":
			entry.append(b"\x7F")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "80":
			entry.append(b"\x80")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "81":
			entry.append(b"\x81")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "82":
			entry.append(b"\x82")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "83":
			entry.append(b"\x83")
			entry.append(bytes.fromhex(dict["DATA"]))
			entry.append(len(dict["NEW_CMDS"]).to_bytes(2, "little"))
			for i in range(len(dict["NEW_CMDS"])):
				ProcessCommands(dict["NEW_CMDS"][i], precalcs)
		case "84":
			entry.append(b"\x84")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "85":
			entry.append(b"\x85")
			entry.append(bytes.fromhex(dict["DATA"]))
			entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
		case "86":
			entry.append(b"\x86")
			entry.append(bytes.fromhex(dict["DATA"]))
			entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
		case "8C":
			entry.append(b"\x8C")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "93":
			entry.append(b"\x93")
			entry.append(bytes.fromhex(dict["DATA"]))
			entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
		case _:
			print("UNKNOWN COMMAND!")
			print(dict["CMD"])
			sys.exit()

	return b"".join(entry)

shutil.rmtree("sn_new")
os.makedirs("sn_new", exist_ok=True)

for i in range(0, 144):
	OUTPUT = []
	PrecalculateOffsets = {}
	if (34 >= i >= 3):
		file = open("jsons/KQA%02d.json" % (i - 2), "r", encoding="UTF-8")
	elif (70 >= i >= 35):
		file = open("jsons/KQB%02d.json" % (i - 34), "r", encoding="UTF-8")
	elif (97 >= i >= 71):
		file = open("jsons/KQC%02d.json" % (i - 70), "r", encoding="UTF-8")
	elif (143 >= i >= 98):
		file = open("jsons/KQD%02d.json" % (i - 97), "r", encoding="UTF-8")
	else:
		file = open("jsons/%04d.json" % i, "r", encoding="UTF-8")
	print(file.name)
	dump = json.load(file)
	file.close()

	if ("ERROR" in dump["COMMANDS"][-1].keys()):
		print("JSON was not properly disassembled, ignoring...")
		continue

	file_new = open("sn_new/%04d.bin" % i, "wb")
	file_new.write((len(dump["HEADER"]) * 2 + 4).to_bytes(4, "little"))

	for x in range(0, len(dump["HEADER"])):
		file_new.write(dump["HEADER"][x].to_bytes(2, "little", signed=True))
	
	offset = len(dump["HEADER"]) * 2 + 4

	for x in range(0, len(dump["COMMANDS"])):
		PrecalculateOffsets[dump["COMMANDS"][x]["LABEL"]] = offset
		offset += len(ProcessCommands(dump["COMMANDS"][x]))

	Utils.text_counter = 0
	for x in range(0, len(dump["COMMANDS"])):
		OUTPUT.append(ProcessCommands(dump["COMMANDS"][x], PrecalculateOffsets))
	
	file_new.write(b"".join(OUTPUT))
	file_new.close()

print("0144")
OUTPUT = []

file = open("jsons/0144.json", "r", encoding="UTF-8")
dump = json.load(file)
file.close()

file_new = open("sn_new/0144.bin", "wb")
for i in range(0, len(dump)):
	for x in range(0, len(dump[i])):
		OUTPUT.append(dump[i][x].to_bytes(4, "little", signed=True))

file_new.write(b"".join(OUTPUT))
file_new.close()

header = []
sn_newfile = open("sn_new_dec.bin", "wb")
offset = 0x910

for i in range(0, 145):
	try:
		file = open("sn_new/%04d.bin" % i, "rb")
	except:
		print("sn_new/%04d.bin was not detected" % i)
		print("Copying file from sn folder...")
		shutil.copyfile("sn/%04d.bin" % i, "sn_new/%04d.bin" % i)
		file = open("sn/%04d.bin" % i, "rb")
	header.append(offset.to_bytes(4, "little"))
	header.append(GetFileSize(file).to_bytes(4, "little"))
	offset += GetFileSize(file)
	file.close()
	header.append(b"\x00" * 8)

sn_newfile.write(b"".join(header))

for i in range(0, 145):
	file = open("sn_new/%04d.bin" % i, "rb")
	sn_newfile.write(file.read())
	file.close()