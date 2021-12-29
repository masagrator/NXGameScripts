import json
import glob
import os
import sys
import numpy
from story_commands import *

character_limit = 57

BR_DICT = {
	"TYPE": "BR",
	"UNK0": "00000a000000"
}

def ReplaceChara(string):
	fromthis = ["«", "»", "––", "——", "…", "é", "ï", "~", ":"]
	tothis = ["≪", "≫", "㊤㊦", "㊤㊥", "...", "e", "i", "〜", "："]
	for i in range(0, len(fromthis)):
		string = string.replace(fromthis[i], tothis[i])
	return string

def invertBitsU8(b1):
	number = numpy.uint8(b1)
	return ~number

def InvertString(bytes):
	chars = []
	for i in range(0, len(bytes)):
		chars.append(invertBitsU8(bytes[i]))
	while (len(b"".join(chars)) % 4 != 0):
		chars.append(b"\x00")
	return b"".join(chars)

def generateCommand(Dict, entry_number):
	try:
		Dict["TYPE"]
	except:
		entry = []
		for i in range(0, len(Dict["STRINGS"])):
			if (i > 0):
				generateCommand.characters_in_line = 0
			if (len(Dict["STRINGS"][i]) > character_limit):
				print("Detected line overflow. Entry number: %d, line: %d. Got: %d, Max allowed: %d" % (entry_number, i+1, generateCommand.characters_in_line, character_limit))
				print("Entry dump:")
				print(Dict["STRINGS"])
				print("Adding break line is not possible.")
				print("Aborting...")
				sys.exit()
			generateCommand.characters_in_line += len(Dict["STRINGS"][i])
			if (generateCommand.characters_in_line > character_limit):
				print("Detected line overflow. Entry number: %d, line: %d. Got: %d, Max allowed: %d" % (entry_number, i+1, generateCommand.characters_in_line, character_limit))
				print("Entry dump:")
				print(Dict["STRINGS"])
				input("If you want to add automatically break line, press ENTER. If not, close window.")
				entry.append(Assemble.BR(BR_DICT))
				generateCommand.characters_in_line = 0
			if (len(Dict["STRINGS"][i]) > 0):
				text_bytes = ReplaceChara(Dict["STRINGS"][i]).encode("shift_jis_2004")
				entry.append(InvertString(text_bytes))
			if (i < (len(Dict["STRINGS"]) - 1)):
				entry.append(Assemble.BR(BR_DICT))
		return b"".join(entry)
	match(Dict["TYPE"]):
		case "DEMO":
			return Assemble.DEMO(Dict)
		case "DEMOtm":
			return Assemble.DEMOtm(Dict)
		case "PAGE":
			return Assemble.PAGE(Dict)
		case "PAGEtm":
			return Assemble.PAGEtm(Dict)
		case "EXTEND":
			return Assemble.EXTEND(Dict)
		case "JUMP":
			return Assemble.JUMP(Dict)
		case "SELECT":
			return Assemble.SELECT(Dict)
		case "SELECTtm":
			generateCommand.characters_in_line = 0
			return Assemble.SELECTtm(Dict)
		case "SI":
			return Assemble.SI(Dict)
		case "SItm":
			return Assemble.SItm(Dict)
		case "IF":
			return Assemble.IF(Dict)
		case "IFtm":
			return Assemble.IFtm(Dict)
		case "IFPARAM":
			return Assemble.IFPARAM(Dict)
		case "IFPARAMtm":
			return Assemble.IFPARAMtm(Dict)
		case "IFSTRING":
			return Assemble.IFSTRING(Dict)
		case "IFSTRINGtm":
			return Assemble.IFSTRINGtm(Dict)
		case "IFRV":
			return Assemble.IFRV(Dict)
		case "IFRVtm":
			return Assemble.IFRVtm(Dict)
		case "SELECT_ITEM":
			return Assemble.SELECT_ITEM(Dict)
		case "SELECT_ITEMtm":
			generateCommand.characters_in_line = 0
			return Assemble.SELECT_ITEMtm(Dict)
		case "WAIT":
			return Assemble.WAIT(Dict)
		case "BWAIT":
			return Assemble.BWAIT(Dict)
		case "TWAIT":
			return Assemble.TWAIT(Dict)
		case "BR":
			generateCommand.characters_in_line = 0
			return Assemble.BR(Dict) #Break Line
		case "FONT":
			return Assemble.FONT(Dict)
		case "FONTtm":
			return Assemble.FONTtm(Dict)
		case "MSPEED":
			return Assemble.MSPEED(Dict)
		case "RUBY":
			return Assemble.RUBY(Dict)
		case "RUBYtm":
			return Assemble.RUBYtm(Dict)
		case "TEXT_LEFT":
			return Assemble.TEXT_LEFT(Dict)
		case "TEXT_RIGHT":
			return Assemble.TEXT_RIGHT(Dict)
		case "TEXT_TOP":
			return Assemble.TEXT_TOP(Dict)
		case "EMBED":
			return Assemble.EMBED(Dict)
		case "SPACE":
			return Assemble.SPACE(Dict)
		case "CURSOR":
			return Assemble.CURSOR(Dict)
		case "TEXT_FADE":
			return Assemble.TEXT_FADE(Dict)
		case "ICON":
			return Assemble.ICON(Dict)
		case "EMBED_PARAM":
			return Assemble.EMBED_PARAM(Dict)
		case "TEXT_MODE":
			return Assemble.TEXT_MODE(Dict)
		case "NML":
			return Assemble.NML(Dict)
		case "WINDOW_ON":
			return Assemble.WINDOW_ON(Dict)
		case "WINDOW_OFF":
			return Assemble.WINDOW_OFF(Dict)
		case "WINDOW_SIZE":
			return Assemble.WINDOW_SIZE(Dict)
		case "WINDOW_MOVE":
			return Assemble.WINDOW_MOVE(Dict)
		case "WINDOW_FADE":
			return Assemble.WINDOW_FADE(Dict)
		case "TXTWND_IN":
			return Assemble.TXTWND_IN(Dict)
		case "TXTWND_OUT":
			return Assemble.TXTWND_OUT(Dict)
		case "BG_LOAD":
			return Assemble.BG_LOAD(Dict)
		case "BG_WAIT":
			return Assemble.BG_WAIT(Dict)
		case "BG_FADE":
			return Assemble.BG_FADE(Dict)
		case "BG_COLOR":
			return Assemble.BG_COLOR(Dict)
		case "BG_MOVE":
			return Assemble.BG_MOVE(Dict)
		case "BG_SIZE":
			return Assemble.BG_SIZE(Dict)
		case "BG_ST":
			return Assemble.BG_ST(Dict)
		case "BG_SET_ADJUST_Z":
			return Assemble.BG_SET_ADJUST_Z(Dict)
		case "TX2_LOAD":
			return Assemble.TX2_LOAD(Dict)
		case "TX2_MOVE":
			return Assemble.TX2_MOVE(Dict)
		case "TX2_FADE":
			return Assemble.TX2_FADE(Dict)
		case "TX2_SIZE":
			return Assemble.TX2_SIZE(Dict)
		case "TX2_ST":
			return Assemble.TX2_ST(Dict)
		case "TX2_COLOR":
			return Assemble.TX2_COLOR(Dict)
		case "TX2_ZGP":
			return Assemble.TX2_ZGP(Dict)
		case "TX2_CENTERING":
			return Assemble.TX2_CENTERING(Dict)
		case "TX2_CTL_TRACK":
			return Assemble.TX2_CTL_TRACK(Dict)
		case "TX2_TRACK":
			return Assemble.TX2_TRACK(Dict)
		case "TX2_PACK_READ":
			return Assemble.TX2_PACK_READ(Dict)
		case "TX2_PACK_WAIT":
			return Assemble.TX2_PACK_WAIT(Dict)
		case "ANM_LOAD":
			return Assemble.ANM_LOAD(Dict)
		case "ANM_MOVE":
			return Assemble.ANM_MOVE(Dict)
		case "ANM_FADE":
			return Assemble.ANM_FADE(Dict)
		case "ANM_SIZE":
			return Assemble.ANM_SIZE(Dict)
		case "ANM_PLAY":
			return Assemble.ANM_PLAY(Dict)
		case "ANM_SKIP":
			return Assemble.ANM_SKIP(Dict)
		case "ANM_STOP":
			return Assemble.ANM_STOP(Dict)
		case "ANM_PACK_READ":
			return Assemble.ANM_PACK_READ(Dict)
		case "ANM_PACK_WAIT":
			return Assemble.ANM_PACK_WAIT(Dict)
		case "SCR_FADE":
			return Assemble.SCR_FADE(Dict)
		case "SCR_VIB":
			return Assemble.SCR_VIB(Dict)
		case "FLAG":
			return Assemble.FLAG(Dict)
		case "PARAM":
			return Assemble.PARAM(Dict)
		case "STRING":
			return Assemble.STRING(Dict)
		case "PARAM_COMPARE":
			return Assemble.PARAM_COMPARE(Dict)
		case "STRING_COMPARE":
			return Assemble.STRING_COMPARE(Dict)
		case "PARAM_COPY":
			return Assemble.PARAM_COPY(Dict)
		case "STRING_COPY":
			return Assemble.STRING_COPY(Dict)
		case "SET_VOL":
			return Assemble.SET_VOL(Dict)
		case "BGM_READY":
			return Assemble.BGM_READY(Dict)
		case "BGM_WAIT":
			return Assemble.BGM_WAIT(Dict)
		case "BGM_PLAY":
			return Assemble.BGM_PLAY(Dict)
		case "BGM_VOL":
			return Assemble.BGM_VOL(Dict)
		case "BGM_STOP":
			return Assemble.BGM_STOP(Dict)
		case "MSG_READY":
			return Assemble.MSG_READY(Dict)
		case "MSG_WAIT":
			return Assemble.MSG_WAIT(Dict)
		case "MSG_PLAY":
			return Assemble.MSG_PLAY(Dict)
		case "MSG_VOL":
			return Assemble.MSG_VOL(Dict)
		case "MSG_STOP":
			return Assemble.MSG_STOP(Dict)
		case "SE_PLAY":
			return Assemble.SE_PLAY(Dict)
		case "SE_VOL":
			return Assemble.SE_VOL(Dict)
		case "SE_STOP":
			return Assemble.SE_STOP(Dict)
		case "SE_ALL_STOP":
			return Assemble.SE_ALL_STOP(Dict)
		case "LOOPS_READY":
			return Assemble.LOOPS_READY(Dict)
		case "LOOPS_WAIT":
			return Assemble.LOOPS_WAIT(Dict)
		case "LOOPS_PLAY":
			return Assemble.LOOPS_PLAY(Dict)
		case "LOOPS_VOL":
			return Assemble.LOOPS_VOL(Dict)
		case "LOOPS_STOP":
			return Assemble.LOOPS_STOP(Dict)
		case "SONG_READY":
			return Assemble.SONG_READY(Dict)
		case "SONG_WAIT":
			return Assemble.SONG_WAIT(Dict)
		case "SONG_PLAT":
			return Assemble.SONG_PLAY(Dict)
		case "SONG_VOL":
			return Assemble.SONG_VOL(Dict)
		case "SONG_STOP":
			return Assemble.SONG_STOP(Dict)
		case "MSG_SYNC":
			return Assemble.MSG_SYNC(Dict)
		case "SONG_SYNC":
			return Assemble.SONG_SYNC(Dict)
		case "EMBED_EDIT":
			return Assemble.EMBED_EDIT(Dict)
		case "TITLE_JUMP":
			return Assemble.TITLE_JUMP(Dict)
		case "DLOGIC":
			return Assemble.DLOGIC(Dict)
		case "GRADE":
			return Assemble.GRADE(Dict)
		case "LOGIC_INFER":
			return Assemble.LOGIC_INFER(Dict)
		case "SAVE_POINT":
			return Assemble.SAVE_POINT(Dict)
		case "PAD_CTL":
			return Assemble.PAD_CTL(Dict)
		case "PAD_VIB":
			return Assemble.PAD_VIB(Dict)
		case "PAD_PUSH":
			return Assemble.PAD_PUSH(Dict)
		case "3D_PLAY":
			return Assemble.CODE_3D_PLAY(Dict)
		case "3D_MOVE":
			return Assemble.CODE_3D_MOVE(Dict)
		case "3D_FADE":
			return Assemble.CODE_3D_FADE(Dict)
		case "3D_ROTATE":
			return Assemble.CODE_3D_ROTATE(Dict)
		case "3D_SIZE":
			return Assemble.CODE_3D_SIZE(Dict)
		case "3D_STOP":
			return Assemble.CODE_3D_STOP(Dict)
		case "3D_PACK_READ":
			return Assemble.CODE_3D_PACK_READ(Dict)
		case "3D_PACK_WAIT":
			return Assemble.CODE_3D_PACK_WAIT(Dict)
		case "3D_CAMERA_SET":
			return Assemble.CODE_3D_CAMERA_SET(Dict)
		case "CALL_DEMO":
			return Assemble.CALL_DEMO(Dict)
		case "WAIT_DEMO_ALL":
			return Assemble.WAIT_DEMO_ALL(Dict)
		case "OPTWND":
			return Assemble.OPTWND(Dict)
		case "RANDOM":
			return Assemble.RANDOM(Dict)
		case "READED_PCT":
			return Assemble.READED_PCT(Dict)
		case "DENY_SKIP":
			return Assemble.DENY_SKIP(Dict)
		case "BACKLOG_CLEAR":
			return Assemble.BACKLOG_CLEAR(Dict)
		case "HIDE_SELECTER_MENU":
			return Assemble.HIDE_SELECTER_MENU(Dict)
		case "HIDE_NAMEEDIT_MENU":
			return Assemble.HIDE_NAMEEDIT_MENU(Dict)
		case "YES_NO_DLG":
			return Assemble.YES_NO_DLG(Dict)
		case "STOP_SKIP":
			return Assemble.STOP_SKIP(Dict)
		case "TXTHIDE_CTL":
			return Assemble.TXTHIDE_CTL(Dict)
		case "STOP_OTHER_DEMO":
			return Assemble.STOP_OTHER_DEMO(Dict)
		case "SUBMENU_CTL":
			return Assemble.SUBMENU_CTL(Dict)
		case "SHORTCUT_CTL":
			return Assemble.SHORTCUT_CTL(Dict)
		case "NOVELCLEAR":
			return Assemble.NOVELCLEAR(Dict)
		case "PLAY_VIDEO":
			return Assemble.PLAY_VIDEO(Dict) # Guessed
		case "PHRASE_SET":
			return Assemble.PHRASE_SET(Dict)
		case "PHRASE_FADE":
			return Assemble.PHRASE_FADE(Dict)
		case "PHRASE_MOVE":
			return Assemble.PHRASE_MOVE(Dict)
		case "NUMBER_SET":
			return Assemble.NUMBER_SET(Dict)
		case "NUMBER_FADE":
			return Assemble.NUMBER_FADE(Dict)
		case "NUMBER_MOVE":
			return Assemble.NUMBER_MOVE(Dict)
		case "NUMBER_SIZE":
			return Assemble.NUMBER_SIZE(Dict)
		case "NUMBER_GET_PARAM":
			return Assemble.NUMBER_GET_PARAM(Dict)
		case "KEYWORD":
			return Assemble.KEYWORD(Dict)
		case "GRADE_POINT":
			return Assemble.GRADE_POINT(Dict)
		case "ADD_MEMO":
			return Assemble.ADD_MEMO(Dict)
		case "LOGIC_MODE":
			return Assemble.LOGIC_MODE(Dict)
		case "LOGIC_SET_KEY":
			return Assemble.LOGIC_SET_KEY(Dict)
		case "LOGIC_GET_KEY":
			return Assemble.LOGIC_GET_KEY(Dict)
		case "LOGIC_CTL":
			return Assemble.LOGIC_CTL(Dict)
		case "LOGIC_LOAD":
			return Assemble.LOGIC_LOAD(Dict)
		case "GAME_END":
			return Assemble.GAME_END(Dict)
		case "FACE":
			return Assemble.FACE(Dict)
		case "CHOOSE_KEYWORD":
			return Assemble.CHOOSE_KEYWORD(Dict)
		case "LOGIC_CLEAR_KEY":
			return Assemble.LOGIC_CLEAR_KEY(Dict)
		case "DATABASE":
			return Assemble.DATABASE(Dict)
		case "SPEAKER":
			return Assemble.SPEAKER(Dict)
		case "LOGIC_SAVE":
			return Assemble.LOGIC_SAVE(Dict)
		case "LOGIC_DRAW_MARK":
			return Assemble.LOGIC_DRAW_MARK(Dict)
		case "DLPAGE":
			return Assemble.DLPAGE(Dict)
		case "DLPAGEtm":
			return Assemble.DLPAGEtm(Dict)
		case "DLKEY":
			return Assemble.DLKEY(Dict)
		case "DLSELSET":
			return Assemble.DLSELSET(Dict)
		case "DLSELSETtm":
			return Assemble.DLSELSETtm(Dict)
		case "DLSEL":
			return Assemble.DLSEL(Dict)
		case "DLSELECT":
			return Assemble.DLSELECT(Dict)
		case "ILCAMERA":
			return Assemble.ILCAMERA(Dict)
		case "ILZOOM":
			return Assemble.ILZOOM(Dict)
		case "CI_LOAD":
			return Assemble.CI_LOAD(Dict)
		case "CI_LOAD_WAIT":
			return Assemble.CI_LOAD_WAIT(Dict)
		case "CI_MOVE":
			return Assemble.CI_MOVE(Dict)
		case "CI_FADE":
			return Assemble.CI_FADE(Dict)
		case "CI_SIZE":
			return Assemble.CI_SIZE(Dict)
		case "CI_ST":
			return Assemble.CI_ST(Dict)
		case "CI_COLOR":
			return Assemble.CI_COLOR(Dict)
		case "CI_ZGP":
			return Assemble.CI_ZGP(Dict)
		case "CI_CENTERING":
			return Assemble.CI_CENTERING(Dict)
		case "CI_CTL_TRACK":
			return Assemble.CI_CTL_TRACK(Dict)
		case "CI_TRACK":
			return Assemble.CI_TRACK(Dict)
		case "CI_NEGAPOSI":
			return Assemble.CI_NEGAPOSI(Dict)
		case "CI_BUSTUP_CENTERING":
			return Assemble.CI_BUSTUP_CENTERING(Dict)
		case "MCR_TEXT_TOP":
			return Assemble.MCR_TEXT_TOP(Dict)
		case "MCR_RUBY":
			return Assemble.MCR_RUBY(Dict)
		case "MCR_BG_START":
			return Assemble.MCR_BG_START(Dict)
		case "MCR_BG_STOP":
			return Assemble.MCR_BG_STOP(Dict)
		case "MCR_BU_START":
			return Assemble.MCR_BU_START(Dict)
		case "MCR_BU_STOP":
			return Assemble.MCR_BU_STOP(Dict)
		case "MCR_CI_START":
			return Assemble.MCR_CI_START(Dict)
		case "MCR_CI_STOP":
			return Assemble.MCR_CI_STOP(Dict)
		case "MCR_TEXTWIN_IN":
			return Assemble.MCR_TEXTWIN_IN(Dict)
		case "MCR_TEXTWIN_OUT":
			return Assemble.MCR_TEXTWIN_OUT(Dict)
		case "MCR_3D_EFFECT":
			return Assemble.MCR_3D_EFFECT(Dict)
		case "MCR_BGM_START":
			return Assemble.MCR_BGM_START(Dict)
		case "MCR_BGM_STOP":
			return Assemble.MCR_BGM_STOP(Dict)
		case "MCR_SE_START":
			return Assemble.MCR_SE_START(Dict)
		case "MCR_LOOPVOICE_START":
			return Assemble.MCR_LOOPVOICE_START(Dict)
		case "MCR_LOOPVOICE_STOP":
			return Assemble.MCR_LOOPVOICE_STOP(Dict)
		case "ANIME_LOAD":
			return Assemble.ANIME_LOAD(Dict)
		case "ANIME_LOAD_WAIT":
			return Assemble.ANIME_LOAD_WAIT(Dict)
		case "ANIME_PLAY":
			return Assemble.ANIME_PLAY(Dict)
		case "ANIME_SKIP":
			return Assemble.ANIME_SKIP(Dict)
		case "ANIME_STOP":
			return Assemble.ANIME_STOP(Dict)
		case "ANIME_MOVE":
			return Assemble.ANIME_MOVE(Dict)
		case "ANIME_FADE":
			return Assemble.ANIME_FADE(Dict)
		case "ANIME_SCALE":
			return Assemble.ANIME_SCALE(Dict)
		case "ANIME_ROT":
			return Assemble.ANIME_ROT(Dict)
		case "ANIME_ZGP":
			return Assemble.ANIME_ZGP(Dict)
		case "ANIME_SYNC":
			return Assemble.ANIME_SYNC(Dict)
		case "ANIME_PAUSE":
			return Assemble.ANIME_PAUSE(Dict)
		case "ANIME_RESUME":
			return Assemble.ANIME_RESUME(Dict)
		case "ANIME_FRAME":
			return Assemble.ANIME_FRAME(Dict)
		case "LIARSART_START":
			return Assemble.LIARSART_START(Dict)
		case "LIARSART_DEMOEND":
			return Assemble.LIARSART_DEMOEND(Dict)
		case "LIARSART_END":
			return Assemble.LIARSART_END(Dict)
		case "LIARSART_TUTORIAL":
			return Assemble.LIARSART_TUTORIAL(Dict)
		case "UNK_2505":
			return Assemble.UNK_2505(Dict)
		case _:
			print("Unknown command! %s" % Dict["TYPE"])
			sys.exit()

