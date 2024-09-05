import sys
import os
import zlib
from array import array

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("ascii"))
        chars.append(c)

def GenerateKey(string):
    table = [5, 6, 4, 5, 6, 5, 4, 5, 5, 6, 6, 5, 6, 4, 6, 4]
    root = "data:/cdvdroot/"
    filename = string
    root += filename
    root = root.encode("ascii")
    strlen = len(root) #X0
    X18 = 0x1A7B9611A7B9611B
    X8 = -1
    W16 = 0x5C
    W0 = 0x1D
    W10 = 0
    W9 = 0
    while(True):
        W12 = root[X8]
        W11 = W12 - 0x61
        W11 &= 0xFF
        if (W11 < 0x1A):
            W11 = W12 - 0x20
        else:
            W11 = W12
        if (W12 == 0x2F):
            break
        W12 = W11 & 0xFF
        if (W12 == 0x5C):
            break
        W11 = W12
        W10 += 1
        W9 = (W10 * W11) + W9
        X8 -= 1
        if (abs(X8) == len(root)):
            break
    iter = W10
    root = "/" + filename
    root = root.encode("ascii")
    W12 = root[1]
    W9 += W10
    W11 = 0
    W10 = 2
    W8 = W9
    for i in range(iter):
        W14 = W12 - 0x61
        W13 = W12 & 0xFF
        W14 &= 0xFF
        if (W14 < 0x1A):
            W12 -= 0x20
        if (W13 == 0x2F):
            W12 = W16
        W12 &= 0xFF
        W12 -= 0x30
        W12 <<= W11
        W8 += W12
        W8 &= 0xFFFFFFFF
        if (W10 == len(root)):
            break
        W12 = W9 & 0xF
        W12 &= 0xFFFFFFFF
        W9 += 1
        W12 = table[W12]
        W11 += W12
        W11 &= 0xFFFFFFFF
        W12 = W11 * X18
        W12 >>= 64
        W13 = W11 - W12
        W12 += (W13 >> 1)
        W12 >>= 4
        W12 &= 0xFFFFFFFF
        W11 = W11 - (W12 * W0)
        W11 &= 0xFFFFFFFF
        W12 = root[W10]
        W10 += 1
    return W8



def Keygen(key):
    RDI_TABLE = [0] * 64
    itr1 = 0 #W8
    w27 = 0xb1aef645
    while(True):
        w13 = 0
        itr2 = 0
        while(True):
            w14 = key + (key << 2)
            w14 &= 0xFFFFFFFF
            flag = w13 == 0
            w15 = w13 - 1
            w14 = w14 + w27
            w14 &= 0xFFFFFFFF
            w14 >>= 1
            w14 &= 0xFFFFFFFF
            if (flag == True):
                key = w14
                w12 = w14
            w14 = RDI_TABLE[itr2]
            w13 = w12 & 1
            w12 = w12 // 2
            w13 <<= itr1
            w13 &= 0xFFFFFFFF
            w13 |= w14
            w13 &= 0xFFFFFFFF
            RDI_TABLE[itr2] = w13
            itr2 += 1
            if (flag == True):
                w13 = 30
            else:
                w13 = w15
            if (itr2 == 64):
                break
        itr1 += 1
        if (itr1 == 32):
            break
    return RDI_TABLE

RDI_KEY = GenerateKey("RES00.RDI")
KEYTABLE = Keygen(RDI_KEY)

RDI_FILE = open("RES00.RDI", "rb")
RDI_FILE.seek(0, 2)
filesize = RDI_FILE.tell()
RDI_FILE.seek(0)

RDI_INTS = []
while(RDI_FILE.tell() < filesize):
    RDI_INTS.append(int.from_bytes(RDI_FILE.read(4), "little"))
RDI_FILE.close()

RDI_OUTPUT = []
for i in range(len(RDI_INTS)):
    KEYTABLE[i % 64] = KEYTABLE[i % 64] ^ KEYTABLE[(i+3) % 64]
    RDI_OUTPUT.append((RDI_INTS[i] ^ KEYTABLE[(i+1) % 64]).to_bytes(4, "little"))

file = open("DEC_RES00.RDI", "wb")
file.write(b"".join(RDI_OUTPUT))
file.close()

os.makedirs("RES", exist_ok=True)

file = open("DEC_RES00.RDI", "rb")
if (file.read(4) != b"RDI2"):
    print("WRONG MAGIC!")
    sys.exit()

