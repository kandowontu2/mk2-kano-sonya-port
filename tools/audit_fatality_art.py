"""Audit original MK3 fatality poses against the current MKII donor payload.

The trace logs provide observed actor pose addresses. This script checks the
actual zero-terminated component groups and their gfx-source rebasing; it does
not mistake a screenshot for an import or claim the finisher is playable.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import build_mk2ks_mk3 as animation


def pose_addresses(log: str, fighter: str) -> list[int]:
    pattern = re.compile(rf"MK3_FATALITY_POSE fighter={fighter}\b.*?pose=([0-9A-F]{{8}})")
    observed = {int(match, 16) for match in pattern.findall(log)}
    # Only the distinctive original finisher groups are in scope. Ordinary
    # stance, hit, and victory groups were audited by the base character port.
    lo, hi = ((0xFF9B2400, 0xFF9B2C00) if fighter == "kano"
              else (0xFF840000, 0xFF840800))
    return sorted(pose for pose in observed if lo <= pose < hi)


def audit(program: bytes, payload: bytes, addresses: list[int]) -> dict:
    groups = []
    unique_frames: set[int] = set()
    for address in addresses:
        frames = animation.frame_group(program, address, address, address + 0x200)
        if not frames:
            raise ValueError(f"observed pose {address:08X} is not a valid MK3 group")
        unique_frames.update(frames)
        offset = animation.stock_file(address)
        actual = [animation.u32(payload, offset + index * 4)
                  for index in range(len(frames) + 1)]
        expected = [animation.relocate_pointer(frame) for frame in frames] + [0]
        groups.append(dict(address=f"{address:08X}",
                           native=f"{animation.relocate_pointer(address):08X}",
                           components=len(frames), relocated=actual == expected))
    descriptors = []
    for frame in sorted(unique_frames):
        offset = animation.stock_file(frame)
        source = animation.u32(program, offset + 8)
        actual = animation.u32(payload, offset + 8)
        descriptors.append(dict(address=f"{frame:08X}",
                                gfx_rebased=actual == source + animation.GFX_REBASE))
    return dict(group_count=len(groups), component_frame_count=len(unique_frames),
                groups_ready=sum(group["relocated"] for group in groups),
                descriptors_ready=sum(item["gfx_rebased"] for item in descriptors),
                groups=groups, missing_descriptors=[item["address"] for item in descriptors
                                             if not item["gfx_rebased"]])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("program", type=Path)
    parser.add_argument("payload", type=Path)
    parser.add_argument("kano_trace", type=Path)
    parser.add_argument("sonya_trace", type=Path)
    parser.add_argument("sonya_effect_trace", type=Path, nargs="?")
    parser.add_argument("--kano-effect-trace", type=Path)
    args = parser.parse_args()
    program, payload = args.program.read_bytes(), args.payload.read_bytes()
    if len(program) != 0x100000 or len(payload) != 0x200000:
        raise ValueError("unexpected original MK3 program or mk2ks payload size")
    report = {}
    for fighter, path in (("kano", args.kano_trace), ("sonya", args.sonya_trace)):
        addresses = pose_addresses(path.read_text(encoding="utf-8"), fighter)
        if not addresses:
            raise ValueError(f"no {fighter} finisher poses in {path}")
        report[fighter] = audit(program, payload, addresses)
    if args.sonya_effect_trace:
        log = args.sonya_effect_trace.read_text(encoding="utf-8")
        observed = {int(value, 16) for value in re.findall(
            r"MK3_FATALITY_OBJECT fighter=sonya\b[^\n]*?pose=([0-9A-F]{8}) kind=group", log)}
        groups = sorted(address for address in observed
                        if 0xFF9B0A00 <= address < 0xFF9B1000)
        if not groups:
            raise ValueError("no Sonya victim burn groups in effect trace")
        report["sonya_burn"] = audit(program, payload, groups)
    if args.kano_effect_trace:
        log = args.kano_effect_trace.read_text(encoding="utf-8")
        observed = {int(value, 16) for value in re.findall(
            r"MK3_FATALITY_OBJECT fighter=kano\b[^\n]*?pose=([0-9A-F]{8}) kind=group", log)}
        groups = sorted(address for address in observed
                        if 0xFF9B22D0 <= address <= 0xFF9B2490)
        if not groups:
            raise ValueError("no Kano detached skeleton groups in effect trace")
        report["kano_skeleton"] = audit(program, payload, groups)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
