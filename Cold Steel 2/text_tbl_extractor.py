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

files = glob.glob("nx/*.tbl")

os.makedirs("jsons", exist_ok=True)

for i in range(0, len(files)):
    print(files[i])
    file = open(files[i], "rb")
    entries_count = int.from_bytes(file.read(2), byteorder="little")
    types_count = int.from_bytes(file.read(4), byteorder="little")
    types = []
    types_sum_check = 0
    for y in range(0, types_count):
        entry3 = {}
        entry3["NAME"] = readString(file)
        entry3["COUNT"] = int.from_bytes(file.read(4), byteorder="little")
        types_sum_check += entry3["COUNT"]
        types.append(entry3)
    assert(types_sum_check == entries_count)
    DUMP = []
    for x in range(0, entries_count):
        entry = {}
        print("0x%x" % file.tell())
        type = readString(file)
        entry_size = int.from_bytes(file.read(2), byteorder="little")
        match(type):
            case "TextTableData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
            
            #Changed
            case "ActiveVoiceTableData":
                entry["TYPE"] = type
                entry["ID1"] = int.from_bytes(file.read(2), byteorder="little")
                entry["ID2"] = int.from_bytes(file.read(2), byteorder="little")
                entry["ID3"] = int.from_bytes(file.read(2), byteorder="little")
                entry["ASSET_SYMBOL"] = readString(file)
                entry["VOICE_FILE_ID"] = int.from_bytes(file.read(4), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK0"] = [struct.unpack("<f", file.read(4))[0], struct.unpack("<f", file.read(4))[0]]
                entry["UNK1"]  = []
                for y in range(0, 5):
                    entry["UNK1"].append(int.from_bytes(file.read(2), byteorder="little"))
            
            #Changed
            case "AttachTableData":
                entry["TYPE"] = type
                entry["UNK"] = file.read(0x16).hex().upper()
                entry["STRINGS"] = [readString(file), readString(file)]
            
            case "BattleUIData":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "bgm":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "QSBookScp":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            #Changed
            case "QSChapter":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK"] = int.from_bytes(file.read(2), byteorder="little")
            
            #Changed
            case "QSBook":
                entry["TYPE"] = type
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
                entry["BOOK"] = readString(file)
                entry["BOOKDATA"] = readString(file)
                entry["ID2"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK1"] = file.read(3).hex().upper()
            
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
            
            #Changed
            case "dlc":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK"] = file.read(0xA).hex().upper()
                entry["STRINGS"] = [readString(file), readString(file)]
                entry["UNK2"] = file.read(0x50).hex().upper()
            
            #Changed
            case "FaceSupplementTableData":
                entry["TYPE"] = type
                entry["UNK"] = file.read(0x12).hex().upper()
                entry["STRING"] = readString(file)
                entry["UNK2"] = file.read(8).hex().upper()
            
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
            
            #Changed
            case "FootStepData":
                entry["TYPE"] = type
                entry["STRING"] = readString(file)
                entry["UNK"] = int.from_bytes(file.read(1), byteorder="little")
            
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
                entry["CATEGORY"] = readString(file)
                entry["UNK1"] = file.read(0x3C).hex()
                entry["STRINGS"] = [readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file)]
            
            #Changed
            case "MapJumpData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING1"] = readString(file)
                entry["UNK1"] = file.read(4).hex()
                entry["STRING2"] = readString(file)
                entry["STRING3"] = readString(file)
                entry["UNK2"] = file.read(0x1E).hex()
            
            case "LinkAbList":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "LinkLevelExp":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "magic":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["GROUP"] = readString(file)
                entry["UNK1"] = file.read(0x28).hex()
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
            
            #Changed
            case "status":
                entry["TYPE"] = type
                entry["STRING1"] = readString(file)
                entry["STRING2"] = readString(file)
                entry["STRING3"] = readString(file)
                entry["UNK0"] = []
                for y in range(0, 7):
                    entry["UNK0"].append(struct.unpack("<f", file.read(4))[0])
                entry["UNK1"] = file.read(0x98).hex()
                entry["STRINGS"] = [readString(file), readString(file), readString(file)]

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
            
            #Changed
            case "NameTableData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING1"] = readString(file)
                entry["STRING2"] = []
                for y in range(0, 6):
                    entry["STRING2"].append(readString(file))
                entry["UNK"] = file.read(0x11).hex()
                
            
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
            
            #Changed
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
                entry["UNK4"] = file.read(0x30).hex()
            
            #Changed
            case "QSFish":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK"] = int.from_bytes(file.read(1), byteorder="little")
                entry["STRING1"] = readString(file)
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK1"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK2"] = []
                for y in range(0, 3):
                    entry["UNK2"].append(struct.unpack("<f", file.read(4))[0])
                entry["UNK3"] = file.read(0x56).hex()
                entry["STRING2"] = readString(file)
                entry["UNK4"] = file.read(0x3E).hex()
            
            case "QSHelp":
                entry["TYPE"] = type
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)

            case "QSMons":
                entry["TYPE"] = type
                entry["STRING"] = readString(file)
                entry["UNK"] = int.from_bytes(file.read(2), byteorder="little")
                entry["ID"] = int.from_bytes(file.read(4), byteorder="little")
            
            case "BaseList":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "OrbLineList":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "PTBadTerm":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            #Changed
            case "PlaceTableData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK0"] = int.from_bytes(file.read(2), byteorder="little")
                entry["NAMEID"] = readString(file)
                entry["STRING"] = readString(file)
                entry["UNK1"] = file.read(4).hex().upper()
            
            case "QuartzCost":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "QSRank":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK0"] = file.read(0x6).hex()
            
            #Changed
            case "preset":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK"] = file.read(entry_size-2).hex().upper()
            
            #Changed
            case "se":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK"] = file.read(0xE).hex().upper()
            
            case "ShopGoods":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            #Changed
            case "ShopTitle":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
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
            
            #Changed
            case "trade":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK"] = file.read(0x16).hex().upper()
            
            case "VoiceTimingInfo":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            #Changed
            case "VoiceTiming":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK"] = file.read(0xA).hex().upper()

            #Changed
            case "voice":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK"] = file.read(0xE).hex()
            
            #Changed
            case "QSTitle":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK0"] = int.from_bytes(file.read(1), byteorder="little")
                entry["STRING"] = readString(file)
                entry["CATEGORY"] = readString(file)
                entry["UNK1"] = file.read(0xB).hex()
            
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
            
            #New start here
            case "MissionText":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(1), byteorder="little")
                entry["STRING"] = readString(file)
            
            case "MG05Root" | "MasterQuartzStatus" | "MasterQuartzDummy" | "MasterQuartzDummy2" | "NaviIconTableData" | "QSCoolVoice" | "ShopConv" | "TitleData" | "MG05Target" | "CompHelpData" | "condition" | "InfItemSet" | "MissionData" | "OverRisePoint" | "BattleVoiceData_A" | "BattleVoiceData_B" | "BattleVoiceData_C" | "BattleVoiceData_D" | "BattleVoiceData_E" | "BattleVoiceData_F" | "BattleVoiceData_G" | "CheckEquipFlag":
                entry["TYPE"] = type
                entry["UNK"] = file.read(entry_size).hex().upper()
            
            case "EventTableData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["EVENT"] = readString(file)
                entry["MAP"] = readString(file)
                entry["UNK"] = file.read(6).hex().upper()
                entry["ARG"] = readString(file)
                entry["UNK2"] = file.read(0x12).hex().upper()

            case "FaceShiftTableData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(1), byteorder="little")
                entry["STRINGS"] = [readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file), readString(file)]

            case "InfMonsSet":
                entry["TYPE"] = type
                entry["UNK"] = file.read(8).hex().upper()
                entry["MONSTERS"] = []
                for y in range(0, 8):
                    entry2 = {}
                    entry2["NAME"] = readString(file)
                    entry2["STATE"] = int.from_bytes(file.read(1), byteorder="little")
                    entry["MONSTERS"].append(entry2)

            case "item_q":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK"] = int.from_bytes(file.read(2), byteorder="little", signed=True)
                entry["CATEGORY"] = readString(file)
                entry["UNK1"] = file.read(0x3C).hex().upper()
                entry["STRINGS"] = [readString(file), readString(file)]
                entry["UNK2"] = file.read(0x14).hex().upper()
            
            case "ItemHelpData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK"] = file.read(0x9).hex().upper()
            
            case "CourageousJumpData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
                entry["UNK"] = file.read(8).hex().upper()
                entry["STRING2"] = readString(file)
                entry["UNK2"] = file.read(0x1B).hex().upper()
            
            case "LinkAbText":
                entry["TYPE"] = type
                entry["UNK"] = int.from_bytes(file.read(1), byteorder="little")
                entry["STRINGS"] = [readString(file), readString(file)]
            
            case "MarkerTableData":
                entry["TYPE"] = type
                entry["UNK"] = file.read(6).hex().upper()
                entry["STRING"] = readString(file)
                entry["UNK2"] = file.read(9).hex().upper()
                entry["STRING2"] = readString(file)
                entry["UNK3"] = file.read(0xC).hex().upper()
            
            case "MG02Help":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRING"] = readString(file)
            
            case "status_p":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["STRINGS"] = [readString(file), readString(file), readString(file)]
                entry["UNK"] = file.read(0xB6).hex().upper()
                entry["STRING"] = readString(file)
                entry["UNK1"] = file.read(2).hex().upper()
            
            case "game_difficulty":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["OFFSET"] = int.from_bytes(file.read(2), byteorder="little", signed=True)
            
            case "CharData":
                entry["TYPE"] = type
                entry["ID"] = int.from_bytes(file.read(2), byteorder="little")
                entry["UNK"] = file.read(0x12).hex().upper()
                entry["STRING"] = readString(file)
            
            case _:
                print("UNKNOWN TYPE! %s" % type)
                sys.exit()
        
        if (len(entry) > 0):
            DUMP.append(entry)
    
    file.close()

    if (len(DUMP) > 0):
        file = open("jsons/%s.json" % files[i][3:-4], "w", encoding="UTF-8")
        json.dump(DUMP, file, indent="\t", ensure_ascii=False)
        file.close()
    else:
        print("MO STRINGS DETECTED!")