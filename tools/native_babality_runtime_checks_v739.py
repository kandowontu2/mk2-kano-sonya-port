"""Versioned native Babality runtime checks for performer verification v739.

Forked from the frozen v728 victim checker; generalized only the winner ID and
handoff sample relative to actual native baby construction (longer commands
activate later). The old v728 standalone verifier below is historical only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import numpy as np
from PIL import Image

BASE = 0xFF800000
IDS = {"kano": 17, "sonya": 18, "liu_kang": 1}
TABLE = BASE + 0xF9600 * 8
FRAMES = {"kano": BASE + 0xF9680 * 8, "sonya": BASE + 0xF96A0 * 8}
PALETTES = {"kano": 0xF9700, "sonya": 0xF9750}


def check(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def records(text):
    rows = []
    for line in text.splitlines():
        match = re.match(r"MK2_NATIVE_BABY_(\w+) (.*)", line)
        if match:
            rows.append((match[1], dict(re.findall(r"(\w+)=([^\s]+)", match[2]))))
    return rows


def entries(rows, tag):
    return [r for t, r in rows if t == tag]


def integer(row, key, hex=False):
    return int(row[key], 16 if hex else 10)


def guest_check(old, new, original, reference):
    check(len(old) == len(new) == len(original) == 0x100000, "complete guest ROM required")
    operand = (0xFF87EB30 - BASE) // 8
    expected = bytearray(old)
    expected[operand:operand + 4] = struct.pack("<I", TABLE)
    expected[0xF9600:0xF9600 + 17 * 4] = original[(0xFF87F020 - BASE)//8:(0xFF87F020 - BASE)//8 + 17 * 4]
    for index, name in enumerate(("kano", "sonya")):
        rec = reference["records"][name]
        frame = bytearray.fromhex(rec["descriptor_hex"])
        struct.pack_into("<I", frame, 8, rec["source_bits"] + 0x10000000)
        struct.pack_into("<I", frame, 14, BASE + PALETTES[name] * 8)
        at = (FRAMES[name] - BASE) // 8
        expected[at:at + 18] = frame
        pal = bytes.fromhex(rec["palette_hex"])
        expected[PALETTES[name]:PALETTES[name] + len(pal)] = pal
        struct.pack_into("<I", expected, 0xF9600 + (17 + index) * 4, FRAMES[name])
    check(new == expected, "guest changed outside exact victim table/original baby records")
    return sum(a != b for a, b in zip(old, new))


def image_match(actual, reference):
    """Exact MAME xRGB555 expansion, including every nontransparent source pixel."""
    mask = reference[:, :, 3] != 0
    five = reference[:, :, :3] >> 3
    expected = (five << 3) | (five >> 2)
    positions = np.argwhere(mask)
    y0, x0 = positions[len(positions) // 2]
    hits = np.argwhere(np.all(actual == expected[y0, x0], axis=2))
    h, w = mask.shape
    matches = []
    for y, x in hits:
        x, y = int(x - x0), int(y - y0)
        if 0 <= x <= actual.shape[1] - w and 0 <= y <= actual.shape[0] - h:
            if np.array_equal(actual[y:y+h, x:x+w][mask], expected[mask]):
                matches.append((x, y))
    check(len(matches) == 1, "original baby pixels absent, changed or duplicated")
    return matches[0], int(mask.sum())


def runtime_check(rows, name, side, reference, table=TABLE, winner_id=4):
    check(len(entries(rows, "BOOT")) == 1 and len(entries(rows, "RESULT")) == 1,
          "watchdog/reboot or incomplete run")
    result = entries(rows, "RESULT")[0]
    check(integer(result, "wins") == 2 and integer(result, "damage") == 322,
          "two genuine earned rounds required")
    check(integer(result, "window") > 0 and integer(result, "action") > integer(result, "window"),
          "native finish input/action missing")
    for tag, row in rows:
        check(row["victim"] == name and integer(row, "winner_slot") == side and
              row["writes"] == "0" and row["assistance"] == "none", "mixed/assisted run")
    selected = entries(rows, "SELECT_ID")
    check(len(selected) == 2, "both physical slots must genuinely select")
    for row in selected:
        wanted = winner_id if integer(row, "slot") == side else IDS[name]
        check(integer(row, "actual") == wanted == integer(row, "target"), "proxy selection")
    damage = entries(rows, "DAMAGE")
    check(sum(integer(r, "before") - integer(r, "after") for r in damage) == 322 and
          sum(integer(r, "after") == 0 for r in damage) == 2 and
          all(r["pc"] == "FF836700" for r in damage), "not original combat knockouts")
    finish = entries(rows, "FINISH_WINDOW")
    check(len(finish) == 1 and finish[0]["native_kos"] == "2" and
          finish[0]["hp_counters"] == "0,0" and finish[0]["lp_counters"] == "0,0",
          "native no-punch babality eligibility missing")
    for address in (0xFF87E120, 0xFF87E230, 0xFF87E300, 0xFF87E520, 0xFF87E8D0, 0xFF87EB20):
        check(any(integer(r, "entry", True) == address for r in entries(rows, "ENTRY")),
              "native babality gate/choreography missing")
    built = entries(rows, "CONSTRUCT")
    check(len(built) == 1 and integer(built[0], "victim_id") == IDS[name] and
          built[0]["pc"] == "FF87EBD0" and integer(built[0], "table", True) == table,
          "true-ID native victim construction missing")
    pointer = FRAMES.get(name, 0xFFB1C960)
    check(integer(built[0], "frame_pointer", True) == pointer, "wrong baby descriptor")
    lookup = entries(rows, "LOOKUP")
    words = [(table + IDS[name] * 32, pointer & 0xFFFF),
             (table + IDS[name] * 32 + 16, pointer >> 16)]
    check(len(lookup) == 2 and [(integer(r, "entry", True), integer(r, "value", True)) for r in lookup] == words
          and all(r["pc"] == "FF83B850" and integer(r, "live_id") == IDS[name] for r in lookup),
          "wrong actual native victim table read")
    initial = [r for r in entries(rows, "FIELD") if integer(r, "age") == 0]
    check(len(initial) == 2, "both native fighter fields missing")
    for row in initial:
        check(row["owner"] == row["actor"] and integer(row, "id") ==
              (winner_id if integer(row, "slot") == side else IDS[name]), "wrong pre-finisher actor/ownership")
    own = next(r for r in initial if integer(r, "slot") == side)
    victim = next(r for r in initial if integer(r, "slot") != side)
    check(built[0]["original_victim"] == victim["actor"] and
          all(r["a8"] == victim["actor"] and r["a13"] == victim["main"] for r in lookup),
          "wrong physical victim ownership at native lookup")
    action_rows = [r for r in entries(rows, "ENTRY") if r["entry"] == "FF87E520"]
    check(len(action_rows) == 1 and action_rows[0]["a8"] == own["actor"],
          "wrong actual human finisher owner")
    constructed_age = integer(built[0], "frame") - integer(result, "window")
    handoff_sample = ((constructed_age + 7) // 8) * 8
    handed = [r for r in entries(rows, "FIELD") if integer(r, "age") == handoff_sample and integer(r, "slot") != side]
    check(len(handed) == 1 and handed[0]["owner"] == built[0]["actor"] and
          handed[0]["actor"] == victim["actor"] and integer(handed[0], "id") == IDS[name],
          "native baby handoff changed original victim identity")
    if name in FRAMES:
        rec = reference["records"][name]
        pal = bytes.fromhex(rec["palette_hex"])
        wanted_colors = list(struct.unpack_from(f'<{rec["palette_count"]}H', pal, 2))
        for age in (160, 200, 240):
            samples = [r for r in entries(rows, "BABY") if integer(r, "age") == age]
            check(len(samples) == 1, "native baby display sample missing")
            sample = samples[0]
            check(sample["actor"] == built[0]["actor"] and integer(sample, "graphic", True) == pointer and
                  integer(sample, "width") == rec["width"] and integer(sample, "height") == rec["height"] and
                  integer(sample, "y") + rec["height"] == 216,
                  "wrong baby frame/size/native floor")
            colors = [int(v, 16) for v in sample["colors"].split(',')]
            check(colors[:len(wanted_colors)] == wanted_colors, "actual native palette differs")
    retire = entries(rows, "RETIRE")
    for address, pc in ((0x01060220, "FF82BBF0"), (0x01060230, "FF82BBF0"),
                        (0x01060DF0, "FF82BC20"), (0x01060E00, "FF82BC20")):
        check(any(integer(r, "entry", True) == address and r["value"] == "0000" and
                  r["mask"] == "FFFF" and r["pc"] == pc for r in retire),
              "original actor retirement missing")
    check(len(entries(rows, "BABY_REUSED")) == 1, "baby object not reclaimed/reused")
    check(any(r["mode"] == "3" and integer(r, "frame") > integer(result, "action")
              for r in entries(rows, "STATE")), "native next-screen transition missing")


def verify(root):
    reference_path = root / "audit_v726_original_baby_reference/reference.json"
    reference = json.loads(reference_path.read_text())
    for path, value in reference["input_hashes"].items():
        check(sha(Path(path)) == value.upper(), "original oracle input changed")
    old = (root / "audit_v684_pit_guest_rom_integrity/diagnostic_v680_native_pit_initial_cache/guest_maincpu.bin").read_bytes()
    original = (root / "mk2/mk2-maincpu.bin").read_bytes()
    report = {"candidate": "diagnostic_v728_native_babality_victims", "cases": [],
              "fullPortAcceptance": False, "fullFinisherAcceptance": False,
              "scope": "Kitana babality victims Kano/Sonya both slots; stock rendering preserved"}
    for side in (2, 1):
        prefix = "audit_v732"
        slot = 3 - side
        for name in ("kano", "sonya", "liu_kang"):
            label = "stock_liu" if name == "liu_kang" else name
            case = root / f"{prefix}_native_baby_{label}_p{slot}"
            result = json.loads((case / "result.json").read_text(encoding="utf-8-sig"))
            check(result["exit_code"] == 0 and result["guest_writes"] == 0 and
                  result["assistance"] == "none" and result["winner_side"] == side, "bad runner result")
            for path, value in result["input_hashes"].items():
                check(sha(Path(path)) == value.upper(), f"executed input changed: {path}")
            script_path = next(Path(p) for p in result["input_hashes"] if p.endswith("babality_probe_v728_v3.lua"))
            script = script_path.read_text()
            check(not re.search(r":write_|\bdofile\s*\(|\bloadfile\s*\(", script), "guest-write/delegating probe")
            text = (case / "run.log").read_text(encoding="utf-8-sig")
            check(not re.search(r"(?:Lua error|fatal error|Error running)", text, re.I), "runtime error")
            rows = records(text)
            runtime_check(rows, name, side, reference)
            delta = guest_check(old, (case / "guest_maincpu.bin").read_bytes(), original, reference)
            pixels = 0
            if name in FRAMES:
                image = np.asarray(Image.open(reference_path.parent / f"{name}_baby.png").convert("RGBA"))
                rec = reference["records"][name]
                check(hashlib.sha256(image.tobytes()).hexdigest() == rec["rgba_sha256"], "oracle pixels changed")
                for age in (160, 200, 240):
                    actual = np.asarray(Image.open(case / "snap" / f"babality_{age}.png").convert("RGB"))
                    position, count = image_match(actual, image)
                    pixels += count
            else:
                before = root / f"audit_v732_old_native_baby_stock_liu_p{slot}"
                baseline = json.loads((before / "result.json").read_text(encoding="utf-8-sig"))
                check(baseline["exit_code"] == 0 and baseline["guest_writes"] == 0 and
                      baseline["assistance"] == "none", "bad stock baseline")
                for path, value in baseline["input_hashes"].items():
                    check(sha(Path(path)) == value.upper(), "stock baseline input changed")
                baseline_text = (before / "run.log").read_text(encoding="utf-8-sig")
                check(not re.search(r"(?:Lua error|fatal error|Error running)", baseline_text, re.I),
                      "stock baseline runtime error")
                runtime_check(records(baseline_text), name, side, reference, table=0xFF87F020)
                check((before / "guest_maincpu.bin").read_bytes() == old, "stock baseline ROM changed")
                for age in range(0, 721, 8):
                    a = np.asarray(Image.open(case / "snap" / f"babality_{age}.png").convert("RGB"))
                    b = np.asarray(Image.open(before / "snap" / f"babality_{age}.png").convert("RGB"))
                    check(np.array_equal(a, b), "stock babality rendered frame changed")
                    pixels += a.shape[0] * a.shape[1]
            report["cases"].append(dict(case=case.name, victim=name, slot=slot,
                                      guest_changed_bytes=delta, checked_display_pixels=pixels))
    return report


if __name__ == "__main__":
    raise SystemExit("Library only: run verify_native_babality_performers_v739.py")
