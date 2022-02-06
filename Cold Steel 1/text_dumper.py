import json
import os
import glob
import sys

files = glob.glob("jsons/*.json")

os.makedirs("Text_dumps", exist_ok=True)

for i in range(0, len(files)):
    file = open(files[i], "r", encoding="UTF-8")
    DUMP = json.load(file)
    file.close()

    OUTPUT = []

    FUNCTIONS = DUMP["FUNCTIONS"]

    keys = list(FUNCTIONS.keys())

    for x in range(0, len(keys)):
        FUNCTION = FUNCTIONS[keys[x]]

        for y in range(0, len(FUNCTION)):
            if (FUNCTION[y]["TYPE"] in ["0x13", "MESSAGE", "OVERRIDE_DIALOG_SPEAKER", "TEXT"]):
                OUTPUT.append(FUNCTION[y])
    
    if (len(OUTPUT) > 0):
        file_new = open("Text_dumps/%s.json" % files[i][6:-5], "w", encoding="UTF-8")
        json.dump(OUTPUT, file_new, indent="\t", ensure_ascii=False)
        file_new.close()