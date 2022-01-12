import glob
import json

files = glob.glob("jsons/*.json")

for i in range(0, len(files)):
    file = open(files[i], "r", encoding="UTF-8")
    DUMP = json.load(file)
    file.close()

    file = open("jsons_reformat/%s" % files[i][6:], "r", encoding="UTF-8")
    TEXTS = json.load(file)
    file.close()

    texts_itr = 0
    select_itr = 0
    for x in range(0, len(DUMP["COMMANDS"])):
        for a in range(0, len(DUMP["COMMANDS"][x])):
            if (DUMP["COMMANDS"][x][a]["TYPE"] == "Text"):
                DUMP["COMMANDS"][x][a]["STRING"] = TEXTS["TEXT"][texts_itr]
                texts_itr += 1
            elif (DUMP["COMMANDS"][x][a]["TYPE"] == "Select"):
                DUMP["COMMANDS"][x][a]["STRINGS"] = TEXTS["SELECT"][select_itr]
                select_itr += 1
    
    file_new = open("jsons_new/%s" % files[i][6:], "w", encoding="UTF-8")
    json.dump(DUMP, file_new, indent="\t", ensure_ascii=False)
    file_new.close()