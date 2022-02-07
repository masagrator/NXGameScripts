import json
import glob
import os
import numpy

def GenerateData(entry):
    new_entry = []
    new_entry.append(entry["TYPE"].encode("UTF-8") + b"\x00")
    temp = []
    match(entry["TYPE"]):
        case "TextTableData":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
        case "ActiveVoiceTableData":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(entry["VOICE_FILE"].encode("UTF-8") + b"\x00")
            temp.append(numpy.uint32(entry["UNK0"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
            temp.append(numpy.float32(entry["UNK1"][0]))
            temp.append(numpy.float32(entry["UNK1"][1]))
            for i in range(0, 6):
                temp.append(numpy.uint16(entry["UNK2"][i]))

        case "QSChapter":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")

        case "QSBook":
            temp.append(numpy.uint16(entry["UNK0"]))
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
            temp.append(entry["BOOK"].encode("UTF-8") + b"\x00")
            temp.append(entry["BOOKDATA"].encode("UTF-8") + b"\x00")
            temp.append(numpy.uint16(entry["ID2"]))
        
        case "TacticalBonus":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
            temp.append(numpy.float32(entry["UNK0"]))
            temp.append(numpy.uint16(entry["UNK1"]))
        
        case "CardTableData":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
            temp.append(bytes.fromhex(entry["UNK0"]))
        
        case "dlc":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(entry["CONTENTID"].encode("UTF-8") + b"\x00")
            temp.append(entry["GROUPID"].encode("UTF-8") + b"\x00")
            temp.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
            temp.append(entry["STRINGS"][1].encode("UTF-8") + b"\x00")
        
        case "text_lst":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
        
        case "hkitugi_lst":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(numpy.uint16(entry["UNK0"]))
            temp.append(numpy.uint16(entry["UNK1"]))
            temp.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
            temp.append(entry["STRINGS"][1].encode("UTF-8") + b"\x00")
        
        case "item":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(numpy.int16(entry["UNK0"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
            temp.append(bytes.fromhex(entry["UNK1"]))
            temp.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
            temp.append(entry["STRINGS"][1].encode("UTF-8") + b"\x00")
        
        case "MapJumpData":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(numpy.uint16(entry["UNK0"]))
            temp.append(entry["STRING1"].encode("UTF-8") + b"\x00")
            temp.append(bytes.fromhex(entry["UNK1"]))
            temp.append(entry["STRING2"].encode("UTF-8") + b"\x00")
            temp.append(entry["STRING3"].encode("UTF-8") + b"\x00")
            temp.append(bytes.fromhex(entry["UNK2"]))
        
        case "LinkAbList":
            temp.append(numpy.uint16(entry["UNK0"]))
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(numpy.uint8(entry["UNK1"]))
            temp.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
            temp.append(entry["STRINGS"][1].encode("UTF-8") + b"\x00")
        
        case "magic":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(numpy.uint16(entry["UNK0"]))
            temp.append(entry["GROUP"].encode("UTF-8") + b"\x00")
            temp.append(bytes.fromhex(entry["UNK1"]))
            temp.append(entry["NAMEID"].encode("UTF-8") + b"\x00")
            temp.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
            temp.append(entry["STRINGS"][1].encode("UTF-8") + b"\x00")
        
        case "MG02Text":
            temp.append(numpy.uint16(entry["UNK0"]))
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(numpy.uint16(entry["UNK1"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
            temp.append(numpy.uint16(entry["UNK2"]))
            temp.append(numpy.int32(entry["UNK3"]))
        
        case "status":
            temp.append(entry["STRING1"].encode("UTF-8") + b"\x00")
            temp.append(entry["STRING2"].encode("UTF-8") + b"\x00")
            temp.append(entry["STRING3"].encode("UTF-8") + b"\x00")
            for i in range(0, 3):
                temp.append(numpy.float32(entry["UNK0"][i]))
            temp.append(bytes.fromhex(entry["UNK1"]))
            temp.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
            temp.append(entry["STRINGS"][1].encode("UTF-8") + b"\x00")
        
        case "MasterQuartzMemo":
            temp.append(numpy.uint16(entry["UNK0"]))
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
        
        case "NameTableData":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(entry["STRING1"].encode("UTF-8") + b"\x00")
            for i in range(0, 5):
                temp.append(entry["STRING2"][i].encode("UTF-8") + b"\x00")
        
        case "NaviTextData":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
            temp.append(bytes.fromhex(entry["UNK0"]))
        
        case "QSCook":
            temp.append(entry["STRING1"].encode("UTF-8") + b"\x00")
            temp.append(bytes.fromhex(entry["UNK0"]))
            temp.append(entry["STRINGS1"][0].encode("UTF-8") + b"\x00")
            temp.append(entry["STRINGS1"][1].encode("UTF-8") + b"\x00")
            temp.append(numpy.uint16(entry["UNK1"]))
            temp.append(entry["STRINGS2"][0].encode("UTF-8") + b"\x00")
            temp.append(entry["STRINGS2"][1].encode("UTF-8") + b"\x00")
            temp.append(numpy.uint16(entry["UNK2"]))
            temp.append(entry["STRINGS3"][0].encode("UTF-8") + b"\x00")
            temp.append(entry["STRINGS3"][1].encode("UTF-8") + b"\x00")
            temp.append(numpy.uint16(entry["UNK3"]))
            temp.append(entry["STRINGS4"][0].encode("UTF-8") + b"\x00")
            temp.append(entry["STRINGS4"][1].encode("UTF-8") + b"\x00")
            temp.append(bytes.fromhex(entry["UNK4"]))
        
        case "QSChar":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(bytes.fromhex(entry["UNK0"]))
            for i in range(0, 10):
                temp.append(entry["STRINGS"][i].encode("UTF-8") + b"\x00")
        
        case "QSFish":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(entry["STRING1"].encode("UTF-8") + b"\x00")
            temp.append(numpy.uint16(entry["UNK0"]))
            for i in range(0, 3):
                temp.append(numpy.float32(entry["UNK1"][i]))
            temp.append(bytes.fromhex(entry["UNK2"]))
            temp.append(entry["STRING2"].encode("UTF-8") + b"\x00")
            temp.append(bytes.fromhex(entry["UNK3"]))
        
        case "QSHelp":
            temp.append(numpy.uint16(entry["UNK0"]))
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
        
        case "PlaceTableData":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(numpy.uint16(entry["UNK0"]))
            temp.append(entry["NAMEID"].encode("UTF-8") + b"\x00")
            temp.append(entry["STRING1"].encode("UTF-8") + b"\x00")
            temp.append(entry["STRING2"].encode("UTF-8") + b"\x00")
        
        case "QSRank":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
            temp.append(bytes.fromhex(entry["UNK0"]))
        
        case "ShopTitle":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(numpy.uint8(entry["UNK0"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
            temp.append(bytes.fromhex(entry["UNK1"]))
        
        case "QSTitle":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(numpy.uint8(entry["UNK0"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
            temp.append(entry["CATEGORY"].encode("UTF-8") + b"\x00")
            temp.append(bytes.fromhex(entry["UNK1"]))
        
        case "QSText":
            temp.append(numpy.uint16(entry["ID"]))
            temp.append(numpy.uint8(entry["UNK0"]))
            temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
            temp.append(numpy.uint8(entry["UNK1"]))

        case _:
            temp.append(bytes.fromhex(entry["UNK"]))
    
    new_entry.append(numpy.uint16(len(b"".join(temp))))
    new_entry.append(b"".join(temp))
    return b"".join(new_entry)

files = glob.glob("text/json/*.json")

os.makedirs("text/new_nx", exist_ok=True)

for i in range(0, len(files)):
    file = open(files[i], "r", encoding="UTF-8")
    dump = json.load(file)
    file.close()

    OUTPUT = []
    for x in range(0, len(dump)):
        OUTPUT.append(GenerateData(dump[x]))
    
    file_new = open("text/new_nx/%s.tbl" % files[i][10:-5], "wb")
    file_new.write(numpy.uint16(len(dump)))
    file_new.write(b"".join(OUTPUT))
    file_new.close()