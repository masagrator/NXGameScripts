import os
import json
import sys
import shutil
import lzss

Filenames = [
	"0000",
	"chapter1",
	"chapter11",
	"chapter12",
	"chapter13",
	"chapter14",
	"chapter15",
	"chapter16",
	"chapter17",
	"chapter18",
	"chapter19",
	"chapter2",
	"chapter20",
	"chapter21",
	"chapter22",
	"chapter23",
	"chapter24",
	"chapter25",
	"chapter26",
	"chapter27",
	"chapter28",
	"chapter29",
	"chapter3",
	"chapter30",
	"chapter31_1",
	"chapter31_2",
	"chapter32_1",
	"chapter32_2",
	"chapter33",
	"chapter34",
	"chapter35_1",
	"chapter35_2",
	"chapter36",
	"chapter37_1",
	"chapter37_2",
	"chapter38",
	"chapter39_1",
	"chapter39_2",
	"chapter4_1",
	"chapter4_2",
	"chapter40_1",
	"chapter40_2",
	"chapter40_3",
	"chapter40_4",
	"chapter41",
	"chapter5_1",
	"chapter5_2",
	"chapter6",
	"chapter7_1",
	"chapter7_2",
	"chapter8",
	"chapter9",
	"chapterC1",
	"chapterC2",
	"chapterC3_alpha",
	"chapterC3_R",
	"chapterC4_alpha",
	"chapterC4_R",
	"chapterL1",
	"chapterL10",
	"chapterL11",
	"chapterL12",
	"chapterL13_1",
	"chapterL13_2",
	"chapterL14",
	"chapterL15",
	"chapterL16_1",
	"chapterL17_1",
	"chapterL17_2",
	"chapterL18",
	"chapterL19",
	"chapterL2",
	"chapterL20",
	"chapterL21_1",
	"chapterL21_2",
	"chapterL22_1",
	"chapterL22_2",
	"chapterL23_1",
	"chapterL23_2",
	"chapterL3",
	"chapterL4",
	"chapterL5",
	"chapterL6",
	"chapterL7",
	"chapterL8",
	"chapterL9",
	"chapterP_hikari",
	"chapterP_hiragino",
	"chapterP_reiri",
	"chapterP_tokiwa",
	"chapterP_touri",
	"chapterP_yukari",
	"chapterR1",
	"chapterR10",
	"chapterR11",
	"chapterR12_1",
	"chapterR12_2",
	"chapterR13_1",
	"chapterR13_2",
	"chapterR2",
	"chapterR3_1",
	"chapterR3_2",
	"chapterR4",
	"chapterR5",
	"chapterR6",
	"chapterR7",
	"chapterR8",
	"chapterR9"
]

class Utils:
	text_counter = 0
	name = None
	STRINGS_COUNTS = []

linesize = 68

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
		case "IFGOTO":
			entry.append(b"\x01")
			if (precalcs == None):
				entry.append(0x0.to_bytes(4, "little"))
			else:
				entry.append(precalcs[dict["TO_LABEL"]].to_bytes(4, "little"))
		case "JMP":
			entry.append(b"\x02")
			entry.append(dict["ID"].to_bytes(4, "little"))
		case "JMP4":
			entry.append(b"\x04")
			entry.append(dict["ID"].to_bytes(4, "little"))
		case "RETURN":
			entry.append(b"\x05")
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
		case "MOV":
			entry.append(b"\x10")
			entry.append((dict["ID"]).to_bytes(2, "little"))
			entry.append((dict["VALUE"]).to_bytes(2, "little"))
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
		case "16":
			entry.append(b"\x16")
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
		case "25":
			entry.append(b"\x25")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "2D":
			entry.append(b"\x2D")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "2E":
			entry.append(b"\x2E")
		case "2F":
			entry.append(b"\x2F")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "31":
			entry.append(b"\x31")
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
		case "36":
			entry.append(b"\x36")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "FACE_NAME":
			entry.append(b"\x39")
			entry.append(bytes.fromhex(dict["DATA"]))
			entry.append(dict["ID"].to_bytes(2, "little"))
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
		case "TEXT2":
			entry.append(b"\x45")
			entry.append(dict["TYPE"].to_bytes(2, "little", signed=True))
			if (dict["TYPE"] in [-1, 10]):
				try:
					dict["ID"]
				except:
					entry.append(Utils.text_counter.to_bytes(2, "little"))
					Utils.text_counter += 1
				else:
					entry.append(dict["ID"].to_bytes(2, "little", signed=True))
			entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
		case "TEXT3":
			entry.append(b"\x46")
			entry.append(dict["TYPE"].to_bytes(2, "little", signed=True))
			if (dict["TYPE"] in [-1, 10]):
				try:
					dict["ID"]
				except:
					entry.append(Utils.text_counter.to_bytes(2, "little"))
					Utils.text_counter += 1
				else:
					entry.append(dict["ID"].to_bytes(2, "little"))
				if (dict["TYPE"] == -1): entry.append(bytes.fromhex(dict["DATA"]))
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
				Utils.name = dict["STRING"]
			elif (dict["TYPE"] == "MESSAGE2"):
				entry.append(0xA.to_bytes(2, "little"))
				entry.append(Utils.text_counter.to_bytes(2, "little"))
				Utils.text_counter += 1
				entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
			elif (dict["TYPE"] == "MESSAGE3"):
				entry.append(0x46.to_bytes(2, "little"))
				entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
			else:
				print("UNKNOWN TEXT TYPE!")
				print(dict["TYPE"])
				sys.exit()
		case "48":
			entry.append(b"\x48")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "NEW_PAGE":
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
		case "51":
			entry.append(b"\x51")
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
		case "TITLE":
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
		case "5A":
			entry.append(b"\x5A")
		case "5F":
			entry.append(b"\x5F")
		case "66":
			entry.append(b"\x66")
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
		case "6E":
			entry.append(b"\x6E")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "6F":
			entry.append(b"\x6F")
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
		case "7A":
			entry.append(b"\x7A")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "7B":
			entry.append(b"\x7B")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "82":
			entry.append(b"\x82")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "83":
			entry.append(b"\x83")
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
		case "8D":
			entry.append(b"\x8D")
		case "94":
			entry.append(b"\x94")
			entry.append(bytes.fromhex(dict["DATA"]))
			entry.append(len(dict["LIST"]).to_bytes(2, "little"))
			entry.append(bytes.fromhex(dict["DATA2"]))
			for s in range(0, len(dict["LIST"])):
				entry.append(dict["LIST"][s]["VALUE"].to_bytes(2, "little"))
				if (precalcs == None):
					entry.append(0x0.to_bytes(4, "little"))
				else:
					entry.append(precalcs[dict["LIST"][s]["TO_LABEL"]].to_bytes(4, "little"))
				entry.append(bytes.fromhex(dict["LIST"][s]["DATA"]))
		case _:
			print("UNKNOWN COMMAND!")
			print(dict["CMD"])
			sys.exit()

	return b"".join(entry)

