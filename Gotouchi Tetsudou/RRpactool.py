#!/usr/bin/env python3

"""
Author unknown.
Modifications made by MasaGratoR:
- autodetect endianness
- properly detect entry sizes instead of guessing
"""

import argparse
import base64
import json
import struct
from pathlib import Path


MAGIC = b"ARC\x00"


def read_u16(data, offset, endian):
    fmt = "<H" if endian == "little" else ">H"
    return struct.unpack_from(fmt, data, offset)[0]


def read_u32(data, offset, endian):
    fmt = "<I" if endian == "little" else ">I"
    return struct.unpack_from(fmt, data, offset)[0]


def write_u16(buf, offset, value, endian):
    fmt = "<H" if endian == "little" else ">H"
    struct.pack_into(fmt, buf, offset, value)


def write_u32(buf, offset, value, endian):
    fmt = "<I" if endian == "little" else ">I"
    struct.pack_into(fmt, buf, offset, value)


def align(value, boundary):
    return (value + (boundary - 1)) & ~(boundary - 1)


def decode_c_string(raw):
    end = raw.find(b"\x00")
    if end == -1:
        return 0
    return raw[:end].decode("ascii", errors="replace").strip()


def safe_name(name):
    name = name.replace("\\", "_").replace("/", "_").replace(":", "_")
    name = "".join(ch if 32 <= ord(ch) < 127 else "_" for ch in name)
    name = name.strip(" .")
    return name or "unnamed"


def is_probably_ascii_descriptor(raw4):
    if len(raw4) != 4:
        return False
    return raw4[:3].isalnum() and raw4[3] == 0


def parse_header(data, endian):
    if len(data) < 0x30:
        raise ValueError("File too small to be a valid PAC")

    if data[:4] != MAGIC:
        raise ValueError("Invalid PAC magic")

    endianness = read_u16(data, 0x4, "little")
    if (endianness == 0x100): endian = "little"
    if (endianness == 0x1): endian = "big"
    count_a = read_u16(data, 0x6, endian)
    count_b = read_u16(data, 0x8, endian)
    archive_name = decode_c_string(data[0x10:0x30])

    if count_a != count_b:
        print(f"Warning: file count mismatch at header (0x6={count_a}, 0x8={count_b}), using first value")

    return {
        "endian": endian,
        "file_count": count_a,
        "archive_name": archive_name
    }


def parse_offset_table(data, file_count, endian):
    offsets = []
    pos = 0x30

    for _ in range(file_count):
        if pos + 4 > len(data):
            raise ValueError("Unexpected EOF while reading offset table")
        offsets.append(read_u32(data, pos, endian))
        pos += 4

    # Skip any null padding bytes after the table, then align up to 0x10.
    while pos < len(data) and data[pos] == 0:
        pos += 1

    pos = align(pos, 0x10)

    return offsets, pos

def detectEntrySize(data, start):
    pos = start+0x14
    len_str = data[pos:].find(b"\x00")
    if len_str < 0xC:
        return 0x20
    return 0x40

def parse_name_entries(data, start, file_count, endian):
    entries = []
    pos = start

    for index in range(file_count):
        entry_size = detectEntrySize(data, pos)
        if pos + entry_size > len(data):
            raise ValueError(f"Unexpected EOF while reading filename entry {index}")

        raw = data[pos:pos + entry_size]

        descriptor = decode_c_string(raw[0:4])
        unk_04_05 = raw[4:6].hex()
        entry_index = read_u16(raw, 0x6, endian)
        unk_08_0F = raw[8:16].hex()
        filename = decode_c_string(raw[0x14:entry_size])

        entries.append({
            "entry_offset": pos,
            "entry_size": entry_size,
            "descriptor": descriptor,
            "entry_index": entry_index,
            "filename": filename,
            "unk_04_05": unk_04_05,
            "unk_08_0F": unk_08_0F,
        })

        pos += entry_size

    return entries, pos


