import sys
import glob
import os
from pathlib import Path

if (os.path.isdir("%s/BANKS" % os.path.basename(os.path.normpath(sys.argv[1]))) == False):
    print("Provided path doesn't store BANKS folder, aborting...")
    sys.exit()

if (os.path.isdir("%s/STREAMS" % os.path.basename(os.path.normpath(sys.argv[1]))) == False):
    print("Provided path doesn't store STREAMS folder, aborting...")
    sys.exit()

bank_files = glob.glob("%s/BANKS/*.bnk" % os.path.normpath(sys.argv[1]))
stream_files = glob.glob("%s/STREAMS/*.wav" % os.path.normpath(sys.argv[1]))

print("Detected %d bank files and %d stream files. Packing..." % (len(bank_files), len(stream_files)))

os.makedirs("PACKED", exist_ok=True)

new_file = open("PACKED/%s.pck" % os.path.basename(os.path.normpath(sys.argv[1])), "wb")
offset = 0x2C
header_size = offset + 4 + (len(bank_files) * 0x14) + 4 + (len(stream_files) * 0x14) + 4

bank_start = header_size
if (bank_start % 0x10 != 0):
    bank_start += 0x10 - (bank_start % 0x10)

new_file.write(b"AKPK")
new_file.write((header_size - 8).to_bytes(4, "little"))
new_file.write(0x1.to_bytes(4, "little"))
new_file.write(0x10.to_bytes(4, "little"))
new_file.write((4 + (0x14 * len(bank_files))).to_bytes(4, "little"))
new_file.write((4 + (0x14 * len(stream_files))).to_bytes(4, "little"))
new_file.write(0x4.to_bytes(4, "little"))

#lang
new_file.write(0x1.to_bytes(4, "little"))
new_file.write(0xC.to_bytes(8, "little"))
new_file.write(b"sfx\x00")

files_offset = bank_start

print("Sorting bank files in numerical order...")
new_file.write(len(bank_files).to_bytes(4, "little"))
BANKS = {}
for i in range(len(bank_files)):
    bank_file = open(bank_files[i], "rb")
    if (bank_file.read(4) != b"BKHD"):
        print("%s: Wrong MAGIC! Aborting..." % bank_files[i])
        bank_file.close()
        new_file.close()
        os.remove("PACKED/%s.pck" % os.path.basename(os.path.normpath(sys.argv[1])))
        sys.exit()
    bank_file.seek(0xC)
    hash = int.from_bytes(bank_file.read(4), "little")
    bank_file.close()
    if (hash in BANKS.keys()):
        print("Doubled key detected! 0x%x" % hash)
        print("File: %s" % bank_files[i])
        print("Already used by: %s" % BANKS[hash])
        sys.exit()
    BANKS[hash] = bank_files[i]

BANKS = dict(sorted(BANKS.items()))
keys = list(BANKS.keys())

for i in range(len(keys)):
    size = os.path.getsize(BANKS[keys[i]])
    new_file.write(keys[i].to_bytes(4, "little"))
    offset_multiplier = 0x10
    new_file.write(offset_multiplier.to_bytes(4, "little"))
    new_file.write(size.to_bytes(4, "little"))
    new_file.write((files_offset // offset_multiplier).to_bytes(4, "little"))
    new_file.write(b"\x00\x00\x00\x00")
    files_offset += size
    if (files_offset % 0x10 != 0):
        files_offset += 0x10 - (files_offset % 0x10)

print("Sorting stream files in numerical order...")
STREAMS = {}
new_file.write(len(stream_files).to_bytes(4, "little"))
for i in range(len(stream_files)):
    hash = bytes.fromhex(Path(stream_files[i]).stem)
    hash = int.from_bytes(hash, "big")
    if (hash in STREAMS.keys()):
        print("Doubled key detected! 0x%x" % hash)
        print("File: %s" % stream_files[i])
        print("Already used by: %s" % STREAMS[hash])
    STREAMS[hash] = stream_files[i]

STREAMS = dict(sorted(STREAMS.items()))
keys2 = list(STREAMS.keys())

for i in range(len(keys2)):
    size = os.path.getsize(STREAMS[keys2[i]])
    new_file.write(keys2[i].to_bytes(4, "little"))
    offset_multiplier = 0x10
    new_file.write(offset_multiplier.to_bytes(4, "little"))
    new_file.write(size.to_bytes(4, "little"))
    new_file.write((files_offset // offset_multiplier).to_bytes(4, "little"))
    new_file.write(b"\x00\x00\x00\x00")
    files_offset += size
    if (files_offset % 0x10 != 0):
        files_offset += 0x10 - (files_offset % 0x10)

new_file.write(b"\x00\x00\x00\x00")
if (new_file.tell() % 0x10 != 0):
    new_file.write(b"\x00" * (0x10 - (new_file.tell() % 0x10)))

assert(new_file.tell() == bank_start)
for i in range(len(keys)):
    print("Bank file %d/%d" % (i+1, len(bank_files)), end="\r")
    file = open(BANKS[keys[i]], "rb")
    new_file.write(file.read())
    file.close()
    if (new_file.tell() % 0x10 != 0):
        new_file.write(b"\x00" * (0x10 - (new_file.tell() % 0x10)))

for i in range(len(keys2)):
    print("Stream file %d/%d" % (i+1, len(keys2)), end="\r")
    file = open(STREAMS[keys2[i]], "rb")
    new_file.write(file.read())
    file.close()
    if ((i+1 < len(keys2)) and (new_file.tell() % 0x10 != 0)):
        new_file.write(b"\x00" * (0x10 - (new_file.tell() % 0x10)))

new_file.close()

print("Packing finished!         ")
print("You can find file at:")
print("PACKED/%s.pck" % os.path.basename(os.path.normpath(sys.argv[1])))