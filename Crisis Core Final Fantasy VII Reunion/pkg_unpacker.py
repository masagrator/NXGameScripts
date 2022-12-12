import zlib
import sys
import os
import math

file = open("discimg_jefigs.pkg", "rb")

if (file.read(4) != b"FGKP"):
    print("WRONG MAGIC!")
    sys.exit()

entry_size = int.from_bytes(file.read(4), "little")
if (entry_size != 16):
    print("WRONG ENTRY SIZE!")
    sys.exit()

entry_count = int.from_bytes(file.read(8), "little")

DATA = []

for i in range(entry_count):
    isEntry = int.from_bytes(file.read(4), "little")
    if (isEntry == 0):
        file.seek(12,1)
        continue
    entry = {}
    entry["ID"] = i
    entry["unc_size"] = int.from_bytes(file.read(4), "little")
    entry["offset"] = int.from_bytes(file.read(8), "little")
    DATA.append(entry)

filtered_entry_count = len(DATA)

os.makedirs("unpacked", exist_ok=True)

for i in range(filtered_entry_count):
    print("Unpacking file: %d/%d" % (i+1, filtered_entry_count), end="\r")
    file.seek(DATA[i]["offset"])
    chunks = []
    for x in range(math.ceil(DATA[i]["unc_size"] / 0x8000)):
        chunks.append(int.from_bytes(file.read(4), "little"))
    chunks_count = len(chunks)
    new_file = open("unpacked/%05d.dat" % DATA[i]["ID"], "wb")
    for x in range(chunks_count):
        buffer = file.read(chunks[x])
        unc_buffer = zlib.decompress(buffer, bufsize=0x8000)
        new_file.write(unc_buffer)
    new_file.close()