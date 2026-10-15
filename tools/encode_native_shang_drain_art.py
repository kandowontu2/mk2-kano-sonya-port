"""Encode selected shrinking-victim drafts, without painting or game writes.

Only alpha isolation, uniform per-pose downsampling, owned-palette quantization
and six-bit packing occur here. Original drafts stay immutable. This is asset
format qualification, NOT native choreography/artwork or whole-port acceptance.
"""
import hashlib
import json
import struct
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import build_native_pit_fall_v2 as palettes
import build_native_projectile_impacts as codec
import build_native_death_art_v900 as independent

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'art_native_shang_drain_encoded_v1'
DRAFTS = ROOT / 'art_native_shang_drain'
GFX_START, GFX_LIMIT = 0x1fb0000, 0x1fc0000
HEIGHTS = (125, 119, 113)
BOTTOMS = (139, 140)
ASSETS = (
    ('kano', '911755BFFE92E49E620DBEAC1ED3E821B7107DFB48C96FB59ACBAC5801971152'),
    ('sonya', 'E159587A7FE975097C2DF7F0F4628C020AD5DCE91C3AF5F2C1D20F4A0E7A9376'),
)


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def need(value, reason):
    if not value:
        raise ValueError(reason)


def encode(sheet, colors, fighter):
    need(sheet.mode == 'RGBA' and sheet.size == (1536, 1024), 'Exact transparent draft canvas')
    output, rows, images = bytearray(), [], []
    for phase, target_height in enumerate(HEIGHTS):
        cell = sheet.crop((phase * 512, 0, (phase + 1) * 512, 1024))
        mask = cell.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
        bounds = mask.getbbox()
        need(bounds and 0 < bounds[0] < bounds[2] < 512 and
             0 < bounds[1] < bounds[3] < 1024, 'Full silhouette inside its own cell')
        crop = cell.crop(bounds)
        factor = target_height / crop.height
        width = round(crop.width * factor)
        need(20 <= width <= 80, 'Native-sized character silhouette')
        # Pillow RGBA resampling is alpha-premultiplied. Invisible background
        # colours do not turn into a glow; pen zero stays transparent.
        scaled = crop.resize((width, target_height), Image.Resampling.LANCZOS)
        indices = palettes.quantize(scaled, colors)
        need(indices.dtype == np.uint8 and 0 < np.max(indices) < 64, 'Six-bit owned opaque pens')
        need(np.array_equal(indices != 0, np.asarray(scaled)[:, :, 3] >= 128),
             'Every native transparent pixel follows the unchanged draft alpha')
        raw = indices.tobytes()
        packed = codec.pack_indices(raw)
        need(independent.unpack(packed, len(raw)) == raw, 'Independent scalar six-bit round trip')
        offset = len(output)
        output.extend(packed)
        output.extend(bytes((-len(output)) % 4))
        # Centre the common planted-foot midpoint, not the changing full-body
        # box. The original stock skeleton/finish handoff remains separate.
        feet = np.where(indices[-3:, :] != 0)[1]
        need(len(feet) > 3, 'Visible planted feet at the native bottom')
        foot_center = round((int(feet.min()) + int(feet.max())) / 2)
        left = -foot_center
        top = BOTTOMS[fighter] - target_height
        rows.append(dict(phase=phase, crop=list(bounds), uniformScale=factor,
                         width=width, height=target_height, xOffset=-left, yOffset=-top,
                         bounds=[left, top, left + width, top + target_height],
                         plantedFootCenter=foot_center, bottom=BOTTOMS[fighter],
                         graphicsSourceBits=(GFX_START + offset) * 8,
                         packedOffset=offset, packedBytes=len(packed),
                         opaquePixels=int(np.count_nonzero(indices)),
                         usedPens=sorted(int(v) for v in np.unique(indices)),
                         indicesSHA256=sha(raw), packedSHA256=sha(packed)))
        images.append((indices, scaled))
    return output, rows, images


