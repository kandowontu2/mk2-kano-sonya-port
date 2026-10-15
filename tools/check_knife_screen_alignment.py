"""Check the rendered MKII Kano knife flight against its body-height hit path.

Run on the native-command suite's 400x254 snapshots. The cyan donor knife has
an isolated screen region in the two-player fight; this catches the old
X-only descriptor translation that drew it alongside the HUD while collision
and damage tests passed.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


CASES = {
    "kano": (range(23, 26), range(200, 275)),  # P1 knife, Sonya victim
    "sonya": (range(72, 75), range(90, 170)),  # P2 Kano knife, Sonya victim
}


def cyan_knife_bounds(path: Path, columns: range) -> tuple[int, int, int] | None:
    image = Image.open(path).convert("RGB")
    if image.size != (400, 254):
        raise ValueError(f"Expected a 400x254 native snapshot: {path}")
    rows = []
    for y in range(25, 190):
        for x in columns:
            red, green, blue = image.getpixel((x, y))
            if blue > 160 and green > 120 and red < 170 and blue * 10 > red * 13:
                rows.append(y)
    return (len(rows), min(rows), max(rows)) if rows else None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fighter", choices=CASES)
    parser.add_argument("snapshots", type=Path, help="Directory containing mk2ks/NNNN.png")
    args = parser.parse_args()

    frames, columns = CASES[args.fighter]
    passed = True
    for frame in frames:
        path = args.snapshots / "mk2ks" / f"{frame:04d}.png"
        bounds = cyan_knife_bounds(path, columns)
        okay = bounds is not None and bounds[0] >= 90 and 85 <= bounds[1] and bounds[2] <= 165
        print(f"knife_visual fighter={args.fighter} frame={frame} bounds={bounds} pass={okay}")
        passed &= okay
    if not passed:
        raise SystemExit("Knife artwork is missing or outside the chest-height flight band")


if __name__ == "__main__":
    main()
