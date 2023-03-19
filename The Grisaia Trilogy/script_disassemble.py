import json
import os
import sys
from enum import Enum

Dump = {}
Dump['Main'] = []

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
	STARTUP_BETGIN = 0x1A
	STARTUP_END = 0x1B
	VARSTR_SET = 0x1C
	VARSTR_ALLOC = 0x1D
	ARFLAGSET = 0x1E
	COLORBG_SET = 0x1F
	SPLINE_SET = 0x20
	SHAKELIST_SET = 0x21
	SCISSOR_TRIANGLELIST_SET = 0x22
	MESSAGE = 0x23
	MESSAGE_CLEAR = 0x24
	MESSAGE_WAIT = 0x25
	SELECT = 0x26
	CLOSE_WINDOW = 0x27
	FADE_WINDOW = 0x28
	LOG = 0x29
	LOG_PAUSE = 0x2A
	LOG_END = 0x2B
	VOICE = 0x2C
	VOICE_STOP = 0x2D
	WAIT_COUNT = 0x2E
	WAIT_TIME = 0x2F
	WAIT_TEXTFEED = 0x30
	FFSTOP = 0x31
	INIT = 0x32
	STOP = 0x33
	IMAGELOAD = 0x34
	IMAGEUPDATE = 0x35
	ARC = 0x36
	MOVE = 0x37
	ROT = 0x38
	PEND = 0x39
	FADE = 0x3A
	SCALE = 0x3B
	SHAKE = 0x3C
	SHAKELIST = 0x3D
	BASE = 0x3E
	MCMOVE = 0x3F
	MCARC = 0x40
	MCROT = 0x41
	MCSHAKE = 0x42
	MCFADE = 0x43
	WAIT = 0x44
	DRAW = 0x45
	WIPE = 0x46
	FRAMEON = 0x47
	FRAMEOFF = 0x48
	FW = 0x49
	SCISSOR = 0x4A
	DELAY = 0x4B
	RASTER = 0x4C
	TONE = 0x4D
	SCALECOSSIN = 0x4E
	BMODE = 0x4F
	SIZE = 0x50
	SPLINE = 0x51
	DISP = 0x52
	MASK = 0x53
	FACE = 0x54
	SEPIA = 0x55
	SEPIA_COLOR = 0x56
	CUSTOMMOVE = 0x57
	SWAP = 0x58
	ADDCOLOR = 0x59
	SUBCOLOR = 0x5A
	SATURATION = 0x5B
	PRIORITY = 0x5C
	UVWH = 0x5D
	EVSCROLL = 0x5E
	COLORLEVEL = 0x5F
	NEGA = 0x60
	QUAKE = 0x61
	BGM = 0x62
	BGM_WAITSTART = 0x63
	BGM_WAITFADE = 0x64
	BGM_PUSH = 0x65
	BGM_POP = 0x66
	SE = 0x67
	SE_STOP = 0x68
	SE_WAIT = 0x69
	SE_WAIT_COUNT = 0x6A
	VOLUME = 0x6B
	MOVIE = 0x6C
	SETCGFLAG = 0x6D
	EX = 0x6E
	TROPHY = 0x6F
	SETBGMFLAG = 0x70
	TASK = 0x71
	PRINTF = 0x72
	VIB_PLAY = 0x73
	COUNTER_WAIT = 0x74
	MANPU = 0x75

