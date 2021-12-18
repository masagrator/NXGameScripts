import glob
import json
import os
import numpy
import shutil
from story_commands import *

def invertBitsU8(b1):
	number = numpy.uint8(b1)
	return ~number

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
			return str(InvertString(b"".join(chars)).decode("shift_jis_2004").replace("㊤㊦", "––").replace("㊤㊥", "——"))
		chars.append(c)

def TakeID(F):
	pos = F.tell()
	F.seek(0x8)
	ID = numpy.fromfile(F, dtype=numpy.uint32, count=1)[0]
	F.seek(pos)
	return ID

def GetFileSize(F):
	pos = F.tell()
	F.seek(0, 2)
	size = F.tell()
	F.seek(pos)
	return size

def Disassemble_CMD(F, cmd, argsize):
	match(cmd):
		case 1:
			return Disassemble.DEMO(F)
		case 2:
			return Disassemble.DEMOtm(F, argsize)
		case 3:
			return Disassemble.PAGE(F, argsize)
		case 4:
			return Disassemble.PAGEtm(F, argsize)
		case 99:
			return Disassemble.EXTEND(F, argsize)
		case 101:
			return Disassemble.JUMP(F)
		case 102:
			return Disassemble.SELECT(F, argsize)
		case 103:
			return Disassemble.SELECTtm(F, argsize)
		case 104:
			return Disassemble.SI(F, argsize)
		case 105:
			return Disassemble.SItm(F, argsize)
		case 106:
			return Disassemble.IF(F, argsize)
		case 107:
			return Disassemble.IFtm(F, argsize)
		case 108:
			return Disassemble.IFPARAM(F, argsize)
		case 109:
			return Disassemble.IFPARAMtm(F, argsize)
		case 112:
			return Disassemble.IFSTRING(F, argsize)
		case 113:
			return Disassemble.IFSTRINGtm(F, argsize)
		case 114:
			return Disassemble.IFRV(F, argsize)
		case 115:
			return Disassemble.IFRVtm(F, argsize)
		case 116:
			if (select_bool == False):
				return Disassemble.SELECT_ITEM(F)
			else:
				return Disassemble.SELECT_ITEM(F, Selects)
		case 117:
			return Disassemble.SELECT_ITEMtm(F, argsize)
		case 201:
			return Disassemble.WAIT(F, argsize)
		case 202:
			return Disassemble.BWAIT(F, argsize)
		case 203:
			return Disassemble.TWAIT(F, argsize)
		case 204:
			return Disassemble.BR(F, argsize) #Break Line
		case 205:
			return Disassemble.FONT(F, argsize)
		case 206:
			return Disassemble.FONTtm(F, argsize)
		case 207:
			return Disassemble.MSPEED(F, argsize)
		case 208:
			return Disassemble.RUBY(F, argsize)
		case 209:
			return Disassemble.RUBYtm(F, argsize)
		case 210:
			return Disassemble.TEXT_LEFT(F, argsize)
		case 211:
			return Disassemble.TEXT_RIGHT(F, argsize)
		case 212:
			return Disassemble.TEXT_TOP(F, argsize)
		case 213:
			return Disassemble.EMBED(F, argsize)
		case 214:
			return Disassemble.SPACE(F, argsize)
		case 215:
			return Disassemble.CURSOR(F, argsize)
		case 216:
			return Disassemble.TEXT_FADE(F, argsize)
		case 217:
			return Disassemble.ICON(F, argsize)
		case 218:
			return Disassemble.EMBED_PARAM(F, argsize)
		case 219:
			return Disassemble.TEXT_MODE(F, argsize)
		case 255:
			return Disassemble.NML(F, argsize)
		case 301:
			return Disassemble.WINDOW_ON(F, argsize)
		case 302:
			return Disassemble.WINDOW_OFF(F, argsize)
		case 303:
			return Disassemble.WINDOW_SIZE(F, argsize)
		case 304:
			return Disassemble.WINDOW_MOVE(F, argsize)
		case 305:
			return Disassemble.WINDOW_FADE(F, argsize)
		case 306:
			return Disassemble.TXTWND_IN(F, argsize)
		case 307:
			return Disassemble.TXTWND_OUT(F, argsize)
		case 401:
			return Disassemble.BG_LOAD(F, argsize)
		case 402:
			return Disassemble.BG_WAIT(F, argsize)
		case 403:
			return Disassemble.BG_FADE(F, argsize)
		case 404:
			return Disassemble.BG_COLOR(F, argsize)
		case 405:
			return Disassemble.BG_MOVE(F, argsize)
		case 406:
			return Disassemble.BG_SIZE(F, argsize)
		case 407:
			return Disassemble.BG_ST(F, argsize)
		case 410:
			return Disassemble.BG_SET_ADJUST_Z(F, argsize)
		case 501:
			return Disassemble.TX2_LOAD(F, argsize)
		case 502:
			return Disassemble.TX2_MOVE(F, argsize)
		case 503:
			return Disassemble.TX2_FADE(F, argsize)
		case 504:
			return Disassemble.TX2_SIZE(F, argsize)
		case 505:
			return Disassemble.TX2_ST(F, argsize)
		case 506:
			return Disassemble.TX2_COLOR(F, argsize)
		case 507:
			return Disassemble.TX2_ZGP(F, argsize)
		case 508:
			return Disassemble.TX2_CENTERING(F, argsize)
		case 509:
			return Disassemble.TX2_CTL_TRACK(F, argsize)
		case 550:
			return Disassemble.TX2_TRACK(F, argsize)
		case 551:
			return Disassemble.TX2_PACK_READ(F, argsize)
		case 552:
			return Disassemble.TX2_PACK_WAIT(F, argsize)
		case 601:
			return Disassemble.ANM_LOAD(F, argsize)
		case 602:
			return Disassemble.ANM_MOVE(F, argsize)
		case 603:
			return Disassemble.ANM_FADE(F, argsize)
		case 604:
			return Disassemble.ANM_SIZE(F, argsize)
		case 605:
			return Disassemble.ANM_PLAY(F, argsize)
		case 606:
			return Disassemble.ANM_SKIP(F, argsize)
		case 607:
			return Disassemble.ANM_STOP(F, argsize)
		case 651:
			return Disassemble.ANM_PACK_READ(F, argsize)
		case 652:
			return Disassemble.ANM_PACK_WAIT(F, argsize)
		case 701:
			return Disassemble.SCR_FADE(F, argsize)
		case 702:
			return Disassemble.SCR_VIB(F, argsize)
		case 801:
			return Disassemble.FLAG(F, argsize)
		case 802:
			return Disassemble.PARAM(F, argsize)
		case 803:
			return Disassemble.STRING(F, argsize)
		case 804:
			return Disassemble.PARAM_COMPARE(F, argsize)
		case 805:
			return Disassemble.STRING_COMPARE(F, argsize)
		case 806:
			return Disassemble.PARAM_COPY(F, argsize)
		case 807:
			return Disassemble.STRING_COPY(F, argsize)
		case 901:
			return Disassemble.SET_VOL(F, argsize)
		case 902:
			return Disassemble.BGM_READY(F, argsize)
		case 903:
			return Disassemble.BGM_WAIT(F, argsize)
		case 904:
			return Disassemble.BGM_PLAY(F, argsize)
		case 905:
			return Disassemble.BGM_VOL(F, argsize)
		case 906:
			return Disassemble.BGM_STOP(F, argsize)
		case 907:
			return Disassemble.MSG_READY(F, argsize)
		case 908:
			return Disassemble.MSG_WAIT(F, argsize)
		case 909:
			return Disassemble.MSG_PLAY(F, argsize)
		case 910:
			return Disassemble.MSG_VOL(F, argsize)
		case 911:
			return Disassemble.MSG_STOP(F, argsize)
		case 914:
			return Disassemble.SE_PLAY(F, argsize)
		case 915:
			return Disassemble.SE_VOL(F, argsize)
		case 916:
			return Disassemble.SE_STOP(F, argsize)
		case 917:
			return Disassemble.SE_ALL_STOP(F, argsize)
		case 918:
			return Disassemble.LOOPS_READY(F, argsize)
		case 919:
			return Disassemble.LOOPS_WAIT(F, argsize)
		case 920:
			return Disassemble.LOOPS_PLAY(F, argsize)
		case 921:
			return Disassemble.LOOPS_VOL(F, argsize)
		case 922:
			return Disassemble.LOOPS_STOP(F, argsize)
		case 923:
			return Disassemble.SONG_READY(F, argsize)
		case 924:
			return Disassemble.SONG_WAIT(F, argsize)
		case 925:
			return Disassemble.SONG_PLAY(F, argsize)
		case 926:
			return Disassemble.SONG_VOL(F, argsize)
		case 927:
			return Disassemble.SONG_STOP(F, argsize)
		case 931:
			return Disassemble.MSG_SYNC(F, argsize)
		case 932:
			return Disassemble.SONG_SYNC(F, argsize)
		case 1001:
			return Disassemble.EMBED_EDIT(F, argsize)
		case 1002:
			return Disassemble.TITLE_JUMP(F, argsize)
		case 1003:
			return Disassemble.DLOGIC(F, argsize)
		case 1004:
			return Disassemble.GRADE(F, argsize)
		case 1005:
			return Disassemble.LOGIC_INFER(F, argsize)
		case 1006:
			return Disassemble.SAVE_POINT(F, argsize)
		case 1101:
			return Disassemble.PAD_CTL(F, argsize)
		case 1102:
			return Disassemble.PAD_VIB(F, argsize)
		case 1103:
			return Disassemble.PAD_PUSH(F, argsize)
		case 1201:
			return Disassemble.CODE_3D_PLAY(F, argsize)
		case 1202:
			return Disassemble.CODE_3D_MOVE(F, argsize)
		case 1203:
			return Disassemble.CODE_3D_FADE(F, argsize)
		case 1204:
			return Disassemble.CODE_3D_ROTATE(F, argsize)
		case 1205:
			return Disassemble.CODE_3D_SIZE(F, argsize)
		case 1206:
			return Disassemble.CODE_3D_STOP(F, argsize)
		case 1251:
			return Disassemble.CODE_3D_PACK_READ(F, argsize)
		case 1252:
			return Disassemble.CODE_3D_PACK_WAIT(F, argsize)
		case 1261:
			return Disassemble.CODE_3D_CAMERA_SET(F, argsize)
		case 1301:
			return Disassemble.CALL_DEMO(F, argsize)
		case 1302:
			return Disassemble.WAIT_DEMO_ALL(F, argsize)
		case 1303:
			return Disassemble.OPTWND(F, argsize)
		case 1304:
			return Disassemble.RANDOM(F, argsize)
		case 1305:
			return Disassemble.READED_PCT(F, argsize)
		case 1306:
			return Disassemble.DENY_SKIP(F, argsize)
		case 1307:
			return Disassemble.BACKLOG_CLEAR(F, argsize)
		case 1308:
			return Disassemble.HIDE_SELECTER_MENU(F, argsize)
		case 1309:
			return Disassemble.HIDE_NAMEEDIT_MENU(F, argsize)
		case 1310:
			return Disassemble.YES_NO_DLG(F, argsize)
		case 1311:
			return Disassemble.STOP_SKIP(F, argsize)
		case 1312:
			return Disassemble.TXTHIDE_CTL(F, argsize)
		case 1313:
			return Disassemble.STOP_OTHER_DEMO(F, argsize)
		case 1314:
			return Disassemble.SUBMENU_CTL(F, argsize)
		case 1315:
			return Disassemble.SHORTCUT_CTL(F, argsize)
		case 1316:
			return Disassemble.NOVELCLEAR(F, argsize)
		case 1317:
			return Disassemble.PLAY_VIDEO(F, argsize) # Guessed
		case 1401:
			return Disassemble.PHRASE_SET(F, argsize)
		case 1402:
			return Disassemble.PHRASE_FADE(F, argsize)
		case 1403:
			return Disassemble.PHRASE_MOVE(F, argsize)
		case 1501:
			return Disassemble.NUMBER_SET(F, argsize)
		case 1502:
			return Disassemble.NUMBER_FADE(F, argsize)
		case 1503:
			return Disassemble.NUMBER_MOVE(F, argsize)
		case 1504:
			return Disassemble.NUMBER_SIZE(F, argsize)
		case 1505:
			return Disassemble.NUMBER_GET_PARAM(F, argsize)
		case 2001:
			if (keyword_bool == False):
				return Disassemble.KEYWORD(F)
			else:
				return Disassemble.KEYWORD(F, Keywords)
		case 2002:
			return Disassemble.GRADE_POINT(F, argsize)
		case 2003:
			return Disassemble.ADD_MEMO(F, argsize)
		case 2004:
			return Disassemble.LOGIC_MODE(F, argsize)
		case 2005:
			return Disassemble.LOGIC_SET_KEY(F, argsize)
		case 2006:
			return Disassemble.LOGIC_GET_KEY(F, argsize)
		case 2007:
			return Disassemble.LOGIC_CTL(F, argsize)
		case 2008:
			return Disassemble.LOGIC_LOAD(F, argsize)
		case 2009:
			return Disassemble.GAME_END(F, argsize)
		case 2010:
			return Disassemble.FACE(F, argsize)
		case 2011:
			return Disassemble.CHOOSE_KEYWORD(F, argsize)
		case 2012:
			return Disassemble.LOGIC_CLEAR_KEY(F, argsize)
		case 2013:
			return Disassemble.DATABASE(F, argsize)
		case 2014:
			if (character_bool == False):
				return Disassemble.SPEAKER(F)
			else:
				return Disassemble.SPEAKER(F, Characters)
		case 2021:
			return Disassemble.LOGIC_SAVE(F, argsize)
		case 2022:
			return Disassemble.LOGIC_DRAW_MARK(F, argsize)
		case 2101:
			return Disassemble.DLPAGE(F, argsize)
		case 2102:
			return Disassemble.DLPAGEtm(F, argsize)
		case 2103:
			return Disassemble.DLKEY(F, argsize)
		case 2104:
			return Disassemble.DLSELSET(F, argsize)
		case 2105:
			return Disassemble.DLSELSETtm(F, argsize)
		case 2106:
			return Disassemble.DLSEL(F, argsize)
		case 2107:
			return Disassemble.DLSELECT(F, argsize)
		case 2108:
			return Disassemble.ILCAMERA(F, argsize)
		case 2109:
			return Disassemble.ILZOOM(F, argsize)
		case 2201:
			return Disassemble.CI_LOAD(F, argsize)
		case 2202:
			return Disassemble.CI_LOAD_WAIT(F, argsize)
		case 2203:
			return Disassemble.CI_MOVE(F, argsize)
		case 2204:
			return Disassemble.CI_FADE(F, argsize)
		case 2205:
			return Disassemble.CI_SIZE(F, argsize)
		case 2206:
			return Disassemble.CI_ST(F, argsize)
		case 2207:
			return Disassemble.CI_COLOR(F, argsize)
		case 2208:
			return Disassemble.CI_ZGP(F, argsize)
		case 2209:
			return Disassemble.CI_CENTERING(F, argsize)
		case 2210:
			return Disassemble.CI_CTL_TRACK(F, argsize)
		case 2211:
			return Disassemble.CI_TRACK(F, argsize)
		case 2212:
			return Disassemble.CI_NEGAPOSI(F, argsize)
		case 2213:
			return Disassemble.CI_BUSTUP_CENTERING(F, argsize)
		case 2301:
			return Disassemble.MCR_TEXT_TOP(F, argsize)
		case 2302:
			return Disassemble.MCR_RUBY(F, argsize)
		case 2303:
			return Disassemble.MCR_BG_START(F, argsize)
		case 2304:
			return Disassemble.MCR_BG_STOP(F, argsize)
		case 2305:
			return Disassemble.MCR_BU_START(F, argsize)
		case 2306:
			return Disassemble.MCR_BU_STOP(F, argsize)
		case 2307:
			return Disassemble.MCR_CI_START(F, argsize)
		case 2308:
			return Disassemble.MCR_CI_STOP(F, argsize)
		case 2309:
			return Disassemble.MCR_TEXTWIN_IN(F, argsize)
		case 2310:
			return Disassemble.MCR_TEXTWIN_OUT(F, argsize)
		case 2311:
			return Disassemble.MCR_3D_EFFECT(F, argsize)
		case 2312:
			return Disassemble.MCR_BGM_START(F, argsize)
		case 2313:
			return Disassemble.MCR_BGM_STOP(F, argsize)
		case 2314:
			return Disassemble.MCR_SE_START(F, argsize)
		case 2315:
			return Disassemble.MCR_LOOPVOICE_START(F, argsize)
		case 2316:
			return Disassemble.MCR_LOOPVOICE_STOP(F, argsize)
		case 2401:
			return Disassemble.ANIME_LOAD(F, argsize)
		case 2402:
			return Disassemble.ANIME_LOAD_WAIT(F, argsize)
		case 2403:
			return Disassemble.ANIME_PLAY(F, argsize)
		case 2404:
			return Disassemble.ANIME_SKIP(F, argsize)
		case 2405:
			return Disassemble.ANIME_STOP(F, argsize)
		case 2406:
			return Disassemble.ANIME_MOVE(F, argsize)
		case 2407:
			return Disassemble.ANIME_FADE(F, argsize)
		case 2408:
			return Disassemble.ANIME_SCALE(F, argsize)
		case 2409:
			return Disassemble.ANIME_ROT(F, argsize)
		case 2410:
			return Disassemble.ANIME_ZGP(F, argsize)
		case 2411:
			return Disassemble.ANIME_SYNC(F, argsize)
		case 2412:
			return Disassemble.ANIME_PAUSE(F, argsize)
		case 2413:
			return Disassemble.ANIME_RESUME(F, argsize)
		case 2414:
			return Disassemble.ANIME_FRAME(F, argsize)
		case 2501:
			return Disassemble.LIARSART_START(F, argsize)
		case 2502:
			return Disassemble.LIARSART_DEMOEND(F, argsize)
		case 2503:
			return Disassemble.LIARSART_END(F, argsize)
		case 2504:
			return Disassemble.LIARSART_TUTORIAL(F, argsize)
		case 2505:
			return Disassemble.UNK_2505(F, argsize)
		case _:
			print("Unknown command! %d" % cmd)
			return None

