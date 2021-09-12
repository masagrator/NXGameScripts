import numpy
import json
import os
import sys
import base64
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
    SCENARIO = 0x7A
    HAIKEI_SET = 0x7B
    FULLQUAKE_ZOOM = 0x7C
    DEL_CALLSTACK = 0x7D
    KEOP = 0x7E

def EQU(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "EQU"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = file.read(argsize).hex()
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
        entry['GOTO_LABEL'] = "%s" % hex(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0])
    else: entry['GOTO_LABEL'] = "%s" % hex(numpy.fromfile(file, dtype=numpy.uint32, count=1)[0])
    MAIN_ENTRY.append(entry)

def IFN(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "IFN"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = file.read(argsize).hex()
    MAIN_ENTRY.append(entry)

# JUMP is used to go to new file. As part of Args contains name of script file (f.e. "com02").
def JUMP(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "JUMP"
    entry['SUBCMD'] = SUBCMD
    if (SUBCMD == 1): entry['Args'] = file.read(2).hex()
    string_size = numpy.fromfile(file, dtype=numpy.int16, count=1)[0]
    entry['Name'] = file.read(abs(string_size)).decode("ascii")
    file.seek(1, 1)
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
            if (text[0] == "@"):
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
            file.seek(2, 1)
            temp_size += string_size + 2
        else:
            text = file.read(string_size).decode("UTF-8")
            if (text[0] == "@"):
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
    if (string_size > 0):
        string_size = string_size * 2
        entry['JPN'] = file.read(string_size).decode("UTF-16-LE")
        file.seek(2, 1)
    elif (string_size < 0):
        entry['JPN'] = file.read(string_size).decode("UTF-8")
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
    if (SUBCMD > 0):
        entry['Args'] = file.read(argsize).hex()
    MAIN_ENTRY.append(entry)

def DRAW(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "DRAW"
    entry['SUBCMD'] = SUBCMD
    if (argsize > 0):
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

def PRINTF(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "PRINTF"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = file.read(argsize).hex()
    MAIN_ENTRY.append(entry)

def VIB_PLAY(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "VIB_PLAY"
    entry['SUBCMD'] = SUBCMD
    entry['Args'] = file.read(argsize).hex()
    MAIN_ENTRY.append(entry)

def DEL_CALLSTACK(SUBCMD, MAIN_ENTRY, file, argsize):
    entry = {}
    entry['LABEL'] = "%s" % (hex(file.tell()-4))
    entry['Type'] = "DEL_CALLSTACK"
    entry['SUBCMD'] = SUBCMD
    MAIN_ENTRY.append(entry)

def GOTO_COMMANDS(CMD, SUBCMD, file,cmdsize):
    if (CMD == Commands.EQU.value): EQU(SUBCMD, Dump['Main'], file, cmdsize-4) #0x0 //
    elif (CMD == Commands.EQUN.value): EQUN(SUBCMD, Dump['Main'], file, cmdsize-4) #0x1 //
    elif (CMD == Commands.VARSTR.value): VARSTR(SUBCMD, Dump['Main'], file, cmdsize-4) #0xB //
    elif (CMD == Commands.GOTO.value): GOTO(SUBCMD, Dump['Main'], file, cmdsize-4) #0xF //
    elif (CMD == Commands.IFN.value): IFN(SUBCMD, Dump['Main'], file, cmdsize-4) #0x13 //
    elif (CMD == Commands.JUMP.value): JUMP(SUBCMD, Dump['Main'], file, cmdsize-4) #0x15 //
    elif (CMD == Commands.JUMPPOINT.value): JUMPPOINT(SUBCMD, Dump['Main'], file, cmdsize-4) #0x18 //
    elif (CMD == Commands.END.value): END(SUBCMD, Dump['Main'], file, cmdsize-4) #0x19 //
    elif (CMD == Commands.STARTUP_BETGIN.value): STARTUP_BETGIN(Dump['Main']) #0x1A //
    elif (CMD == Commands.STARTUP_END.value): STARTUP_END(Dump['Main']) #0x1B //
    elif (CMD == Commands.VARSTR_SET.value): VARSTR_SET(SUBCMD, Dump['Main'], file, cmdsize-4) #0x1C //
    elif (CMD == Commands.ARFLAGSET.value): ARFLAGSET(SUBCMD, Dump['Main'], file, cmdsize-4) #0x1E //
    elif (CMD == Commands.SHAKELIST_SET.value): SHAKELIST_SET(SUBCMD, Dump['Main'], file, cmdsize-4) #0x21 //
    elif (CMD == Commands.MESSAGE.value): MESSAGE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x23 //
    elif (CMD == Commands.SELECT.value): SELECT(SUBCMD, Dump['Main'], file, cmdsize-4) #0x26 //
    elif (CMD == Commands.CLOSE_WINDOW.value): CLOSE_WINDOW(SUBCMD, Dump['Main'], file, cmdsize-4) #0x27 //
    elif (CMD == Commands.LOG.value): LOG(SUBCMD, Dump['Main'], file, cmdsize-4) #0x29 //
    elif (CMD == Commands.LOG_END.value): LOG_END(SUBCMD, Dump['Main'], file, cmdsize-4) #0x2B //
    elif (CMD == Commands.FFSTOP.value): FFSTOP(SUBCMD, Dump['Main'], file, cmdsize-4) #0x31 //
    elif (CMD == Commands.INIT.value): INIT(SUBCMD, Dump['Main'], file, cmdsize-4) #0x32 //
    elif (CMD == Commands.STOP.value): STOP(SUBCMD, Dump['Main'], file, cmdsize-4) #0x33 //
    elif (CMD == Commands.IMAGELOAD.value): IMAGELOAD(SUBCMD, Dump['Main'], file, cmdsize-4) #0x34 //
    elif (CMD == Commands.MOVE.value): MOVE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x37 //
    elif (CMD == Commands.FADE.value): FADE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x3A //
    elif (CMD == Commands.SHAKELIST.value): SHAKELIST(SUBCMD, Dump['Main'], file, cmdsize-4) #0x3D //
    elif (CMD == Commands.WAIT.value): WAIT(SUBCMD, Dump['Main'], file, cmdsize-4) #0x44 //
    elif (CMD == Commands.DRAW.value): DRAW(SUBCMD, Dump['Main'], file, cmdsize-4) #0x46 //
    elif (CMD == Commands.BGM_WAITFADE.value): BGM_WAITFADE(SUBCMD, Dump['Main'], file, cmdsize-4) #0x67 //
    elif (CMD == Commands.BGM_POP.value): BGM_POP(SUBCMD, Dump['Main'], file, cmdsize-4) #0x69 //
    elif (CMD == Commands.SE_WAIT.value): SE_WAIT(SUBCMD, Dump['Main'], file, cmdsize-4) #0x6C //
    elif (CMD == Commands.EX.value): EX(SUBCMD, Dump['Main'], file, cmdsize-4) #0x71 //
    elif (CMD == Commands.PRINTF.value): PRINTF(SUBCMD, Dump['Main'], file, cmdsize-4) #0x75 //
    elif (CMD == Commands.VIB_PLAY.value): VIB_PLAY(SUBCMD, Dump['Main'], file, cmdsize-4) #0x76 //
    elif (CMD == Commands.DEL_CALLSTACK.value): DEL_CALLSTACK(SUBCMD, Dump['Main'], file, cmdsize-4) #0x7D //
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
        GOTO_COMMANDS(numpy.fromfile(file, dtype=numpy.uint8, count=1)[0], int(numpy.fromfile(file, dtype=numpy.uint8, count=1)[0]), file, command_size)
        end = file.tell()
        if (end % 2 != 0):
            file.seek(2 - (end % 2), 1)
    file.close()
    new_file = open("json\%s.json" % (Filenames[i]), "w", encoding="UTF-8")
    json.dump(Dump, new_file, indent=4, ensure_ascii=False)
    new_file.close()
    Dump['Main'] = []