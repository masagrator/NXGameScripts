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
		case 0:
			return Disassemble.NOP()
		
		case 1:
			return Disassemble.GetU32(file)
		
		case 2:
			return Disassemble.POP()
		
		case 3:
			return Disassemble.JMP(file)
		
		case 4:
			return Disassemble.JZ(file)
		
		case 6:
			return Disassemble.CALL()
		
		case 8:
			return Disassemble.DUP()
		
		case 0xB:
			return Disassemble.SWAP2()
		
		case 0xE:
			return Disassemble.RET()
		
		case 0x10:
			return Disassemble.LNOT()
		
		case 0x1B:
			return Disassemble.GE()
		
		case 0x1C:
			return Disassemble.EQ()
		
		case 0x1D:
			return Disassemble.NE()
		
		case 0x1F:
			return Disassemble.LOR()
		
		case 0x20:
			return Disassemble.SETF()
		
		case 0x21:
			return Disassemble.GETF()
		
		case 0x22:
			return Disassemble.SETSF()
		
		case 0x23:
			return Disassemble.GETSF()
		
		case 0x2A:
			return Disassemble.SETRES()

		case 0x2B:
			return Disassemble.GETRES()
		
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
		
		case 0x4D:
			return Disassemble.VoicePos()
		
		case 0x50:
			return Disassemble.BGMVol()
		
		case 0x54:
			return Disassemble.SEPlay()
		
		case 0x5C:
			return Disassemble.SetBG()
		
		case 0x5E:
			return Disassemble.SetBlack()
		
		case 0x61:
			return Disassemble.Fade()
		
		case 0x62:
			return Disassemble.FadeBGtoSetBG()
		
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
		
		case 0x71:
			return Disassemble.GetWeek()
		
		case 0x72:
			return Disassemble.SetTime()
		
		case 0x76:
			return Disassemble.SetWeather()
		
		case 0x78:
			return Disassemble.Select()
		
		case 0x79:
			return Disassemble.ShowOpening()
		
		case 0x7C:
			return Disassemble.MiniGame()
		
		case 0x7D:
			return Disassemble.UNK_x7D()

		case 0x7F:
			return Disassemble.UNK_x7F()

		case 0x80:
			return Disassemble.MapMove()
		
		case 0x82:
			return Disassemble.AddMin()
		
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
		
		case 0x95:
			return Disassemble.AddRainPower()
		
		case _:
			print("UNKNOWN COMMAND!")
			print("Offset: 0x%x" % (file.tell() - 2))
			print("ID: 0x%x" % ID)
			sys.exit()
		

file = open(sys.argv[1], "rb")

if (file.read(0x4) != b"SR10"): #0x0
	print("WRONG MAGIC!")
	sys.exit()

Main = {}
Main["HEADER"] = {}

SIZE = int.from_bytes(file.read(0x4), byteorder="little") #0x4
Main["HEADER"]["FILE_ID"] = int.from_bytes(file.read(0x4), byteorder="little") #0x8
Main["HEADER"]["CRC"] = file.read(0x4).hex().upper() #0xC
registration_offset = int.from_bytes(file.read(0x4), byteorder="little") #0x10
registration_size = int.from_bytes(file.read(0x4), byteorder="little") #0x14
registration_entries = int.from_bytes(file.read(0x4), byteorder="little") #0x18
command_block_offset = int.from_bytes(file.read(0x4), byteorder="little") #0x1C
command_block_size = int.from_bytes(file.read(0x4), byteorder="little") #0x20
command_block_entries = int.from_bytes(file.read(0x4), byteorder="little") #0x24
text_block_registration_offset = int.from_bytes(file.read(0x4), byteorder="little") #0x28
text_block_registration_size = int.from_bytes(file.read(0x4), byteorder="little") #0x2C
text_block_registration_entries = int.from_bytes(file.read(0x4), byteorder="little") #0x30
text_blob_start = int.from_bytes(file.read(0x4), byteorder="little") #0x34
text_blob_size = int.from_bytes(file.read(0x4), byteorder="little") #0x38
text_count = int.from_bytes(file.read(0x4), byteorder="little") #0x3C

file.seek(registration_offset)
Main["HEADER"]["REGISTRATION_BLOCK"] = []
for i in range(0, registration_entries):
	entry = {}
	temp = file.tell()
	block_size = int.from_bytes(file.read(0x2), byteorder="little")
	entry["ID"] = int.from_bytes(file.read(0x4), byteorder="little")
	string_size = int.from_bytes(file.read(0x2), byteorder="little")
	entry["UNK1"] = int.from_bytes(file.read(0x2), byteorder="little")
	entry["UNK2"] = int.from_bytes(file.read(0x2), byteorder="little")
	entry["UNK3"] = int.from_bytes(file.read(0x2), byteorder="little")
	entry["UNK4"] = int.from_bytes(file.read(0x2), byteorder="little")
	entry["UNK5"] = int.from_bytes(file.read(0x2), byteorder="little")
	entry["UNK6"] = int.from_bytes(file.read(0x2), byteorder="little")
	entry["UNK7"] = int.from_bytes(file.read(0x2), byteorder="little")
	entry["STRING"] = readString(file)
	Main["HEADER"]["REGISTRATION_BLOCK"].append(entry)
	file.seek(temp+block_size)

file.seek(command_block_offset)
block_size = int.from_bytes(file.read(0x4), byteorder="little")

string_size = int.from_bytes(file.read(0x2), byteorder="little")
commands_blob_size = int.from_bytes(file.read(0x4), byteorder="little")
temp = file.tell()
Main["HEADER"]["FUN_1"] = readString(file)
file.seek(temp + string_size)

Main["COMMANDS"] = []

CMD_blob_end = file.tell() + commands_blob_size
while(file.tell() < CMD_blob_end):
	ID = int.from_bytes(file.read(0x2), byteorder="little")
	check = ProcessCommands(ID, file)
	if (check != None):
		Main["COMMANDS"].append(check)

file.seek(text_block_registration_offset)
Main["HEADER"]["BLOCK_2_STRINGS"] = []
for i in range(0, text_block_registration_entries):
	block_size = int.from_bytes(file.read(0x2), byteorder="little")
	CMD = int.from_bytes(file.read(0x2), byteorder="little")
	if (CMD != 0x3):
		print("Registration Assert Failed!")
		print("0x%x" % file.tell())
		sys.exit()
	Main["HEADER"]["BLOCK_2_STRINGS"].append(readString(file))

file.seek(text_blob_start)

Texts = []
Texts.append("DUMMY")

for i in range(0, text_count):
	temp = file.tell()
	temp += int.from_bytes(file.read(0x2), byteorder="little")
	Texts.append(readString(file))
	file.seek(temp)


for i in range(0, len(Main["COMMANDS"])):
	if (Main["COMMANDS"][i]["TYPE"] == "Text"):
		ID = Main["COMMANDS"][i]["U32"][0]
		Main["COMMANDS"][i].pop("U32")
		Main["COMMANDS"][i]["STRING"] = Texts[ID]

os.makedirs("jsons", exist_ok=True)
new_file = open("jsons/%s.json" % sys.argv[1][:-4], "w", encoding="UTF-8")
json.dump(Main, new_file, indent="\t", ensure_ascii=False)