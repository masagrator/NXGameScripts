from sys import byteorder


def DEMO(F):
    entry = {}
    entry["TYPE"] = "DEMO"
    entry["UNK0"] = F.read(0x4).hex()
    entry["SCRIPT_ID"] = int.from_bytes(F.read(0x4), byteorder="little")
    entry["UNK1"] = F.read(0x4).hex()
    return entry

def DEMOtm(F, size):
    entry = {}
    entry["TYPE"] = "DEMOtm"
    entry["UNK0"] = F.read(size).hex()
    return entry

def PAGE(F, size):
    entry = {}
    entry["TYPE"] = "PAGE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def PAGEtm(F, size):
    entry = {}
    entry["TYPE"] = "PAGEtm"
    entry["UNK0"] = F.read(size).hex()
    return entry

def EXTEND(F, size):
    entry = {}
    entry["TYPE"] = "EXTEND"
    entry["UNK0"] = F.read(size).hex()
    return entry

def JUMP(F):
    entry = {}
    entry["TYPE"] = "JUMP"
    entry["UNK0"] = F.read(0x4).hex()
    entry["SCRIPT_ID"] = int.from_bytes(F.read(0x4), byteorder="little")
    return entry

def SELECT(F, size):
    entry = {}
    entry["TYPE"] = "SELECT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SELECTtm(F, size):
    entry = {}
    entry["TYPE"] = "SELECTtm"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SI(F, size):
    entry = {}
    entry["TYPE"] = "SI"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SItm(F, size):
    entry = {}
    entry["TYPE"] = "SItm"
    entry["UNK0"] = F.read(size).hex()
    return entry

def IF(F, size):
    entry = {}
    entry["TYPE"] = "IF"
    entry["UNK0"] = F.read(size).hex()
    return entry

def IFtm(F, size):
    entry = {}
    entry["TYPE"] = "IFtm"
    entry["UNK0"] = F.read(size).hex()
    return entry

def IFPARAM(F, size):
    entry = {}
    entry["TYPE"] = "IFPARAM"
    entry["UNK0"] = F.read(size).hex()
    return entry

def IFPARAMtm(F, size):
    entry = {}
    entry["TYPE"] = "IFPARAMtm"
    entry["UNK0"] = F.read(size).hex()
    return entry

def IFSTRING(F, size):
    entry = {}
    entry["TYPE"] = "IFSTRING"
    entry["UNK0"] = F.read(size).hex()
    return entry

def IFSTRINGtm(F, size):
    entry = {}
    entry["TYPE"] = "IFSTRINGtm"
    entry["UNK0"] = F.read(size).hex()
    return entry

def IFRV(F, size):
    entry = {}
    entry["TYPE"] = "IFRV"
    entry["UNK0"] = F.read(size).hex()
    return entry

def IFRVtm(F, size):
    entry = {}
    entry["TYPE"] = "IFRVtm"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SELECT_ITEM(F, selectdatabase = None):
    entry = {}
    entry["TYPE"] = "SELECT_ITEM"
    entry["UNK0"] = F.read(0x4).hex()
    entry["SELECT_ITEM_ID"] = int.from_bytes(F.read(0x2), byteorder="little")
    if (selectdatabase != None):
        entry["SELECT_ITEM_INFO"] = selectdatabase["%d" % entry["SELECT_ITEM_ID"]]
    entry["UNK1"] = F.read(0x4).hex()
    return entry

def SELECT_ITEMtm(F, size):
    entry = {}
    entry["TYPE"] = "SELECT_ITEMtm"
    entry["UNK0"] = F.read(size).hex()
    return entry

def WAIT(F, size):
    entry = {}
    entry["TYPE"] = "WAIT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BWAIT(F, size):
    entry = {}
    entry["TYPE"] = "BWAIT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TWAIT(F, size):
    entry = {}
    entry["TYPE"] = "TWAIT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BR(F, size):
    entry = {}
    entry["TYPE"] = "BR"
    entry["UNK0"] = F.read(size).hex()
    return entry

def FONT(F, size):
    entry = {}
    entry["TYPE"] = "FONT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def FONTtm(F, size):
    entry = {}
    entry["TYPE"] = "FONTtm"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MSPEED(F, size):
    entry = {}
    entry["TYPE"] = "MSPEED"
    entry["UNK0"] = F.read(size).hex()
    return entry

