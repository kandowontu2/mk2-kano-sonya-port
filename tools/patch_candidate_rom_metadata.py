#!/usr/bin/env python3
"""Make a diagnostic EXE accept one alternate mk2ks.mdata checksum.

Only the unique ASCII CRC32/SHA1 ROM metadata is changed. The stock playable
EXE is read-only; this is not a substitute for a source rebuild for release.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import zlib


def checksums(path: Path) -> tuple[bytes, bytes]:
    data = path.read_bytes()
    return (f"{zlib.crc32(data) & 0xFFFFFFFF:08x}".encode("ascii"),
            hashlib.sha1(data).hexdigest().encode("ascii"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_exe", type=Path)
    parser.add_argument("source_payload", type=Path)
    parser.add_argument("trial_payload", type=Path)
    parser.add_argument("output_exe", type=Path)
    args = parser.parse_args()
    if args.output_exe.exists():
        raise SystemExit(f"Refusing to overwrite {args.output_exe}")
    old_crc, old_sha1 = checksums(args.source_payload)
    new_crc, new_sha1 = checksums(args.trial_payload)
    if old_crc == new_crc or old_sha1 == new_sha1:
        raise SystemExit("Trial payload checksum did not change")
    source = args.source_exe.read_bytes()
    if source.count(old_crc) != 1 or source.count(old_sha1) != 1:
        raise SystemExit("Expected exactly one old CRC32 and SHA1 in EXE")
    output = source.replace(old_crc, new_crc).replace(old_sha1, new_sha1)
    assert len(output) == len(source)
    assert sum(a != b for a, b in zip(source, output)) <= 48
    args.output_exe.parent.mkdir(parents=True, exist_ok=True)
    args.output_exe.write_bytes(output)
    print(f"rom_crc32={new_crc.decode()} rom_sha1={new_sha1.decode()} "
          f"exe_sha256={hashlib.sha256(output).hexdigest()}")


if __name__ == "__main__":
    main()
