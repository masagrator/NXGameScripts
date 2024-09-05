

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

RDI_KEY = Keygen(0xf006f0c9)

print(RDI_KEY)

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
    RDI_KEY[i % 64] = RDI_KEY[i % 64] ^ RDI_KEY[(i+3) % 64]
    RDI_OUTPUT.append((RDI_INTS[i] ^ RDI_KEY[(i+1) % 64]).to_bytes(4, "little"))

file = open("dump.bin", "wb")
file.write(b"".join(RDI_OUTPUT))
file.close()