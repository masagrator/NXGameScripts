import os

os.makedirs("sn", exist_ok=True)

file = open("sn_dec.bin", "rb")

Offsets = []
Sizes = []

header_size = int.from_bytes(file.read(0x4), byteorder="little")
file.seek(0)

while(file.tell() < header_size):
    Offsets.append(int.from_bytes(file.read(0x4), byteorder="little"))
    Sizes.append(int.from_bytes(file.read(0x4), byteorder="little"))
    file.seek(8, 1)

for i in range(0, len(Offsets)):
    file.seek(Offsets[i])
    file_new = open("sn/%04d-%06x.bin" % (i, file.tell()), "wb")
    file_new.write(file.read(Sizes[i]))
    file_new.close()