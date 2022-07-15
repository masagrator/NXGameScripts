import json
import os
import sys
import numpy
from enum import Enum
import shutil

IgnoreMessage = False
ENG = False
LABELS = {}

class Commands(Enum):
	EQU = 0x0
	EQUN = 0x1
	EQUV = 0x2
	ADD = 0x3
	SUB = 0x4
	MUL = 0x5
	DIV = 0x6
	MOD = 0x7
	AND = 0x8
	OR = 0x9
	RANDOM = 0xA
	VARSTR = 0xB
	VARSTR_ADD = 0xC
	SET = 0xD
	FLAGCLR = 0xE
	GOTO = 0xF
	ONGOTO = 0x10
	GOSUB = 0x11
	IFY = 0x12
	IFN = 0x13
	RETURN = 0x14
	JUMP = 0x15
	FARCALL = 0x16
	FARRETURN = 0x17
	JUMPPOINT = 0x18
	END = 0x19
	VARSTR_SET = 0x1A
	VARSTR_ALLOC = 0x1B
	TALKNAME_SET = 0x1C
	ARFLAGSET = 0x1D
	COLORBG_SET = 0x1E
	SPLINE_SET = 0x1F
	SHAKELIST_SET = 0x20
	SCISSOR_TRIANGLELIST_SET = 0x21
	MESSAGE = 0x22
	MESSAGE_CLEAR = 0x23
	MESSAGE_WAIT = 0x24
	SELECT = 0x25
	CLOSE_WINDOW = 0x26
	LOG = 0x27
	LOG_PAUSE = 0x28
	LOG_END = 0x29
	VOICE = 0x2A
	WAIT_COUNT = 0x2B
	WAIT_TIME = 0x2C
	WAIT_TEXTFEED = 0x2D
	FFSTOP = 0x2E
	INIT = 0x2F
	STOP = 0x30
	IMAGELOAD = 0x31
	IMAGEUPDATE = 0x32
	ARC = 0x33
	MOVE = 0x34
	MOVE2 = 0x35
	ROT = 0x36
	PEND = 0x37
	FADE = 0x38
	SCALE = 0x39
	SHAKE = 0x3A
	SHAKELIST = 0x3B
	BASE = 0x3C
	MCMOVE = 0x3D
	MCARC = 0x3E
	MCROT = 0x3F
	MCSHAKE = 0x40
	MCFADE = 0x41
	WAIT = 0x42
	DRAW = 0x43
	WIPE = 0x44
	FRAMEON = 0x45
	FRAMEOFF = 0x46
	FW = 0x47
	SCISSOR = 0x48
	DELAY = 0x49
	RASTER = 0x4A
	TONE = 0x4B
	SCALECOSSIN = 0x4C
	BMODE = 0x4D
	SIZE = 0x4E
	SPLINE = 0x4F
	DISP = 0x50
	MASK = 0x51
	FACE = 0x52
	SEPIA = 0x53
	SEPIA_COLOR = 0x54
	CUSTOMMOVE = 0x55
	SWAP = 0x56
	ADDCOLOR = 0x57
	SUBCOLOR = 0x58
	SATURATION = 0x59
	PRIORITY = 0x5A
	UVWH = 0x5B
	EVSCROLL = 0x5C
	COLORLEVEL = 0x5D
	QUAKE = 0x5E
	BGM = 0x5F
	BGM_WAITSTART = 0x60
	BGM_WAITFADE = 0x61
	BGM_PUSH = 0x62
	BGM_POP = 0x63
	SE = 0x64
	SE_STOP = 0x65
	SE_WAIT = 0x66
	SE_WAIT_COUNT = 0x67
	VOLUME = 0x68
	MOVIE = 0x69
	SETCGFLAG = 0x6A
	EX = 0x6B
	TROPHY = 0x6C
	SETBGMFLAG = 0x6D
	TASK = 0x6E
	PRINTF = 0x6F
	WAIT_FADE = 0x70
	MYSCALE = 0x71
	MYSCALE_CLEAR = 0x72
	ENROLL_WAIT = 0x73
	ENROLL_BGSTART = 0x74
	ENROLL_FRAMEENABLE = 0x75
	DATAEYECATCH = 0x76
	MAPSELECT = 0x77

