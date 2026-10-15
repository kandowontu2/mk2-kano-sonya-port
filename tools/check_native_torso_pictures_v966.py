"""Match actual presented PNGs to encoded section pixels; no image edits."""
import json
import re
import struct
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.signal import correlate
import build_native_torso_art_v956 as assets
import build_native_death_art_v900 as death

ROOT = assets.ROOT


def check_case(case, version, payload, records):
    directory = ROOT / case
    result = json.loads((directory / 'result.json').read_text(encoding='utf-8-sig'))
    name = result['player']
    report = json.loads((ROOT / 'audit_v956_owned_torso_grounding_encoding/report.json').read_text())
    poses = report['fighters'][name]['poses']
    by_source = {int(c['graphics'], 16): p for p in poses for c in p['components']}
    text = (directory / 'run.log').read_text(encoding='utf-8-sig')
    rows = records(text, f'MK2_CAGE_TORSO_V{version}')
    snapshots = [r for tag, r in rows if tag == 'POSE_SNAPSHOT' and int(r['source'], 16) in by_source]
    dmas = [r for tag, r in rows if tag == 'DMA']
    palette_dumps = {int(r['source'], 16): directory / r['file'] for tag, r in rows if tag == 'PALETTE_DUMP'}
    results = []
    for snap in snapshots:
        source = int(snap['source'], 16)
        pose = by_source[source]
        parts = []
        for component in pose['components']:
            w, h = component['size']
            at = assets.PIXELS + int(component['graphics'], 16) // 8 - assets.GFX
            raw = death.unpack(payload[at:at + (w * h * 6 + 7) // 8], w * h)
            parts.append(np.frombuffer(raw, dtype=np.uint8).reshape(h, w))
        indices = np.concatenate(parts, axis=1)
        first = next(r for r in dmas if r['frame'] == snap['queued_frame'] and r['source'] == snap['source'])
        if int(first['command'], 16) & 16:
            indices = indices[:, ::-1]
        palette = np.array(struct.unpack('<64I', palette_dumps[source].read_bytes()), dtype=np.uint32)
        template = palette[indices]
        # Black/grayscale scenery is not evidence of the fighter. Match
        # exact chromatic body/costume/blood hardware pens, not luminance.
        red, green, blue = template >> 16, template >> 8 & 255, template & 255
        maximum, minimum = np.maximum.reduce([red, green, blue]), np.minimum.reduce([red, green, blue])
        meaningful = (indices > 0) & (maximum > 40) & (maximum - minimum > 10)
        path = directory / 'snap' / f"torso_pose_{snap['actor_pose']}_{snap['frame']}.png"
        picture = np.asarray(Image.open(path).convert('RGB'), dtype=np.uint32)
        actual = picture[:, :, 0] << 16 | picture[:, :, 1] << 8 | picture[:, :, 2]
        matches = np.zeros((actual.shape[0] - template.shape[0] + 1, actual.shape[1] - template.shape[1] + 1))
        for rgb in np.unique(template[meaningful]):
            mask = meaningful & (template == rgb)
            matches += correlate((actual == rgb).astype(float), mask.astype(float), mode='valid', method='fft')
        y, x = np.unravel_index(np.argmax(matches), matches.shape)
        count = int(meaningful.sum())
        score = float(matches[y, x]) / count
        results.append(dict(pose=pose['pose'], source=f'{source:08X}', score=score,
                            exactChromaticPixels=round(float(matches[y, x])), encodedChromaticPixels=count,
                            pictureX=int(x), pictureY=int(y), snapshot=str(path)))
    return results


if __name__ == '__main__':
    import argparse
    import verify_native_torso_art_v964 as proof
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', type=int, default=963)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('Preserve actual picture evidence')
    payload = (ROOT / 'diagnostic_v958_owned_cage_torso_grounding/roms/mk2ks/mk2ks.mdata').read_bytes()
    report = {}
    for name in ('kano', 'sonya'):
        for side in (1, 2):
            case = f'audit_v{args.version}_cage_{name}_p{side}_owned_torso'
            report[case] = check_case(case, args.version, payload, proof.records)
    scores = [r['score'] for rows in report.values() for r in rows]
    args.output.mkdir()
    accepted = len(scores) == 24 and min(scores) >= 0.5
    (args.output / 'pixel-matches.json').write_text(json.dumps(dict(passed=accepted, minimumMatch=min(scores), cases=report), indent=2) + '\n')
    print(json.dumps(dict(passed=accepted, minimumMatch=min(scores), scores=[[round(r['score'], 3) for r in rows] for rows in report.values()])))
    raise SystemExit(0 if accepted else 1)