def RUBY(F, size):
    entry = {}
    entry["TYPE"] = "RUBY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def RUBYtm(F, size):
    entry = {}
    entry["TYPE"] = "RUBYtm"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TEXT_LEFT(F, size):
    entry = {}
    entry["TYPE"] = "TEXT_LEFT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TEXT_RIGHT(F, size):
    entry = {}
    entry["TYPE"] = "TEXT_RIGHT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TEXT_TOP(F, size):
    entry = {}
    entry["TYPE"] = "TEXT_TOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def EMBED(F, size):
    entry = {}
    entry["TYPE"] = "EMBED"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SPACE(F, size):
    entry = {}
    entry["TYPE"] = "SPACE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CURSOR(F, size):
    entry = {}
    entry["TYPE"] = "CURSOR"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TEXT_FADE(F, size):
    entry = {}
    entry["TYPE"] = "TEXT_FADE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ICON(F, size):
    entry = {}
    entry["TYPE"] = "ICON"
    entry["UNK0"] = F.read(size).hex()
    return entry

def EMBED_PARAM(F, size):
    entry = {}
    entry["TYPE"] = "EMBED_PARAM"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TEXT_MODE(F, size):
    entry = {}
    entry["TYPE"] = "TEXT_MODE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def NML(F, size):
    entry = {}
    entry["TYPE"] = "NML"
    entry["UNK0"] = F.read(size).hex()
    return entry

def WINDOW_ON(F, size):
    entry = {}
    entry["TYPE"] = "WINDOW_ON"
    entry["UNK0"] = F.read(size).hex()
    return entry

def WINDOW_OFF(F, size):
    entry = {}
    entry["TYPE"] = "WINDOW_OFF"
    entry["UNK0"] = F.read(size).hex()
    return entry

def WINDOW_SIZE(F, size):
    entry = {}
    entry["TYPE"] = "WINDOW_SIZE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def WINDOW_MOVE(F, size):
    entry = {}
    entry["TYPE"] = "WINDOW_MOVE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def WINDOW_FADE(F, size):
    entry = {}
    entry["TYPE"] = "WINDOW_FADE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TXTWND_IN(F, size):
    entry = {}
    entry["TYPE"] = "TXTWND_IN"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TXTWND_OUT(F, size):
    entry = {}
    entry["TYPE"] = "TXTWND_OUT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BG_LOAD(F, size):
    entry = {}
    entry["TYPE"] = "BG_LOAD"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BG_WAIT(F, size):
    entry = {}
    entry["TYPE"] = "BG_WAIT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BG_FADE(F, size):
    entry = {}
    entry["TYPE"] = "BG_FADE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BG_COLOR(F, size):
    entry = {}
    entry["TYPE"] = "BG_COLOR"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BG_MOVE(F, size):
    entry = {}
    entry["TYPE"] = "BG_MOVE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BG_SIZE(F, size):
    entry = {}
    entry["TYPE"] = "BG_SIZE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BG_ST(F, size):
    entry = {}
    entry["TYPE"] = "BG_ST"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BG_SET_ADJUST_Z(F, size):
    entry = {}
    entry["TYPE"] = "BG_SET_ADJUST_Z"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TX2_LOAD(F, size):
    entry = {}
    entry["TYPE"] = "TX2_LOAD"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TX2_MOVE(F, size):
    entry = {}
    entry["TYPE"] = "TX2_MOVE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TX2_FADE(F, size):
    entry = {}
    entry["TYPE"] = "TX2_FADE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TX2_SIZE(F, size):
    entry = {}
    entry["TYPE"] = "TX2_SIZE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TX2_ST(F, size):
    entry = {}
    entry["TYPE"] = "TX2_ST"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TX2_COLOR(F, size):
    entry = {}
    entry["TYPE"] = "TX2_COLOR"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TX2_ZGP(F, size):
    entry = {}
    entry["TYPE"] = "TX2_ZGP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TX2_CENTERING(F, size):
    entry = {}
    entry["TYPE"] = "TX2_CENTERING"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TX2_CTL_TRACK(F, size):
    entry = {}
    entry["TYPE"] = "TX2_CTL_TRACK"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TX2_TRACK(F, size):
    entry = {}
    entry["TYPE"] = "TX2_TRACK"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TX2_PACK_READ(F, size):
    entry = {}
    entry["TYPE"] = "TX2_PACK_READ"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TX2_PACK_WAIT(F, size):
    entry = {}
    entry["TYPE"] = "TX2_PACK_WAIT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANM_LOAD(F, size):
    entry = {}
    entry["TYPE"] = "ANM_LOAD"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANM_MOVE(F, size):
    entry = {}
    entry["TYPE"] = "ANM_MOVE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANM_FADE(F, size):
    entry = {}
    entry["TYPE"] = "ANM_FADE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANM_SIZE(F, size):
    entry = {}
    entry["TYPE"] = "ANM_SIZE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANM_PLAY(F, size):
    entry = {}
    entry["TYPE"] = "ANM_PLAY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANM_SKIP(F, size):
    entry = {}
    entry["TYPE"] = "ANM_SKIP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANM_STOP(F, size):
    entry = {}
    entry["TYPE"] = "ANM_STOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANM_PACK_READ(F, size):
    entry = {}
    entry["TYPE"] = "ANM_PACK_READ"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANM_PACK_WAIT(F, size):
    entry = {}
    entry["TYPE"] = "ANM_PACK_WAIT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SCR_FADE(F, size):
    entry = {}
    entry["TYPE"] = "SCR_FADE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SCR_VIB(F, size):
    entry = {}
    entry["TYPE"] = "SCR_VIB"
    entry["UNK0"] = F.read(size).hex()
    return entry

