import sys
import glob
import os
from pathlib import Path
from enum import Enum
import json

charset = []

def checkMagic(file):
	if (file.read(4) != b"MES\x00"):
		print("WRONG MAGIC!")
		sys.exit()

def checkVersion(file):
	if (int.from_bytes(file.read(4), "little") != 1):
		print("WRONG VERSION!")
		sys.exit()

def getSize(file):
	temp_pos = file.tell()
	file.seek(0, 2)
	size = file.tell()
	file.seek(temp_pos)
	return size

class Commands(Enum):
	LineBreak = 0x0
	NameStart = 0x1
	LineStart = 0x2
	Present_1 = 0x3
	Color = 0x4
	Present_2 = 0x5
	PresentReset = 0x8
	RubyBaseStart = 0x9
	RubyTextStart = 0xA
	RubyTextEnd = 0xB
	FontSize = 0xC
	Parallel = 0xE
	Center = 0xF
	MarginTop = 0x11
	MarginLeft = 0x12
	HardcodedValue = 0x13
	Eval = 0x15
	UNK_x18 = 0x18
	AutoForward_1 = 0x19
	AutoForward_2 = 0x1A
	RubyCenterPerChar = 0x1E
	AltLineBreak = 0x1F
	Terminator = 0xFF

def processString(file, string_size: int):
	i = 0
	entry = []
	while (i < string_size):
		c = file.read(1)
		i += 1
		check = int.from_bytes(c, "little", signed=False) 
		values = [member.value for member in Commands]
		if (check in values):
			match(check):
				case Commands.LineBreak.value: entry.append("<br>")
				case Commands.NameStart.value: entry.append("<name>")
				case Commands.LineStart.value: entry.append("<lineStart>")
				case Commands.Present_1.value: entry.append("<pr1>")
				case Commands.Color.value: 
					type = int.from_bytes(file.read(1), "little")
					if (type == 0xA0):
						entry.append("<color hex=%x>" % int.from_bytes(file.read(3), "big"))
						i += 4
					else:
						entry.append("<color id=%d>" % type)
						file.seek(2, 1)
						i += 3
				case Commands.Present_2.value: entry.append("<pr2>")
				case Commands.PresentReset.value: entry.append("</pr>")
				case Commands.Parallel.value: entry.append("<parallel>")
				case Commands.RubyBaseStart.value: entry.append("<rubybase>")
				case Commands.RubyTextStart.value: entry.append("<rubytext>")
				case Commands.RubyTextEnd.value: entry.append("</rubytext>")
				case Commands.RubyCenterPerChar.value: entry.append("</rubycpc>")
				case Commands.Eval.value:
					string = "<eval="
					while(True):
						temp = file.read(1)
						i += 1
						if int.from_bytes(temp, "little") == 0:
							temp = file.read(1)
							i += 1
							string += "00"
							if int.from_bytes(temp, "little") == 0:
								string += "00>"
								break
							else:
								string += temp.hex()
						else:
							string += temp.hex()
					entry.append(string)
				case Commands.FontSize.value:
					fontsize =  int.from_bytes(file.read(2), "little")
					entry.append("<fontsize=%d>" % fontsize)
					i += 2
				case Commands.Terminator.value: entry.append("\f")
				case Commands.UNK_x18.value: entry.append("<x18>")
				case Commands.AltLineBreak.value: entry.append("<altbr>")
				case Commands.AutoForward_1.value: entry.append("<afw1>")
				case _:
					print("Command not implemented: 0x%x" % check)
					print("offset: 0x%x" % (file.tell() - 1))
					sys.exit()
		else:
			c += file.read(1)
			index = int.from_bytes(c, "big") & 0x7FFF
			i += 1
			if (0xF8FF >= int.from_bytes(charset[index].encode("UTF-16-LE"), "little") >= 0xE000):
				entry.append("<compound=\\u%02X>" % int.from_bytes(charset[index].encode("UTF-16-LE"), "little"))
				print("Detected unknown compound: 0x%02X at offset: 0x%x" % (int.from_bytes(charset[index].encode("UTF-16-LE"), "little"), file.tell() - 2))
			try:
				entry.append(charset[index])
			except Exception:
				print("Decoding failed!")
				print("offset: 0x%x" % (file.tell() - 2))
				sys.exit()

	return "".join(entry)



files = glob.glob("%s/*.msb" % sys.argv[1])

charset_file = open("charset.utf8", "r", encoding="UTF-8")
charset_file.seek(0, 2)
charset_size = charset_file.tell()
charset_file.seek(0)
for i in range(charset_size):
	charset.append(charset_file.read(1))
charset_file.close()

for file in files:
	print(Path(file).stem)
	og_file = open(file, "rb")
	checkMagic(og_file)
	checkVersion(og_file)
	file_size = getSize(og_file)
	stringCount = int.from_bytes(og_file.read(4), "little")
	if (stringCount == 0):
		print("Strings not detected, ignoring...")
		continue
	stringsBlockOffset = int.from_bytes(og_file.read(4), "little")

	stringInfo = []
	for x in range(stringCount):
		ID = int.from_bytes(og_file.read(4), "little")
		offset = int.from_bytes(og_file.read(4), "little")
		stringInfo.append((ID, offset))
	
	DUMP = []
	for x in range(stringCount):
		og_file.seek(stringsBlockOffset + stringInfo[x][1])
		entry = {}
		entry["ID"] = stringInfo[x][0]
		if (x+1 == stringCount):
			string_size = file_size - stringInfo[x][1]
		else:
			string_size = stringInfo[x+1][1] - stringInfo[x][1]
		entry["String"] = processString(og_file, string_size)
		DUMP.append(entry)
	
	og_file.close()
	os.makedirs("Extracted", exist_ok=True)
	new_file = open("Extracted/%s.json" % Path(file).stem, "w", encoding="UTF-8")
	json.dump(DUMP, new_file, indent="\t", ensure_ascii=False)
	new_file.close()