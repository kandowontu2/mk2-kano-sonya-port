#!/usr/bin/env python3
"""Compare MKII main-59 victim art bounds with the port's MK3 main-63 poses."""

from __future__ import annotations

import argparse
from pathlib import Path

import build_mk2ks_mk3 as build
import upgrade_ksui_previews as gfx


def groups(program: bytes, root: int, special: int,
           block: tuple[int, int], animation: int) -> list[tuple[int, list[int]]]:
    span = build.sequence_spans(program, root, block, (root, special))[animation]
    return list(dict((address, frames) for _, address, frames in
                     build.group_references(program, *span, *block)).items())


def bounds(program: bytes, frames: list[int]) -> tuple[int, int, int, int]:
    specs = [gfx.component_spec(program, address) for address in frames]
    return (min(-s[4] for s in specs), min(-s[5] for s in specs),
            max(-s[4] + s[2] for s in specs),
            max(-s[5] + s[3] for s in specs))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args()
    mk2 = (args.workspace / "mk2/mk2-maincpu.bin").read_bytes()
    mk3 = (args.workspace / "mk3/mk3-maincpu.bin").read_bytes()
    stock = groups(mk2, build.LIU_MAIN, build.LIU_SPECIAL, build.LIU_BLOCK, 59)
    if len(stock) != 3:
        raise SystemExit("Unexpected MKII main-59 pose count")
    for name, program, poses, indices in (
        ("liu-stock", mk2, stock, range(3)),
        ("kano-port", mk3, groups(mk3, build.KANO_MAIN, build.KANO_SPECIAL,
                                  build.KANO_BLOCK, 63), (0, 2, 5)),
        ("sonya-port", mk3, groups(mk3, build.SONYA_MAIN, build.SONYA_SPECIAL,
                                   build.SONYA_BLOCK, 63), (0, 2, 5)),
    ):
        print(name)
        for slot, index in enumerate(indices):
            address, frames = poses[index]
            print(f"  slot={slot} donor_pose={index} group={address:08X} "
                  f"frames={','.join(f'{f:08X}' for f in frames)} "
                  f"bounds={bounds(program, frames)}")


if __name__ == "__main__":
    main()
