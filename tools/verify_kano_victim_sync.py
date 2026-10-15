"""Verify the character-owned victim's paired windup, pull and collapse."""
import argparse
import json
import re
from pathlib import Path

from verify_skeleton_sync import ARMS, BONES, verify as verify_skeleton

# Native body groups: main-55 pose 2 and main-60 unique poses 0,1,3,5,6
# were audited from the original MKII ROM, imported Sonya timing in MK3
# diagnostic_v116_mk3_kano_vs_sonya_fatality. MK3 group addresses relocate
# FF9Bxxxx -> FE9Bxxxx. All twelve stock fighters retain native MKII bodies.
VICTIMS = {
    "kung_lao": (0, (0xFF91A150, 0xFF91E1A0, 0xFF91E220, 0xFF91E320, 0xFF91E420, 0xFF91E4A0)),
    "liu_kang": (1, (0xFF926010, 0xFF92B890, 0xFF92B930, 0xFF92BAB0, 0xFF92BBB0, 0xFF92BC70)),
    "cage": (2, (0xFF934B50, 0xFF93A410, 0xFF93A470, 0xFF93A550, 0xFF93A6B0, 0xFF93A750)),
    "baraka": (3, (0xFF941CF0, 0xFF947390, 0xFF947410, 0xFF947530, 0xFF947690, 0xFF947750)),
    "kitana": (4, (0xFF94DA00, 0xFF958330, 0xFF958390, 0xFF958470, 0xFF958570, 0xFF958610)),
    "mileena": (5, (0xFF94DA00, 0xFF958330, 0xFF958390, 0xFF958470, 0xFF958570, 0xFF958610)),
    "shang_tsung": (6, (0xFF960080, 0xFF9663D0, 0xFF966430, 0xFF966510, 0xFF966610, 0xFF966690)),
    "raiden": (7, (0xFF96E5D0, 0xFF975010, 0xFF975070, 0xFF975150, 0xFF975270, 0xFF975310)),
    "sub_zero": (8, (0xFF97FAD0, 0xFF989570, 0xFF9895D0, 0xFF9896B0, 0xFF9897B0, 0xFF989830)),
    "reptile": (9, (0xFF97FAD0, 0xFF989570, 0xFF9895D0, 0xFF9896B0, 0xFF9897B0, 0xFF989830)),
    "scorpion": (10, (0xFF97FAD0, 0xFF989570, 0xFF9895D0, 0xFF9896B0, 0xFF9897B0, 0xFF989830)),
    "jax": (11, (0xFF991950, 0xFF997980, 0xFF9979E0, 0xFF997AA0, 0xFF997B60, 0xFF997BE0)),
    "kano": (17, (0xFE9B29B0, 0xFE9B2A30, 0xFE9B2AB0, 0xFE9B2B30, 0xFE9B2B70, 0xFE9B2BB0)),
    "sonya": (18, (0xFE9B2D10, 0xFE9B2DB0, 0xFE9B2E50, 0xFE9B2EF0, 0xFE9B2F70, 0xFE9B2FB0)),
}
OFFSETS = (-59, 0, 8, 76, 84, 92)
PAIRED_ARMS = (0xFE9B2670, ARMS[0], ARMS[1], ARMS[-1], ARMS[-1], ARMS[-1])


def verify(log: str, side: int, victim: str) -> dict:
    skeleton = verify_skeleton(log, side)
    errors = list(skeleton["errors"])
    identity, groups = VICTIMS[victim]
    birth = skeleton["phases"][0]["frame"] if skeleton["phases"] else None
    records = []
    for match in re.finditer(r"MK2_FINISH_ACTORS frame=(\d+)[^\r\n]*?p1=(\S+) p2=(\S+)", log):
        own = match.group(side + 1).split(":")
        other = match.group(4 - side).split(":")
        records.append((int(match.group(1)), int(own[1], 16), int(own[2], 16),
                        int(other[1], 16), int(other[2], 16)))
    phases = []
    if birth is not None:
        windup = [row[0] for row in records if row[2] == PAIRED_ARMS[0] and row[0] <= birth]
        start = min(windup + [birth - 59])
        window = [row for row in records if start <= row[0] <= birth + 100]
        if any(row[1] != 17 or row[3] != identity for row in window):
            errors.append("Wrong attacker or victim identity during paired choreography")
        for index, (group, offset, arm) in enumerate(zip(groups, OFFSETS, PAIRED_ARMS)):
            matches = [row for row in window if row[4] == group]
            first = matches[0] if matches else None
            if first is None or first[0] != birth + offset or first[2] != arm:
                errors.append(f"Victim phase {index}: expected relative age {offset} and arm {arm:08X}, got {first}")
            phases.append({"group": f"{group:08X}", "expected_age": offset,
                           "age": first[0] - birth if first else None,
                           "arm": f"{first[2]:08X}" if first else None})
    else:
        errors.append("Missing skeleton birth")
    return {"passed": not errors, "side": side, "victim": victim,
            "skeleton_birth": birth, "phases": phases, "errors": errors}


def normalize_mk3_sonya_reference(log: str) -> str:
    """Normalize recorded original MK3 poses, not invented timing events."""
    poses = [None, None]
    lines = []
    for line in log.splitlines():
        actor = re.search(r"MK3_FATALITY_POSE fighter=kano frame=(\d+).*?side=(\d+) id=(\d+) pose=([0-9A-F]+)", line)
        if actor:
            frame, side, identity = map(int, actor.groups()[:3])
            assert identity == side - 1, "Unexpected donor actor identity"
            pose = int(actor.group(4), 16)
            poses[side - 1] = pose - 0x01000000 if 0xFF9B0000 <= pose < 0xFF9C0000 else pose
            if all(pose is not None for pose in poses):
                lines.append(f"MK2_FINISH_ACTORS frame={frame} p1=01000000:0011:{poses[0]:08X} p2=01000100:0012:{poses[1]:08X}")
        bone = re.search(r"MK3_FATALITY_OBJECT fighter=kano frame=(\d+).*?pose=([0-9A-F]+) kind=group", line)
        if bone:
            pose = int(bone.group(2), 16) - 0x01000000
            if pose in BONES:
                lines.append(f"MK2_FINISH_SKELETON frame={bone.group(1)} pose={pose:08X}")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    parser.add_argument("--side", type=int, choices=(1, 2), default=1)
    parser.add_argument("--victim", choices=VICTIMS, required=True)
    parser.add_argument("--original-mk3-reference", action="store_true")
    args = parser.parse_args()
    log = args.log.read_text(encoding="utf-8-sig")
    if args.original_mk3_reference:
        assert args.side == 1 and args.victim == "sonya", "This reference normalizer is specific to original Kano versus Sonya"
        log = normalize_mk3_sonya_reference(log)
    result = verify(log, args.side, args.victim)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
