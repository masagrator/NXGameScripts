# This script is to allow packing files in the same manner as original PAKs. Game supports normal ZIPs perfectly fine.
# python Pack_PAK.py [in_folder] [pak_file]

import zipfileKC
import os
import sys
from pathlib import Path

zf = zipfileKC.ZipFile(sys.argv[2], "w", zipfileKC.ZIP_OODLE, compresslevel=2)
for dirname, subdirs, files in os.walk(sys.argv[1]):
    for filename in files:
        filepath = Path(os.path.join(dirname, filename))
        arcname = os.path.relpath(filepath, os.path.normpath(sys.argv[1]))
        print(arcname)
        zf.write(filepath, arcname)
zf.close()