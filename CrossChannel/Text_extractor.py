import os
import json

OUTPUT = []

os.makedirs("Text_extracted", exist_ok=True)

for i in range(0, 316):
    file = open("jsons/%04d.json" % i, "r", encoding="UTF-8")
    dump = json.load(file)["COMMANDS"]
    file.close()

    entry = []
    for x in range(0, len(dump)):
        entry2 = {}
        match(dump[x]["CMD"]):
            case "31":
                entry2["TYPE"] = "SELECT2"
                entry3 = []
                for y in range(0, len(dump[x]["LIST"])):
                    entry3.append(dump[x]["LIST"][y]["STRING"])
                entry2["STRINGS"] = entry3
            case "SELECT":
                entry2["TYPE"] = "SELECT"
                entry3 = []
                for y in range(0, len(dump[x]["LIST"])):
                    entry3.append(dump[x]["LIST"][y]["STRING"])
                entry2["STRINGS"] = entry3
            case "VOICE":
                if (dump[x]["TYPE"] != "WITH_TEXT"):
                    continue
                entry2["TYPE"] = "VOICE"
                entry2["STRING"] = dump[x]["STRING"]
            case "TEXT2":
                entry2["TYPE"] = "TEXT2"
                entry2["STRING"] = dump[x]["STRING"]
            case "TEXT":
                entry2["TYPE"] = "TEXT"
                if (dump[x]["TYPE"] == "MESSAGE"):
                    entry2["SUBTYPE"] = "MESSAGE"
                else:
                    entry2["SUBTYPE"] = "NAME"
                entry2["STRING"] = dump[x]["STRING"]
            case _:
                continue
        if (len(entry2) != 0):
            entry.append(entry2)
    if (len(entry) > 0):
        file_new = open("Text_extracted/%04d.json" % i, "w", encoding="UTF-8")
        json.dump(entry, file_new, indent="\t", ensure_ascii=False)
        file_new.close()