def COLORLEVEL(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "COLORLEVEL"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def ARC(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "ARC"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def MCARC(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "MCARC"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def VOICE_STOP(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "VOICE_STOP"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def BASE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "BASE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SHAKE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SHAKE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def MANPU(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "MANPU"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def MCSHAKE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "MCSHAKE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SCISSOR_TRIANGLELIST_SET(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SCISSOR_TRIANGLELIST_SET"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def VARSTR_ALLOC(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "VARSTR_ALLOC"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SUB(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SUB"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def RANDOM(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "RANDOM"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SWAP(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SWAP"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def ROT(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "ROT"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def IFY(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "IFY"
	entry['SUBCMD'] = SUBCMD
	if (SUBCMD == 1):
		entry['Args'] = file.read(2).hex()
	entry["Equation"] = readString(file)
	if (SUBCMD > 1):
		print("IFN higher than 1 detected. SUBCMD: %d, file: %s, offset: %s" % (SUBCMD, file.name, entry['LABEL']))
		sys.exit()
	else:
		entry['GOTO_LABEL'] = "%s" % hex(int.from_bytes(file.read(4), "little"))
	MAIN_ENTRY.append(entry)

def MESSAGE_CLEAR(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "MESSAGE_CLEAR"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def WAIT_TEXTFEED(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "WAIT_TEXTFEED"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def ADDCOLOR(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "ADDCOLOR"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SATURATION(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SATURATION"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def VOICE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "VOICE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def MASK(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "MASK"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def VOLUME(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "VOLUME"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def DISP(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "DISP"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SCISSOR(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SCISSOR"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def PRIORITY(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "PRIORITY"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SETCGFLAG(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SETCGFLAG"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SEPIA(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SEPIA"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SEPIA_COLOR(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SEPIA_COLOR"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def WIPE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "WIPE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def CUSTOMMOVE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "CUSTOMMOVE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def IMAGEUPDATE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "IMAGEUPDATE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def QUAKE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "QUAKE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def EVSCROLL(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "EVSCROLL"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SCALE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SCALE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def BMODE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "BMODE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def ADD(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "ADD"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def RETURN(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "RETURN"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def GOSUB(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "GOSUB"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize-4).hex()
	entry['GOTO_LABEL'] = "%s" % hex(int.from_bytes(file.read(4), "little"))
	MAIN_ENTRY.append(entry)

def BGM(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "BGM"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def MOVIE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "MOVIE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(4).hex()
	string_size = int.from_bytes(file.read(2), "little", signed=True)
	argsize -= 6
	if (string_size > 0):
		string_size *= 2
		entry["Name"] = file.read(string_size).decode("UTF-16-LE")
		file.seek(2, 1)
		entry['Args2'] = file.read(argsize - (string_size + 2)).hex()
	else:
		string_size *= -1
		entry["Name"] = file.read(string_size).decode("UTF-8")
		file.seek(1, 1)
		entry['Args2'] = file.read(argsize - (string_size + 1)).hex()
	MAIN_ENTRY.append(entry)

def SETBGMFLAG(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SETBGMFLAG"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def COLORBG_SET(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "COLORBG_SET"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def ONGOTO(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "ONGOTO"
	entry['SUBCMD'] = SUBCMD
	if (SUBCMD == 1):
		entry['Args'] = file.read(2).hex()
		argsize -= 2
	else:
		print("UNKNOWN SUBCMD ONGOTO: %d" % SUBCMD)
		sys.exit()
	entry["String"] = readString(file)
	jump_count = int((argsize - (len(entry["String"]) + 1)) / 6)
	entry["Args2"] = []
	entry['GOTO_LABEL'] = []
	for i in range(jump_count):
		entry["Args2"].append(int.from_bytes(file.read(2), "little"))
		entry['GOTO_LABEL'].append("%s" % hex(int.from_bytes(file.read(4), "little")))
	MAIN_ENTRY.append(entry)

def FARCALL(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "FARCALL"
	entry['SUBCMD'] = SUBCMD
	if (SUBCMD == 0):
		entry['Args'] = file.read(2).hex()
	else:
		entry['Args'] = file.read(4).hex()
	entry["String"] = readString(file)
	entry['GOTO_LABEL'] = "%s" % hex(int.from_bytes(file.read(4), "little"))
	print(entry)
	MAIN_ENTRY.append(entry)

def FLAGCLR(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "FLAGCLR"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def EQU(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "EQU"
	entry['SUBCMD'] = SUBCMD
	match(SUBCMD):
		case 0:
			entry['Args'] = file.read(2).hex()
		case 1:
			entry['Args'] = file.read(4).hex()
		case _:
			print("UNKNOWN EQU SUBCMD: %d" % SUBCMD)
			print(entry['LABEL'])
			sys.exit()
	entry["String"] = readString(file)
	MAIN_ENTRY.append(entry)

def EQUN(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "EQUN"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def VARSTR(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "EQUN"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

# Jumps to offset in the same file.
def GOTO(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "GOTO"
	entry['SUBCMD'] = SUBCMD
	if (SUBCMD == 1): 
		entry['Args'] = (file.read(2).hex())
		entry['GOTO_LABEL'] = "%s" % hex(int.from_bytes(file.read(4), "little"))
	else: entry['GOTO_LABEL'] = "%s" % hex(int.from_bytes(file.read(4), "little"))
	MAIN_ENTRY.append(entry)

def IFN(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "IFN"
	entry['SUBCMD'] = SUBCMD
	if (SUBCMD == 1):
		entry['Args'] = file.read(2).hex()
	entry["Equation"] = readString(file)
	if (SUBCMD > 1):
		print("IFN higher than 1 detected. SUBCMD: %d, file: %s, offset: %s" % (SUBCMD, file.name, entry['LABEL']))
		sys.exit()
	else:
		entry['GOTO_LABEL'] = "%s" % hex(int.from_bytes(file.read(4), "little"))
	MAIN_ENTRY.append(entry)

# JUMP is used to go to new file. As part of Args contains name of script file (f.e. "com02").
def JUMP(SUBCMD, MAIN_ENTRY, file, argsize):
	#print("0x%x" % ((file.tell())-4))
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "JUMP"
	entry['SUBCMD'] = SUBCMD
	if (SUBCMD == 1): 
		entry['Args'] = file.read(2).hex()
	string_size = int.from_bytes(file.read(2), "little", signed=True)
	if (string_size > 0):
		string_size *= 2
		entry['Name'] = file.read(string_size).decode("UTF-16-LE")
		file.seek(2, 1)
	else:
		string_size *= -1
		entry['Name'] = file.read(string_size).decode("UTF-8")
		file.seek(1, 1)
	MAIN_ENTRY.append(entry)

def JUMPPOINT(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "JUMPPOINT"
	entry['SUBCMD'] = SUBCMD
	if (SUBCMD != 0):
		entry["Args"] = file.read(2).hex()
	MAIN_ENTRY.append(entry)

def VARSTR_SET(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "VARSTR_SET"
	entry['SUBCMD'] = SUBCMD
	if (SUBCMD == 1):
		entry['Args'] = file.read(2).hex()
		entry["ID"] = int.from_bytes(file.read(2), "little", signed=True)
		string_size = int.from_bytes(file.read(2), "little", signed=True)
		if (string_size < 0):
			print("Uh, no?")
			sys.exit()
		string_size *= 2
		entry["STRING"] = file.read(string_size).decode("UTF-16-LE")
		file.seek(2, 1)
	else:	
		entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def END(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "END"
	entry['SUBCMD'] = SUBCMD
	if (SUBCMD > 0):
		entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def ARFLAGSET(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "ARFLAGSET"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SHAKELIST_SET(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SHAKELIST_SET"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def MESSAGE(SUBCMD, MAIN_ENTRY, file, argsize):
	debug_offset = file.tell()
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "MESSAGE"   
	entry['SUBCMD'] = SUBCMD
	SUBCMD2 = int(int.from_bytes(file.read(2), "little"))
	entry['SUBCMD2'] = SUBCMD2
	entry['MSGID'] = int(int.from_bytes(file.read(2), "little"))
	temp_numb = int(int.from_bytes(file.read(2), "little"))
	if (temp_numb != 0): entry['VOICEID'] = temp_numb
	string_size = int.from_bytes(file.read(2), "little", signed=True)
	if (string_size == 0):
		file.seek(-2, 1)
		entry['Args'] = file.read(argsize-6).hex()
	else:
		temp_size = 0
		if (string_size > 0):
			string_size = string_size * 2
			text = file.read(string_size).decode("UTF-16-LE")
			if (text[0] == "@"):
				char_count = 0
				for i in range(1, 32):
					if (text[i] == "@"): 
						char_count = i
						break
				entry['NameJPN'] = text[1:char_count]
				entry['JPN'] = text[char_count+1:]
			else:    
				entry['JPN'] = text
			file.seek(2, 1)
			temp_size += string_size + 2
		else:
			string_size *= -1
			text = file.read(string_size).decode("UTF-8")
			if (text[0] == "@"):
				char_count = 0
				for i in range(1, 16):
					if (text[i] == "@"): 
						char_count = i
						break
				entry['NameJPN'] = text[1:char_count]
				entry['JPN'] = text[char_count+1:]
			else:    
				entry['JPN'] = text
			file.seek(1, 1)
			temp_size += abs(string_size) + 1
		string_size = int.from_bytes(file.read(2), "little", signed=True)
		if (string_size > 0):
			string_size = string_size * 2
			text = file.read(string_size).decode("UTF-16-LE")
			if (text[0] == "@"):
				char_count = 0
				for i in range(1, 32):
					if (text[i] == "@"): 
						char_count = i
						break
				entry['NameENG'] = text[1:char_count]
				entry['ENG'] = text[char_count+1:]
			else:    
				entry['ENG'] = text
			file.seek(2, 1)
			temp_size += string_size + 2
		else:
			string_size *= -1
			text = file.read(string_size).decode("UTF-8")
			if (text[0] == "@"):
				char_count = 0
				for i in range(1, 16):
					if (text[i] == "@"): 
						char_count = i
						break
				entry['NameENG'] = text[1:char_count]
				entry['ENG'] = text[char_count+1:]
			else:    
				entry['ENG'] = text
			file.seek(1, 1)
			temp_size += abs(string_size) + 1
		try:
			entry['Args'] = file.read(argsize - temp_size - 10).hex()
		except:
			print("Error while processing message. Start offset: 0x%x" % (debug_offset-2))
			sys.exit()
	MAIN_ENTRY.append(entry)

def SELECT(SUBCMD, MAIN_ENTRY, file, argsize):
	debug_offset = file.tell() - 2
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SELECT"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(9).hex()
	temp_size = 0
	if (file.read(1) == b"@"):
		string_size = int.from_bytes(file.read(2), "little", signed=True)
		if (string_size > 0): 
			string_size = string_size * 2
			entry['JAP'] = file.read(string_size).decode("UTF-16-LE").split("$d", -1)
			file.seek(2, 1)
			temp_size += string_size + 2
		else:
			string_size *= -1
			entry['JAP'] = file.read(string_size).decode("UTF-8").split("$d", -1)
			file.seek(1, 1)
			temp_size += string_size + 1
		string_size = int.from_bytes(file.read(2), "little", signed=True)
		if (string_size > 0): 
			string_size = string_size * 2
			entry['ENG'] = file.read(string_size).decode("UTF-16-LE").split("$d", -1)
			file.seek(2, 1)
			temp_size += string_size + 2
		else:
			string_size *= -1
			entry['ENG'] = file.read(string_size).decode("UTF-8").split("$d", -1)
			file.seek(1, 1)
			temp_size += string_size + 1
	try:
		entry['Args2'] = file.read(argsize - 14 - temp_size).hex()
	except:
		print("Error while processing select. Start offset: 0x%x" % (debug_offset-2))
		sys.exit()
	MAIN_ENTRY.append(entry)

def CLOSE_WINDOW(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "CLOSE_WINDOW"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def FADE_WINDOW(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "FADE_WINDOW"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def LOG(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "LOG"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(7).hex()
	string_size = int.from_bytes(file.read(2), "little", signed=True)
	if (string_size == 0):
		file.seek(-9, 1)
		entry['Args'] = file.read(argsize).hex()
		MAIN_ENTRY.append(entry)
		return
	if (string_size > 0):
		string_size = string_size * 2
		text = file.read(string_size).decode("UTF-16-LE")
		if (text[0] == "@"):
			char_count = 0
			for i in range(1, 32):
				if (text[i] == "@"): 
					char_count = i
					break
			entry['NameJPN'] = text[1:char_count]
			entry['JPN'] = text[char_count+1:]
		else:    
			entry['JPN'] = text
		file.seek(2, 1)
	else:
		string_size *= -1
		text = file.read(string_size).decode("UTF-8")
		if (text[0] == "@"):
			char_count = 0
			for i in range(1, 32):
				if (text[i] == "@"): 
					char_count = i
					break
			entry['NameJPN'] = text[1:char_count]
			entry['JPN'] = text[char_count+1:]
		else:    
			entry['JPN'] = text
		file.seek(1, 1)
	string_size = int.from_bytes(file.read(2), "little", signed=True)
	if (string_size > 0):
		string_size = string_size * 2
		text = file.read(string_size).decode("UTF-16-LE")
		if (text[0] == "`"):
			char_count = 0
			for i in range(1, 32):
				if (text[i] == "@"): 
					char_count = i
					break
			entry['NameENG'] = text[1:char_count]
			entry['ENG'] = text[char_count+1:]
		else:    
			entry['ENG'] = text
		file.seek(2, 1)
	else:
		string_size *= -1
		text = file.read(string_size).decode("UTF-8")
		if (text[0] == "`"):
			char_count = 0
			for i in range(1, 32):
				if (text[i] == "@"): 
					char_count = i
					break
			entry['NameENG'] = text[1:char_count]
			entry['ENG'] = text[char_count+1:]
		else:    
			entry['ENG'] = text
		file.seek(1, 1)
	entry['Args2'] = file.read(1).hex()
	MAIN_ENTRY.append(entry)

def LOG_END(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "LOG_END"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def FFSTOP(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "FFSTOP"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def INIT(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "INIT"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def STOP(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "STOP"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def IMAGELOAD(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "IMAGELOAD"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def MOVE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "MOVE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def MCMOVE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "MCMOVE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def MCFADE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "MCFADE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def RASTER(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "RASTER"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def UVWH(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "UVWH"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def TONE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "TONE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SPLINE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SPLINE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SPLINE_SET(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SPLINE_SET"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SIZE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SIZE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def MCROT(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "MCROT"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def DELAY(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "DELAY"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def PEND(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "PEND"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def FADE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "FADE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SHAKELIST(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SHAKELIST"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def WAIT(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "WAIT"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SE_STOP(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SE_STOP"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def DRAW(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "DRAW"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def BGM_WAITFADE(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "BGM_WAITFADE"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def BGM_POP(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "BGM_POP"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def STARTUP_BETGIN(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "STARTUP_BETGIN"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def STARTUP_END(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "STARTUP_END"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def NEGA(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "NEGA"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def SE_WAIT(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "SE_WAIT"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def EX(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "EX"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def WAIT_COUNT(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "WAIT_COUNT"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def TASK(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "TASK"
	entry['SUBCMD'] = SUBCMD
	match(SUBCMD):
		case 0:
			entry['Args'] = file.read(2).hex()
			match(entry['Args']):
				case "0800":
					string = readString16(file)
					entry["Category"] = int.from_bytes(file.read(2), byteorder="little")
					entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
					entry["JPN"] = string
					entry["ENG"] = ""
				case "2700":
					entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
					entry["Args2"] = file.read(4).hex()
					string = readString16(file)
					entry["JPN"] = string
					entry["ENG"] = ""
					entry["Args3"] = file.read(6).hex()
				case _:
					file.seek(-2, 1)
					entry['Args'] = file.read(argsize).hex()
		case 1:
			entry['Args'] = file.read(argsize).hex()
		case 3:
			entry['Args'] = file.read(4).hex()
			entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
			match(entry["ID"]):
				case 1:
					entry['Args2'] = file.read(10).hex()
					character_count = int.from_bytes(file.read(2), "little")
					entry["String"] = file.read(character_count * 2).decode("UTF-16-LE")
					print(entry["Strings"])
					file.seek(2, 1)
				case 2:
					character_count = int.from_bytes(file.read(2), "little")
					entry["String"] = file.read(character_count * 2).decode("UTF-16-LE")
					file.seek(2, 1)
					entry['Args2'] = file.read(12).hex()
				case _:
					entry['Args2'] = file.read(argsize-6).hex()
		case _:
			entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)
	print(entry)

def PRINTF(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "PRINTF"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def LOG_END(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "LOG_END"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def GOTO_COMMANDS(CMD, SUBCMD, file, cmdsize):

	match (CMD):
		#case Commands.COLORLEVEL.value: COLORLEVEL(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.STARTUP_BETGIN.value: STARTUP_BETGIN(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.STARTUP_END.value: STARTUP_END(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SPLINE.value: SPLINE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SPLINE_SET.value: SPLINE_SET(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MCMOVE.value: MCMOVE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MCARC.value: MCARC(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MCROT.value: MCROT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MCSHAKE.value: MCSHAKE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MCFADE.value: MCFADE(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.SCISSOR_TRIANGLELIST_SET.value: SCISSOR_TRIANGLELIST_SET(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.VARSTR_ALLOC.value: VARSTR_ALLOC(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.SUB.value: SUB(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.MUL.value: MUL(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.DIV.value: DIV(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.RASTER.value: RASTER(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.RANDOM.value: RANDOM(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.SWAP.value: SWAP(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.PEND.value: PEND(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.ROT.value: ROT(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.IFY.value: IFY(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.SET.value: IFY(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.MESSAGE_WAIT.value: MESSAGE_WAIT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MESSAGE_CLEAR.value: MESSAGE_CLEAR(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.WAIT_TEXTFEED.value: WAIT_TEXTFEED(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.WAIT_COUNT.value: WAIT_COUNT(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.WAIT_TIME.value: WAIT_TIME(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.ADDCOLOR.value: ADDCOLOR(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.SUBCOLOR.value: SUBCOLOR(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.UVWH.value: UVWH(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SATURATION.value: SATURATION(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.NEGA.value: NEGA(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.VOICE.value: VOICE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.VOICE_STOP.value: VOICE_STOP(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MASK.value: MASK(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.VOLUME.value: VOLUME(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.DISP.value: DISP(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SCISSOR.value: SCISSOR(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.PRIORITY.value: PRIORITY(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SETCGFLAG.value: SETCGFLAG(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SEPIA.value: SEPIA(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.SEPIA_COLOR.value: SEPIA_COLOR(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.WIPE.value: WIPE(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.CUSTOMMOVE.value: CUSTOMMOVE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.IMAGEUPDATE.value: IMAGEUPDATE(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.QUAKE.value: QUAKE(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.EVSCROLL.value: EVSCROLL(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.SCALECOSSIN.value: SCALECOSSIN(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SIZE.value: SIZE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SCALE.value: SCALE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.BMODE.value: BMODE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.ADD.value: ADD(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.MOD.value: MOD(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.RETURN.value: RETURN(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.GOSUB.value: GOSUB(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.BGM.value: BGM(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SE.value: SE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MOVIE.value: MOVIE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SETBGMFLAG.value: SETBGMFLAG(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.AND.value: AND(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.OR.value: OR(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.COLORBG_SET.value: COLORBG_SET(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.ARC.value: ARC(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.EQU.value: EQU(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.EQUN.value: EQUN(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.EQUV.value: EQUV(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.VARSTR.value: VARSTR(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.GOTO.value: GOTO(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.ONGOTO.value: ONGOTO(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.IFN.value: IFN(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.JUMP.value: JUMP(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.JUMPPOINT.value: JUMPPOINT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.END.value: END(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.FRAMEON.value: FRAMEON(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.FRAMEOFF.value: FRAMEOFF(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.FACE.value: FACE(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.FLAGCLR.value: FLAGCLR(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.FARCALL.value: FARCALL(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.FARRETURN.value: FARRETURN(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.VARSTR_SET.value: VARSTR_SET(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.ARFLAGSET.value: ARFLAGSET(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SHAKELIST_SET.value: SHAKELIST_SET(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MESSAGE.value: MESSAGE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SELECT.value: SELECT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.CLOSE_WINDOW.value: CLOSE_WINDOW(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.LOG.value: LOG(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.LOG_PAUSE.value: LOG_PAUSE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.LOG_END.value: LOG_END(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.FFSTOP.value: FFSTOP(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.FW.value: INIT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.INIT.value: INIT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.STOP.value: STOP(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.IMAGELOAD.value: IMAGELOAD(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.BASE.value: BASE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MOVE.value: MOVE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.FADE_WINDOW.value: FADE_WINDOW(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.FADE.value: FADE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SHAKE.value: SHAKE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SHAKELIST.value: SHAKELIST(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.DELAY.value: DELAY(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.WAIT.value: WAIT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.DRAW.value: DRAW(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.BGM_WAITFADE.value: BGM_WAITFADE(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.BGM_POP.value: BGM_POP(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.BGM_PUSH.value: BGM_PUSH(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.BGM_WAITSTART.value: BGM_WAITSTART(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SE_WAIT.value: SE_WAIT(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.SE_STOP.value: SE_STOP(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.SE_WAIT_COUNT.value: SE_WAIT_COUNT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.TONE.value: TONE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.EX.value: EX(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.TROPHY.value: TROPHY(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.TASK.value: TASK(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.PRINTF.value: PRINTF(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.VIB_PLAY.value: VIB_PLAY(SUBCMD, Dump['Main'], file, cmdsize-4)
		#case Commands.COUNTER_WAIT.value: COUNTER_WAIT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MANPU.value: MANPU(SUBCMD, Dump['Main'], file, cmdsize-4)
		case _: 
			print("Not implemented command: 0x%x, offset: %x" % (CMD, file.tell()-2))
			input("Press ENTER")
			sys.exit()

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("shift_jis_2004"))
		chars.append(c)

def readString16(myfile):
	chars = []
	while True:
		c = myfile.read(2)
		if c == b'\x00\x00':
			return str(b"".join(chars).decode("UTF-16-LE"))
		chars.append(c)

def taskDecompile(file, filesize):
	while (file.tell() < filesize):
		Dump["Main"].append(readString(file))


os.makedirs("%s/json/grisaia1" % os.path.basename(sys.argv[1])[:-4], exist_ok=True)
os.makedirs("%s/json/grisaia2" % os.path.basename(sys.argv[1])[:-4], exist_ok=True)
os.makedirs("%s/json/grisaia3" % os.path.basename(sys.argv[1])[:-4], exist_ok=True)
os.makedirs("%s/json/side" % os.path.basename(sys.argv[1])[:-4], exist_ok=True)
os.makedirs("%s/new/grisaia1" % os.path.basename(sys.argv[1])[:-4], exist_ok=True)
os.makedirs("%s/new/grisaia2" % os.path.basename(sys.argv[1])[:-4], exist_ok=True)
os.makedirs("%s/new/grisaia3" % os.path.basename(sys.argv[1])[:-4], exist_ok=True)
os.makedirs("%s/new/side" % os.path.basename(sys.argv[1])[:-4], exist_ok=True)

file = open(sys.argv[1], "rb")

header_size = int.from_bytes(file.read(4), "little", signed=True)
if (header_size % 0x2000 == 0): raise ValueError("This script is dedicated only to script packages. Detected not correct one")

file_count = int.from_bytes(file.read(4), "little", signed=True)
unk2_int32 = int.from_bytes(file.read(4), "little", signed=True)
round_to = int.from_bytes(file.read(4), "little", signed=True)
reserved0 = file.read(0x10)
flag0 = int.from_bytes(file.read(1), "little", signed=True)
flag1 = int.from_bytes(file.read(1), "little", signed=True)
flag2 = int.from_bytes(file.read(1), "little", signed=True)
flag3 = int.from_bytes(file.read(1), "little", signed=True)
offset_start_file_names = int.from_bytes(file.read(4), "little")

file_table = {}
file_table['offset'] = []
file_table['size'] = []

for i in range(0, file_count):
	file_table['offset'].append(int.from_bytes(file.read(4), "little")*4)
	file_table['size'].append(int.from_bytes(file.read(4), "little"))

Filenames = []

for i in range(0, file_count):
	Filenames.append(readString(file))

with open("%s/chapternames.json" % os.path.basename(sys.argv[1])[:-4], "w", encoding="UTF-8") as chapter_names:
	json.dump(Filenames, chapter_names, indent="\t", ensure_ascii=False)

for i in range(0, file_count):
	file.seek(file_table['offset'][i], 0)
	file_new = open("%s/new/%s.dat" % (os.path.basename(sys.argv[1])[:-4], Filenames[i]), "wb")
	file_new.write(file.read(file_table['size'][i]))
	file_new.close()

for i in range(0, len(Filenames)):
	EXCEPTIONS = ["_voice_param", "_varnum", "_scr_label", "_cgmode", "_build_count"]
	if (Filenames[i] in EXCEPTIONS): 
		print("%s in EXCEPTIONS. Ignoring..." % (Filenames[i]))
		continue
	print(Filenames[i])
	file = open("%s/new/%s.dat" % (os.path.basename(sys.argv[1])[:-4], Filenames[i]), "rb")
	file.seek(0, 2)
	file_size = file.tell()
	file.seek(0, 0)
	if (Filenames[i] == "_task"):
		taskDecompile(file, file_size)
	else:
		while (file.tell() < file_size):
			command_size = int.from_bytes(file.read(2), "little")
			GOTO_COMMANDS(int.from_bytes(file.read(1), "little"), int(int.from_bytes(file.read(1), "little")), file, command_size)
			end = file.tell()
			if (end % 2 != 0):
				file.seek(1, 1)
	file.close()
	new_file = open("%s/json/%s.json" % (os.path.basename(sys.argv[1])[:-4], Filenames[i]), "w", encoding="UTF-8")
	json.dump(Dump['Main'], new_file, indent="\t", ensure_ascii=False)
	new_file.close()
	Dump['Main'] = []