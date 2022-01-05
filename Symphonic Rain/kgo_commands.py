class Storage:

    ints = []

class Disassemble:

    def NOP():
        entry = {}
        entry["TYPE"] = "NOP"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def GetU32(file):
        Storage.ints.append(int.from_bytes(file.read(0x4), byteorder="little"))
        return None

    def POP():
        entry = {}
        entry["TYPE"] = "POP"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def JMP(file):
        entry = {}
        entry["TYPE"] = "JMP"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        entry["ARG"] = int.from_bytes(file.read(0x4), byteorder="little")
        return entry

    def JZ(file):
        entry = {}
        entry["TYPE"] = "JZ"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        entry["ARG"] = int.from_bytes(file.read(0x4), byteorder="little")
        return entry

    def CALL():
        entry = {}
        entry["TYPE"] = "CALL"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def DUP():
        entry = {}
        entry["TYPE"] = "DUP"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SWAP2():
        entry = {}
        entry["TYPE"] = "SWAP2"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry
    
    def RET():
        entry = {}
        entry["TYPE"] = "RET"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def LNOT():
        entry = {}
        entry["TYPE"] = "LNOT"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def GE():
        entry = {}
        entry["TYPE"] = "GE"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def EQ():
        entry = {}
        entry["TYPE"] = "EQ"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def NE():
        entry = {}
        entry["TYPE"] = "NE"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def LOR():
        entry = {}
        entry["TYPE"] = "LOR"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SETF():
        entry = {}
        entry["TYPE"] = "SETF"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def GETF():
        entry = {}
        entry["TYPE"] = "GETF"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SETSF():
        entry = {}
        entry["TYPE"] = "SETSF"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def GETSF():
        entry = {}
        entry["TYPE"] = "GETSF"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SETRES():
        entry = {}
        entry["TYPE"] = "SETRES"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def GETRES():
        entry = {}
        entry["TYPE"] = "GETRES"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SCNCHG():
        entry = {}
        entry["TYPE"] = "SCNCHG"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def Text():
        entry = {}
        entry["TYPE"] = "Text"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def NewLine():
        entry = {}
        entry["TYPE"] = "NewLine"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def NewPage():
        entry = {}
        entry["TYPE"] = "NewPage"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def TextShow():
        entry = {}
        entry["TYPE"] = "TextShow"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def TextHide():
        entry = {}
        entry["TYPE"] = "TextHide"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def TextSpeed():
        entry = {}
        entry["TYPE"] = "TextSpeed"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def NovelMode():
        entry = {}
        entry["TYPE"] = "NovelMode"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def Locate():
        entry = {}
        entry["TYPE"] = "Locate"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def Wait():
        entry = {}
        entry["TYPE"] = "Wait"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SkipDisable():
        entry = {}
        entry["TYPE"] = "SkipDisable"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def Voice():
        entry = {}
        entry["TYPE"] = "Voice"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def VoicePos():
        entry = {}
        entry["TYPE"] = "VoicePos"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def BGMVol():
        entry = {}
        entry["TYPE"] = "BGMVol"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SEPlay():
        entry = {}
        entry["TYPE"] = "SEPlay"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SetBG():
        entry = {}
        entry["TYPE"] = "SetBG"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SetBlack():
        entry = {}
        entry["TYPE"] = "SetBlack"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry
    
    def KeyWait():
        entry = {}
        entry["TYPE"] = "KeyWait"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def Fade():
        entry = {}
        entry["TYPE"] = "Fade"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def FadeBGtoSetBG():
        entry = {}
        entry["TYPE"] = "FadeBGtoSetBG"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def BlackOut():
        entry = {}
        entry["TYPE"] = "BlackOut"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def MoveChar():
        entry = {}
        entry["TYPE"] = "MoveChar"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def HideChar():
        entry = {}
        entry["TYPE"] = "HideChar"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def AllHideChar():
        entry = {}
        entry["TYPE"] = "AllHideChar"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def ShowPlace():
        entry = {}
        entry["TYPE"] = "ShowPlace"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def GetWeek():
        entry = {}
        entry["TYPE"] = "GetWeek"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SetTime():
        entry = {}
        entry["TYPE"] = "SetTime"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SetWeather():
        entry = {}
        entry["TYPE"] = "SetWeather"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def Select():
        entry = {}
        entry["TYPE"] = "Select"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def ShowOpening():
        entry = {}
        entry["TYPE"] = "ShowOpening"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def UNK_x7D():
        entry = {}
        entry["TYPE"] = "UNK_x7D"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def UNK_x7F():
        entry = {}
        entry["TYPE"] = "UNK_x7F"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def MapMove():
        entry = {}
        entry["TYPE"] = "MapMove"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def MiniGame():
        entry = {}
        entry["TYPE"] = "MiniGame"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def AddMin():
        entry = {}
        entry["TYPE"] = "AddMin"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def RainVol():
        entry = {}
        entry["TYPE"] = "RainVol"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def DateShow():
        entry = {}
        entry["TYPE"] = "DateShow"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def DateHide():
        entry = {}
        entry["TYPE"] = "DateHide"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def TimeHide():
        entry = {}
        entry["TYPE"] = "TimeHide"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def TimeShow():
        entry = {}
        entry["TYPE"] = "TimeShow"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def BGMPlay():
        entry = {}
        entry["TYPE"] = "BGMPlay"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def BGMStop():
        entry = {}
        entry["TYPE"] = "BGMStop"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SongPlay():
        entry = {}
        entry["TYPE"] = "SongPlay"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def EnvPlay():
        entry = {}
        entry["TYPE"] = "EnvPlay"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def EnvStop():
        entry = {}
        entry["TYPE"] = "EnvStop"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SongEnable():
        entry = {}
        entry["TYPE"] = "SongEnable"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SetRainPower():
        entry = {}
        entry["TYPE"] = "SetRainPower"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def AddRainPower():
        entry = {}
        entry["TYPE"] = "AddRainPower"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry