import json
import glob
import os
import sys
import shutil

def invertBitsU8(b1):
	return (255-b1).to_bytes(1, "little")

def InvertString(bytes):
	chars = []
	for i in range(0, len(bytes)):
		chars.append(invertBitsU8(bytes[i]))
	return b"".join(chars)

def generateCommand(Dict):
	data = [b"\xFF"]
	size = 4
	match(Dict["TYPE"]):
		case "MESSAGE":
			data = []
			string = Dict["STRING"].encode("shift_jis_2004")
			if (Dict["ENG"] != ""):
				string = Dict["ENG"].encode("shift_jis_2004")
			data.append(InvertString(string))
		case "DEMO":
			size += 8
			data.append(size.to_bytes(1, "little"))
			data.append((1).to_bytes(2, "little"))
			data.append(Dict["FILE_ID"].to_bytes(4, "little"))
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "DEMOtm":
			data.append(size.to_bytes(1, "little"))
			data.append((2).to_bytes(2, "little"))
		case "PAGE":
			size += 6
			data.append(size.to_bytes(1, "little"))
			data.append((3).to_bytes(2, "little"))			
			data.append(Dict["POS_X"].to_bytes(2, "little"))
			data.append(Dict["POS_Y"].to_bytes(2, "little"))
			data.append(Dict["PAGE_NUMBER"].to_bytes(2, "little"))
			data.append(b"\x00\x00")
			end = {}
			end["TYPE"] = "PAGEtm"
			Dict["COMMANDS"].append(end)
			copy = data
			for x in range(len(Dict["COMMANDS"])):
				command = generateCommand(Dict["COMMANDS"][x])
				offset = len(b"".join(copy)) + len(command)
				if (offset % 4 != 0):
					command += b"\x00" * (4 - (offset % 4))
				copy.append(command)
			data = copy
		case "PAGEtm":
			data.append(size.to_bytes(1, "little"))
			data.append((4).to_bytes(2, "little"))		
		case "JUMP":
			size += 4
			data.append(size.to_bytes(1, "little"))
			data.append((101).to_bytes(2, "little"))	
			data.append(Dict["FILE_ID"].to_bytes(4, "little"))
		case "SELECT":
			data.append(size.to_bytes(1, "little"))
			data.append((102).to_bytes(2, "little"))	
		case "SELECTtm":
			data.append(size.to_bytes(1, "little"))
			data.append((103).to_bytes(2, "little"))	
		case "SI":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((104).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "SItm":
			data.append(size.to_bytes(1, "little"))
			data.append((105).to_bytes(2, "little"))	
		case "IF":
			size += 4
			data.append(size.to_bytes(1, "little"))
			data.append((106).to_bytes(2, "little"))	
			data.append(Dict["ARG1"].to_bytes(2, "little"))
			data.append(Dict["ARG2"].to_bytes(2, "little"))
		case "IFtm":
			data.append(size.to_bytes(1, "little"))
			data.append((107).to_bytes(2, "little"))	
		case "IFPARAM":
			size += len(bytes.fromhex(Dict["ARG"]))
			data.append(size.to_bytes(1, "little"))
			data.append((108).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["ARG"]))
		case "IFPARAMtm":
			data.append(size.to_bytes(1, "little"))
			data.append((109).to_bytes(2, "little"))
		case "IFRV":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((114).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "IFRVtm":
			data.append(size.to_bytes(1, "little"))
			data.append((115).to_bytes(2, "little"))
		case "WAIT":
			size += 2
			data.append(size.to_bytes(1, "little"))
			data.append((201).to_bytes(2, "little"))	
			data.append(Dict["ARG"].to_bytes(2, "little"))
		case "BWAIT":
			size += 4
			data.append(size.to_bytes(1, "little"))
			data.append((202).to_bytes(2, "little"))	
			data.append(Dict["ARG"].to_bytes(4, "little"))
		case "TWAIT":
			data.append(size.to_bytes(1, "little"))
			data.append((203).to_bytes(2, "little"))
		case "BR":
			size += 2
			data.append(size.to_bytes(1, "little"))
			data.append((204).to_bytes(2, "little"))	
			if (Dict["ARGS"] == "BREAK_LINE"): data.append(b"\x00\x00")
			elif (Dict["ARGS"] == "PRESS_TO_BREAK_LINE"): data.append(b"\x01\x00")	
			elif (Dict["ARGS"] == "PRESS_TO_END_MESSAGE"): data.append(b"\x01\x03")		
			else:
				data.append(Dict["ARGS"][0].to_bytes(1, "little"))
				data.append(Dict["ARGS"][1].to_bytes(1, "little"))
		case "FONT":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((205).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "FONTtm":
			data.append(size.to_bytes(1, "little"))
			data.append((206).to_bytes(2, "little"))
		case "MSPEED":
			size += 2
			data.append(size.to_bytes(1, "little"))
			data.append((207).to_bytes(2, "little"))
			data.append(Dict["ARG"].to_bytes(2, "little"))
		case "RUBY":
			string = Dict["STRING"].encode("shift_jis_2004")
			if (Dict["ENG"] != ""):
				string = Dict["ENG"].encode("shift_jis_2004")
			size += 1 + len(string) + 1
			data.append(size.to_bytes(1, "little"))
			data.append((208).to_bytes(2, "little"))	
			data.append(len(string).to_bytes(1, "little"))
			data.append(InvertString(string))
		case "RUBYtm":
			data.append(size.to_bytes(1, "little"))
			data.append((209).to_bytes(2, "little"))
		case "TEXT_LEFT":
			size += 2
			data.append(size.to_bytes(1, "little"))
			data.append((210).to_bytes(2, "little"))
			data.append(Dict["ARG"].to_bytes(2, "little"))
		case "TEXT_RIGHT":
			size += 2
			data.append(size.to_bytes(1, "little"))
			data.append((211).to_bytes(2, "little"))
			data.append(Dict["ARG"].to_bytes(2, "little"))
		case "TEXT_TOP":
			size += 2
			data.append(size.to_bytes(1, "little"))
			data.append((212).to_bytes(2, "little"))
			data.append(Dict["ARG"].to_bytes(2, "little"))
		case "EMBED":
			size += 2
			data.append(size.to_bytes(1, "little"))
			data.append((213).to_bytes(2, "little"))
			data.append(Dict["ARG"].to_bytes(2, "little"))
		case "SPACE":
			size += 2
			data.append(size.to_bytes(1, "little"))
			data.append((214).to_bytes(2, "little"))
			data.append(Dict["ARG"].to_bytes(2, "little"))
		case "CURSOR":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((215).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "TEXT_FADE":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((216).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "ICON":
			size += 2
			data.append(size.to_bytes(1, "little"))
			data.append((217).to_bytes(2, "little"))
			data.append(Dict["ARG"].to_bytes(2, "little"))
		case "BG_LOAD":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((401).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "BG_WAIT":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((402).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "BG_FADE":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((403).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "BG_COLOR":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((404).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "BG_MOVE":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((405).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "BG_SIZE":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((406).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "BG_ST":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((407).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "TX2_LOAD":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((501).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "TX2_MOVE":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((502).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "TX2_FADE":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((503).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "TX2_SIZE":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((504).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "TX2_ST":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((505).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "TX2_COLOR":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((506).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "TX2_ZGP":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((507).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "TX2_CENTERING":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((508).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "TX2_CTL_TRACK":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((509).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "TX2_PACK_READ":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((551).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "TX2_PACK_WAIT":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((552).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "SCR_FADE":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((701).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "SCR_VIB":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((702).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "FLAG":
			size += 2
			if (isinstance(Dict["ARG2"], int) == True):
				size += 2
			else: size += len(bytes.fromhex(Dict["ARG2"]))
			data.append(size.to_bytes(1, "little"))
			data.append((801).to_bytes(2, "little"))
			data.append(Dict["ARG1"].to_bytes(2, "little"))
			if (isinstance(Dict["ARG2"], int) == True):
				data.append(Dict["ARG2"].to_bytes(2, "little"))
			else: data.append(bytes.fromhex(Dict["ARG2"]))
		case "PARAM":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((802).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "STRING":
			string = Dict["STRING"].encode("shift_jis_2004")
			if (Dict["ENG"] != ""):
				string = Dict["ENG"].encode("shift_jis_2004")
			size += 1 + len(string) + 1
			data.append(size.to_bytes(1, "little"))
			data.append((803).to_bytes(2, "little"))
			data.append(Dict["ID"].to_bytes(1, "little"))
			data.append(InvertString(string) + b"\x00")
		case "PARAM_COMPARE":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((804).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "PARAM_COPY":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((806).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "BGM_READY":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((902).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "BGM_WAIT":
			data.append(size.to_bytes(1, "little"))
			data.append((903).to_bytes(2, "little"))	
		case "BGM_PLAY":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((904).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "BGM_VOL":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((905).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "BGM_STOP":
			data.append(size.to_bytes(1, "little"))
			data.append((906).to_bytes(2, "little"))	
		case "MSG_UNK_912":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((912).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "MSG_UNK_913":
			size += 2
			data.append(size.to_bytes(1, "little"))
			data.append((913).to_bytes(2, "little"))	
			data.append(Dict["ARG"].to_bytes(2, "little"))
			data.append(b"\x00\x00\x00\x00\x00\x00") # Additional bytes put by this opcode that do nothing.
		case "SE_PLAY":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((914).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "SE_VOL":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((915).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "SE_STOP":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((916).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "SE_ALL_STOP":
			data.append(size.to_bytes(1, "little"))
			data.append((917).to_bytes(2, "little"))	
		case "EMBED_EDIT":
			string = Dict["STRING"].encode("shift_jis_2004")
			if (Dict["ENG"] != ""):
				string = Dict["ENG"].encode("shift_jis_2004")
			size += 2 + 5 + 1 + len(string) + 1
			data.append(size.to_bytes(1, "little"))
			data.append((1001).to_bytes(2, "little"))
			data.append(Dict["ID1"].to_bytes(2, "little"))
			data.append(bytes.fromhex(Dict["UNK0"]))
			data.append(Dict["ID2"].to_bytes(1, "little"))
			data.append(InvertString(string) + b"\x00")
		case "LOGIC_INFER":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((1005).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "SAVE_POINT":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((1006).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "PAD_VIB":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((1102).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "CODE_3D_PLAY":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((1201).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "CODE_3D_FADE":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((1203).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "CODE_3D_ROTATE":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((1204).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "CALL_DEMO":
			size += 4 + len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((1301).to_bytes(2, "little"))	
			data.append(Dict["FILE_ID"].to_bytes(4, "little"))
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "WAIT_DEMO_ALL":
			data.append(size.to_bytes(1, "little"))
			data.append((1302).to_bytes(2, "little"))	
		case "OPTWND":
			size += 2
			data.append(size.to_bytes(1, "little"))
			data.append((1303).to_bytes(2, "little"))	
			data.append(Dict["ARG"].to_bytes(2, "little"))
		case "RANDOM":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((1304).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "DENY_SKIP":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((1306).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "BACKLOG_CLEAR":
			data.append(size.to_bytes(1, "little"))
			data.append((1307).to_bytes(2, "little"))	
		case "HIDE_SELECTER_MENU":
			size += 2
			data.append(size.to_bytes(1, "little"))
			data.append((1308).to_bytes(2, "little"))	
			data.append(Dict["ARG"].to_bytes(2, "little"))
		case "HIDE_NAMEEDIT_MENU":
			size += 2
			data.append(size.to_bytes(1, "little"))
			data.append((1309).to_bytes(2, "little"))	
			data.append(Dict["ARG"].to_bytes(2, "little"))
		case "STOP_SKIP":
			data.append(size.to_bytes(1, "little"))
			data.append((1311).to_bytes(2, "little"))	
		case "TXTHIDE_CTL":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((1312).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "PHRASE_SET":
			string = Dict["STRING"].encode("shift_jis_2004")
			if (Dict["ENG"] != ""):
				string = Dict["ENG"].encode("shift_jis_2004")
			size += 4 + len(string) + 1 + 1
			data.append(size.to_bytes(1, "little"))
			data.append((1401).to_bytes(2, "little"))	
			data.append(Dict["ID"].to_bytes(4, "little"))
			data.append(InvertString(string) + b"\x00")
			data.append(Dict["UNK"].to_bytes(1, "little"))
		case "PHRASE_FADE":
			size += len(bytes.fromhex(Dict["UNK0"])) + 2
			data.append(size.to_bytes(1, "little"))
			data.append((1402).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
			data.append(Dict["PHRASE_ID"].to_bytes(2, "little"))
		case "PHRASE_MOVE":
			size += len(bytes.fromhex(Dict["UNK0"])) + 2
			data.append(size.to_bytes(1, "little"))
			data.append((1403).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
			data.append(Dict["PHRASE_ID"].to_bytes(2, "little"))
		case "KEYWORD":
			size += 2
			data.append(size.to_bytes(1, "little"))
			data.append((2001).to_bytes(2, "little"))	
			data.append(Dict["KEYWORD_ID"].to_bytes(2, "little"))
		case "ADD_MEMO":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((2003).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "LOGIC_MODE":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((2004).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "LOGIC_SET_KEY":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((2005).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "LOGIC_GET_KEY":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((2006).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "LOGIC_CTL":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((2007).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "LOGIC_LOAD":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((2008).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "GAME_END":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((2009).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "CHOOSE_KEYWORD":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((2011).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "LOGIC_CLEAR_KEY":
			data.append(size.to_bytes(1, "little"))
			data.append((2012).to_bytes(2, "little"))	
		case "DLPAGE":
			data.append(size.to_bytes(1, "little"))
			data.append((2101).to_bytes(2, "little"))	
		case "DLPAGEtm":
			data.append(size.to_bytes(1, "little"))
			data.append((2102).to_bytes(2, "little"))	
		case "DLKEY":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((2103).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "DLSELSET":
			data.append(size.to_bytes(1, "little"))
			data.append((2104).to_bytes(2, "little"))	
		case "DLSELSETtm":
			data.append(size.to_bytes(1, "little"))
			data.append((2105).to_bytes(2, "little"))	
		case "DLSEL":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((2106).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "DLSELECT":
			data.append(size.to_bytes(1, "little"))
			data.append((2107).to_bytes(2, "little"))	
		case "ILCAMERA":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((2108).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case "ILZOOM":
			size += len(bytes.fromhex(Dict["UNK0"]))
			data.append(size.to_bytes(1, "little"))
			data.append((2109).to_bytes(2, "little"))	
			data.append(bytes.fromhex(Dict["UNK0"]))
		case _:
			print("Unknown command! %s" % Dict["TYPE"])
			sys.exit()
	return b"".join(data)

def sortByNumber(elem):
	return int(os.path.basename(elem)[:-5], base=10)

os.makedirs("new_database", exist_ok=True)
new_file = open("new_database/story1.dat", "wb")

orderfile = open("json/order.txt", "r")
order = orderfile.readlines()
order = [line.rstrip() for line in order]
orderfile.close()

header_size = (0x8 + (0x8 * len(order)))
new_file.write(header_size.to_bytes(4, "little"))
new_file.write(len(order).to_bytes(4, "little"))
scripts_block = []

for i in range(0, len(order)):
	try:
		json_file = open("scenario/%s.json" % order[i], "r", encoding="UTF-8")
	except:
		json_file = open("json/%s.json" % order[i], "r", encoding="UTF-8")
	print(json_file.name)
	DUMP = json.load(json_file)
	json_file.close()
	new_file.write(DUMP[0]["FILE_ID"].to_bytes(4, "little"))
	new_file.write((header_size + len(b"".join(scripts_block))).to_bytes(4, "little"))
	size = 0
	test_data = []
	for x in range(0, len(DUMP)):
		data = generateCommand(DUMP[x])
		if (len(data) % 4 != 0):
			data += b"\x00" * (4 - (len(data) % 4))
		# size += len(data)
		scripts_block.append(data)
		test_data.append(data)
	# size_check_file = open("extracted/%s.dat" % order[i], "rb")
	# size_check_file.seek(0, 2)
	# size_check = size_check_file.tell()
	# size_check_file.close()
	# if (size_check != size):
	# 	print("Size check failed! Expected: %d B, got: %d B" % (size_check, size))
	# 	test_file = open("new_database/%s.dat" % order[i], "wb")
	# 	test_file.write(b"".join(test_data))
	# 	test_file.close()
	# 	sys.exit()
	# else:
	# 	try: 
	# 		os.remove("new_database/%s.dat" % order[i])
	# 	except:
	# 		pass

new_file.write(b"".join(scripts_block))
new_file.close()
