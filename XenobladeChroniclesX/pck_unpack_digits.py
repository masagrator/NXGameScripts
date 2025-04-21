import sys
import os
from pathlib import Path

BANKS_NAMES = ["ma", "dl_engine_01", "dl_engine_02", "dl_engine_03", "dl_engine_04", "dl_engine_05", "dl_engine_06", "dl_engine_07", "dl_engine_08", "oj820101", "oj820102", "oj820103", "oj820104", "oj820105", "oj820106", "oj820107", "oj820108", "oj820109", "oj820110", "oj820111", "oj820116", "oj820117", "oj820118", "oj820119", "oj820122", "oj820123", "oj820124", "oj820125", "oj820127", "oj820129", "oj820131", "oj820132", "oj850001", "en010310", "en011001", "en011101", "en011102", "en011103", "en011104", "en011201", "en011302", "en011501", "en011502", "en011601", "en011602", "en011801", "en011802", "en011803", "en011901", "en012001", "en012501", "en012601", "en012603", "en012604", "en012605", "en012701", "en013001", "en013002", "en013101", "en013201", "en021001", "en021101", "en021201", "en021301", "en025001", "en025101", "en025201", "en025301", "en025401", "en040106", "en041001", "en041002", "en041101", "en041102", "en060706", "en061001", "en061101", "en061201", "wd_034701", "wd_034801", "wd_035301", "wd_042201", "wd_061101", "wd_061301", "wd_300701", "wd_302001", "wd_302101", "wd_302201", "wd_034109", "wd_034301", "wd_034601", "wd_012101", "wd_012107", "wd_012201", "wd_012207", "wd_012211", "wd_012601", "wd_012605", "wd_013101", "wd_022301", "wd_022701", "wd_022801", "wd_032801", "wd_032805", "wd_033101", "wd_034101", "wd_034105", "bu1116", "oj820901", "oj820133", "oj820115", "oj860001", "oj860002", "oj860003", "oj860004", "oj860008", "oj860010", "oj860070", "oj850020", "oj850030", "oj850031", "oj400101", "oj400106", "oj400201", "oj400501", "oj400702", "oj820201", "oj820301", "oj820302", "oj840009", "oj840031", "oj840037", "oj340501", "en780101", "en710101", "se_zone2001", "se_zone2201", "se_zone5001", "se_zone5999", "se_zone6000", "se_zone8000", "se_zone8001", "Init", "bgm", "Common_2xx", "CS_music", "CS_FX", "CS_dialog", "Common_0xx", "Common_1xx", "Common_3xx", "Common_6xx", "Common_etc", "Common2", "BG", "Weather", "Maps", "ev_voice", "voice_mb", "voice_np", "pc_voices", "SeVoices", "BradeRoomDoor", "CookingJingle", "missions", "Gimmick_etc", "town1", "town2", "Talk", "syanai", "takeda", "Voice202307"]
BANKS_IDS = {}

def hash(string: str) -> int:
    string = string.lower()
    FNV1_INIT = 0x811C9DC5
    FNV1_PRIME = 0x1000193
    string = string.encode("ascii")
    for i in range(len(string)):
        FNV1_INIT = ((FNV1_PRIME * FNV1_INIT) & 0xFFFFFFFF) ^ string[i]
    return FNV1_INIT

for i in range(len(BANKS_NAMES)):
    BANKS_IDS[hash(BANKS_NAMES[i])] = BANKS_NAMES[i]
for i in range(11, 28):
    BANKS_IDS[hash("ws%d" % i)] = "ws%d" % i
    BANKS_IDS[hash("ws%d_ph" % i)] = "ws%d_ph" % i
    BANKS_IDS[hash("ws%d_bm" % i)] = "ws%d_bm" % i
    BANKS_IDS[hash("ws%d_dm" % i)] = "ws%d_dm" % i
    BANKS_IDS[hash("ws%d_fr" % i)] = "ws%d_fr" % i
    BANKS_IDS[hash("ws%d_gv" % i)] = "ws%d_gv" % i
    BANKS_IDS[hash("ws%d_vt" % i)] = "ws%d_vt" % i
