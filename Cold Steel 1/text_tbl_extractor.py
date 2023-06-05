import glob
import json
import os
import sys
import struct

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("UTF-8"))
        chars.append(c)

files = glob.glob("text/nx/*.tbl")

os.makedirs("text/json", exist_ok=True)

for i in range(0, len(files)):
    print(files[i])
    file = open(files[i], "rb")
    count = int.from_bytes(file.read(2), byteorder="little")

    DUMP = []
    for x in range(0, count):
        entry = {}
        #print("0x%x" % file.tell())
        type = readString(file)
        entry_size = int.from_bytes(file.read(2), byteorder="little")
        match(type):
            case "TextTableData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
            
            case "ActiveVoiceTableData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["VOICE_FILE"] = readString(file)
                entry["UNK0"] = int.from_bytes(file.read(4), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK1"] = [struct.unpack("<f", file.read(4))[0], struct.unpack("<f", file.read(4))[0]]
                entry["UNK2"]  = []
                for y in range(0, 6):
                    entry["UNK2"].append(int.from_bytes(file.read(2), byteorder="little"))
            
            case "AttachTableData":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "BattleUIData":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "bgm":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "QSBookScp":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "QSChapter":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
            
            case "QSBook":
                entry["TYPE"] = type
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
                entry["BOOK"] = readString(file)
                entry["BOOKDATA"] = readString(file)
                entry["ID2"] = int.from_bytes(file.read(2), byteorder="little")
            
            case "TacticalBonus":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK0"] = struct.unpack("<f", file.read(4))[0]
                entry["UNK1"] = int.from_bytes(file.read(2), byteorder="little")
            
            case "AtBonus":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "CardTableData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK0"] = file.read(26).hex()
            
            case "dlc":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["CONTENTID"] = readString(file)
                entry["GROUPID"] = readString(file)
                entry["STRINGS"] = [readString(file), readString(file)]
            
            case "FaceSupplementTableData":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "fish_pnt":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "rod_lst":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "text_lst":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
            
            case "FootStepData":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "hkitugi_lst":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK1"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRINGS"] = [readString(file), readString(file)]

            case "item":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little", signed=True)
                entry["STRING"] = readString(file)
                entry["UNK1"] = file.read(0x2E).hex()
                entry["STRINGS"] = [readString(file), readString(file)]
            
            case "MapJumpData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING1"] = readString(file)
                entry["UNK1"] = file.read(4).hex()
                entry["STRING2"] = readString(file)
                entry["STRING3"] = readString(file)
                entry["UNK2"] = file.read(0x1C).hex()
            
            case "LinkAbList":
                entry["TYPE"] = type
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK1"] = int.from_bytes(file.read(1), byteorder="little")
                entry["STRINGS"] = [readString(file), readString(file)]
            
            case "LinkLevelExp":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "magic":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["GROUP"] = readString(file)
                entry["UNK1"] = file.read(0x18).hex()
                entry["NAMEID"] = readString(file)
                entry["STRINGS"] = [readString(file), readString(file)]
            
            case "MapBgmTableData":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "MG02Title":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "MG02Text":
                entry["TYPE"] = type
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK1"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK2"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK3"] = int.from_bytes(file.read(4), byteorder="little", signed=True)
            
            case "SMG04TableData":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "status":
                entry["TYPE"] = type
                entry["STRING1"] = readString(file)
                entry["STRING2"] = readString(file)
                entry["STRING3"] = readString(file)
                entry["UNK0"] = []
                for y in range(0, 3):
                    entry["UNK0"].append(struct.unpack("<f", file.read(4))[0])
                entry["UNK1"] = file.read(0x65).hex()
                if (entry["UNK1"][-2:] != "00"):
                    while (entry["UNK1"][-2:] != "00"):
                       entry["UNK1"] += file.read(0x1).hex() 
                entry["STRINGS"] = [readString(file), readString(file)]

            case "MasterQuartzBase":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "MasterQuartzData":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "MasterQuartzMemo":
                entry["TYPE"] = type
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
            
            case "NameTableData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING1"] = readString(file)
                entry["STRING2"] = []
                for y in range(0, 5):
                    entry["STRING2"].append(readString(file))
            
            case "NaviTextData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK0"] = file.read(4).hex()
            
            case "QSChar":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK0"] = file.read(4).hex()
                entry["STRINGS"] = []
                for y in range(0, 10):
                    entry["STRINGS"].append(readString(file))
            
            case "QSCook":
                entry["TYPE"] = type
                entry["STRING1"] = readString(file)
                entry["UNK0"] = file.read(0x24).hex()
                entry["STRINGS1"] = [readString(file), readString(file)]
                entry["UNK1"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRINGS2"] = [readString(file), readString(file)]
                entry["UNK2"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRINGS3"] = [readString(file), readString(file)]
                entry["UNK3"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRINGS4"] = [readString(file), readString(file)]
                entry["UNK4"] = file.read(0xB).hex()
            
            case "QSFish":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING1"] = readString(file)
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK1"] = []
                for y in range(0, 3):
                    entry["UNK1"].append(struct.unpack("<f", file.read(4))[0])
                entry["UNK2"] = file.read(0x52).hex()
                entry["STRING2"] = readString(file)
                entry["UNK3"] = file.read(0x3E).hex()
            
            case "QSHelp":
                entry["TYPE"] = type
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)

            case "QSMons":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "BaseList":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "OrbLineList":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "PTBadTerm":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "PlaceTableData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["NAMEID"] = readString(file)
                entry["STRING1"] = readString(file)
                entry["STRING2"] = readString(file)
            
            case "QuartzCost":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "QSRank":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK0"] = file.read(0x6).hex()
            
            case "preset":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "se":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "ShopGoods":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "ShopTitle":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK0"] = int.from_bytes(file.read(1), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK1"] = file.read(8).hex()
            
            case "ShopItem":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "HoriItem":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "FPointItem":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "SlotEp":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()

            case "SlotCost":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()

            case "growth":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "trade":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "VoiceTimingInfo":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "VoiceTiming":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()

            case "voice":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), "little")
                entry["NAME"] = readString(file)
                entry["UNK"] = file.read(entry_size-3-len(entry["NAME"])).hex().upper()
            
            case "QSTitle":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK0"] = int.from_bytes(file.read(1), byteorder="little")
                entry["STRING"] = readString(file)
                entry["CATEGORY"] = readString(file)
                entry["UNK1"] = file.read(9).hex()
            
            case "QSText":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK0"] = int.from_bytes(file.read(1), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK1"] = int.from_bytes(file.read(1), byteorder="little")
            
            case "char_revise":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "weapon_attribute":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()

            case "status_revise":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case _:
                print("UNKNOWN TYPE! %s" % type)
                sys.exit()
        
        if (len(entry) > 0):
            DUMP.append(entry)
    
    file.close()

    if (len(DUMP) > 0):
        file = open("text/json/%s.json" % files[i][8:-4], "w", encoding="UTF-8")
        json.dump(DUMP, file, indent="\t", ensure_ascii=False)
        file.close()
    else:
        print("MO STRINGS DETECTED!")