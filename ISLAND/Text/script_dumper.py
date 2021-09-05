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
    WAIT_BSKIP = 0x45
    DRAW = 0x46
    WIPE = 0x47
    FRAMEON = 0x48
    FRAMEOFF = 0x49
    FW = 0x4A
    SCISSOR = 0x4B
    DELAY = 0x4C
    RASTER = 0x4D
    TONE = 0x4E
    SCALECOSSIN = 0x4F
    BMODE = 0x50
    SIZE = 0x51
    SPLINE = 0x52
    DISP = 0x53
    MASK = 0x54
    FACE = 0x55
    SEPIA = 0x56
    SEPIA_COLOR = 0x57
    CUSTOMMOVE = 0x58
    SWAP = 0x59
    ADDCOLOR = 0x5A
    SUBCOLOR = 0x5B
    SATURATION = 0x5C
    CONTRAST = 0x5D
    PRIORITY = 0x5E
    UVWH = 0x5F
    EVSCROLL = 0x60
    COLORLEVEL = 0x61
    NEGA = 0x62
    TONECURVE = 0x63
    QUAKE = 0x64
    BGM = 0x65
    BGM_WAITSTART = 0x66
    BGM_WAITFADE = 0x67
    BGM_PUSH = 0x68
    BGM_POP = 0x69
    SE = 0x6A
    SE_STOP = 0x6B
    SE_WAIT = 0x6C
    SE_WAIT_COUNT = 0x6D
    VOLUME = 0x6E
    MOVIE = 0x6F
    SETCGFLAG = 0x70
    EX = 0x71
    TROPHY = 0x72
    SETBGMFLAG = 0x73
    TASK = 0x74
    PRINTF = 0x75
    VIB_PLAY = 0x76
    VIB_FILE = 0x77
    VIB_STOP = 0x78
    MANPU = 0x79

