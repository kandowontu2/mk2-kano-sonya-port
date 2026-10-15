#!/usr/bin/env python3
"""Upgrade the MK2 port's selector ROM with stable native-style previews."""

from __future__ import annotations

import argparse
import struct
from pathlib import Path

from PIL import Image, ImageOps

from build_mk2ks_mk3 import (
    KANO_BLOCK,
    KANO_MAIN,
    KANO_SPECIAL,
    SONYA_BLOCK,
    SONYA_MAIN,
    SONYA_SPECIAL,
    group_references,
    sequence_spans,
    signed,
    stock_file,
)


COLORS = 64
PREVIEW_WIDTH = 80
PREVIEW_HEIGHT = 155
PREVIEW_FRAMES = 8
TILE_WIDTH = 63
TILE_HEIGHT = 78


GFX_BANKS = (
    (0x0000000, (133, 132, 131, 130)),
    (0x0400000, (129, 128, 127, 126)),
    (0x0800000, (125, 124, 123, 122)),
    (0x0C00000, (121, 120, 119, 118)),
    (0x1000000, (117, 116, 115, 114)),
)


STANDING_COMPONENTS = {
    "kano": (
        (0x00000120, 0xE182, 33, 128, 31, -11),
        (0x00003F6A, 0xE582, 38, 127, -2, -11),
    ),
    "sonya": (
        (0x005199B0, 0xE582, 26, 127, 22, -13),
        (0x0051C214, 0xE582, 38, 125, -4, -13),
    ),
}


PALETTE_DESCRIPTORS = {"kano": 0x092BBC, "sonya": 0x092CF2}


def u16(data: bytes | bytearray, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]


def xrgb555(value: int) -> tuple[int, int, int]:
    return (
        ((value >> 10) & 0x1F) * 255 // 31,
        ((value >> 5) & 0x1F) * 255 // 31,
        (value & 0x1F) * 255 // 31,
    )


def rgb_to_xrgb555(red: int, green: int, blue: int) -> int:
    return ((red >> 3) << 10) | ((green >> 3) << 5) | (blue >> 3)


def load_gfx(rom_dir: Path) -> bytes:
    region = bytearray(0x1200000)
    for base, chips in GFX_BANKS:
        for lane, chip in enumerate(chips):
            path = rom_dir / f"l1_mortal_kombat_3_u{chip}_game_rom.u{chip}"
            payload = path.read_bytes()
            region[base + lane : base + lane + len(payload) * 4 : 4] = payload
    return bytes(region)


def donor_palette(program: bytes, fighter: str) -> list[tuple[int, int, int, int]]:
    offset = PALETTE_DESCRIPTORS[fighter]
    count = min(struct.unpack_from("<I", program, offset)[0], 0xFF)
    colors = [(0, 0, 0, 0)]
    for index in range(count):
        colors.append((*xrgb555(u16(program, offset + 4 + index * 2)), 255))
    while len(colors) < 256:
        colors.append((0, 0, 0, 255))
    return colors


def extract_bits(data: bytes, bit_offset: int, mask: int) -> int:
    byte = bit_offset >> 3
    word = data[byte] | (data[byte + 1] << 8)
    return (word >> (bit_offset & 7)) & mask


def decode_component(
    gfx: bytes,
    palette: list[tuple[int, int, int, int]],
    source: int,
    command: int,
    width: int,
    height: int,
) -> Image.Image:
    bpp = (command >> 12) & 7
    mask = (1 << bpp) - 1
    preskip = (command >> 8) & 3
    postskip = (command >> 10) & 3
    cursor = source
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = result.load()

    for y in range(height):
        row = cursor
        skip = extract_bits(gfx, row, 0xFF)
        row += 8
        pre = (skip & 0x0F) << preskip
        post = ((skip >> 4) & 0x0F) << postskip
        limit = max(pre, width - post)
        for x in range(pre, limit):
            index = extract_bits(gfx, row, mask)
            row += bpp
            if index:
                pixels[x, y] = palette[index]
        cursor += 8 + max(0, width - pre - post) * bpp
    return result


