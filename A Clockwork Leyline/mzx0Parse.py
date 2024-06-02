import os
import json
from pathlib import Path
import sys
import struct
from io import BytesIO

"""
mzx0_decompress() taken from
https://github.com/Hintay/PS-HuneX_Tools/blob/ad40001f9ea6c44ecfe75db723fccb5b942d0462/tools/mzx/decomp_mzx0.py

and slightly modified
"""

def mzx0_decompress(f, xorff=False) -> bytes:
    """
    Decompress a block of data.
    """
    key = 0xFF

    if (f.read(4) != b"MZX0"):
        print("WRONG MAGIC!")
        f.close()
        sys.exit()
    
    file.seek(0, 2)
    max = file.tell()
    file.seek(4)
    exlen = int.from_bytes(file.read(4), "little")

    out_data = BytesIO()  # slightly overprovision for writes past end of buffer
    ring_buf = [b'\xFF\xFF'] * 64 if xorff else [b'\x00\x00'] * 64
    ring_wpos = 0

    clear_count = 0
    last = b'\xFF\xFF' if xorff else b'\x00\x00'

    while out_data.tell() < exlen:
        if f.tell() >= max:
            break
        if clear_count <= 0:
            clear_count = 0x1000
            last = b'\xFF\xFF' if xorff else b'\x00\x00'
        flags = ord(f.read(1))

        clear_count -= 1 if (flags & 0x03) == 2 else flags // 4 + 1

        if flags & 0x03 == 0:
            out_data.write(last * ((flags // 4) + 1))

        elif flags & 0x03 == 1:
            k = 2 * (ord(f.read(1)) + 1)
            for i in range(flags // 4 + 1):
                out_data.seek(-k, 1)
                last = out_data.read(2)
                out_data.seek(0, 2)
                out_data.write(last)

        elif flags & 0x03 == 2:
            last = ring_buf[flags // 4]
            out_data.write(last)

        else:
            for i in range(flags // 4 + 1):
                last = ring_buf[ring_wpos] = bytes([byte ^ key for byte in f.read(2)]) if xorff else f.read(2)
                out_data.write(last)

                ring_wpos += 1
                ring_wpos %= 64

    out_data.truncate(exlen)  # Resize stream to decompress size
    out_data.seek(0)
    return out_data.read()

os.makedirs("Parsed", exist_ok=True)

file = open(sys.argv[1], "rb")
unc_data = mzx0_decompress(file, True)

try:
    unc_data = unc_data.decode("shift_jis_2004")
except:
    print("Couldn't decode file to UTF-8, writing in bytes format")
    new_file = open(f"Parsed/{Path(sys.argv[1]).stem}.txt", "wb")
else:
    unc_data = unc_data.replace(";", ";\n")
    new_file = open(f"Parsed/{Path(sys.argv[1]).stem}.txt", "w", encoding="UTF-8")
new_file.write(unc_data)
new_file.close()