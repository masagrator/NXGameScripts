# Author: MasaGratoR
# This tool converts PC save of Don't Starve Together to format compatible with Nintendo Switch saves

# Provide correct folder with files from PC version of game as argument
# Folder name should have 16 random characters like "04305C68F3229C15". It must have 4 files: 0000000002, 0000000002.meta, 0000000003, 0000000003.meta
# You can find them in Master/save/session and Caves/save/session in any Cluster.
# Converted folder will be outputted to ConvertedSave folder.
# Copy sdfs files and replace them on Switch in the same path (So session from Caves goes to Caves, and Master to Master). 
# Ignore that folder in Switch save with sdfs files will have different 16 random characters than on PC.

import sys
from pathlib import Path
import zlib
import os

files_main = ["0000000002", "0000000003"]

os.makedirs(f"ConvertedSave/{os.path.basename(os.path.normpath(sys.argv[1]))}", exist_ok=True)

for i in range(len(files_main)):

    file = open(f"{sys.argv[1]}/{files_main[i]}", "r", encoding="ascii")
    buffer = file.read().encode("ascii")
    file.close()

    new_file = open(f"ConvertedSave/{os.path.basename(os.path.normpath(sys.argv[1]))}/{files_main[i]}.sdfs", "wb")
    new_file.write(len(files_main[i]).to_bytes(4, "little"))
    new_file.write(files_main[i].encode("ascii"))
    new_file.write(b"\x00\x80\x00\x00\x00\x00\x00\x00")
    new_file.write(zlib.crc32(buffer).to_bytes(4, "little")) # This value is random, putting zlib.crc32 just for fun
    new_file.write((i + 2).to_bytes(1, "little"))
    new_file.write(b"\x01\x00\x00")
    new_file.write(0x4.to_bytes(4, "little")) # Compression flag

    com_buffer = zlib.compress(buffer)

    new_file.write((len(com_buffer) + 0x10).to_bytes(4, "little"))
    new_file.write(0x1.to_bytes(4, "little"))
    new_file.write(0x10.to_bytes(4, "little"))
    new_file.write(len(buffer).to_bytes(4, "little"))
    new_file.write(len(com_buffer).to_bytes(4, "little"))
    new_file.write(com_buffer)
    new_file.close()

for i in range(len(files_main)):

    file = open(f"{sys.argv[1]}/{files_main[i]}.meta", "r", encoding="ascii")
    buffer = file.read().encode("ascii")
    file.close()

    filename = files_main[i] + ".meta"

    new_file = open(f"ConvertedSave/{os.path.basename(os.path.normpath(sys.argv[1]))}/{filename}.sdfs", "wb")
    new_file.write(len(filename).to_bytes(4, "little"))
    new_file.write(filename.encode("ascii"))
    new_file.write(b"\x00\x80\x00\x00\x00\x00\x00\x00")
    new_file.write(zlib.crc32(buffer).to_bytes(4, "little")) # This value is random, putting zlib.crc32 just for fun
    new_file.write((i + 2).to_bytes(1, "little"))
    new_file.write(b"\x01\x00\x00")
    new_file.write(0x0.to_bytes(4, "little")) # No compression

    new_file.write(len(buffer).to_bytes(4, "little"))
    new_file.write(buffer)
    new_file.close()