def stance_groups(program: bytes, fighter: str) -> list[list[int]]:
    if fighter == "kano":
        main, special, block = KANO_MAIN, KANO_SPECIAL, KANO_BLOCK
    else:
        main, special, block = SONYA_MAIN, SONYA_SPECIAL, SONYA_BLOCK
    spans = sequence_spans(program, main, block, (main, special))
    groups = group_references(program, *spans[0], *block)
    frames = [components for _, _, components in groups[:PREVIEW_FRAMES]]
    if len(frames) != PREVIEW_FRAMES:
        raise SystemExit(f"{fighter} stance has {len(frames)} frames, expected {PREVIEW_FRAMES}")
    return frames


def component_spec(program: bytes, address: int) -> tuple[int, int, int, int, int, int]:
    offset = stock_file(address)
    return (
        struct.unpack_from("<I", program, offset + 8)[0],
        u16(program, offset + 12),
        u16(program, offset),
        u16(program, offset + 2),
        signed(u16(program, offset + 4)),
        signed(u16(program, offset + 6)),
    )


def standing_previews(gfx: bytes, program: bytes, fighter: str) -> list[Image.Image]:
    palette = donor_palette(program, fighter)
    all_specs = [[component_spec(program, address) for address in group]
                 for group in stance_groups(program, fighter)]
    left = min(-spec[4] for specs in all_specs for spec in specs)
    right = max(-spec[4] + spec[2] for specs in all_specs for spec in specs)
    top = min(-spec[5] for specs in all_specs for spec in specs)
    bottom = max(-spec[5] + spec[3] for specs in all_specs for spec in specs)
    scale = min(70 / (right - left), 146 / (bottom - top))
    previews = []

    for specs in all_specs:
        composite = Image.new("RGBA", (right - left, bottom - top), (0, 0, 0, 0))
        for source, command, width, height, x_offset, y_offset in specs:
            part = decode_component(gfx, palette, source, command, width, height)
            composite.alpha_composite(part, (-x_offset - left, -y_offset - top))
        size = (max(1, round(composite.width * scale)), max(1, round(composite.height * scale)))
        composite = composite.resize(size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (PREVIEW_WIDTH, PREVIEW_HEIGHT), (0, 0, 0, 0))
        canvas.alpha_composite(
            composite,
            ((PREVIEW_WIDTH - composite.width) // 2, PREVIEW_HEIGHT - composite.height - 3),
        )
        previews.append(canvas)
    return previews


def words_from_palette(palette: list[int], count: int = COLORS) -> bytes:
    words = bytearray()
    palette += [0] * (count * 3 - len(palette))
    for index in range(count):
        red, green, blue = palette[index * 3 : index * 3 + 3]
        words += struct.pack("<H", rgb_to_xrgb555(red, green, blue))
    return bytes(words)


def encode_opaque(image: Image.Image, colors: int = COLORS) -> tuple[bytes, bytes]:
    quantized = image.convert("RGB").quantize(
        colors=colors,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.FLOYDSTEINBERG,
    )
    return words_from_palette(quantized.getpalette()[: colors * 3]), quantized.tobytes()


def encode_transparent(image: Image.Image) -> tuple[bytes, bytes]:
    rgba = image.convert("RGBA")
    quantized = rgba.convert("RGB").quantize(
        colors=COLORS - 1,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.FLOYDSTEINBERG,
    )
    alpha = rgba.getchannel("A").tobytes()
    source = quantized.tobytes()
    pixels = bytes(0 if alpha[index] < 40 else source[index] + 1 for index in range(len(source)))
    palette = [0, 0, 0] + quantized.getpalette()[: (COLORS - 1) * 3]
    return words_from_palette(palette), pixels


def decode_old_portraits(payload: bytes) -> tuple[list[Image.Image], int, int, bytes]:
    if payload[:4] not in (b"KSU2", b"KSU3"):
        raise SystemExit("input is not an MK2KS selector ROM")
    width, height, colors = struct.unpack_from("<BBH", payload, 4)
    cursor = 8
    portraits = []
    for _ in range(2):
        palette = [xrgb555(u16(payload, cursor + index * 2)) for index in range(colors)]
        cursor += colors * 2
        indices = payload[cursor : cursor + width * height]
        cursor += width * height
        image = Image.new("RGB", (width, height))
        image.putdata([palette[index] for index in indices])
        portraits.append(image)
    name_width, name_height = struct.unpack_from("<BB", payload, cursor)
    names_end = cursor + 2 + name_width * name_height * 2
    return portraits, width, height, payload[cursor:names_end]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_ui", type=Path)
    parser.add_argument("output_ui", type=Path)
    parser.add_argument("--mk3-program", type=Path, required=True)
    parser.add_argument("--mk3-rom-dir", type=Path, required=True)
    parser.add_argument("--background-source", type=Path, required=True)
    parser.add_argument("--liu-source", type=Path, required=True)
    parser.add_argument("--reptile-source", type=Path, required=True)
    parser.add_argument("--preview", type=Path)
    args = parser.parse_args()

    portraits, portrait_width, portrait_height, names = decode_old_portraits(args.input_ui.read_bytes())
    program = args.mk3_program.read_bytes()
    gfx = load_gfx(args.mk3_rom_dir)
    previews = [standing_previews(gfx, program, fighter) for fighter in ("kano", "sonya")]

    background_source = Image.open(args.background_source).convert("RGB")
    background = ImageOps.mirror(background_source.crop((320, 98, 400, 253)))
    background = background.resize((PREVIEW_WIDTH, PREVIEW_HEIGHT), Image.Resampling.BICUBIC)
    clean_tiles = [
        Image.open(args.liu_source).convert("RGB").crop((79, 20, 142, 98)),
        Image.open(args.liu_source).convert("RGB").crop((140, 20, 203, 98)),
        Image.open(args.liu_source).convert("RGB").crop((199, 20, 262, 98)),
        Image.open(args.reptile_source).convert("RGB").crop((259, 20, 322, 98)),
    ]

    output = bytearray(b"KSU4")
    output += struct.pack("<BBH", portrait_width, portrait_height, COLORS)
    for portrait in portraits:
        palette, pixels = encode_opaque(portrait)
        output += palette + pixels
    output += names

    output += struct.pack("<BBHB", PREVIEW_WIDTH, PREVIEW_HEIGHT, COLORS, PREVIEW_FRAMES)
    for fighter_previews in previews:
        for preview in fighter_previews:
            palette, pixels = encode_transparent(preview)
            output += palette + pixels

    output += struct.pack("<BBH", PREVIEW_WIDTH, PREVIEW_HEIGHT, COLORS)
    background_palette, background_pixels = encode_opaque(background, COLORS - 3)
    output += background_palette + background_pixels

    output += struct.pack("<BBH", TILE_WIDTH, TILE_HEIGHT, COLORS)
    for tile in clean_tiles:
        palette, pixels = encode_opaque(tile)
        output += palette + pixels

    args.output_ui.parent.mkdir(parents=True, exist_ok=True)
    args.output_ui.write_bytes(output)

    if args.preview:
        sheet = Image.new("RGB", (PREVIEW_WIDTH * 2, PREVIEW_HEIGHT * PREVIEW_FRAMES), "black")
        for index, fighter_previews in enumerate(previews):
            for frame, preview in enumerate(fighter_previews):
                panel = background.copy()
                panel.paste(preview, (0, 0), preview)
                sheet.paste(panel, (index * PREVIEW_WIDTH, frame * PREVIEW_HEIGHT))
        args.preview.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(args.preview)


if __name__ == "__main__":
    main()