def EQU(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "EQU"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def EQUN(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "EQUN"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def VARSTR(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "VARSTR"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

# Jumps to offset in the same file.
def GOTO(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "GOTO"
    entry['SUBCMD'] = SUBCMD
    if (SUBCMD == 1): 
        entry['Args'] = (file.read(2)[::-1].hex())
        entry['GOTO_LABEL'] = "0x%s" % (file.read(argsize-2)[::-1].hex())
    else: entry['GOTO_LABEL'] = "0x%s" % (file.read(argsize)[::-1].hex())
    MAIN_ENTRY.append(entry)

def ONGOTO(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "ONGOTO"
    entry['SUBCMD'] = SUBCMD
    entry['Fun_ARGS'] = "%s" % (file.read(2))
    string_size = numpy.fromfile(file, dtype=numpy.int16, count=1)[0]
    entry['Variable'] = "%s" % (file.read(abs(string_size)).decode("ascii").strip("\x00"))
    file.seek(8 - abs(string_size), 1)
    entry['GOTO_LABEL_0'] = "0x%s" % (file.read(4)[::-1].hex())
    argsize -= 16
    if (argsize > 0):
        entry['Args1'] = "%s" % (file.read(2))
        entry['GOTO_LABEL_1'] = "0x%s" % (file.read(4)[::-1].hex())
        argsize -= 6
        if (argsize > 0):
            entry['Args2'] = "%s" % (file.read(2))
            entry['GOTO_LABEL_2'] = "0x%s" % (file.read(4)[::-1].hex())
            argsize -= 6
            if (argsize > 0):
                entry['Args3'] = "%s" % (file.read(2))
                entry['GOTO_LABEL_3'] = "0x%s" % (file.read(4)[::-1].hex())
                argsize -= 6
                if (argsize > 0):
                    print("WHAAAT")
                    input("ENTER")
                    sys.exit()
    MAIN_ENTRY.append(entry)

def IFN(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "IFN"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

# JUMP is used to go to new file. As part of Args contains name of script file (f.e. "com02").
def JUMP(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "JUMP"
    entry['SUBCMD'] = SUBCMD
    if (SUBCMD == 1): entry['Args'] = "%s" % (file.read(2))
    string_size = numpy.fromfile(file, dtype=numpy.int16, count=1)[0]
    entry['Name'] = file.read(abs(string_size)).decode("ascii")
    file.seek(1, 1)
    if (SUBCMD == 1): entry['Args2'] = "%s" % (file.read(argsize - (abs(string_size)+1+4)))
    elif (SUBCMD == 0): entry['Args2'] = "%s" % (file.read(argsize - (abs(string_size)+1+2)))
    MAIN_ENTRY.append(entry)

def JUMPPOINT(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "JUMPPOINT"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def END(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "END"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def STARTUP_BETGIN(MAIN_ENTRY):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "STARTUP_BETGIN"
    MAIN_ENTRY.append(entry)

def STARTUP_END(MAIN_ENTRY):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "STARTUP_END"
    MAIN_ENTRY.append(entry)

def VARSTR_SET(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "VARSTR_SET"
    entry['SUBCMD'] = SUBCMD
    entry["Metadata"] = "%s" % (file.read(4))
    string_size = (numpy.fromfile(file, dtype=numpy.uint16, count=1)[0] + 1) * 2
    entry["String"] = file.read(string_size)[:-2].decode("UTF-16-LE")
    MAIN_ENTRY.append(entry)

def ARFLAGSET(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "ARFLAGSET"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def COLORBG_SET(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "COLORBG_SET"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SHAKELIST_SET(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SHAKELIST_SET"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def MESSAGE(SUBCMD, MAIN_ENTRY, file, argsize):
    SUBCMD2_EXCEPTIONS = [0x14, 0xB, 0x3]
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "MESSAGE"   
    entry['SUBCMD'] = SUBCMD
    SUBCMD2 = int(numpy.fromfile(file, dtype=numpy.uint16, count=1)[0])
    entry['SUBCMD2'] = SUBCMD2
    if ((SUBCMD2 >= 0xFF00) or (SUBCMD2 in SUBCMD2_EXCEPTIONS)):
        entry['Args'] = "%s" % (file.read(argsize-2))
    else:
        entry['MSGID'] = int(numpy.fromfile(file, dtype=numpy.uint16, count=1)[0])
        temp_numb = int(numpy.fromfile(file, dtype=numpy.uint16, count=1)[0])
        if (temp_numb != 0): entry['VOICEID'] = temp_numb
        string_size = numpy.fromfile(file, dtype=numpy.int16, count=1)[0]
        if (string_size == 0):
            file.seek(-6, 1)
            entry['Args'] = "%s" % (file.read(argsize-2))
        else:
            temp_size = 0
            if (string_size > 0):
                string_size = string_size * 2
                entry['JPN'] = file.read(string_size).decode("UTF-16-LE")
                file.seek(2, 1)
                temp_size += string_size + 2
            else:
                entry['JPN'] = file.read(string_size).decode("UTF-8")
                file.seek(1, 1)
                temp_size += abs(string_size) + 1
            string_size = numpy.fromfile(file, dtype=numpy.int16, count=1)[0]
            if (string_size > 0): 
                string_size = string_size * 2
                entry['ENG'] = file.read(string_size).decode("UTF-16-LE")
                file.seek(2, 1)
                temp_size += string_size + 2
            else:
                string = file.read(abs(string_size))
                entry['ENG'] = string.decode("UTF-8")
                file.seek(1, 1)
                temp_size += abs(string_size) + 1
            entry['Args'] = "%s" % (file.read(argsize - temp_size - 10))
    MAIN_ENTRY.append(entry)

def MESSAGE_CLEAR(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "MESSAGE_CLEAR"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def CLOSE_WINDOW(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "CLOSE_WINDOW"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SELECT(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SELECT"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(9))
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
        string_size = numpy.fromfile(file, dtype=numpy.int16, count=1)[0]
        if (string_size > 0): 
            string_size = string_size * 2
            entry['ENG'] = file.read(string_size).decode("UTF-16-LE").split("$d", -1)
            file.seek(2, 1)
            temp_size += string_size + 2
        else:
            entry['ENG'] = file.read(string_size).decode("UTF-8").split("$d", -1)
            file.seek(1, 1) 
            temp_size += string_size + 1       
    entry['Args2'] = "%s" % (file.read(argsize - 14 - temp_size))
    MAIN_ENTRY.append(entry)

def FFSTOP(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "FFSTOP"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def STOP(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "STOP"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def IMAGELOAD(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "IMAGELOAD"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def IMAGEUPDATE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "IMAGEUPDATE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def ARC(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "ARC"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def FADE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "FADE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def MOVE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "MOVE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def ROT(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "ROT"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SCALE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SCALE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SHAKE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SHAKE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SHAKELIST(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SHAKELIST"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def MCMOVE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "MCMOVE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def BASE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "BASE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def INIT(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "INIT"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def MCFADE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "MCFADE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def MCARC(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "MCARC"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)
    
def MCSHAKE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "MCSHAKE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def WAIT(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "WAIT"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def WAIT_BSKIP(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "WAIT_BSKIP"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def DRAW(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "DRAW"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def PRIORITY(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "PRIORITY"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def QUAKE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "QUAKE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def BGM_POP(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "BGM_POP"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def WIPE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "WIPE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SCISSOR(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SCISSOR"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def DELAY(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "DELAY"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def TONE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "TONE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SCALECOSSIN(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SCALECOSSIN"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def BMODE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "BMODE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SIZE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SIZE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def DISP(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "DISP"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SEPIA(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SEPIA"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SEPIA_COLOR(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SEPIA_COLOR"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SATURATION(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SATURATION"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def UVWH(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "UVWH"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def NEGA(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "NEGA"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def BGM(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "BGM"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SE_WAIT_COUNT(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SE_WAIT_COUNT"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def VOLUME(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "VOLUME"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SETBGMFLAG(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SETBGMFLAG"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def SETCGFLAG(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "SETCGFLAG"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def MOVIE(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "MOVIE"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def EX(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "EX"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def TASK(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "TASK"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def VIB_PLAY(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "VIB_PLAY"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def MANPU(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "MANPU"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = "%s" % (file.read(argsize))
    MAIN_ENTRY.append(entry)

def GOTO_COMMANDS(CMD, SUBCMD, file,cmdsize):
    SUBCMD = int(SUBCMD)
    if (CMD == Commands.EQU.value): EQU(SUBCMD, Dump['Main'], file, cmdsize-4) #0x0
    elif (CMD == Commands.EQUN.value): EQUN(SUBCMD, Dump['Main'], file, cmdsize-4) #0x1
    elif (CMD == Commands.VARSTR.value): VARSTR(SUBCMD, Dump['Main'], file, cmdsize-4) #0xB
    elif (CMD == Commands.GOTO.value): GOTO(SUBCMD, Dump['Main'], file, cmdsize-4) #0xF
    elif (CMD == Commands.ONGOTO.value): ONGOTO(SUBCMD, Dump['Main'], file, cmdsize-4) #0x10
    elif (CMD == Commands.IFN.value): IFN(SUBCMD, Dump['Main'], file, cmdsize-4) #0x13
    elif (CMD == Commands.JUMP.value): JUMP(SUBCMD, Dump['Main'], file, cmdsize-4) #0x15
    elif (CMD == Commands.JUMPPOINT.value): JUMPPOINT(SUBCMD, Dump['Main'], file, cmdsize-4) #0x18
    elif (CMD == Commands.END.value): END(SUBCMD, Dump['Main'], file, cmdsize-4) #0x19
    elif (CMD == Commands.STARTUP_BETGIN.value): STARTUP_BETGIN(Dump['Main']) #0x1A
    elif (CMD == Commands.STARTUP_END.value): STARTUP_END(Dump['Main']) #0x1B
    elif (CMD == Commands.VARSTR_SET.value): VARSTR_SET(SUBCMD, Dump['Main'], file, cmdsize-4) #0x1C
    elif (CMD == Commands.ARFLAGSET.value): ARFLAGSET(SUBCMD, Dump['Main'], file, cmdsize-4) #0x1E
    elif (CMD == Commands.COLORBG_SET.value): COLORBG_SET(SUBCMD, Dump['Main'], file, cmdsize-4) #0x1F
    elif (CMD == Commands.SHAKELIST_SET.value): SHAKELIST_SET(SUBCMD, Dump['Main'], file, cmdsize-4) #0x21
    elif (CMD == Commands.MESSAGE.value): MESSAGE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x23
    elif (CMD == Commands.MESSAGE_CLEAR.value): MESSAGE_CLEAR(SUBCMD, Dump['Main'], file, cmdsize-4) #0x24
    elif (CMD == Commands.SELECT.value): SELECT(SUBCMD, Dump['Main'], file, cmdsize-4) #0x26
    elif (CMD == Commands.CLOSE_WINDOW.value): CLOSE_WINDOW(SUBCMD, Dump['Main'], file, cmdsize-4) #0x27
    elif (CMD == Commands.FFSTOP.value): FFSTOP(SUBCMD, Dump['Main'], file, cmdsize-4) #0x31
    elif (CMD == Commands.INIT.value): INIT(SUBCMD, Dump['Main'], file, cmdsize-4) #0x32
    elif (CMD == Commands.STOP.value): STOP(SUBCMD, Dump['Main'], file, cmdsize-4) #0x33
    elif (CMD == Commands.IMAGELOAD.value): IMAGELOAD(SUBCMD, Dump['Main'], file, cmdsize-4) #0x34
    elif (CMD == Commands.IMAGEUPDATE.value): IMAGEUPDATE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x35
    elif (CMD == Commands.ARC.value): ARC(SUBCMD, Dump['Main'], file, cmdsize-4) #0x36
    elif (CMD == Commands.MOVE.value): MOVE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x37
    elif (CMD == Commands.ROT.value): ROT(SUBCMD, Dump['Main'], file, cmdsize-4) #0x38
    elif (CMD == Commands.FADE.value): FADE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x3A
    elif (CMD == Commands.SCALE.value): SCALE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x3B
    elif (CMD == Commands.SHAKE.value): SHAKE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x3C
    elif (CMD == Commands.SHAKELIST.value): SHAKELIST(SUBCMD, Dump['Main'], file, cmdsize-4) #0x3D
    elif (CMD == Commands.BASE.value): BASE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x3E
    elif (CMD == Commands.MCMOVE.value): MCMOVE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x3F
    elif (CMD == Commands.MCARC.value): MCARC(SUBCMD, Dump['Main'], file, cmdsize-4) #0x40
    elif (CMD == Commands.MCSHAKE.value): MCSHAKE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x42
    elif (CMD == Commands.MCFADE.value): MCFADE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x43
    elif (CMD == Commands.WAIT.value): WAIT(SUBCMD, Dump['Main'], file, cmdsize-4) #0x44
    elif (CMD == Commands.DRAW.value): DRAW(SUBCMD, Dump['Main'], file, cmdsize-4) #0x46
    elif (CMD == Commands.WIPE.value): WIPE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x47
    elif (CMD == Commands.SCISSOR.value): SCISSOR(SUBCMD, Dump['Main'], file, cmdsize-4) #0x4B
    elif (CMD == Commands.DELAY.value): DELAY(SUBCMD, Dump['Main'], file, cmdsize-4) #0x4C
    elif (CMD == Commands.TONE.value): SCISSOR(SUBCMD, Dump['Main'], file, cmdsize-4) #0x4E
    elif (CMD == Commands.SCALECOSSIN.value): SCALECOSSIN(SUBCMD, Dump['Main'], file, cmdsize-4) #0x4F
    elif (CMD == Commands.BMODE.value): BMODE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x50
    elif (CMD == Commands.SIZE.value): SIZE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x51
    elif (CMD == Commands.DISP.value): DISP(SUBCMD, Dump['Main'], file, cmdsize-4) #0x53
    elif (CMD == Commands.SEPIA.value): SEPIA(SUBCMD, Dump['Main'], file, cmdsize-4) #0x57
    elif (CMD == Commands.SEPIA_COLOR.value): SEPIA_COLOR(SUBCMD, Dump['Main'], file, cmdsize-4) #0x57
    elif (CMD == Commands.SATURATION.value): SATURATION(SUBCMD, Dump['Main'], file, cmdsize-4) #0x5C
    elif (CMD == Commands.UVWH.value): UVWH(SUBCMD, Dump['Main'], file, cmdsize-4) #0x5f
    elif (CMD == Commands.NEGA.value): NEGA(SUBCMD, Dump['Main'], file, cmdsize-4) #0x62
    elif (CMD == Commands.BGM.value): BGM(SUBCMD, Dump['Main'], file, cmdsize-4) #0x65
    elif (CMD == Commands.SE.value): SE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x6A
    elif (CMD == Commands.VOLUME.value): VOLUME(SUBCMD, Dump['Main'], file, cmdsize-4) #0x6E
    elif (CMD == Commands.MOVIE.value): MOVIE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x6E
    elif (CMD == Commands.SETBGMFLAG.value): SETBGMFLAG(SUBCMD, Dump['Main'], file, cmdsize-4) #0x6E
    elif (CMD == Commands.SETCGFLAG.value): SETCGFLAG(SUBCMD, Dump['Main'], file, cmdsize-4) #0x70
    elif (CMD == Commands.EX.value): EX(SUBCMD, Dump['Main'], file, cmdsize-4) #0x71
    elif (CMD == Commands.TASK.value): TASK(SUBCMD, Dump['Main'], file, cmdsize-4) #0x74
    elif (CMD == Commands.VIB_PLAY.value): VIB_PLAY(SUBCMD, Dump['Main'], file, cmdsize-4) #0x76
    elif (CMD == Commands.MANPU.value): MANPU(SUBCMD, Dump['Main'], file, cmdsize-4) #0x79
    else: 
        print("Not implemented command: 0x%x, offset: %x" % (CMD, file.tell()-2))
        input("Press ENTER")
        sys.exit()

try:
    os.mkdir("json")
except:
    pass

Filenames = []

with open("chapternames.txt", 'r', encoding="ascii") as f:
    Filenames = [line.strip("\r\n").strip("\n").split("\t", -1)[0] for line in f]

for i in range(0, len(Filenames)):
    EXCEPTIONS = ["_varstr", "_arflag", "_colorbg", "_shakelist"]
    if (Filenames[i][0] == "_"): 
        if (Filenames[i] not in EXCEPTIONS):
            print("%s not in EXCEPTIONS. Ignoring..." % (Filenames[i]))
            continue
    print(Filenames[i])
    file = open("new\%s.dat" % (Filenames[i]), "rb")
    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0, 0)
    while (file.tell() < file_size):
        command_size = numpy.fromfile(file, dtype=numpy.uint16, count=1)[0]
        GOTO_COMMANDS(numpy.fromfile(file, dtype=numpy.uint8, count=1)[0], numpy.fromfile(file, dtype=numpy.uint8, count=1)[0], file, command_size)
        end = file.tell()
        if (end % 2 != 0):
            file.seek(2 - (end % 2), 1)
    file.close()
    new_file = open("json\%s.json" % (Filenames[i]), "w", encoding="UTF-8")
    json.dump(Dump, new_file, indent=4, ensure_ascii=False)
    new_file.close()
    Dump['Main'] = []