def parse_file_regions(data, offsets, endian):
    regions = []

    for i, stored_offset in enumerate(offsets):
        if stored_offset + 6 > len(data):
            raise ValueError(f"Stored offset for entry {i} is outside file: 0x{stored_offset:X}")

        identifier = data[stored_offset:stored_offset + 4]
        spacing = read_u16(data, stored_offset + 4, endian)
        actual_start = stored_offset + spacing

        if actual_start > len(data):
            raise ValueError(
                f"Actual start outside file for entry {i}: "
                f"stored=0x{stored_offset:X}, spacing=0x{spacing:X}, actual=0x{actual_start:X}"
            )

        if i + 1 < len(offsets):
            file_end = offsets[i + 1]
        else:
            file_end = len(data)

        if file_end < actual_start:
            raise ValueError(
                f"Invalid bounds for entry {i}: actual_start=0x{actual_start:X}, file_end=0x{file_end:X}"
            )

        prefix_blob = data[stored_offset:actual_start]
        payload = data[actual_start:file_end]

        regions.append({
            "stored_offset": stored_offset,
            "identifier_hex": identifier.hex(),
            "spacing": spacing,
            "actual_start": actual_start,
            "file_end": file_end,
            "prefix_blob_b64": base64.b64encode(prefix_blob).decode("ascii"),
            "payload_size": len(payload),
        })

    return regions


def build_output_name(name_entry, index):
    original_name = name_entry["filename"] or f"entry_{index:04d}"
    cleaned = safe_name(original_name)

    if "." not in cleaned:
        desc = safe_name(name_entry["descriptor"]).strip(".")
        if desc and desc != "unnamed":
            cleaned += f".{desc.lower()}"
        else:
            cleaned += ".bin"

    return cleaned


def unpack_pac(input_path, mode, output_dir=None):
    endian = "little" if mode == "switch" else "big"
    input_path = Path(input_path)

    with input_path.open("rb") as f:
        data = f.read()

    header = parse_header(data, endian)
    endian = header["endian"]
    print(endian)
    offsets, names_start = parse_offset_table(data, header["file_count"], endian)
    name_entries, _ = parse_name_entries(data, names_start, header["file_count"], endian)
    file_regions = parse_file_regions(data, offsets, endian)

    if output_dir is None:
        output_dir = input_path.with_name(input_path.name + "_out")
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "source_pac": input_path.name,
        "mode": mode,
        "endian": endian,
        "archive_name": header["archive_name"],
        "file_count": header["file_count"],
        "name_table_start": names_start,
        "files": [],
    }

    used_names = set()

    for i, (name_entry, region) in enumerate(zip(name_entries, file_regions)):
        extracted_name = build_output_name(name_entry, i)

        if extracted_name in used_names:
            p = Path(extracted_name)
            extracted_name = f"{p.stem}_{i:04d}{p.suffix}"
        used_names.add(extracted_name)

        out_path = output_dir / extracted_name
        payload = data[region["actual_start"]:region["file_end"]]

        with out_path.open("wb") as f:
            f.write(payload)

        manifest["files"].append({
            "index": i,
            "descriptor": name_entry["descriptor"],
            "entry_index": name_entry["entry_index"],
            "original_filename": name_entry["filename"],
            "extracted_filename": extracted_name,
            "entry_size": name_entry["entry_size"],
            "entry_offset": name_entry["entry_offset"],
            "unk_04_05": name_entry["unk_04_05"],
            "unk_08_0F": name_entry["unk_08_0F"],
            "stored_offset": region["stored_offset"],
            "identifier_hex": region["identifier_hex"],
            "spacing": region["spacing"],
            "actual_start": region["actual_start"],
            "file_end": region["file_end"],
            "original_size": region["payload_size"],
            "prefix_blob_b64": region["prefix_blob_b64"],
        })

        print(
            f"[{i:04d}] {name_entry['filename']!r} -> {extracted_name!r} "
            f"(stored=0x{region['stored_offset']:X}, actual=0x{region['actual_start']:X}, size=0x{region['payload_size']:X})"
        )

    manifest_path = output_dir / "manifest.json"
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nUnpacked to: {output_dir}")
    print(f"Manifest written to: {manifest_path}")


