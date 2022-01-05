import sys
import os
import json
import glob
import numpy

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("UTF-8"))
		chars.append(c)

files = glob.glob("KGO\*.kgo")

os.makedirs("New_KGO", exist_ok=True)

for x in range(0, len(files)):

    file = open(files[x], "rb")

    if (file.read(0x4) != b"SR10"): #0x0
        print("WRONG MAGIC!")
        sys.exit()

    Main = {}
    Main["HEADER"] = {}

    SIZE = int.from_bytes(file.read(0x4), byteorder="little") #0x4
    Main["HEADER"]["FILE_ID"] = int.from_bytes(file.read(0x4), byteorder="little") #0x8
    Main["HEADER"]["CRC"] = file.read(0x4).hex().upper() #0xC
    registration_offset = int.from_bytes(file.read(0x4), byteorder="little") #0x10
    registration_size = int.from_bytes(file.read(0x4), byteorder="little") #0x14
    registration_entries = int.from_bytes(file.read(0x4), byteorder="little") #0x18
    command_block_offset = int.from_bytes(file.read(0x4), byteorder="little") #0x1C
    command_block_size = int.from_bytes(file.read(0x4), byteorder="little") #0x20
    command_block_entries = int.from_bytes(file.read(0x4), byteorder="little") #0x24
    text_block_registration_offset = int.from_bytes(file.read(0x4), byteorder="little") #0x28
    text_block_registration_size = int.from_bytes(file.read(0x4), byteorder="little") #0x2C
    text_block_registration_entries = int.from_bytes(file.read(0x4), byteorder="little") #0x30
    text_blob_start = int.from_bytes(file.read(0x4), byteorder="little") #0x34
    text_blob_size = int.from_bytes(file.read(0x4), byteorder="little") #0x38
    text_count = int.from_bytes(file.read(0x4), byteorder="little") #0x3C

    file.seek(0)

    data = file.read(text_blob_start)

    jsonfile = open("Texts/%s.json" % files[x][4:-4], "r", encoding="UTF-8")
    dump = json.load(jsonfile)
    jsonfile.close()
    if (len(dump) != text_count):
        print("Detected wrong text count!")
        print("Original file has %d text strings." % text_count)
        print("Detected JSON has %d text strings." % len(dump))
        print("ABORTING...")
        sys.exit()

    text_block = []
    for i in range(0, text_count):
        block_length = len(dump[i].encode("UTF-8")) + 2 + 1
        if (block_length % 2 != 0):
            text_block.append(numpy.uint16(block_length + 1))
        else:
            text_block.append(numpy.uint16(block_length))
        text_block.append(dump[i].encode("UTF-8"))
        if (block_length % 2 != 0):
            text_block.append(b"\x00\x00")
        else:
            text_block.append(b"\x00")

    file_new = open("New_KGO/%s" % files[x][4:], "wb")
    file_new.write(data)
    file_new.write(b"".join(text_block))
    while (file_new.tell() % 16 != 0):
        file_new.write(b"\x00")
    file_new.seek(0x38)
    file_new.write(numpy.uint32(len(b"".join(text_block))))
    file_new.close()