def FLAG(F, size):
    entry = {}
    entry["TYPE"] = "FLAG"
    entry["UNK0"] = F.read(size).hex()
    return entry

def PARAM(F, size):
    entry = {}
    entry["TYPE"] = "PARAM"
    entry["UNK0"] = F.read(size).hex()
    return entry

def STRING(F, size):
    entry = {}
    entry["TYPE"] = "STRING"
    entry["UNK0"] = F.read(size).hex()
    return entry

def PARAM_COMPARE(F, size):
    entry = {}
    entry["TYPE"] = "PARAM_COMPARE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def STRING_COMPARE(F, size):
    entry = {}
    entry["TYPE"] = "STRING_COMPARE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def PARAM_COPY(F, size):
    entry = {}
    entry["TYPE"] = "PARAM_COPY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def STRING_COPY(F, size):
    entry = {}
    entry["TYPE"] = "STRING_COPY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SET_VOL(F, size):
    entry = {}
    entry["TYPE"] = "SET_VOL"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BGM_READY(F, size):
    entry = {}
    entry["TYPE"] = "BGM_READY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BGM_WAIT(F, size):
    entry = {}
    entry["TYPE"] = "BGM_WAIT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BGM_PLAY(F, size):
    entry = {}
    entry["TYPE"] = "BGM_PLAY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BGM_VOL(F, size):
    entry = {}
    entry["TYPE"] = "BGM_VOL"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BGM_STOP(F, size):
    entry = {}
    entry["TYPE"] = "BGM_STOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MSG_READY(F, size):
    entry = {}
    entry["TYPE"] = "MSG_READY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MSG_WAIT(F, size):
    entry = {}
    entry["TYPE"] = "MSG_WAIT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MSG_PLAY(F, size):
    entry = {}
    entry["TYPE"] = "MSG_PLAY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MSG_VOL(F, size):
    entry = {}
    entry["TYPE"] = "MSG_VOL"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MSG_STOP(F, size):
    entry = {}
    entry["TYPE"] = "MSG_STOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SE_PLAY(F, size):
    entry = {}
    entry["TYPE"] = "SE_PLAY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SE_VOL(F, size):
    entry = {}
    entry["TYPE"] = "SE_VOL"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SE_STOP(F, size):
    entry = {}
    entry["TYPE"] = "SE_STOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SE_ALL_STOP(F, size):
    entry = {}
    entry["TYPE"] = "SE_ALL_STOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LOOPS_READY(F, size):
    entry = {}
    entry["TYPE"] = "LOOPS_READY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LOOPS_WAIT(F, size):
    entry = {}
    entry["TYPE"] = "LOOPS_WAIT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LOOPS_PLAY(F, size):
    entry = {}
    entry["TYPE"] = "LOOPS_PLAY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LOOPS_VOL(F, size):
    entry = {}
    entry["TYPE"] = "LOOPS_VOL"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LOOPS_STOP(F, size):
    entry = {}
    entry["TYPE"] = "LOOPS_STOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SONG_READY(F, size):
    entry = {}
    entry["TYPE"] = "SONG_READY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SONG_WAIT(F, size):
    entry = {}
    entry["TYPE"] = "SONG_WAIT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SONG_PLAY(F, size):
    entry = {}
    entry["TYPE"] = "SONG_PLAY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SONG_VOL(F, size):
    entry = {}
    entry["TYPE"] = "SONG_VOL"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SONG_STOP(F, size):
    entry = {}
    entry["TYPE"] = "SONG_STOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MSG_SYNC(F, size):
    entry = {}
    entry["TYPE"] = "MSG_SYNC"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SONG_SYNC(F, size):
    entry = {}
    entry["TYPE"] = "SONG_SYNC"
    entry["UNK0"] = F.read(size).hex()
    return entry