def processAssembly(file, size):
	Dump = []
	while (file.tell() < size):
		entry = {}
		if (file.read(0x1) == b"\xFF"):
			command_size = numpy.fromfile(file, dtype=numpy.uint8, count=1)[0] - 4
			command_ID = numpy.fromfile(file, dtype=numpy.uint16, count=1)[0]
			Result = Disassemble_CMD(file, command_ID, command_size)
			if (Result == None):
				entry["ARGS"] = file.read(command_size).hex()
				entry["CMD_ID"] = int(command_ID)
				Dump.append(entry)
			else:
				Dump.append(Result)
			while (file.tell() % 4 != 0):
				file.seek(1, 1)
			
		else:
			file.seek(-1, 1)
			entry["STRING"] = readString(file)
			Dump.append(entry)
	return Dump

def reformatDump(Dict):
	Dump = []
	i = 0
	addName = 0
	addSurname = 0
	while (i < len(Dict)):
		try:
			Dict[i]["TYPE"]
		except:
			entry = {}
			entry["STRINGS"] = []
			flag = False
			while(flag == False):
				string = Dict[i]["STRING"]
				if (addName != 0 or addSurname != 0): # Add name and surname to strings
					if (addName == 2):
						string = "北條紗希" + string
					elif (addName == 1):
						string = "紗希" + string
					elif (addSurname == 1):
						string = "北條" + string
					addName = 0
					addSurname = 0
				try: # Check if we didn't split strings to separate entries because of name injection
					Dump[len(Dump) - 1]["STRINGS"]
				except:
					entry["STRINGS"].append(string)
				else:
					count = len(Dump[len(Dump) - 1]["STRINGS"])
					Dump[len(Dump) - 1]["STRINGS"][count - 1] = Dump[len(Dump) - 1]["STRINGS"][count - 1] + string
					flag = True
					continue
				if (Dict[i+1]["TYPE"] != "BR"): flag = True # Check if we don't need to break line
				else:
					if (Dict[i+1]["UNK0"][8:] != "0000"): 
						flag = True
						continue
					try:
						Dict[i+2]["STRING"]
					except:
						flag = True
					else:
						i += 2
			if (len(entry["STRINGS"]) > 0): # If STRINGS entry is empty, ignore entry
				Dump.append(entry)
		else:
			match(Dict[i]["TYPE"]):
				case "EMBED_EDIT": # This removes Change Name popup at the beginning of game
					None
				case "EMBED": # Removes embedding user's character name in favour of original name
					if (Dict[i]["UNK0"][4:] == "0a000100"):
						if (addSurname == 1):
							addName = 2
						else:
							addName = 1
					elif (Dict[i]["UNK0"][4:] == "0a000000"):
							addSurname = 1
					else:
						Dump.append(Dict[i])
				case _:
					Dump.append(Dict[i])
		i += 1
	return Dump

