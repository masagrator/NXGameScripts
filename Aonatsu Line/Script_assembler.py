import glob
import sys
from pathlib import Path
import os

STRINGS = []
STRINGS.append("")

def splitToList(string: str):
	return string[1:-1].split(",")

def AddToStrings(string: str):
	print(string)
	print(string[1:-1])
	input()
	if (string[1:-1] not in STRINGS):
		index = len(STRINGS)
		STRINGS.append(string[1:-1])
	else:
		index = STRINGS.index(string[1:-1])
	return index

files = glob.glob(f"{sys.argv[1]}/*.asm")
os.makedirs("Compiled", exist_ok=True)

for i in range(0, len(files)):
	DUMP = []
	print(Path(files[i]).stem)
	file = open(files[i], "r", encoding="UTF-8")
	for line in file:
		Args = line.strip().split("\t")
		if (Args[0][0:3] == "CMD"):
			if (len(Args) == 3):
				values = splitToList(Args[2])
				for x in range(len(values)):
					DUMP.append(0x0.to_bytes(4, "little"))
					DUMP.append(int(values[x], base=16).to_bytes(4, "little"))
			DUMP.append(int(Args[0][4:], base=16).to_bytes(4, "little"))
			DUMP.append(int(Args[1], base=16).to_bytes(4, "little"))
		else: 
			match(Args[0]):
				case "LOAD_STRING":
					DUMP.append(0x0.to_bytes(4, "little"))
					DUMP.append(AddToStrings(Args[1]).to_bytes(4, "little"))
					DUMP.append(0x5.to_bytes(4, "little"))
					DUMP.append(0x1.to_bytes(4, "little"))
				case "PUSH_MESSAGE":
					DUMP.append(0x7.to_bytes(4, "little"))
					DUMP.append(0x4006f.to_bytes(4, "little"))
				case "LOAD_CUSTOM_TEXT":
					DUMP.append(0x0.to_bytes(4, "little"))
					DUMP.append(AddToStrings(Args[2]).to_bytes(4, "little"))
					DUMP.append(0x6.to_bytes(4, "little"))
					DUMP.append(int(Args[1], base=16).to_bytes(4, "little"))
				case "PUSH_CUSTOM_TEXT":
					DUMP.append(0x9.to_bytes(4, "little"))
					DUMP.append(0x1.to_bytes(4, "little"))
				case "SET_EFFECT":
					DUMP.append(0x0.to_bytes(4, "little"))
					DUMP.append(AddToStrings(Args[2]).to_bytes(4, "little"))
					DUMP.append(0x4.to_bytes(4, "little"))
					DUMP.append(int(Args[1], base=16).to_bytes(4, "little"))
				case _:
					print("Undetected command!")
					print(Args[0])
					sys.exit()

	new_file = open(f"Compiled/{Path(files[i]).stem}.binu8", "wb")
	new_file.write(b"\x00" * 4)
	new_file.write(int(len(DUMP)/2).to_bytes(4, "little"))
	new_file.write(b"".join(DUMP))
	new_file.write(len(STRINGS).to_bytes(4, "little"))
	for x in range(len(STRINGS)):
		string = STRINGS[x].encode("UTF-8") + b"\x00"
		new_file.write(len(string).to_bytes(4, "little"))
		new_file.write(string)
	new_file.close()