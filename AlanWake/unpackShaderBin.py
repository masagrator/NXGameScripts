# Unpacker for the custom .shaderbin format.
#
# Layout:
#   0x00  magic "RFX "
#   0x04  version
#   0x08  tuple_count (number of hash+len+string tuples that follow the name)
#   0x0C  main_name length
#   0x10  main_name string
#   then (tuple_count - 1) include tuples: [hash(4)][len(4)][string(len)]
#   then 1 final tuple, the first technique's name: [hash(4)][technique_count(4)][namelen(4)][name(namelen)]
#   then, repeated: [CODE section][CONTROL section][optional trailing data]
#     - CODE section starts with magic 0x12345678 (graphics) or 0x12345679 (compute)
#     - CONTROL section starts with magic 0x98761234, its size is given by the
#       two u32 fields at CONTROL_offset+0x20 (unk_section_offset + unk_section_size)
#     - a new technique (e.g. the fragment shader following a vertex shader, or a
#       later technique) may be preceded by a name block right after the previous
#       CONTROL section: [8 zero bytes][namelen(4)][name(namelen)]; if that pattern
#       isn't found, the technique name carries over from the previous pair.
#
# Usage: python unpackShaderBin.py <input.shaderbin | input_folder> -o <output_folder>

import struct
import glob
import os
import sys
import argparse

CODE_MAGICS = (0x12345678, 0x12345679)
CONTROL_MAGIC = 0x98761234

STAGE_NAMES = {
    0: "VERTEX",
    1: "FRAGMENT",
    2: "GEOMETRY",
    3: "TESS_CONTROL",
    4: "TESS_EVALUATION",
    5: "COMPUTE",
}


def parse_shaderbin(data):
    if data[0:4] != b"RFX ":
        raise ValueError(f"not a shaderbin file (bad magic {data[0:4]!r})")

    tuple_count = struct.unpack_from("<I", data, 0x8)[0]
    name_len = struct.unpack_from("<I", data, 0xC)[0]
    main_name = data[0x10:0x10 + name_len].decode("ascii")
    pos = 0x10 + name_len

    # skip include tuples
    for _ in range(tuple_count - 1):
        pos += 4  # hash
        ln = struct.unpack_from("<I", data, pos)[0]
        pos += 4 + ln

    # final tuple: first technique's name -- only present if there are any
    # techniques at all; a technique_count of 0 means this shader compiled to
    # nothing (e.g. disabled for this platform/config) and the file ends here
    pos += 4  # hash
    technique_count = struct.unpack_from("<I", data, pos)[0]
    pos += 4
    if technique_count == 0:
        return main_name, []
    ln = struct.unpack_from("<I", data, pos)[0]
    pos += 4
    cur_name = data[pos:pos + ln].decode("ascii")
    pos += ln
    header_end = pos

    # scan for CODE/CONTROL magics
    hits = []
    for off in range(header_end, len(data) - 4):
        val = struct.unpack_from("<I", data, off)[0]
        if val in CODE_MAGICS or val == CONTROL_MAGIC:
            hits.append((off, val))

    pairs = []
    prev_end = header_end
    i = 0
    while i < len(hits):
        code_off, code_magic = hits[i]
        if code_magic not in CODE_MAGICS:
            raise ValueError(f"expected CODE magic at 0x{code_off:x}, got 0x{code_magic:x}")
        control_off, control_magic = hits[i + 1]
        if control_magic != CONTROL_MAGIC:
            raise ValueError(f"expected CONTROL magic at 0x{control_off:x}, got 0x{control_magic:x}")

        # detect an optional technique-name block right after the previous CONTROL section
        gap = data[prev_end:code_off]
        if len(gap) >= 12 and all(b == 0 for b in gap[0:8]):
            ln2 = struct.unpack_from("<I", gap, 8)[0]
            if 1 <= ln2 <= 64 and len(gap) >= 8 + 4 + ln2:
                name_bytes = gap[12:12 + ln2]
                if all(32 <= c < 127 for c in name_bytes):
                    cur_name = name_bytes.decode("ascii")

        unk_off = struct.unpack_from("<I", data, control_off + 0x20)[0]
        unk_sz = struct.unpack_from("<I", data, control_off + 0x24)[0]
        control_size = unk_off + unk_sz
        control_end = control_off + control_size

        stage_byte = data[control_off + 0x714]
        stage = STAGE_NAMES.get(stage_byte, f"UNK{stage_byte}")

        pairs.append({
            "name": cur_name,
            "stage": stage,
            "code_start": code_off,
            "code_end": control_off,
            "control_start": control_off,
            "control_end": control_end,
        })

        prev_end = control_end
        i += 2

    return main_name, pairs


def unpack_file(path, output_folder):
    data = open(path, "rb").read()
    main_name, pairs = parse_shaderbin(data)

    base = os.path.splitext(os.path.basename(path))[0]
    out_dir = os.path.join(output_folder, base)
    os.makedirs(out_dir, exist_ok=True)

    # disambiguate repeated name+stage combinations (e.g. multiple permutations
    # of the same technique/stage) by appending a running counter per key
    seen = {}
    for idx, p in enumerate(pairs):
        key = (p["name"], p["stage"])
        seen[key] = seen.get(key, 0) + 1
        suffix = "" if seen[key] == 1 else f"_{seen[key]}"
        out_name = f"{idx:02d}_{p['name']}_{p['stage']}{suffix}.bin"
        out_path = os.path.join(out_dir, out_name)
        control_bytes = data[p["control_start"]:p["control_end"]]
        code_bytes = data[p["code_start"]:p["code_end"]]
        with open(out_path, "wb") as f:
            f.write(control_bytes)
            f.write(code_bytes)

    print(f"{path}: main_name={main_name}, {len(pairs)} sections -> {out_dir}")


def main():
    parser = argparse.ArgumentParser(description="Unpack .shaderbin files into individual CODE+CONTROL shader blobs.")
    parser.add_argument("input", help="A .shaderbin file, or a folder containing .shaderbin files")
    parser.add_argument("-o", "--output-folder", dest="output_folder", required=True,
                         help="Folder to write unpacked shader blobs into (created if missing)")
    args = parser.parse_args()

    if os.path.isdir(args.input):
        files = glob.glob(os.path.join(args.input, "*.shaderbin"))
    else:
        files = [args.input]

    if not files:
        print("No .shaderbin files found.")
        sys.exit(1)

    os.makedirs(args.output_folder, exist_ok=True)

    for path in files:
        unpack_file(path, args.output_folder)


if __name__ == "__main__":
    main()