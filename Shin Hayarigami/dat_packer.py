import glob
import sys
import numpy
import os

def GetFileSize(file):
    pos = file.tell()
    file.seek(0, 2)
    size = file.tell()
    file.seek(pos)
    return size

def GetHeaderSize(count):
    size = 0x10 + (0x30 * count)
    if (size & 0xFFF > 0xA00):
        size += 0x1000
    size = size & 0xFFFFF000
    return size + 0xA00

files = glob.glob("%s\\*.*" % sys.argv[1])

new_file = open("%s_new.dat" % sys.argv[1], "wb")
new_file.write(b"PS_FS_V1")
new_file.write(numpy.uint64(len(files)))
header_size = GetHeaderSize(len(files))
offset = 0
for i in range(0, len(files)):
    entry = []
    entry.append(os.path.basename(files[i]).encode("ASCII"))
    while (len(b"".join(entry)) < 0x30):
        entry.append(b"\x00")
    new_file.write(b"".join(entry))
    file = open(files[i], "rb")
    new_file.write(numpy.uint64(GetFileSize(file)))
    new_file.write(numpy.uint64(header_size + offset))
    offset += numpy.uint64(GetFileSize(file))
    if (offset % 512 != 0):
        offset += 512 - (offset % 512)
if (new_file.tell() < header_size):
    new_file.seek(header_size - new_file.tell(), 1)
for i in range(0, len(files)):
    file = open(files[i], "rb")
    new_file.write(file.read())
    if (i == (len(files) - 1)):
        while(new_file.tell() % 512 != 0):
            new_file.write(b"\x00")
        break
    if (new_file.tell() % 512 != 0):
        new_file.seek(512 - (new_file.tell() % 512), 1)
new_file.close()