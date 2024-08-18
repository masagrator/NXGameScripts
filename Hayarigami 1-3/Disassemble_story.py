import glob
import json
import os
import shutil

def SortNumber(elem):
	return elem

def invertBitsU8(b1):
	return (255-b1).to_bytes(1, "little", signed=False)

def InvertString(bytes):
	chars = []
	for i in range(0, len(bytes)):
		chars.append(invertBitsU8(bytes[i]))
	return b"".join(chars)

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if ((c == b'\x00') or (c == b'\xFF')):
			myfile.seek(-1, 1)
			while (myfile.tell() % 4 != 0):
				myfile.seek(1, 1)
			return str(InvertString(b"".join(chars)).decode("shift_jis_2004"))
		chars.append(c)

def TakeID(F):
	pos = F.tell()
	F.seek(0x4)
	ID = int.from_bytes(F.read(4), "little")
	F.seek(pos)
	return ID

def GetFileSize(F):
	pos = F.tell()
	F.seek(0, 2)
	size = F.tell()
	F.seek(pos)
	return size

def Disassemble_CMD(F, cmd, argsize):
	start_offset = F.tell()
	entry = {}
	match(cmd):
		case 1:
			entry["TYPE"] = "DEMO"
			entry["FILE_ID"] = int.from_bytes(F.read(4), "little")
			entry["UNK0"] = F.read(4).hex()
		case 2:
			entry["TYPE"] = "DEMOtm"
		case 3:
			entry["TYPE"] = "PAGE"
			entry["POS_X"] = int.from_bytes(F.read(2), "little")
			entry["POS_Y"] = int.from_bytes(F.read(2), "little")
			entry["PAGE_NUMBER"] = int.from_bytes(F.read(2), "little")
			return entry
		case 4:
			entry["TYPE"] = "PAGEtm"
		case 101:
			entry["TYPE"] = "JUMP"
			entry["FILE_ID"] = int.from_bytes(F.read(4), "little")
		case 102:
			entry["TYPE"] = "SELECT"
		case 103:
			entry["TYPE"] = "SELECTtm"
		case 104:
			entry["TYPE"] = "SI"
			entry["UNK0"] = F.read(argsize).hex()
		case 105:
			entry["TYPE"] = "SItm"
		case 106:
			entry["TYPE"] = "IF"
			entry["ARG1"] = int.from_bytes(F.read(2), "little")
			entry["ARG2"] = int.from_bytes(F.read(2), "little")
		case 107:
			entry["TYPE"] = "IFtm"
		case 108:
			entry["TYPE"] = "IFPARAM"
			entry["ARG"] = F.read(argsize).hex()
		case 109:
			entry["TYPE"] = "IFPARAMtm"
		case 114:
			entry["TYPE"] = "IFRV"
			entry["UNK0"] = F.read(argsize).hex()
		case 115:
			entry["TYPE"] = "IFRVtm"
		case 201:
			entry["TYPE"] = "WAIT"
			entry["ARG"] = int.from_bytes(F.read(2), "little")
		case 202:
			entry["TYPE"] = "BWAIT"
			entry["ARG"] = int.from_bytes(F.read(4), "little")
		case 203:
			entry["TYPE"] = "TWAIT"
		case 204:
			entry["TYPE"] = "BR"
			entry["ARGS"] = [int.from_bytes(F.read(1), "little"), int.from_bytes(F.read(1), "little")]
			if (entry["ARGS"] == [0, 0]): entry["ARGS"] = "BREAK_LINE"
			elif (entry["ARGS"] == [1, 0]): entry["ARGS"] = "PRESS_TO_BREAK_LINE"
			elif (entry["ARGS"] == [1, 3]): entry["ARGS"] = "PRESS_TO_END_MESSAGE"
		case 205:
			entry["TYPE"] = "FONT"
			entry["UNK0"] = F.read(argsize).hex()
		case 206:
			entry["TYPE"] = "FONTtm"
		case 207:
			entry["TYPE"] = "MSPEED"
			entry["ARG"] = int.from_bytes(F.read(2), "little")
		case 208:
			entry["TYPE"] = "RUBY"
			F.seek(1, 1) # string size
			entry["STRING"] = readString(F)
			entry["ENG"] = ""
			F.seek(start_offset + argsize)
		case 209:
			entry["TYPE"] = "RUBYtm"
		case 212:
			entry["TYPE"] = "TEXT_TOP"
			entry["ARG"] = int.from_bytes(F.read(2), "little")
		case 213:
			entry["TYPE"] = "EMBED"
			entry["ARG"] = int.from_bytes(F.read(2), "little")
		case 214:
			entry["TYPE"] = "SPACE"
			entry["ARG"] = int.from_bytes(F.read(2), "little")
		case 217:
			entry["TYPE"] = "ICON"
			entry["ARG"] = int.from_bytes(F.read(2), "little")
		case 503:
			entry["TYPE"] = "TX2_FADE"
			entry["UNK0"] = F.read(argsize).hex()
		case 701:
			entry["TYPE"] = "SCR_FADE"
			entry["UNK0"] = F.read(argsize).hex()
		case 801:
			entry["TYPE"] = "FLAG"
			entry["ARG1"] = int.from_bytes(F.read(2), "little")
			if (entry["ARG1"] == 1):
				entry["ARG2"] = int.from_bytes(F.read(2), "little")
			else: entry["ARG2"] = F.read(argsize-2).hex()
		case 802:
			entry["TYPE"] = "PARAM"
			entry["UNK0"] = F.read(argsize).hex()
		case 803:
			entry["TYPE"] = "STRING"
			entry["ID"] = int.from_bytes(F.read(1), "little")
			entry["STRING"] = readString(F)
			entry["ENG"] = ""
			F.seek(start_offset + argsize)
		case 903:
			entry["TYPE"] = "BGM_WAIT"
		case 906:
			entry["TYPE"] = "BGM_STOP"
		case 917:
			entry["TYPE"] = "SE_ALL_STOP"
		case 1001:
			entry["TYPE"] = "EMBED_EDIT"
			entry["ID1"] = int.from_bytes(F.read(2), "little")
			entry["UNK0"] = F.read(5).hex()
			entry["ID2"] = int.from_bytes(F.read(1), "little")
			entry["STRING"] = readString(F)
			entry["ENG"] = ""
			F.seek(start_offset + argsize)
		case 1301:
			entry["TYPE"] = "CALL_DEMO"
			entry["UNK0"] = F.read(argsize).hex()
		case 1302:
			entry["TYPE"] = "WAIT_DEMO_ALL"
		case 1303:
			entry["TYPE"] = "OPTWND"
			entry["ARG"] = int.from_bytes(F.read(2), "little")
		case 1307:
			entry["TYPE"] = "BACKLOG_CLEAR"
		case 1308:
			entry["TYPE"] = "HIDE_SELECTER_MENU"
			entry["ARG"] = int.from_bytes(F.read(2), "little")
		case 1309:
			entry["TYPE"] = "HIDE_NAMEEDIT_MENU"
			entry["ARG"] = int.from_bytes(F.read(2), "little")
		case 1311:
			entry["TYPE"] = "STOP_SKIP"
		case 1401:
			entry["TYPE"] = "PHRASE_SET"
			entry["ID"] = int.from_bytes(F.read(4), "little")
			entry["STRING"] = readString(F)
			entry["ENG"] = ""
			F.seek(start_offset + argsize)
		case 1402:
			entry["TYPE"] = "PHRASE_FADE"
			entry["UNK0"] = F.read(argsize-2).hex()
			entry["PHRASE_ID"] = int.from_bytes(F.read(2), "little")
		case 1403:
			entry["TYPE"] = "PHRASE_MOVE"
			entry["UNK0"] = F.read(argsize-2).hex()
			entry["PHRASE_ID"] = int.from_bytes(F.read(2), "little")
		case 2012:
			entry["TYPE"] = "LOGIC_CLEAR_KEY"
		case 2101:
			entry["TYPE"] = "DLPAGE"
		case 2102:
			entry["TYPE"] = "DLPAGEtm"
		case 2104:
			entry["TYPE"] = "DLSELSET"
		case 2105:
			entry["TYPE"] = "DLSELSETtm"
		case 2107:
			entry["TYPE"] = "DLSELECT"
		case _:
			entry["TYPE"] = "%d" % cmd
			if (argsize > 0):
				entry["UNK0"] = F.read(argsize).hex()
	return entry

