"""Bounded native Friendship palette integration, not full-port acceptance.

Requires eight genuine-input v786 runs and their pre-fix v784 controls.
Every original fade exclusion and fader byte is preserved. Body art is
checked without colour tolerances or arbitrary occlusion masks; unresolved
groups are explicitly reported rather than counted as pixel acceptance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import numpy as np
from PIL import Image
from native_babality_runtime_checks_v739 import image_match

BASE = 0xff800000
PALETTES = (0xfda00, 0xfdb00, 0xf1500, 0xf1600, 0xf59a0, 0xf5a40)
OPERANDS = (0xff80f760, 0xff80f7f0, 0xff8cdf10)

def check(value, message):
    if not value:
        raise ValueError(message)

def off(address):
    return (address - BASE) // 8

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def parse(path):
    rows = []
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        match = re.match(r'MK2_FRIEND_(\w+) (.*)', line)
        if match:
            rows.append((match[1], dict(re.findall(r'(\w+)=([^\s]+)', match[2]))))
    return rows

def select(rows, tag):
    return [r for kind, r in rows if kind == tag]

def guest_check(old, new, original):
    check(len(old) == len(new) == len(original) == 0x100000, 'Complete guest required')
    check(old[0xfa700:0xfa800] == b'\xff' * 256, 'Reserved storage already occupied')
    source = off(0xff908120)
    original_list = original[source:source + 47 * 4]
    check(old[source:source + 47 * 4] == original_list, 'Pre-fix original list changed')
    entries = struct.unpack('<47I', original_list)
    check(all(entries[:46]) and entries[-1] == 0, 'Original list boundary wrong')
    expected = bytearray(old)
    expected[0xfa700:0xfa700 + 46 * 4] = original_list[:46 * 4]
    for index, palette in enumerate(PALETTES):
        check(struct.unpack_from('<H', new, palette)[0] == (65 if index < 4 else 64),
              'Excluded pointer is not expected fighter palette')
        struct.pack_into('<I', expected, 0xfa700 + (46 + index) * 4, BASE + palette * 8)
    struct.pack_into('<I', expected, 0xfa700 + 52 * 4, 0)
    for address in OPERANDS:
        check(struct.unpack_from('<I', old, off(address))[0] == 0xff908120,
              'Original exclusion consumer changed')
        struct.pack_into('<I', expected, off(address), BASE + 0xfa700 * 8)
    check(new == expected, 'Guest changed outside exact list and three operands')
    # Explicitly retain executable native fader and 5-bit channel converter.
    for start, end in ((0xff80fbc0, 0xff8100b0), (0xff8100b0, 0xff810290)):
        check(new[off(start):off(end)] == original[off(start):off(end)], 'Native fader replaced')
    return {'changed_bytes': sum(a != b for a, b in zip(old, new)),
            'preserved_entries': 46, 'added_palette_records': [f'{BASE+p*8:08X}' for p in PALETTES],
            'rebound_operands': [f'{x:08X}' for x in OPERANDS]}

def palette_check(rows, guest, ids):
    visual = [r for r in select(rows, 'VISUAL') if 0 <= int(r['age']) <= 240]
    banks = set()
    for slot, fid in enumerate(ids, 1):
        observations = [r for r in visual if int(r['slot']) == slot]
        check([int(r['age']) for r in observations] == list(range(241)),
              'Missing/duplicated per-field fighter observations')
        pointer = BASE + PALETTES[fid - 17] * 8 if fid >= 17 else struct.unpack_from(
            '<I', guest, off(0xff907910) + fid * 4)[0]
        count = struct.unpack_from('<H', guest, off(pointer))[0]
        words = list(struct.unpack_from(f'<{count}H', guest, off(pointer) + 2))
        for row in observations:
            check(int(row['id']) == fid, 'Fighter identity changed during scene')
            actual = [int(x, 16) for x in row['colors'].split(',')]
            check(actual[:count] == words, 'Fighter palette dimmed or recoloured')
            banks.add(int(row['bank'], 16))
    fades = select(rows, 'FADE')
    check(fades and not any(int(r['bank'], 16) in banks for r in fades),
          'Native fader still scales a fighter palette')
    grouped = {}
    for row in fades:
        grouped.setdefault((row['bank'], row['source']), []).append(row)
    check(all([int(r['factor']) for r in group] == list(range(120, 47, -8))
              and [int(r['age']) for r in group] == list(range(10))
              for group in grouped.values()), 'Native scenery fade cadence changed')
    return {'fighter_fields': len(visual), 'scenery_palette_fades': len(grouped),
            'native_fade_factors': list(range(120, 47, -8))}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    root, output = args.root.resolve(), args.output.resolve()
    check(not output.exists(), 'Do not overwrite evidence')
    tracked = {}
    historical = load(root / 'audit_v785_pre_fade_exclusion_fix/snapshot_hashes.json')
    def track(path, wanted=None):
        path = Path(path)
        actual = sha(path)
        if wanted is not None and actual != wanted:
            saved = historical.get(str(path))
            check(saved is not None and saved['sha256'] == wanted, 'Changed input: ' + str(path))
            path = Path(saved['snapshot'])
            actual = sha(path)
        check(wanted is None or actual == wanted, 'Snapshot mismatch: ' + str(path))
        tracked[str(path.resolve())] = actual
    track(Path(__file__))
    import native_babality_runtime_checks_v739 as shared
    track(Path(shared.__file__))
    track(root / 'audit_v785_pre_fade_exclusion_fix/snapshot_hashes.json')
    original_path = root / 'mk2/mk2-maincpu.bin'
    track(original_path, '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23')
    original = original_path.read_bytes()
    oracle_path = root / 'audit_v756_original_friendship_art_checked/verification.json'
    track(oracle_path)
    for path, value in load(oracle_path)['checked_inputs'].items():
        track(path, value)
    ref_path = root / 'audit_v755_original_friendship_art/reference.json'
    track(ref_path)
    reference = load(ref_path)
    reports = {}
    for label, winner, fid, victim in (('kano', 'kano', 17, 18), ('sonya', 'sonya', 18, 17),
                                     ('cage', 'cage', 2, 1), ('liu', 'liu_kang', 1, 2)):
        for side in (1, 2):
            folder = root / f'audit_v786_{label}_visual_p{side}'
            old_folder = root / f'audit_v784_{label}_{"visual" if fid >= 17 else "control"}_p{side}'
            for case_folder in (folder, old_folder):
                result = load(case_folder / 'result.json')
                check(result['exit_code'] == 0 and result['winner'] == winner and result['side'] == side
                      and result['guest_writes'] == 0 and result['assistance'] == 'none'
                      and result['command_case'] == 'positive', 'Wrong/unfinished executed case')
                for path, value in result['input_hashes'].items():
                    track(path, value)
                for name in ('result.json', 'run.log', 'guest_maincpu.bin'):
                    track(case_folder / name)
            guest = (folder / 'guest_maincpu.bin').read_bytes()
            old_guest = (old_folder / 'guest_maincpu.bin').read_bytes()
            report = {'guest': guest_check(old_guest, guest, original)}
            rows, before = parse(folder / 'run.log'), parse(old_folder / 'run.log')
            check(all(r.get('writes') == '0' and r.get('assistance') == 'none' for _, r in rows),
                  'Assisted gameplay trace')
            stable = lambda items: [(kind, row) for kind, row in items if kind not in ('VISUAL', 'FADE')]
            check(stable(rows) == stable(before), 'Gameplay/scene choreography differs from pre-fix run')
            final = select(rows, 'RESULT')
            check(len(final) == 1 and final[0]['kos'] == '2' and final[0]['damage'] == '322'
                  and int(final[0]['action']) > int(final[0]['window']) > 0
                  and final[0]['cleanup'] == 'true', 'Native action or common handoff incomplete')
            ids = (fid, victim) if side == 1 else (victim, fid)
            report.update(palette_check(rows, guest, ids))
            if fid < 17:
                check(rows == before, 'Stock trace changed')
                for age in range(241):
                    photo = folder / 'snap' / f'visual_field_{age}.png'
                    old_photo = old_folder / 'snap' / photo.name
                    track(photo); track(old_photo)
                    check(photo.read_bytes() == old_photo.read_bytes(), 'Stock rendered frame changed')
                report['unchanged_stock_frames'] = 241
            else:
                report['exact_body_groups'] = []
                report['unresolved_body_groups'] = []
                poses = select(rows, 'POSE')
                for asset in reference['records'][winner]['groups']:
                    if asset['effect']:
                        continue
                    image_path = root / 'audit_v755_original_friendship_art' / asset['file']
                    track(image_path)
                    sprite = np.asarray(Image.open(image_path).convert('RGBA'))
                    candidates = [int(r['age']) for r in poses if int(r['pose'], 16) + 0x1000000 == asset['group']]
                    matched = None
                    for start in candidates:
                        for age in range(start + 1, min(start + 5, 241)):
                            photo = folder / 'snap' / f'visual_field_{age}.png'
                            track(photo)
                            actual = np.asarray(Image.open(photo).convert('RGB'))
                            for flip in (False, True):
                                try:
                                    origin, pixels = image_match(actual, sprite[:, ::-1] if flip else sprite)
                                except ValueError:
                                    continue
                                matched = {'group': f'{asset["group"]:08X}', 'age': age,
                                           'flip': flip, 'origin': origin, 'pixels': pixels}
                                break
                            if matched:
                                break
                        if matched:
                            break
                    if matched:
                        report['exact_body_groups'].append(matched)
                    else:
                        report['unresolved_body_groups'].append(f'{asset["group"]:08X}')
                report['next_screen_observed'] = select(rows, 'FIELD')[-1]['mode'] == '3' and final[0]['retired'] == 'true'
                check(report['next_screen_observed'], 'Added actor did not retire into next screen')
            reports[folder.name] = report
    output.mkdir(parents=True)
    complete_pixels = all(not case.get('unresolved_body_groups') for case in reports.values())
    report = {'scope': __doc__, 'cases': reports, 'checked_inputs': tracked,
              'boundedFriendshipFadeIntegrationAcceptance': True,
              'completeBodyPixelAcceptance': complete_pixels,
              'currentCandidateAudioAcceptance': False,
              'fullFinisherAcceptance': False, 'fullPortAcceptance': False}
    (output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'cases': len(reports), 'checked_inputs': len(tracked),
                      'boundedFriendshipFadeIntegrationAcceptance': True,
                      'completeBodyPixelAcceptance': complete_pixels,
                      'unresolved': {k: v.get('unresolved_body_groups') for k, v in reports.items()
                                     if v.get('unresolved_body_groups')}}, indent=2))

if __name__ == '__main__':
    main()
