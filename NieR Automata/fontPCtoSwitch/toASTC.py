import subprocess
import glob
import sys
from pathlib import Path
from PIL import Image
import convert
import os

files = glob.glob(f"{sys.argv[1]}_*.dds")

for i in range(0, len(files)):
    img = Image.open(files[i])
    img.save(f"{sys.argv[1]}_{i}.png")
    img.close()
    subprocess.run(["astcenc-avx2.exe", "-cl", f"{sys.argv[1]}_{i}.png", f"{sys.argv[1]}_{i}.astc", "4x4", "-thorough"])
    convert.lib(f"{sys.argv[1]}_{i}.astc", f"{sys.argv[1]}_{i}_swizzled.astc")