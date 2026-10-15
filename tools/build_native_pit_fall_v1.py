"""Encode dedicated draft Pit sprites into native MKII data, non-destructively.

Raster operations here are asset encoding (alpha cutout, uniform downsampling,
existing-palette quantization), not painting or costume/pose edits. The source
PNG sheets were generated with image_gen and remain unchanged. Art and actual
scene acceptance must be checked separately; this builder is not proof of them.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import zlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import build_mk2ks_mk3 as b
import build_native_projectile_impacts as codec
import upgrade_ksui_previews as ui

HEADER, TABLE = 0x130000, 0x130100
SEQUENCES = (0x130200, 0x130240)
GROUPS, FRAMES = 0x130400, 0x130800
PIXELS, END = 0x134000, 0x160000
GFX_DEST, GFX_END = 0x1E80000, 0x1EC0000
STOCK_TABLE = 0xFF85E6B0
SOURCE_SHA = '82fe153fb56b46a6f9d42f493451ac3d59ad61713433714aca7704e2881f8951'
STOCK_SHA = '45b3285496db555efaf4a3608a4f59845dd47a82e4a0593607e0592f47b36f23'
PNG_NAMES = ('kano-pit-draft-v1.png', 'sonya-pit-draft-v2.png')
PNG_SHAS = ('3dab1f2fbc65b8ef0e4cf3e023a5dcd086b7d71c9a5b72b1dae08a64e95c600b',
            'cf4f8396cf0882ab8c4eb451d631cd49995a4d7803e9dcd3c71d7dde12087492')
PALETTE_RECORDS = ((0x92BBC, 0x92C3E), (0x92CF2, 0x92D74))
TOPS = (1, 3, -7, -5, 2, 0)
X_CENTERS = (1, -2, 5, 14, 14, 4)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def address(at):
    return b.DONOR_TMS_BASE + at * 8


def palette(program, at):
    if b.u32(program, at) != 64:
        raise ValueError('Body palette header changed')
    return np.array([(0, 0, 0)] + [ui.xrgb555(b.u16(program, at + 4 + i * 2))
                                  for i in range(64)], dtype=np.uint8)


def quantize(image, colors):
    pixels = np.asarray(image)
    visible = pixels[:, :, 3] >= 128
    # Pen zero is always transparent; original opaque body pens 1..63 remain
    # semantic indices so native alternate costumes/fades retain ownership.
    rgb = pixels[:, :, :3].astype(np.int32)
    ramps = colors[1:64].astype(np.int32)
    distance = np.sum((rgb[:, :, None, :] - ramps[None, None, :, :]) ** 2, axis=3)
    indices = (np.argmin(distance, axis=2) + 1).astype(np.uint8)
    indices[~visible] = 0
    return indices


def decoded(indices, colors):
    rgba = np.zeros((*indices.shape, 4), dtype=np.uint8)
    rgba[:, :, :3] = colors[indices]
    rgba[:, :, 3] = np.where(indices, 255, 0)
    return Image.fromarray(rgba)


def build(root, drafts, output):
    source = (root / 'diagnostic_v545_native_roll_edge_clearance/roms/mk2ks/mk2ks.mdata').read_bytes()
    stock = (root / 'mk2/mk2-maincpu.bin').read_bytes()
    donor = (root / 'mk3/mk3-maincpu.bin').read_bytes()
    if len(source) != 0x200000 or sha(source) != SOURCE_SHA or sha(stock) != STOCK_SHA:
        raise ValueError('Use exact v545 candidate and original MKII program')
    if any(value != 255 for value in source[HEADER:END]):
        raise ValueError('Dedicated Pit allocation is occupied')
    if output.exists():
        raise ValueError('Never overwrite asset evidence or payload')
    payload = bytearray(source)
    table = list(struct.unpack_from('<19I', stock, b.stock_file(STOCK_TABLE)))
    report = dict(scope='dedicated_draft_assets_not_scene_or_visual_acceptance',
                  source_sha256=sha(source), stock_sha256=sha(stock),
                  header=HEADER, table=f'{address(TABLE):08X}',
                  stock_table=f'{STOCK_TABLE:08X}', gfx_destination=GFX_DEST,
                  alpha_cutoff=128, palette_policy='existing_native_body_indices_1_through_63',
                  fighters={}, preserved_stock_rows=table[:17], fullPortAcceptance=False)
    frame_at, group_at, pixel_at = FRAMES, GROUPS, PIXELS
    previews = []
    for fighter_index, fighter in enumerate(('kano', 'sonya')):
        path = drafts / PNG_NAMES[fighter_index]
        png = path.read_bytes()
        if sha(png) != PNG_SHAS[fighter_index]:
            raise ValueError('Selected source PNG changed')
        sheet = Image.open(path).convert('RGBA')
        if sheet.size != (1536, 1024):
            raise ValueError('Unexpected six-cell draft sheet')
        cells, bounds = [], []
        for index in range(6):
            cell = sheet.crop(((index % 3) * 512, (index // 3) * 512,
                               (index % 3 + 1) * 512, (index // 3 + 1) * 512))
            box = cell.getchannel('A').point(lambda a: 255 if a >= 128 else 0).getbbox()
            if not box or box[0] == 0 or box[1] == 0 or box[2] == 512 or box[3] == 512:
                raise ValueError('Draft cropped at cell boundary')
            cells.append(cell.crop(box)); bounds.append(box)
        # One uniform factor for the entire fighter, not six independently
        # stretched poses: straight-leg impact matches native Liu's 131 px.
        factor = 131 / cells[5].height
        normal = palette(donor, PALETTE_RECORDS[fighter_index][0])
        alternate = palette(donor, PALETTE_RECORDS[fighter_index][1])
        groups, frames = [], []
        for phase, cell in enumerate(cells):
            size = (round(cell.width * factor), round(cell.height * factor))
            scaled = cell.resize(size, Image.Resampling.LANCZOS)
            indices = quantize(scaled, normal)
            raw = indices.tobytes()
            packed = codec.pack_indices(raw)
            if frame_at + 16 > PIXELS or group_at + 8 > FRAMES or pixel_at + len(packed) > END:
                raise ValueError('Dedicated Pit payload storage overflow')
            if GFX_DEST + pixel_at - PIXELS + len(packed) > GFX_END:
                raise ValueError('Dedicated Pit graphics storage overflow')
            # 14-byte native multipart descriptor, no embedded palette: the
            # cinematic owns the actual victim's normal/alternate palette.
            width, height = size
            left, top = X_CENTERS[phase] - width // 2, TOPS[phase]
            native_frame, native_group = address(frame_at), address(group_at)
            struct.pack_into('<4hIH', payload, frame_at, width, height, -left, -top,
                             (GFX_DEST + pixel_at - PIXELS) * 8, 0x6000)
            struct.pack_into('<2I', payload, group_at, native_frame, 0)
            payload[pixel_at:pixel_at + len(packed)] = packed
            groups.append(native_group)
            frames.append(dict(phase=phase, frame=f'{native_frame:08X}', group=f'{native_group:08X}',
                               crop=list(bounds[phase]), size=list(size), bounds=[left, top, left+width, top+height],
                               graphics_source=(GFX_DEST + pixel_at - PIXELS) * 8,
                               packed_bytes=len(packed), indices_sha256=sha(raw),
                               used_indices=sorted(set(raw))))
            previews.append((fighter, phase, decoded(indices, normal), decoded(indices, alternate)))
            frame_at += 16; group_at += 8; pixel_at = (pixel_at + len(packed) + 3) & ~3
        sequence = address(SEQUENCES[fighter_index])
        # Preserve the original MKII Pit grammar: five-frame loop, loop token
        # 1 and own stream pointer, phase separator 0, impact frame, final 0.
        words = (*groups[:5], 1, sequence, 0, groups[5], 0)
        struct.pack_into('<10I', payload, SEQUENCES[fighter_index], *words)
        table[17 + fighter_index] = sequence
        report['fighters'][fighter] = dict(id=17+fighter_index, png=str(path), png_sha256=sha(png),
                                         uniform_scale=factor, sequence=f'{sequence:08X}',
                                         sequence_words=list(words), frames=frames)
    struct.pack_into('<19I', payload, TABLE, *table)
    struct.pack_into('<4s8I', payload, HEADER, b'KPT1', PIXELS, pixel_at-PIXELS, GFX_DEST,
                     address(TABLE), address(SEQUENCES[0]), address(SEQUENCES[1]), 19, 12)
    if payload[:HEADER] != source[:HEADER] or payload[END:] != source[END:]:
        raise ValueError('Unrelated payload changed')
    report.update(pixel_bytes=pixel_at-PIXELS, payload_sha256=sha(payload),
                  payload_crc32=f'{zlib.crc32(payload):08x}', payload_sha1=hashlib.sha1(payload).hexdigest())
    output.mkdir(parents=True)
    target = output / 'roms/mk2ks/mk2ks.mdata'
    target.parent.mkdir(parents=True)
    target.write_bytes(payload)
    preview = Image.new('RGB', (6*180, 4*185), (40, 42, 48))
    draw = ImageDraw.Draw(preview)
    for fighter, phase, normal, alt in previews:
        row = 0 if fighter == 'kano' else 2
        for variant, image in enumerate((normal, alt)):
            x, y = phase*180, (row+variant)*185
            draw.text((x+3,y+3), f'{fighter} {phase} '+('normal' if variant==0 else 'alternate'), fill='white')
            preview.paste(image, (x+90-image.width//2, y+34+TOPS[phase]), image)
    preview.save(output / 'native-palette-preview.png')
    (output / 'asset-report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ('scope','pixel_bytes','payload_sha256','payload_crc32','payload_sha1')},indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    build(root, root / 'diagnostic_v595_pit_sprite_drafts', args.output)
