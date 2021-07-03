import numpy
import os

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("Shift-JIS"))
        chars.append(c)

MAGIC = b"RSC\x00"
page_align = 0x10

filelist = []

for s in os.listdir():
    if s.endswith(".bin"): 
        if (s.startswith("a") and not s.endswith("_newgame.bin")): filelist.append(s)
        elif (s.startswith("b") and not s.endswith("_newgame.bin")): filelist.append(s)
        elif s.startswith("c"): filelist.append(s)

for x in range(0, len(filelist)):
    file = open(filelist[x], "rb")

    if (file.read(4) == b"RSI\x00"):
        file.close()
        continue
    
    file.seek(0,0)
    
    if (MAGIC != file.read(4)):
        file.seek(0,0)
        raise ValueError("Wrong Magic! File: %s, MAGIC: %s" % (filelist[x], file.read(4)))

    file.seek(0x10, 0)

    text_block_offset = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0] + 0x20
    text_block_size = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
    offset_block_size = numpy.fromfile(file, dtype=numpy.uint32, count=1)[0]
    file.seek(0, 2)
    offset_block_offset = file.tell() - offset_block_size
    file.seek(text_block_offset, 0)

    listing = []

    while (((file.tell() + 0x10) & 0xFFFFFF0) < text_block_offset + text_block_size):
        text = readString(file)
        if (text != ""): listing.append(text)

    file.close()

    new_file = open("%s.tsv" % (filelist[x][:-4]), "w", encoding="UTF-8")
    for i in range(0, len(listing)-1):
        new_file.write(listing[i])
        new_file.write("\n")
    new_file.close()
    listing.clear()