generateCommand.characters_in_line = 0
generateCommand.row_count = 0

def sortByNumber(elem):
	return int(os.path.basename(elem)[:-5], base=10)

os.makedirs("new_database", exist_ok=True)
new_file = open("new_database\story.dat", "wb")

orderfile = open("order.txt", "r")
order = orderfile.readlines()
order = [line.rstrip() for line in order]
orderfile.close()

header_size = numpy.uint32(0x8 + (0x8 * len(order)))
new_file.write(header_size)
new_file.write(numpy.uint32(len(order)))
scripts_block = []

for i in range(0, len(order)):
	json_file = open("json\\%s.json" % order[i], "r", encoding="UTF-8")
	print(json_file.name)
	DUMP = json.load(json_file)
	json_file.close()
	new_file.write(numpy.uint32(DUMP[0]["SCRIPT_ID"]))
	new_file.write(numpy.uint32(header_size + len(b"".join(scripts_block))))
	size = 0
	for x in range(0, len(DUMP)):
		data = generateCommand(DUMP[x], x)
#        size += len(data)
		scripts_block.append(data)
#    size_check_file = open("extracted\\%s.dat" % order[i], "rb")
#    size_check_file.seek(0, 2)
#    size_check = size_check_file.tell()
#    size_check_file.close()
#    if (size_check != size):
#        print("Size check failed! Expected: %d B, got: %d B" % (size_check, size))
#        sys.exit()

new_file.write(b"".join(scripts_block))
new_file.close()
