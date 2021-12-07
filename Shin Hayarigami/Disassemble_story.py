import glob
import json
import os
from types import ClassMethodDescriptorType
import numpy
import shutil
import sys
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
            return str(InvertString(b"".join(chars)).decode("shift_jis_2004"))
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
            return DEMO(F)
        case 2:
            return DEMOtm(F, argsize)
        case 3:
            return PAGE(F, argsize)
        case 4:
            return PAGEtm(F, argsize)
        case 99:
            return EXTEND(F, argsize)
        case 101:
            return JUMP(F)
        case 102:
            return SELECT(F, argsize)
        case 103:
            return SELECTtm(F, argsize)
        case 104:
            return SI(F, argsize)
        case 105:
            return SItm(F, argsize)
        case 106:
            return IF(F, argsize)
        case 107:
            return IFtm(F, argsize)
        case 108:
            return IFPARAM(F, argsize)
        case 109:
            return IFPARAMtm(F, argsize)
        case 112:
            return IFSTRING(F, argsize)
        case 113:
            return IFSTRINGtm(F, argsize)
        case 114:
            return IFRV(F, argsize)
        case 115:
            return IFRVtm(F, argsize)
        case 116:
            return SELECT_ITEM(F, argsize)
        case 117:
            return SELECT_ITEMtm(F, argsize)
        case 201:
            return WAIT(F, argsize)
        case 202:
            return BWAIT(F, argsize)
        case 203:
            return TWAIT(F, argsize)
        case 204:
            return BR(F, argsize) #Break Line
        case 205:
            return FONT(F, argsize)
        case 206:
            return FONTtm(F, argsize)
        case 207:
            return MSPEED(F, argsize)
        case 208:
            return RUBY(F, argsize)
        case 209:
            return RUBYtm(F, argsize)
        case 210:
            return TEXT_LEFT(F, argsize)
        case 211:
            return TEXT_RIGHT(F, argsize)
        case 212:
            return TEXT_TOP(F, argsize)
        case 213:
            return EMBED(F, argsize)
        case 214:
            return SPACE(F, argsize)
        case 215:
            return CURSOR(F, argsize)
        case 216:
            return TEXT_FADE(F, argsize)
        case 217:
            return ICON(F, argsize)
        case 218:
            return EMBED_PARAM(F, argsize)
        case 219:
            return TEXT_MODE(F, argsize)
        case 255:
            return NML(F, argsize)
        case 301:
            return WINDOW_ON(F, argsize)
        case 302:
            return WINDOW_OFF(F, argsize)
        case 303:
            return WINDOW_SIZE(F, argsize)
        case 304:
            return WINDOW_MOVE(F, argsize)
        case 305:
            return WINDOW_FADE(F, argsize)
        case 306:
            return TXTWND_IN(F, argsize)
        case 307:
            return TXTWND_OUT(F, argsize)
        case 401:
            return BG_LOAD(F, argsize)
        case 402:
            return BG_WAIT(F, argsize)
        case 403:
            return BG_FADE(F, argsize)
        case 404:
            return BG_COLOR(F, argsize)
        case 405:
            return BG_MOVE(F, argsize)
        case 406:
            return BG_SIZE(F, argsize)
        case 407:
            return BG_ST(F, argsize)
        case 410:
            return BG_SET_ADJUST_Z(F, argsize)
        case 501:
            return TX2_LOAD(F, argsize)
        case 502:
            return TX2_MOVE(F, argsize)
        case 503:
            return TX2_FADE(F, argsize)
        case 504:
            return TX2_SIZE(F, argsize)
        case 505:
            return TX2_ST(F, argsize)
        case 506:
            return TX2_COLOR(F, argsize)
        case 507:
            return TX2_ZGP(F, argsize)
        case 508:
            return TX2_CENTERING(F, argsize)
        case 509:
            return TX2_CTL_TRACK(F, argsize)
        case 550:
            return TX2_TRACK(F, argsize)
        case 551:
            return TX2_PACK_READ(F, argsize)
        case 552:
            return TX2_PACK_WAIT(F, argsize)
        case 601:
            return ANM_LOAD(F, argsize)
        case 602:
            return ANM_MOVE(F, argsize)
        case 603:
            return ANM_FADE(F, argsize)
        case 604:
            return ANM_SIZE(F, argsize)
        case 605:
            return ANM_PLAY(F, argsize)
        case 606:
            return ANM_SKIP(F, argsize)
        case 607:
            return ANM_STOP(F, argsize)
        case 651:
            return ANM_PACK_READ(F, argsize)
        case 652:
            return ANM_PACK_WAIT(F, argsize)
        case 701:
            return SCR_FADE(F, argsize)
        case 702:
            return SCR_VIB(F, argsize)
        case 801:
            return FLAG(F, argsize)
        case 802:
            return PARAM(F, argsize)
        case 803:
            return STRING(F, argsize)
        case 804:
            return PARAM_COMPARE(F, argsize)
        case 805:
            return STRING_COMPARE(F, argsize)
        case 806:
            return PARAM_COPY(F, argsize)
        case 807:
            return STRING_COPY(F, argsize)
        case 901:
            return SET_VOL(F, argsize)
        case 902:
            return BGM_READY(F, argsize)
        case 903:
            return BGM_WAIT(F, argsize)
        case 904:
            return BGM_PLAY(F, argsize)
        case 905:
            return BGM_VOL(F, argsize)
        case 906:
            return BGM_STOP(F, argsize)
        case 907:
            return MSG_READY(F, argsize)
        case 908:
            return MSG_WAIT(F, argsize)
        case 909:
            return MSG_PLAY(F, argsize)
        case 910:
            return MSG_VOL(F, argsize)
        case 911:
            return MSG_STOP(F, argsize)
        case 914:
            return SE_PLAY(F, argsize)
        case 915:
            return SE_VOL(F, argsize)
        case 916:
            return SE_STOP(F, argsize)
        case 917:
            return SE_ALL_STOP(F, argsize)
        case 918:
            return LOOPS_READY(F, argsize)
        case 919:
            return LOOPS_WAIT(F, argsize)
        case 920:
            return LOOPS_PLAY(F, argsize)
        case 921:
            return LOOPS_VOL(F, argsize)
        case 922:
            return LOOPS_STOP(F, argsize)
        case 923:
            return SONG_READY(F, argsize)
        case 924:
            return SONG_WAIT(F, argsize)
        case 925:
            return SONG_PLAY(F, argsize)
        case 926:
            return SONG_VOL(F, argsize)
        case 927:
            return SONG_STOP(F, argsize)
        case 931:
            return MSG_SYNC(F, argsize)
        case 932:
            return SONG_SYNC(F, argsize)
        case 1001:
            return EMBED_EDIT(F, argsize)
        case 1002:
            return TITLE_JUMP(F, argsize)
        case 1003:
            return DLOGIC(F, argsize)
        case 1004:
            return GRADE(F, argsize)
        case 1005:
            return LOGIC_INFER(F, argsize)
        case 1006:
            return SAVE_POINT(F, argsize)
        case 1101:
            return PAD_CTL(F, argsize)
        case 1102:
            return PAD_VIB(F, argsize)
        case 1103:
            return PAD_PUSH(F, argsize)
        case 1201:
            return CODE_3D_PLAY(F, argsize)
        case 1202:
            return CODE_3D_MOVE(F, argsize)
        case 1203:
            return CODE_3D_FADE(F, argsize)
        case 1204:
            return CODE_3D_ROTATE(F, argsize)
        case 1205:
            return CODE_3D_SIZE(F, argsize)
        case 1206:
            return CODE_3D_STOP(F, argsize)
        case 1251:
            return CODE_3D_PACK_READ(F, argsize)
        case 1252:
            return CODE_3D_PACK_WAIT(F, argsize)
        case 1261:
            return CODE_3D_CAMERA_SET(F, argsize)
        case 1301:
            return CALL_DEMO(F, argsize)
        case 1302:
            return WAIT_DEMO_ALL(F, argsize)
        case 1303:
            return OPTWND(F, argsize)
        case 1304:
            return RANDOM(F, argsize)
        case 1305:
            return READED_PCT(F, argsize)
        case 1306:
            return DENY_SKIP(F, argsize)
        case 1307:
            return BACKLOG_CLEAR(F, argsize)
        case 1308:
            return HIDE_SELECTER_MENU(F, argsize)
        case 1309:
            return HIDE_NAMEEDIT_MENU(F, argsize)
        case 1310:
            return YES_NO_DLG(F, argsize)
        case 1311:
            return STOP_SKIP(F, argsize)
        case 1312:
            return TXTHIDE_CTL(F, argsize)
        case 1313:
            return STOP_OTHER_DEMO(F, argsize)
        case 1314:
            return SUBMENU_CTL(F, argsize)
        case 1315:
            return SHORTCUT_CTL(F, argsize)
        case 1316:
            return NOVELCLEAR(F, argsize)
        case 1317:
            return PLAY_VIDEO(F, argsize) # Guessed
        case 1401:
            return PHRASE_SET(F, argsize)
        case 1402:
            return PHRASE_FADE(F, argsize)
        case 1403:
            return PHRASE_MOVE(F, argsize)
        case 1501:
            return NUMBER_SET(F, argsize)
        case 1502:
            return NUMBER_FADE(F, argsize)
        case 1503:
            return NUMBER_MOVE(F, argsize)
        case 1504:
            return NUMBER_SIZE(F, argsize)
        case 1505:
            return NUMBER_GET_PARAM(F, argsize)
        case 2001:
            return KEYWORD(F)
        case 2002:
            return GRADE_POINT(F, argsize)
        case 2003:
            return ADD_MEMO(F, argsize)
        case 2004:
            return LOGIC_MODE(F, argsize)
        case 2005:
            return LOGIC_SET_KEY(F, argsize)
        case 2006:
            return LOGIC_GET_KEY(F, argsize)
        case 2007:
            return LOGIC_CTL(F, argsize)
        case 2008:
            return LOGIC_LOAD(F, argsize)
        case 2009:
            return GAME_END(F, argsize)
        case 2010:
            return FACE(F, argsize)
        case 2011:
            return CHOOSE_KEYWORD(F, argsize)
        case 2012:
            return LOGIC_CLEAR_KEY(F, argsize)
        case 2013:
            return DATABASE(F, argsize)
        case 2014:
            return SPEAKER(F)
        case 2021:
            return LOGIC_SAVE(F, argsize)
        case 2022:
            return LOGIC_DRAW_MARK(F, argsize)
        case 2101:
            return DLPAGE(F, argsize)
        case 2102:
            return DLPAGEtm(F, argsize)
        case 2103:
            return DLKEY(F, argsize)
        case 2104:
            return DLSELSET(F, argsize)
        case 2105:
            return DLSELSETtm(F, argsize)
        case 2106:
            return DLSEL(F, argsize)
        case 2107:
            return DLSELECT(F, argsize)
        case 2108:
            return ILCAMERA(F, argsize)
        case 2109:
            return ILZOOM(F, argsize)
        case 2201:
            return CI_LOAD(F, argsize)
        case 2202:
            return CI_LOAD_WAIT(F, argsize)
        case 2203:
            return CI_MOVE(F, argsize)
        case 2204:
            return CI_FADE(F, argsize)
        case 2205:
            return CI_SIZE(F, argsize)
        case 2206:
            return CI_ST(F, argsize)
        case 2207:
            return CI_COLOR(F, argsize)
        case 2208:
            return CI_ZGP(F, argsize)
        case 2209:
            return CI_CENTERING(F, argsize)
        case 2210:
            return CI_CTL_TRACK(F, argsize)
        case 2211:
            return CI_TRACK(F, argsize)
        case 2212:
            return CI_NEGAPOSI(F, argsize)
        case 2213:
            return CI_BUSTUP_CENTERING(F, argsize)
        case 2301:
            return MCR_TEXT_TOP(F, argsize)
        case 2302:
            return MCR_RUBY(F, argsize)
        case 2303:
            return MCR_BG_START(F, argsize)
        case 2304:
            return MCR_BG_STOP(F, argsize)
        case 2305:
            return MCR_BU_START(F, argsize)
        case 2306:
            return MCR_BU_STOP(F, argsize)
        case 2307:
            return MCR_CI_START(F, argsize)
        case 2308:
            return MCR_CI_STOP(F, argsize)
        case 2309:
            return MCR_TEXTWIN_IN(F, argsize)
        case 2310:
            return MCR_TEXTWIN_OUT(F, argsize)
        case 2311:
            return MCR_3D_EFFECT(F, argsize)
        case 2312:
            return MCR_BGM_START(F, argsize)
        case 2313:
            return MCR_BGM_STOP(F, argsize)
        case 2314:
            return MCR_SE_START(F, argsize)
        case 2315:
            return MCR_LOOPVOICE_START(F, argsize)
        case 2316:
            return MCR_LOOPVOICE_STOP(F, argsize)
        case 2401:
            return ANIME_LOAD(F, argsize)
        case 2402:
            return ANIME_LOAD_WAIT(F, argsize)
        case 2403:
            return ANIME_PLAY(F, argsize)
        case 2404:
            return ANIME_SKIP(F, argsize)
        case 2405:
            return ANIME_STOP(F, argsize)
        case 2406:
            return ANIME_MOVE(F, argsize)
        case 2407:
            return ANIME_FADE(F, argsize)
        case 2408:
            return ANIME_SCALE(F, argsize)
        case 2409:
            return ANIME_ROT(F, argsize)
        case 2410:
            return ANIME_ZGP(F, argsize)
        case 2411:
            return ANIME_SYNC(F, argsize)
        case 2412:
            return ANIME_PAUSE(F, argsize)
        case 2413:
            return ANIME_RESUME(F, argsize)
        case 2414:
            return ANIME_FRAME(F, argsize)
        case 2501:
            return LIARSART_START(F, argsize)
        case 2502:
            return LIARSART_DEMOEND(F, argsize)
        case 2503:
            return LIARSART_END(F, argsize)
        case 2504:
            return LIARSART_TUTORIAL(F, argsize)
        case _:
            print("Unknown command! %d" % cmd)
            return None


file = open("story.dat", "rb")

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

os.makedirs("json", exist_ok=True)
for i in range(0, len(files)):
    file = open(files[i], "rb")
    ID = TakeID(file)
    print(ID)
    size = GetFileSize(file)
    file_new = open("json\%s.json" % ID, "w", encoding="UTF-8")
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
    json.dump(Dump, file_new, indent="\t", ensure_ascii=False)
    file.close()

#shutil.rmtree('extracted')