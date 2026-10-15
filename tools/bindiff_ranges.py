#!/usr/bin/env python3
"""Summarize contiguous byte-difference ranges between two files."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("old", type=Path)
    parser.add_argument("new", type=Path)
    parser.add_argument("--merge-gap", type=int, default=0)
    parser.add_argument("--min-size", type=int, default=1)
    args = parser.parse_args()

    old = args.old.read_bytes()
    new = args.new.read_bytes()
    extent = max(len(old), len(new))
    changed = [
        index
        for index in range(extent)
        if (old[index] if index < len(old) else None)
        != (new[index] if index < len(new) else None)
    ]
    if not changed:
        return

    ranges: list[tuple[int, int]] = []
    start = end = changed[0]
    for index in changed[1:]:
        if index <= end + args.merge_gap + 1:
            end = index
        else:
            ranges.append((start, end + 1))
            start = end = index
    ranges.append((start, end + 1))

    total = len(changed)
    print(f"changed_bytes={total} ranges={len(ranges)}")
    for start, end in ranges:
        if end - start >= args.min_size:
            print(f"0x{start:06x}-0x{end - 1:06x} size=0x{end - start:x}")


if __name__ == "__main__":
    main()
