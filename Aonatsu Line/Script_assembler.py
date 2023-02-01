import glob
import sys
from pathlib import Path
import os

STRINGS = []

def splitToList(string: str):
	return string[1:-1].split(",")

def AddToStrings(string: str):
	if (string[1:-1] not in STRINGS):
		index = len(STRINGS)
		STRINGS.append(string[1:-1])
	else:
		index = STRINGS.index(string[1:-1])
	return index

files = glob.glob(f"{sys.argv[1]}/*.asm")
os.makedirs("Compiled", exist_ok=True)

for i in range(0, len(files)):
	BASE = {}
	DUMP = []
	STRINGS = []
	STRINGS.append("")
	print(Path(files[i]).stem)
	file = open(files[i], "r", encoding="UTF-8")
	itr = 0
	for line in file:
		Args = line.strip().split("\t")
		if (Args[0][0] == ";"):
			continue
		if(Args[0][0:1] == "{"):
			value = int(Args[0][1:-1], base=16)
			if (("0x%04x" % value) in BASE):
				print("DETECTED IDENTICAL LABELS! CEASING OPERATION")
				print(Args[0])
				sys.exit()
			match(Args[1]):
				case "LOAD_STRING" | "LOAD_CUSTOM_TEXT" | "SET_EFFECT" | "SPECIAL_TEXT":
					BASE["0x%04x" % (value - 1)] = itr - 1
					BASE["0x%04x" % value] = itr
					itr += 2
				case _:
					if (len(Args) == 4):
						values = splitToList(Args[3])
						for z in range(1, len(values)+1):
							BASE["0x%04x" % (value - z)] = itr - z
						BASE["0x%04x" % value] = itr
						itr = itr + 1 + len(values)
					else:
						BASE["0x%04x" % value] = itr
						itr += 1
		else:
			match(Args[1]):
				case "LOAD_STRING" | "LOAD_CUSTOM_TEXT" | "SET_EFFECT" | "SPECIAL_TEXT":
					itr += 2
				case _:
					if (len(Args) == 4):
						values = splitToList(Args[3])
						itr = itr + 1 + len(values)
					else:
						itr += 1
	file.seek(0)
	for line in file:
		Args = line.strip().split("\t")
		if (Args[0][0] == ";"):
			continue
		elif (Args[1][0:3] == "CMD"):
			if (len(Args) == 4):
				values = splitToList(Args[3])
				for x in range(len(values)):
					DUMP.append(0x0.to_bytes(4, "little"))
					DUMP.append(int(values[x], base=16).to_bytes(4, "little"))
			DUMP.append(int(Args[1][4:], base=16).to_bytes(4, "little"))
			DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
		else: 
			match(Args[1]):
				case "INIT":
					DUMP.append(0x1B.to_bytes(4, "little"))
					DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
				case "DEINIT":
					DUMP.append(0x1C.to_bytes(4, "little"))
					DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
				case "CMPR0":
					DUMP.append(0x10.to_bytes(4, "little"))
					DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
				case "CMPR5":
					DUMP.append(0x15.to_bytes(4, "little"))
					DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
				case "CMPR7":
					DUMP.append(0x17.to_bytes(4, "little"))
					DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
				case "CMPR8":
					DUMP.append(0x18.to_bytes(4, "little"))
					DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
				case "CMPRA":
					DUMP.append(0x1A.to_bytes(4, "little"))
					DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
				case "JNGE":
					DUMP.append(0x41.to_bytes(4, "little"))
					DUMP.append(BASE[Args[2]].to_bytes(4, "little"))
				case "JNLE":
					DUMP.append(0x42.to_bytes(4, "little"))
					DUMP.append(BASE[Args[2]].to_bytes(4, "little"))
				case "INF1":
					if (len(Args) == 4):
						values = splitToList(Args[3])
						for x in range(len(values)):
							DUMP.append(0x0.to_bytes(4, "little"))
							DUMP.append(int(values[x], base=16).to_bytes(4, "little"))
					DUMP.append(0x1D.to_bytes(4, "little"))
					DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
				case "INF2":
					DUMP.append(0x2C.to_bytes(4, "little"))
					DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
				case "PUSH":
					if (len(Args) == 4):
						values = splitToList(Args[3])
						for x in range(len(values)):
							DUMP.append(0x0.to_bytes(4, "little"))
							DUMP.append(int(values[x], base=16).to_bytes(4, "little"))
					DUMP.append(0x5.to_bytes(4, "little"))
					DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
				case "CMPR":
					DUMP.append(0x18.to_bytes(4, "little"))
					DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
				case "LOAD_STRING":
					DUMP.append(0x0.to_bytes(4, "little"))
					DUMP.append(AddToStrings(Args[2]).to_bytes(4, "little"))
					DUMP.append(0x5.to_bytes(4, "little"))
					DUMP.append(0x1.to_bytes(4, "little"))
				case "PUSH_MESSAGE":
					DUMP.append(0x7.to_bytes(4, "little"))
					DUMP.append(0x4006f.to_bytes(4, "little"))
				case "FUNC":
					DUMP.append(0x7.to_bytes(4, "little"))
					match(Args[2]):
						case "'WAIT'":
							DUMP.append(0x20005.to_bytes(4, "little"))
						case "'PUSH_MESSAGE'":
							DUMP.append(0x4006f.to_bytes(4, "little"))
						case "'BG_FADE'":
							DUMP.append(0x2009A.to_bytes(4, "little"))
						case "'BG_PUSH'":
							DUMP.append(0x8803E.to_bytes(4, "little"))
						case "'VOICE_FADE'":
							DUMP.append(0x301C2.to_bytes(4, "little"))
						case "'TEX_CLEAR'":
							DUMP.append(0x2014f.to_bytes(4, "little"))
						case "'TEX_FADE'":
							DUMP.append(0x60165.to_bytes(4, "little"))
						case "'TEX_PUSH'":
							DUMP.append(0x90143.to_bytes(4, "little"))
						case "'BGM_PLAY'":
							DUMP.append(0x501b2.to_bytes(4, "little"))
						case "'SE_PLAY'":
							DUMP.append(0x501bf.to_bytes(4, "little"))
						case "'SYSTEM_VOICE_PLAY'":
							DUMP.append(0x601c0.to_bytes(4, "little"))
						case _:
							DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
				case "LOAD_CUSTOM_TEXT":
					DUMP.append(0x0.to_bytes(4, "little"))
					DUMP.append(AddToStrings(Args[3]).to_bytes(4, "little"))
					DUMP.append(0x6.to_bytes(4, "little"))
					DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
				case "PUSH_CUSTOM_TEXT":
					DUMP.append(0x9.to_bytes(4, "little"))
					DUMP.append(0x1.to_bytes(4, "little"))
				case "SET_EFFECT":
					DUMP.append(0x0.to_bytes(4, "little"))
					DUMP.append(AddToStrings(Args[3]).to_bytes(4, "little"))
					DUMP.append(0x4.to_bytes(4, "little"))
					DUMP.append(int(Args[2], base=16).to_bytes(4, "little"))
				case "SPECIAL_TEXT":
					DUMP.append(0x0.to_bytes(4, "little"))
					DUMP.append(AddToStrings(Args[3]).to_bytes(4, "little"))
					DUMP.append(0xE.to_bytes(4, "little"))
					value = int(Args[2], base=16) + 0x80000000
					DUMP.append(value.to_bytes(4, "little"))
				case _:
					print("Undetected command!")
					print(Args[1])
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