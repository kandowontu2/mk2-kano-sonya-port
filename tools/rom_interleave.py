#!/usr/bin/env python3
"""Interleave equal-sized ROM byte lanes in MAME load order."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("lanes", nargs="+", type=Path)
    args = parser.parse_args()

    lanes = [path.read_bytes() for path in args.lanes]
    if not lanes or len({len(lane) for lane in lanes}) != 1:
        raise ValueError("all input lanes must exist and have the same size")

    result = bytearray(len(lanes) * len(lanes[0]))
    for lane_number, lane in enumerate(lanes):
        result[lane_number :: len(lanes)] = lane
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(result)


if __name__ == "__main__":
    main()
