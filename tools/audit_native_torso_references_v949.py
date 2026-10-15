"""Decode native Cage victim body sections without changing ROM/artwork."""
import hashlib
import json
import struct
from pathlib import Path
from PIL import Image, ImageDraw
import audit_animation_poses as poses
import audit_native_inflation_references_v931 as native
import upgrade_ksui_previews as ui

ROOT = native.ROOT
OUT = ROOT / 'audit_v949_native_torso_references'
GROUPS = (0xff926130, 0xff92b250, 0xff92b2b0, 0xff92b330, 0xff92b370, 0xff92b3d0, 0xff92b430, 0xff92bcf0)
UPPER = ((0xffb49b80, 0xffb49bf0), (0xffb49c60, 0xffb49cd0, 0xffb49d40),
         (0xffb49db0,), (0xffb49e20, 0xffb49e90), (0xffb49f00, 0xffb49f70), (0xffb49fe0, 0xffb4a050))


def main():
    if OUT.exists():
        raise ValueError('Preserve references')
    program = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
    assert native.digest(program) == '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
    gfx = bytearray(0xc00000)
    pins = {'mk2/mk2-maincpu.bin': native.digest(program)}
    for base, pair in enumerate(((14, 19), (16, 20), (17, 22))):
        for lane, (side, chip) in enumerate((('g', pair[0]), ('j', pair[0]), ('g', pair[1]), ('j', pair[1]))):
            name = f'mk2/l1_mortal_kombat_ii_game_rom_u{side}{chip}.u{side}{chip}'
            data = (ROOT / name).read_bytes(); assert len(data) == 0x100000
            pins[name] = native.digest(data)
            gfx[base * 0x400000 + lane:base * 0x400000 + lane + len(data) * 4:4] = data
    OUT.mkdir()
    groups = []
    for group in GROUPS:
        frames = []
        for index in range(8):
            value = struct.unpack_from('<I', program, native.off(group) + index * 4)[0]
            if value == 0: break
            frames.append(value)
        else: raise ValueError('Unterminated native group')
        groups.append(tuple(frames))
    normal, severed = native.palette(program, 0xffadc8b0), native.palette(program, 0xffadd0d0)
    report = {'scope': 'original_native_torso_rip_reference_only', 'inputHashes': pins, 'groups': [], 'upper': []}
    for kind, lists in (('groups', groups), ('upper', UPPER)):
        sheet = Image.new('RGBA', (1200, 400 if kind == 'groups' else 240), (35, 35, 40, 255))
        draw = ImageDraw.Draw(sheet)
        for index, frames in enumerate(lists):
            specs = [ui.component_spec(program, frame) for frame in frames]
            bounds = [min(-s[4] for s in specs), min(-s[5] for s in specs),
                      max(-s[4] + s[2] for s in specs), max(-s[5] + s[3] for s in specs)]
            image = poses.render_group(program, gfx, normal if kind == 'groups' and index == 0 else severed, frames)
            image.save(OUT / f'liu-torso-{kind}-{index}.png')
            cellw, cellh, cols = (300, 200, 4) if kind == 'groups' else (200, 240, 6)
            x, y = index % cols * cellw, index // cols * cellh
            scaled = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)
            if scaled.height > cellh - 45:
                scaled = image
            sheet.alpha_composite(scaled, (x + (cellw - scaled.width) // 2, y + cellh - 8 - scaled.height))
            draw.text((x + 3, y + 2), f'{kind} {index}: {bounds}', fill='white')
            draw.text((x + 3, y + 16), ','.join(f'{f:08X}' for f in frames), fill='white')
            report[kind].append({'index': index, 'group': f'{GROUPS[index]:08X}' if kind == 'groups' else None,
                                 'frames': [f'{f:08X}' for f in frames], 'bounds': bounds, 'component_specs': specs})
        sheet.save(OUT / f'liu-torso-{kind}-reference.png')
    words = struct.unpack_from('<52I', program, native.off(0xff92aef0))
    report['native_main57_words'] = [f'{w:08X}' for w in words]
    (OUT / 'reference.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'output': str(OUT), 'native_groups': 8, 'upper_section_poses': 6, 'rom_writes': 0}))


if __name__ == '__main__': main()
