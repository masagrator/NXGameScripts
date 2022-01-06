import numpy

class Storage:

    ints = []
    Textcounter = 1

class Disassemble:

    def NOP():
        entry = {}
        entry["TYPE"] = "NOP"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def GetU32(file):
        Storage.ints.append(int.from_bytes(file.read(0x4), byteorder="little", signed = True))
        return None

    def POP():
        entry = {}
        entry["TYPE"] = "POP"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def JMP(file, pos):
        entry = {}
        entry["TYPE"] = "JMP"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        offset = int.from_bytes(file.read(0x4), byteorder="little", signed = True)
        entry["JUMP_TO_LABEL"] = "0x%x" % (pos + offset)
        return entry

    def JZ(file, pos):
        entry = {}
        entry["TYPE"] = "JZ"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        offset = int.from_bytes(file.read(0x4), byteorder="little", signed = True)
        entry["JUMP_TO_LABEL"] = "0x%x" % (pos + offset)
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

    def ADD():
        entry = {}
        entry["TYPE"] = "ADD"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SUB():
        entry = {}
        entry["TYPE"] = "SUB"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def LT():
        entry = {}
        entry["TYPE"] = "LT"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def LE():
        entry = {}
        entry["TYPE"] = "LE"
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

    def LAND():
        entry = {}
        entry["TYPE"] = "LAND"
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

    def SETV():
        entry = {}
        entry["TYPE"] = "SETV"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def GETV():
        entry = {}
        entry["TYPE"] = "GETV"
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

    def KeyWait():
        entry = {}
        entry["TYPE"] = "KeyWait"
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

    def VoiceVol():
        entry = {}
        entry["TYPE"] = "VoiceVol"
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

    def SongVol():
        entry = {}
        entry["TYPE"] = "SongVol"
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

    def SEStop():
        entry = {}
        entry["TYPE"] = "SEStop"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SEVol():
        entry = {}
        entry["TYPE"] = "SEVol"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SEPos():
        entry = {}
        entry["TYPE"] = "SEPos"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def EnvVol():
        entry = {}
        entry["TYPE"] = "EnvVol"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def EnvPos():
        entry = {}
        entry["TYPE"] = "EnvPos"
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

    def SetChar():
        entry = {}
        entry["TYPE"] = "SetChar"
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

    def WhiteOut():
        entry = {}
        entry["TYPE"] = "WhiteOut"
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

    def AllMoveChartoActionChar2():
        entry = {}
        entry["TYPE"] = "AllMoveChartoActionChar2"
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

    def Effect():
        entry = {}
        entry["TYPE"] = "Effect"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def ShowCursor():
        entry = {}
        entry["TYPE"] = "ShowCursor"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def HideCursor():
        entry = {}
        entry["TYPE"] = "HideCursor"
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

    def SetDate():
        entry = {}
        entry["TYPE"] = "SetDate"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def GetDate():
        entry = {}
        entry["TYPE"] = "GetDate"
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

    def ShowEnding():
        entry = {}
        entry["TYPE"] = "ShowEnding"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def GoTitle():
        entry = {}
        entry["TYPE"] = "GoTitle"
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

    def AddDay():
        entry = {}
        entry["TYPE"] = "AddDay"
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

    def AllMoveChartoActionChar():
        entry = {}
        entry["TYPE"] = "AllMoveChartoActionChar"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SetChangeChar():
        entry = {}
        entry["TYPE"] = "SetChangeChar"
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

    def TimeShow():
        entry = {}
        entry["TYPE"] = "TimeShow"
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

    def SongStop():
        entry = {}
        entry["TYPE"] = "SongStop"
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

    def GetRainPower():
        entry = {}
        entry["TYPE"] = "GetRainPower"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SetRainLevel():
        entry = {}
        entry["TYPE"] = "SetRainLevel"
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

    def SubRainPower():
        entry = {}
        entry["TYPE"] = "SubRainPower"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def AddRainPowLv():
        entry = {}
        entry["TYPE"] = "AddRainPowLv"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

    def SubRainPowLv():
        entry = {}
        entry["TYPE"] = "SubRainPowLv"
        if (len(Storage.ints) > 0):
            entry["U32"] = Storage.ints
            Storage.ints = []
        return entry

