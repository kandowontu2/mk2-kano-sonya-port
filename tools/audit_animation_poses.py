#!/usr/bin/env python3
"""Render ROM pose lists for semantic animation-table review (no ROM writes)."""
from __future__ import annotations

import argparse
import struct
from pathlib import Path

from PIL import Image, ImageDraw

import build_mk2ks_mk3 as b
import upgrade_ksui_previews as ui


def render_group(program, gfx, palette, frames):
    specs = [ui.component_spec(program, address) for address in frames]
    left = min(-s[4] for s in specs)
    top = min(-s[5] for s in specs)
    right = max(-s[4] + s[2] for s in specs)
    bottom = max(-s[5] + s[3] for s in specs)
    canvas = Image.new("RGBA", (right - left, bottom - top))
    for source, command, width, height, xo, yo in specs:
        if command & 0x80:
            part = ui.decode_component(gfx, palette, source, command, width, height)
        else:
            part = Image.new("RGBA", (width, height))
            bits = (command >> 12) & 7
            for y in range(height):
                for x in range(width):
                    index = ui.extract_bits(gfx, source + (y * width + x) * bits, (1 << bits) - 1)
                    if index:
                        part.putpixel((x, y), palette[index])
        canvas.alpha_composite(part, (-xo - left, -yo - top))
    return canvas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("fighter", choices=("kano", "sonya", "liu"))
    parser.add_argument("output", type=Path)
    parser.add_argument("--special", action="store_true", help="inspect the secondary animation table")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.fighter == "liu":
        program = (args.workspace / "mk2/mk2-maincpu.bin").read_bytes()
        root, special, block = b.LIU_MAIN, b.LIU_SPECIAL, b.LIU_BLOCK
        gfx = bytearray(0xc00000)
        for base, pair in enumerate(((14, 19), (16, 20), (17, 22))):
            for lane, (side, chip) in enumerate((('g', pair[0]), ('j', pair[0]), ('g', pair[1]), ('j', pair[1]))):
                payload = (args.workspace / "mk2" / f"l1_mortal_kombat_ii_game_rom_u{side}{chip}.u{side}{chip}").read_bytes()
                gfx[base * 0x400000 + lane:base * 0x400000 + lane + len(payload) * 4:4] = payload
        offset = b.stock_file(0xffadc8b0)
        count = b.u16(program, offset)
        palette = [(0, 0, 0, 0)] + [(*ui.xrgb555(b.u16(program, offset + 2 + i * 2)), 255) for i in range(1, min(count, 256))]
        palette += [(255, 255, 255, 255)] * (256 - len(palette))
    else:
        program = (args.workspace / "mk3/mk3-maincpu.bin").read_bytes()
        gfx = ui.load_gfx(args.workspace / "roms_v22_clean/mk2ks")
        palette = ui.donor_palette(program, args.fighter)
        root, special, block = ((b.KANO_MAIN, b.KANO_SPECIAL, b.KANO_BLOCK) if args.fighter == "kano"
                                else (b.SONYA_MAIN, b.SONYA_SPECIAL, b.SONYA_BLOCK))
    selected_root = special if args.special else root
    spans = b.sequence_spans(program, selected_root, block, (root, special))
    kind = "special" if args.special else "main"
    # Unlike the 65-cell main dispatch table, the special table ends where
    # the first main pose script begins.  Continuing to scan that region is
    # useful for reviewing embedded component lists, but those cells are not
    # independent special-move IDs.
    special_slots = (b.u32(program, b.stock_file(root)) - special) // 32
    for page in range((b.ANIMATION_ENTRIES + 15) // 16):
        sheet = Image.new("RGB", (1040, 680), (45, 45, 50))
        draw = ImageDraw.Draw(sheet)
        for index in range(page * 16, page * 16 + 16):
            x, y = (index % 4) * 260, (index // 4 % 4) * 170
            if index not in spans:
                continue
            span = spans[index]
            groups = b.group_references(program, *span, *block)
            groups = list(dict((value, frames) for _, value, frames in groups).items())
            # Some late MKII dispatch entries are direct frame lists, not
            # pointers to zero-terminated composite groups.  Show those too:
            # skipping them made live entries 60-64 look empty in the audit.
            direct = False
            if not groups:
                refs = b.frame_references(program, *span)
                groups = list(dict((value, [value]) for _, value in refs).items())
                direct = bool(groups)
            form = "direct frames" if direct else "poses"
            label = "component data" if args.special and index >= special_slots else kind
            draw.text((x + 4, y + 2), f"{args.fighter} {label} {index} / {span[0]:08X} ({len(groups)} {form})", fill="white")
            if not groups:
                continue
            for slot, position in enumerate((0, len(groups) // 2, len(groups) - 1)):
                address, frames = groups[position]
                pose = render_group(program, gfx, palette, frames)
                pose.thumbnail((84, 142), Image.Resampling.NEAREST)
                sheet.paste(pose, (x + slot * 86 + (84 - pose.width) // 2, y + 20 + 142 - pose.height), pose)
                draw.text((x + slot * 86, y + 158), f"{address & 0xfffff:05X}", fill="yellow")
        filename = f"{args.fighter}_special_{page}.png" if args.special else f"{args.fighter}_{page}.png"
        path = args.output / filename
        sheet.save(path)
        print(path)


if __name__ == "__main__":
    main()
