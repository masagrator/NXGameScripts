import os
import json
import sys
import shutil
import lzss

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

class Utils:
	text_counter = 0
	name = None
	EOF = []
	EEOF = []
	EEOF_temp = []
	jump_counter = 0
	choices_counter = 0
	message_line_size = 0

linesize = 62
linesize2 = 9999

def GetFileSize(file):
	pos = file.tell()
	file.seek(0, 2)
	size = file.tell()
	file.seek(pos)
	return size
	
def ProcessMessage(entry, dict):
	entry.append(dict["MESSAGE_TYPE_ID"].to_bytes(2, "little", signed=True))
	new_string = ""
	if (dict["MESSAGE_TYPE_ID"] in [-1, 10]):
		try:
			dict["ID"]
		except:
			entry.append(Utils.text_counter.to_bytes(2, "little"))
			Utils.text_counter += 1
		else:
			entry.append(dict["ID"].to_bytes(2, "little", signed=True))
		"""
		if (dict["STRING"].count("%N") == 0) and ((len(dict["STRING"].encode("shift_jis_2004")) + Utils.message_line_size) > (linesize if dict["MESSAGE_TYPE_ID"] != 10 else linesize2)):
			string = dict["STRING"].split(" ")
			if (len(string) > 1):
				begin = 0
				for i in range(len(string) + 1):
					temp_string = " ".join(string[begin:i])
					if ((len(temp_string.encode("shift_jis_2004")) + Utils.message_line_size) > (linesize if dict["MESSAGE_TYPE_ID"] != 10 else linesize2)):
						new_string += " ".join(string[begin:i-1]) + " %N"
						begin = i - 1
						Utils.message_line_size = 0
				new_string += " ".join(string[begin:])
				Utils.message_line_size += len(" ".join(string[begin:]).encode("shift_jis_2004"))
		elif (dict["STRING"].count("%N") == 0): Utils.message_line_size += len(dict["STRING"].encode("shift_jis_2004"))
		"""
	if (new_string != ""):
		if (dict["MESSAGE_TYPE_ID"] != 10 and new_string.count("%N") > 2):
			print("Text has too many lines! %d lines!" % (new_string.count("%N") + 1))
			print("LINE: ")
			print(new_string)
			input("Press ENTER to continue")
		entry.append(new_string.encode("shift_jis_2004") + b"\x00")
	else: entry.append(dict["STRING"].encode("shift_jis_2004") + b"\x00")
	return entry

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
		case "GOTO":
			entry.append(b"\x0D")
			entry.append(dict["ID"].to_bytes(2, "little"))
			if (precalcs == None):
				entry.append(0x0.to_bytes(4, "little"))
			else:
				entry.append(precalcs[dict["TO_LABEL"]].to_bytes(4, "little"))
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
		case "12":
			entry.append(b"\x12")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "16":
			entry.append(b"\x16")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "ATTACH_BG":
			entry.append(b"\x1A")
			entry.append((dict["ID"]).to_bytes(2, "little"))
			entry.append((dict["BGID"]).to_bytes(2, "little"))			
		case "1B":
			entry.append(b"\x1B")
		case "1C":
			entry.append(b"\x1C")
		case "1D":
			entry.append(b"\x1D")
			entry.append((dict["ID"]).to_bytes(2, "little"))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "1E":
			entry.append(b"\x1E")
			entry.append((dict["ID"]).to_bytes(2, "little"))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "1F":
			entry.append(b"\x1F")
			entry.append((dict["ID"]).to_bytes(2, "little"))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "21":
			entry.append(b"\x21")
			entry.append((dict["ID"]).to_bytes(2, "little"))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "22":
			entry.append(b"\x22")
			entry.append((dict["ID"]).to_bytes(2, "little"))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "25":
			entry.append(b"\x25")
			entry.append((dict["ID"]).to_bytes(2, "little"))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "2D":
			entry.append(b"\x2D")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "2E":
			entry.append(b"\x2E")
		case "SELECT2":
			entry.append(b"\x31\x80\x80")
			count = len(dict["LIST"]) + (dict["COUNT_TYPE"] * 100)
			entry.append(count.to_bytes(2, "little"))
			entry.append(0x0.to_bytes(2, "little"))
			for s in range(0, len(dict["LIST"])):
				entry.append(dict["LIST"][s]["UNK0"].to_bytes(2, "little"))
				entry.append(dict["LIST"][s]["ID"].to_bytes(2, "little"))
				entry.append(dict["LIST"][s]["UNK1"].to_bytes(2, "little"))
				if ((precalcs == None) or (dict["LIST"][s]["JUMP_TO_LABEL"] == "0x0")):
					entry.append(0x0.to_bytes(4, "little"))
				else:
					entry.append(precalcs[dict["LIST"][s]["JUMP_TO_LABEL"]].to_bytes(4, "little"))
					Utils.choices_counter += 1
				entry.append(dict["LIST"][s]["STRING"].encode("shift_jis_2004") + b"\x00")
		case "SELECT":
			entry.append(b"\x32\x80\x80")
			entry.append(len(dict["LIST"]).to_bytes(2, "little"))
			entry.append(dict["UNK0"].to_bytes(2, "little"))
			for s in range(0, len(dict["LIST"])):
				entry.append(dict["LIST"][s]["UNK0"].to_bytes(2, "little"))
				entry.append(dict["LIST"][s]["ID"].to_bytes(2, "little"))
				entry.append(dict["LIST"][s]["UNK1"].to_bytes(2, "little"))
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
		case "37":
			entry.append(b"\x37")
		case "39":
			entry.append(b"\x39")
			entry.append(bytes.fromhex(dict["DATA"]))
			entry.append(dict["ID"].to_bytes(2, "little"))
		case "3B":
			entry.append(b"\x3B")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "WAIT":
			entry.append(b"\x3C")
			entry.append(dict["VALUE"].to_bytes(2, "little"))
		case "43":
			entry.append(b"\x43")
			entry.append((dict["ID"]).to_bytes(2, "little"))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "VOICE":
			entry.append(b"\x44")
			entry.append(dict["MESSAGE_TYPE_ID"].to_bytes(2, "little", signed=True))
			entry.append(dict["VOICE_ID"].to_bytes(2, "little"))
		case "TEXT2":
			entry.append(b"\x45")
			entry = ProcessMessage(entry, dict)
		case "TEXT":
			entry.append(b"\x47")
			entry = ProcessMessage(entry, dict)
		case "NEW_PAGE":
			entry.append(b"\x49")
			entry.append(b"\xFF\xFF\xFF\xFF")
			Utils.message_line_size = 0
		case "KEY_WAIT":
			entry.append(b"\x4A")
			entry.append(dict["MESSAGE_TYPE_ID"].to_bytes(2, "little", signed=True))
		case "4B":
			entry.append(b"\x4B")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "TEXT_BOX_TEXTURE_POS":
			entry.append(b"\x4C")
			entry.append(dict["MESSAGE_TYPE_ID"].to_bytes(2, "little", signed=True))
			entry.append(dict["POS_X"].to_bytes(2, "little", signed=True))
			entry.append(dict["POS_Y"].to_bytes(2, "little", signed=True))
		case "4E":
			entry.append(b"\x4E")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "4F":
			entry.append(b"\x4F")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "51":
			entry.append(b"\x51")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "59":
			entry.append(b"\x59")
		case "5A":
			entry.append(b"\x5A")
		case "TEXT_BOX":
			entry.append(b"\x68")
			entry.append(dict["MESSAGE_TYPE_ID"].to_bytes(2, "little"))
			entry.append(dict["TEXT_POS_X"].to_bytes(2, "little"))
			entry.append(dict["TEXT_POS_Y"].to_bytes(2, "little"))
			entry.append(dict["SIZE_X"].to_bytes(2, "little"))
			entry.append(dict["SIZE_Y"].to_bytes(2, "little"))
		case "69":
			entry.append(b"\x69")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "6A":
			entry.append(b"\x6A")
			entry.append(b"\xFF\xFF\xFF\xFF")
		case "6B":
			entry.append(b"\x6B")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "6C":
			entry.append(b"\x6C")
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
			entry.append((dict["ID"]).to_bytes(2, "little"))
			entry.append(bytes.fromhex(dict["DATA"]))
		case "74":
			entry.append(b"\x74")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "75":
			entry.append(b"\x75")
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
			entry = ProcessMessage(entry, dict)
		case "8D":
			entry.append(b"\x8D")
		case "92":
			entry.append(b"\x92")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "93":
			entry.append(b"\x93")
			entry.append(bytes.fromhex(dict["DATA"]))
		case "9D":
			entry.append(b"\x9D")
			entry.append((dict["ID"]).to_bytes(2, "little"))
			entry.append(bytes.fromhex(dict["DATA"]))
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
	
	offset = len(dump["HEADER"]) * 4 + 4

	for x in range(0, len(dump["COMMANDS"])):
		PrecalculateOffsets[dump["COMMANDS"][x]["LABEL"]] = offset
		offset += len(ProcessCommands(dump["COMMANDS"][x]))
	
	Utils.text_counter = 0
	for x in range(0, len(dump["COMMANDS"])):
		OUTPUT.append(ProcessCommands(dump["COMMANDS"][x], PrecalculateOffsets))

	for x in range(0, len(dump["HEADER"])):
		file_new.write(PrecalculateOffsets[dump["HEADER"][x]].to_bytes(4, "little", signed=True))
	
	footer = []
	footer.append(Utils.text_counter.to_bytes(4, "little"))
	footer.append(Utils.choices_counter.to_bytes(4, "little"))
	footer.append(Utils.jump_counter.to_bytes(4, "little"))
	footer.append(dump["FOOTER"]["ID"].to_bytes(4, "little", signed=True))
	OUTPUT.append(b"".join(footer))
	Utils.EOF.append(footer)
	file_new.write(b"".join(OUTPUT))
	if (file_new.tell() % 16 != 0):
		file_new.write(b"\x00" * (16 - (file_new.tell() % 16)))
	file_new.close()
	if (Utils.EEOF_temp == []):
		Utils.EEOF_temp.append(len(dump["HEADER"]) * 4 + 4)
	Utils.EEOF.append(Utils.EEOF_temp)
	Utils.EEOF_temp = []
	Utils.text_counter = 0
	Utils.choices_counter = 0
	Utils.jump_counter = 0