def repack_pac(original_pac, input_dir, mode, output_pac=None):
    endian = "little" if mode == "switch" else "big"
    original_pac = Path(original_pac)
    input_dir = Path(input_dir)
    manifest_path = input_dir / "manifest.json"

    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing manifest: {manifest_path}")

    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    with original_pac.open("rb") as f:
        original_data = f.read()

    header = parse_header(original_data, endian)
    endian = header["endian"]
    offsets, names_start = parse_offset_table(original_data, header["file_count"], endian)

    if len(manifest["files"]) != header["file_count"]:
        raise ValueError(
            f"Manifest file count ({len(manifest['files'])}) does not match PAC file count ({header['file_count']})"
        )

    # Empty archive: nothing to repack, just emit the original bytes unchanged.
    if not offsets:
        if output_pac is None:
            output_pac = original_pac.with_name(original_pac.stem + "_repacked" + original_pac.suffix)
        else:
            output_pac = Path(output_pac)
        with output_pac.open("wb") as f:
            f.write(original_data)
        print(f"\nArchive is empty (file_count=0); written unchanged to: {output_pac}")
        return

    first_data_offset = min(offsets)
    rebuilt = bytearray(original_data[:first_data_offset])

    new_offsets = []
    file_blobs = []
    running_offset = first_data_offset

    for entry in manifest["files"]:
        replacement_path = input_dir / entry["extracted_filename"]
        if not replacement_path.exists():
            raise FileNotFoundError(f"Missing replacement file: {replacement_path}")

        with replacement_path.open("rb") as f:
            new_payload = f.read()

        prefix_blob = base64.b64decode(entry["prefix_blob_b64"])
        new_offsets.append(running_offset)
        blob = prefix_blob + new_payload
        file_blobs.append(blob)

        actual_start = running_offset + len(prefix_blob)
        print(
            f"[{entry['index']:04d}] {entry['original_filename']!r} "
            f"-> stored=0x{running_offset:X}, actual=0x{actual_start:X}, size=0x{len(new_payload):X}"
        )

        running_offset += len(blob)

    for i, new_offset in enumerate(new_offsets):
        write_u32(rebuilt, 0x30 + i * 4, new_offset, endian)

    for blob in file_blobs:
        rebuilt.extend(blob)

    write_u16(rebuilt, 0x6, len(new_offsets), endian)
    write_u16(rebuilt, 0x8, len(new_offsets), endian)

    if output_pac is None:
        output_pac = original_pac.with_name(original_pac.stem + "_repacked" + original_pac.suffix)
    else:
        output_pac = Path(output_pac)

    with output_pac.open("wb") as f:
        f.write(rebuilt)

    print(f"\nRepacked to: {output_pac}")


def main():
    parser = argparse.ArgumentParser(
        description="Unpack/repack PAC archives for Switch (little endian) and Wii U (big endian)."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    unpack_parser = subparsers.add_parser("unpack", help="Unpack a PAC archive")
    unpack_parser.add_argument("input_pac", help="Input PAC file")
    unpack_parser.add_argument("-o", "--output-dir", help="Output directory (default: <input>.pac_out)")

    repack_parser = subparsers.add_parser("repack", help="Repack a PAC archive")
    repack_parser.add_argument("original_pac", help="Original PAC file used as template")
    repack_parser.add_argument("input_dir", help="Directory produced by unpack")
    repack_parser.add_argument("-o", "--output-pac", help="Output PAC path")

    args = parser.parse_args()

    if args.command == "unpack":
        unpack_pac(args.input_pac, "switch", args.output_dir)
    elif args.command == "repack":
        repack_pac(args.original_pac, args.input_dir, "switch", args.output_pac)


if __name__ == "__main__":
    main()