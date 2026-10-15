#!/usr/bin/env python3
"""Render the MK3 donor hit/fall poses used by MKII main-59."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

import build_mk2ks_mk3 as build
import upgrade_ksui_previews as gfx


def render_pose(program: bytes, graphics: bytes, fighter: str,
                frames: list[int]) -> Image.Image:
    palette = gfx.donor_palette(program, fighter)
    result = Image.new("RGBA", (180, 170), (28, 28, 32, 255))
    for address in frames:
        source, command, width, height, x_offset, y_offset = gfx.component_spec(
            program, address)
        component = gfx.decode_component(graphics, palette, source, command,
                                         width, height)
        result.alpha_composite(component, (130 - x_offset, 10 - y_offset))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}")
    program = (args.workspace / "mk3/mk3-maincpu.bin").read_bytes()
    graphics = gfx.load_gfx(args.workspace / "mk3")
    sheet = Image.new("RGB", (6 * 190, 2 * 210), (18, 18, 20))
    draw = ImageDraw.Draw(sheet)
    for row, (fighter, root, special, block) in enumerate((
        ("kano", build.KANO_MAIN, build.KANO_SPECIAL, build.KANO_BLOCK),
        ("sonya", build.SONYA_MAIN, build.SONYA_SPECIAL, build.SONYA_BLOCK),
    )):
        span = build.sequence_spans(program, root, block, (root, special))[63]
        groups = list(dict((address, frames) for _, address, frames in
                           build.group_references(program, *span, *block)).items())
        if len(groups) != 6:
            raise SystemExit(f"{fighter}: expected 6 poses, got {len(groups)}")
        for col, (address, frames) in enumerate(groups):
            x, y = col * 190, row * 210
            draw.text((x + 5, y + 3), f"{fighter} pose {col}", fill="white")
            sheet.paste(render_pose(program, graphics, fighter, frames),
                        (x + 5, y + 24))
            draw.text((x + 5, y + 196), f"{address:08X}", fill="white")
            print(f"{fighter} pose={col} group={address:08X} "
                  f"frames={','.join(f'{frame:08X}' for frame in frames)}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(f"sheet={args.output}")


if __name__ == "__main__":
    main()
