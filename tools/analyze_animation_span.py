#!/usr/bin/env python3
"""Annotate MKII/MK3 fighter animation spans for hybrid-port development."""

from __future__ import annotations

import argparse
from pathlib import Path
import struct


ROM_BASE = 0xFF800000


def u16(data: bytes, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]


def u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def file_offset(address: int) -> int:
    return (address - ROM_BASE) // 8


def signed(value: int) -> int:
    return value - 0x10000 if value & 0x8000 else value


def looks_like_frame(data: bytes, address: int) -> bool:
    if not ROM_BASE <= address <= 0xFFFFFFFF or address & 0x0F:
        return False
    offset = file_offset(address)
    if offset < 0 or offset + 14 > len(data):
        return False
    coordinates = [signed(u16(data, offset + index * 2)) for index in range(4)]
    source = u32(data, offset + 8)
    command = u16(data, offset + 12)
    return (
        all(-0x400 <= value <= 0x400 for value in coordinates)
        and source < 0x10000000
        and bool(command & 0x0080)
        and 3 <= ((command >> 12) & 7) <= 7
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("program", type=Path)
    parser.add_argument("root", type=lambda value: int(value, 0))
    parser.add_argument("block_end", type=lambda value: int(value, 0))
    parser.add_argument("animation", type=lambda value: int(value, 0))
    args = parser.parse_args()

    data = args.program.read_bytes()
    root_offset = file_offset(args.root)
    pointers = [u32(data, root_offset + index * 4) for index in range(65)]
    valid = sorted({value for value in pointers if args.root <= value < args.block_end})
    start = pointers[args.animation]
    position = valid.index(start)
    end = valid[position + 1] if position + 1 < len(valid) else args.block_end
    print(f"animation={args.animation:#x} span={start:08x}-{end:08x} bytes={(end-start)//8}")

    for offset in range(file_offset(start), file_offset(end) - 3, 4):
        address = ROM_BASE + offset * 8
        value = u32(data, offset)
        if looks_like_frame(data, value):
            target = file_offset(value)
            coords = [signed(u16(data, target + index * 2)) for index in range(4)]
            source = u32(data, target + 8)
            command = u16(data, target + 12)
            label = f"FRAME xywh={coords} src={source:08x} cmd={command:04x}"
        elif start <= value < end and not value & 0x0F:
            label = "LOCAL"
        elif ROM_BASE <= value <= 0xFFFFFFFF and not value & 0x0F:
            label = "POINTER"
        elif value <= 0x100:
            label = "TOKEN"
        else:
            label = "DATA"
        print(f"{address:08x}: {value:08x} {label}")


if __name__ == "__main__":
    main()
