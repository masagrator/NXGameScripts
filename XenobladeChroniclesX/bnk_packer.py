import sys
import os
import json
from pathlib import Path
import struct

def hash(string: str) -> int:
    string = string.lower()
    FNV1_INIT = 0x811C9DC5
    FNV1_PRIME = 0x1000193
    string = string.lower()
    string = string.encode("ascii")
    for i in range(len(string)):
        FNV1_INIT = ((FNV1_PRIME * FNV1_INIT) & 0xFFFFFFFF) ^ string[i]
    return FNV1_INIT

bank_name = Path(sys.argv[1]).stem
data = [b"BKHD"]
header_size = 0x14
HIRC = False
DATA = False
if (os.path.isfile("%s/HIRC.json" % bank_name) == True):
    header_size += 4
    HIRC = True
if (os.path.isdir("%s/DATA" % bank_name) == True):
    header_size += 8
    DATA = True
    print("This script doesn't support DIDX/DATA...")
    sys.exit()
data.append(header_size.to_bytes(4, "little"))
data.append(0x8C.to_bytes(4, "little"))
data.append(hash(bank_name).to_bytes(4, "little"))
data.append(hash("sfx").to_bytes(4, "little"))
data.append(0x10.to_bytes(4, "little"))
data.append(0x3484.to_bytes(8, "little"))
if (HIRC == True):
    data.append(b"HIRC")
    size_id = len(data)
    data.append(b"\x00" * 4)
    rel_offset = len(b"".join(data))
    file = open("%s/HIRC.json" % bank_name, "r", encoding="ascii")
    HIRC = json.load(file)
    file.close()
    data.append(len(HIRC).to_bytes(4, "little"))
    for i in range(len(HIRC)):
        if (isinstance(HIRC[i]["HircType"], int) == True):
            data.append(int(HIRC[i]["HircType"]).to_bytes(1, "little"))
            bytesarray = bytes.fromhex(HIRC[i]["raw_data"])
            data.append(len(bytesarray).to_bytes(4, "little"))
            data.append(bytesarray)
        elif (HIRC[i]["HircType"] == "MusicTrack"):
            data.append(0xB.to_bytes(1, "little"))
            last_item = len(data)
            data.append(0x0.to_bytes(4, "little"))
            size_start = len(b"".join(data))
            data.append(bytes.fromhex(HIRC[i]["Data1"]))
            data.append(len(HIRC[i]["Sources"]).to_bytes(4, "little"))
            for x in range(len(HIRC[i]["Sources"])):
                data.append(bytes.fromhex(HIRC[i]["Sources"][x]))
            data.append(len(HIRC[i]["PlayListItems"]).to_bytes(4, "little"))
            for x in range(len(HIRC[i]["PlayListItems"])):
                data.append(HIRC[i]["PlayListItems"][x]["TrackID"].to_bytes(4, "little"))
                data.append(int(HIRC[i]["PlayListItems"][x]["Hash_filename"], base=0).to_bytes(4, "little"))
                data.append(HIRC[i]["PlayListItems"][x]["EventID"].to_bytes(4, "little"))
                data.append(struct.pack('d', HIRC[i]["PlayListItems"][x]["PlayAt"]))
                data.append(struct.pack('d', HIRC[i]["PlayListItems"][x]["BeginTrimOffset"]))
                data.append(struct.pack('d', HIRC[i]["PlayListItems"][x]["EndTrimOffset"]))
                data.append(struct.pack('d', HIRC[i]["PlayListItems"][x]["SrcDuration"]))
            data.append(bytes.fromhex(HIRC[i]["Data2"]))
            data.append(HIRC[i]["MusicSegmentID"].to_bytes(4, "little"))
            data.append(bytes.fromhex(HIRC[i]["Data3"]))
            data[last_item] = (len(b"".join(data)) - size_start).to_bytes(4, "little")
        elif (HIRC[i]["HircType"] == "MusicSegment"):
            data.append(0xA.to_bytes(1, "little"))
            last_item = len(data)
            data.append(0x0.to_bytes(4, "little"))
            size_start = len(b"".join(data))
            data.append(HIRC[i]["ID"].to_bytes(4, "little"))
            data.append(bytes.fromhex(HIRC[i]["Data1"]))
            data.append(len(HIRC[i]["Props"]).to_bytes(1, "little"))
            for x in range(len(HIRC[i]["Props"])):
                data.append(bytes.fromhex(HIRC[i]["Props"][x]))
            data.append(len(HIRC[i]["Props>"]).to_bytes(1, "little"))
            for x in range(len(HIRC[i]["Props>"])):
                data.append(bytes.fromhex(HIRC[i]["Props>"][x]))
            data.append(bytes.fromhex(HIRC[i]["Data2"]))
            data.append(len(HIRC[i]["StateProps"]).to_bytes(1, "little"))
            for x in range(len(HIRC[i]["StateProps"])):
                data.append(bytes.fromhex(HIRC[i]["StateProps"][x]))
            data.append(len(HIRC[i]["StateGroups"]).to_bytes(1, "little"))
            for x in range(len(HIRC[i]["StateGroups"])):
                data.append(bytes.fromhex(HIRC[i]["StateGroups"][x]))
            data.append(len(HIRC[i]["RTPC"]).to_bytes(2, "little"))
            for x in range(len(HIRC[i]["RTPC"])):
                data.append(bytes.fromhex(HIRC[i]["RTPC"][x]))  
            data.append(bytes.fromhex(HIRC[i]["Data3"])) 
            data.append(len(HIRC[i]["Stingers"]).to_bytes(4, "little"))
            for x in range(len(HIRC[i]["Stingers"])):
                data.append(bytes.fromhex(HIRC[i]["Stingers"][x]))  
            data.append(struct.pack('d', HIRC[i]["Duration"]))
            data.append(len(HIRC[i]["Markers"]).to_bytes(4, "little"))
            for x in range(len(HIRC[i]["Markers"])):
                data.append(HIRC[i]["Markers"][x]["ID"].to_bytes(4, "little"))
                data.append(struct.pack('d', HIRC[i]["Markers"][x]["Position"]))
                data.append(HIRC[i]["Markers"][x]["Name"].encode("ascii") + b"\x00")
            data[last_item] = (len(b"".join(data)) - size_start).to_bytes(4, "little")
        else:
            print("Unknown HircType: %s, aborting..." % HIRC[i]["HircType"])
            sys.exit()
    data[size_id] = (len(b"".join(data)) - rel_offset).to_bytes(4, "little")
os.makedirs("PACKED", exist_ok=True)
new_file = open("PACKED/%s.bnk" % bank_name, "wb")
new_file.write(b"".join(data))
new_file.close()
print("Finished work!")
