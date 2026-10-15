"""Blood-only index conversion using immutable imagegen semantic guides."""
import hashlib
import json
import struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import build_native_arm_rip_v1043 as original
import build_native_torso_art_v977 as blood
import build_native_pit_fall_v2 as colors
import build_native_projectile_impacts as codec
import verify_rolling_heads_v1014 as decode

ROOT = original.ROOT
OUT = ROOT / 'audit_v1060_owned_arm_blood_encoding'
SOURCE = ROOT / 'diagnostic_v1048_owned_jax_arm_tables/roms/mk2ks/mk2ks.mdata'
GUIDES = {'body': 'FD289A6D7651D99567EA887EB6C2C0402B33049505EE274BA9997A6430351F41',
          'arms': 'F2EB1BFAD9AED27624E44DBFDC89866FDEE8198E306FD5761F32970AD08C5EFE'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main():
    if OUT.exists():
        raise ValueError('Preserve encoding evidence')
    assert digest(SOURCE) == 'F6069CBEE72DFF4D31FAD244365F7711B59E904AB2AFC852F0D9A4F51934A562'
    source = SOURCE.read_bytes()
    payload = bytearray(source)
    donor = (ROOT / 'mk3/mk3-maincpu.bin').read_bytes()
    normal, alternate = (colors.palette(donor, at) for at in (0x92bbc, 0x92c3e))
    metadata_path = ROOT / 'audit_v1043_owned_arm_rip_encoding/report.json'
    metadata = json.loads(metadata_path.read_text())
    pins = {str(SOURCE): digest(SOURCE), str(metadata_path): digest(metadata_path),
            str(ROOT / 'mk3/mk3-maincpu.bin'): digest(ROOT / 'mk3/mk3-maincpu.bin')}
    for path in (ROOT / 'art_native_arm_blood_v1059').iterdir():
        if path.is_file():
            pins[str(path)] = digest(path)
    OUT.mkdir()
    preview = Image.new('RGBA', (1000, 720), (35, 35, 40, 255))
    draw = ImageDraw.Draw(preview)
    records, spans = [], []
    for kind in ('body', 'arms'):
        source_path = ROOT / f'art_native_arm_rip_v1041/kano-{kind}-five.png'
        guide_path = ROOT / f'art_native_arm_blood_v1059/kano-{kind}-blood-guide.png'
        assert digest(guide_path) == GUIDES[kind]
        sheet, guide = (Image.open(path).convert('RGBA') for path in (source_path, guide_path))
        assert sheet.size == guide.size == (1774, 887)
        assert sheet.getextrema()[3] == guide.getextrema()[3] == (0, 255)
        pins[str(source_path)] = digest(source_path)
        xs = np.flatnonzero((np.asarray(sheet)[:, :, 3] >= 128).any(axis=0))
        runs = np.split(xs, np.flatnonzero(np.diff(xs) > 25) + 1)
        assert len(runs) == 5
        for pose in range(5):
            record = next(row for row in metadata['fighters']['kano']['poses']
                          if row['kind'] == kind and row['pose'] == pose)
            image, box = original.crop(sheet, pose)
            x0 = int(runs[pose][0]) - 3
            global_box = (x0 + box[0], box[1], x0 + box[2], box[3])
            coded = guide.crop(global_box)
            scaled = image.resize(tuple(record['size']), Image.Resampling.LANCZOS)
            coded = coded.resize(tuple(record['size']), Image.Resampling.LANCZOS)
            indices, mask, base = blood.quantize_blood(scaled, coded, normal, alternate)
            if kind == 'body' and pose == 0:
                assert not mask.any(), 'Intact arms must not receive blood correction'
            else:
                assert int(mask.sum()) >= 8, 'Each actual wound must be classified'
            assert np.array_equal(indices[~mask], base[~mask])
            assert np.array_equal(indices == 0, base == 0)
            assert set(np.unique(indices[mask])).issubset(blood.BLOOD_PENS)
            assert np.array_equal(normal[list(blood.BLOOD_PENS)], alternate[list(blood.BLOOD_PENS)])
            width = indices.shape[1]
            count = len(record['components'])
            changed = 0
            for column, component in enumerate(record['components']):
                left, right = column * width // count, (column + 1) * width // count
                old = decode.decode(source[component['pixelOffset']:component['pixelOffset'] + component['packedBytes']],
                                    component['size'][0] * component['size'][1]).reshape(tuple(reversed(component['size'])))
                assert np.array_equal(old, base[:, left:right]), 'Original indices reconstructed from unchanged sprites'
                tile = indices[:, left:right]
                packed = codec.pack_indices(tile.tobytes())
                assert len(packed) == component['packedBytes']
                at = component['pixelOffset']
                payload[at:at + len(packed)] = packed
                spans.append((at, at + len(packed)))
                changed += int(np.count_nonzero(old != tile))
            assert changed > 0 or kind == 'body' and pose == 0
            records.append({'kind': kind, 'pose': pose, 'bloodPixels': int(mask.sum()),
                            'changedIndices': changed, 'nonbloodIndicesUnchanged': True,
                            'originalAlphaUnchanged': True, 'sourceBox': list(global_box)})
            for costume, palette in enumerate((normal, alternate)):
                native = colors.decoded(indices, palette)
                native.save(OUT / f'kano-{kind}-{pose}-{("normal", "alternate")[costume]}.png')
                row = (0 if kind == 'body' else 2) + costume
                x, y = pose * 200, row * 180
                draw.text((x + 2, y + 2), f'Kano {kind}{pose} {("normal", "alternate")[costume]}', fill='white')
                preview.alpha_composite(native, (x + (200 - native.width) // 2, y + 175 - native.height))
    changed_bytes = [i for i, (a, b) in enumerate(zip(source, payload)) if a != b]
    assert changed_bytes and all(any(lo <= i < hi for lo, hi in spans) for i in changed_bytes)
    # Every descriptor, position, stream, palette, Sonya component and every
    # other move asset remains byte-identical. No new CPU code is installed.
    assert payload[0x1c3000:0x1c3800] == source[0x1c3000:0x1c3800]
    out = OUT / 'roms/mk2ks/mk2ks.mdata'
    out.parent.mkdir(parents=True)
    out.write_bytes(payload)
    preview.save(OUT / 'kano-normal-alternate-blood.png')
    report = {'scope': 'Kano arm-rip blood indices only; native runtime still unverified',
              'sourceSHA256': digest(SOURCE), 'payloadSHA256': digest(out), 'inputHashes': pins,
              'guides': GUIDES, 'bloodPens': list(blood.BLOOD_PENS), 'poses': records,
              'changedPackedBytes': len(changed_bytes), 'changedIndices': sum(r['changedIndices'] for r in records),
              'bloodPixels': sum(r['bloodPixels'] for r in records),
              'nativeDescriptorsStreamsPositionsAndPalettesUnchanged': True,
              'sonyaAndEveryOtherMoveAssetUnchanged': True,
              'runtimeAccepted': False, 'naturalAlternateSelectionAccepted': False,
              'fullPortAccepted': False}
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('inputHashes', 'poses')}, indent=2))


if __name__ == '__main__':
    main()
