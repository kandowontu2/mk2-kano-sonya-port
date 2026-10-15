#!/usr/bin/env python3
"""Patch only the live MKII main-59 pose lists in an isolated ROM trial.

A regenerated hybrid block shifts later custom allocations and would erase
move-specific patches. This uses the existing list slots and direct-frame
fields, and refuses any byte that differs from the untouched builder output.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import build_mk2ks_mk3 as build


VARIANTS = (
    ("kano", "kano", {}),
    ("sonya", "sonya", {}),
    ("kano_grab", "kano", {("main", 30): ("special", 2)}),
    ("sonya_bicycle", "sonya", {("main", 30): ("special", 1)}),
    ("kano_effect", "kano", {("special", 0): ("main", 36)}),
    ("sonya_effect", "sonya", {("special", 0): ("main", 36)}),
)


def donor_file(pointer: int) -> int:
    if (pointer < build.DONOR_TMS_BASE or pointer >= build.TMS_ROM_BASE or
            (pointer - build.DONOR_TMS_BASE) % 8):
        raise ValueError(f"Not a donor pointer: {pointer:08X}")
    return (pointer - build.DONOR_TMS_BASE) // 8


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--output", type=Path,
                        help="write a new isolated trial payload after validation")
    parser.add_argument("--group-poses", type=int, nargs=3, default=(0, 2, 5),
                        metavar=("FIRST", "MIDDLE", "LAST"),
                        help="MK3 main-63 pose indices for MKII's three lists")
    parser.add_argument("--direct-poses", type=int, nargs=4, default=(0, 2, 3, 5),
                        metavar=("FIRST", "SECOND", "THIRD", "LAST"),
                        help="MK3 main-63 direct-frame indices")
    args = parser.parse_args()
    if any(index < 0 or index > 5 for index in
           (*args.group_poses, *args.direct_poses)):
        raise SystemExit("Pose indices must be 0..5")
    if list(args.group_poses) != sorted(args.group_poses) or \
            list(args.direct_poses) != sorted(args.direct_poses):
        raise SystemExit("Pose indices must be in animation order")
    root = args.workspace
    mk2 = (root / "mk2/mk2-maincpu.bin").read_bytes()
    mk3 = (root / "mk3/mk3-maincpu.bin").read_bytes()
    released = root / "diagnostic_v251_full_body_ending_trial/roms/mk2ks/mk2ks.mdata"
    original = released.read_bytes()
    payload = bytearray(original)
    if len(payload) != build.DONOR_SIZE:
        raise SystemExit("Unexpected playable payload size")

    source_start = build.stock_file(build.LIU_MAIN)
    stock_span = build.sequence_spans(mk2, build.LIU_MAIN, build.LIU_BLOCK,
                                      (build.LIU_MAIN, build.LIU_SPECIAL))[59]
    stock_groups = build.group_references(mk2, *stock_span, *build.LIU_BLOCK)
    stock_group_values = build.ordered_unique([value for _, value, _ in stock_groups])
    stock_refs = build.frame_references(mk2, *stock_span)
    stock_ref_values = build.ordered_unique([value for _, value in stock_refs])
    if len(stock_group_values) != 3 or len(stock_ref_values) != 4:
        raise SystemExit("MKII main-59 shape changed")

    total_changed = 0
    for variant, fighter, prior_overrides in VARIANTS:
        block = build.KANO_BLOCK if fighter == "kano" else build.SONYA_BLOCK
        main_root = build.KANO_MAIN if fighter == "kano" else build.SONYA_MAIN
        special_root = build.KANO_SPECIAL if fighter == "kano" else build.SONYA_SPECIAL
        base = (build.HYBRID_FILE_BASES.get(variant) or
                build.HYBRID_VARIANT_BASES[variant])
        baseline = bytearray(b"\xff" * build.DONOR_SIZE)
        build.build_hybrid_block(baseline, mk2, mk3, fighter, block,
                                 main_root, special_root, destination=base,
                                 override_updates=prior_overrides)
        donor_span = build.sequence_spans(mk3, main_root, block,
                                          (main_root, special_root))[63]
        donor_groups = build.group_references(mk3, *donor_span, *block)
        donor_group_values = build.ordered_unique([value for _, value, _ in donor_groups])
        donor_frames_by_group = {value: frames for _, value, frames in donor_groups}
        donor_refs = build.frame_references(mk3, *donor_span)
        donor_ref_values = build.ordered_unique([value for _, value in donor_refs])
        if len(donor_group_values) != 6 or len(donor_ref_values) != 6:
            raise SystemExit(f"{variant}: MK3 main-63 shape changed")

        root_pointer = build.u32(payload, base + 59 * 4)
        expected_root = build.donor_address(base + build.stock_file(stock_span[0]) - source_start)
        if root_pointer != expected_root:
            raise SystemExit(f"{variant}: unexpected main-59 root {root_pointer:08X}")

        unique_group_slots: dict[int, int] = {}
        for location, stock_group, _ in stock_groups:
            slot = build.u32(payload, base + location - source_start)
            if slot != build.u32(baseline, base + location - source_start):
                raise SystemExit(f"{variant}: later patch owns main-59 group field")
            if stock_group in unique_group_slots and unique_group_slots[stock_group] != slot:
                raise SystemExit(f"{variant}: split main-59 group list")
            unique_group_slots[stock_group] = slot
        for stock_group, slot in unique_group_slots.items():
            references = sum(build.u32(payload, offset) == slot
                             for offset in range(base, base + 0x4000 - 3, 2))
            expected = sum(value == stock_group for _, value, _ in stock_groups)
            if references != expected:
                raise SystemExit(f"{variant}: main-59 group is shared outside its script")
            location = donor_file(slot)
            if payload[location:location + 12] != baseline[location:location + 12]:
                raise SystemExit(f"{variant}: later patch owns main-59 pose list")
            donor_group = donor_group_values[
                args.group_poses[stock_group_values.index(stock_group)]]
            frames = donor_frames_by_group[donor_group]
            if len(frames) != 1:
                raise SystemExit(f"{variant}: main-63 pose does not fit existing slot")
            build.put_u32(payload, location, build.relocate_pointer(frames[0]))
            build.put_u32(payload, location + 4, 0)

        for location, stock_frame in stock_refs:
            field = base + location - source_start
            if payload[field:field + 4] != baseline[field:field + 4]:
                raise SystemExit(f"{variant}: later patch owns main-59 direct frame")
            donor_frame = donor_ref_values[
                args.direct_poses[stock_ref_values.index(stock_frame)]]
            descriptor = build.stock_file(donor_frame)
            expected_source = (build.u32(mk3, descriptor + 8) + build.GFX_REBASE) & 0xFFFFFFFF
            if build.u32(payload, descriptor + 8) != expected_source:
                raise SystemExit(f"{variant}: main-63 frame descriptor is not relocated")
            build.put_u32(payload, field, build.relocate_pointer(donor_frame))

        changed = sum(payload[offset] != original[offset]
                      for offset in range(base, base + 0x4000))
        total_changed += changed
        print(f"{variant}: changed={changed} main59={root_pointer:08X} "
              f"group_frames={len(unique_group_slots)} direct_frames={len(stock_refs)} "
              f"group_poses={args.group_poses} direct_poses={args.direct_poses}")

    print(f"total_changed={total_changed} "
          f"released_sha256={hashlib.sha256(original).hexdigest()} "
          f"trial_sha256={hashlib.sha256(payload).hexdigest()}")
    if args.output:
        output = args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.exists():
            raise SystemExit(f"Refusing to overwrite: {output}")
        output.write_bytes(payload)
        print(f"trial_payload={output}")


if __name__ == "__main__":
    main()