def main():
    need(not OUT.exists(), 'Never overwrite executed asset evidence')
    donor_path = ROOT / 'mk3/mk3-maincpu.bin'
    donor = donor_path.read_bytes()
    need(sha(donor) == '1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651',
         'Original owned normal/alternate palette input')
    paths = [Path(__file__), donor_path, DRAFTS / 'prompts.json',
             ROOT / 'art_reference_native_shang_drain/reference.json',
             ROOT / 'source_native_paired_stumble_table/midtunit_m.cpp',
             ROOT / 'tools/native_shang_owned_reaction.inc',
             Path(palettes.__file__), Path(codec.__file__), Path(independent.__file__)]
    pins = {str(p.resolve()): sha(p.read_bytes()) for p in paths}
    pixel_data, fighters, previews = bytearray(), [], []
    for fighter, (name, expected_hash) in enumerate(ASSETS):
        path = DRAFTS / (name + '-drain-draft-v1.png')
        need(sha(path.read_bytes()) == expected_hash, 'Selected immutable generated atlas')
        pins[str(path)] = expected_hash
        normal = palettes.palette(donor, palettes.PALETTE_RECORDS[fighter][0])
        alternate = palettes.palette(donor, palettes.PALETTE_RECORDS[fighter][1])
        encoded, rows, images = encode(Image.open(path), normal, fighter)
        base = len(pixel_data)
        for row in rows:
            row['packedOffset'] += base
            row['graphicsSourceBits'] += base * 8
        pixel_data.extend(encoded)
        fighters.append(dict(name=name, trueIdentity=17 + fighter, draftSHA256=expected_hash,
                             normalPaletteSource=palettes.PALETTE_RECORDS[fighter][0],
                             alternatePaletteSource=palettes.PALETTE_RECORDS[fighter][1],
                             frames=rows))
        previews.append((name, normal, alternate, images))
    need(GFX_START + len(pixel_data) <= GFX_LIMIT, 'Bounded proposed native graphics allocation')
    # Review at actual 1x and enlarged NEAREST 3x, in BOTH costumes. This is
    # an authoring contact sheet, never labelled an emulator screenshot.
    preview = Image.new('RGB', (900, 740), (34, 35, 41))
    draw = ImageDraw.Draw(preview)
    for fighter, (name, normal, alternate, images) in enumerate(previews):
        for variant, colors in enumerate((normal, alternate)):
            row_y = (fighter * 2 + variant) * 185
            for phase, (indices, _) in enumerate(images):
                im = palettes.decoded(indices, colors)
                x = phase * 300
                draw.text((x + 7, row_y + 5), f'{name} phase {phase+1} ' +
                          ('normal' if variant == 0 else 'alternate') + ' - authoring only', fill='white')
                draw.text((x + 7, row_y + 20), f'Native {im.width}x{im.height}; 1x', fill='white')
                preview.paste(im, (x + 15, row_y + 172 - im.height), im)
    enlarged_preview = Image.new('RGB', (900, 1720), (34, 35, 41))
    larger_draw = ImageDraw.Draw(enlarged_preview)
    for fighter, (name, normal, alternate, images) in enumerate(previews):
        for variant, colors in enumerate((normal, alternate)):
            y = (fighter * 2 + variant) * 430
            for phase, (indices, _) in enumerate(images):
                im = palettes.decoded(indices, colors)
                im = im.resize((im.width * 3, im.height * 3), Image.Resampling.NEAREST)
                x = phase * 300
                larger_draw.text((x + 7, y + 8), f'{name} phase {phase+1}; ' +
                                 ('normal' if variant == 0 else 'alternate') + '; 3x authoring', fill='white')
                enlarged_preview.paste(im, (x + 70, y + 410 - im.height), im)
    need(all(sha(Path(p).read_bytes()) == h for p, h in pins.items()), 'All source/draft inputs conserved')
    OUT.mkdir()
    packed_path = OUT / 'drain-six-bit.bin'
    packed_path.write_bytes(pixel_data)
    preview.save(OUT / 'native-size-preview.png')
    enlarged_preview.save(OUT / 'native-size-preview-3x.png')
    output_hashes = {str(p): sha(p.read_bytes()) for p in OUT.iterdir()}
    report = dict(passed=True, scope=__doc__, sourceOnlyAccepted=True, formatRoundTrips=6,
                  graphicsStart=GFX_START, graphicsLimit=GFX_LIMIT, pixelBytes=len(pixel_data),
                  packedSHA256=sha(pixel_data), alphaCutoff=128,
                  palettePolicy='owned normal semantic pens 1..63; native alternate uses same pens',
                  anchorPolicy='same owned body bottoms 139/140; planted-foot midpoint centred',
                  graphicsReservationStillNeedsWholeInitializerCheck=True,
                  primaryAndSecondaryRuntimeTablesStillUnrepaired=True,
                  nativeRepairAccepted=False, artworkRuntimeAccepted=False,
                  fullPortAcceptance=False, gameWrites=0, newEmulatorBuilds=0,
                  newROMCopies=0, newRawGameplayMedia=0, newZIPs=0, publicPlayableChanged=False,
                  previousGoalTurnClassification='no progress: requested status only',
                  thisGoalTurnClassification='progress: six owned shrinking poses encoded and independently round-trip checked',
                  fighters=fighters, inputHashes=pins, outputHashes=output_hashes, goalStatus='active')
    (OUT / 'asset-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(passed=True, pixelBytes=len(pixel_data),
                         packedSHA256=report['packedSHA256'], nativeRepairAccepted=False,
                         fullPortAcceptance=False, output=str(OUT))))


if __name__ == '__main__':
    main()
