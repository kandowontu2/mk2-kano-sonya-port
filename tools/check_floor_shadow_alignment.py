"""Compare imported fighters' airborne floor-shadow row with a stock control.

Inputs are deterministic ground-alignment captures at jump=88. The selected
fighter is airborne and entirely above the search band, so the first row
with nine near-black pixels is its projected shadow rather than its body.
"""

import argparse
from pathlib import Path

from PIL import Image


def shadow_top(image_path: Path, side: int) -> int:
    with Image.open(image_path) as source:
        image = source.convert("RGB")
        if image.size != (400, 300):
            raise ValueError(f"Unexpected capture dimensions: {image_path}: {image.size}")
        x_range = range(55, 150) if side == 1 else range(230, 340)
        for y in range(190, 240):
            dark = sum(max(image.getpixel((x, y))) < 45 for x in x_range)
            if dark > 8:
                return y
    raise ValueError(f"No airborne shadow in {image_path}")


def capture(root: Path, prefix: str, side: int, fighter: str) -> Path:
    number = "0019" if side == 1 else "0020"
    return root / f"{prefix}_side{side}_{fighter}_kitana" / "snap" / "mk2ks" / f"{number}.png"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prefix", help="Ground-alignment evidence case prefix")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    errors = []
    for side in (1, 2):
        stock = shadow_top(capture(args.root, args.prefix, side, "sub_zero"), side)
        for fighter in ("kano", "sonya"):
            observed = shadow_top(capture(args.root, args.prefix, side, fighter), side)
            delta = observed - stock
            passed = abs(delta) <= 8
            print(f"side={side} fighter={fighter} top={observed} stock={stock} delta={delta:+d} pass={str(passed).lower()}")
            if not passed:
                errors.append(f"side{side} {fighter}: {delta:+d} pixels")
    if errors:
        raise SystemExit("Airborne shadow misalignment: " + ", ".join(errors))


if __name__ == "__main__":
    main()
