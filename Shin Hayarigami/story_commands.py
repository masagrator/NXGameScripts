import numpy

class Disassemble:

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
        entry["TYPE"] = "OPTWND"
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

    def UNK_2505(F, size):
        entry = {}
        entry["TYPE"] = "UNK_2505"
        entry["UNK0"] = F.read(size).hex()
        return entry

class Assemble:

    def DEMO(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry.append(numpy.uint32(Dict["SCRIPT_ID"]))
        entry.append(bytes.fromhex(Dict["UNK1"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def DEMOtm(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def PAGE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(3))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def PAGEtm(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(4))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def EXTEND(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(99))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def JUMP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(101))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry.append(numpy.uint32(Dict["SCRIPT_ID"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SELECT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(102))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SELECTtm(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(103))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SI(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(104))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SItm(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(105))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def IF(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(106))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def IFtm(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(107))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def IFPARAM(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(108))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def IFPARAMtm(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(109))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def IFSTRING(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(112))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def IFSTRINGtm(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(113))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)
    def IFRV(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(114))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def IFRVtm(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(115))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SELECT_ITEM(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(116))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry.append(numpy.uint16(Dict["SELECT_ITEM_ID"]))
        entry.append(bytes.fromhex(Dict["UNK1"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SELECT_ITEMtm(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(117))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def WAIT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(201))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BWAIT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(202))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TWAIT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(203))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BR(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(204))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def FONT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(205))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def FONTtm(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(206))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MSPEED(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(207))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def RUBY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(208))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def RUBYtm(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(209))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TEXT_LEFT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(210))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TEXT_RIGHT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(211))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TEXT_TOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(212))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def EMBED(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(213))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SPACE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(214))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CURSOR(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(215))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TEXT_FADE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(216))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ICON(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(217))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def EMBED_PARAM(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(218))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TEXT_MODE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(219))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def NML(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(255))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def WINDOW_ON(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(301))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def WINDOW_OFF(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(302))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def WINDOW_SIZE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(303))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def WINDOW_MOVE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(304))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def WINDOW_FADE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(305))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TXTWND_IN(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(306))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TXTWND_OUT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(307))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BG_LOAD(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(401))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BG_WAIT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(402))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BG_FADE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(403))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BG_COLOR(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(404))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BG_MOVE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(405))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BG_SIZE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(406))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BG_ST(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(407))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BG_SET_ADJUST_Z(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(410))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TX2_LOAD(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(501))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TX2_MOVE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(502))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TX2_FADE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(503))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TX2_SIZE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(504))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TX2_ST(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(505))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TX2_COLOR(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(506))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TX2_ZGP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(507))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TX2_CENTERING(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(508))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TX2_CTL_TRACK(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(509))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TX2_TRACK(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(550))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TX2_PACK_READ(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(551))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TX2_PACK_WAIT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(552))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANM_LOAD(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(601))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANM_MOVE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(602))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANM_FADE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(603))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANM_SIZE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(604))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANM_PLAY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(605))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANM_SKIP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(606))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANM_STOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(607))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANM_PACK_READ(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(651))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANM_PACK_WAIT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(652))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SCR_FADE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(701))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SCR_VIB(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(702))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def FLAG(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(801))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def PARAM(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(802))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def STRING(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(803))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def PARAM_COMPARE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(804))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def STRING_COMPARE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(805))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def PARAM_COPY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(806))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def STRING_COPY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(807))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SET_VOL(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(901))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BGM_READY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(902))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BGM_WAIT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(903))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BGM_PLAY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(904))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BGM_VOL(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(905))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BGM_STOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(906))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MSG_READY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(907))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MSG_WAIT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(908))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MSG_PLAY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(909))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MSG_VOL(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(910))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MSG_STOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(911))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SE_PLAY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(914))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SE_VOL(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(915))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SE_STOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(916))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SE_ALL_STOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(917))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LOOPS_READY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(918))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LOOPS_WAIT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(919))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LOOPS_PLAY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(920))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LOOPS_VOL(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(921))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LOOPS_STOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(922))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SONG_READY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(923))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SONG_WAIT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(924))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SONG_PLAY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(925))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SONG_VOL(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(926))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SONG_STOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(927))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MSG_SYNC(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(931))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SONG_SYNC(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(932))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def EMBED_EDIT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1001))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TITLE_JUMP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1002))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def DLOGIC(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1003))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def GRADE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1004))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LOGIC_INFER(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1005))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SAVE_POINT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1005))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def PAD_CTL(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1101))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def PAD_VIB(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1102))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def PAD_PUSH(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1103))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CODE_3D_PLAY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1201))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CODE_3D_MOVE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1202))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CODE_3D_FADE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1203))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CODE_3D_ROTATE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1204))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CODE_3D_SIZE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1205))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CODE_3D_STOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1206))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CODE_3D_PACK_READ(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1251))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CODE_3D_PACK_WAIT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1252))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CODE_3D_CAMERA_SET(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1261))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CALL_DEMO(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1301))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def WAIT_DEMO_ALL(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1302))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def OPTWND(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1303))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def RANDOM(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1304))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def READED_PCT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1305))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def DENY_SKIP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1306))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def BACKLOG_CLEAR(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1307))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def HIDE_SELECTER_MENU(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1308))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def HIDE_NAMEEDIT_MENU(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1309))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def YES_NO_DLG(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1310))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def STOP_SKIP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1311))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def TXTHIDE_CTL(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1312))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def STOP_OTHER_DEMO(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1313))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SUBMENU_CTL(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1314))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SHORTCUT_CTL(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1315))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def NOVELCLEAR(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1316))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def PLAY_VIDEO(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1317))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def PHRASE_SET(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1401))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def PHRASE_FADE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1402))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def PHRASE_MOVE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1403))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def NUMBER_SET(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1501))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def NUMBER_FADE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1502))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def NUMBER_MOVE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1503))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def NUMBER_SIZE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1504))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def NUMBER_GET_PARAM(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(1505))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def KEYWORD(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2001))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry.append(numpy.uint16(Dict["KEYWORD_ID"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def GRADE_POINT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2002))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ADD_MEMO(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2003))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LOGIC_MODE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2004))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LOGIC_SET_KEY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2005))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LOGIC_GET_KEY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2006))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LOGIC_CTL(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2007))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LOGIC_LOAD(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2008))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def GAME_END(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2009))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def FACE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2010))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CHOOSE_KEYWORD(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2011))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LOGIC_CLEAR_KEY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2012))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def DATABASE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2013))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def SPEAKER(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2014))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry.append(numpy.uint16(Dict["CHARACTER_ID"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LOGIC_SAVE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2021))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LOGIC_DRAW_MARK(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2022))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def DLPAGE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2101))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def DLPAGEtm(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2102))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def DLKEY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2103))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def DLSELSET(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2104))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def DLSELSETtm(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2105))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def DLSEL(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2106))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def DLSELECT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2107))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ILCAMERA(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2108))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ILZOOM(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2109))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CI_LOAD(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2201))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CI_LOAD_WAIT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2202))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CI_MOVE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2203))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CI_FADE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2204))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CI_SIZE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2205))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CI_ST(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2206))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CI_COLOR(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2207))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CI_ZGP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2208))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CI_CENTERING(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2209))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CI_CTL_TRACK(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2210))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CI_TRACK(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2211))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CI_NEGAPOSI(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2212))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def CI_BUSTUP_CENTERING(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2213))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_TEXT_TOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2301))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_RUBY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2302))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_BG_START(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2303))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_BG_STOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2304))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_BU_START(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2305))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_BU_STOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2306))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_CI_START(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2307))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_CI_STOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2308))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_TEXTWIN_IN(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2309))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_TEXTWIN_OUT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2310))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_3D_EFFECT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2311))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_BGM_START(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2312))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_BGM_STOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2313))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_SE_START(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2314))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_LOOPVOICE_START(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2315))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def MCR_LOOPVOICE_STOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2316))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANIME_LOAD(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2401))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANIME_LOAD_WAIT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2402))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANIME_PLAY(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2403))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANIME_SKIP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2404))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANIME_STOP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2405))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANIME_MOVE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2406))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANIME_FADE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2407))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANIME_SCALE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2408))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANIME_ROT(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2409))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANIME_ZGP(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2410))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANIME_SYNC(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2411))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANIME_PAUSE(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2412))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANIME_RESUME(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2413))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def ANIME_FRAME(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2414))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LIARSART_START(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2501))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LIARSART_DEMOEND(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2502))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LIARSART_END(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2503))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def LIARSART_TUTORIAL(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2504))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)

    def UNK_2505(Dict):
        entry = []
        entry.append(b"\xFF")
        entry.append(numpy.uint8(0))
        entry.append(numpy.uint16(2505))
        entry.append(bytes.fromhex(Dict["UNK0"]))
        entry[1] = numpy.uint8(len(b"".join(entry)))
        while (len(b"".join(entry)) % 4 != 0):
            entry.append(b"\x00")
        return b"".join(entry)