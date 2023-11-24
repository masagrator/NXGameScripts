import os
from PIL import Image

os.makedirs("new_font48", exist_ok=True)

DUMP = []

DUMP.append(b"xtx\x00")
DUMP.append(b"\x05\x00\x00\x00")
DUMP.append((1536).to_bytes(4, "big"))
DUMP.append((3072).to_bytes(4, "big"))
DUMP.append((1536).to_bytes(4, "big"))
DUMP.append((3072).to_bytes(4, "big"))
DUMP.append((0).to_bytes(4, "big"))
DUMP.append((0).to_bytes(4, "big"))

channels = []
for i in range(4):
    image = Image.open("font48/%d.png" % i)
    raw = image.tobytes("raw")
    channels.append(raw[3::4])
    image.close()

new_raw = []

for i in range(len(channels[0])):
    R = channels[0][i] >> 4
    G = channels[1][i]
    B = channels[2][i] >> 4
    A = channels[3][i]

    RG = G | R
    BA = B | A

    new_raw.append(RG.to_bytes(1, "little"))
    new_raw.append(BA.to_bytes(1, "little"))

new_file = open("new_font48/font48.xtx", "wb")
new_file.write(b"".join(DUMP))
new_file.write(b"".join(new_raw))
new_file.close()