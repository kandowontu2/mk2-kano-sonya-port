#!/usr/bin/env python3
"""Apply a classic IPS patch to a binary file."""

from __future__ import annotations

import argparse
from pathlib import Path


def read_u24(data: bytes, offset: int) -> tuple[int, int]:
    return int.from_bytes(data[offset : offset + 3], "big"), offset + 3


def apply_ips(source: bytes, patch: bytes) -> bytearray:
    if not patch.startswith(b"PATCH"):
        raise ValueError("not an IPS patch")

    result = bytearray(source)
    cursor = 5
    while patch[cursor : cursor + 3] != b"EOF":
        target, cursor = read_u24(patch, cursor)
        size = int.from_bytes(patch[cursor : cursor + 2], "big")
        cursor += 2

        if size:
            payload = patch[cursor : cursor + size]
            cursor += size
        else:
            run_size = int.from_bytes(patch[cursor : cursor + 2], "big")
            cursor += 2
            payload = patch[cursor : cursor + 1] * run_size
            cursor += 1

        end = target + len(payload)
        if end > len(result):
            result.extend(b"\x00" * (end - len(result)))
        result[target:end] = payload

    cursor += 3
    if cursor + 3 <= len(patch):
        truncate_size, _ = read_u24(patch, cursor)
        del result[truncate_size:]
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("patch", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    output = apply_ips(args.source.read_bytes(), args.patch.read_bytes())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(output)


if __name__ == "__main__":
    main()
