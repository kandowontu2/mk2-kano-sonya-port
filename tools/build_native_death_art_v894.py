"""Encode custom death artwork; preserve original native animation grammar.

This is format conversion, not painting: isolate existing alpha components,
uniformly downsample each source scale group, quantize to the owned costume
palette, and pack native six-bit pixels. Source PNGs are never modified.
Builder success does not constitute in-game art or whole-port acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label

import build_native_pit_fall_v2 as palettes
import build_native_projectile_impacts as codec

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_BASE = 0xFE800000
ROM_BASE = 0xFF800000
HEADER, DESCRIPTORS, PIXELS, END = 0x160000, 0x160400, 0x164000, 0x180000
ROM_DESCRIPTORS = 0xFAA00
GFX = 0x1EC0000
SOURCE_SHA = '7896c93822473376ad724bb5e747ede88c198203786f3f9b928cd1d860bae019'
STOCK_SHA = '45b3285496db555efaf4a3608a4f59845dd47a82e4a0593607e0592f47b36f23'
DONOR_SHA = '1bc7a53a023f15b20f01398f87e38478a27c670df27ea320e36125d0957ee651'
ASSETS = {
    'kano-bodies-first-five.png': 'ef72edcbf572b9d460b4372c95f32f43eaad4f2c7b3f090c6f93920be4435a13',
    'kano-bodies-last-two.png': '91ac4e2e7aecc9f9efd9ff083fd46cee4c6a88ef04c6ef1858d02668fb51cc5e',
    'kano-heads.png': '69a8b33de3835ab33627627fdad410fcb5f29836c1f248acf5492167077043a2',
    'sonya-bodies.png': '805f6a9e244d0ceecb0706b6c2ce5bb7744af6deb26c0850a1c1e5215d28c674',
    'sonya-heads.png': 'f5d2e85765f366b4fd530b9f7c58097f5fb0953f9db436f2d90dab4a5408d3b9',
}
GROUPS = {
    'kano': (0xFF0137E0, 0xFF013840, 0xFF0138A0, 0xFF013900, 0xFF013960, 0xFF0139C0, 0xFF013A20),
    'sonya': (0xFF0339A0, 0xFF033A00, 0xFF033A60, 0xFF033AC0, 0xFF033B20, 0xFF033B80, 0xFF033BE0),
}
OLD_PARTS = {
    'kano': ((0xFEB0D610, 0xFEB0D6A0), (0xFEB0D730, 0xFEB0D7A0),
             (0xFEB0D8F0, 0xFEB0D960), (0xFEB0D9D0, 0xFEB0DA40),
             (0xFEB0DAB0, 0xFEB0DB20), (0xFEB0DC70, 0xFEB0DCE0), (0xFEB0DD50, 0xFEB0DDC0)),
    'sonya': ((0xFEB19C70, 0xFEB19D00), (0xFEB19D90, 0xFEB19E00),
              (0xFEB19E70, 0xFEB19EE0), (0xFEB1A030, 0xFEB1A0A0),
              (0xFEB1A110, 0xFEB1A180), (0xFEB1A1F0, 0xFEB1A260), (0xFEB1A2D0, 0xFEB1A340)),
}
STREAMS = {'kano': (0xFF00BA30, 0xFF00B910), 'sonya': (0xFF02BA30, 0xFF02B910)}
# Native MKII headless-body anchors, not a changed physical actor/floor.
LEFTS = (-14, -20, -14, -13, -15, -10, -15)
BOTTOMS = (143, 143, 143, 143, 143, 149, 153)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def offset(pointer):
    if pointer < PAYLOAD_BASE or pointer >= PAYLOAD_BASE + 0x200000 * 8 or pointer & 7:
        raise ValueError('Invalid owned payload pointer')
    return (pointer - PAYLOAD_BASE) // 8


def components(path):
    image = Image.open(path).convert('RGBA')
    pixels = np.array(image)
    labels, count = label(pixels[:, :, 3] >= 128, np.ones((3, 3)))
    result = []
    for component in range(1, count + 1):
        yy, xx = np.where(labels == component)
        if len(xx) < 10000:
            continue
        box = (int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1)
        crop = pixels[box[1]:box[3], box[0]:box[2]].copy()
        crop[:, :, 3] = np.where(labels[box[1]:box[3], box[0]:box[2]] == component, 255, 0)
        result.append((box, Image.fromarray(crop), len(xx)))
    return sorted(result, key=lambda part: (part[0][1] // (image.height // 2), part[0][0]))


def unpack(packed, count):
    # Independent scalar decoder catches packing/row-crossing errors.
    output = bytearray(count)
    for pixel in range(count):
        bit = pixel * 6
        word = packed[bit // 8]
        if bit // 8 + 1 < len(packed):
            word |= packed[bit // 8 + 1] << 8
        output[pixel] = (word >> (bit % 8)) & 63
    return bytes(output)


def build(output):
    if output.exists():
        raise ValueError('Refuse to overwrite evidence or payload')
    source_path = ROOT / 'diagnostic_v873_native_headless_palettes/roms/mk2ks/mk2ks.mdata'
    source = source_path.read_bytes()
    stock = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
    donor = (ROOT / 'mk3/mk3-maincpu.bin').read_bytes()
    if len(source) != 0x200000 or sha(source) != SOURCE_SHA or sha(stock) != STOCK_SHA or sha(donor) != DONOR_SHA:
        raise ValueError('Exact accepted base and original ROM references required')
    if source[HEADER:END] != b'\xff' * (END - HEADER):
        raise ValueError('Death-art allocation occupied')
    parts = {}
    for filename, expected in ASSETS.items():
        path = ROOT / 'art_native_death_v893' / filename
        if sha(path.read_bytes()) != expected:
            raise ValueError('Selected source PNG changed: ' + filename)
        parts[filename] = components(path)
    kano_first = parts['kano-bodies-first-five.png']
    kano_last = parts['kano-bodies-last-two.png']
    sonya = parts['sonya-bodies.png']
    if len(kano_first) != 6 or len(kano_last) != 2 or len(sonya) != 7:
        raise ValueError('Unexpected isolated body count')
    bodies = {'kano': kano_first[:5] + kano_last, 'sonya': sonya}
    body_factors = {'kano': [110 / kano_first[0][1].height] * 5 + [130 / kano_last[1][1].width] * 2,
                    'sonya': [105 / sonya[0][1].height] * 5 + [125 / sonya[6][1].width] * 2}
    payload = bytearray(source)
    allowed = [(HEADER, END)]
    pixel_at, descriptor_at = PIXELS, DESCRIPTORS
    report = {'scope': 'custom_asset_encoding_not_runtime_or_art_acceptance', 'source_sha256': sha(source),
              'original_mk2_sha256': sha(stock), 'original_mk3_sha256': sha(donor),
              'assets': ASSETS, 'alpha_cutoff': 128, 'palette_policy': 'owned_native_indices_1_to_63',
              'header_offset': HEADER, 'descriptor_offset': DESCRIPTORS, 'rom_descriptor_offset': ROM_DESCRIPTORS,
              'pixel_offset': PIXELS, 'gfx_destination': GFX, 'fighters': {},
              'artAcceptance': False, 'runtimeAcceptance': False, 'fullPortAcceptance': False}
    previews = []
    for fighter_index, fighter in enumerate(('kano', 'sonya')):
        heads = parts[fighter + '-heads.png']
        if len(heads) != 7:
            raise ValueError('Unexpected detached head count')
        normal = palettes.palette(donor, (0x92BBC, 0x92CF2)[fighter_index])
        alternate = palettes.palette(donor, (0x92C3E, 0x92D74)[fighter_index])
        stream60, stream61 = STREAMS[fighter]
        original60 = bytes(source[offset(stream60):offset(stream60) + 64])
        # The original list's 0x70/0x90 descriptor strides are not uniform.
        old_heads = (0xFFB4A4B0, 0xFFB4A540, 0xFFB4A5B0, 0xFFB4A620, 0xFFB4A690, 0xFFB4A700, 0xFFB4A770)
        if struct.unpack_from('<9I', source, offset(stream61)) != (*old_heads, 1, stream61):
            raise ValueError('Original owned main61 grammar changed')
        records = []
        for kind, source_parts, factors in (
                ('body', bodies[fighter], body_factors[fighter]),
                ('head', heads, [27 / heads[0][1].height] * 7)):
            for pose, (part, factor) in enumerate(zip(source_parts, factors)):
                box, image, area = part
                size = (round(image.width * factor), round(image.height * factor))
                scaled = image.resize(size, Image.Resampling.LANCZOS)
                indices = palettes.quantize(scaled, normal)
                raw = indices.tobytes()
                packed = codec.pack_indices(raw)
                if unpack(packed, len(raw)) != raw or max(raw) > 63 or not any(raw):
                    raise ValueError('Native six-bit pixel roundtrip failed')
                if pixel_at + len(packed) > END or descriptor_at + 20 > PIXELS:
                    raise ValueError('Death-art allocation overflow')
                descriptor = ROM_BASE + (ROM_DESCRIPTORS + descriptor_at - DESCRIPTORS) * 8
                width, height = size
                if kind == 'body':
                    left, top = LEFTS[pose], BOTTOMS[pose] - height
                    group_at = offset(GROUPS[fighter][pose])
                    if struct.unpack_from('<3I', source, group_at) != (*OLD_PARTS[fighter][pose], 0):
                        raise ValueError('Original headed group changed')
                    struct.pack_into('<2I', payload, group_at, descriptor, 0)
                    allowed.append((group_at, group_at + 8))
                else:
                    left, top = -(width // 2), -(height // 2)
                    word_at = offset(stream61) + pose * 4
                    struct.pack_into('<I', payload, word_at, descriptor)
                    allowed.append((word_at, word_at + 4))
                graphic = (GFX + pixel_at - PIXELS) * 8
                own_palette = (0xFFFED000, 0xFFFED800)[fighter_index]
                struct.pack_into('<4hIHI', payload, descriptor_at, width, height, -left, -top,
                                 graphic, 0x6000, own_palette)
                # Pad two bytes to keep every native descriptor on a 20-byte stride.
                struct.pack_into('<H', payload, descriptor_at + 18, 0)
                payload[pixel_at:pixel_at + len(packed)] = packed
                records.append({'kind': kind, 'pose': pose, 'source_crop': box, 'source_alpha_area': area,
                                'scale': factor, 'size': size, 'bounds': [left, top, left + width, top + height],
                                'descriptor': f'{descriptor:08X}', 'payload_descriptor_offset': descriptor_at,
                                'graphics': f'{graphic:08X}', 'pixel_offset': pixel_at,
                                'packed_bytes': len(packed), 'indices_sha256': sha(raw), 'used_indices': sorted(set(raw))})
                previews.append((fighter, kind, pose, palettes.decoded(indices, normal), palettes.decoded(indices, alternate)))
                pixel_at = (pixel_at + len(packed) + 3) & ~3
                descriptor_at += 20
        if payload[offset(stream60):offset(stream60) + 64] != original60:
            raise ValueError('Native main60 animation control words changed')
        if payload[offset(stream61) + 28:offset(stream61) + 36] != source[offset(stream61) + 28:offset(stream61) + 36]:
            raise ValueError('Native main61 loop changed')
        report['fighters'][fighter] = {'main60': f'{stream60:08X}', 'main61': f'{stream61:08X}',
                                       'original_main60_sha256': sha(original60), 'frames': records}
    pixel_bytes = pixel_at - PIXELS
    struct.pack_into('<4s9I', payload, HEADER, b'KDH1', PIXELS, pixel_bytes, GFX,
                     DESCRIPTORS, ROM_DESCRIPTORS, 28, 20, 7, 2)
    changed = [at for at, (before, after) in enumerate(zip(source, payload)) if before != after]
    if any(not any(start <= at < end for start, end in allowed) for at in changed):
        raise ValueError('Unexpected unrelated payload changes')
    report.update(pixel_bytes=pixel_bytes, descriptor_bytes=28 * 20, changed_bytes=len(changed),
                  allowed_changes=allowed, output_sha256=sha(payload), native_control_grammar_preserved=True,
                  six_bit_pixel_roundtrip_passed=True,
                  scale_policy='uniform within first-five and final-two body source groups; uniform seven-head group; no stretching')
    output.mkdir(parents=True)
    roms = output / 'roms/mk2ks'
    roms.mkdir(parents=True)
    (roms / 'mk2ks.mdata').write_bytes(payload)
    body_sheet = Image.new('RGBA', (1120, 640), (35, 35, 40, 255))
    head_sheet = Image.new('RGBA', (560, 200), (35, 35, 40, 255))
    for fighter, kind, pose, normal, alternate in previews:
        for costume, image in enumerate((normal, alternate)):
            row = (0 if fighter == 'kano' else 2) + costume
            sheet = body_sheet if kind == 'body' else head_sheet
            cellw, cellh = (160, 160) if kind == 'body' else (80, 50)
            x, y = pose * cellw, row * cellh
            draw = ImageDraw.Draw(sheet)
            draw.text((x + 2, y + 1), f'{fighter} {costume}/{pose}', fill='white')
            if kind == 'body':
                sheet.alpha_composite(image, (x + 20, y + 156 - image.height))
                draw.line((x, y + 156, x + 155, y + 156), fill=(75, 75, 80))
            else:
                sheet.alpha_composite(image, (x + (cellw - image.width) // 2, y + 17))
    body_sheet.save(output / 'native-body-preview.png')
    head_sheet.save(output / 'native-head-preview.png')
    body_sheet.resize((2240, 1280), Image.Resampling.NEAREST).save(output / 'native-body-preview-2x.png')
    head_sheet.resize((2240, 800), Image.Resampling.NEAREST).save(output / 'native-head-preview-4x.png')
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'payload_sha256': report['output_sha256'], 'frames': 28,
                      'pixel_bytes': pixel_bytes, 'changed_bytes': len(changed), 'artAcceptance': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    build(parser.parse_args().output)
