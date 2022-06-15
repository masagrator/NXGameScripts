# Script that detects image formats from unpacked PAK archives using LucaSystemTools

import sys
import os
import glob

files = glob.glob("%s/*" % sys.argv[1])

for i in range(0, len(files)):
    if (os.path.basename(files[i]).find(".") != -1):
        continue
    print(files[i])
    file = open(files[i], "rb")
    magic = file.read(4)
    file.close()
    if (magic[0:2] == b"CZ"):
        os.rename(files[i], files[i] + ".%s" % magic[0:3].decode("ascii"))
    elif (magic[1:4] == b"PNG"):
        os.rename(files[i], files[i] + ".png")
    else:
        print("UNKNOWN FORMAT")