class Assemble:

    def POP(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(2))
        return b"".join(bytes)

    def JMP(dict, offset):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(3))
        bytes.append(numpy.int32(offset))
        return b"".join(bytes)

    def JZ(dict, offset):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(4))
        bytes.append(numpy.int32(offset))
        return b"".join(bytes)

    def CALL(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(6))
        return b"".join(bytes)

    def DUP(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(8))
        return b"".join(bytes)

    def SWAP2(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0xB))
        return b"".join(bytes)
    
    def RET(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0xE))
        return b"".join(bytes)

    def LNOT(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x10))
        return b"".join(bytes)

    def ADD(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x16))
        return b"".join(bytes)

    def SUB(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x17))
        return b"".join(bytes)

    def LT(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x18))
        return b"".join(bytes)

    def LE(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x19))
        return b"".join(bytes)

    def GE(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x1B))
        return b"".join(bytes)

    def EQ(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x1C))
        return b"".join(bytes)

    def NE(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x1D))
        return b"".join(bytes)

    def LAND(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x1E))
        return b"".join(bytes)

    def LOR(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x1F))
        return b"".join(bytes)

    def SETF(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x20))
        return b"".join(bytes)

    def GETF(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x21))
        return b"".join(bytes)

    def SETSF(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x22))
        return b"".join(bytes)

    def GETSF(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x23))
        return b"".join(bytes)

    def SETV(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x24))
        return b"".join(bytes)

    def GETV(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x25))
        return b"".join(bytes)

    def SETRES(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x2A))
        return b"".join(bytes)

    def GETRES(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x2B))
        return b"".join(bytes)

    def SCNCHG(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x30))
        return b"".join(bytes)

    def Text(dict, Offsets):
        bytes = []
        for i in range(0, len(dict["STRING"])):
            bytes.append(numpy.uint16(1))
            bytes.append(numpy.uint32(Storage.Textcounter))
            bytes.append(numpy.uint16(0x40))
            if (Offsets != None):
                Storage.Textcounter += 1
            if (i < len(dict["STRING"]) - 1):
                NewLineDict = {"TYPE": "NewLine"}
                bytes.append(Assemble.NewLine(NewLineDict))
        return b"".join(bytes)

    def NewLine(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x41))
        return b"".join(bytes)

    def NewPage(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x42))
        return b"".join(bytes)

    def TextShow(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x43))
        return b"".join(bytes)

    def TextHide(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x44))
        return b"".join(bytes)

    def TextSpeed(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x45))
        return b"".join(bytes)

    def NovelMode(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x46))
        return b"".join(bytes)

    def Locate(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x47))
        return b"".join(bytes)

    def Wait(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x48))
        return b"".join(bytes)

    def KeyWait(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x49))
        return b"".join(bytes)

    def SkipDisable(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x4A))
        return b"".join(bytes)

    def Voice(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x4B))
        return b"".join(bytes)

    def VoiceVol(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x4C))
        return b"".join(bytes)

    def VoicePos(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x4D))
        return b"".join(bytes)

    def BGMVol(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x50))
        return b"".join(bytes)

    def SongVol(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x53))
        return b"".join(bytes)

    def SEPlay(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x54))
        return b"".join(bytes)

    def SEStop(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x55))
        return b"".join(bytes)

    def SEVol(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x56))
        return b"".join(bytes)

    def SEPos(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x57))
        return b"".join(bytes)

    def EnvVol(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x5A))
        return b"".join(bytes)

    def EnvPos(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x5B))
        return b"".join(bytes)

    def SetBG(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x5C))
        return b"".join(bytes)

    def SetBlack(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x5E))
        return b"".join(bytes)

    def SetChar(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x5F))
        return b"".join(bytes)

    def Fade(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x61))
        return b"".join(bytes)

    def FadeBGtoSetBG(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x62))
        return b"".join(bytes)

    def WhiteOut(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x63))
        return b"".join(bytes)

    def BlackOut(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x64))
        return b"".join(bytes)

    def MoveChar(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x65))
        return b"".join(bytes)

    def HideChar(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x66))
        return b"".join(bytes)

    def AllMoveChartoActionChar2(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x67))
        return b"".join(bytes)

    def AllHideChar(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x68))
        return b"".join(bytes)

    def Effect(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x69))
        return b"".join(bytes)

    def ShowCursor(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x6A))
        return b"".join(bytes)

    def HideCursor(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x6B))
        return b"".join(bytes)

    def ShowPlace(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x6C))
        return b"".join(bytes)

    def SetDate(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x6D))
        return b"".join(bytes)

    def GetDate(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x6E))
        return b"".join(bytes)

    def GetWeek(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x71))
        return b"".join(bytes)

    def SetTime(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x72))
        return b"".join(bytes)

    def SetWeather(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x76))
        return b"".join(bytes)

    def Select(dict, Offsets):
        bytes = []
        for i in range(0, len(dict["STRINGS"])):
            bytes.append(numpy.uint16(1))
            bytes.append(numpy.uint32(Storage.Textcounter))
            if (Offsets != None):
                Storage.Textcounter += 1
        for i in range(0, 4-len(dict["STRINGS"])):
            bytes.append(numpy.uint16(1))
            bytes.append(numpy.uint32(0))
        bytes.append(numpy.uint16(0x78))
        return b"".join(bytes)

    def ShowOpening(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x79))
        return b"".join(bytes)

    def ShowEnding(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x7A))
        return b"".join(bytes)

    def GoTitle(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x7B))
        return b"".join(bytes)

    def MiniGame(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x7C))
        return b"".join(bytes)

    def UNK_x7D(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x7D))
        return b"".join(bytes)

    def UNK_x7F(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x7F))
        return b"".join(bytes)

    def MapMove(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x80))
        return b"".join(bytes)

    def AddDay(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x81))
        return b"".join(bytes)

    def AddMin(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x82))
        return b"".join(bytes)

    def RainVol(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x83))
        return b"".join(bytes)

    def AllMoveChartoActionChar(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x84))
        return b"".join(bytes)

    def SetChangeChar(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x85))
        return b"".join(bytes)

    def DateShow(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x86))
        return b"".join(bytes)

    def DateHide(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x87))
        return b"".join(bytes)

    def TimeShow(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x88))
        return b"".join(bytes)

    def TimeHide(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x89))
        return b"".join(bytes)

    def BGMPlay(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x8A))
        return b"".join(bytes)

    def BGMStop(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x8B))
        return b"".join(bytes)

    def SongPlay(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x8C))
        return b"".join(bytes)

    def SongStop(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x8D))
        return b"".join(bytes)

    def EnvPlay(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x8E))
        return b"".join(bytes)

    def EnvStop(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x8F))
        return b"".join(bytes)

    def SongEnable(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x90))
        return b"".join(bytes)

    def SetRainPower(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x91))
        return b"".join(bytes)

    def GetRainPower(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x92))
        return b"".join(bytes)

    def SetRainLevel(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x93))
        return b"".join(bytes)

    def AddRainPower(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x95))
        return b"".join(bytes)

    def SubRainPower(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x96))
        return b"".join(bytes)

    def AddRainPowLv(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x97))
        return b"".join(bytes)

    def SubRainPowLv(dict):
        bytes = []
        try:
            dict["U32"]
        except:
            pass
        else:
            for i in range(0, len(dict["U32"])):
                bytes.append(numpy.uint16(1))
                bytes.append(numpy.uint32(dict["U32"][i]))
        bytes.append(numpy.uint16(0x98))
        return b"".join(bytes)