def EMBED_EDIT(F, size):
    entry = {}
    entry["TYPE"] = "EMBED_EDIT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TITLE_JUMP(F, size):
    entry = {}
    entry["TYPE"] = "TITLE_JUMP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def DLOGIC(F, size):
    entry = {}
    entry["TYPE"] = "DLOGIC"
    entry["UNK0"] = F.read(size).hex()
    return entry

def GRADE(F, size):
    entry = {}
    entry["TYPE"] = "GRADE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LOGIC_INFER(F, size):
    entry = {}
    entry["TYPE"] = "LOGIC_INFER"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SAVE_POINT(F, size):
    entry = {}
    entry["TYPE"] = "SAVE_POINT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def PAD_CTL(F, size):
    entry = {}
    entry["TYPE"] = "PAD_CTL"
    entry["UNK0"] = F.read(size).hex()
    return entry

def PAD_VIB(F, size):
    entry = {}
    entry["TYPE"] = "PAD_VIB"
    entry["UNK0"] = F.read(size).hex()
    return entry

def PAD_PUSH(F, size):
    entry = {}
    entry["TYPE"] = "PAD_PUSH"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CODE_3D_PLAY(F, size):
    entry = {}
    entry["TYPE"] = "3D_PLAY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CODE_3D_MOVE(F, size):
    entry = {}
    entry["TYPE"] = "3D_MOVE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CODE_3D_FADE(F, size):
    entry = {}
    entry["TYPE"] = "3D_FADE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CODE_3D_ROTATE(F, size):
    entry = {}
    entry["TYPE"] = "3D_ROTATE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CODE_3D_SIZE(F, size):
    entry = {}
    entry["TYPE"] = "3D_SIZE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CODE_3D_STOP(F, size):
    entry = {}
    entry["TYPE"] = "3D_STOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CODE_3D_PACK_READ(F, size):
    entry = {}
    entry["TYPE"] = "3D_PACK_READ"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CODE_3D_PACK_WAIT(F, size):
    entry = {}
    entry["TYPE"] = "3D_PACK_WAIT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CODE_3D_CAMERA_SET(F, size):
    entry = {}
    entry["TYPE"] = "3D_CMAERA_SET"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CALL_DEMO(F, size):
    entry = {}
    entry["TYPE"] = "CALL_DEMO"
    entry["UNK0"] = F.read(size).hex()
    return entry

def WAIT_DEMO_ALL(F, size):
    entry = {}
    entry["TYPE"] = "WAIT_DEMO_ALL"
    entry["UNK0"] = F.read(size).hex()
    return entry

def OPTWND(F, size):
    entry = {}
    entry["TYPE"] = "OPTWIND"
    entry["UNK0"] = F.read(size).hex()
    return entry

def RANDOM(F, size):
    entry = {}
    entry["TYPE"] = "RANDOM"
    entry["UNK0"] = F.read(size).hex()
    return entry

