"""Audit the six original-game real-input captures without touching emulation."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent.parent
STATE = re.compile(r"MK3_BICYCLE_STATE frame=(\d+) side=(\d+) id=(\d+) action=([0-9A-F]+) "
    r"x=(-?\d+) y=(-?\d+) vx=([0-9A-F]+) vy=([0-9A-F]+) gravity=([0-9A-F]+) pose=([0-9A-F]+) health=(\d+)")
results = []
for mode in ("near", "far", "block", "duck", "duck_block", "air"):
    path = ROOT / f"diagnostic_v46_mk3_bicycle_{mode}/run.log"
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    assert f"MK3_BICYCLE_REFERENCE_RESULT pass=true target={mode}" in text
    assert "MK3_BICYCLE_REFERENCE_END frame=4651" in text
    assert "LUA ERROR" not in text
    states = {}
    for match in STATE.finditer(text):
        frame, side, identity, action, x, y, vx, vy, gravity, pose, health = match.groups()
        states[int(frame), int(side)] = dict(identity=int(identity), action=int(action, 16),
            x=int(x), y=int(y), vx=int(vx, 16), vy=int(vy, 16), gravity=int(gravity, 16),
            pose=int(pose, 16), health=int(health))
    damage = states[3890, 2]["health"] - states[4200, 2]["health"]
    assert damage == (22 if mode in ("near", "air") else 3 if mode == "block" else 0)
    starts = []
    for pose in (0xFF83EA40, 0xFF83EA80, 0xFF83EAE0):
        starts.append(min(frame for (frame, side), state in states.items() if side == 1 and state["pose"] == pose))
    assert starts[1] - starts[0] == starts[2] - starts[1] == 2
    for previous, current in zip(starts, starts[1:]):
        assert states[current, 1]["x"] - states[previous, 1]["x"] == 5
        assert states[current, 1]["y"] - states[previous, 1]["y"] == 10
    rise, slow = [], []
    if mode in ("near", "air"):
        for frame in range(3915, 4100):
            own, victim = states[frame, 1], states[frame, 2]
            if victim["health"] != 144 or victim["action"] != 0:
                continue
            if own["vy"] == 0xFFFD0000:
                assert own["vx"] == 0x30000
                rise.append(frame)
            elif own["vy"] == 0x8000:
                assert own["vx"] == 0x10000
                slow.append(frame)
        assert 1 <= len(rise) <= 32 and len(slow) == 16
        for frame in rise[1:] + slow:
            own, victim = states[frame, 1], states[frame, 2]
            assert (victim["x"] - own["x"], victim["y"] - own["y"]) == (48, -32)
    results.append(dict(mode=mode, damage=damage, startup_frames=starts,
        rising_fields=len(rise), float_fields=len(slow), log_sha256=hashlib.sha256(raw).hexdigest().upper()))
print(json.dumps(dict(passed=True, game="original MK3 2.1", command="B,B,D+HK", cases=results), indent=2))
