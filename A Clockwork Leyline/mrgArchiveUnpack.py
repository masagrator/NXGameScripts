import sys
from pathlib import Path
import os

DATA = []

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("UTF-8"))
        chars.append(c)

print()
try:
    file = open(f"{os.path.dirname(os.path.abspath(sys.argv[1]))}{os.path.sep}{Path(sys.argv[1]).stem}.hed", "rb")
except:
    print(f"Not detected {Path(sys.argv[1]).stem}.hed file!")
    print(f"You are trying to unpack mrg file that is not an archive.")
    sys.exit()
else:
    while(True):
        start_pos = int.from_bytes(file.read(2), "little", signed=True)
        if (start_pos == -1):
            break
        entry = {}
        entry["START_POS"] = start_pos * 0x800
        unk = int.from_bytes(file.read(2), "little", signed=True)
        entry["READ_BUFFER"] = int.from_bytes(file.read(2), "little", signed=True) * 0x800
        entry["UNC_BUFFER_SIZE"] = int.from_bytes(file.read(2), "little", signed=True) * 0x800
        DATA.append(entry)

    file.close()

FILENAMES = []

try:
    file = open(f"{os.path.dirname(os.path.abspath(sys.argv[1]))}{os.path.sep}{Path(sys.argv[1]).stem}.nam", "rb")
except:
    print(f"Not detected {Path(sys.argv[1]).stem}.nam file!")
else:
    i = 0
    while(True):
        file.seek(i * 0x20)
        string = readString(file)
        if len(string) == 0:
            break
        FILENAMES.append(string)
        i += 1
    file.close()

file = open(sys.argv[1], "rb")
os.makedirs(Path(sys.argv[1]).stem, exist_ok=True)
if FILENAMES != []:
    for i in range(len(FILENAMES)):
        print(FILENAMES[i])
        new_file = open(f"{Path(sys.argv[1]).stem}/{FILENAMES[i]}", "wb")
        file.seek(DATA[i]["START_POS"])
        new_file.write(file.read(DATA[i]["READ_BUFFER"]))
        new_file.close()
else:
    for i in range(len(DATA)):
        print("%04d.dat" % i)
        new_file = open("%s/%04d.dat" % (Path(sys.argv[1]).stem, i), "wb")
        file.seek(DATA[i]["START_POS"])
        new_file.write(file.read(DATA[i]["READ_BUFFER"]))
        new_file.close()

file.close()