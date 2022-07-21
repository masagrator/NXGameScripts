import numpy
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

def COLORLEVEL(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "COLORLEVEL"
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
		entry['GOTO_LABEL'] = "%s" % hex(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0])
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
	entry['GOTO_LABEL'] = "%s" % hex(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0])
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
	argsize -= 4
	entry["Name"] = readString(file)
	entry['Args2'] = file.read(argsize - (len(entry["Name"]) + 1)).hex()
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
	entry['GOTO_LABEL'] = "%s" % hex(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0])
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
	entry['Type'] = "VARSTR"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(4).hex()
	if (SUBCMD == 1):
		entry['Args'] += file.read(2).hex()
	entry["JPN"] = readString16(file)
	entry["ENG"] = ""
	MAIN_ENTRY.append(entry)

# Jumps to offset in the same file.
def GOTO(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "GOTO"
	entry['SUBCMD'] = SUBCMD
	if (SUBCMD == 1): 
		entry['Args'] = (file.read(2).hex())
		entry['GOTO_LABEL'] = "%s" % hex(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0])
	else: entry['GOTO_LABEL'] = "%s" % hex(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0])
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
		entry['GOTO_LABEL'] = "%s" % hex(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0])
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
	entry['Name'] = readString(file)
	entry['GOTO_LABEL'] = "0x%x" % int.from_bytes(file.read(4), byteorder="little")
	MAIN_ENTRY.append(entry)

