import glob
import os
import json

files = glob.glob("scenario/*.json")

os.makedirs("DUMP", exist_ok=True)
os.makedirs("DUMP_NO_TAGS", exist_ok=True)
for i in range(len(files)):
	print(files[i])
	NEW_DUMP = []
	NEW_DUMP_TEXTS = []
	file = open(files[i], "r", encoding="UTF-8")
	DUMP = json.load(file)
	file.close()
	ID = 0
	for x in range(len(DUMP)):
		if (DUMP[x]["TYPE"] == "DEMO"):
			ID = DUMP[x]["FILE_ID"]
			continue
		elif (DUMP[x]["TYPE"] == "JUMP"):
			NEW_DUMP.append(["`\JUMP TO FILE: %d\`" % DUMP[x]["FILE_ID"]])
			continue
		elif (DUMP[x]["TYPE"] != "PAGE"):
			continue
		entry = []
		entry2 = []
		msg_count = 0
		for y in range(len(DUMP[x]["COMMANDS"])):
			if DUMP[x]["COMMANDS"][y]["TYPE"] == "MESSAGE": msg_count += 1
		msg_count2 = 0
		for y in range(len(DUMP[x]["COMMANDS"])):
			if (DUMP[x]["COMMANDS"][y]["TYPE"] == "BR" and isinstance(DUMP[x]["COMMANDS"][y]["ARGS"], str) == True): 
				entry.append("`\%s\`" % DUMP[x]["COMMANDS"][y]["ARGS"])
				if (DUMP[x]["COMMANDS"][y]["ARGS"] in ["BREAK_LINE", "PRESS_TO_BREAK_LINE"]): entry2.append("\\n")
				continue
			if (DUMP[x]["COMMANDS"][y]["TYPE"] == "KEYWORD"): 
				entry.append("`\KEYWORD:%d\`" % DUMP[x]["COMMANDS"][y]["KEYWORD_ID"])
				continue
			if (DUMP[x]["COMMANDS"][y]["TYPE"] == "RUBY"): 
				entry.append("`\RUBY:%s\`" % DUMP[x]["COMMANDS"][y]["STRING"])
				continue
			if (DUMP[x]["COMMANDS"][y]["TYPE"] == "RUBYtm"): 
				entry.append("`\RUBYtm\`")
				continue
			if DUMP[x]["COMMANDS"][y]["TYPE"] == "MESSAGE":
				if (DUMP[x]["COMMANDS"][y-1]["TYPE"] == "MESSAGE"):
					entry.append("``")
				entry.append(DUMP[x]["COMMANDS"][y]["STRING"])
				entry2.append(DUMP[x]["COMMANDS"][y]["STRING"])
				msg_count2 += 1
				continue
			if (msg_count2 == 0):
				continue
			if msg_count2 == msg_count: break
			else: entry.append("`\%s\`" % DUMP[x]["COMMANDS"][y]["TYPE"])
		NEW_DUMP.append(entry)
		NEW_DUMP_TEXTS.append(entry2)
	new_file = open("DUMP/%d.md" % ID, "w", encoding="UTF-8")
	for x in range(len(NEW_DUMP)):
		new_file.write("".join(NEW_DUMP[x]))
		new_file.write("\n")
	new_file.close()
	new_file = open("DUMP_NO_TAGS/%d.txt" % ID, "w", encoding="UTF-8")
	for x in range(len(NEW_DUMP_TEXTS)):
		new_file.write("".join(NEW_DUMP_TEXTS[x]))
		new_file.write("\n")
	new_file.close()