file.seek(0, 2)
filesize = file.tell()
file.seek(4)
flag1 = int.from_bytes(file.read(2), "little")
assert(flag1 == 1)
flag2 = int.from_bytes(file.read(2), "little")
assert(flag2 in [0, 2])
if filesize != int.from_bytes(file.read(4), "little"):
    print("SIZE CHECK FAILED!")
    sys.exit()
flag3 = int.from_bytes(file.read(4), "little")
if (flag3 == 2):
    print("Detected index with patch, patch RES11.RDB not supported...")
file_count = int.from_bytes(file.read(4), "little")
file_count2 = int.from_bytes(file.read(4), "little")
assert(file_count == file_count2)
flag4 = int.from_bytes(file.read(4), "little")
assert(flag4 == 0)
flag5 = int.from_bytes(file.read(4), "little")
assert(flag5 == 2)
flag6 = int.from_bytes(file.read(4), "little")
assert(flag6 == 0x10)
last_table_entries = int.from_bytes(file.read(4), "little")
flag8 = int.from_bytes(file.read(8), "little")
assert(flag8 == 0)
some_offset = int.from_bytes(file.read(4), "little")
some_number = int.from_bytes(file.read(4), "little")
if (flag3 == 2):
    some_offset2 = int.from_bytes(file.read(4), "little")
    some_number2 = int.from_bytes(file.read(4), "little")

TABLE = []
for i in range(file_count):
    entry = {}
    entry["NAME_OFFSET"] = int.from_bytes(file.read(4), "little")
    TABLE.append(entry)

flags = []
for i in range(file_count):
    TABLE[i]["OFFSET"] = int.from_bytes(file.read(4), "little")
    TABLE[i]["DEC_SIZE"] = int.from_bytes(file.read(4), "little")
    TABLE[i]["flag"] = int.from_bytes(file.read(1), "little")
    if (TABLE[i]["flag"] not in flags):
        flags.append(TABLE[i]["flag"])
    if (TABLE[i]["flag"] in [0x20, 0]):
        TABLE[i]["OFFSET"] = TABLE[i]["OFFSET"] * 0x200
    else: 
        TABLE[i]["ID"] = TABLE[i]["OFFSET"]
        TABLE[i].pop("OFFSET")

TABLE2 = {}
for i in range(last_table_entries):
    entry = {}
    entry["OFFSET"] = "0x%X" % (int.from_bytes(file.read(4), "little") * 0x200)
    entry["PATCH_SIZE"] = "0x%X" % int.from_bytes(file.read(4), "little")
    TABLE2[i] = entry

base = file.tell()
for i in range(file_count):
    file.seek(base + TABLE[i]["NAME_OFFSET"])
    TABLE[i]["FILENAME"] = readString(file)
    TABLE[i].pop("NAME_OFFSET")

file.close()

file = open("RES00.RDB", "rb")
for i in range(len(TABLE)):
    if (TABLE[i]["flag"] > 0x20):
        continue
    print("%d/%d: %s" % (i+1, len(TABLE), TABLE[i]["FILENAME"]))
    file.seek(TABLE[i]["OFFSET"])
    DATA = array('I')
    DATA.fromfile(file, TABLE[i]["DEC_SIZE"] // 4)

    KEYTABLE = Keygen(RDI_KEY ^ GenerateKey(TABLE[i]["FILENAME"]))
    RDI_OUTPUT = []
    for x in range(len(DATA)):
        KEYTABLE[x % 64] = KEYTABLE[x % 64] ^ KEYTABLE[(x+3) % 64]
        RDI_OUTPUT.append((DATA[x] ^ KEYTABLE[(x+1) % 64]).to_bytes(4, "little"))  

    filesize = RDI_OUTPUT[6]
    try:
        dec_data = zlib.decompress(b"".join(RDI_OUTPUT[8:]))
    except:
        print("Failed decompressing data! Dumping raw file to \"FAILED\" folder. Ignoring...")
        os.makedirs("FAILED/RAW", exist_ok=True)
        os.makedirs("FAILED/DECRYPTED", exist_ok=True)
        new_file = open("FAILED/DECRYPTED/%s" % TABLE[i]["FILENAME"], "wb")
        new_file.write(b"".join(RDI_OUTPUT))
        new_file.close()
        new_file = open("FAILED/RAW/%s" % TABLE[i]["FILENAME"], "wb")
        for x in range(len(DATA)):
            new_file.write(DATA[x].to_bytes(4, "little"))
        new_file.close()
        continue
    new_file = open("RES/%s" % TABLE[i]["FILENAME"], "wb")
    new_file.write(b"".join(RDI_OUTPUT[0:8]))
    new_file.write(dec_data)
    new_file.close()