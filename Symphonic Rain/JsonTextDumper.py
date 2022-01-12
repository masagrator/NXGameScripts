import json
import os
import glob

files = glob.glob("jsons/*.json")

os.makedirs("jsons_texts", exist_ok=True)

for i in range(0, len(files)):
    file = open(files[i], "r", encoding="UTF-8")
    dump = json.load(file)
    file.close()

    textlist = {}
    textlist["TEXT"] = []
    textlist["SELECT"] = []
    for x in range(0, len(dump["COMMANDS"])):
        for y in range(0, len(dump["COMMANDS"][x])):
            match(dump["COMMANDS"][x][y]["TYPE"]):
                case "Text":
                    textlist["TEXT"].append(dump["COMMANDS"][x][y]["STRING"])
                case "Select":
                    textlist["SELECT"].append(dump["COMMANDS"][x][y]["STRINGS"])
    
    file_new = open("jsons_texts/%s" % files[i][6:], "w", encoding="UTF-8")
    json.dump(textlist, file_new, indent="\t", ensure_ascii=False)
    file_new.close()