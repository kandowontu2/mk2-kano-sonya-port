#!/usr/bin/env python3
"""Render original victim composites with their origin, not resized thumbnails.

Read-only ROM audit. The stock alternatives are not accepted mappings: review
the actual poses and contact points before selecting a native paired sequence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw

import build_mk2ks_mk3 as b
import upgrade_ksui_previews as ui
from audit_animation_poses import render_group
from leg_contact_points import POINTS, ALIASES, contact_points, flip_indices


NAMES = ("kung_lao", "liu_kang", "cage", "baraka", "kitana", "mileena",
         "shang_tsung", "raiden", "sub_zero", "reptile", "scorpion", "jax",
         "kintaro", "shao_kahn", "smoke", "noob", "jade")


def stock_gfx(workspace):
    gfx = bytearray(0xC00000)
    for base, pair in enumerate(((14, 19), (16, 20), (17, 22))):
        for lane, (side, chip) in enumerate((('g', pair[0]), ('j', pair[0]), ('g', pair[1]), ('j', pair[1]))):
            raw = (workspace / "mk2" / f"l1_mortal_kombat_ii_game_rom_u{side}{chip}.u{side}{chip}").read_bytes()
            gfx[base * 0x400000 + lane:base * 0x400000 + lane + len(raw) * 4:4] = raw
    return gfx


def stock_palette(program, fighter_id):
    pointer = b.u32(program, b.stock_file(0xFF907910) + fighter_id * 4)
    at = b.stock_file(pointer)
    count = b.u16(program, at)
    if not 1 <= count <= 256:
        raise ValueError(f"Unexpected stock palette {pointer:08X}: {count}")
    return [(0, 0, 0, 0)] + [(*ui.xrgb555(b.u16(program, at + 2 + i * 2)), 255)
                           for i in range(1, count)] + [(255, 0, 255, 255)] * (256 - count)


def stock_phases(program, root, index, phase_count):
    """Decode the native pose/XY token lists needed by this audit, bounded."""
    at = b.stock_file(b.u32(program, b.stock_file(root) + index * 4))
    limit, phases, groups = at + 0x180, 0, []
    while at < limit and phases < phase_count:
        token = b.u32(program, at)
        at += 4
        if token == 0:
            phases += 1
        elif token in (3, 8):
            at += 2
        elif token == 4:
            at += 4  # packed relative X/Y, not a group pointer
        elif token <= 9:
            raise ValueError(f"Unsupported audit token {token} at {at-4:X}")
        else:
            components = b.frame_group(program, token, b.TMS_ROM_BASE, 0xFFFFFFFF)
            if not components:
                raise ValueError(f"Invalid stock composite {token:08X}")
            if token not in groups:
                groups.append(token)
    if phases != phase_count:
        raise ValueError("Unterminated native pose list")
    return groups


def write_sheet(program, gfx, palette, groups, title, output, grid=False):
    cell_w, cell_h = 220, 235
    sheet = Image.new("RGB", (cell_w * 5, cell_h * ((len(groups) + 4) // 5)), (40, 42, 48))
    draw = ImageDraw.Draw(sheet)
    metadata = []
    for index, (label, pointer) in enumerate(groups):
        frames = b.frame_group(program, pointer, b.TMS_ROM_BASE, 0xFFFFFFFF)
        if not frames:
            raise ValueError(f"Invalid composite {pointer:08X}")
        specs = [ui.component_spec(program, value) for value in frames]
        left, top = min(-s[4] for s in specs), min(-s[5] for s in specs)
        x, y = (index % 5) * cell_w, (index // 5) * cell_h
        origin_x, origin_y = x + 95, y + 52
        if grid:
            for dx in range(-90, 121, 10):
                draw.line((origin_x + dx, y + 30, origin_x + dx, y + cell_h - 1), fill=(55, 57, 64))
                if dx % 20 == 0:
                    draw.text((origin_x + dx - 5, y + cell_h - 13), str(dx), fill=(130, 150, 150))
            for dy in range(-20, 171, 10):
                draw.line((x, origin_y + dy, x + cell_w - 1, origin_y + dy), fill=(55, 57, 64))
                if dy % 20 == 0:
                    draw.text((x + 2, origin_y + dy - 4), str(dy), fill=(130, 150, 150))
        draw.line((x, origin_y, x + cell_w - 1, origin_y), fill=(70, 85, 85))
        draw.line((origin_x, y + 30, origin_x, y + cell_h - 1), fill=(70, 85, 85))
        pose = render_group(program, gfx, palette, frames)
        sheet.paste(pose, (origin_x + left, origin_y + top), pose)
        draw.text((x + 3, y + 3), f"{title} {label}", fill="white")
        draw.text((x + 3, y + 17), f"{pointer:08X} origin 0,0", fill="yellow")
        if grid and (title in POINTS or title in ALIASES):
            px, py = contact_points(title)[index]
            cx, cy = origin_x + px, origin_y + py
            draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), outline="cyan")
            draw.text((x + 4, y + cell_h - 28), f"pivot ({px},{py})", fill="cyan")
        metadata.append({"label": label, "group": f"{pointer:08X}", "bounds":
                         [left, top, left + pose.width, top + pose.height]})
    sheet.save(output)
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--selected-grid", action="store_true", help="Show only the five current victim poses with native-pixel rulers")
    parser.add_argument("--roll-options", action="store_true", help="Audit all native forward-roll composites alongside the throw poses")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    stock = (args.workspace / "mk2/mk2-maincpu.bin").read_bytes()
    donor = (args.workspace / "mk3/mk3-maincpu.bin").read_bytes()
    sgfx, dgfx = stock_gfx(args.workspace), ui.load_gfx(args.workspace / "roms_v22_clean/mk2ks")
    report = {}
    for fighter, root in (("kano", b.KANO_MAIN), ("sonya", b.SONYA_MAIN)):
        at = b.stock_file(b.u32(donor, b.stock_file(root) + 54 * 4))
        groups = [(f"leg {i}", b.u32(donor, at + i * 12 + 8)) for i in range(5)]
        report[fighter] = write_sheet(donor, dgfx, ui.donor_palette(donor, fighter), groups,
                                     fighter, args.output / f"{fighter}_original.png", args.selected_grid)
    for fighter_id, name in enumerate(NAMES):
        if fighter_id in (12, 13):
            continue
        root = b.u32(stock, b.MK2_MAIN_TABLE + fighter_id * 4)
        if args.selected_grid:
            flip = stock_phases(stock, root, 43, 2)
            groups = [("leg 0", stock_phases(stock, root, 15, 1)[0])]
            groups += [(f"leg {i+1}", flip[position]) for i, position in enumerate(flip_indices(fighter_id))]
        else:
            groups = [(f"main{animation}:{i}", pointer) for animation, phases in ((15, 1), (43, 2))
                      for i, pointer in enumerate(stock_phases(stock, root, animation, phases))]
        if args.roll_options:
            at = b.stock_file(b.u32(stock, b.stock_file(root) + 7 * 4))
            roll = []
            for i in range(8):
                pointer = b.u32(stock, at + i * 4)
                if not b.frame_group(stock, pointer, b.TMS_ROM_BASE, 0xFFFFFFFF):
                    raise ValueError(f"Unexpected native roll layout: {name}")
                roll.append((f"roll {i}", pointer))
            groups = roll + groups
        report[name] = write_sheet(stock, sgfx, stock_palette(stock, fighter_id), groups,
                                  name, args.output / f"{name}_options.png", args.selected_grid and not args.roll_options)
    (args.output / "original_pose_inventory.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"Rendered {len(report)} original-pose sheets to {args.output}")


if __name__ == "__main__":
    main()
