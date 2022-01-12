import sys
import os
import json
import glob
from kgo_commands import *

def ProcessCommands(dict, Offsets = None):
	match(dict["TYPE"]):
		
		case "POP":
			return Assemble.POP(dict)
		
		case "JMP":
			if (Offsets == None):
				offset = 4
			else:
				offset = Offsets[dict["JUMP_TO_LABEL"]] - Offsets[dict["LABEL"]]
			return Assemble.JMP(dict, offset)
		
		case "JZ":
			if (Offsets == None):
				offset = 4
			else:
				offset = Offsets[dict["JUMP_TO_LABEL"]] - Offsets[dict["LABEL"]]
			return Assemble.JZ(dict, offset)
		
		case "CALL":
			return Assemble.CALL(dict)
		
		case "DUP":
			return Assemble.DUP(dict)
		
		case "SWAP2":
			return Assemble.SWAP2(dict)
		
		case "RET":
			return Assemble.RET(dict)
		
		case "LNOT":
			return Assemble.LNOT(dict)
		
		case "ADD":
			return Assemble.ADD(dict)
		
		case "SUB":
			return Assemble.SUB(dict)
		
		case "LT":
			return Assemble.LT(dict)
		
		case "LE":
			return Assemble.LE(dict)
		
		case "GE":
			return Assemble.GE(dict)
		
		case "EQ":
			return Assemble.EQ(dict)
		
		case "NE":
			return Assemble.NE(dict)
		
		case "LAND":
			return Assemble.LAND(dict)
		
		case "LOR":
			return Assemble.LOR(dict)
		
		case "SETF":
			return Assemble.SETF(dict)
		
		case "GETF":
			return Assemble.GETF(dict)
		
		case "SETSF":
			return Assemble.SETSF(dict)
		
		case "GETSF":
			return Assemble.GETSF(dict)
		
		case "SETV":
			return Assemble.SETV(dict)
			
		case "GETV":
			return Assemble.GETV(dict)
		
		case "SETRES":
			return Assemble.SETRES(dict)

		case "GETRES":
			return Assemble.GETRES(dict)
		
		case "SCNCHG":
			return Assemble.SCNCHG(dict)

		case "Text":
			if (Offsets == None):
				return Assemble.Text(dict, Offsets)
			else:
				for i in range(0, len(dict["STRING"])):
					bytes = []
					text = dict["STRING"][i].encode("UTF-8")
					length = len(text) + 2 + 1
					if (length % 2 != 0):
						bytes.append(numpy.uint16(length + 1))
					else:
						bytes.append(numpy.uint16(length))
					bytes.append(text)
					if (length % 2 != 0):
						bytes.append(b"\x00\x00")
					else:
						bytes.append(b"\x00")
					ProcessCommands.text_blob.append(b"".join(bytes))
				return Assemble.Text(dict, Offsets)
		
		case "NewLine":
			return Assemble.NewLine(dict)
		
		case "NewPage":
			return Assemble.NewPage(dict)
		
		case "TextShow":
			return Assemble.TextShow(dict)
		
		case "TextHide":
			return Assemble.TextHide(dict)
		
		case "TextSpeed":
			return Assemble.TextSpeed(dict)
		
		case "NovelMode":
			return Assemble.NovelMode(dict)

		case "Locate":
			return Assemble.Locate(dict)
		
		case "Wait":
			return Assemble.Wait(dict)
		
		case "KeyWait":
			return Assemble.KeyWait(dict)
		
		case "SkipDisable":
			return Assemble.SkipDisable(dict)
		
		case "Voice":
			return Assemble.Voice(dict)
		
		case "VoiceVol":
			return Assemble.VoiceVol(dict)
		
		case "VoicePos":
			return Assemble.VoicePos(dict)
		
		case "BGMVol":
			return Assemble.BGMVol(dict)
		
		case "SongVol":
			return Assemble.SongVol(dict)
		
		case "SEPlay":
			return Assemble.SEPlay(dict)
		
		case "SEStop":
			return Assemble.SEStop(dict)
		
		case "SEVol":
			return Assemble.SEVol(dict)
		
		case "SEPos":
			return Assemble.SEPos(dict)
		
		case "EnvVol":
			return Assemble.EnvVol(dict)
		
		case "EnvPos":
			return Assemble.EnvPos(dict)
		
		case "SetBG":
			return Assemble.SetBG(dict)
		
		case "SetBlack":
			return Assemble.SetBlack(dict)
		
		case "SetChar":
			return Assemble.SetChar(dict)
		
		case "Fade":
			return Assemble.Fade(dict)
		
		case "FadeBGtoSetBG":
			return Assemble.FadeBGtoSetBG(dict)
		
		case "WhiteOut":
			return Assemble.WhiteOut(dict)
		
		case "BlackOut":
			return Assemble.BlackOut(dict)
		
		case "MoveChar":
			return Assemble.MoveChar(dict)
		
		case "HideChar":
			return Assemble.HideChar(dict)
		
		case "AllMoveChartoActionChar2":
			return Assemble.AllMoveChartoActionChar2(dict)
		
		case "AllHideChar":
			return Assemble.AllHideChar(dict)
		
		case "Effect":
			return Assemble.Effect(dict)
		
		case "ShowCursor":
			return Assemble.ShowCursor(dict)
		
		case "HideCursor":
			return Assemble.HideCursor(dict)
		
		case "ShowPlace":
			return Assemble.ShowPlace(dict)
		
		case "SetDate":
			return Assemble.SetDate(dict)
		
		case "GetDate":
			return Assemble.GetDate(dict)
		
		case "GetWeek":
			return Assemble.GetWeek(dict)
		
		case "SetTime":
			return Assemble.SetTime(dict)
		
		case "SetWeather":
			return Assemble.SetWeather(dict)
		
		case "Select":
			if (Offsets == None):
				return Assemble.Select(dict, Offsets)
			else:
				for i in range(0, len(dict["STRINGS"])):
					bytes = []
					text = dict["STRINGS"][i].encode("UTF-8")
					length = len(text) + 2 + 1
					if (length % 2 != 0):
						bytes.append(numpy.uint16(length + 1))
					else:
						bytes.append(numpy.uint16(length))
					bytes.append(text)
					if (length % 2 != 0):
						bytes.append(b"\x00\x00")
					else:
						bytes.append(b"\x00")
					ProcessCommands.text_blob.append(b"".join(bytes))
				return Assemble.Select(dict, Offsets)
		
		case "ShowOpening":
			return Assemble.ShowOpening(dict)
		
		case "ShowEnding":
			return Assemble.ShowEnding(dict)
		
		case "GoTitle":
			return Assemble.GoTitle(dict)
		
		case "MiniGame":
			return Assemble.MiniGame(dict)
		
		case "UNK_x7D":
			return Assemble.UNK_x7D(dict)

		case "UNK_x7F":
			return Assemble.UNK_x7F(dict)

		case "MapMove":
			return Assemble.MapMove(dict)
		
		case "AddDay":
			return Assemble.AddDay(dict)
		
		case "AddMin":
			return Assemble.AddMin(dict)
		
		case "RainVol":
			return Assemble.RainVol(dict)
		
		case "AllMoveChartoActionChar":
			return Assemble.AllMoveChartoActionChar(dict)
		
		case "SetChangeChar":
			return Assemble.SetChangeChar(dict)
		
		case "DateShow":
			return Assemble.DateShow(dict)
		
		case "DateHide":
			return Assemble.DateHide(dict)
		
		case "TimeShow":
			return Assemble.TimeShow(dict)
		
		case "TimeHide":
			return Assemble.TimeHide(dict)
		
		case "BGMPlay":
			return Assemble.BGMPlay(dict)
		
		case "BGMStop":
			return Assemble.BGMStop(dict)
		
		case "SongPlay":
			return Assemble.SongPlay(dict)
		
		case "SongStop":
			return Assemble.SongStop(dict)
		
		case "EnvPlay":
			return Assemble.EnvPlay(dict)
		
		case "EnvStop":
			return Assemble.EnvStop(dict)
		
		case "SongEnable":
			return Assemble.SongEnable(dict) #Guessed
		
		case "SetRainPower":
			return Assemble.SetRainPower(dict)
		
		case "GetRainPower":
			return Assemble.GetRainPower(dict)

		case "SetRainLevel":
			return Assemble.SetRainLevel(dict)
		
		case "AddRainPower":
			return Assemble.AddRainPower(dict)
		
		case "SubRainPower":
			return Assemble.SubRainPower(dict)
		
		case "AddRainPowLv":
			return Assemble.AddRainPowLv(dict)
		
		case "SubRainPowLv":
			return Assemble.SubRainPowLv(dict)
		
		case _:
			print("UNKNOWN COMMAND!")
			print(dict["TYPE"])
			sys.exit()

