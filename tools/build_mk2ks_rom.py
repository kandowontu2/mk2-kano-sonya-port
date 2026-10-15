#!/usr/bin/env python3
"""Build the MKII Kano/Sonya development program ROM pair.

This keeps every stock MKII fighter ID intact, appends Kano as ID 0x11 and
Sonya as ID 0x12, and points those IDs at relocated MK1 animation tables.
The matching MK1 graphics ROMs are appended by the custom MAME driver.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import re
import struct
import zlib
from pathlib import Path


TMS_ROM_BASE = 0xFF800000
KSDATA_TMS_BASE = 0xFF000000
KSDATA_SIZE = 0x100000
KSDATA_DMA_TABLE = 0x80000
GFX_POINTER_MIN = 0x02000000
GFX_POINTER_MAX = 0x05000000
GFX_REBASE = 0x06000000

SONYA_SOURCE = (0x09E260, 0x0A0410)
KANO_SOURCE = (0x0A249A, 0x0A496C)
SONYA_DEST = 0x0F8000
KANO_DEST = 0x0FA202  # preserve the source table's 16-bit, non-32-bit alignment

MK1_PRELUDE = (0x08F000, SONYA_SOURCE[0])
MK1_GLOBAL = (0x0A9000, 0x0F8000)

MK2_MAIN_TABLE = 0x020C2A
MK2_SPECIAL_TABLE = 0x020C6E
TABLE_ENTRY_COUNT = 0x11
NEW_MAIN_TABLE = 0x0FC800
NEW_SPECIAL_TABLE = 0x0FC880

# MOVI immediates used by MKII's two animation lookup paths.
SPECIAL_TABLE_IMMEDIATE = 0x020C0C
MAIN_TABLE_IMMEDIATE = 0x020C14


def tms_address(file_offset: int) -> int:
    return TMS_ROM_BASE + file_offset * 8


def ksdata_address(file_offset: int) -> int:
    return KSDATA_TMS_BASE + file_offset * 8


def u32(data: bytes | bytearray, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def put_u32(data: bytearray, offset: int, value: int) -> None:
    struct.pack_into("<I", data, offset, value)


def relocate_program_pointer(value: int) -> tuple[int, str | None]:
    # TMS34010 program/data pointers are bit addresses aligned to a 16-bit
    # word.  This rejects signed coordinate pairs that happen to resemble an
    # 0xFFxxxxxx ROM address when interpreted as an overlapping 32-bit value.
    if value & 0x0F:
        return value, None
    for name, (start, end), dest in (
        ("sonya", SONYA_SOURCE, SONYA_DEST),
        ("kano", KANO_SOURCE, KANO_DEST),
    ):
        start_address = tms_address(start)
        end_address = tms_address(end)
        if start_address <= value < end_address:
            return tms_address(dest) + (value - start_address), name
    return value, None


def transform_words(
    data: bytearray,
    start: int,
    end: int,
    known_dma_sources: frozenset[int],
    frame_map: dict[int, int],
) -> dict[str, int]:
    counts = {"gfx": 0, "sonya": 0, "kano": 0, "frames": 0}
    replacements: list[tuple[int, int, str]] = []
    # TMS34010 data is 16-bit aligned, so 32-bit values may begin at offset 2.
    # Inspect an immutable snapshot: mutating while scanning would let one
    # replacement manufacture a false overlapping candidate two bytes later.
    snapshot = bytes(data)
    for offset in range(start, end - 3, 2):
        value = u32(snapshot, offset)
        if value in frame_map:
            replacements.append((offset, frame_map[value], "frames"))
            continue
        replacement, relocated = relocate_program_pointer(value)
        if relocated is not None:
            replacements.append((offset, replacement, relocated))

    # Exact runtime DMA addresses make false gfx matches extremely unlikely.
    # Still reject overlapping 32-bit candidates so a malformed source cannot
    # silently corrupt a neighboring field.
    last_end = -1
    last_candidate: tuple[int, int, str] | None = None
    for offset, replacement, kind in replacements:
        if offset < last_end:
            raise SystemExit(
                f"overlapping relocation candidates: {last_candidate!r} then "
                f"{(offset, replacement, kind)!r}"
            )
        put_u32(data, offset, replacement)
        counts[kind] += 1
        last_end = offset + 4
        last_candidate = (offset, replacement, kind)
    return counts


def merge_counts(total: dict[str, int], addition: dict[str, int]) -> None:
    for key, value in addition.items():
        total[key] += value


def copy_and_transform(
    output: bytearray,
    donor: bytes,
    source: tuple[int, int],
    destination: int,
    counts: dict[str, int],
    known_dma_sources: frozenset[int],
    frame_map: dict[int, int],
) -> None:
    start, end = source
    block = bytearray(donor[start:end])
    merge_counts(counts, transform_words(block, 0, len(block), known_dma_sources, frame_map))
    output[destination : destination + len(block)] = block


def parse_dma_metadata(paths: list[Path]) -> dict[int, int]:
    pattern = re.compile(r"MIDBLIT_META raw=([0-9A-Fa-f]{8}) command=([0-9A-Fa-f]{4})")
    observations: dict[int, Counter[int]] = {}
    for path in paths:
        for match in pattern.finditer(path.read_text(encoding="utf-8", errors="replace")):
            raw = int(match.group(1), 16)
            command = int(match.group(2), 16)
            observations.setdefault(raw, Counter())[command] += 1
    return {raw: counts.most_common(1)[0][0] for raw, counts in observations.items()}


def signed_u16(value: int) -> int:
    return value - 0x10000 if value & 0x8000 else value


def find_mk1_frame_descriptors(donor: bytes) -> dict[int, tuple[int, int, int | None]]:
    """Return old TMS pointer -> (file offset, raw gfx source, optional tail pointer).

    MK1 uses 12-byte frame records (four 16-bit geometry fields plus a
    32-bit graphics source).  The first record in many sequences is 16 bytes
    and adds a trailing program-data pointer.  MKII adds a 16-bit blitter
    command to both forms, producing 14- and 18-byte records respectively.
    """
    result: dict[int, tuple[int, int, int | None]] = {}
    for offset in range(0, len(donor) - 11, 2):
        coordinates = [signed_u16(struct.unpack_from("<H", donor, offset + i * 2)[0]) for i in range(4)]
        if any(value < -0x400 or value > 0x400 for value in coordinates):
            continue
        gfx_source = u32(donor, offset + 8)
        if not (GFX_POINTER_MIN <= gfx_source < GFX_POINTER_MAX):
            continue
        tail_pointer: int | None = None
        if offset + 16 <= len(donor):
            candidate = u32(donor, offset + 12)
            if TMS_ROM_BASE <= candidate <= 0xFFFFFFFF and not (candidate & 0x0F):
                tail_pointer = candidate
        result[tms_address(offset)] = (offset, gfx_source, tail_pointer)
    return result


def referenced_frame_pointers(
    donor: bytes,
    descriptors: dict[int, tuple[int, int, int | None]],
) -> set[int]:
    pointers: set[int] = set()
    for start, end in (SONYA_SOURCE, KANO_SOURCE):
        for offset in range(start, end - 3, 2):
            value = u32(donor, offset)
            if value in descriptors:
                pointers.add(value)
    return pointers


def build_converted_frames(
    donor: bytes,
    dma_commands: dict[int, int],
) -> tuple[bytearray, dict[int, int], dict[str, int]]:
    candidates = find_mk1_frame_descriptors(donor)
    required = referenced_frame_pointers(donor, candidates)
    descriptors = {pointer: candidates[pointer] for pointer in required}
    ksdata = bytearray(b"\xFF" * KSDATA_SIZE)
    frame_map: dict[int, int] = {}
    command_sources = {"captured": 0, "defaulted": 0}
    cursor = 0
    long_records = 0
    short_records = 0
    for old_pointer, (source_offset, gfx_source, tail_pointer) in sorted(descriptors.items()):
        record_size = 18 if tail_pointer is not None else 14
        if cursor + record_size > KSDATA_DMA_TABLE:
            raise SystemExit("converted MK1 frame records exceed the ksdata region")
        command = dma_commands.get(gfx_source)
        if command is None:
            command = 0xE048
            command_sources["defaulted"] += 1
        else:
            command_sources["captured"] += 1
        new_pointer = ksdata_address(cursor)
        frame_map[old_pointer] = new_pointer
        ksdata[cursor : cursor + 8] = donor[source_offset : source_offset + 8]
        put_u32(ksdata, cursor + 8, gfx_source + GFX_REBASE)
        struct.pack_into("<H", ksdata, cursor + 12, command)
        if tail_pointer is not None:
            relocated_tail, _ = relocate_program_pointer(tail_pointer)
            put_u32(ksdata, cursor + 14, relocated_tail)
            long_records += 1
        else:
            short_records += 1
        cursor += record_size

    # The custom video-device shim uses this exact-source table to turn the
    # MKII engine's one-scanline fallback for MK1 commands back into the
    # original full-frame DMA.  Non-base scanline addresses are suppressed.
    dma_entries: dict[int, tuple[int, int, int]] = {}
    for _, (source_offset, gfx_source, _) in descriptors.items():
        command = dma_commands.get(gfx_source, 0xE048)
        width = struct.unpack_from("<H", donor, source_offset)[0]
        height = struct.unpack_from("<H", donor, source_offset + 2)[0]
        dma_entries.setdefault(gfx_source + GFX_REBASE, (command, width, height))
    table = KSDATA_DMA_TABLE
    ksdata[table : table + 4] = b"MK1D"
    put_u32(ksdata, table + 4, len(dma_entries))
    table += 8
    for raw_source, (command, width, height) in sorted(dma_entries.items()):
        if table + 12 > len(ksdata):
            raise SystemExit("MK1 DMA metadata exceeds the ksdata region")
        put_u32(ksdata, table, raw_source)
        struct.pack_into("<HHH", ksdata, table + 4, command, width, height)
        struct.pack_into("<H", ksdata, table + 10, 0)
        table += 12
    return ksdata, frame_map, {
        "candidate_records": len(candidates),
        "records": len(descriptors),
        "short_records": short_records,
        "long_records": long_records,
        "bytes_used": cursor,
        "dma_entries": len(dma_entries),
        "dma_table_bytes": table - KSDATA_DMA_TABLE,
        **command_sources,
    }


def digest(path: Path) -> dict[str, str | int]:
    data = path.read_bytes()
    return {
        "size": len(data),
        "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}",
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mk2_program", type=Path)
    parser.add_argument("mk1_program", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument(
        "--dma-log",
        action="append",
        default=[],
        type=Path,
        help="MK1 midblit PNG directory; may be supplied more than once",
    )
    parser.add_argument(
        "--dma-meta",
        action="append",
        default=[],
        type=Path,
        help="instrumented MK1 error.log with MIDBLIT_META lines",
    )
    args = parser.parse_args()

    mk2 = bytearray(args.mk2_program.read_bytes())
    mk1 = args.mk1_program.read_bytes()
    if len(mk2) != 0x100000 or len(mk1) != 0x100000:
        raise SystemExit("Both combined program images must be exactly 1 MiB")

    known_dma_sources: set[int] = set()
    for directory in args.dma_log:
        for path in directory.glob("0x*.png"):
            try:
                source = int(path.stem, 16)
            except ValueError:
                continue
            if GFX_POINTER_MIN <= source < GFX_POINTER_MAX:
                known_dma_sources.add(source)
    if not known_dma_sources:
        raise SystemExit("At least one --dma-log directory with MK1 PNGDMA output is required")
    frozen_dma_sources = frozenset(known_dma_sources)
    dma_commands = parse_dma_metadata(args.dma_meta)
    ksdata, frame_map, frame_report = build_converted_frames(mk1, dma_commands)

    # Refuse to overwrite unexpected stock MKII content in the chosen caves.
    cave_ranges = (MK1_PRELUDE, MK1_GLOBAL, (SONYA_DEST, NEW_SPECIAL_TABLE + 0x4C))
    for start, end in cave_ranges:
        occupied = sum(byte != 0xFF for byte in mk2[start:end])
        if occupied:
            raise SystemExit(
                f"MKII cave 0x{start:06x}-0x{end:06x} contains {occupied} non-FF bytes"
            )

    counts = {"gfx": 0, "sonya": 0, "kano": 0, "frames": 0}

    # Copy supporting MK1 code/data into caves at the same TMS addresses.  This
    # preserves all pointers except the two character blocks that collide with
    # live MKII data and therefore must be relocated.
    for start, end in (MK1_PRELUDE, MK1_GLOBAL):
        block = bytearray(mk1[start:end])
        # Supporting code/data stays at its original address.  Do not rewrite
        # every frame-like pointer in this broad slice: only the two relocated
        # character animation blocks are authoritative consumers of the
        # converted MKII-format records.
        merge_counts(counts, transform_words(block, 0, len(block), frozen_dma_sources, {}))
        mk2[start:end] = block

    copy_and_transform(mk2, mk1, SONYA_SOURCE, SONYA_DEST, counts, frozen_dma_sources, frame_map)
    copy_and_transform(mk2, mk1, KANO_SOURCE, KANO_DEST, counts, frozen_dma_sources, frame_map)

    stock_main = [u32(mk2, MK2_MAIN_TABLE + index * 4) for index in range(TABLE_ENTRY_COUNT)]
    stock_special = [u32(mk2, MK2_SPECIAL_TABLE + index * 4) for index in range(TABLE_ENTRY_COUNT)]

    # IDs 0x11/0x12 are new; none of MKII's stock or hidden IDs are replaced.
    main_table = stock_main + [tms_address(KANO_DEST), tms_address(SONYA_DEST)]
    # Until MK1 special-move handlers are adapted, use stable MKII dispatch
    # handlers with compatible body types: Jax for Kano, Kitana for Sonya.
    special_table = stock_special + [stock_special[0x0B], stock_special[0x04]]

    for index, value in enumerate(main_table):
        put_u32(mk2, NEW_MAIN_TABLE + index * 4, value)
    for index, value in enumerate(special_table):
        put_u32(mk2, NEW_SPECIAL_TABLE + index * 4, value)

    put_u32(mk2, MAIN_TABLE_IMMEDIATE, tms_address(NEW_MAIN_TABLE))
    put_u32(mk2, SPECIAL_TABLE_IMMEDIATE, tms_address(NEW_SPECIAL_TABLE))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    combined = args.output_dir / "mk2ks-maincpu.bin"
    uj12 = args.output_dir / "mk2ks.uj12"
    ug12 = args.output_dir / "mk2ks.ug12"
    kdata = args.output_dir / "mk2ks.kdata"
    combined.write_bytes(mk2)
    uj12.write_bytes(mk2[0::2])
    ug12.write_bytes(mk2[1::2])
    kdata.write_bytes(ksdata)

    report = {
        "fighter_ids": {"kano": "0x11", "sonya": "0x12"},
        "animation_tables": {
            "main": f"0x{tms_address(NEW_MAIN_TABLE):08x}",
            "special": f"0x{tms_address(NEW_SPECIAL_TABLE):08x}",
            "kano": f"0x{tms_address(KANO_DEST):08x}",
            "sonya": f"0x{tms_address(SONYA_DEST):08x}",
        },
        "relocations": counts,
        "known_dma_sources": len(frozen_dma_sources),
        "dma_command_sources": len(dma_commands),
        "converted_frames": frame_report,
        "files": {
            combined.name: digest(combined),
            uj12.name: digest(uj12),
            ug12.name: digest(ug12),
            kdata.name: digest(kdata),
        },
    }
    report_path = args.output_dir / "mk2ks-build-report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
