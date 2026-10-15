"""Read the selected portrait's green-border pixel count over eight frames."""

import argparse
from pathlib import Path

from PIL import Image


BOUNDS = {"kano": (19, 81), "liu_kang": (79, 143), "sonya": (318, 383)}
FRAMES = (2, 3, 4, 5, 7, 8, 9, 10)


def count_border(image_path: Path, left: int, right: int) -> int:
    with Image.open(image_path) as source:
        image = source.convert("RGB")
        if image.size != (400, 300):
            raise ValueError(f"Unexpected image dimensions: {image_path}")
        result = 0
        for x in range(left, right):
            for y in range(22, 115):
                if left + 5 <= x < right - 5 and 27 <= y <= 109:
                    continue
                red, green, _ = image.getpixel((x, y))
                result += green > 140 and green > red * 1.5
        return result


def border_geometry(image_path: Path, left: int, right: int) -> tuple[int, int, int, int]:
    """Measure the four solid sides, excluding portrait-color interference."""
    with Image.open(image_path) as source:
        image = source.convert("RGB")

        def green(x: int, y: int) -> bool:
            red, channel, _ = image.getpixel((x, y))
            return channel > 140 and channel > red * 1.5

        columns = [x for x in range(left - 2, right + 3)
                   if sum(green(x, y) for y in range(29, 111)) >= 80]
        if len(columns) != 8:
            raise SystemExit(f"Expected eight solid vertical border columns: "
                             f"{image_path}: {columns}")
        left_width = sum(x < (columns[0] + columns[-1]) // 2 for x in columns)
        right_width = len(columns) - left_width
        first, last = columns[0], columns[-1]
        top_width = sum(sum(green(x, y) for x in range(first, last + 1)) >= 60
                        for y in range(24, 28))
        bottom_width = sum(sum(green(x, y) for x in range(first, last + 1)) >= 60
                           for y in range(111, 115))
        return left_width, right_width, top_width, bottom_width


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prefix")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    captures = {}
    geometries = {}
    for fighter, (left, right) in BOUNDS.items():
        directory = args.root / f"{args.prefix}_{fighter}" / "snap" / "mk2ks"
        counts = [count_border(directory / f"{number:04}.png", left, right)
                  for number in FRAMES]
        if any((count < 900 if index % 2 == 0 else count > 10)
               for index, count in enumerate(counts)):
            raise SystemExit(f"{fighter} cursor did not blink like stock: {counts}")
        with Image.open(directory / "0001.png") as before_source, \
                Image.open(directory / "0006.png") as after_source:
            before, after = before_source.convert("RGB"), after_source.convert("RGB")
            pose_delta = sum(before.getpixel((x, y)) != after.getpixel((x, y))
                             for x in range(0, 80) for y in range(130, 295))
        if pose_delta < 1000:
            raise SystemExit(f"{fighter} preview pose did not animate: {pose_delta}")
        print(f"{fighter}: border={counts} preview_changed_pixels={pose_delta}")
        captures[fighter] = directory
        geometries[fighter] = border_geometry(directory / "0002.png", left, right)
    if len(set(geometries.values())) != 1 or geometries["liu_kang"] != (4, 4, 4, 4):
        raise SystemExit(f"Custom cursor border differs from stock geometry: {geometries}")
    print(f"Kano/Sonya cursor sides match stock Liu Kang: {geometries}")
    with Image.open(captures["kano"] / "0002.png") as kano_source, \
            Image.open(captures["sonya"] / "0002.png") as sonya_source:
        kano, sonya = kano_source.convert("RGB"), sonya_source.convert("RGB")
        backdrop_diffs = sum(kano.getpixel((x, y)) != sonya.getpixel((x, y))
                             for x in range(0, 11) for y in range(190, 271))
        pane = ((x, y) for x in range(1, 78) for y in range(120, 298))
        unshifted = shifted_left = shifted_right = 0
        for x, y in pane:
            color = kano.getpixel((x, y))
            unshifted += color == sonya.getpixel((x, y))
            shifted_left += color == sonya.getpixel((x - 1, y))
            shifted_right += color == sonya.getpixel((x + 1, y))
    if backdrop_diffs:
        raise SystemExit(f"Custom CSS backdrop differs outside the animated pose: {backdrop_diffs}")
    if unshifted < 4000 or max(shifted_left, shifted_right) >= unshifted // 4:
        raise SystemExit(f"Custom CSS preview backdrop may shift: same={unshifted}, "
                         f"left={shifted_left}, right={shifted_right}")
    print(f"Kano/Sonya backdrop stays aligned: matching pixels "
          f"unshifted={unshifted}, left={shifted_left}, right={shifted_right}")


if __name__ == "__main__":
    main()