def READED_PCT(F, size):
    entry = {}
    entry["TYPE"] = "READED_PCT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def DENY_SKIP(F, size):
    entry = {}
    entry["TYPE"] = "DENY_SKIP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def BACKLOG_CLEAR(F, size):
    entry = {}
    entry["TYPE"] = "BACKLOG_CLEAR"
    entry["UNK0"] = F.read(size).hex()
    return entry

def HIDE_SELECTER_MENU(F, size):
    entry = {}
    entry["TYPE"] = "HIDE_SELECTER_MENU"
    entry["UNK0"] = F.read(size).hex()
    return entry

def HIDE_NAMEEDIT_MENU(F, size):
    entry = {}
    entry["TYPE"] = "HIDE_NAMEEDIT_MENU"
    entry["UNK0"] = F.read(size).hex()
    return entry

def YES_NO_DLG(F, size):
    entry = {}
    entry["TYPE"] = "YES_NO_DLG"
    entry["UNK0"] = F.read(size).hex()
    return entry

def STOP_SKIP(F, size):
    entry = {}
    entry["TYPE"] = "STOP_SKIP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def TXTHIDE_CTL(F, size):
    entry = {}
    entry["TYPE"] = "TXTHIDE_CTL"
    entry["UNK0"] = F.read(size).hex()
    return entry

def STOP_OTHER_DEMO(F, size):
    entry = {}
    entry["TYPE"] = "STOP_OTHER_DEMO"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SUBMENU_CTL(F, size):
    entry = {}
    entry["TYPE"] = "SUBMENU_CTL"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SHORTCUT_CTL(F, size):
    entry = {}
    entry["TYPE"] = "SHORTCUT_CTL"
    entry["UNK0"] = F.read(size).hex()
    return entry

def NOVELCLEAR(F, size):
    entry = {}
    entry["TYPE"] = "NOVELCLEAR"
    entry["UNK0"] = F.read(size).hex()
    return entry

def PLAY_VIDEO(F, size):
    entry = {}
    entry["TYPE"] = "PLAY_VIDEO"
    entry["UNK0"] = F.read(size).hex()
    return entry

def PHRASE_SET(F, size):
    entry = {}
    entry["TYPE"] = "PHRASE_SET"
    entry["UNK0"] = F.read(size).hex()
    return entry

def PHRASE_FADE(F, size):
    entry = {}
    entry["TYPE"] = "PHRASE_FADE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def PHRASE_MOVE(F, size):
    entry = {}
    entry["TYPE"] = "PHRASE_MOVE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def NUMBER_SET(F, size):
    entry = {}
    entry["TYPE"] = "NUMBER_SET"
    entry["UNK0"] = F.read(size).hex()
    return entry

def NUMBER_FADE(F, size):
    entry = {}
    entry["TYPE"] = "NUMBER_FADE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def NUMBER_MOVE(F, size):
    entry = {}
    entry["TYPE"] = "NUMBER_MOVE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def NUMBER_SIZE(F, size):
    entry = {}
    entry["TYPE"] = "NUMBER_SIZE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def NUMBER_GET_PARAM(F, size):
    entry = {}
    entry["TYPE"] = "NUMBER_GET_PARAM"
    entry["UNK0"] = F.read(size).hex()
    return entry

def KEYWORD(F, keyworddatabase = None):
    entry = {}
    entry["TYPE"] = "KEYWORD"
    entry["UNK0"] = F.read(0x4).hex()
    entry["KEYWORD_ID"] = int.from_bytes(F.read(0x2), byteorder="little")
    if (keyworddatabase != None):
        entry["KEYWORD"] = keyworddatabase["%d" % entry["KEYWORD_ID"]]
    return entry

def GRADE_POINT(F, size):
    entry = {}
    entry["TYPE"] = "GRADE_POINT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ADD_MEMO(F, size):
    entry = {}
    entry["TYPE"] = "ADD_MEMO"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LOGIC_MODE(F, size):
    entry = {}
    entry["TYPE"] = "LOGIC_MODE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LOGIC_SET_KEY(F, size):
    entry = {}
    entry["TYPE"] = "LOGIC_SET_KEY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LOGIC_GET_KEY(F, size):
    entry = {}
    entry["TYPE"] = "LOGIC_GET_KEY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LOGIC_CTL(F, size):
    entry = {}
    entry["TYPE"] = "LOGIC_CTL"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LOGIC_LOAD(F, size):
    entry = {}
    entry["TYPE"] = "LOGIC_LOAD"
    entry["UNK0"] = F.read(size).hex()
    return entry