def processAssembly(file, size):
	Dump = []
	file.seek(0x0)
	page = False
	while (file.tell() < size):
		if (page == False):
			entry = {}
		if (file.read(0x1) == b"\xFF"):
			command_size = int.from_bytes(file.read(1), "little") - 4
			command_ID = int.from_bytes(file.read(2), "little")
			Result = Disassemble_CMD(file, command_ID, command_size)
			if (Result == None):
				entry["ARGS"] = file.read(command_size).hex()
				entry["CMD_ID"] = int(command_ID)
				Result = entry
			elif (Result["TYPE"] == "PAGE"):
				entry = {}
				entry["TYPE"] = "PAGE"
				entry["POS_X"] = Result["POS_X"]
				entry["POS_Y"] = Result["POS_Y"]
				entry["PAGE_NUMBER"] = Result["PAGE_NUMBER"]
				entry["COMMANDS"] = []
				page = True
			elif (Result["TYPE"] == "PAGEtm"):
				Result = entry
				page = False
			if (page == False):
				Dump.append(Result)
			elif (Result["TYPE"] != "PAGE"):
				entry["COMMANDS"].append(Result)
			while (file.tell() % 4 != 0):
				file.seek(1, 1)
		else:
			file.seek(-1, 1)
			entry2 = {}
			entry2["TYPE"] = "MESSAGE"
			if (file.read(2) == b"\x00\x00"):
				if (file.tell() % 4 != 0):
					file.seek(4 - (file.tell() % 4), 1)
			else: file.seek(-2, 1)
			entry2["STRING"] = readString(file)
			if (entry2["STRING"] != ""):
				entry2["ENG"] = ""
			else: 
				entry2.pop("STRING")
				entry2["TYPE"] = "MESSAGE_EMPTY"
			if (file.tell() % 4 != 0):
				file.seek(4 - (file.tell() % 4), 1)
			if (page == False):
				Dump.append(entry2)
			else: entry["COMMANDS"].append(entry2)
	return Dump

file = open("story1.dat", "rb")

header_size = int.from_bytes(file.read(4), "little")
table_entries = int.from_bytes(file.read(4), "little")

offsets = []
IDs = []
for i in range(0, table_entries):
	IDs.append(int.from_bytes(file.read(4), "little"))
	offsets.append(int.from_bytes(file.read(4), "little"))

os.makedirs("extracted", exist_ok=True)

for i in range(0, table_entries):
	new_file = open("extracted\%s.dat" % IDs[i], "wb")
	file.seek(offsets[i])
	if (i != table_entries - 1):
		new_file.write(file.read(offsets[i+1]-offsets[i]))
	else:
		new_file.write(file.read())
	new_file.close()

file.close()

files = glob.glob("extracted/*.dat")

os.makedirs("json", exist_ok=True)
for i in range(0, len(files)):
	file = open(files[i], "rb")
	ID = TakeID(file)
	print(ID)
	size = GetFileSize(file)
	file_new = open("json\%s.json" % ID, "w", encoding="UTF-8")
	Dump = processAssembly(file, size)
	file.close()
	json.dump(Dump, file_new, indent="\t", ensure_ascii=False)
	file_new.close()

shutil.rmtree('extracted')