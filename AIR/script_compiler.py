import json
import os
import sys
from enum import Enum

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

def EQU(entry):
    array = []
    array.append(Commands.EQU.value.to_bytes(1, byteorder='little'))
    array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
    array.append(bytes.fromhex(entry['Args']))
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
    return b''.join(array)

def GOTO(entry, string):
    array = []
    array.append(Commands.GOTO.value.to_bytes(1, byteorder='little'))
    array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
    if (entry['SUBCMD'] == 1):
        array.append(bytes.fromhex(entry['Args']))
        if (string == "COMMAND"):
            array.append(LABELS[entry['GOTO_LABEL']].to_bytes(4, byteorder='little'))
        else: array.append(int(entry['GOTO_LABEL'], 16).to_bytes(4, byteorder='little'))
    else: 
        if (string == "COMMAND"):
            array.append(LABELS[entry['GOTO_LABEL']].to_bytes(4, byteorder='little'))
        else: array.append(int(entry['GOTO_LABEL'], 16).to_bytes(4, byteorder='little'))
    return b''.join(array)

def IFN(entry, string):
    array = []
    array.append(Commands.IFN.value.to_bytes(1, byteorder='little'))
    array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
    array.append(bytes.fromhex(entry['Args']))
    if (string == "COMMAND"):
        array.append(LABELS[entry['GOTO_LABEL']].to_bytes(4, byteorder='little'))
    else: array.append(int(entry['GOTO_LABEL'], 16).to_bytes(4, byteorder='little'))
    return b''.join(array)

def JUMP(entry):
    array = []
    array.append(Commands.JUMP.value.to_bytes(1, byteorder='little'))
    array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
    if (entry['SUBCMD'] == 1):
        array.append(bytes.fromhex(entry['Args']))
    array.append((0x10000 - len(entry['Name'].encode('ascii'))).to_bytes(2, byteorder='little'))
    array.append(entry['Name'].encode('ascii'))
    array.append(b"\x00")
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

def STARTUP_BETGIN(entry):
    array = []
    array.append(Commands.STARTUP_BETGIN.value.to_bytes(1, byteorder='little'))
    array.append(b"\x00")
    return b''.join(array)

def STARTUP_END(entry):
    array = []
    array.append(Commands.STARTUP_END.value.to_bytes(1, byteorder='little'))
    array.append(b"\x00")
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
    if (ENG == False):
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
        if (ENG == False): Name = ("@%s@" % (entry['NameJPN'])).encode("UTF-16-LE")
        else: Name = ("@%s@" % (entry['NameENG'])).encode("UTF-16-LE")
    except:
        pass
    try:
        if (ENG == False): Text = entry["JPN"].encode("UTF-16-LE")
        else: Text = entry["ENG"].encode("UTF-16-LE")
    except:
        array.append(bytes.fromhex(entry['Args']))
        return b''.join(array)
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
        else:
            temp += len(entry['ENG'][i].encode("UTF-16-LE"))
            string.extend(entry['ENG'][i].encode("UTF-16-LE"))
        if (i != (len(entry['JPN']) - 1)): 
            temp += 4
            string.extend("\x24\x64".encode("UTF-16-LE"))
    array.append(int(temp / 2).to_bytes(2, byteorder='little'))
    array.append(string)
    array.append(b"\x00\x00")
    array.append(int(entry['LongBar']).to_bytes(1, byteorder='little'))
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
    if (ENG == False):
        size = len(entry['JPN'].encode("UTF-16-LE"))
        array.append(int(size / 2).to_bytes(2, byteorder='little'))
        array.append(entry['JPN'].encode("UTF-16-LE"))
    else:
        size = len(entry['ENG'].encode("UTF-16-LE"))
        array.append(int(size / 2).to_bytes(2, byteorder='little'))
        array.append(entry['ENG'].encode("UTF-16-LE"))       
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
    try:
        array.append(bytes.fromhex(entry['Args']))
    except:
        pass
    return b''.join(array)

def DRAW(entry):
    array = []
    array.append(Commands.DRAW.value.to_bytes(1, byteorder='little'))
    array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
    try:
        array.append(bytes.fromhex(entry['Args']))
    except:
        pass
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

