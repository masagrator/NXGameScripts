import os
import json
import glob

os.makedirs("jsons_new", exist_ok=True)

files = glob.glob("Text_extracted/*.json")
for i in range(0, len(files)):
    print(files[i])
    if (files[i][15:-5] == "0000"):
        continue
    file = open(files[i], "r", encoding="UTF-8")
    TEXT_DUMP = json.load(file)
    file.close()

    file = open("jsons/%s" % files[i][15:], "r", encoding="UTF-8")
    ORIG_DUMP = json.load(file)
    file.close()

    a = 0
    for x in range(0, len(ORIG_DUMP["COMMANDS"])):
        #print(ORIG_DUMP["COMMANDS"][x])
        match(ORIG_DUMP["COMMANDS"][x]["CMD"]):
            case "31":
                for y in range(0, len(ORIG_DUMP["COMMANDS"][x]["LIST"])):
                    ORIG_DUMP["COMMANDS"][x]["LIST"][y]["STRING"] = TEXT_DUMP[a]["STRINGS"][y]
                a += 1
            case "SELECT":
                for y in range(0, len(ORIG_DUMP["COMMANDS"][x]["LIST"])):
                    ORIG_DUMP["COMMANDS"][x]["LIST"][y]["STRING"] = TEXT_DUMP[a]["STRINGS"][y]
                a += 1
            case "VOICE":
                if (ORIG_DUMP["COMMANDS"][x]["TYPE"] == "WITH_TEXT"):
                    ORIG_DUMP["COMMANDS"][x]["STRING"] = TEXT_DUMP[a]["STRING"]
                    a += 1
            case "TEXT2":
                ORIG_DUMP["COMMANDS"][x]["STRING"] = TEXT_DUMP[a]["STRING"]
                a += 1
            case "TEXT":
                ORIG_DUMP["COMMANDS"][x]["STRING"] = TEXT_DUMP[a]["STRING"]
                a += 1
            case _:
                pass
    
    file = open("jsons_new/%s" % files[i][15:], "w", encoding="UTF-8")
    json.dump(ORIG_DUMP, file, indent="\t", ensure_ascii=False)
    file.close()