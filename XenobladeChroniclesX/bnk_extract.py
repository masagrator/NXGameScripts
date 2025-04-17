import sys
import os
from pathlib import Path
import json
import struct

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("ascii"))
		chars.append(c)

file = open(sys.argv[1], "rb")
if (file.read(4) != b"BKHD"):
	print("Invalid bank file! Aborting...")
	file.close()
	sys.exit()
data_start = int.from_bytes(file.read(4), "little")
rel_offset = file.tell()
unk = int.from_bytes(file.read(4), "little")
hash_name = file.read(4)
lang_name = int.from_bytes(file.read(4), "little")
match(lang_name):
	case 0x17705D3E:
		print("Lang: sfx")
	case 0x6C772760:
		print("Lang: en")
	case 0x67771F5F:
		print("Lang: jp")
	case _:
		print("Lank: Unknown: 0x%08x" % lang_name)
unk2 = int.from_bytes(file.read(4), "little")
unk3 = int.from_bytes(file.read(4), "little")
Blocks_amount = (data_start - (file.tell() - rel_offset)) // 4
file.seek(rel_offset + data_start)
DUMP = {}
for i in range(Blocks_amount):
	type = file.read(4)
	size = int.from_bytes(file.read(4), "little")
	rel_offset = file.tell()
	match(type):
		case b"DIDX":
			os.makedirs("%s/DATA" % Path(sys.argv[1]).stem, exist_ok=True)
			DUMP["DIDX"] = []
			while(file.tell() < rel_offset + size):
				entry = {}
				entry["file_hash"] = int.from_bytes(file.read(4), "little")
				entry["offset_start"] = int.from_bytes(file.read(4), "little")
				entry["size"] = int.from_bytes(file.read(4), "little")
				DUMP["DIDX"].append(entry)
		case b"DATA":
			if ("DIDX" not in DUMP.keys()):
				print("Something went really wrong, aborting...")
				file.close()
				sys.exit()
			for x in range(len(DUMP["DIDX"])):
				file.seek(rel_offset + DUMP["DIDX"][x]["offset_start"])
				filetype = ".dat"
				if (file.read(4) == b"RIFF"):
					filetype = ".wav"
				file.seek(-4, 1)
				print("Unpacking file: %08x%s" % (DUMP["DIDX"][x]["file_hash"], filetype))
				new_file = open("%s/DATA/%08x%s" % (Path(sys.argv[1]).stem, DUMP["DIDX"][x]["file_hash"], filetype), "wb")
				new_file.write(file.read(DUMP["DIDX"][x]["size"]))
				new_file.close()
		case b"HIRC":
			os.makedirs("%s" % Path(sys.argv[1]).stem, exist_ok=True)
			entries_count = int.from_bytes(file.read(4), "little")
			HIRC = []
			for x in range(entries_count):
				entry = {}
				entry["HircType"] = file.read(1)[0]
				entrySize = int.from_bytes(file.read(4), "little")
				entryTell = file.tell()
				if (entry["HircType"] == 0xB):
					entry["HircType"] = "MusicTrack"
					entry["Data1"] = file.read(5).hex()
					numSources = int.from_bytes(file.read(4), "little")
					entry["Sources"] = []
					for y in range(numSources):
						entry2 = file.read(14).hex()
						entry["Sources"].append(entry2)
					numPlaylistItems = int.from_bytes(file.read(4), "little")
					entry["PlayListItems"] = []
					for y in range(numPlaylistItems):
						entry2 = {}
						entry2["TrackID"] = int.from_bytes(file.read(4), "little")
						entry2["Hash_filename"] = "0x%x" % int.from_bytes(file.read(4), "little")
						entry2["EventID"] = int.from_bytes(file.read(4), "little")
						entry2["PlayAt"] = struct.unpack('d', file.read(8))[0]
						entry2["BeginTrimOffset"] = struct.unpack('d', file.read(8))[0]
						entry2["EndTrimOffset"] = struct.unpack('d', file.read(8))[0]
						entry2["SrcDuration"] = struct.unpack('d', file.read(8))[0]
						entry["PlayListItems"].append(entry2)
					entry["Data2"] = file.read(0x11).hex()
					entry["MusicSegmentID"] = int.from_bytes(file.read(4), "little")
					entry["Data3"] = file.read(entrySize - (file.tell() - entryTell)).hex()
				elif (entry["HircType"] == 0xA):
					entry["HircType"] = "MusicSegment"
					entry["ID"] = int.from_bytes(file.read(4), "little")
					entry["Data1"] = file.read(0xF).hex()
					numProps = file.read(1)[0]
					entry["Props"] = []
					for y in range(numProps):
						entry2 = file.read(5).hex()
						entry["Props"].append(entry2)
					numProps = file.read(1)[0]
					entry["Props>"] = []
					for y in range(numProps):
						entry2 = file.read(5).hex() ##unk
						entry["Props>"].append(entry2)
					BitsPositioning = file.read(1)[0]
					file.seek(-1, 1)
					entry["Data2"] = file.read(0xC).hex()
					if (BitsPositioning == 3):
						entry["Data2"] += file.read(1).hex()
					numStateProps = file.read(1)[0]
					entry["StateProps"] = []
					for y in range(numStateProps):
						entry2 = file.read(5).hex() ##unk
						entry["StateProps"].append(entry2)
					numStateGroups = file.read(1)[0]
					entry["StateGroups"] = []
					for y in range(numStateGroups):
						entry2 = file.read(5).hex() ##unk
						entry["StateGroups"].append(entry2)
					numRTPC = int.from_bytes(file.read(2), "little")
					entry["RTPC"] = []
					for y in range(numRTPC):
						entry2 = file.read(5).hex() ##unk
						entry["numRTPC"].append(entry2)       
					entry["Data3"] = file.read(31).hex()
					numStingers = int.from_bytes(file.read(4), "little")
					entry["Stingers"] = []
					for y in range(numStingers):
						entry2 = file.read(5).hex() ##unk
						entry["Stingers"].append(entry2)          
					entry["Duration"] = struct.unpack('d', file.read(8))[0]
					numMarkers = int.from_bytes(file.read(4), "little")
					entry["Markers"] = []
					for y in range(numMarkers):
						entry2 = {}
						entry2["ID"] = int.from_bytes(file.read(4), "little")
						entry2["Position"] = struct.unpack('d', file.read(8))[0]
						entry2["Name"] = readString(file)
						entry["Markers"].append(entry2)
				else:
					entry["raw_data"] = file.read(entrySize).hex()
				HIRC.append(entry)
			new_file = open("%s/HIRC.json" % (Path(sys.argv[1]).stem), "w", encoding="ascii")
			json.dump(HIRC, new_file, indent="\t", ensure_ascii=False)
			new_file.close()
		case _:
			print("Unsupported type: %s, skipping block..." % type.decode("ascii"))
			file.seek(size, 1)
file.close()
print("Script finished execution!")
