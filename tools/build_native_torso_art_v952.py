"""Encode owned Cage victim sections, preserving every native main57 token.

Alpha-cell crop, uniform resampling, palette quantization and column tiling
are format conversion only. This tool never paints or synthesizes artwork.
Encoding is not native runtime, alternate-costume or full-port acceptance.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import build_native_death_art_v900 as death
import build_native_pit_fall_v2 as colors
import build_native_projectile_impacts as codec

ROOT = Path(__file__).resolve().parents[1]
HEADER, DESCRIPTORS, GROUPS, PIXELS, END = 0x1b0000, 0x1b0400, 0x1b0800, 0x1b1000, 0x1c0000
ROM_DESCRIPTORS, ROM_GROUPS, GFX, GFX_END = 0xfb200, 0xfb480, 0x1f20000, 0x1f40000
SOURCE_SHA = '6482D45F2105D9E6410C9CCE3AE64B6C5A28671972F8F7EDD3F7B54F3A42F637'
ASSETS = {'kano-upper-torsos.png': '8728BE7511E511B1FA2D3582F63C8422FB636AF2EDE04BB3387BA14D9A620F6E',
          'sonya-upper-torsos.png': '1E3CF3FE88077D8FB5053435F818B504537D11F499D3B8DF75ED8D0C9586639C',
          'lower-stumps.png': 'F17F2528885C2E751965A7E9634CFA2358DB833A2A84C87F2577468730828DE0'}
STREAMS = (0xff00b290, 0xff02b290)
COUNTS = (2, 3, 1, 2, 2, 2, 2)
OLD_GROUPS = ((0xff0133a0, 0xff0133e0, 0xff013440, 0xff0134a0, 0xff013560, 0xff0134e0, 0xff013520),
              (0xff0334e0, 0xff033540, 0xff0335a0, 0xff033600, 0xff033700, 0xff033660, 0xff0336c0))
GROUP_WORDS = {6: 0, 9: 1, 13: 1, 17: 2, 20: 3, 22: 5, 23: 5, 25: 6,
               45: 0, 46: 1, 47: 2, 48: 3, 49: 4, 50: 5}
RAW_WORDS = (27, 28, 30, 31, 32, 34, 36, 37, 39, 40, 42, 43)
OLD_RAW = (0xffb49b80, 0xffb49bf0, 0xffb49c60, 0xffb49cd0, 0xffb49d40, 0xffb49db0,
           0xffb49e20, 0xffb49e90, 0xffb49f00, 0xffb49f70, 0xffb49fe0, 0xffb4a050)
BOUNDS = ((-7, -10, 47, 66), (-14, 9, 52, 66), (-13, 4, 27, 72),
          (-20, 21, 49, 67), (-4, 24, 44, 80), (-14, 52, 71, 88))


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def address(at):
    return 0xff800000 + at * 8


def crop_cell(image, box):
    cell = image.crop(box)
    alpha = cell.getchannel('A').point(lambda value: 255 if value >= 128 else 0)
    bounds = alpha.getbbox()
    if not bounds or min(bounds[:2]) < 2 or bounds[2] > cell.width - 2 or bounds[3] > cell.height - 2:
        raise ValueError('Missing or clipped transparent sprite cell')
    return cell.crop(bounds), list(bounds)


def build(output):
    if output.exists():
        raise ValueError('Preserve all existing builds and evidence')
    source = (ROOT / 'diagnostic_v936_owned_inflation_art/roms/mk2ks/mk2ks.mdata').read_bytes()
    donor = (ROOT / 'mk3/mk3-maincpu.bin').read_bytes()
    stock = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
    if len(source) != 0x200000 or sha(source) != SOURCE_SHA or sha(donor) != death.DONOR_SHA.upper() or sha(stock) != death.STOCK_SHA.upper():
        raise ValueError('Exact current candidate and immutable original programs required')
    if source[HEADER:END] != b'\xff' * (END - HEADER):
        raise ValueError('Torso allocation is not empty')
    images = {}
    for name, digest in ASSETS.items():
        path = ROOT / 'art_native_torso_v951' / name
        if sha(path.read_bytes()) != digest:
            raise ValueError('Selected transparent source changed: ' + name)
        images[name] = Image.open(path).convert('RGBA')
    if any(images[name].size != (1536, 1024) for name in ASSETS if name != 'lower-stumps.png'):
        raise ValueError('Six equal 512px cells required')
    if images['lower-stumps.png'].size != (1254, 1254):
        raise ValueError('Selected built-in output has two equal 627px columns')
    payload = bytearray(source)
    report = dict(scope='owned Cage torso section encoding; not native runtime or artwork acceptance',
                  source_sha256=SOURCE_SHA, assets=ASSETS, header=HEADER, descriptors=DESCRIPTORS,
                  groups=GROUPS, pixels=PIXELS, end=END, rom_descriptors=ROM_DESCRIPTORS,
                  rom_groups=ROM_GROUPS, gfx=GFX, gfx_end=GFX_END, alpha_cutoff=128,
                  source_artwork_immutable=True, native_component_counts=list(COUNTS), fighters={},
                  artAcceptance=False, runtimeAcceptance=False, alternateCostumeAcceptance=False, fullPortAcceptance=False)
    pixel_at, descriptor_index, group_at = PIXELS, 0, GROUPS
    allowed = [(HEADER, END)]
    preview = Image.new('RGBA', (1400, 480), (35, 35, 40, 255))
    draw = ImageDraw.Draw(preview)
    for fighter, name in enumerate(('kano', 'sonya')):
        atlas = images[name + '-upper-torsos.png']
        parts = [crop_cell(atlas, (pose % 3 * 512, pose // 3 * 512, (pose % 3 + 1) * 512, (pose // 3 + 1) * 512)) for pose in range(6)]
        upper_factor = 76 / parts[0][0].height
        lower = crop_cell(images['lower-stumps.png'], (fighter * 627, 0, (fighter + 1) * 627, 1254))
        # Native construction copies the victim at floor-1 in this action.
        # Contact bottom is therefore own standing anchor+1: 140/141.
        lower_bottom = 140 + fighter
        lower_factor = (lower_bottom - 47) / lower[0].height
        normal = colors.palette(donor, (0x92bbc, 0x92cf2)[fighter])
        alternate = colors.palette(donor, (0x92c3e, 0x92d74)[fighter])
        original = list(struct.unpack_from('<52I', source, death.offset(STREAMS[fighter])))
        for word, pose in GROUP_WORDS.items():
            if original[word] != OLD_GROUPS[fighter][pose]:
                raise ValueError('Owned main57 group grammar changed')
        if [original[word] for word in RAW_WORDS] != list(OLD_RAW):
            raise ValueError('Original raw body-section grammar changed')
        words = original.copy()
        group_pointers, raw_pointers, poses = [], [], []
        for pose, (image, crop) in enumerate(parts + [lower]):
            factor = upper_factor if pose < 6 else lower_factor
            width, height = round(image.width * factor), round(image.height * factor)
            if not 1 <= width <= 120 or not 1 <= height <= 120:
                raise ValueError('Section outside native bounds')
            indices = colors.quantize(image.resize((width, height), Image.Resampling.LANCZOS), normal)
            if pose < 6:
                native = BOUNDS[pose]
                left, bottom = round((native[0] + native[2] - width) / 2), native[3]
            else:
                left, bottom = round((5 - width) / 2), lower_bottom
            top = bottom - height
            components = []
            for column in range(COUNTS[pose]):
                x0, x1 = column * width // COUNTS[pose], (column + 1) * width // COUNTS[pose]
                tile = indices[:, x0:x1].copy()
                raw = tile.tobytes()
                packed = codec.pack_indices(raw)
                if not any(raw) or death.unpack(packed, len(raw)) != raw:
                    raise ValueError('Empty native component or bad six-bit round trip')
                if pixel_at + len(packed) > END or GFX + pixel_at - PIXELS + len(packed) > GFX_END:
                    raise ValueError('Native graphics allocation overflow')
                desc_at = DESCRIPTORS + descriptor_index * 20
                descriptor = address(ROM_DESCRIPTORS + descriptor_index * 20)
                graphic = (GFX + pixel_at - PIXELS) * 8
                own_palette = address((0xfda00, 0xfdb00)[fighter])
                struct.pack_into('<4hIHIH', payload, desc_at, x1 - x0, height, -left - x0, -top, graphic, 0x6000, own_palette, 0)
                payload[pixel_at:pixel_at + len(packed)] = packed
                components.append(dict(descriptor=f'{descriptor:08X}', graphics=f'{graphic:08X}',
                                       column=[x0, x1], size=[x1 - x0, height], bounds=[left + x0, top, left + x1, bottom],
                                       pixel_offset=pixel_at, packed_bytes=len(packed), indices_sha256=sha(raw)))
                pixel_at = (pixel_at + len(packed) + 3) & ~3
                descriptor_index += 1
            group = address(ROM_GROUPS + group_at - GROUPS)
            pointers = [int(c['descriptor'], 16) for c in components]
            struct.pack_into('<' + str(len(pointers) + 1) + 'I', payload, group_at, *pointers, 0)
            group_at += (len(pointers) + 1) * 4
            group_pointers.append(group)
            if pose < 6:
                raw_pointers.extend(pointers)
            poses.append(dict(pose=pose, kind='upper' if pose < 6 else 'lower', group=f'{group:08X}',
                              source_crop=crop, scale=factor, size=[width, height], bounds=[left, top, left + width, bottom],
                              full_indices_sha256=sha(indices.tobytes()), components=components))
            for costume, palette in enumerate((normal, alternate)):
                x, y = pose * 200, (fighter * 2 + costume) * 120
                draw.text((x + 2, y + 2), f'{name} {pose}/{costume}: {width}x{height}', fill='white')
                preview.alpha_composite(colors.decoded(indices, palette), (x + (200 - width) // 2, y + 118 - height))
        for word, pose in GROUP_WORDS.items():
            words[word] = group_pointers[pose]
        for word, pointer in zip(RAW_WORDS, raw_pointers):
            words[word] = pointer
        at = death.offset(STREAMS[fighter])
        struct.pack_into('<52I', payload, at, *words)
        allowed.append((at, at + 52 * 4))
        if any(words[i] != original[i] for i in range(52) if i not in GROUP_WORDS and i not in RAW_WORDS):
            raise ValueError('Native coordinate/control/function/separator changed')
        report['fighters'][name] = dict(id=17 + fighter, stream=f'{STREAMS[fighter]:08X}',
                                        original_words=[f'{w:08X}' for w in original], words=[f'{w:08X}' for w in words],
                                        upper_uniform_scale=upper_factor, lower_uniform_scale=lower_factor, poses=poses)
    assert descriptor_index == 28 and group_at - GROUPS == 168
    byte_count = pixel_at - PIXELS
    struct.pack_into('<4s11I', payload, HEADER, b'KTR1', PIXELS, byte_count, GFX, DESCRIPTORS, ROM_DESCRIPTORS,
                     28, 20, GROUPS, ROM_GROUPS, 168, 7)
    changed = [i for i, (a, b) in enumerate(zip(source, payload)) if a != b]
    if any(not any(lo <= i < hi for lo, hi in allowed) for i in changed):
        raise ValueError('Unrelated payload data changed')
    report.update(pixel_bytes=byte_count, descriptor_bytes=560, group_bytes=168, changed_bytes=len(changed),
                  allowed_changes=allowed, payload_sha256=sha(payload), native_52_word_control_grammar_preserved=True,
                  native_multipart_component_counts_preserved=True, six_bit_roundtrip=True)
    (output / 'roms/mk2ks').mkdir(parents=True)
    (output / 'roms/mk2ks/mk2ks.mdata').write_bytes(payload)
    preview.save(output / 'native-torso-preview.png')
    preview.resize((2800, 960), Image.Resampling.NEAREST).save(output / 'native-torso-preview-2x.png')
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ('pixel_bytes', 'payload_sha256', 'changed_bytes', 'artAcceptance', 'runtimeAcceptance')}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    build(parser.parse_args().output)
