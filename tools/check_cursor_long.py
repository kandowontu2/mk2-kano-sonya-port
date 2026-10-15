"""Check preview animation and stock-width cursor blinking over a long CSS hover."""

import argparse
from pathlib import Path
import re

from PIL import Image

from check_cursor_temporal import BOUNDS, border_geometry, count_border


AGES = tuple(65 + window * 80 + index * 4 for window in range(3) for index in range(8))


def captures(root: Path, prefix: str, fighter: str):
    case = root / f"{prefix}_{fighter}"
    log = (case / "run.log").read_text(encoding="utf-8")
    css_match = re.search(r"MK2KS_EXIT css=(\d+)", log)
    if not css_match:
        raise ValueError(f"Missing selector entry in {case}")
    css = int(css_match.group(1))
    matches = re.findall(
        r"MK2KS_EXIT snapshot=(\d+) label=cursor_trace_long frame=(\d+)", log
    )
    if tuple(int(frame) - css for _, frame in matches) != AGES:
        raise ValueError(f"Wrong long-hover sample ages in {case}: {matches}")
    directory = case / "snap" / "mk2ks"
    paths = [directory / f"{int(number):04d}.png" for number, _ in matches]
    if not all(path.is_file() for path in paths):
        raise ValueError(f"Missing long-hover capture in {case}")
    return paths


def preview_difference(left: Image.Image, right: Image.Image) -> int:
    return sum(left.getpixel((x, y)) != right.getpixel((x, y))
               for x in range(0, 80) for y in range(130, 295))


def backdrop_difference(left: Image.Image, right: Image.Image) -> int:
    return sum(left.getpixel((x, y)) != right.getpixel((x, y))
               for x in range(0, 11) for y in range(230, 271))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prefix")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    results = {}
    for fighter, bounds in BOUNDS.items():
        paths = captures(args.root, args.prefix, fighter)
        images = []
        for path in paths:
            with Image.open(path) as source:
                images.append(source.convert("RGB"))
        counts = [count_border(path, *bounds) for path in paths]
        blink = [count > 900 for count in counts]
        if any(count not in range(0, 11) and count < 900 for count in counts):
            raise SystemExit(f"Partial cursor border during {fighter} hover: {counts}")
        if any(blink[start:start + 8] != [True, False] * 4
               for start in (0, 8, 16)):
            raise SystemExit(f"Cursor did not keep blinking for {fighter}: {counts}")
        geometry = [border_geometry(paths[index], *bounds)
                    for index in (0, 8, 16)]
        if any(value != (4, 4, 4, 4) for value in geometry):
            raise SystemExit(f"Cursor width changed for {fighter}: {geometry}")
        pose_changes = [max(preview_difference(images[start], images[index])
                            for index in range(start + 1, start + 8))
                        for start in (0, 8, 16)]
        if min(pose_changes) < 500:
            raise SystemExit(f"Preview stopped animating for {fighter}: {pose_changes}")
        backdrop_changes = [backdrop_difference(images[0], image)
                            for image in images]
        if max(backdrop_changes):
            raise SystemExit(f"Selection backdrop shifted for {fighter}: "
                             f"max changed pixels={max(backdrop_changes)}")
        print(f"{fighter}: blink={blink} pose_changes={pose_changes} "
              f"backdrop_changed=0 geometry={geometry}")
        results[fighter] = blink
    if results["kano"] != results["liu_kang"] or results["sonya"] != results["liu_kang"]:
        raise SystemExit("Imported cursor cadence differs from stock Liu Kang")
    print("LONG_CURSOR_RESULT pass=true fighters=3 windows=3 frames=24")


if __name__ == "__main__":
    main()
