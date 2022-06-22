# Script that detects image formats from unpacked PAK archives and converts them to PNG using LucaSystemTools

import sys
import os
import glob
import subprocess

files = glob.glob("%s/*" % sys.argv[1])

for i in range(0, len(files)):
    if (os.path.basename(files[i]).find(".") != -1):
        continue
    print(files[i])
    file = open(files[i], "rb")
    magic = file.read(4)
    file.close()
    if (magic[0:2] == b"CZ"):
        print(subprocess.run(["LucaSystemTool/LucaSystemTools.exe", "-t", magic[0:3].decode("ascii").lower(), "-m", "export", "-f", files[i]], capture_output=True))
    elif (magic[1:4] == b"PNG"):
        print("%s.png" % files[i][:-4])
        os.rename(files[i], "%s.png" % files[i][:-4])
    else:
        print("UNKNOWN FORMAT")