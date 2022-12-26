# On PC file name is "discimg.pkg"

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
    unc_buffer_size = int.from_bytes(file.read(4), "little")
    if (unc_buffer_size == 0):
        file.seek(12,1)
        continue
    entry = {}
    entry["unc_buffer_size"] = unc_buffer_size
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
    for x in range(math.ceil(DATA[i]["unc_size"] / DATA[i]["unc_buffer_size"])):
        chunks.append(int.from_bytes(file.read(4), "little"))
    datatype = "dat"
    for x in range(len(chunks)):
        unc_buffer = zlib.decompress(file.read(chunks[x]), bufsize=DATA[i]["unc_buffer_size"])
        if (x == 0):
            MAGIC = unc_buffer[0:4]
            if MAGIC == b"Atel":
                datatype = "atel"
            elif MAGIC[0:2] == b"GT":
                datatype = "gt"
            elif MAGIC[0:3] == b"MBD":
                datatype = "mbd"
            elif MAGIC[0:3] == b"FRR":
                datatype = "frr"
            elif MAGIC[0:3] == b"FEP":
                datatype = "fep"
            elif MAGIC[0:3] == b"FBT":
                datatype = "fbt"
            elif MAGIC[0:3] == b"EPF":
                datatype = "epf"
            new_file = open("unpacked/%05d.%s" % (DATA[i]["ID"], datatype), "wb")
        new_file.write(unc_buffer)
    new_file.close()
print(f"Unpacked successfully {filtered_entry_count} files.")