def reformatDump2(Dict):
	Dump = []
	i = 0
	flag = False
	while (i < len(Dict)):
		try:
			Dict[i]["TYPE"]
		except:
			if (flag == False):
				Dump.append(Dict[i])
			else:
				try:
					Dump[len(Dump) - 1]["STRINGS"]
				except:
					Dump.append(Dict[i])
				else:
					Dump[len(Dump) - 1]["STRINGS"] += Dict[i]["STRINGS"]
				flag = False
		else:
			if (Dict[i]["TYPE"] != "BR"):
				Dump.append(Dict[i])
			else:
				if (Dict[i]["UNK0"][8:] != "0000"):
					Dump.append(Dict[i])
				else:
					try:
						Dict[i+1]["STRINGS"]
					except:
						Dump.append(Dict[i])
					else:
						flag = True
		i += 1
	return Dump


file = open("database\\story.dat", "rb")

buffer = numpy.fromfile(file, dtype=numpy.uint32, count=2)
header_size = buffer[0]
table_entries = buffer[1]

offsets = []
IDs = []
for i in range(0, table_entries):
	buffer = numpy.fromfile(file, dtype=numpy.uint32, count=2)
	offsets.append(buffer[1])
	IDs.append(buffer[0])

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

character_bool = True
try:
	chars_file = open("strings/characterdatabase.json", "r", encoding="UTF-8")
except:
	print("characterdatabase not detected. Names won't be passed to output.")
	character_bool = False
else:
	Characters = json.load(chars_file)
	chars_file.close()

keyword_bool = True
try:
	keywords_file = open("strings/keyword.json", "r", encoding="UTF-8")
except:
	print("keyword not detected. Keywords won't be passed to output.")
	keyword_bool = False
else:
	Keywords = json.load(keywords_file)
	keywords_file.close()

select_bool = True
try:
	selects_file = open("strings/selectinfo.json", "r", encoding="UTF-8")
except:
	print("Selectinfo not detected. Selects won't be passed to output.")
	select_bool = False
else:
	Selects = json.load(selects_file)
	selects_file.close()

os.makedirs("json", exist_ok=True)
for i in range(0, len(files)):
	file = open(files[i], "rb")
	ID = TakeID(file)
	print(ID)
	size = GetFileSize(file)
	file_new = open("json\%s.json" % ID, "w", encoding="UTF-8")
	Dump = processAssembly(file, size)
	file.close()
	Dump = reformatDump(Dump)
	Dump = reformatDump2(Dump)
	json.dump(Dump, file_new, indent="\t", ensure_ascii=False)
	file_new.close()

shutil.rmtree('extracted')