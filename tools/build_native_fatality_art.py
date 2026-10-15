"""Relocate observed MK3 fatality pose groups into the MKII donor window.

MK3 art is already appended to mk2ks's graphics ROM. The distinct Kano
fatality groups live outside his ordinary character block, so the existing
builder never relocated their component pointers or graphic bit offsets.
Sonya's observed attacker groups are already inside her imported block.
The observed Sonya victim burn sequence is also outside her character block.
Kano's pulled skeleton is a separate object, not one of the two fighter poses;
its six observed groups also need their own relocation.
The ordinary seven-pose MK3 dizzy reactions for Kano and Sonya are needed
when either is the victim of a character-specific finisher.
This stage imports art only; it does not install a finisher command or effect.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import build_mk2ks_mk3 as animation

KANO_GROUPS = (
    0xFF9B24F0, 0xFF9B2550, 0xFF9B25B0, 0xFF9B2610, 0xFF9B2670,
    0xFF9B26D0, 0xFF9B2730, 0xFF9B2790, 0xFF9B2810,
    0xFF9B29B0, 0xFF9B2A30, 0xFF9B2AB0, 0xFF9B2B30, 0xFF9B2B70,
    0xFF9B2BB0,
)
KANO_SKELETON_GROUPS = (
    0xFF9B22D0, 0xFF9B2310, 0xFF9B2350,
    0xFF9B23D0, 0xFF9B2430, 0xFF9B2490,
)
KANO_SONYA_VICTIM_GROUPS = (
    0xFF9B2D10, 0xFF9B2DB0, 0xFF9B2E50,
    0xFF9B2EF0, 0xFF9B2F70, 0xFF9B2FB0,
)
KANO_JAX_VICTIM_GROUPS = (
    0xFF9B3110, 0xFF9B3190, 0xFF9B3210,
    0xFF9B3290, 0xFF9B32F0, 0xFF9B3330,
)
KANO_DIZZY_GROUPS = (
    0xFF82A380, 0xFF82A3E0, 0xFF82A440, 0xFF82A4C0,
    0xFF82A540, 0xFF82A5A0, 0xFF82A600,
)
SONYA_DIZZY_GROUPS = (
    0xFF83B680, 0xFF83B6E0, 0xFF83B740, 0xFF83B7A0,
    0xFF83B800, 0xFF83B860, 0xFF83B8C0,
)
SONYA_GROUPS = (
    0xFF8402C0, 0xFF840340, 0xFF8403C0, 0xFF840440, 0xFF8404C0,
    0xFF840540, 0xFF8405C0, 0xFF840640, 0xFF8406C0, 0xFF840740,
    0xFF8407A0,
)
SONYA_BURN_GROUPS = (
    0xFF9B0AE0, 0xFF9B0B20, 0xFF9B0B60, 0xFF9B0BA0, 0xFF9B0BE0,
    0xFF9B0C20, 0xFF9B0C60, 0xFF9B0CA0, 0xFF9B0CE0, 0xFF9B0D40,
    0xFF9B0DA0, 0xFF9B0E00, 0xFF9B0E60, 0xFF9B0EC0, 0xFF9B0F20,
)


def build(payload: bytearray, original: bytes) -> dict:
    if len(payload) != 0x200000 or len(original) != 0x100000:
        raise ValueError("unexpected donor payload or MK3 program length")
    groups_changed = 0
    frames_changed = 0
    palette_pointers_changed = 0
    frames: set[int] = set()
    for group in (*KANO_GROUPS, *KANO_SKELETON_GROUPS,
                  *KANO_SONYA_VICTIM_GROUPS, *KANO_JAX_VICTIM_GROUPS,
                  *KANO_DIZZY_GROUPS, *SONYA_GROUPS,
                  *SONYA_DIZZY_GROUPS, *SONYA_BURN_GROUPS):
        components = animation.frame_group(original, group, group, group + 0x200)
        if not components:
            raise ValueError(f"not an original MK3 fatality group: {group:08X}")
        frames.update(components)
        offset = animation.stock_file(group)
        for index, frame in enumerate(components):
            at = offset + 4 * index
            value = animation.u32(payload, at)
            native = animation.relocate_pointer(frame)
            if value == frame:
                animation.put_u32(payload, at, native)
                groups_changed += 1
            elif value != native:
                raise ValueError(f"unexpected fatality group component at {at:X}")
        if animation.u32(payload, offset + 4 * len(components)) != 0:
            raise ValueError(f"missing fatality group terminator at {group:08X}")
    for frame in sorted(frames):
        offset = animation.stock_file(frame)
        if not animation.looks_like_frame(original, offset):
            raise ValueError(f"invalid original fatality frame {frame:08X}")
        source = animation.u32(original, offset + 8)
        current = animation.u32(payload, offset + 8)
        rebased = source + animation.GFX_REBASE
        if current == source:
            animation.put_u32(payload, offset + 8, rebased)
            frames_changed += 1
        elif current != rebased:
            raise ValueError(f"unexpected fatality frame graphics at {frame:08X}")
        tail = animation.u32(original, offset + 14)
        if animation.TMS_ROM_BASE <= tail <= 0xFFFFFFFF and not tail & 0x0F:
            current = animation.u32(payload, offset + 14)
            native = animation.relocate_pointer(tail)
            if current == tail:
                animation.put_u32(payload, offset + 14, native)
                palette_pointers_changed += 1
            elif current != native:
                raise ValueError(f"unexpected fatality frame palette at {frame:08X}")
    return dict(groups=len(KANO_GROUPS) + len(KANO_SKELETON_GROUPS) +
                len(KANO_SONYA_VICTIM_GROUPS) + len(KANO_JAX_VICTIM_GROUPS) +
                len(KANO_DIZZY_GROUPS) + len(SONYA_GROUPS) +
                len(SONYA_DIZZY_GROUPS) + len(SONYA_BURN_GROUPS),
                unique_frames=len(frames), groups_changed=groups_changed,
                frames_changed=frames_changed,
                palette_pointers_changed=palette_pointers_changed)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("original_mk3_program", type=Path)
    parser.add_argument("existing_mk2ks_payload", type=Path)
    parser.add_argument("output_payload", type=Path)
    args = parser.parse_args()
    if args.output_payload.exists():
        raise ValueError(f"refusing to overwrite {args.output_payload}")
    payload = bytearray(args.existing_mk2ks_payload.read_bytes())
    report = build(payload, args.original_mk3_program.read_bytes())
    args.output_payload.parent.mkdir(parents=True, exist_ok=True)
    args.output_payload.write_bytes(payload)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
