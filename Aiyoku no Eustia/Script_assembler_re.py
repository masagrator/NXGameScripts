import glob
import sys
from pathlib import Path
import os
import pyvips

STRINGS = []
voice = False
load_string_last_empty = False

font_use = False

def getStringLength(string: str, postprocess = False) -> int:
	if (postprocess == False):
		i = 1
		sep = 1
	else:
		i = 0
		sep = 0
	parsed_string = ""
	while(i < len(string) - sep):
		if i+sep == len(string):
			c = string[i:]
		else:
			c = string[i:i+1]
		if (c != "@"):
			parsed_string += c
			i += 1
			continue
		i += 1
		c = string[i:i+1]
		match(c):
			case "n": # Break line
				parsed_string += "&#10;"
				i += 1
			case "v": # Voice file, always added separately from voice number which is 5 digits
				i += 1
			case "r": # Text over text
				while(True):
					i += 1
					c = string[i:i+1]
					if (c == "@"):
						break
					parsed_string += c
				while(True):
					i += 1
					c = string[i:i+1]
					if (c == "@"):
						i += 1
						break
			case "b": #Bold(?) If it is, it seems Bold doesn't change width of text
				i += 1
			case "t": # Timed pause
				i += 1
				i += 4
			case "h": #Sprite change
				while(i < len(string)):
					i += 1
					c = string[i:i+1]
					if ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_".find(c) == -1):
						break
			case "k": # activate preloaded effect
				i += 1
			case "s": #Unknown
				i += 1
				i += 4
			case "e": #Unknown
				i += 1
			case "m": #Unknown
				i += 1
				i += 2
			case "d": #Unknown
				i += 1
			case "o":
				i += 1
				i += 3
			case _:
				print(f"Unknown case! Tag: {c}")
				print(f"String: {string}")
				print("Aborting...")
				sys.exit()
	parsed_string = parsed_string.replace("&", "&amp;")
	if (len(parsed_string) == 0):
		return 0
	try:
		img = pyvips.Image.text(parsed_string, dpi=159,fontfile=sys.argv[2])
	except Exception as exc:
		print("Something went wrong with text processing!")
		print("Original string:")
		print(string)
		print("Parsed string len: %d" % len(parsed_string))
		print(parsed_string)
		print(exc)
		print("Aborting...")
		sys.exit()
	return img.width

def splitToList(string: str):
	if (string[0:2] == "['" and string[-2:] == "']"):
		return [string[1:-1]]
	return string[1:-1].split(",")

def AddToStrings(string: str):
	string_check = string[1:-1].replace("\\n", "@n")
	if (string_check not in STRINGS):
		index = len(STRINGS)
		STRINGS.append(string_check)
	else:
		index = STRINGS.index(string_check)
	return index

if (len(sys.argv) < 3):
	print("Arguments are not valid!")
	print("Script_assembler_re.py [*.asm folder] [font filepath]")
	print("Files will be processed without autoadding break lines!")
else: font_use = True

files = glob.glob(f"{sys.argv[1]}/*.asm")
os.makedirs("Compiled", exist_ok=True)

text_width = 807

