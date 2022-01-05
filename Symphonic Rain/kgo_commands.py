class Storage:

    ints = []

class Disassemble:

    def GetU32(file):
        Storage.ints.append(int.from_bytes(file.read(0x4), byteorder="little"))
        return None

    def CMD_x2():
        entry = {}
        entry["TYPE"] = "CMD_x2"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def CMD_x8():
        entry = {}
        entry["TYPE"] = "CMD_x8"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def CMD_xB():
        entry = {}
        entry["TYPE"] = "CMD_xB"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def CMD_xE():
        entry = {}
        entry["TYPE"] = "CMD_xE"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry
    
    def CMD_x10():
        entry = {}
        entry["TYPE"] = "CMD_x10"
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

    def SetBG():
        entry = {}
        entry["TYPE"] = "SetBG"
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

    def ShowOpening():
        entry = {}
        entry["TYPE"] = "ShowOpening"
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