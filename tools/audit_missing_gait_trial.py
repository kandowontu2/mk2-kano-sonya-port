#!/usr/bin/env python3
"""Compare a semantic walk-frame mapping with the current hybrid blocks.

This is an isolated diagnostic; it never rewrites the installed ROM payload.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import build_mk2ks_mk3 as build


WALK_OVERRIDES = {
    "kano": {("special", 62): ("special", 61),
             ("special", 64): ("special", 63)},
    "sonya": {("special", 60): ("special", 59),
              ("special", 62): ("special", 61),
              ("special", 63): ("special", 61),
              ("special", 64): ("special", 61)},
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--output", type=Path,
                        help="Write an isolated trial .mdata after conflict checking")
    args = parser.parse_args()
    root = args.workspace
    mk2 = (root / "mk2/mk2-maincpu.bin").read_bytes()
    mk3 = (root / "mk3/mk3-maincpu.bin").read_bytes()
    payload = bytearray((root / "diagnostic_v138_jax_roms/roms/mk2ks/mk2ks.mdata").read_bytes())
    fighters = {
        "kano": (build.KANO_BLOCK, build.KANO_MAIN, build.KANO_SPECIAL),
        "sonya": (build.SONYA_BLOCK, build.SONYA_MAIN, build.SONYA_SPECIAL),
    }
    for fighter, (block, main_root, special_root) in fighters.items():
        old = bytearray(b"\xff" * build.DONOR_SIZE)
        new = bytearray(b"\xff" * build.DONOR_SIZE)
        base = build.HYBRID_FILE_BASES[fighter]
        build.build_hybrid_block(old, mk2, mk3, fighter, block, main_root, special_root)
        build.build_hybrid_block(new, mk2, mk3, fighter, block, main_root, special_root,
                                 override_updates=WALK_OVERRIDES[fighter])
        changed = [i for i in range(base, base + 0x4000) if old[i] != new[i]]
        conflicts = [i for i in changed if payload[i] != old[i]]
        first = ",".join(f"{i-base:04x}" for i in changed[:30])
        print(f"{fighter}: changed_bytes={len(changed)} payload_conflicts={len(conflicts)} "
              f"first_offsets={first}")
        if conflicts:
            print("  conflict_offsets=" + ",".join(f"{i-base:04x}" for i in conflicts[:30]))
            raise SystemExit("Trial would overwrite a later payload patch")
        if args.output:
            for offset in changed:
                payload[offset] = new[offset]
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.exists():
            raise SystemExit(f"Refusing to overwrite existing trial: {args.output}")
        args.output.write_bytes(payload)
        print(f"trial_payload={args.output}")


if __name__ == "__main__":
    main()
