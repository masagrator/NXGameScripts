import json
import glob
import os
import numpy

def GenerateData(entry):
	new_entry = []
	new_entry.append(entry["TYPE"].encode("UTF-8") + b"\x00")
	print(entry["TYPE"])
	temp = []
	match(entry["TYPE"]):
		case "TextTableData":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
		case "ActiveVoiceTableData":
			temp.append(numpy.uint16(entry["ID1"]))
			temp.append(numpy.uint16(entry["ID2"]))
			temp.append(numpy.uint16(entry["ID3"]))
			temp.append(entry["ASSET_SYMBOL"].encode("UTF-8") + b"\x00")
			temp.append(numpy.uint32(entry["VOICE_FILE_ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(numpy.float32(entry["UNK0"][0]))
			temp.append(numpy.float32(entry["UNK0"][1]))
			for i in range(0, 5):
				temp.append(numpy.uint16(entry["UNK1"][i]))

		case "AttachTableData":
			temp.append(bytes.fromhex(entry["UNK"]))
			temp.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			temp.append(entry["STRINGS"][1].encode("UTF-8") + b"\x00")

		case "QSChapter":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(numpy.uint16(entry["UNK"]))

		case "QSBook":
			temp.append(numpy.uint16(entry["UNK0"]))
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(entry["BOOK"].encode("UTF-8") + b"\x00")
			temp.append(entry["BOOKDATA"].encode("UTF-8") + b"\x00")
			temp.append(numpy.uint16(entry["ID2"]))
			temp.append(bytes.fromhex(entry["UNK1"]))
		
		case "TacticalBonus":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(numpy.float32(entry["UNK0"]))
			temp.append(numpy.uint16(entry["UNK1"]))
		
		case "CardTableData":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK0"]))
		
		case "dlc":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(bytes.fromhex(entry["UNK"]))
			temp.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			temp.append(entry["STRINGS"][1].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK2"]))
		
		case "FaceSupplementTableData":
			temp.append(bytes.fromhex(entry["UNK"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK2"]))
		
		case "text_lst":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")

		case "FootStepData":
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(numpy.uint8(entry["UNK"]))
		
		case "hkitugi_lst":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(numpy.uint16(entry["UNK0"]))
			temp.append(numpy.uint16(entry["UNK1"]))
			temp.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			temp.append(entry["STRINGS"][1].encode("UTF-8") + b"\x00")
		
		case "item":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(numpy.int16(entry["UNK0"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK1"]))
			temp.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			temp.append(entry["STRINGS"][1].encode("UTF-8") + b"\x00")
		
		case "MapJumpData":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(numpy.uint16(entry["UNK0"]))
			temp.append(entry["STRING1"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK1"]))
			temp.append(entry["STRING2"].encode("UTF-8") + b"\x00")
			temp.append(entry["STRING3"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK2"]))
		
		case "magic":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(numpy.uint16(entry["UNK0"]))
			temp.append(entry["GROUP"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK1"]))
			temp.append(entry["NAMEID"].encode("UTF-8") + b"\x00")
			temp.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			temp.append(entry["STRINGS"][1].encode("UTF-8") + b"\x00")
		
		case "MG02Text":
			temp.append(numpy.uint16(entry["UNK0"]))
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(numpy.uint16(entry["UNK1"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(numpy.uint16(entry["UNK2"]))
			temp.append(numpy.int32(entry["UNK3"]))
		
		case "status":
			temp.append(entry["STRING1"].encode("UTF-8") + b"\x00")
			temp.append(entry["STRING2"].encode("UTF-8") + b"\x00")
			temp.append(entry["STRING3"].encode("UTF-8") + b"\x00")
			for i in range(0, 7):
				temp.append(numpy.float32(entry["UNK0"][i]))
			temp.append(bytes.fromhex(entry["UNK1"]))
			temp.append(entry["STRINGS"][0].encode("UTF-8") + b"\x00")
			temp.append(entry["STRINGS"][1].encode("UTF-8") + b"\x00")
			temp.append(entry["STRINGS"][2].encode("UTF-8") + b"\x00")
		
		case "MasterQuartzMemo":
			temp.append(numpy.uint16(entry["UNK0"]))
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
		
		case "NameTableData":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING1"].encode("UTF-8") + b"\x00")
			for i in range(0, 6):
				temp.append(entry["STRING2"][i].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK"]))
		
		case "NaviTextData":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK0"]))
		
		case "QSCook":
			temp.append(entry["STRING1"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK0"]))
			temp.append(entry["STRINGS1"][0].encode("UTF-8") + b"\x00")
			temp.append(entry["STRINGS1"][1].encode("UTF-8") + b"\x00")
			temp.append(numpy.uint16(entry["UNK1"]))
			temp.append(entry["STRINGS2"][0].encode("UTF-8") + b"\x00")
			temp.append(entry["STRINGS2"][1].encode("UTF-8") + b"\x00")
			temp.append(numpy.uint16(entry["UNK2"]))
			temp.append(entry["STRINGS3"][0].encode("UTF-8") + b"\x00")
			temp.append(entry["STRINGS3"][1].encode("UTF-8") + b"\x00")
			temp.append(numpy.uint16(entry["UNK3"]))
			temp.append(entry["STRINGS4"][0].encode("UTF-8") + b"\x00")
			temp.append(entry["STRINGS4"][1].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK4"]))
		
		case "QSChar":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(bytes.fromhex(entry["UNK0"]))
			for i in range(0, 10):
				temp.append(entry["STRINGS"][i].encode("UTF-8") + b"\x00")
		
		case "QSFish":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(numpy.uint8(entry["UNK"]))
			temp.append(entry["STRING1"].encode("UTF-8") + b"\x00")
			temp.append(numpy.uint16(entry["UNK0"]))
			temp.append(numpy.uint16(entry["UNK1"]))
			for i in range(0, 3):
				temp.append(numpy.float32(entry["UNK2"][i]))
			temp.append(bytes.fromhex(entry["UNK3"]))
			temp.append(entry["STRING2"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK4"]))
		
		case "QSHelp":
			temp.append(numpy.uint16(entry["UNK0"]))
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
		
		case "QSMons":
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(numpy.uint16(entry["UNK"]))
			temp.append(numpy.uint32(entry["ID"]))
		
		case "PlaceTableData":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(numpy.uint16(entry["UNK0"]))
			temp.append(entry["NAMEID"].encode("UTF-8") + b"\x00")
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK1"]))
		
		case "preset":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(bytes.fromhex(entry["UNK"]))
		
		case "QSRank":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK0"]))
		
		case "se":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK"]))
		
		case "ShopTitle":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(bytes.fromhex(entry["UNK"]))
		
		case "QSTitle":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(numpy.uint8(entry["UNK0"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(entry["CATEGORY"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK1"]))
		
		case "QSText":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(numpy.uint8(entry["UNK0"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(numpy.uint8(entry["UNK1"]))
		
		case "trade":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(bytes.fromhex(entry["UNK"]))
		
		case "LinkAbList" | "MG05Root" | "MasterQuartzStatus" | "MasterQuartzDummy" | "MasterQuartzDummy2" | "NaviIconTableData" | "QSCoolVoice" | "ShopConv" | "TitleData" | "MG05Target" | "CompHelpData" | "condition" | "InfItemSet" | "MissionData" | "OverRisePoint" | "BattleVoiceData_A" | "BattleVoiceData_B" | "BattleVoiceData_C" | "BattleVoiceData_D" | "BattleVoiceData_E" | "BattleVoiceData_F" | "BattleVoiceData_G" | "CheckEquipFlag":
			temp.append(bytes.fromhex(entry["UNK"]))

		case "VoiceTiming":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(bytes.fromhex(entry["UNK"]))
		
		case "voice":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK"]))
		
		case "MissionText":
			temp.append(numpy.uint8(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
		
		case "EventTableData":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["EVENT"].encode("UTF-8") + b"\x00")
			temp.append(entry["MAP"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK"]))
			temp.append(entry["ARG"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK2"]))
		
		case "FaceShiftTableData":
			temp.append(numpy.uint16(entry["ID"]))
			for x in range(0, len(entry["STRINGS"])):
				temp.append(entry["STRINGS"][x].encode("UTF-8") + b"\x00")
		
		case "InfMonsSet":
			temp.append(bytes.fromhex(entry["UNK"]))
			for x in range(0, len(entry["MONSTERS"])):
				temp.append(entry["MOSNTERS"][x]["NAME"].encode("UTF-8") + b"\x00")
				temp.append(numpy.uint8(entry["MONSTERS"][x]["STATE"]))
		
		case "item_q":
			temp.append(bytes.fromhex(entry["UNK"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK1"]))
			for x in range(0, len(entry["STRINGS"])):
				temp.append(entry["STRINGS"][x].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK2"]))
		
		case "ItemHelpData":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK"]))

		case "CourageousJumpData":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK"]))
			temp.append(entry["STRING2"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK2"]))
		
		case "LinkAbText":
			temp.append(numpy.uint8(entry["UNK"]))
			for x in range(0, len(entry["STRINGS"])):
				temp.append(entry["STRINGS"][x].encode("UTF-8") + b"\x00")
		
		case "MarkerTableData":
			temp.append(bytes.fromhex(entry["UNK"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK2"]))
			temp.append(entry["STRING2"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK3"]))

		case "MG02Help":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")

		case "status_p":
			temp.append(numpy.uint16(entry["ID"]))
			for x in range(0, len(entry["STRINGS"])):
				temp.append(entry["STRINGS"][x].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")
			temp.append(bytes.fromhex(entry["UNK1"]))
	
		case "game_difficulty":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(numpy.int16(entry["OFFSET"]))
		
		case "CharData":
			temp.append(numpy.uint16(entry["ID"]))
			temp.append(bytes.fromhex(entry["UNK"]))
			temp.append(entry["STRING"].encode("UTF-8") + b"\x00")

		case _:
			temp.append(bytes.fromhex(entry["UNK"]))
	
	new_entry.append(numpy.uint16(len(b"".join(temp))))
	new_entry.append(b"".join(temp))
	return b"".join(new_entry)

files = glob.glob("jsons/*.json")

os.makedirs("new_nx", exist_ok=True)

for i in range(0, len(files)):
	file = open(files[i], "r", encoding="UTF-8")
	dump = json.load(file)
	file.close()

	COUNT = {}
	for x in range(0, len(dump)):
		if (dump[x]["TYPE"] not in COUNT.keys()):
			COUNT[dump[x]["TYPE"]] = 1
		else: COUNT[dump[x]["TYPE"]] += 1

	OUTPUT = []
	for x in range(0, len(dump)):
		OUTPUT.append(GenerateData(dump[x]))
	
	file_new = open("new_nx/%s.tbl" % files[i][6:-5], "wb")
	file_new.write(numpy.uint16(len(dump)))
	file_new.write(numpy.uint32(len(COUNT.keys())))
	lista = list(COUNT.keys())
	for x in range(0, len(lista)):
		file_new.write(lista[x].encode("UTF-8") + b"\x00")
		file_new.write(numpy.uint32(COUNT[lista[x]]))
	file_new.write(b"".join(OUTPUT))
	file_new.close()