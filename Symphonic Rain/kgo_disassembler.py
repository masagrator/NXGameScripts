import sys
import os
import json
from kgo_commands import *

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("UTF-8"))
		chars.append(c)

def ProcessCommands(ID, file):
	match(ID):
		case 1:
			return Disassemble.GetU32(file)
		
		case 2:
			return Disassemble.CMD_x2()
		
		case 8:
			return Disassemble.CMD_x8()
		
		case 0xB:
			return Disassemble.CMD_xB()
		
		case 0xE:
			return Disassemble.CMD_xE()
		
		case 0x10:
			return Disassemble.CMD_x10()
		
		case 0x22:
			return Disassemble.SETSF()
		
		case 0x23:
			return Disassemble.GETSF()
		
		case 0x30:
			return Disassemble.SCNCHG()

		case 0x40:
			return Disassemble.Text()
		
		case 0x41:
			return Disassemble.NewLine()
		
		case 0x42:
			return Disassemble.NewPage()
		
		case 0x43:
			return Disassemble.TextShow()
		
		case 0x44:
			return Disassemble.TextHide()
		
		case 0x45:
			return Disassemble.TextSpeed()
		
		case 0x46:
			return Disassemble.NovelMode()

		case 0x47:
			return Disassemble.Locate()
		
		case 0x48:
			return Disassemble.Wait()
		
		case 0x49:
			return Disassemble.KeyWait()
		
		case 0x4A:
			return Disassemble.SkipDisable()
		
		case 0x4B:
			return Disassemble.Voice()
		
		case 0x50:
			return Disassemble.BGMVol()
		
		case 0x54:
			return Disassemble.SEPlay()
		
		case 0x5E:
			return Disassemble.SetBlack()
		
		case 0x61:
			return Disassemble.Fade()
		
		case 0x62:
			return Disassemble.SetBG()
		
		case 0x64:
			return Disassemble.BlackOut()
		
		case 0x65:
			return Disassemble.MoveChar()
		
		case 0x66:
			return Disassemble.HideChar()
		
		case 0x68:
			return Disassemble.AllHideChar()
		
		case 0x6C:
			return Disassemble.ShowPlace()
		
		case 0x72:
			return Disassemble.SetTime()
		
		case 0x76:
			return Disassemble.SetWeather()
		
		case 0x79:
			return Disassemble.ShowOpening()
		
		case 0x83:
			return Disassemble.RainVol()
		
		case 0x86:
			return Disassemble.DateShow()
		
		case 0x87:
			return Disassemble.DateHide()
		
		case 0x88:
			return Disassemble.TimeShow()
		
		case 0x89:
			return Disassemble.TimeHide()
		
		case 0x8A:
			return Disassemble.BGMPlay()
		
		case 0x8B:
			return Disassemble.BGMStop()
		
		case 0x8C:
			return Disassemble.SongPlay()
		
		case 0x8E:
			return Disassemble.EnvPlay()
		
		case 0x8F:
			return Disassemble.EnvStop()
		
		case 0x90:
			return Disassemble.SongEnable() #Guessed
		
		case 0x91:
			return Disassemble.SetRainPower()
		
		case _:
			print("UNKNOWN COMMAND!")
			print("Offset: 0x%x" % (file.tell() - 2))
			print("ID: 0x%x" % ID)
			sys.exit()
		

file = open(sys.argv[1], "rb")

if (file.read(0x4) != b"SR10"):
	print("WRONG MAGIC!")
	sys.exit()

Size = int.from_bytes(file.read(0x4), byteorder="little")
file.seek(4, 1)
CRC = file.read(0x4)
registration_offset = int.from_bytes(file.read(0x4), byteorder="little")
file.seek(8, 1)
command_block_offset = int.from_bytes(file.read(0x4), byteorder="little")
command_block_size = int.from_bytes(file.read(0x4), byteorder="little")
file.seek(4, 1)
text_block_registration_offset = int.from_bytes(file.read(0x4), byteorder="little")
file.seek(12, 1)
text_block_size = int.from_bytes(file.read(0x4), byteorder="little")
text_count = int.from_bytes(file.read(0x4), byteorder="little")

file.seek(registration_offset)
block_size = int.from_bytes(file.read(0x2), byteorder="little")
file.seek(4, 1)
string_size = int.from_bytes(file.read(0x2), byteorder="little")
file.seek(0xE, 1)
Registration_name = readString(file)

file.seek(command_block_offset)
block_size = int.from_bytes(file.read(0x4), byteorder="little")
if (block_size != command_block_size):
	print("BLOCK SIZE ASSERT FAILED!")
	sys.exit()

string_size = int.from_bytes(file.read(0x2), byteorder="little")
commands_blob_size = int.from_bytes(file.read(0x4), byteorder="little")
temp = file.tell()
Function_name = readString(file)
file.seek(temp + string_size)

DUMP = []

CMD_blob_end = file.tell() + commands_blob_size
while(file.tell() < CMD_blob_end):
	ID = int.from_bytes(file.read(0x2), byteorder="little")
	check = ProcessCommands(ID, file)
	if (check != None):
		DUMP.append(check)

file.seek(text_block_registration_offset)
file.seek(2, 1)
string_size = int.from_bytes(file.read(0x2), byteorder="little")
string = readString(file)
while (file.tell() % 16 != 0):
	file.seek(1, 1)

Texts = []
Texts.append("DUMMY")

for i in range(0, text_count):
	temp = file.tell()
	temp += int.from_bytes(file.read(0x2), byteorder="little")
	Texts.append(readString(file))
	file.seek(temp)


for i in range(0, len(DUMP)):
	if (DUMP[i]["TYPE"] == "Text"):
		ID = DUMP[i]["U32"][0]
		DUMP[i].pop("U32")
		DUMP[i]["STRING"] = Texts[ID]

new_file = open("jsons/%s.json" % sys.argv[1][:-4], "w", encoding="UTF-8")
json.dump(DUMP, new_file, indent="\t", ensure_ascii=False)