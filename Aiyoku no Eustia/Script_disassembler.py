import glob
import sys
from pathlib import Path
import os
import json

copy = ""

def swap32(x: str):
	string = x[6:8] + x[4:6] + x[2:4] + x[0:2]

	while(string[0] == "0"):
		if len(string) < 2:
			break
		string = string[1:]
	return string

files = glob.glob(f"{sys.argv[1]}/*.binu8")

def Sort(key: int):
	return key

def ProcessDump(BLOB: list):
	pops = []
	for i in range(len(BLOB["COMMANDS"])):
		match(BLOB["COMMANDS"][i]["CMD"]):
			case 4:
				if (BLOB["COMMANDS"][i]["DATA"] != "00000000"):
					continue
				if "U32" not in BLOB["COMMANDS"][i].keys():
					continue
				if (BLOB["COMMANDS"][i+2]["CMD"] != 0x1A):
					continue
				if "U32" in BLOB["COMMANDS"][i+2].keys():
					continue
				if (BLOB["COMMANDS"][i+2]["DATA"] != "01000000"):
					continue
				if (BLOB["COMMANDS"][i+1]["CMD"] != 6):
					continue
				if "U32" not in BLOB["COMMANDS"][i+1].keys():
					string_id = -1
				elif len(BLOB["COMMANDS"][i+1]["U32"]) > 1:
					print("ERROR")
				else: 
					string_id = int.from_bytes(bytes.fromhex(BLOB["COMMANDS"][i]["U32"][0]), "little", signed=True)
				if (string_id < 0):
					continue
				BLOB["COMMANDS"][i]["CMD"] = "CASE4"
				BLOB["COMMANDS"][i]["STRING"] = BLOB["STRINGS"][string_id]
				BLOB["COMMANDS"][i].pop("DATA")
				if string_id not in pops:
					pops.append(string_id)
			case 5:
				if (BLOB["COMMANDS"][i]["DATA"] != "01000000"):
					BLOB["COMMANDS"][i]["CMD"] = "PUSH"
					continue
				if "U32" not in BLOB["COMMANDS"][i].keys():
					string_id = -1
				elif len(BLOB["COMMANDS"][i]["U32"]) > 1:
					print("ERROR")
				else: 
					string_id = int.from_bytes(bytes.fromhex(BLOB["COMMANDS"][i]["U32"][0]), "little", signed=True)
				if (string_id < 0):
					continue
				BLOB["COMMANDS"][i].pop("U32")
				BLOB["COMMANDS"][i]["CMD"] = "LOAD_STRING"
				BLOB["COMMANDS"][i]["STRING"] = BLOB["STRINGS"][string_id]
				BLOB["COMMANDS"][i].pop("DATA")
				if string_id not in pops:
					pops.append(string_id)
			case 7:
					BLOB["COMMANDS"][i]["CMD"] = "FUNC"
			case 9:
				if (BLOB["COMMANDS"][i]["DATA"] != "01000000"):
					continue
				if BLOB["COMMANDS"][i-1]["CMD"] != 6:
					continue
				string_id = int.from_bytes(bytes.fromhex(BLOB["COMMANDS"][i-1]["U32"][0]), "little", signed=True)
				if (string_id < 0 and string_id != -2147483644):
					continue
				if (string_id != -2147483644):
					BLOB["COMMANDS"][i]["CMD"] = "PUSH_CUSTOM_TEXT"
					BLOB["COMMANDS"][i].pop("DATA")
					BLOB["COMMANDS"][i-1]["STRING"] = BLOB["STRINGS"][string_id]
					BLOB["COMMANDS"][i-1].pop("U32")
					BLOB["COMMANDS"][i-1]["CMD"] = "LOAD_CUSTOM_TEXT"
					if string_id not in pops:
						pops.append(string_id)
					if BLOB["COMMANDS"][i-2]["CMD"] != 4:
						continue
					if "U32" not in BLOB["COMMANDS"][i-2].keys():
						continue
					string_id = int.from_bytes(bytes.fromhex(BLOB["COMMANDS"][i-2]["U32"][0]), "little", signed=True)
					if (string_id < 0):
						continue
					BLOB["COMMANDS"][i-2]["CMD"] = "SET_EFFECT"
					BLOB["COMMANDS"][i-2]["STRING"] = BLOB["STRINGS"][string_id]
					BLOB["COMMANDS"][i-2].pop("U32")
					if string_id not in pops:
						pops.append(string_id)
				else:
					BLOB["COMMANDS"][i]["CMD"] = "PUSH_CUSTOM_TEXT"
					BLOB["COMMANDS"][i].pop("DATA")
					if BLOB["COMMANDS"][i-2]["CMD"] != 4:
						continue
					if "U32" not in BLOB["COMMANDS"][i-2].keys():
						continue
					string_id = int.from_bytes(bytes.fromhex(BLOB["COMMANDS"][i-2]["U32"][0]), "little", signed=True)
					if (string_id < 0):
						continue
					BLOB["COMMANDS"][i-2]["CMD"] = "SET_EFFECT"
					BLOB["COMMANDS"][i-2]["STRING"] = BLOB["STRINGS"][string_id]
					BLOB["COMMANDS"][i-2].pop("U32")
					if string_id not in pops:
						pops.append(string_id)
			case 0xE:
				if (BLOB["COMMANDS"][i]["DATA"][6:] != "80"):
					continue
				if ("U32" not in BLOB["COMMANDS"][i].keys()):
					continue
				if (len(BLOB["COMMANDS"][i]["U32"]) > 1):
					continue
				string_id = int.from_bytes(bytes.fromhex(BLOB["COMMANDS"][i]["U32"][0]), "little", signed=True)
				if (string_id < 0):
					continue
				BLOB["COMMANDS"][i]["CMD"] = "SPECIAL_TEXT"
				BLOB["COMMANDS"][i].pop("U32")
				BLOB["COMMANDS"][i]["STRING"] = BLOB["STRINGS"][string_id]
				if string_id not in pops:
					pops.append(string_id)
			case 0x1B:
				BLOB["COMMANDS"][i]["CMD"] = "INIT"
			case 0x1C:
				BLOB["COMMANDS"][i]["CMD"] = "DEINIT"
			case 0x1D:
				BLOB["COMMANDS"][i]["CMD"] = "INF1"
			case 0x2C:
				BLOB["COMMANDS"][i]["CMD"] = "INF2"
			case 0x41:
				BLOB["COMMANDS"][i]["CMD"] = "JNGE"
			case 0x42:
				BLOB["COMMANDS"][i]["CMD"] = "JNLE"
			case _:
				continue
	pops.sort(key=Sort)
	pops.reverse()
	for i in range(len(pops)):
		BLOB["STRINGS"].pop(pops[i])
	if len(BLOB["STRINGS"]) == 1:
		if BLOB["STRINGS"][0] != "":
			print("Some string were not pulled!")
			print(BLOB["STRINGS"])
			#sys.exit()
	elif len(BLOB["STRINGS"]) > 0:
		print("Some string were not pulled!")
		print(BLOB["STRINGS"])
		#sys.exit()
	
	BLOB.pop("STRINGS")
	BLOB = BLOB["COMMANDS"]
	return BLOB


