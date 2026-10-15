"""Read-only ROM decoding of the native six-pose inflation grammar.

This renders original assets for reference; it does not paint replacement art
or mutate program/graphics data. Native descriptors retain their own anchors.
"""
import hashlib
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw
import audit_animation_poses as poses
import upgrade_ksui_previews as ui

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_v931_native_inflation_references'


def off(pointer):
    return (pointer - 0xff800000) // 8


def digest(data):
    return hashlib.sha256(data).hexdigest().upper()


def palette(program, address):
    at = off(address)
    count = struct.unpack_from('<I', program, at)[0]
    assert 1 <= count <= 255
    colors = [(0, 0, 0, 0)]
    colors.extend((*ui.xrgb555(struct.unpack_from('<H', program, at + 4 + i * 2)[0]), 255)
                  for i in range(count))
    colors += [(255, 0, 255, 255)] * (256 - len(colors))
    return colors


def main():
    if OUT.exists():
        raise ValueError('Refuse to replace reference evidence')
    program = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
    assert digest(program) == '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
    gfx = bytearray(0xc00000)
    inputs = {'mk2/mk2-maincpu.bin': digest(program)}
    for base, pair in enumerate(((14, 19), (16, 20), (17, 22))):
        for lane, (side, chip) in enumerate((('g', pair[0]), ('j', pair[0]), ('g', pair[1]), ('j', pair[1]))):
            name = f'mk2/l1_mortal_kombat_ii_game_rom_u{side}{chip}.u{side}{chip}'
            data = (ROOT / name).read_bytes()
            assert len(data) == 0x100000
            inputs[name] = digest(data)
            gfx[base * 0x400000 + lane:base * 0x400000 + lane + len(data) * 4:4] = data
    OUT.mkdir()
    report = {'scope': 'original_rom_reference_only', 'inputHashes': inputs, 'fighters': {}}
    for name, stream, first, last in (
            ('liu', 0xff9f0f80, 0xffaf84a0, 0xffaf6c60),
            ('kitana', 0xff9f1a00, 0xffaf8880, 0xffaf7070)):
        words = struct.unpack_from('<8I', program, off(stream))
        assert words[5] == words[7] == 0
        groups = [words[index] for index in (0, 1, 2, 3, 4, 6)]
        sheet = Image.new('RGBA', (1200, 360), (35, 35, 40, 255))
        draw = ImageDraw.Draw(sheet)
        records = []
        for pose, group in enumerate(groups):
            frames = []
            for index in range(8):
                value = struct.unpack_from('<I', program, off(group) + index * 4)[0]
                if value == 0:
                    break
                frames.append(value)
            else:
                raise ValueError('Unterminated original body group')
            specs = [ui.component_spec(program, frame) for frame in frames]
            bounds = [min(-s[4] for s in specs), min(-s[5] for s in specs),
                      max(-s[4] + s[2] for s in specs), max(-s[5] + s[3] for s in specs)]
            pal = first if pose < 5 else last
            image = poses.render_group(program, gfx, palette(program, pal), frames)
            image.save(OUT / f'{name}-inflate-{pose}.png')
            scaled = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)
            sheet.alpha_composite(scaled, (pose * 200 + (200 - scaled.width) // 2, 348 - scaled.height))
            draw.text((pose * 200 + 4, 3), f'{name} {pose}: {group:08X}', fill='white')
            draw.text((pose * 200 + 4, 17), f'bounds {bounds}', fill='white')
            records.append({'pose': pose, 'group': f'{group:08X}', 'frames': [f'{v:08X}' for v in frames],
                            'component_specs': specs, 'bounds': bounds, 'palette': f'{pal:08X}',
                            'rgba_sha256': digest(image.tobytes())})
        sheet.save(OUT / f'{name}-inflation-reference.png')
        report['fighters'][name] = {'stream': f'{stream:08X}', 'words': [f'{v:08X}' for v in words], 'poses': records}
    (OUT / 'reference.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'output': str(OUT), 'original_poses': 12, 'rom_writes': 0}))


if __name__ == '__main__':
    main()