OUTPUT = []

file_new = open("sn_new/%04d.bin" % (len(Filenames)), "wb")

sums = [0, 0, 0, 0]
for i in range(len(Filenames)):
	file_new.write(Utils.EOF[i][0])
	sums[0] += int.from_bytes(Utils.EOF[i][0], "little")
	file_new.write(Utils.EOF[i][1])
	sums[1] += int.from_bytes(Utils.EOF[i][1], "little")
	file_new.write(Utils.EOF[i][2])
	sums[2] += int.from_bytes(Utils.EOF[i][2], "little")
	file_new.write(Utils.EOF[i][3])
	sums[3] += int.from_bytes(Utils.EOF[i][3], "little", signed=True)

print(sums)
file_new.write(sums[0].to_bytes(4, "little"))
file_new.write(sums[1].to_bytes(4, "little"))
file_new.write(sums[2].to_bytes(4, "little"))
file_new.write(sums[3].to_bytes(4, "little"))
file_new.write(b"\xFF\xFF\xFF\xFF")

file_new.write(0x0.to_bytes(12, "little"))
file_new.close()

header = []

offset = (len(Filenames) + 1) * 0x10

for i in range(len(Filenames) + 1):
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

for i in range(len(Filenames) + 1):
	file = open("sn_new/%04d.bin" % i, "rb")
	data += file.read()
	file.close()

dec_filesize = len(data)

dump = lzss.compress(data, 0)

titleid = 0x01004B30171B8000
os.makedirs("%016X/romfs" % titleid, exist_ok=True)

file_new = open("%016X/romfs/sn.bin" % titleid, "wb")
file_new.write(dec_filesize.to_bytes(4, "little"))
file_new.write(dump)
file_new.close()