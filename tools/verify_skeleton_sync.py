"""Check native actor traces for Kano's six simultaneous pull phases."""
import argparse
import json
import re
from pathlib import Path


BONES = (0xFE9B22D0, 0xFE9B2310, 0xFE9B2350, 0xFE9B23D0, 0xFE9B2430, 0xFE9B2490)
# Original MK3 trace diagnostic_v116_mk3_kano_vs_sonya_fatality: relative
# skeleton ages 0,8,16,24,32,40. The second arm pose holds for two phases.
ARMS = (0xFE9B26D0, 0xFE9B2730, 0xFE9B2730, 0xFE9B2790, 0xFE9B2810, 0xFE9B2810)


def verify(log: str, side: int) -> dict:
    actor_pattern = re.compile(r"MK2_FINISH_ACTORS frame=(\d+).*?p1=(\S+) p2=(\S+)")
    bone_pattern = re.compile(r"MK2_FINISH_SKELETON frame=(\d+).*?pose=([0-9A-F]+)")
    current_arm = None
    current_id = None
    phases = []
    errors = []
    for line in log.splitlines():
        actor = actor_pattern.search(line)
        if actor:
            fields = actor.group(1 + side).split(":")
            current_arm = int(fields[2], 16)
            current_id = int(fields[1], 16)
        bone = bone_pattern.search(line)
        if bone:
            if current_id != 17:
                errors.append(f"Skeleton owner on side {side} is not Kano: {current_id}")
            phases.append((int(bone.group(1)), int(bone.group(2), 16), current_arm))
    if len(phases) != 6:
        errors.append(f"Expected six skeleton phases, found {len(phases)}")
    for index, (frame, skeleton, arm) in enumerate(phases[:6]):
        if skeleton != BONES[index] or arm != ARMS[index]:
            errors.append(f"Phase {index}: skeleton={skeleton:08X}, arm={arm}, expected arm={ARMS[index]:08X}")
        if index and frame - phases[index - 1][0] != 8:
            errors.append(f"Phase {index}: expected eight-field cadence, got {frame - phases[index - 1][0]}")
    return {"passed": not errors, "side": side,
            "phases": [{"frame": frame, "skeleton": f"{bone:08X}",
                        "arm": f"{arm:08X}" if arm is not None else None}
                       for frame, bone, arm in phases], "errors": errors}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    parser.add_argument("--side", type=int, choices=(1, 2), default=1)
    args = parser.parse_args()
    result = verify(args.log.read_text(encoding="utf-8-sig"), args.side)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
