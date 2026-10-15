"""Encode generated owned inflation sprites without changing native behavior.

Only format conversion: alpha-cell isolation, one uniform fighter scale,
palette quantization and six-bit packing. No painting/pose synthesis in code.
Original PNGs, stock assets, sequence tokens and prior payload are immutable.
This builder alone is NOT runtime, artistic or full-port acceptance.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

import build_native_pit_fall_v2 as colors
import build_native_projectile_impacts as codec
import build_native_death_art_v900 as death
import upgrade_ksui_previews as ui

ROOT = Path(__file__).resolve().parents[1]
HEADER, DESCRIPTORS, GROUPS, PALETTES, STREAMS = 0x180000, 0x180400, 0x180600, 0x180800, 0x180a80
PIXELS, END = 0x184000, 0x1c0000
ROM_DESCRIPTORS, ROM_GROUPS, GFX, GFX_END = 0xfb040, 0xfb180, 0x1ee0000, 0x1f20000
ROM_STREAMS = (0xfad40, 0xfad60)
ROM_PALETTES = ((0xfae00, 0xfae90), (0xfaf20, 0xfafb0))
SOURCE_SHA = 'CC4F29043DE71AEEB0820D15E5A449A14073CDFBFA3F58B756751C92073964DF'
ASSETS = {'kano': 'FDC367B9CBF98CD16710DA6A2FAF79375EB9EED0F895535478A7983B6EAF2E6A',
          'sonya': 'AEA66EAE9C8EC517C619372BD39038EEE346A15AEB2EC1141A17771542708221'}
HEIGHTS, FLOORS, CENTERS = (130, 131), (139, 140), (3, -2)


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def addr(at):
    return 0xff800000 + at * 8


def cells(path):
    image = Image.open(path).convert('RGBA')
    if image.size != (1536, 1024):
        raise ValueError('Exact three-by-two atlas required')
    array = np.array(image)
    result = []
    for pose in range(6):
        x, y = pose % 3 * 512, pose // 3 * 512
        part = array[y:y + 512, x:x + 512]
        yy, xx = np.where(part[:, :, 3] >= 128)
        if len(xx) < 10000:
            raise ValueError('Missing full-body alpha silhouette')
        box = [int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1]
        if min(box[:2]) < 2 or max(box[2:]) > 510:
            raise ValueError('Sprite or spray clipped at atlas cell boundary')
        result.append((box, Image.fromarray(part[box[1]:box[3], box[0]:box[2]].copy()), len(xx)))
    return result


def palette_record(palette):
    # Index zero is transparency. Indices 1..64 use the original loader's
    # count/header and RGB555 packing; the six-bit renderer can use 1..63.
    return struct.pack('<I64H', 64, *(ui.rgb_to_xrgb555(*map(int, rgb)) for rgb in palette[1:65]))


def build(output):
    if output.exists():
        raise ValueError('Refuse to overwrite build or evidence')
    source_path = ROOT / 'diagnostic_v918_native_gore_victim_tables/roms/mk2ks/mk2ks.mdata'
    source = source_path.read_bytes()
    donor = (ROOT / 'mk3/mk3-maincpu.bin').read_bytes()
    stock = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
    if sha(source) != SOURCE_SHA or sha(donor) != death.DONOR_SHA.upper() or sha(stock) != death.STOCK_SHA.upper():
        raise ValueError('Exact accepted payload and original programs required')
    if source[HEADER:END] != b'\xff' * (END - HEADER):
        raise ValueError('Owned inflation allocation occupied')
    payload = bytearray(source)
    report = {'scope': 'owned_inflation_asset_encoding_not_runtime_or_art_acceptance',
              'base_payload_sha256': sha(source), 'stock_program_sha256': sha(stock),
              'donor_program_sha256': sha(donor), 'fighters': {}, 'palette_count': 64,
              'header': HEADER, 'descriptors': DESCRIPTORS, 'groups': GROUPS, 'palettes': PALETTES,
              'streams': STREAMS, 'pixels': PIXELS, 'end': END, 'rom_descriptors': ROM_DESCRIPTORS,
              'rom_groups': ROM_GROUPS, 'gfx_destination': GFX, 'gfx_end': GFX_END,
              'alpha_cutoff': 128, 'uniform_scale': True, 'native_control_grammar_preserved': True,
              'artAcceptance': False, 'runtimeAcceptance': False, 'fullPortAcceptance': False}
    sheet = Image.new('RGBA', (1200, 360), (35, 35, 40, 255))
    draw = ImageDraw.Draw(sheet)
    pixel_at = PIXELS
    for fighter, name in enumerate(('kano', 'sonya')):
        path = ROOT / 'art_native_inflation_v933' / (name + '-inflation.png')
        if sha(path.read_bytes()) != ASSETS[name]:
            raise ValueError('Selected inflation artwork changed: ' + name)
        parts = cells(path)
        factor = HEIGHTS[fighter] / parts[0][1].height
        normal = colors.palette(donor, (0x92bbc, 0x92cf2)[fighter])
        burst = normal.copy()
        burst[59:63] = [(255, 0, 0), (197, 0, 0), (139, 0, 0), (82, 0, 0)]
        for phase, pal in enumerate((normal, burst)):
            at = PALETTES + (fighter * 2 + phase) * 144
            encoded = palette_record(pal)
            payload[at:at + len(encoded)] = encoded
        records, pointers = [], []
        for pose, (box, image, area) in enumerate(parts):
            width, height = round(image.width * factor), round(image.height * factor)
            if not 1 <= width <= 180 or not 1 <= height <= 180:
                raise ValueError('Inflation silhouette outside owned native bounds')
            scaled = image.resize((width, height), Image.Resampling.LANCZOS)
            pal = normal if pose < 5 else burst
            indices = colors.quantize(scaled, pal)
            raw = indices.tobytes()
            packed = codec.pack_indices(raw)
            if death.unpack(packed, width * height) != raw or not any(raw):
                raise ValueError('Independent six-bit round trip failed')
            if pixel_at + len(packed) > END or GFX + pixel_at - PIXELS + len(packed) > GFX_END:
                raise ValueError('Inflation pixel allocation overflow')
            index = fighter * 6 + pose
            descriptor_at, group_at = DESCRIPTORS + index * 20, GROUPS + index * 8
            descriptor, group = addr(ROM_DESCRIPTORS + index * 20), addr(ROM_GROUPS + index * 8)
            left, top = CENTERS[fighter] - width // 2, FLOORS[fighter] - height
            graphic = (GFX + pixel_at - PIXELS) * 8
            palette = addr(ROM_PALETTES[fighter][0 if pose < 5 else 1])
            struct.pack_into('<4hIHIH', payload, descriptor_at, width, height, -left, -top, graphic, 0x6000, palette, 0)
            struct.pack_into('<2I', payload, group_at, descriptor, 0)
            payload[pixel_at:pixel_at + len(packed)] = packed
            pointers.append(group)
            records.append({'pose': pose, 'descriptor': f'{descriptor:08X}', 'group': f'{group:08X}',
                            'palette': f'{palette:08X}', 'source_crop': box, 'source_alpha_area': area,
                            'size': [width, height], 'bounds': [left, top, left + width, FLOORS[fighter]],
                            'graphics': f'{graphic:08X}', 'pixel_offset': pixel_at, 'packed_bytes': len(packed),
                            'indices_sha256': sha(raw), 'used_indices': sorted(set(raw))})
            x, y = pose * 200, fighter * 180
            draw.text((x + 3, y + 2), f'{name} {pose}: {width}x{height}', fill='white')
            sheet.alpha_composite(colors.decoded(indices, pal), (x + (200 - width) // 2, y + 176 - height))
            draw.line((x, y + 176, x + 199, y + 176), fill=(70, 70, 75))
            pixel_at = (pixel_at + len(packed) + 3) & ~3
        stream = [*pointers[:5], 0, pointers[5], 0]
        struct.pack_into('<8I', payload, STREAMS + fighter * 32, *stream)
        report['fighters'][name] = {'id': 17 + fighter, 'png': str(path), 'png_sha256': ASSETS[name],
                                    'scale': factor, 'ground_anchor': FLOORS[fighter], 'rom_stream': f'{addr(ROM_STREAMS[fighter]):08X}',
                                    'stream_words': [f'{v:08X}' for v in stream], 'frames': records}
    byte_count = pixel_at - PIXELS
    struct.pack_into('<4s13I', payload, HEADER, b'KIF1', PIXELS, byte_count, GFX,
                     DESCRIPTORS, ROM_DESCRIPTORS, 12, 20, GROUPS, ROM_GROUPS, PALETTES, STREAMS, 6, 2)
    if payload[:HEADER] != source[:HEADER] or payload[END:] != source[END:]:
        raise ValueError('Unrelated payload data changed')
    report.update(pixel_bytes=byte_count, output_sha256=sha(payload),
                  source_pngs_unchanged=True, six_bit_roundtrip=True,
                  burst_palette_policy='owned costume with red ramps at pens 59..62; unchanged native phase change')
    (output / 'roms/mk2ks').mkdir(parents=True)
    (output / 'roms/mk2ks/mk2ks.mdata').write_bytes(payload)
    sheet.save(output / 'native-inflation-preview.png')
    sheet.resize((2400, 720), Image.Resampling.NEAREST).save(output / 'native-inflation-preview-2x.png')
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'payload_sha256': report['output_sha256'], 'frames': 12, 'pixel_bytes': byte_count,
                      'artAcceptance': False, 'runtimeAcceptance': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    build(parser.parse_args().output)
