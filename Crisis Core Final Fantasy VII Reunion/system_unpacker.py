# For PC change "system_jefigs.bin" to "system.bin"

import os

file = open("system_jefigs.bin", "rb")

file_count = int.from_bytes(file.read(4), "little")

DATA = []
for i in range(file_count):
    entry = {}
    entry["rel_offset"] = int.from_bytes(file.read(4), "little")
    entry["size"] = int.from_bytes(file.read(4), "little")
    DATA.append(entry)

unk = int.from_bytes(file.read(4), "little")

blob_start_offset = file.tell()

os.makedirs("system", exist_ok=True)

for i in range(file_count):
    print("Unpacking file %d/%d" % (i+1, file_count), end="\r")
    file.seek(blob_start_offset + DATA[i]["rel_offset"])
    MAGIC = file.read(4)
    file.seek(-4,1)
    filetype = "dat"
    if MAGIC[0:2] == b"GT":
        filetype = "gt"
    elif MAGIC[0:3] == b"MBD":
        filetype = "mbd"
    
    
    new_file = open("system/%02d.%s" % (i, filetype), "wb")
    new_file.write(file.read(DATA[i]["size"]))
    new_file.close()

print("Unpacked %d files.        " % file_count)