def PRINTF(entry):
    array = []
    array.append(Commands.PRINTF.value.to_bytes(1, byteorder='little'))
    array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
    array.append(bytes.fromhex(entry['Args']))
    return b''.join(array)

def VIB_PLAY(entry):
    array = []
    array.append(Commands.VIB_PLAY.value.to_bytes(1, byteorder='little'))
    array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
    array.append(bytes.fromhex(entry['Args']))
    return b''.join(array)

def DEL_CALLSTACK(entry):
    array = []
    array.append(Commands.DEL_CALLSTACK.value.to_bytes(1, byteorder='little'))
    array.append(entry['SUBCMD'].to_bytes(1, byteorder='little'))
    return b''.join(array)

def Make_command(entry, string):
    match (entry['Type']):
        case "EQU": return EQU(entry)
        case "EQUN": return EQUN(entry)
        case "VARSTR": return VARSTR(entry)
        case "GOTO": return GOTO(entry, string)
        case "IFN": return IFN(entry, string)
        case "JUMP": return JUMP(entry)
        case "JUMPPOINT": return JUMPPOINT(entry)
        case "END": return END(entry)
        case "STARTUP_BETGIN": return STARTUP_BETGIN(entry)
        case "STARTUP_END": return STARTUP_END(entry)
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
        case "FADE": return FADE(entry)
        case "SHAKELIST": return SHAKELIST(entry)
        case "WAIT": return WAIT(entry)
        case "DRAW": return DRAW(entry)
        case "BGM_WAITFADE": return BGM_WAITFADE(entry)
        case "BGM_POP": return BGM_POP(entry)
        case "SE_WAIT": return SE_WAIT(entry)
        case "EX": return EX(entry)
        case "PRINTF": return PRINTF(entry)
        case "VIB_PLAY": return VIB_PLAY(entry)
        case "DEL_CALLSTACK": return DEL_CALLSTACK(entry)
        case _:
            print("Type not supported: %s" % (entry['Type']))
            sys.exit()

def Process(string, entry, offset_new):
    match (string):
        case "SIZE":
            _COM = Make_command(entry, string)
            LABELS[entry['LABEL']] = offset_new
            return len(_COM)
        case "COMMAND":
            return Make_command(entry, string)
        case _:
            print("Unsupported Process command: %s" % (string))
            sys.exit()

if (len(sys.argv) != 2):
    print("script_compiler.py [ENG/JPN]")
    sys.exit()

if (sys.argv[1] == "ENG"): ENG = True
elif (sys.argv[1] != "JPN"):
    print("script_compiler.py [ENG/JPN]")
    sys.exit()

try:
    os.mkdir("Compiled")
except:
    pass

with open("chapternames.txt", 'r', encoding="ascii") as f:
    Filenames = [line.strip("\n").split("\t", -1)[0] for line in f]

for i in range(0, len(Filenames)):
    offset_new = 0
    EXCEPTIONS = ["_varstr", "_arflag", "_colorbg", "_shakelist"]
    if (Filenames[i][0] == "_"): 
        if (Filenames[i] not in EXCEPTIONS):
            print("%s not in EXCEPTIONS. Ignoring..." % (Filenames[i]))
            continue
    print(Filenames[i])
    file = open("json\%s.json" % (Filenames[i]), "r")
    DUMP = json.load(file)
    COMMAND_OUTPUT_SIZE = []
    file.close()
    for x in range(0, len(DUMP)):
        Size = Process("SIZE", DUMP[x], offset_new)
        if (Size % 2 != 0): Size += 1
        COMMAND_OUTPUT_SIZE.append(Size)
        offset_new += Size + 2
    file = open("Compiled\%s.dat" % (Filenames[i]), "wb")
    for x in range(0, len(DUMP)):
        COM = Process("COMMAND", DUMP[x], offset_new)
        file.write((len(COM)+2).to_bytes(2, byteorder='little'))
        file.write(COM)
        if (len(COM) % 2 != 0): file.write(b"\x00")