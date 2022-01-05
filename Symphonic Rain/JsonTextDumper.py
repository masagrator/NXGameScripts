import json
import os
import glob

files = glob.glob("jsons/*.json")

os.makedirs("jsons_texts", exist_ok=True)

for i in range(0, len(files)):
    file = open(files[i], "r", encoding="UTF-8")
    dump = json.load(file)
    file.close()

    textlist = []
    for x in range(0, len(dump["COMMANDS"])):
        if (dump["COMMANDS"][x]["TYPE"] == "Text"):
            textlist.append(dump["COMMANDS"][x]["STRING"])
    
    file_new = open("jsons_texts/%s" % files[i][6:], "w", encoding="UTF-8")
    json.dump(textlist, file_new, indent="\t", ensure_ascii=False)
    file_new.close()