import sys
import os

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("UTF-8"))
        chars.append(c)

file = open(sys.argv[1], "rb")

if (file.read(0x8) != b"PS_FS_V1"):
    print("WRONG MAGIC!")
    sys.exit()

file_count = int.from_bytes(file.read(8), "little")

filenames = []
sizes = []
offsets = []

for i in range(0, file_count):
    og_pos = file.tell()
    filenames.append(readString(file))
    file.seek(og_pos + 0x30)
    sizes.append(int.from_bytes(file.read(8), "little"))
    offsets.append(int.from_bytes(file.read(8), "little"))

os.makedirs("%s" % sys.argv[1][:-4], exist_ok=True)

for i in range(0, file_count):
    new_file = open("%s/%s" % (sys.argv[1][:-4], filenames[i]), "wb")
    file.seek(offsets[i])
    new_file.write(file.read(sizes[i]))
    new_file.close()

print("Script is finished.")
