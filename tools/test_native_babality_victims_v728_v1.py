"""Mutation tests use copies only; frozen evidence and game files are untouched."""
from pathlib import Path
import copy
import json
import numpy as np
from PIL import Image
import verify_native_babality_victims_v728_v1 as v

ROOT = Path(__file__).resolve().parents[1]


def main():
    reference = json.loads((ROOT / "audit_v726_original_baby_reference/reference.json").read_text())
    case = ROOT / "audit_v732_native_baby_kano_p1"
    rows = v.records((case / "run.log").read_text(encoding="utf-8-sig"))
    v.runtime_check(rows, "kano", 2, reference)
    total = 1

    def reject(label, function):
        nonlocal total
        try:
            function()
        except ValueError:
            total += 1
        else:
            raise AssertionError("Accepted corrupt case: " + label)

    def alter(tag, key, value, predicate=lambda r: True):
        changed = copy.deepcopy(rows)
        row = next(r for t, r in changed if t == tag and predicate(r))
        row[key] = value
        return changed

    for label, tag, key, value, predicate in [
        ("unearned round", "RESULT", "wins", "1", lambda r: True),
        ("assistance", "RESULT", "writes", "1", lambda r: True),
        ("proxy selection", "SELECT_ID", "actual", "1", lambda r: r["slot"] == "1"),
        ("non-native damage", "DAMAGE", "pc", "FF80DE20", lambda r: True),
        ("punch eligibility", "FINISH_WINDOW", "hp_counters", "1,0", lambda r: True),
        ("wrong victim ID", "CONSTRUCT", "victim_id", "1", lambda r: True),
        ("wrong baby frame", "CONSTRUCT", "frame_pointer", "FFB1C960", lambda r: True),
        ("wrong lookup word", "LOOKUP", "value", "002C", lambda r: True),
        ("proxy table lookup", "LOOKUP", "live_id", "1", lambda r: True),
        ("wrong human owner", "FIELD", "owner", "01031D10", lambda r: r["age"] == "0" and r["slot"] == "2"),
        ("lost true victim ID", "FIELD", "id", "1", lambda r: r["age"] == "128" and r["slot"] == "1"),
        ("wrong baby floor", "BABY", "y", "174", lambda r: r["age"] == "160"),
        ("wrong original palette", "BABY", "colors", "0000," + ",".join(v.entries(rows, "BABY")[0]["colors"].split(",")[1:]), lambda r: r["age"] == "160"),
        ("non-native retirement", "RETIRE", "pc", "FF80DE20", lambda r: r["entry"] == "01060220"),
    ]:
        changed = alter(tag, key, value, predicate)
        reject(label, lambda changed=changed: v.runtime_check(changed, "kano", 2, reference))
    for label, tag, predicate in [
        ("missing gate", "ENTRY", lambda r: r["entry"] == "FF87E520"),
        ("missing retirement", "RETIRE", lambda r: r["entry"] == "01060230"),
        ("unreclaimed baby", "BABY_REUSED", lambda r: True),
    ]:
        changed = [(t, r) for t, r in rows if not (t == tag and predicate(r))]
        reject(label, lambda changed=changed: v.runtime_check(changed, "kano", 2, reference))
    reset = copy.deepcopy(rows) + [("BOOT", copy.deepcopy(v.entries(rows, "BOOT")[0]))]
    reject("watchdog reset", lambda: v.runtime_check(reset, "kano", 2, reference))

    old = (ROOT / "audit_v684_pit_guest_rom_integrity/diagnostic_v680_native_pit_initial_cache/guest_maincpu.bin").read_bytes()
    new = (case / "guest_maincpu.bin").read_bytes()
    original = (ROOT / "mk2/mk2-maincpu.bin").read_bytes()
    v.guest_check(old, new, original, reference)
    total += 1
    for label, at in [("unrelated gameplay byte", 0x12345), ("native babality instruction", 0xFC24),
                      ("baby pointer", 0xF9600 + 17 * 4), ("baby art descriptor", 0xF9680),
                      ("baby palette", 0xF9702), ("lost stock table word", 0xF9604)]:
        changed = bytearray(new)
        changed[at] ^= 1
        reject(label, lambda changed=changed: v.guest_check(old, changed, original, reference))

    image = np.asarray(Image.open(case / "snap/babality_160.png").convert("RGB"))
    needle = np.asarray(Image.open(ROOT / "audit_v726_original_baby_reference/kano_baby.png").convert("RGBA"))
    (x, y), pixels = v.image_match(image, needle)
    total += 1
    yy, xx = np.argwhere(needle[:, :, 3] != 0)[0]
    changed = image.copy()
    changed[y + yy, x + xx, 0] ^= 1
    reject("one rendered pixel changed", lambda: v.image_match(changed, needle))
    reject("wrong character art", lambda: v.image_match(image, np.asarray(Image.open(
        ROOT / "audit_v726_original_baby_reference/sonya_baby.png").convert("RGBA"))))
    print(json.dumps({"tests_passed": total, "mutations_are_in_memory_only": True,
                      "fullPortAcceptance": False}, indent=2))


if __name__ == "__main__":
    main()
