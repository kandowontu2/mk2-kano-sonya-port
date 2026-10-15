#!/usr/bin/env python3
"""Find runs of little-endian TMS34010 program pointers in a ROM image."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--min-count", type=int, default=8)
    parser.add_argument("--base", type=lambda value: int(value, 0), default=0xFF800000)
    args = parser.parse_args()

    image = args.image.read_bytes()
    for alignment in range(4):
        offset = alignment
        while offset + 4 <= len(image):
            start = offset
            values: list[int] = []
            while offset + 4 <= len(image):
                value = int.from_bytes(image[offset : offset + 4], "little")
                if not (args.base <= value <= 0xFFFFFFFF and value % 0x10 == 0):
                    break
                values.append(value)
                offset += 4
            if len(values) >= args.min_count:
                location = args.base + start * 8
                preview = " ".join(f"{value:08X}" for value in values[:20])
                suffix = " ..." if len(values) > 20 else ""
                print(
                    f"file=0x{start:06X} tms=0x{location:08X} "
                    f"count={len(values)} {preview}{suffix}"
                )
            offset = max(offset + 4, start + 4)


if __name__ == "__main__":
    main()
