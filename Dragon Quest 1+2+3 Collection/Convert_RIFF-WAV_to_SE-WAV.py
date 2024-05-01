import subprocess
import os
import sys
from pathlib import Path

os.makedirs("Converted", exist_ok=True)

file = open(sys.argv[1], "rb")
file.seek(0x16)
channel_count = int.from_bytes(file.read(2), "little")
file.close()

for i in range(channel_count):
    subprocess.run(["VgAudioCli.exe", "-c", "-i:%d" % i, "%s" % sys.argv[1], "%s-%d.dsp" % (sys.argv[1][:-4], i+1)])

data = []
for i in range(channel_count):
    file = open("%s-%d.dsp" % (sys.argv[1][:-4], i+1), "rb")
    data.append(file.read())
    file.close()

new_file = open(f"Converted/{Path(sys.argv[1]).stem}.wav", "wb")
new_file.write(b"\x00" * 4)
new_file.write(channel_count.to_bytes(4, "little"))
header_size = 0x40
new_file.write(header_size.to_bytes(4, "little"))
for i in range(channel_count):
    new_file.write(len(data[i]).to_bytes(4, "little"))
    if (i + 1 != channel_count):
        offset = len(data[i]) + (0x100 - (len(data[i]) % 0x100)) + header_size
        new_file.write(offset.to_bytes(4, "little"))
new_file.write(b"\x00" * (header_size - (new_file.tell() % header_size)))
for i in range(channel_count):
    new_file.write(data[i])
    new_file.write(b"\x00" * (0x100 - ((new_file.tell() - header_size) % 0x100)))
new_file.close()