ProcessCommands.text_blob = []

Offsets = {}
Offsets["MAGIC"] = 0
Offsets["SIZE"] = 4
Offsets["FILE_ID"] = 8
Offsets["CRC"] = 0xC
Offsets["registration_offset"] = 0x10
Offsets["registration_size"] = 0x14
Offsets["registration_entries"] = 0x18
Offsets["command_block_offset"] = 0x1C
Offsets["command_block_size"] = 0x20
Offsets["command_block_entries"] = 0x24
Offsets["text_block_registration_offset"] = 0x28
Offsets["text_block_registration_size"] = 0x2C
Offsets["text_block_registration_entries"] = 0x30
Offsets["text_blob_start"] = 0x34
Offsets["text_blob_size"] = 0x38
Offsets["text_count"] = 0x3C

files = glob.glob("jsons_new/*.json")

os.makedirs("New_KGO", exist_ok=True)

for y in range(0, len(files)):
	print(files[y])
	file = open(files[y], "r", encoding="UTF-8")
	dump = json.load(file)
	file.close()

	Storage.Textcounter = 1
	registration_block = []
	main_commands_block = []
	ProcessCommands.text_blob = []
	text_block_registration = []
	Precalculation_offsets = {}

	for i in range(0, len(dump["HEADER"]["REGISTRATION_BLOCK"])):
		entry = []
		Registration_dump = dump["HEADER"]["REGISTRATION_BLOCK"][i]
		entry.append(numpy.uint16(0))
		entry.append(numpy.uint32(Registration_dump["ID"]))
		string_size = len(Registration_dump["STRING"].encode("UTF-8")) + 1
		if (string_size % 2 != 0):
			string_size += 1
		entry.append(numpy.uint16(string_size))
		entry.append(numpy.uint16(Registration_dump["UNK1"]))
		entry.append(numpy.uint16(Registration_dump["UNK2"]))
		entry.append(numpy.uint16(Registration_dump["UNK3"]))
		entry.append(numpy.uint16(Registration_dump["UNK4"]))
		entry.append(numpy.uint16(Registration_dump["UNK5"]))
		entry.append(numpy.uint16(Registration_dump["UNK6"]))
		entry.append(numpy.uint16(Registration_dump["UNK7"]))
		string = Registration_dump["STRING"].encode("UTF-8") + b"\x00"
		entry.append(string)
		if (len(string) != string_size):
			entry.append(b"\x00")
		entry[0] = numpy.uint16(len(b"".join(entry)))
		registration_block.append(entry)

	for i in range(0, len(dump["COMMANDS"])):

		if (len(registration_block) != 0):
			if (registration_block[i][10] != b"da07_2\x00"):
				registration_block[i][4] = numpy.uint16(len(b"".join(main_commands_block)))
			else:
				registration_block[i][4] = numpy.uint16(0)

		commands_block = []
		commands_block_true = []
	
		commands_block.append(numpy.uint32(0)) # Size
		length = len(dump["HEADER"]["FUNS"][i].encode("UTF-8")) + 1
		if (length % 2 != 0):
			length += 1
		commands_block.append(numpy.uint16(length))

		CommandOffset = 0
		for a in range(0, len(dump["COMMANDS"][i])):
			Precalculation_offsets[dump["COMMANDS"][i][a]["LABEL"]] = CommandOffset
			CommandOffset += len(ProcessCommands(dump["COMMANDS"][i][a]))
		
		for a in range(0, len(dump["COMMANDS"][i])):
			commands_block_true.append(ProcessCommands(dump["COMMANDS"][i][a], Precalculation_offsets))
		
		commands_block.append(numpy.uint32(len(b"".join(commands_block_true))))
		commands_block.append(dump["HEADER"]["FUNS"][i].encode("UTF-8") + b"\x00")
		if (len(dump["HEADER"]["FUNS"][i].encode("UTF-8") + b"\x00") % 2 != 0):
			commands_block.append(b"\x00")

		while((len(b"".join(commands_block)) + len(b"".join(commands_block_true))) % 16 != 0):
			commands_block_true.append(b"\x00")
		
		commands_block[0] = numpy.uint32(len(b"".join(commands_block)) + len(b"".join(commands_block_true)))

		main_commands_block.append(b"".join(commands_block) + b"".join(commands_block_true))
	
	for i in range(0, len(dump["HEADER"]["BLOCK_2_REGISTRATION"])):
		entry = []
		block_2_registration = dump["HEADER"]["BLOCK_2_REGISTRATION"][i]
		entry.append(numpy.uint16(0))
		entry.append(numpy.uint16(block_2_registration["TYPE"]))
		entry.append(block_2_registration["STRING"].encode("UTF-8") + b"\x00")
		entry[0] = numpy.uint16(len(b"".join(entry)))
		text_block_registration.append(b"".join(entry))

	file = open("New_KGO/%s.kgo" % files[y][10:-5], "wb")
	file.write(b"SR10")
	file.write(b"\x00" * 4)
	file.write(numpy.uint32(dump["HEADER"]["FILE_ID"]))
	file.write(bytes.fromhex(dump["HEADER"]["CRC"]))
	file.write(numpy.uint32(0x40))
	size = 0
	for i in range(0, len(registration_block)):
		size += len(b"".join(registration_block[i]))
	file.write(numpy.uint32(size))
	file.write(numpy.uint32(len(dump["HEADER"]["REGISTRATION_BLOCK"])))
	offset = 0x40 + size
	while(offset % 16 != 0):
		offset += 1
	file.write(numpy.uint32(offset))
	file.write(numpy.uint32(len(b"".join(main_commands_block))))
	file.write(numpy.uint32(len(main_commands_block)))
	offset += len(b"".join(main_commands_block))
	while(offset % 16 != 0):
		offset += 1
	file.write(numpy.uint32(offset))
	file.write(numpy.uint32(len(b"".join(text_block_registration))))
	file.write(numpy.uint32(len(text_block_registration)))
	offset += len(b"".join(text_block_registration))
	while(offset % 16 != 0):
		offset += 1
	file.write(numpy.uint32(offset))
	file.write(numpy.uint32(len(b"".join(ProcessCommands.text_blob))))
	file.write(numpy.uint32(Storage.Textcounter-1))
	for i in range(0, len(registration_block)):
		file.write(b"".join(registration_block[i]))
	while(file.tell() % 16 != 0):
		file.write(b"\x00")
	file.write(b"".join(main_commands_block))
	while(file.tell() % 16 != 0):
		file.write(b"\x00")
	file.write(b"".join(text_block_registration))
	while(file.tell() % 16 != 0):
		file.write(b"\x00")
	file.write(b"".join(ProcessCommands.text_blob))
	while(file.tell() % 16 != 0):
		file.write(b"\x00")
	size = file.tell()
	file.seek(4)
	file.write(numpy.uint32(size))
	file.close()