"""Current v786 human Babality regression; not complete finisher/release QA.

Both own performers/victims in both slots, native rejection gates, original
baby art/ground anchors/retirement and unchanged stock rendering. No audio,
all-arena/CPU certification or complete campaign inference.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import numpy as np
from PIL import Image
import verify_native_babality_performers_v739 as baba
import verify_native_fade_exclusions_v787 as fade

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    root, output = args.root.resolve(), args.output.resolve()
    fade.check(not output.exists(), 'Do not overwrite verification')
    tracked = {}
    def track(path, wanted=None):
        path = Path(path)
        actual = fade.sha(path)
        fade.check(wanted is None or actual == wanted, 'Executed/reference input changed: ' + str(path))
        tracked[str(path.resolve())] = actual
    for module in (baba, baba.v, fade):
        track(Path(module.__file__))
    track(Path(__file__))
    audio_proof = root / 'audit_v791_native_friendship_audio_checked/verification.json'
    track(audio_proof)
    current = fade.load(audio_proof)
    fade.check(current['boundedHumanFriendshipAudioAcceptance'] and current['candidate'] ==
               'diagnostic_v786_native_fighter_fade_exclusions', 'Wrong current accepted candidate')
    for path, value in current['checked_inputs'].items():
        track(path, value)
    accepted_guest = (root / 'audit_v790_kano_friendship_p1/guest_maincpu.bin').read_bytes()
    prior_path = root / 'audit_v741_native_babality_performers_checked_inputs/verification.json'
    track(prior_path)
    prior = fade.load(prior_path)
    fade.check(prior['boundedHumanBabalityAcceptance'] is True, 'Previous Babality checkpoint absent')
    def historical(path):
        wanted = prior['input_hashes'].get(str(path.resolve()))
        fade.check(wanted is not None, 'Historical baseline not pinned: ' + str(path))
        track(path, wanted)
    old_path = root / 'audit_v738_kano_babality_p1/guest_maincpu.bin'
    historical(old_path)
    old = old_path.read_bytes()
    for first, last in ((0xf9600, 0xf98a0), (fade.off(0xff87e120), fade.off(0xff880000)),
                        (0xff2c0, 0xff2c0 + 19 * 4)):
        fade.check(accepted_guest[first:last] == old[first:last], 'Original/owned Babality code changed')
    ref_path = root / 'audit_v726_original_baby_reference/reference.json'
    historical(ref_path)
    reference = fade.load(ref_path)
    for path, value in reference['input_hashes'].items():
        track(path, value.upper())
    # Recheck the original actual LK records and direction encodings, not just
    # the copied command constants in a port-side verifier.
    baba.original_reference(root)
    for name in ('audit_v734_original_babality_commands', 'audit_v735_original_babality_directions'):
        folder = root / name
        for file in ('result.json', 'run.log'):
            historical(folder / file)
        for path, value in fade.load(folder / 'result.json')['input_hashes'].items():
            track(path, value)
    reports = {}
    cases = [(winner, victim, f'{winner}_babality', side, 'positive')
             for winner, victim in (('kano', 'sonya'), ('sonya', 'kano')) for side in (1, 2)]
    cases += [(winner, victim, f'{winner}_wrong', 1, 'wrong_direction')
              for winner, victim in (('kano', 'sonya'), ('sonya', 'kano'))]
    cases += [(winner, victim, f'{winner}_punch', 2, 'punch_used')
              for winner, victim in (('kano', 'sonya'), ('sonya', 'kano'))]
    cases += [('kitana', 'liu_kang', 'stock_liu', side, 'positive') for side in (1, 2)]
    for winner, victim, label, side, command in cases:
        folder = root / f'audit_v793_{label}_p{side}'
        result = fade.load(folder / 'result.json')
        baba.provenance(result)
        fade.check(result['winner'] == winner and result['victim'] == victim and result['winner_side'] == side
                   and result['command_case'] == command and result['candidate'] == current['candidate'],
                   'Mixed current-candidate Babality metadata')
        for path, value in result['input_hashes'].items():
            track(path, value)
        for name in ('result.json', 'run.log', 'guest_maincpu.bin'):
            track(folder / name)
        fade.check((folder / 'guest_maincpu.bin').read_bytes() == accepted_guest, 'Different guest in regression')
        text = (folder / 'run.log').read_text(encoding='utf-8-sig')
        fade.check(not re.search(r'Lua error|fatal error|Error running', text, re.I), 'Runtime error')
        rows = baba.v.records(text)
        report = {'winner': winner, 'victim': victim, 'winner_side': side, 'command_case': command,
                  'native_damage': 322, 'native_wins': 2, 'checked_display_pixels': 0}
        if command == 'positive':
            baba.v.runtime_check(rows, victim, side, reference, winner_id=baba.WINNERS[winner])
            baba.command_check(rows, winner, side, command)
            if victim in baba.v.FRAMES:
                photo = ref_path.parent / f'{victim}_baby.png'
                historical(photo)
                sprite = np.asarray(Image.open(photo).convert('RGBA'))
                fade.check(hashlib.sha256(sprite.tobytes()).hexdigest() == reference['records'][victim]['rgba_sha256'],
                           'Original infant artwork changed')
                report['original_baby_pixel_checks'] = []
                for age in (160, 200, 240):
                    capture = folder / 'snap' / f'babality_{age}.png'
                    track(capture)
                    origin, count = baba.v.image_match(np.asarray(Image.open(capture).convert('RGB')), sprite)
                    report['checked_display_pixels'] += count
                    report['original_baby_pixel_checks'].append({'age': age, 'origin': origin, 'pixels': count})
            else:
                before = root / f'audit_v{738 if side == 1 else 740}_stock_liu_p{side}'
                for name in ('result.json', 'run.log', 'guest_maincpu.bin'):
                    historical(before / name)
                fade.check((before / 'guest_maincpu.bin').read_bytes() == old, 'Historical stock guest changed')
                for age in range(0, 721, 8):
                    capture = folder / 'snap' / f'babality_{age}.png'
                    baseline = before / 'snap' / capture.name
                    track(capture); historical(baseline)
                    fade.check(capture.read_bytes() == baseline.read_bytes(), 'Stock Babality frame changed')
                    report['checked_display_pixels'] += 400 * 254
                report['unchanged_stock_frames'] = 91
        else:
            baba.negative_check(rows, winner, victim, side, command)
        reports[folder.name] = report
    output.mkdir(parents=True)
    report = {'scope': __doc__, 'candidate': current['candidate'], 'cases': reports, 'checked_inputs': tracked,
              'boundedCurrentHumanBabalityRegressionAcceptance': True,
              'fullFinisherAcceptance': False, 'fullPortAcceptance': False}
    (output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'cases': len(reports), 'checked_inputs': len(tracked),
                      'original_baby_pixels': sum(v['checked_display_pixels'] for v in reports.values()
                                                   if v['victim'] != 'liu_kang'),
                      'unchanged_stock_frames': sum(v.get('unchanged_stock_frames', 0) for v in reports.values()),
                      'boundedCurrentHumanBabalityRegressionAcceptance': True,
                      'fullPortAcceptance': False}, indent=2))

if __name__ == '__main__':
    main()