for i in range(0, len(files)):
	BASE = {}
	DUMP = []
	STRINGS = []
	STRINGS.append("")
	Extra = []
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
				print(Args)
				sys.exit()
			match(Args[1]):
				case "LOAD_STRING" | "LOAD_CUSTOM_TEXT" | "SET_EFFECT" | "CASE4":
					BASE["0x%04x" % (value + 1)] = itr + 1
					BASE["0x%04x" % value] = itr
					itr += 2
				case _:
					if (len(Args) == 4):
						values = splitToList(Args[3])
						for z in range(1, len(values)+1):
							BASE["0x%04x" % (value + z)] = itr + z
						BASE["0x%04x" % value] = itr
						itr = itr + 1 + len(values)
					else:
						BASE["0x%04x" % value] = itr
						itr += 1
		else:
			match(Args[1]):
				case "LOAD_STRING" | "LOAD_CUSTOM_TEXT" | "SET_EFFECT":
					itr += 2
				case "EXTRA":
					continue
				case _:
					if (len(Args) == 4):
						values = splitToList(Args[3])
						itr = itr + 1 + len(values)
					else:
						itr += 1
	file.seek(0)
	line = file.readlines()
	for iter in range(len(line)):
		Args = line[iter].strip().split("\t")
		if (len(Args) == 0 or Args[0][0] == ";"):
			continue
		elif (Args[1] == "CMD.43"):
				DUMP.append(0x43.to_bytes(4, "little"))
				DUMP.append(BASE["0x%04x" % (int(Args[2], base=16))].to_bytes(4, "little"))			
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
					if (len(Args) == 4):
						values = splitToList(Args[3])
						for x in range(len(values)):
							DUMP.append(0x0.to_bytes(4, "little"))
							DUMP.append(int(values[x], base=16).to_bytes(4, "little"))
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
					if (len(Args) == 4):
						values = splitToList(Args[3])
						for x in range(len(values)):
							DUMP.append(0x0.to_bytes(4, "little"))
							DUMP.append(int(values[x], base=16).to_bytes(4, "little"))
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
				case "CASE4":
					DUMP.append(0x0.to_bytes(4, "little"))
					DUMP.append(AddToStrings(Args[2]).to_bytes(4, "little"))
					DUMP.append(0x4.to_bytes(4, "little"))
					DUMP.append(0x0.to_bytes(4, "little"))
				case "LOAD_STRING":
					DUMP.append(0x0.to_bytes(4, "little"))
					if (font_use and len(Args[2]) > 32):
						width = getStringLength(Args[2][1:-1])
						if (width > text_width):
							string = []
							array = Args[2][1:-1].split( )
							line_count = 1
							b = 0
							a = 1
							while(a <= len(array)):
								width = getStringLength(" ".join(array[b:a]))
								if (width > text_width):
									string.append(" ".join(array[b:a-1]))
									string.append("\\n")
									line_count += 1
									b = a - 1
								else: a += 1
							string.append(" ".join(array[b:]))
							Args[2] = "'%s'" % "".join(string)
							if (line_count > 3):
								print("Detected %d lines" % line_count)
								print("".join(string))
					DUMP.append(AddToStrings(Args[2]).to_bytes(4, "little"))
					DUMP.append(0x5.to_bytes(4, "little"))
					DUMP.append(0x1.to_bytes(4, "little"))
				case "FUNC":
					DUMP.append(0x7.to_bytes(4, "little"))
					match(Args[2]):
						case "'PUSH_NAME'":
							DUMP.append(0x40070.to_bytes(4, "little"))
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
					values = splitToList(Args[3])
					DUMP.append(0x0.to_bytes(4, "little"))
					if (font_use and len(values[0]) > 32):
						width = getStringLength(values[0][1:-1])
						if (width > text_width):
							string = []
							array = values[0][1:-1].split( )
							b = 0
							a = 1
							while(a <= len(array)):
								width = getStringLength(" ".join(array[b:a]))
								if (width > text_width):
									string.append(" ".join(array[b:a-1]))
									string.append("\\n")
									b = a - 1
								else: a += 1
							string.append(" ".join(array[b:]))
							values[0] = "'%s'" % "".join(string)
					DUMP.append(AddToStrings(values[0]).to_bytes(4, "little"))							
					DUMP.append(0xE.to_bytes(4, "little"))
					DUMP.append((int(Args[2], base=16)).to_bytes(4, "little"))
				case "EXTRA":
					Extra = splitToList(Args[2])
				case _:
					print("Undetected command!")
					print(Args[1])
					print(Args[0])
					sys.exit()

	new_file = open(f"Compiled/{Path(files[i]).stem}.binu8", "wb")
	new_file.write(int(len(Extra)/2).to_bytes(4, "little"))
	for x in range(len(Extra)):
		new_file.write(int(Extra[x], base=16).to_bytes(4, "little"))
	new_file.write(int(len(DUMP)/2).to_bytes(4, "little"))
	new_file.write(b"".join(DUMP))
	new_file.write(len(STRINGS).to_bytes(4, "little"))
	for x in range(len(STRINGS)):
		string = STRINGS[x].encode("UTF-8") + b"\x00"
		new_file.write(len(string).to_bytes(4, "little"))
		new_file.write(string)
	new_file.close()