def JUMPPOINT(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "JUMPPOINT"
	entry['SUBCMD'] = SUBCMD
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

def TALKNAME_SET(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "TALKNAME_SET"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def MOVE2(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "MOVE2"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def VARSTR_SET(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "VARSTR_SET"
	entry['SUBCMD'] = SUBCMD
	entry["Metadata"] = file.read(4).hex()
	string_size_temp = numpy.fromfile(file, dtype=numpy.uint16, count=1)[0]
	if (string_size_temp > 0):
		string_size = (string_size_temp + 1) * 2
		entry["JPN"] = file.read(string_size)[:-2].decode("UTF-16-LE")
		entry['ENG'] = ""
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
	SUBCMD2 = int(numpy.fromfile(file, dtype=numpy.uint16, count=1)[0])
	entry['SUBCMD2'] = SUBCMD2
	entry['MSGID'] = int(numpy.fromfile(file, dtype=numpy.uint16, count=1)[0])
	temp_numb = int(numpy.fromfile(file, dtype=numpy.uint16, count=1)[0])
	if (temp_numb != 0): entry['VOICEID'] = temp_numb
	string_size = numpy.fromfile(file, dtype=numpy.int16, count=1)[0]
	if (string_size == 0):
		file.seek(-2, 1)
		entry['Args'] = file.read(argsize-6).hex()
	else:
		temp_size = 0
		if (string_size > 0):
			string_size = string_size * 2
			text = file.read(string_size).decode("UTF-16-LE")
			if (text[0] == "`"):
				char_count = 0
				for i in range(1, 32):
					if (text[i] == "@"): 
						char_count = i
						break
				entry['NameJPN'] = text[1:char_count]
				entry['JPN'] = text[char_count+1:]
				entry['NameENG'] = ""
			else:    
				entry['JPN'] = text
			file.seek(2, 1)
			temp_size += string_size + 2
		else:
			text = file.read(string_size).decode("UTF-8")
			if (text[0] == "`"):
				char_count = 0
				for i in range(1, 16):
					if (text[i] == "@"): 
						char_count = i
						break
				entry['NameJPN'] = text[1:char_count]
				entry['JPN'] = text[char_count+1:]
				entry['NameENG'] = ""
			else:    
				entry['JPN'] = text
			file.seek(1, 1)
			temp_size += abs(string_size) + 1
		entry['ENG'] = ""
		try:
			entry['Args'] = file.read(argsize - temp_size - 8).hex()
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
		string_size = numpy.fromfile(file, dtype=numpy.int16, count=1)[0]
		if (string_size > 0): 
			string_size = string_size * 2
			entry['JPN'] = file.read(string_size).decode("UTF-16-LE").split("$d", -1)
			file.seek(2, 1)
			temp_size += string_size + 2
		else:
			entry['JPN'] = file.read(string_size).decode("UTF-8").split("$d", -1)
			file.seek(1, 1)
			temp_size += string_size + 1
		entry["ENG"] = []
		for i in range(0, len(entry['JPN'])):
			entry["ENG"].append("")
	try:
		entry['Args2'] = file.read(argsize - 12 - temp_size).hex()
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

def LOG(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "LOG"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(7).hex()
	string_size = numpy.fromfile(file, dtype=numpy.int16, count=1)[0]
	if (string_size == 0):
		file.seek(-9, 1)
		entry['Args'] = file.read(argsize).hex()
		MAIN_ENTRY.append(entry)
		return
	elif (string_size > 0):
		string_size = string_size * 2
		text = file.read(string_size).decode("UTF-16-LE")
		if (text[0] == "`"):
			char_count = 0
			for i in range(1, 32):
				if (text[i] == "@"): 
					char_count = i
					break
			entry['NameJPN'] = text[1:char_count]
			entry['JPN'] = text[char_count+1:]
			entry['NameENG'] = ""
		else:    
			entry['JPN'] = text
		file.seek(2, 1)
	else:
		text = file.read(string_size).decode("UTF-8")
		if (text[0] == "`"):
			char_count = 0
			for i in range(1, 32):
				if (text[i] == "@"): 
					char_count = i
					break
			entry['NameJPN'] = text[1:char_count]
			entry['JPN'] = text[char_count+1:]
			entry['NameENG'] = ""
		else:    
			entry['JPN'] = text
		file.seek(1, 1)
	entry['ENG'] = ""
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
			entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
			entry['Args'] = file.read(2).hex()
			if (entry['Args'] != "0800"):
				file.seek(-4, 1)
				entry.pop("ID")
				entry['Args'] = file.read(argsize).hex()
			else:
				string = readString16(file)
				entry["Category"] = int.from_bytes(file.read(2), byteorder="little")
				entry["Index"] = int.from_bytes(file.read(2), byteorder="little")
				entry["JPN"] = string
				entry["ENG"] = ""
		case 3:
			entry['Args'] = file.read(4).hex()
			entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
			if (entry["ID"] == 1):
				entry['Args2'] = file.read(10).hex()
				character_count = numpy.fromfile(file, dtype=numpy.uint16, count=1)[0]
				entry["Strings"] = list(file.read(character_count * 2).decode("UTF-16-LE").split("$d"))
				print(entry["Strings"])
				file.seek(2, 1)
			else:
				entry['Args2'] = file.read(argsize-6).hex()
		case _:
			entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def PRINTF(SUBCMD, MAIN_ENTRY, file, argsize):
	entry = {}
	entry['LABEL'] = "%s" % (hex(file.tell()-4))
	entry['Type'] = "PRINTF"
	entry['SUBCMD'] = SUBCMD
	entry['Args'] = file.read(argsize).hex()
	MAIN_ENTRY.append(entry)

def GOTO_COMMANDS(CMD, SUBCMD, file, cmdsize):
	#print("CMD: 0x%x, offset: 0x%x" % (CMD, file.tell()-2))
	match (CMD):
		case Commands.COLORLEVEL.value: COLORLEVEL(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MCSHAKE.value: MCSHAKE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SCISSOR_TRIANGLELIST_SET.value: SCISSOR_TRIANGLELIST_SET(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.VARSTR_ALLOC.value: VARSTR_ALLOC(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SUB.value: SUB(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.RANDOM.value: RANDOM(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SWAP.value: SWAP(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.ROT.value: ROT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.IFY.value: IFY(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MESSAGE_CLEAR.value: MESSAGE_CLEAR(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.WAIT_TEXTFEED.value: WAIT_TEXTFEED(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.ADDCOLOR.value: ADDCOLOR(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SATURATION.value: SATURATION(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.VOICE.value: VOICE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MASK.value: MASK(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.VOLUME.value: VOLUME(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.DISP.value: DISP(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SCISSOR.value: SCISSOR(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.PRIORITY.value: PRIORITY(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SETCGFLAG.value: SETCGFLAG(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SEPIA.value: SEPIA(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SEPIA_COLOR.value: SEPIA_COLOR(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.WIPE.value: WIPE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.CUSTOMMOVE.value: CUSTOMMOVE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.IMAGEUPDATE.value: IMAGEUPDATE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.QUAKE.value: QUAKE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.EVSCROLL.value: EVSCROLL(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SCALE.value: SCALE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.BMODE.value: BMODE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.ADD.value: ADD(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.RETURN.value: RETURN(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.GOSUB.value: GOSUB(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.BGM.value: BGM(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SE.value: SE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MOVIE.value: MOVIE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SETBGMFLAG.value: SETBGMFLAG(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.COLORBG_SET.value: COLORBG_SET(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.EQU.value: EQU(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.EQUN.value: EQUN(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.VARSTR.value: VARSTR(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.GOTO.value: GOTO(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.IFN.value: IFN(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.JUMP.value: JUMP(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.JUMPPOINT.value: JUMPPOINT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.END.value: END(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.FLAGCLR.value: FLAGCLR(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.FARCALL.value: FARCALL(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.TALKNAME_SET.value: TALKNAME_SET(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.VARSTR_SET.value: VARSTR_SET(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.ARFLAGSET.value: ARFLAGSET(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SHAKELIST_SET.value: SHAKELIST_SET(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MESSAGE.value: MESSAGE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SELECT.value: SELECT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.CLOSE_WINDOW.value: CLOSE_WINDOW(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.LOG.value: LOG(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.LOG_END.value: LOG_END(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.FFSTOP.value: FFSTOP(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.INIT.value: INIT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.STOP.value: STOP(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.IMAGELOAD.value: IMAGELOAD(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MOVE.value: MOVE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.MOVE2.value: MOVE2(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.FADE.value: FADE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SHAKELIST.value: SHAKELIST(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.WAIT.value: WAIT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.DRAW.value: DRAW(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.BGM_WAITFADE.value: BGM_WAITFADE(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.BGM_POP.value: BGM_POP(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.SE_WAIT.value: SE_WAIT(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.EX.value: EX(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.TASK.value: TASK(SUBCMD, Dump['Main'], file, cmdsize-4)
		case Commands.PRINTF.value: PRINTF(SUBCMD, Dump['Main'], file, cmdsize-4)
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


os.makedirs("%s/json" % os.path.basename(sys.argv[1])[:-4], exist_ok=True)
os.makedirs("%s/new" % os.path.basename(sys.argv[1])[:-4], exist_ok=True)

file = open(sys.argv[1], "rb")

header_size = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
if (header_size % 0x2000 == 0): raise ValueError("This script is dedicated only to script packages. Detected not correct one")

file_count = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
unk2_int32 = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
round_to = numpy.fromfile(file, dtype=numpy.int32, count=1)[0]
reserved0 = file.read(0x10)
flag0 = numpy.fromfile(file, dtype=numpy.int8, count=1)[0]
flag1 = numpy.fromfile(file, dtype=numpy.int8, count=1)[0]
flag2 = numpy.fromfile(file, dtype=numpy.int8, count=1)[0]
flag3 = numpy.fromfile(file, dtype=numpy.int8, count=1)[0]
offset_start_file_names = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]

file_table = {}
file_table['offset'] = []
file_table['size'] = []

for i in range(0, file_count):
	file_table['offset'].append(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]*4)
	file_table['size'].append(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0])

Filenames = []

for i in range(0, file_count):
	Filenames.append(readString(file))

os.makedirs("%s" % os.path.basename(sys.argv[1])[:-4], exist_ok=True)

with open("%s/chapternames.json" % os.path.basename(sys.argv[1])[:-4], "w", encoding="UTF-8") as chapter_names:
	json.dump(Filenames, chapter_names, indent="\t", ensure_ascii=False)

for i in range(0, file_count):
	file.seek(file_table['offset'][i], 0)
	file_new = open("%s/new/%s.dat" % (os.path.basename(sys.argv[1])[:-4], Filenames[i]), "wb")
	file_new.write(file.read(file_table['size'][i]))
	file_new.close()

for i in range(0, len(Filenames)):
	EXCEPTIONS = ["_VOICE_PARAM", "_VARNUM", "_SCR_LABEL", "_CGMODE", "_BUILD_COUNT"]
	if (Filenames[i] in EXCEPTIONS): 
		print("%s in EXCEPTIONS. Ignoring..." % (Filenames[i]))
		continue
	print(Filenames[i])
	file = open("%s/new/%s.dat" % (os.path.basename(sys.argv[1])[:-4], Filenames[i]), "rb")
	file.seek(0, 2)
	file_size = file.tell()
	file.seek(0, 0)
	if (Filenames[i] == "_TASK"):
		taskDecompile(file, file_size)
	else:
		while (file.tell() < file_size):
			command_size = numpy.fromfile(file, dtype=numpy.uint16, count=1)[0]
			GOTO_COMMANDS(numpy.fromfile(file, dtype=numpy.uint8, count=1)[0], int(numpy.fromfile(file, dtype=numpy.uint8, count=1)[0]), file, command_size)
			end = file.tell()
			if (end % 2 != 0):
				file.seek(1, 1)
	file.close()
	new_file = open("%s/json/%s.json" % (os.path.basename(sys.argv[1])[:-4], Filenames[i]), "w", encoding="UTF-8")
	json.dump(Dump['Main'], new_file, indent="\t", ensure_ascii=False)
	new_file.close()
	Dump['Main'] = []