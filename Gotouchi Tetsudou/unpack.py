import RRpactool
import argparse
import os
import zlib
import lzma

"""
Script made to recursively unpack/repack .pac files.
It also handles automatic decompression of compressed .pac files. No compression applied for repack.
"""


def decompress_cmp(filepath):
    """
    If the file starts with b"cmp\x00", decompress it in-place and return True.
    Returns False if the file is not compressed, raises on unsupported type.
    """
    with open(filepath, "rb") as f:
        magic = f.read(4)
        if magic != b"cmp\x00":
            return False

        com_type = f.read(4)
        com_size = int.from_bytes(f.read(4), "little")
        dec_size = int.from_bytes(f.read(4), "little")
        data = f.read(com_size)

    match com_type:
        case b"zlib":
            dec_data = zlib.decompress(data)
            assert len(dec_data) == dec_size

        case b"lzma":
            props = data[0]
            dict_size = int.from_bytes(data[1:5], "little")
            pb = props // 45
            lp = (props % 45) // 9
            lc = (props % 45) % 9
            stream = data[5:]

            filters = [{"id": lzma.FILTER_LZMA1, "lc": lc, "lp": lp, "pb": pb, "dict_size": dict_size}]
            dec = lzma.LZMADecompressor(format=lzma.FORMAT_RAW, filters=filters)
            dec_data = dec.decompress(stream, max_length=dec_size)
            assert len(dec_data) == dec_size

        case _:
            raise ValueError(f"Unsupported compression type: {com_type!r} in {filepath}")

    print(f"Decompressed: {filepath} ({com_size} -> {dec_size} bytes)")
    with open(filepath, "wb") as f:
        f.write(dec_data)

    return True


def is_arc(filepath):
    """Return True if the file starts with the ARC\x00 magic bytes."""
    try:
        with open(filepath, "rb") as f:
            return f.read(4) == b"ARC\x00"
    except (OSError, IOError):
        return False


def unpack_recursive(pac_file, platform, output_dir=None):
    """Unpack an ARC file, then recursively decompress/unpack any ARC files found inside."""
    if output_dir is None:
        output_dir = pac_file + "_out"

    # Decompress the input file itself if it's compressed
    decompress_cmp(pac_file)

    print(f"Unpacking: {pac_file} -> {output_dir}")
    RRpactool.unpack_pac(pac_file, platform, output_dir)

    for root, _, files in os.walk(output_dir):
        for fname in files:
            nested_file = os.path.join(root, fname)
            decompress_cmp(nested_file)
            if is_arc(nested_file):
                nested_out = nested_file + "_out"
                unpack_recursive(nested_file, platform, nested_out)


def repack_recursive(original_pac, input_dir, platform, output_pac=None):
    """Recursively repack nested ARC files first, then repack the outer one."""
    if output_pac is None:
        output_pac = original_pac

    for root, dirs, _ in os.walk(input_dir):
        for d in dirs:
            if d.endswith("_out"):
                nested_out_dir = os.path.join(root, d)
                nested_original = os.path.join(root, d[:-4])  # strip "_out"

                if os.path.isfile(nested_original):
                    repack_recursive(nested_original, nested_out_dir, platform, nested_original)
                else:
                    print(f"Warning: no original file found for {nested_out_dir}, skipping.")

    print(f"Repacking: {input_dir} -> {output_pac}")
    RRpactool.repack_pac(original_pac, input_dir, platform, output_pac)


parser = argparse.ArgumentParser(
    description="Unpack/repack PAC archives for Switch."
)
subparsers = parser.add_subparsers(dest="command", required=True)

unpack_parser = subparsers.add_parser("unpack", help="Unpack a PAC archive (recursively)")
unpack_parser.add_argument("input_pac", help="Input PAC file")
unpack_parser.add_argument("-o", "--output-dir", help="Output directory (default: <input>.pac_out)")

repack_parser = subparsers.add_parser("repack", help="Repack a PAC archive (recursively)")
repack_parser.add_argument("original_pac", help="Original PAC file used as template")
repack_parser.add_argument("input_dir", help="Directory produced by unpack")
repack_parser.add_argument("-o", "--output-pac", help="Output PAC path")

args = parser.parse_args()

if args.command == "unpack":
    unpack_recursive(args.input_pac, "switch", args.output_dir)
elif args.command == "repack":
    repack_recursive(args.original_pac, args.input_dir, "switch", args.output_pac)