import sys
from pathlib import Path
import subprocess

arguments = len(sys.argv)
if (arguments != 2 and arguments != 5):
    print("Wrong arguments!")
    print("python Convert.py input_s16le.wav")
    sys.exit()

frame_size = 480
subprocess.run(["NXAenc.exe", "-i", sys.argv[1], "-o", Path(sys.argv[1]).stem + ".wem", "-f", "%d" % frame_size])
print("")
wem_file = open(Path(sys.argv[1]).stem + ".wem", "rb")
wem_file.seek(0x24)
size = int.from_bytes(wem_file.read(4), "little")
assert(frame_size == int.from_bytes(wem_file.read(4), "big"))
frame_size += 8
frame_count =  size // frame_size
wem_file.seek(-4, 1)
frames = []
for i in range(frame_count):
    frames.append(wem_file.read(frame_size))
wem_file.close()
frame_count -= 1
frames.pop(0)
data = []
channel_count = 2
sample_rate = 48000
data.append(b"RIFF")
data.append(0x0.to_bytes(4, "little"))
data.append(b"WAVEfmt ")
data.append(0x28.to_bytes(4, "little")) #WAVEfmt header size
codec_format = 12345 #NSOPUS
data.append(codec_format.to_bytes(2, "little"))
data.append(channel_count.to_bytes(2, "little"))
data.append(sample_rate.to_bytes(4, "little"))
data.append((192000).to_bytes(4, "little")) #Average bitrate
data.append((4).to_bytes(2, "little")) #block size (?)
bits_per_sample = 16
data.append(bits_per_sample.to_bytes(2, "little"))
data.append((6).to_bytes(2, "little")) #size of extra segment
samples_per_channel = 960
data.append((samples_per_channel).to_bytes(2, "little"))
data.append((12546).to_bytes(4, "little"))
data.append((frame_count * samples_per_channel).to_bytes(8, "little"))
data.append(size.to_bytes(4, "little"))
data.append((frame_count * 4).to_bytes(4, "little"))
data.append(b"data")
data.append((size + (frame_count * 4)).to_bytes(4, "little"))
offset = 0
for i in range(frame_count):
    data.append(offset.to_bytes(4, "little"))
    offset += frame_size
data.append(b"".join(frames))
data[1] = (len(b"".join(data)) - 8).to_bytes(4, "little")

new_file = open("%s.wem" % Path(sys.argv[1]).stem, "wb")
new_file.write(b"".join(data))
new_file.close()
print("Finished conversion. Sample count: %d, miliseconds: %f" % ((frame_count * samples_per_channel), (frame_count * samples_per_channel) / 48))