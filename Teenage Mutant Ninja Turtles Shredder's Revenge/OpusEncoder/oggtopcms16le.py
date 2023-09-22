import os
import sys
import pydub
import glob
from pathlib import Path

files = glob.glob(f"{sys.argv[1]}/*.ogg")
os.makedirs("converted", exist_ok=True)

for i in range(0, len(files)):
    print(Path(files[i]).stem)
    orig_audio = pydub.AudioSegment.from_ogg(files[i])
    orig_audio = orig_audio.set_frame_rate(48000)
    orig_audio.export(out_f = "converted/%s.pcm" % Path(files[i]).stem, format="s16le")