def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("UTF-8"))
		chars.append(c)

os.makedirs("Unpacked", exist_ok=True)

for i in range(len(files)):
	BLOB = {}
	print(f"{Path(files[i]).stem}")
	script = open(files[i], "rb")
	extra_data_count = int.from_bytes(script.read(4), "little")
	extra = []
	if (extra_data_count != 0):
		for x in range(extra_data_count):
			entry = []
			entry.append(int.from_bytes(script.read(4), "little"))
			entry.append(int.from_bytes(script.read(4), "little"))
			extra.append(entry)
	commands_count = int.from_bytes(script.read(4), "little")
	COMMANDS = []
	u32_value = []
	label = 0
	for x in range(commands_count):
		entry = {}
		if (label == 0):
			label = script.tell()
		cmd = int.from_bytes(script.read(4), "little")
		if (cmd == 0):
			u32_value.append(script.read(4).hex())
			continue
		else:
			entry["LABEL"] = label
			label = 0
			if (len(u32_value) > 0):
				entry["U32"] = u32_value
				u32_value = []
			entry["CMD"] = cmd
		entry["DATA"] = script.read(4).hex()
		COMMANDS.append(entry)
	strings_count = int.from_bytes(script.read(4), "little")
	print(strings_count)
	BLOB["STRINGS"] = []
	for x in range(strings_count):
		temp_pos = script.tell()
		string_size = int.from_bytes(script.read(4), "little") - 1
		string = readString(script)
		if (string_size != len(string.encode("UTF-8"))):
			print("String size check failed! Expected: %d, got %d" % (string_size, len(string.encode("UTF-8"))))
			print("Offset: 0x%x" % temp_pos)
			print(string)
			sys.exit()
		BLOB["STRINGS"].append(string.replace("\n", "\\n"))
	BLOB["COMMANDS"] = COMMANDS
	new_file = open(f"Unpacked/{Path(files[i]).stem}.json", "w", encoding="UTF-8")
	json.dump(BLOB["STRINGS"], new_file, indent="\t", ensure_ascii=False)
	new_file.close()
	BLOB = ProcessDump(BLOB)

	new_file = open(f"Unpacked/{Path(files[i]).stem}.asm", "w", encoding="UTF-8")
	label_offset = 1
	if extra != []:
		label_offset += len(extra)
		new_file.write("#\tEXTRA\t[")
		for x in range(len(extra) - 1):
			new_file.write("0x%x, 0x%x, " % (extra[x][0], extra[x][1]))
		new_file.write("0x%x, 0x%x]\n" % (extra[len(extra) - 1][0], extra[len(extra) - 1][1]))
	for x in range(len(BLOB)):
		if isinstance(BLOB[x]["CMD"], int) == True:
			new_file.write("{0x%04X}" % (int(BLOB[x]["LABEL"]/8) - label_offset))
			new_file.write("\tCMD.%X\t" % BLOB[x]["CMD"])
			new_file.write("0x%s" % swap32(BLOB[x]["DATA"]))
			if "U32" in BLOB[x].keys():
				new_file.write("\t[")
				iters = len(BLOB[x]["U32"])
				for y in range(iters):
					new_file.write("0x%s" % swap32(BLOB[x]["U32"][y]))
					if (y+1 < iters):
						new_file.write(",")
				new_file.write("]")
			new_file.write("\n")
		else:
			new_file.write("{0x%04X}" % (int(BLOB[x]["LABEL"]/8) - label_offset))
			new_file.write("\t%s" % BLOB[x]["CMD"])
			match(BLOB[x]["CMD"]):
				case "PUSH_MESSAGE" | "PUSH_CUSTOM_TEXT":
					pass
				case "JNGE" | "JNLE":
					new_file.write("\t0x%04x" % int(swap32(BLOB[x]["DATA"]), base=16))
					if "U32" in BLOB[x].keys():
						new_file.write("\t[")
						iters = len(BLOB[x]["U32"])
						for y in range(iters):
							new_file.write("0x%s" % swap32(BLOB[x]["U32"][y]))
							if (y+1 < iters):
								new_file.write(",")
						new_file.write("]")	
				case "LOAD_STRING" | "CASE4":
					new_file.write("\t'%s'" % BLOB[x]["STRING"])
				case "LOAD_CUSTOM_TEXT" | "SET_EFFECT":
					new_file.write("\t0x%s" % swap32(BLOB[x]["DATA"]))
					new_file.write("\t'%s'" % BLOB[x]["STRING"])
				case "PUSH":
					new_file.write("\t0x%x" % int(swap32(BLOB[x]["DATA"]), base=16))
					if "U32" in BLOB[x].keys():
						new_file.write("\t[")
						iters = len(BLOB[x]["U32"])
						for y in range(iters):
							new_file.write("0x%s" % swap32(BLOB[x]["U32"][y]))
							if (y+1 < iters):
								new_file.write(",")
						new_file.write("]")
				case "SPECIAL_TEXT":
					if "DATA" not in BLOB[x].keys():
						new_file.write("\t'%s'" % BLOB[x]["STRING"])
					else:
						new_file.write("\t0x%x" % int(swap32(BLOB[x]["DATA"]), base=16))
						new_file.write("\t[")
						if ("DATA2" in BLOB[x].keys()):
							new_file.write("0x%s," % swap32(BLOB[x]["DATA2"]))
						new_file.write("'%s']" % BLOB[x]["STRING"])
				case "FUNC":
					FUNC_ID = int.from_bytes(bytes.fromhex(BLOB[x]["DATA"]), "little", signed=True)
					match(FUNC_ID):
						case 0x40070:
							new_file.write("\t'PUSH_NAME'")
						case _:
							new_file.write("\t0x%X" % FUNC_ID)
				case _:
					new_file.write("\t0x%x" % int(swap32(BLOB[x]["DATA"]), base=16))
					if "U32" in BLOB[x].keys():
						new_file.write("\t[")
						iters = len(BLOB[x]["U32"])
						for y in range(iters):
							new_file.write("0x%s" % swap32(BLOB[x]["U32"][y]))
							if (y+1 < iters):
								new_file.write(",")
						new_file.write("]")
			new_file.write("\n")
	new_file.close()