import sys
import os
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

RDI_KEY = Keygen(GenerateKey("RES00.RDI"))

RDI_FILE = open(sys.argv[1], "rb")
RDI_FILE.seek(0, 2)
filesize = RDI_FILE.tell()
RDI_FILE.seek(0)

RDI_INTS = []
while(RDI_FILE.tell() < filesize):
    RDI_INTS.append(int.from_bytes(RDI_FILE.read(4), "little"))
RDI_FILE.close()

RDI_OUTPUT = []
for i in range(len(RDI_INTS)):
    RDI_KEY[i % 64] = RDI_KEY[i % 64] ^ RDI_KEY[(i+3) % 64]
    RDI_OUTPUT.append((RDI_INTS[i] ^ RDI_KEY[(i+1) % 64]).to_bytes(4, "little"))

file = open("DEC_RES00.RDI", "wb")
file.write(b"".join(RDI_OUTPUT))
file.close()