def GAME_END(F, size):
    entry = {}
    entry["TYPE"] = "GAME_END"
    entry["UNK0"] = F.read(size).hex()
    return entry

def FACE(F, size):
    entry = {}
    entry["TYPE"] = "FACE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CHOOSE_KEYWORD(F, size):
    entry = {}
    entry["TYPE"] = "CHOOSE_KEYWORD"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LOGIC_CLEAR_KEY(F, size):
    entry = {}
    entry["TYPE"] = "LOGIC_CLEAR_KEY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def DATABASE(F, size):
    entry = {}
    entry["TYPE"] = "DATABASE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def SPEAKER(F, characterdatabase = None):
    entry = {}
    entry["TYPE"] = "SPEAKER"
    entry["UNK0"] = F.read(0x4).hex()
    entry["CHARACTER_ID"] = int.from_bytes(F.read(0x2), byteorder="little")
    if (characterdatabase != None):
        entry["NAME"] = characterdatabase["%d" % entry["CHARACTER_ID"]]
    return entry

def LOGIC_SAVE(F, size):
    entry = {}
    entry["TYPE"] = "LOGIC_SAVE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LOGIC_DRAW_MARK(F, size):
    entry = {}
    entry["TYPE"] = "LOGIC_DRAW_MARK"
    entry["UNK0"] = F.read(size).hex()
    return entry

def DLPAGE(F, size):
    entry = {}
    entry["TYPE"] = "DLPAGE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def DLPAGEtm(F, size):
    entry = {}
    entry["TYPE"] = "DLPAGEtm"
    entry["UNK0"] = F.read(size).hex()
    return entry

def DLKEY(F, size):
    entry = {}
    entry["TYPE"] = "DLKEY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def DLSELSET(F, size):
    entry = {}
    entry["TYPE"] = "DLSELSET"
    entry["UNK0"] = F.read(size).hex()
    return entry

def DLSELSETtm(F, size):
    entry = {}
    entry["TYPE"] = "DLSELSETtm"
    entry["UNK0"] = F.read(size).hex()
    return entry

def DLSEL(F, size):
    entry = {}
    entry["TYPE"] = "DLSEL"
    entry["UNK0"] = F.read(size).hex()
    return entry

def DLSELECT(F, size):
    entry = {}
    entry["TYPE"] = "DLSELECT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ILCAMERA(F, size):
    entry = {}
    entry["TYPE"] = "ILCAMERA"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ILZOOM(F, size):
    entry = {}
    entry["TYPE"] = "ILZOOM"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CI_LOAD(F, size):
    entry = {}
    entry["TYPE"] = "CI_LOAD"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CI_LOAD_WAIT(F, size):
    entry = {}
    entry["TYPE"] = "CI_LOAD_WAIT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CI_MOVE(F, size):
    entry = {}
    entry["TYPE"] = "CI_MOVE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CI_FADE(F, size):
    entry = {}
    entry["TYPE"] = "CI_FADE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CI_SIZE(F, size):
    entry = {}
    entry["TYPE"] = "CI_SIZE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CI_ST(F, size):
    entry = {}
    entry["TYPE"] = "CI_ST"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CI_COLOR(F, size):
    entry = {}
    entry["TYPE"] = "CI_COLOR"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CI_ZGP(F, size):
    entry = {}
    entry["TYPE"] = "CI_ZGP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CI_CENTERING(F, size):
    entry = {}
    entry["TYPE"] = "CI_CENTERING"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CI_CTL_TRACK(F, size):
    entry = {}
    entry["TYPE"] = "CI_CTL_TRACK"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CI_TRACK(F, size):
    entry = {}
    entry["TYPE"] = "CI_TRACK"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CI_NEGAPOSI(F, size):
    entry = {}
    entry["TYPE"] = "CI_NEGAPOSI"
    entry["UNK0"] = F.read(size).hex()
    return entry

