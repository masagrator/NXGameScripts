import glob
import os
import json
import sys
from pathlib import Path

files = glob.glob("DUMP/*.md")

os.makedirs("Patched", exist_ok=True)
for i in range(len(files)):
	print(files[i])
	file = open(files[i], "r", encoding="UTF-8")
	DUMP = file.readlines()
	file.close()
	DUMP_TAGS = []
	for x in range(len(DUMP)):
		DUMP_TAGS.append(DUMP[x].replace("\n", "").split('`'))
		DUMP_TAGS[-1][:] = [x for x in DUMP_TAGS[-1] if x]
	file = open("scenario/%s.json" % Path(files[i]).stem, "r", encoding="UTF-8")
	JSON_DUMP = json.load(file)
	file.close()

	index = 0
	for x in range(len(JSON_DUMP)):
		if (JSON_DUMP[x]["TYPE"] == "JUMP"):
			index += 1
			continue
		if (JSON_DUMP[x]["TYPE"]) != "PAGE":
			continue
		message_was = False
		tag_index = 0
		for y in range(len(JSON_DUMP[x]["COMMANDS"])):
			if (y >= (len(DUMP_TAGS[index]))):
				break
			if (JSON_DUMP[x]["COMMANDS"][y]["TYPE"] == "MESSAGE"):
				if (DUMP_TAGS[index][tag_index][0:1] == "\\"):
					print(JSON_DUMP[x]["COMMANDS"][y])
					print(DUMP_TAGS[index])
					print("WRONG FORMATTING 1st!")
					print("MD LINE: %d" % (index + 1))
					print("JSON ENTRY INDEX: %d" % x)
					print("PAGE COMMAND INDEX: %d" % y)
					print("EXPECTED MESSAGE, GOT: %s" % DUMP_TAGS[index][tag_index])
					sys.exit()
				JSON_DUMP[x]["COMMANDS"][y]["ENG"] = DUMP_TAGS[index][tag_index]
				message_was = True
			elif (JSON_DUMP[x]["COMMANDS"][y]["TYPE"] == "RUBY"):
				if (DUMP_TAGS[index][tag_index][0:6] != "\\RUBY:" or DUMP_TAGS[index][tag_index][-1] != "\\"):
					print(JSON_DUMP[x]["COMMANDS"][y])
					print("WRONG FORMATTING 2nd!")
					print("MD LINE: %d" % (index + 1))
					print("JSON ENTRY INDEX: %d" % x)
					print("PAGE COMMAND INDEX: %d" % y)
					print("EXPECTED RUBY, GOT: %s" % DUMP_TAGS[index][tag_index])
					sys.exit()
				JSON_DUMP[x]["COMMANDS"][y]["ENG"] = DUMP_TAGS[index][tag_index][6:-1]
			elif (JSON_DUMP[x]["COMMANDS"][y]["TYPE"] == "BR"):
				if (DUMP_TAGS[index][tag_index] != "\\" + JSON_DUMP[x]["COMMANDS"][y]["ARGS"] + "\\"):
					print(JSON_DUMP[x]["COMMANDS"][y])
					print(DUMP_TAGS[index])
					print("WRONG FORMATTING 3th!")
					print("MD LINE: %d" % (index + 1))
					print("JSON ENTRY INDEX: %d" % x)
					print("PAGE COMMAND INDEX: %d" % y)
					print("EXPECTED BREAK_LINE:, GOT: %s" % DUMP_TAGS[index][tag_index])
					sys.exit()
			elif (JSON_DUMP[x]["COMMANDS"][y]["TYPE"] == "KEYWORD"):
				if (DUMP_TAGS[index][tag_index][0:9] != "\\KEYWORD:" or DUMP_TAGS[index][tag_index][-1] != "\\"):
					print(JSON_DUMP[x]["COMMANDS"][y])
					print("WRONG FORMATTING 5!")
					print("MD LINE: %d" % (index + 1))
					print("JSON ENTRY INDEX: %d" % x)
					print("PAGE COMMAND INDEX: %d" % y)
					print("EXPECTED KEYWORD, GOT: %s" % DUMP_TAGS[index][tag_index])
					sys.exit()
			else:
				if (message_was == False):
					continue
				if (JSON_DUMP[x]["COMMANDS"][y]["TYPE"] != DUMP_TAGS[index][tag_index][1:-1]):
					print(JSON_DUMP[x]["COMMANDS"][y])
					print("WRONG FORMATTING 4th!")
					print("MD LINE: %d" % (index + 1))
					print("JSON ENTRY INDEX: %d" % x)
					print("PAGE COMMAND INDEX: %d" % y)
					print("EXPECTED %s, GOT: %s" % (JSON_DUMP[x]["COMMANDS"][y]["TYPE"], DUMP_TAGS[index][tag_index]))
					sys.exit()
			tag_index += 1
		index += 1
	file = open("Patched/%s.json" % Path(files[i]).stem, "w", encoding="UTF-8")
	json.dump(JSON_DUMP, file, indent="\t", ensure_ascii=False)
	file.close()