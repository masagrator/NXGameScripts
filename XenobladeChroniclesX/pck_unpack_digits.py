import sys
from pathlib import Path

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

bank_count = len(BANKS)
for i in range(bank_count):
    print("Unpacking bank %d/%d" % (i+1, bank_count), end="\r")
    file.seek(BANKS[i]["offset"], 0)
    new_file = open("%s/%u.bnk" % (Path(sys.argv[1]).stem, BANKS[i]["hash"]), "wb")
    new_file.write(file.read(BANKS[i]["size"]))
    new_file.close()

print("Unpacked all banks!         ")

stream_count = len(STREAMS)
for i in range(stream_count):
    print("Unpacking stream %d/%d" % (i+1, stream_count), end="\r")
    file.seek(STREAMS[i]["offset"], 0)
    new_file = open("%s/%u.wem" % (Path(sys.argv[1]).stem, STREAMS[i]["hash"]), "wb")
    new_file.write(file.read(STREAMS[i]["size"]))
    new_file.close()

print("Unpacked all streams!       ")

file.close()