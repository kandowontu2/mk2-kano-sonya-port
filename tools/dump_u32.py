#!/usr/bin/env python3
"""Dump little-endian 32-bit words from a binary image."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("offset", type=lambda value: int(value, 0))
    parser.add_argument("count", type=lambda value: int(value, 0))
    parser.add_argument("--base", type=lambda value: int(value, 0), default=0xFF800000)
    args = parser.parse_args()

    image = args.image.read_bytes()
    for index in range(args.count):
        offset = args.offset + index * 4
        value = int.from_bytes(image[offset : offset + 4], "little")
        print(
            f"[{index:02X}] file=0x{offset:06X} "
            f"tms=0x{args.base + offset * 8:08X} value=0x{value:08X}"
        )


if __name__ == "__main__":
    main()
