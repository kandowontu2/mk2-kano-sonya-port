"""Compare custom floor-shadow height with stock Sub-Zero across a jump arc.

Uses opt-in, named captures from mk2ks_ground_alignment_test.lua. The actor
is clear of the search band at the five measured airborne heights.
"""

import argparse
from pathlib import Path
import re

from PIL import Image


OFFSETS = (15, 20, 25, 30, 35)
FIGHTERS = ("sub_zero", "kano", "sonya")


def shadow_top(path: Path, side: int) -> int:
    with Image.open(path) as source:
        image = source.convert("RGB")
        if image.size != (400, 300):
            raise ValueError(f"Unexpected capture size: {path}: {image.size}")
        columns = range(55, 150) if side == 1 else range(230, 340)
        for y in range(190, 265):
            dark = sum(max(image.getpixel((x, y))) < 45 for x in columns)
            if dark > 8:
                return y
    raise ValueError(f"No shadow in {path}")


def case(root: Path, prefix: str, side: int, fighter: str) -> Path:
    return root / f"{prefix}_side{side}_{fighter}_kitana"


def arc_height(folder: Path, frame: int, side: int) -> int:
    text = (folder / "run.log").read_text(encoding="utf-8")
    pattern = rf"MK2KS_SHADOW_ARC frame={frame} side={side} id=\d+ jump=(\d+)"
    match = re.search(pattern, text)
    if not match:
        raise ValueError(f"Missing recorded jump height: {folder}, frame {frame}")
    return int(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prefix", help="Common evidence prefix for all six cases")
    parser.add_argument("--prefix-side1", help="Optional side-one evidence prefix")
    parser.add_argument("--prefix-side2", help="Optional side-two evidence prefix")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--max-error", type=int, default=3)
    args = parser.parse_args()
    errors = []
    squared = []
    for side in (1, 2):
        prefix = (args.prefix_side1 if side == 1 else args.prefix_side2) or args.prefix
        for offset in OFFSETS:
            frame = (1500 if side == 1 else 1700) + offset
            stock_folder = case(args.root, prefix, side, "sub_zero")
            stock_height = arc_height(stock_folder, frame, side)
            stock_top = shadow_top(stock_folder / "snap" /
                f"shadow_arc_side{side}_frame{frame}.png", side)
            for fighter in FIGHTERS[1:]:
                folder = case(args.root, prefix, side, fighter)
                jump = arc_height(folder, frame, side)
                if jump != stock_height:
                    raise ValueError(f"Unequal jump height: {folder}: {jump} vs {stock_height}")
                top = shadow_top(folder / "snap" /
                    f"shadow_arc_side{side}_frame{frame}.png", side)
                delta = top - stock_top
                squared.append(delta * delta)
                passed = abs(delta) <= args.max_error
                print(f"side={side} fighter={fighter} frame={frame} jump={jump} "
                    f"top={top} stock={stock_top} delta={delta:+d} pass={str(passed).lower()}")
                if not passed:
                    errors.append(f"side{side} {fighter} frame{frame}: {delta:+d}px")
    rms = (sum(squared) / len(squared)) ** 0.5
    print(f"ARC_RESULT cases={len(squared)} max_error={args.max_error} rms={rms:.2f} "
        f"pass={str(not errors).lower()}")
    if errors:
        raise SystemExit("Shadow arc mismatch: " + ", ".join(errors))


if __name__ == "__main__":
    main()