for i in range(6):
    BANKS_IDS[hash("se_zone%04d" % i)] = "se_zone%04d" % i
for i in range(10, 18):
    BANKS_IDS[hash("se_zone%02d01" % i)] = "se_zone%02d01" % i
for i in range(10):
    for x in range(10):
        for y in range(6):
            BANKS_IDS[hash("en%02d%02d%02d" % (i, x, y))] = "en%02d%02d%02d" % (i, x, y)

file = open(sys.argv[1], "rb")
if (file.read(4) != b"AKPK"):
    file.close()
    print("WRONG MAGIC!")
    sys.exit()
header_size = int.from_bytes(file.read(4), "little") # not ideally aligned?
version = int.from_bytes(file.read(4), "little")
LangMapsSize = int.from_bytes(file.read(4), "little")
BanksSize = int.from_bytes(file.read(4), "little")
StreamsSize = int.from_bytes(file.read(4), "little")
ExternalSize = int.from_bytes(file.read(4), "little")

if (LangMapsSize != 0):
    Langs_count = int.from_bytes(file.read(4), "little")
    if (Langs_count):
        lang_entry_size = (LangMapsSize - 4) // Langs_count
        for i in range(Langs_count):
            file.seek(lang_entry_size, 1)

BANKS = []

if (BanksSize != 0):
    Banks_count = int.from_bytes(file.read(4), "little")
    if (Banks_count):
        for i in range(Banks_count):
            entry = {}
            entry["hash"] = int.from_bytes(file.read(4), "little")
            offset_multiplier = int.from_bytes(file.read(4), "little")
            entry["size"] = int.from_bytes(file.read(4), "little")
            entry["offset"] = int.from_bytes(file.read(4), "little") * offset_multiplier
            file.seek(4, 1)
            BANKS.append(entry)

STREAMS = []
if (StreamsSize):
    Streams_count = int.from_bytes(file.read(4), "little")
    if (Streams_count):
        for i in range(Streams_count):
            entry = {}
            entry["hash"] = int.from_bytes(file.read(4), "little")
            offset_multiplier = int.from_bytes(file.read(4), "little")
            entry["size"] = int.from_bytes(file.read(4), "little")
            entry["offset"] = int.from_bytes(file.read(4), "little") * offset_multiplier
            file.seek(4, 1)
            STREAMS.append(entry)


if (ExternalSize):
    Externals_count = int.from_bytes(file.read(4), "little")
    if (Externals_count):
        External_entry_size = (ExternalSize - 4) // Externals_count
        for i in range(Externals_count):
            file.seek(External_entry_size, 1)

print("Banks detected:", len(BANKS))
print("Streams detected:", len(STREAMS))

os.makedirs("%s/BANKS" % Path(sys.argv[1]).stem, exist_ok=True)
os.makedirs("%s/STREAMS" % Path(sys.argv[1]).stem, exist_ok=True)

bank_count = len(BANKS)
for i in range(bank_count):
    print("Unpacking bank %d/%d" % (i+1, bank_count), end="\r")
    file.seek(BANKS[i]["offset"], 0)
    if (BANKS[i]["hash"] not in BANKS_IDS):
        new_file = open("%s/BANKS/%08X.bnk" % (Path(sys.argv[1]).stem, BANKS[i]["hash"]), "wb")
        print("Couldn't find name for bank: 0x%x, using hash instead..." % BANKS[i]["hash"])
    else: new_file = open("%s/BANKS/%s.bnk" % (Path(sys.argv[1]).stem, BANKS_IDS[BANKS[i]["hash"]]), "wb")
    new_file.write(file.read(BANKS[i]["size"]))
    new_file.close()

print("Unpacked all banks!         ")

stream_count = len(STREAMS)
for i in range(stream_count):
    print("Unpacking stream %d/%d" % (i+1, stream_count), end="\r")
    file.seek(STREAMS[i]["offset"], 0)
    new_file = open("%s/STREAMS/%u.wem" % (Path(sys.argv[1]).stem, STREAMS[i]["hash"]), "wb")
    new_file.write(file.read(STREAMS[i]["size"]))
    new_file.close()

print("Unpacked all streams!       ")

file.close()