#!/usr/bin/env python3
"""Find little-endian 32-bit values in a TMS34010 program image."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("values", nargs="+")
    parser.add_argument("--base", type=lambda value: int(value, 0), default=0xFF800000)
    args = parser.parse_args()

    image = args.image.read_bytes()
    for text_value in args.values:
        value = int(text_value, 0)
        needle = value.to_bytes(4, "little")
        print(f"value=0x{value:08X}")
        cursor = 0
        while True:
            offset = image.find(needle, cursor)
            if offset < 0:
                break
            print(f"  file=0x{offset:06X} tms=0x{args.base + offset * 8:08X}")
            cursor = offset + 1


if __name__ == "__main__":
    main()