def CI_BUSTUP_CENTERING(F, size):
    entry = {}
    entry["TYPE"] = "CI_BUSTUP_CENTERING"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_TEXT_TOP(F, size):
    entry = {}
    entry["TYPE"] = "MCR_TEXT_TOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_RUBY(F, size):
    entry = {}
    entry["TYPE"] = "MCR_RUBY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_BG_START(F, size):
    entry = {}
    entry["TYPE"] = "MCR_BG_START"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_BG_STOP(F, size):
    entry = {}
    entry["TYPE"] = "MCR_BG_STOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_BU_START(F, size):
    entry = {}
    entry["TYPE"] = "MCR_BU_START"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_BU_STOP(F, size):
    entry = {}
    entry["TYPE"] = "MCR_BU_STOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_CI_START(F, size):
    entry = {}
    entry["TYPE"] = "MCR_CI_START"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_CI_STOP(F, size):
    entry = {}
    entry["TYPE"] = "MCR_CI_STOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_TEXTWIN_IN(F, size):
    entry = {}
    entry["TYPE"] = "MCR_TEXTWIN_IN"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_TEXTWIN_OUT(F, size):
    entry = {}
    entry["TYPE"] = "MCR_TEXTWIN_OUT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_3D_EFFECT(F, size):
    entry = {}
    entry["TYPE"] = "MCR_3D_EFFECT"
    entry["UNK0"] = F.read(size).hex()
    return 

def MCR_BGM_START(F, size):
    entry = {}
    entry["TYPE"] = "MCR_BGM_START"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_BGM_STOP(F, size):
    entry = {}
    entry["TYPE"] = "MCR_BGM_STOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_SE_START(F, size):
    entry = {}
    entry["TYPE"] = "MCR_SE_START"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_LOOPVOICE_START(F, size):
    entry = {}
    entry["TYPE"] = "MCR_LOOPOVICE_START"
    entry["UNK0"] = F.read(size).hex()
    return entry

def MCR_LOOPVOICE_STOP(F, size):
    entry = {}
    entry["TYPE"] = "MCR_LOOPOVICE_STOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANIME_LOAD(F, size):
    entry = {}
    entry["TYPE"] = "ANIME_LOAD"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANIME_LOAD_WAIT(F, size):
    entry = {}
    entry["TYPE"] = "ANIME_LOAD_WAIT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANIME_PLAY(F, size):
    entry = {}
    entry["TYPE"] = "ANIME_PLAY"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANIME_SKIP(F, size):
    entry = {}
    entry["TYPE"] = "ANIME_SKIP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANIME_STOP(F, size):
    entry = {}
    entry["TYPE"] = "ANIME_STOP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANIME_MOVE(F, size):
    entry = {}
    entry["TYPE"] = "ANIME_MOVE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANIME_FADE(F, size):
    entry = {}
    entry["TYPE"] = "ANIME_FADE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANIME_SCALE(F, size):
    entry = {}
    entry["TYPE"] = "ANIME_SCALE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANIME_ROT(F, size):
    entry = {}
    entry["TYPE"] = "ANIME_ROT"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANIME_ZGP(F, size):
    entry = {}
    entry["TYPE"] = "ANIME_ZGP"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANIME_SYNC(F, size):
    entry = {}
    entry["TYPE"] = "ANIME_SYNC"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANIME_PAUSE(F, size):
    entry = {}
    entry["TYPE"] = "ANIME_PAUSE"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANIME_RESUME(F, size):
    entry = {}
    entry["TYPE"] = "ANIME_RESUME"
    entry["UNK0"] = F.read(size).hex()
    return entry

def ANIME_FRAME(F, size):
    entry = {}
    entry["TYPE"] = "ANIME_FRAME"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LIARSART_START(F, size):
    entry = {}
    entry["TYPE"] = "LIARSART_START"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LIARSART_DEMOEND(F, size):
    entry = {}
    entry["TYPE"] = "LIARSART_DEMOEND"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LIARSART_END(F, size):
    entry = {}
    entry["TYPE"] = "LIARSART_END"
    entry["UNK0"] = F.read(size).hex()
    return entry

def LIARSART_TUTORIAL(F, size):
    entry = {}
    entry["TYPE"] = "LIARSART_TUTORIAL"
    entry["UNK0"] = F.read(size).hex()
    return entry