shutil.rmtree("sn_new", ignore_errors=True)
os.makedirs("sn_new", exist_ok=True)

for i in range(len(Filenames)):
	OUTPUT = []
	PrecalculateOffsets = {}
	file = open(f"{sys.argv[1]}/%s.json" % (Filenames[i]), "r", encoding="UTF-8")
	print(file.name)
	dump = json.load(file)
	file.close()

	if ("ERROR" in dump["COMMANDS"][-1].keys()):
		print("JSON was not properly disassembled, ignoring...")
		continue

	file_new = open("sn_new/%04d.bin" % i, "wb")
	file_new.write((len(dump["HEADER"]) * 4 + 4).to_bytes(4, "little"))

	for x in range(0, len(dump["HEADER"])):
		file_new.write(dump["HEADER"][x].to_bytes(4, "little", signed=True))
	
	offset = len(dump["HEADER"]) * 4 + 4

	for x in range(0, len(dump["COMMANDS"])):
		PrecalculateOffsets[dump["COMMANDS"][x]["LABEL"]] = offset
		offset += len(ProcessCommands(dump["COMMANDS"][x]))
	
	Utils.text_counter = 0
	for x in range(0, len(dump["COMMANDS"])):
		OUTPUT.append(ProcessCommands(dump["COMMANDS"][x], PrecalculateOffsets))
	
	Utils.STRINGS_COUNTS.append(Utils.text_counter)
	OUTPUT.append(Utils.text_counter.to_bytes(4, "little"))
	OUTPUT.append(bytes.fromhex(dump["FOOTER"][8:]))
	file_new.write(b"".join(OUTPUT))
	if (file_new.tell() % 16 != 0):
		file_new.write(b"\x00" * (16 - (file_new.tell() % 16)))
	file_new.close()

print("0108")
OUTPUT = []

file = open(f"{sys.argv[1]}/0108.json", "r", encoding="UTF-8")
dump = json.load(file)
file.close()

file_new = open("sn_new/0108.bin", "wb")

for x in dump[0].keys():
	OUTPUT.append(dump[0][x].to_bytes(4, "little", signed=True))

for i in range(1, len(dump) - 2):
	OUTPUT.append(Utils.STRINGS_COUNTS[i].to_bytes(4, "little", signed=True))
	OUTPUT.append(dump[i]["VALUE2"].to_bytes(4, "little", signed=True))
	OUTPUT.append(dump[i]["VALUE3"].to_bytes(4, "little", signed=True))
	OUTPUT.append(dump[i]["ID"].to_bytes(4, "little", signed=True))

OUTPUT.append(sum(Utils.STRINGS_COUNTS).to_bytes(4, "little", signed=True))
OUTPUT.append(dump[-2]["VALUE2"].to_bytes(4, "little", signed=True))
OUTPUT.append(dump[-2]["VALUE3"].to_bytes(4, "little", signed=True))
OUTPUT.append(dump[-2]["ID"].to_bytes(4, "little", signed=True))

OUTPUT.append(dump[-1]["STRING_COUNT"].to_bytes(4, "little", signed=True))
OUTPUT.append(dump[-1]["VALUE2"].to_bytes(4, "little", signed=True))
OUTPUT.append(dump[-1]["VALUE3"].to_bytes(4, "little", signed=True))
OUTPUT.append(dump[-1]["ID"].to_bytes(4, "little", signed=True))

file_new.write(b"".join(OUTPUT))
file_new.close()

header = []

offset = 0x6D0

for i in range(0, 109):
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

data = b"".join(header)

for i in range(0, 109):
	file = open("sn_new/%04d.bin" % i, "rb")
	data += file.read()
	file.close()

dec_filesize = len(data)

dump = lzss.compress(data, 0)

os.makedirs("010071C00CBA4000/romfs", exist_ok=True)

file_new = open("010071C00CBA4000/romfs/sn.bin", "wb")
file_new.write(dec_filesize.to_bytes(4, "little"))
file_new.write(dump)
file_new.close()