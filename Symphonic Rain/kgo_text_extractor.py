import sys
import os
import json
import glob

def readString(myfile):
	chars = []
	while True:
		c = myfile.read(1)
		if c == b'\x00':
			return str(b"".join(chars).decode("UTF-8"))
		chars.append(c)

files = glob.glob("KGO\*.kgo")

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

    file.seek(text_blob_start)

    Texts = []

    for i in range(0, text_count):
        temp = file.tell()
        block_size = int.from_bytes(file.read(0x2), byteorder="little")
        Texts.append(readString(file))
        file.seek(temp + block_size)

    os.makedirs("Texts", exist_ok=True)
    file_new = open("Texts/%s.json" % files[x][4:-4], "w", encoding="UTF-8")
    json.dump(Texts, file_new, indent="\t", ensure_ascii=False)