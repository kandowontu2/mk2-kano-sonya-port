"""Supplement v787 with unobscured physical Sonya poses and stock teardown.

Native positive human Friendships in one arena at two physical distances.
Not negative-command, CPU, alternate/frozen runtime, audio or full-port QA.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from PIL import Image
import verify_native_fade_exclusions_v787 as fade
import verify_native_friendship_dispatch_v778 as dispatch

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    root, output = args.root.resolve(), args.output.resolve()
    fade.check(not output.exists(), 'Do not overwrite evidence')
    tracked = {}
    def track(path, wanted=None):
        path = Path(path)
        actual = fade.sha(path)
        fade.check(wanted is None or actual == wanted, 'Executed input changed: ' + str(path))
        tracked[str(path.resolve())] = actual
    for module in (fade, dispatch):
        track(Path(module.__file__))
    track(Path(__file__))
    track(root / 'tools/test_native_fade_exclusions_v787.py')
    unit_log = root / 'audit_v787_native_fade_units/unit-tests.log'
    track(unit_log)
    unit_text = unit_log.read_text(encoding='utf-8-sig')
    fade.check('Ran 18 tests' in unit_text and unit_text.rstrip().endswith('OK'), 'Unit checks did not pass')
    base_path = root / 'audit_v787_native_fade_exclusions_checked/verification.json'
    track(base_path)
    base = fade.load(base_path)
    fade.check(base['boundedFriendshipFadeIntegrationAcceptance'] is True,
               'Underlying eight-case fade integration not accepted')
    for path, value in base['checked_inputs'].items():
        track(path, value)
    original = (root / 'mk2/mk2-maincpu.bin').read_bytes()
    old = (root / 'audit_v784_kano_visual_p1/guest_maincpu.bin').read_bytes()
    reference = fade.load(root / 'audit_v755_original_friendship_art/reference.json')
    reports = {}
    cases = [('sonya', 2, 'audit_v788_sonya_gap140_p2', 140, 720)]
    cases += [(name, side, f'audit_v788_{label}_extended_p{side}', 160, 1600)
              for label, name in (('cage', 'cage'), ('liu', 'liu_kang')) for side in (1, 2)]
    for winner, side, folder_name, gap, observation in cases:
        folder = root / folder_name
        result = fade.load(folder / 'result.json')
        fade.check(result['exit_code'] == 0 and result['winner'] == winner and result['side'] == side
                   and result['requested_gap'] == gap and result['observation'] == observation
                   and result['guest_writes'] == 0 and result['assistance'] == 'none'
                   and result['command_case'] == 'positive', 'Wrong/incomplete supplemental run')
        for path, value in result['input_hashes'].items():
            track(path, value)
        for name in ('result.json', 'run.log', 'guest_maincpu.bin'):
            track(folder / name)
        rows = fade.parse(folder / 'run.log')
        fade.check(all(r['writes'] == '0' and r['assistance'] == 'none' for _, r in rows), 'Assisted run')
        boot = fade.select(rows, 'BOOT')
        final = fade.select(rows, 'RESULT')
        fade.check(len(boot) == len(final) == 1 and boot[0]['requested_gap'] == str(gap)
                   and boot[0]['observation'] == str(observation), 'Wrong harness boot/terminal')
        positions = fade.select(rows, 'COMMAND_POSITION')
        fade.check(len(positions) == 1 and gap <= int(positions[0]['gap']) < gap + 6,
                   'Actual physical command distance differs from requested distance')
        guest = (folder / 'guest_maincpu.bin').read_bytes()
        report = {'guest': fade.guest_check(old, guest, original)}
        fid, victim = {'sonya': (18, 17), 'cage': (2, 1), 'liu_kang': (1, 2)}[winner]
        report.update(fade.palette_check(rows, guest, (fid, victim) if side == 1 else (victim, fid)))
        if winner == 'sonya':
            report['native_dispatch'] = dispatch.runtime(rows, winner, side, 'positive')
            poses = fade.select(rows, 'POSE')
            report['exact_body_groups'] = []
            for asset in reference['records']['sonya']['groups']:
                fade.check(not asset['effect'], 'Unexpected Sonya group type')
                image_path = root / 'audit_v755_original_friendship_art' / asset['file']
                track(image_path)
                sprite = np.asarray(Image.open(image_path).convert('RGBA'))
                matched = None
                starts = [int(r['age']) for r in poses if int(r['pose'], 16) + 0x1000000 == asset['group']]
                for start in starts:
                    for age in range(start + 1, min(start + 5, 241)):
                        photo = folder / 'snap' / f'visual_field_{age}.png'
                        track(photo)
                        actual = np.asarray(Image.open(photo).convert('RGB'))
                        for flip in (False, True):
                            try:
                                origin, pixels = fade.image_match(actual, sprite[:, ::-1] if flip else sprite)
                            except ValueError:
                                continue
                            matched = {'group': f'{asset["group"]:08X}', 'age': age,
                                       'flip': flip, 'origin': origin, 'pixels': pixels}
                            break
                        if matched:
                            break
                    if matched:
                        break
                fade.check(matched is not None, 'Unobscured Sonya pixels do not match: ' + hex(asset['group']))
                report['exact_body_groups'].append(matched)
            fade.check(len(report['exact_body_groups']) == 11, 'Missing original Sonya group')
            report['native_physical_gap'] = int(positions[0]['gap'])
        else:
            base_folder = root / f'audit_v786_{"liu" if winner == "liu_kang" else winner}_visual_p{side}'
            before = fade.parse(base_folder / 'run.log')
            window = int(fade.select(rows, 'WINDOW')[0]['frame'])
            normalize = lambda items: [(kind, {k: v for k, v in row.items() if k not in ('requested_gap', 'observation')})
                                       for kind, row in items if kind != 'RESULT' and int(row['frame']) <= window + 720]
            fade.check(normalize(rows) == normalize(before), 'Stock gameplay before extended observation changed')
            damage = fade.select(rows, 'DAMAGE')
            fade.check(sum(int(r['before']) - int(r['after']) for r in damage) == 322
                       and sum(r['after'] == '0' for r in damage) == 2
                       and all(r['pc'] == 'FF836700' for r in damage), 'Stock control lacked genuine KOs')
            fade.check(final[0]['kos'] == '2' and int(final[0]['action']) > window
                       and final[0]['cleanup'] == 'true' and final[0]['retired'] == 'true',
                       'Stock action/common handoff/retirement incomplete')
            last = fade.select(rows, 'FIELD')[-1]
            fade.check(last['age'] == str(observation) and last['mode'] == '3' and last['ids'] == '-1,-1',
                       'Stock scene did not reach next screen')
            # Capture proof that the next-screen render is no longer the Friendship frame.
            scene_photo = folder / 'snap/visual_field_100.png'
            next_photo = folder / 'snap' / f'friendship_{observation}.png'
            track(scene_photo); track(next_photo)
            fade.check(scene_photo.read_bytes() != next_photo.read_bytes(), 'Next-screen image did not change')
            report['stock_next_screen_observed'] = True
            report['observed_window_fields'] = observation
        reports[folder_name] = report
    groups = {}
    for name in ('kano', 'sonya'):
        wanted = {f'{g["group"]:08X}' for g in reference['records'][name]['groups'] if not g['effect']}
        for side in (1, 2):
            key = f'audit_v786_{name}_visual_p{side}'
            actual = {r['group'] for r in base['cases'][key]['exact_body_groups']}
            if name == 'sonya' and side == 2:
                actual |= {r['group'] for r in reports['audit_v788_sonya_gap140_p2']['exact_body_groups']}
            fade.check(actual == wanted, 'Incomplete original body coverage across slots')
            groups[f'{name}_p{side}'] = len(actual)
    output.mkdir(parents=True)
    report = {'scope': __doc__, 'cases': reports, 'checked_inputs': tracked,
              'body_groups_by_character_slot': groups,
              'boundedFriendshipFadeIntegrationAcceptance': True,
              'allOriginalBodyGroupsBothSlotsPixelAcceptance': True,
              'stockFriendshipNextScreenBothSlotsAcceptance': True,
              'currentCandidateAudioAcceptance': False,
              'fullFinisherAcceptance': False, 'fullPortAcceptance': False}
    (output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('body_groups_by_character_slot',
        'allOriginalBodyGroupsBothSlotsPixelAcceptance', 'stockFriendshipNextScreenBothSlotsAcceptance',
        'fullFinisherAcceptance', 'fullPortAcceptance')}, indent=2))

if __name__ == '__main__':
    main()
