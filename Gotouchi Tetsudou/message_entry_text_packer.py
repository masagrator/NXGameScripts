import sys
import glob
import json
import os

dumped_dir = os.path.join(sys.argv[1], "dumped")
output_dir = sys.argv[1]

json_files = glob.glob("*.json", root_dir=dumped_dir)

for json_file in json_files:
    json_path = os.path.join(dumped_dir, json_file)
    file_name = json_file[:-5]  # strip .json

    with open(json_path, "r", encoding="UTF-8") as f:
        dump = json.load(f)

    texts = dump["TEXTS"]
    text_count = len(texts)

    # offset_addon = 4 means stored offsets == actual file positions
    offset_addon = 4

    # --- Layout calculation ---
    # 0x00: offset_addon (4)
    # 0x04: "ARC\x00" (4)
    # 0x08: endianness big-endian 1 (2)
    # 0x0A: text_count (2 LE)
    # 0x0C: text_count (2 LE)
    # 0x0E: zeros (6)
    # 0x14: file_name null-terminated, zero-padded to 0x34
    # 0x34: offsets array (text_count * 4 bytes)
    # <padding to align to 0x20 boundary relative to offset_addon>
    # metadata section (text_count * 0x20 bytes each)
    # text data entries

    after_offsets = 0x34 + text_count * 4
    remainder = (after_offsets - offset_addon) % 0x20
    meta_start = after_offsets if remainder == 0 else after_offsets + (0x20 - remainder)
    data_start = meta_start + text_count * 0x20

    # --- Pre-compute text entries and their offsets ---
    # Each entry layout:
    #   [0]  entry_size  (4) — total size of entry in bytes
    #   [4]  data_type=4 (4)
    #   [8]  zero        (4)
    #   [12] 0x10        (4)
    #   [16] chara_count (2)
    #   [18] text_len    (2)
    #   [20] zero        (4)
    #   [24] text bytes  (text_len)

    entry_data = []
    offsets = []
    current_offset = data_start

    for entry in texts:
        text = entry["TEXT"]
        encoded = text.encode("UTF-8")
        text_len = len(encoded)  # excludes null terminator
        chara_count = len(text)
        has_null = text_len > 0
        total_size = 0x18 + text_len + (1 if has_null else 0)  # null terminator only for non-empty strings
        entry_size = 0x10 + text_len + (1 if has_null else 0)  # from byte[8], excl. first 8 bytes
        aligned_size = (total_size + 3) & ~3  # pad to 4-byte boundary

        offsets.append(current_offset - offset_addon)
        entry_data.append((entry_size, aligned_size, total_size, chara_count, text_len, encoded, has_null))
        current_offset += aligned_size

    # --- Build binary buffer ---
    buf = bytearray()

    # Header
    buf += offset_addon.to_bytes(4, "little")           # 0x00
    buf += b"ARC\x00"                                   # 0x04
    buf += (1).to_bytes(2, "big")                       # 0x08 endianness
    buf += text_count.to_bytes(2, "little")             # 0x0A
    buf += text_count.to_bytes(2, "little")             # 0x0C
    buf += b"\x00" * (0x14 - len(buf))                  # 0x0E-0x13 padding

    # File name (null-terminated, zero-padded up to 0x34)
    name_bytes = file_name.encode("ascii") + b"\x00"
    buf += name_bytes
    buf += b"\x00" * (0x34 - len(buf))

    # Offsets array
    for off in offsets:
        buf += off.to_bytes(4, "little")

    # Padding to metadata start
    buf += b"\x00" * (meta_start - len(buf))

    # Metadata entries (0x20 bytes each)
    for entry in texts:
        buf += b"bin\x00"
        buf += entry["global_id"].to_bytes(2, "little")
        buf += entry["internal_id"].to_bytes(2, "little")
        buf += b"\x00" * 4
        buf += (0x10000).to_bytes(4, "little")
        buf += b"\x00" * 0x10

    # Text data entries
    for (entry_size, aligned_size, total_size, chara_count, text_len, encoded, has_null) in entry_data:
        buf += entry_size.to_bytes(4, "little")
        buf += (4).to_bytes(4, "little")
        buf += b"\x00" * 4
        buf += (0x10).to_bytes(4, "little")
        buf += chara_count.to_bytes(2, "little")
        buf += text_len.to_bytes(2, "little")
        buf += b"\x00" * 4
        buf += encoded
        if has_null:
            buf += b"\x00"  # null terminator (only for non-empty strings)
        buf += b"\x00" * (aligned_size - total_size)  # 4-byte alignment padding

    out_path = os.path.join(output_dir, "entry_%04d.pac" % dump["ENTRY"])
    with open(out_path, "wb") as f:
        f.write(buf)

    print(f"Written: {out_path}")