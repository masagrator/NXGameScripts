# python Unpack_PAK.py [pak_file] [folder_out]

import zipfileKC
import sys

zf = zipfileKC.ZipFile(sys.argv[1], "r", print_names = True)
zf.extractall(sys.argv[2])
zf.close()