def COLORLEVEL(entry):
	array = []
	array.append(Commands.COLORLEVEL.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def MCSHAKE(entry):
	array = []
	array.append(Commands.MCSHAKE.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def SCISSOR_TRIANGLELIST_SET(entry):
	array = []
	array.append(Commands.SCISSOR_TRIANGLELIST_SET.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def VARSTR_ALLOC(entry):
	array = []
	array.append(Commands.VARSTR_ALLOC.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def SUB(entry):
	array = []
	array.append(Commands.SUB.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def RANDOM(entry):
	array = []
	array.append(Commands.RANDOM.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def SWAP(entry):
	array = []
	array.append(Commands.SWAP.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def ROT(entry):
	array = []
	array.append(Commands.ROT.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def IFY(entry, string, filename):
	array = []
	array.append(Commands.IFY.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	if (entry['SUBCMD'] == 1):
		array.append(bytes.fromhex(entry['Args']))
	array.append(entry['Equation'].encode("shift_jis_2004") + b"\x00")
	if (string == "COMMAND"):
		array.append(LABELS[filename][entry['GOTO_LABEL']].to_bytes(4, byteorder='little'))
	else: array.append(int(entry['GOTO_LABEL'], 16).to_bytes(4, byteorder='little'))
	return b''.join(array)

def MESSAGE_CLEAR(entry):
	array = []
	array.append(Commands.MESSAGE_CLEAR.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def WAIT_TEXTFEED(entry):
	array = []
	array.append(Commands.WAIT_TEXTFEED.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def ADDCOLOR(entry):
	array = []
	array.append(Commands.ADDCOLOR.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def SATURATION(entry):
	array = []
	array.append(Commands.SATURATION.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def VOICE(entry):
	array = []
	array.append(Commands.VOICE.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def MASK(entry):
	array = []
	array.append(Commands.MASK.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def VOLUME(entry):
	array = []
	array.append(Commands.VOLUME.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def DISP(entry):
	array = []
	array.append(Commands.DISP.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def SCISSOR(entry):
	array = []
	array.append(Commands.SCISSOR.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def PRIORITY(entry):
	array = []
	array.append(Commands.PRIORITY.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def SETCGFLAG(entry):
	array = []
	array.append(Commands.SETCGFLAG.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def SEPIA(entry):
	array = []
	array.append(Commands.SEPIA.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def SEPIA_COLOR(entry):
	array = []
	array.append(Commands.SEPIA_COLOR.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def WIPE(entry):
	array = []
	array.append(Commands.WIPE.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def CUSTOMMOVE(entry):
	array = []
	array.append(Commands.CUSTOMMOVE.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def IMAGEUPDATE(entry):
	array = []
	array.append(Commands.IMAGEUPDATE.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def QUAKE(entry):
	array = []
	array.append(Commands.QUAKE.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def EVSCROLL(entry):
	array = []
	array.append(Commands.EVSCROLL.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def SCALE(entry):
	array = []
	array.append(Commands.SCALE.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def BMODE(entry):
	array = []
	array.append(Commands.BMODE.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def ADD(entry):
	array = []
	array.append(Commands.ADD.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def RETURN(entry):
	array = []
	array.append(Commands.RETURN.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def GOSUB(entry, string, filename):
	array = []
	array.append(Commands.GOSUB.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	if (string == "COMMAND"):
		array.append(LABELS[filename][entry['GOTO_LABEL']].to_bytes(4, byteorder='little'))
	else: array.append(int(entry['GOTO_LABEL'], 16).to_bytes(4, byteorder='little'))
	return b''.join(array)

def BGM(entry):
	array = []
	array.append(Commands.BGM.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def SE(entry):
	array = []
	array.append(Commands.SE.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def MOVIE(entry):
	array = []
	array.append(Commands.MOVIE.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	array.append(entry["Name"].encode("shift_jis_2004") + b"\x00")
	array.append(bytes.fromhex(entry['Args2']))
	return b''.join(array)

def SETBGMFLAG(entry):
	array = []
	array.append(Commands.SETBGMFLAG.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def COLORBG_SET(entry):
	array = []
	array.append(Commands.COLORBG_SET.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def FARCALL(entry, string):
	array = []
	array.append(Commands.FARCALL.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	array.append(entry["String"].encode("shift_jis_2004") + b"\x00")
	if (string == "COMMAND"):
		array.append(LABELS[entry["String"].lower()][entry['GOTO_LABEL']].to_bytes(4, byteorder='little'))
	else: array.append(int(entry['GOTO_LABEL'], 16).to_bytes(4, byteorder='little'))
	return b''.join(array)

def FLAGCLR(entry):
	array = []
	array.append(Commands.FLAGCLR.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def EQU(entry):
	array = []
	array.append(Commands.EQU.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	array.append(entry["String"].encode("shift_jis_2004") + b"\x00")
	return b''.join(array)

def EQUN(entry):
	array = []
	array.append(Commands.EQUN.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def VARSTR(entry):
	array = []
	array.append(Commands.VARSTR.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	if (ENG == False):
		array.append(entry["JPN"].encode("UTF-16-LE") + b"\x00\x00")
	elif (len(entry['ENG']) == 0):
		print("DETECTED UNTRANSLATED VARSTR!")
		print(entry)
		sys.exit()
	else:
		array.append(entry["ENG"].encode("UTF-16-LE") + b"\x00\x00")
	return b''.join(array)

def GOTO(entry, string, filename):
	array = []
	array.append(Commands.GOTO.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	if (entry['SUBCMD'] == 1):
		array.append(bytes.fromhex(entry['Args']))
		if (string == "COMMAND"):
			array.append(LABELS[filename][entry['GOTO_LABEL']].to_bytes(4, byteorder='little'))
		else: array.append(int(entry['GOTO_LABEL'], 16).to_bytes(4, byteorder='little'))
	else: 
		if (string == "COMMAND"):
			array.append(LABELS[filename][entry['GOTO_LABEL']].to_bytes(4, byteorder='little'))
		else: array.append(int(entry['GOTO_LABEL'], 16).to_bytes(4, byteorder='little'))
	return b''.join(array)

def IFN(entry, string, filename):
	array = []
	array.append(Commands.IFN.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	if (entry['SUBCMD'] == 1):
		array.append(bytes.fromhex(entry['Args']))
	array.append(entry["Equation"].encode("shift_jis_2004") + b"\x00")
	if (string == "COMMAND"):
		array.append(LABELS[filename][entry['GOTO_LABEL']].to_bytes(4, byteorder='little'))
	else: array.append(int(entry['GOTO_LABEL'], 16).to_bytes(4, byteorder='little'))
	return b''.join(array)

def JUMP(entry, string):
	array = []
	array.append(Commands.JUMP.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	if (entry['SUBCMD'] == 1):
		array.append(bytes.fromhex(entry['Args']))
	array.append(entry['Name'].encode('shift_jis_2004') + b"\x00")
	if (string == "COMMAND"):
		array.append(LABELS[entry["Name"].lower()][entry['GOTO_LABEL']].to_bytes(4, byteorder='little'))
	else: array.append(int(entry['GOTO_LABEL'], 16).to_bytes(4, byteorder='little'))
	return b''.join(array)

def JUMPPOINT(entry):
	array = []
	array.append(Commands.JUMPPOINT.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def END(entry):
	array = []
	array.append(Commands.END.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	if (entry['SUBCMD'] > 0):
		array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def TALKNAME_SET(entry):
	array = []
	array.append(Commands.TALKNAME_SET.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)


def VARSTR_SET(entry):
	array = []
	array.append(Commands.VARSTR_SET.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Metadata']))
	try:
		entry["JPN"]
	except:
		array.append(b"\x00\x00")
		return b''.join(array)
	if ((ENG == False) or (len(entry["ENG"]) == 0)):
		size = len(entry["JPN"].encode("UTF-16-LE"))
		array.append(int(size / 2).to_bytes(2, byteorder='little'))
		array.append(entry["JPN"].encode("UTF-16-LE"))
	else:
		size = len(entry["ENG"].encode("UTF-16-LE"))
		array.append(int(size / 2).to_bytes(2, byteorder='little'))
		array.append(entry["ENG"].encode("UTF-16-LE"))
	array.append(b"\x00\x00")
	return b''.join(array)

def ARFLAGSET(entry):
	array = []
	array.append(Commands.ARFLAGSET.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def SHAKELIST_SET(entry):
	array = []
	array.append(Commands.SHAKELIST_SET.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def MESSAGE(entry):
	array = []
	array.append(Commands.MESSAGE.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD2'].to_bytes(2, byteorder='little'))
	array.append(entry['MSGID'].to_bytes(2, byteorder='little'))
	try:
		array.append(entry['VOICEID'].to_bytes(2, byteorder='little'))
	except:
		array.append(b"\x00\x00")
	Name = b''
	try:
		entry['NameJPN']
	except:
		pass
	else:
		if (ENG == False or IgnoreMessage == True): Name = ("`%s@" % (entry['NameJPN'])).encode("UTF-16-LE")
		elif (len(entry['NameENG']) == 0):
			print("DETECTED UNTRANSLATED MESSAGE NAME")
			print(entry)
			sys.exit()
		else: Name = ("`%s@" % (entry['NameENG'])).encode("UTF-16-LE")
	try:
		entry["JPN"]
	except:
		array.append(bytes.fromhex(entry['Args']))
		return b''.join(array)
	else:
		if (ENG == False or IgnoreMessage == True): Text = entry["JPN"].encode("UTF-16-LE")
		elif (len(entry['ENG']) == 0):
			print("DETECTED UNTRANSLATED MESSAGE TEXT")
			print(entry)
			sys.exit()
		else: Text = entry["ENG"].encode("UTF-16-LE")
	size = (len(Name) + len(Text))
	array.append(int(size / 2).to_bytes(2, byteorder='little'))
	array.append(Name)
	array.append(Text)
	array.append(b"\x00\x00")
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def SELECT(entry):
	array = []
	array.append(Commands.SELECT.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	array.append(b"@")
	temp = 0
	string = bytearray('', 'ascii')
	for i in range(0, len(entry['JPN'])):
		if (ENG == False):
			temp += len(entry['JPN'][i].encode("UTF-16-LE"))
			string.extend(entry['JPN'][i].encode("UTF-16-LE"))
		elif (len(entry['ENG'][i]) == 0):
			print("DETECTED UNSTRANSLATED SELECT!")
			print(entry)
			sys.exit()
		else:
			temp += len(entry['ENG'][i].encode("UTF-16-LE"))
			string.extend(entry['ENG'][i].encode("UTF-16-LE"))
		if (i != (len(entry['JPN']) - 1)): 
			temp += 4
			string.extend("\x24\x64".encode("UTF-16-LE"))
	array.append(int(temp / 2).to_bytes(2, byteorder='little'))
	array.append(string)
	array.append(b"\x00\x00")
	array.append(bytes.fromhex(entry['Args2']))
	return b''.join(array)

def CLOSE_WINDOW(entry):
	array = []
	array.append(Commands.CLOSE_WINDOW.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def LOG(entry):
	array = []
	array.append(Commands.LOG.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	try:
		entry['JPN']
	except:
		return b''.join(array)
	Name = b''
	try:
		if ((ENG == False) or (len(entry['NameENG']) == 0)): Name = ("`%s@" % (entry['NameJPN'])).encode("UTF-16-LE")
		else: Name = ("`%s@" % (entry['NameENG'])).encode("UTF-16-LE")
	except:
		pass
	if ((ENG == False) or (len(entry["ENG"]) == 0)): Text = entry["JPN"].encode("UTF-16-LE")
	else: Text = entry["ENG"].encode("UTF-16-LE")
	size = (len(Name) + len(Text))
	array.append(int(size / 2).to_bytes(2, byteorder='little'))
	array.append(Name)
	array.append(Text)
	array.append(b"\x00\x00")
	array.append(bytes.fromhex(entry['Args2']))
	return b''.join(array)

def LOG_END(entry):
	array = []
	array.append(Commands.LOG_END.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def FFSTOP(entry):
	array = []
	array.append(Commands.FFSTOP.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def INIT(entry):
	array = []
	array.append(Commands.INIT.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def STOP(entry):
	array = []
	array.append(Commands.STOP.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def IMAGELOAD(entry):
	array = []
	array.append(Commands.IMAGELOAD.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def MOVE(entry):
	array = []
	array.append(Commands.MOVE.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def MOVE2(entry):
	array = []
	array.append(Commands.MOVE2.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def FADE(entry):
	array = []
	array.append(Commands.FADE.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def SHAKELIST(entry):
	array = []
	array.append(Commands.SHAKELIST.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def WAIT(entry):
	array = []
	array.append(Commands.WAIT.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def DRAW(entry):
	array = []
	array.append(Commands.DRAW.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def BGM_WAITFADE(entry):
	array = []
	array.append(Commands.BGM_WAITFADE.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def BGM_POP(entry):
	array = []
	array.append(Commands.BGM_POP.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def SE_WAIT(entry):
	array = []
	array.append(Commands.SE_WAIT.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def EX(entry):
	array = []
	array.append(Commands.EX.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def TASK(entry):
	array = []
	array.append(Commands.TASK.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	match(entry['SUBCMD']):
		case 0:
			array.append(bytes.fromhex(entry['Args']))
			if (entry['Args'] == "0800"):
				if ((ENG == True) and (len(entry["ENG"]) > 0)):
					array.append(entry["ENG"].encode("UTF-16-LE") + b"\x00\x00")
				else:
					array.append(entry["JPN"].encode("UTF-16-LE") + b"\x00\x00")
				array.append(entry["Category"].to_bytes(2, byteorder="little", signed=True))
				array.append(entry["ID"].to_bytes(2, byteorder="little", signed=True))
		case 1:
			if (entry['Args'] == "0800"):
				array.append(entry["ID"].to_bytes(2, byteorder="little"))
				array.append(bytes.fromhex(entry['Args']))
				if ((ENG == True) and (len(entry["ENG"]) > 0)):
					array.append(entry["ENG"].encode("UTF-16-LE") + b"\x00\x00")
				else:
					array.append(entry["JPN"].encode("UTF-16-LE") + b"\x00\x00")
				array.append(entry["Category"].to_bytes(2, byteorder="little", signed=True))
				array.append(entry["Index"].to_bytes(2, byteorder="little", signed=True))
			else:
				array.append(bytes.fromhex(entry['Args']))
		case 3:
			array.append(bytes.fromhex(entry['Args']))
			try:
				array.append(numpy.uint16(entry['ID']))
			except: 
				return b''.join(array)
			else:
				array.append(bytes.fromhex(entry['Args2']))
				if (entry['ID'] == 1):
					string = "$d".join(entry["Strings"])
					stringbytes = string.encode("UTF-16-LE") + b"\x00\x00"
					array.append(numpy.uint16(len(stringbytes)))
					array.append(stringbytes)
		case _:
			array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def PRINTF(entry):
	array = []
	array.append(Commands.PRINTF.value.to_bytes(1, byteorder='little'))
	array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
	array.append(bytes.fromhex(entry['Args']))
	return b''.join(array)

def Make_command(entry, string, filename = None):
	match (entry['Type']):
		case "IMAGEUPDATE": return IMAGEUPDATE(entry)
		case "FARCALL": return FARCALL(entry, string)
		case "COLORLEVEL": return COLORLEVEL(entry)
		case "MCSHAKE": return MCSHAKE(entry)
		case "SCISSOR_TRIANGLELIST_SET": return SCISSOR_TRIANGLELIST_SET(entry)
		case "VARSTR_ALLOC": return VARSTR_ALLOC(entry)
		case "SUB": return SUB(entry)
		case "RANDOM": return RANDOM(entry)
		case "SWAP": return SWAP(entry)
		case "ROT": return ROT(entry)
		case "IFY": return IFY(entry, string, filename)
		case "MESSAGE_CLEAR": return MESSAGE_CLEAR(entry)
		case "WAIT_TEXTFEED": return WAIT_TEXTFEED(entry)
		case "ADDCOLOR": return ADDCOLOR(entry)
		case "SATURATION": return SATURATION(entry)
		case "VOICE": return VOICE(entry)
		case "MASK": return MASK(entry)
		case "VOLUME": return VOLUME(entry)
		case "DISP": return DISP(entry)
		case "SCISSOR": return SCISSOR(entry)
		case "PRIORITY": return PRIORITY(entry)
		case "SETCGFLAG": return SETCGFLAG(entry)
		case "SEPIA": return SEPIA(entry)
		case "SEPIA_COLOR": return SEPIA_COLOR(entry)
		case "WIPE": return WIPE(entry)
		case "CUSTOMMOVE": return CUSTOMMOVE(entry)
		case "IMAGEUUPDATE": return IMAGEUPDATE(entry)
		case "QUAKE": return QUAKE(entry)
		case "EVSCROLL": return EVSCROLL(entry)
		case "SCALE": return SCALE(entry)
		case "BMODE": return BMODE(entry)
		case "ADD": return ADD(entry)
		case "RETURN": return RETURN(entry)
		case "GOSUB": return GOSUB(entry, string, filename)
		case "BGM": return BGM(entry)
		case "SE": return SE(entry)
		case "MOVIE": return MOVIE(entry)
		case "SETBGMFLAG": return SETBGMFLAG(entry)
		case "COLORBG_SET": return COLORBG_SET(entry)
		case "EQU": return EQU(entry)
		case "EQUN": return EQUN(entry)
		case "VARSTR": return VARSTR(entry)
		case "GOTO": return GOTO(entry, string, filename)
		case "IFN": return IFN(entry, string, filename)
		case "JUMP": return JUMP(entry, string)
		case "JUMPPOINT": return JUMPPOINT(entry)
		case "END": return END(entry)
		case "TALKNAME_SET": return TALKNAME_SET(entry)
		case "VARSTR_SET": return VARSTR_SET(entry)
		case "ARFLAGSET": return ARFLAGSET(entry)
		case "SHAKELIST_SET": return SHAKELIST_SET(entry)
		case "MESSAGE": return MESSAGE(entry)
		case "SELECT": return SELECT(entry)
		case "CLOSE_WINDOW": return CLOSE_WINDOW(entry)
		case "LOG": return LOG(entry)
		case "LOG_END": return LOG_END(entry)
		case "FFSTOP": return FFSTOP(entry)
		case "INIT": return INIT(entry)
		case "STOP": return STOP(entry)
		case "IMAGELOAD": return IMAGELOAD(entry)
		case "MOVE": return MOVE(entry)
		case "MOVE2": return MOVE2(entry)
		case "FADE": return FADE(entry)
		case "SHAKELIST": return SHAKELIST(entry)
		case "WAIT": return WAIT(entry)
		case "DRAW": return DRAW(entry)
		case "BGM_WAITFADE": return BGM_WAITFADE(entry)
		case "BGM_POP": return BGM_POP(entry)
		case "SE_WAIT": return SE_WAIT(entry)
		case "EX": return EX(entry)
		case "TASK": return TASK(entry)
		case "PRINTF": return PRINTF(entry)
		case _:
			print("Type not supported: %s" % (entry['Type']))
			sys.exit()

def Process(string, entry, offset_new, filename):
	match (string):
		case "SIZE":
			_COM = Make_command(entry, string)
			LABELS[filename][entry['LABEL']] = offset_new
			return len(_COM)
		case "DUMMYSIZE":
			_COM = Make_command(entry, string)
			return len(_COM)
		case "COMMAND":
			return Make_command(entry, string, filename)
		case _:
			print("Unsupported Process command: %s" % (string))
			sys.exit()

if (len(sys.argv) != 4):
	print("script_compiler.py [ENG/JPN] [input folder] [output file]")
	sys.exit()

if (sys.argv[1] == "ENG"): ENG = True
elif (sys.argv[1] != "JPN"):
	print("script_compiler.py [ENG/JPN] [input folder] [output file]")
	sys.exit()

try:
	os.mkdir("%s/Compiled" % sys.argv[2])
except:
	pass

with open("%s/chapternames.json" % sys.argv[2], 'r', encoding="UTF-8") as f:
	Filenames = json.load(f)

print("BUILDING OFFSET JUMP DATABASE...")
for i in range(0, len(Filenames)):
	print("%s" % Filenames[i], end="\r")
	IgnoreMessage = False
	offset_new = 0
	EXCEPTIONS = ["_VOICE_PARAM", "_VARNUM", "_SCR_LABEL", "_CGMODE", "_BUILD_COUNT", "_TASK"]
	if (Filenames[i] in EXCEPTIONS):
		continue
	if (Filenames[i] in ["_島モン_CS用処理", "0_デバッグジャンプ", "RB99_ボイスチェックCS用"]):
		IgnoreMessage = True
	LABELS[Filenames[i].lower()] = {}
	file = open("%s/json/%s.json" % (sys.argv[2], Filenames[i]), "r", encoding="UTF-8")
	DUMP = json.load(file)
	file.close()
	for x in range(0, len(DUMP)):
		try:
			Size = Process("SIZE", DUMP[x], offset_new, Filenames[i].lower())
		except Exception as exc:
			print("Catched exception in %s" % Filenames[i])
			print(exc)
			sys.exit()
		if (Size % 2 != 0): Size += 1
		offset_new += Size + 2
	print(" " * 64, end='\r')

print("BUILDING SCRIPT")
for i in range(0, len(Filenames)):
	IgnoreMessage = False
	offset_new = 0
	EXCEPTIONS = ["_VOICE_PARAM", "_VARNUM", "_SCR_LABEL", "_CGMODE", "_BUILD_COUNT"]
	if (Filenames[i] in EXCEPTIONS):
		print("%s in EXCEPTIONS. Ignoring..." % (Filenames[i]))
		shutil.copy("%s/new/%s.dat" % (sys.argv[2], Filenames[i]), "%s/Compiled/%s.dat" % (sys.argv[2], Filenames[i]))
		continue
	print("%s" % Filenames[i])
	if (Filenames[i] in ["_島モン_CS用処理", "0_デバッグジャンプ", "RB99_ボイスチェックCS用"]):
		IgnoreMessage = True
	file = open("%s/json/%s.json" % (sys.argv[2], Filenames[i]), "r", encoding="UTF-8")
	DUMP = json.load(file)
	file.close()
	if (Filenames[i] == "_TASK"):
		file = open("%s/Compiled/%s.dat" % (sys.argv[2], Filenames[i]), "wb")
		for x in range(0, len(DUMP)):
			file.write(DUMP[x].encode("shift_jis_2004")+b"\x00")
		file.close()
	else:
		COMMAND_OUTPUT_SIZE = []
		for x in range(0, len(DUMP)):
			Size = Process("DUMMYSIZE", DUMP[x], offset_new, Filenames[i].lower())
			if (Size % 2 != 0): Size += 1
			COMMAND_OUTPUT_SIZE.append(Size)
			offset_new += Size + 2
		file = open("%s/Compiled/%s.dat" % (sys.argv[2], Filenames[i]), "wb")
		for x in range(0, len(DUMP)):
			COM = Process("COMMAND", DUMP[x], offset_new, Filenames[i].lower())
			file.write((len(COM)+2).to_bytes(2, byteorder='little'))
			file.write(COM)
			if (len(COM) % 2 != 0): file.write(b"\x00")
		file.close()

print(" " * 64, end='\r')
print("WRITING SCRIPT")
unk0 = []

unk2_int32 = 1
round_to = 4

new_file = open(sys.argv[3], "wb")
new_file.write(b"\x00" * 4)
new_file.write(numpy.uint32(len(Filenames)))
new_file.write(numpy.uint32(unk2_int32))
new_file.write(numpy.uint32(round_to))
new_file.write(b"\x00" * 16)
new_file.write(numpy.uint32(0x200))
new_file.write(b"\x00" * 4)

#Calculate header size
base = new_file.tell()
offset = 0
for i in range(0, len(Filenames)):
	offset += 8
new_file.seek(0x24)
new_file.write(numpy.uint32(base + offset))
for i in range(0, len(Filenames)):
	offset += (len(Filenames[i].encode("shift_jis_2004") ) + 1)
if (offset % 4 != 0):
	offset += (4 - (offset % 4))
new_file.seek(0)
new_file.write(numpy.uint32(base + offset))
new_file.seek(0, 2)

header_size = base + offset

scripts_size = []

for i in range(0, len(Filenames)):
	script = open("%s/Compiled/%s.dat" % (sys.argv[2], Filenames[i]), "rb")
	script.seek(0, 2)
	scripts_size.append(script.tell())
	script.close()

offset = header_size / 4

for i in range(0, len(Filenames)):
	new_file.write(numpy.uint32(offset))
	new_file.write(numpy.uint32(scripts_size[i]))
	offset += int(round((scripts_size[i]+1) / 4))

for i in range(0, len(Filenames)):
	new_file.write(Filenames[i].encode("shift_jis_2004"))
	new_file.write(b"\x00")

while(True):
	if (new_file.tell() == header_size): break
	new_file.write(b"\x00")

for i in range(0, len(Filenames)):
	script = open("%s/Compiled/%s.dat" % (sys.argv[2], Filenames[i]), "rb")
	temp = script.read()
	new_file.write(temp)
	if (len(temp) != (4 * round((scripts_size[i]+1) / 4))):
		rest = (4 * round((scripts_size[i]+1) / 4) - len(temp))
		for i in range(0, rest):
			new_file.write(b"\x00")

if (new_file.tell() % 16 != 0):
	rest = 16 - (new_file.tell() % 16)
	for i in range(0, rest):
		new_file.write(b"\x00")
