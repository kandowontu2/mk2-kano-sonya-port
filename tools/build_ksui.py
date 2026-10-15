#!/usr/bin/env python3
"""Build the indexed portrait/name ROM used by the MKII port selector."""

from __future__ import annotations

import argparse
import struct
from pathlib import Path

from PIL import Image


WIDTH = 54
HEIGHT = 72
COLORS = 128
NAME_WIDTH = 54
NAME_HEIGHT = 12


def encode_portrait(source: Image.Image, crop: tuple[int, int, int, int]) -> tuple[bytes, bytes, Image.Image]:
    portrait = source.crop(crop).resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).convert("RGB")
    indexed = portrait.quantize(colors=COLORS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    palette = indexed.getpalette()[: COLORS * 3]
    palette += [0] * (COLORS * 3 - len(palette))

    words = bytearray()
    for index in range(COLORS):
        red, green, blue = palette[index * 3 : index * 3 + 3]
        xrgb555 = ((red >> 3) << 10) | ((green >> 3) << 5) | (blue >> 3)
        words += struct.pack("<H", xrgb555)

    return bytes(words), indexed.tobytes(), portrait


def yellow_mask(source: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    """Extract the yellow face of a native MKII lettering glyph."""
    rgb = source.crop(box).convert("RGB")
    mask = Image.new("L", rgb.size, 0)
    source_pixels = rgb.load()
    mask_pixels = mask.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            red, green, blue = source_pixels[x, y]
            if red > 120 and green > 105 and blue < 150 and red + green > 300:
                mask_pixels[x, y] = 255
    return mask


def native_glyphs(
    liu_hud: Image.Image,
    scorpion_hud: Image.Image,
    mk2_css: Image.Image,
) -> dict[str, Image.Image]:
    """Build only the glyphs needed for KANO and SONYA from native MKII art."""
    glyphs = {
        "K": yellow_mask(liu_hud, (57, 31, 64, 40)),
        "A": yellow_mask(liu_hud, (66, 31, 74, 40)),
        "N": yellow_mask(liu_hud, (76, 31, 84, 40)),
        "S": yellow_mask(scorpion_hud, (29, 31, 36, 40)),
        "O": yellow_mask(scorpion_hud, (48, 31, 56, 40)),
    }
    # MKII has no stock HUD name containing Y.  Its large SELECT header uses
    # the same hand-drawn alphabet, so scale the Y from "YOUR" to HUD height.
    large_y = yellow_mask(mk2_css, (172, 4, 184, 19))
    glyphs["Y"] = large_y.resize((7, 9), Image.Resampling.LANCZOS)
    return glyphs


def encode_name(text: str, glyphs: dict[str, Image.Image]) -> bytes:
    """Assemble a HUD label from native MKII glyph masks."""
    spacing = 1
    width = sum(glyphs[letter].width for letter in text) + spacing * (len(text) - 1)
    canvas = Image.new("L", (NAME_WIDTH, NAME_HEIGHT), 0)
    x = (NAME_WIDTH - width) // 2
    y = (NAME_HEIGHT - 9) // 2
    for letter in text:
        glyph = glyphs[letter]
        canvas.paste(glyph, (x, y), glyph)
        x += glyph.width + spacing
    return canvas.tobytes()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="native MK3 character-select screenshot")
    parser.add_argument("output", type=Path, help="mk2ks.ui output path")
    parser.add_argument("--preview", type=Path)
    parser.add_argument("--mk2-liu-hud", type=Path, required=True)
    parser.add_argument("--mk2-scorpion-hud", type=Path, required=True)
    parser.add_argument("--mk2-css", type=Path, required=True)
    args = parser.parse_args()

    source = Image.open(args.source).convert("RGB")
    # MK3's top row is Shang Tsung, Sindel, Jax, Kano, Liu Kang.  Kano is
    # therefore the fourth tile, not the upper-left tile.  Exclude the normal
    # tile frame and retain only his portrait interior.
    kano_palette, kano_pixels, kano_rgb = encode_portrait(source, (230, 38, 277, 97))
    sonya_palette, sonya_pixels, sonya_rgb = encode_portrait(source, (69, 104, 116, 162))
    glyphs = native_glyphs(
        Image.open(args.mk2_liu_hud),
        Image.open(args.mk2_scorpion_hud),
        Image.open(args.mk2_css),
    )

    payload = bytearray(b"KSU2")
    payload += struct.pack("<BBH", WIDTH, HEIGHT, COLORS)
    payload += kano_palette + kano_pixels
    payload += sonya_palette + sonya_pixels
    payload += struct.pack("<BB", NAME_WIDTH, NAME_HEIGHT)
    kano_name = encode_name("KANO", glyphs)
    sonya_name = encode_name("SONYA", glyphs)
    payload += kano_name
    payload += sonya_name
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)

    if args.preview:
        preview = Image.new("RGB", (WIDTH * 2 + 12, HEIGHT + NAME_HEIGHT + 4), "black")
        preview.paste(kano_rgb, (0, 0))
        preview.paste(sonya_rgb, (WIDTH + 12, 0))
        for offset, name in ((0, kano_name), (WIDTH + 12, sonya_name)):
            mask = Image.frombytes("L", (NAME_WIDTH, NAME_HEIGHT), name)
            yellow = Image.new("RGB", (NAME_WIDTH, NAME_HEIGHT), (255, 220, 0))
            preview.paste(yellow, (offset, HEIGHT + 4), mask)
        args.preview.parent.mkdir(parents=True, exist_ok=True)
        preview.save(args.preview)


if __name__ == "__main__":
    main()
