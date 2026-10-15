"""Freeze verified v786 visual/audio/Babality gates and current unit evidence.

This is a bounded regression checkpoint, explicitly not release acceptance.
"""
import argparse
import hashlib
import json
from pathlib import Path

def check(value, message):
    if not value:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    root, output = args.root.resolve(), args.output.resolve()
    check(not output.exists(), 'Do not overwrite checkpoint')
    tracked, gates = {}, {}
    def track(path, wanted=None):
        path = Path(path)
        actual = sha(path)
        check(wanted is None or actual == wanted, 'Checked input changed: ' + str(path))
        tracked[str(path.resolve())] = actual
    track(Path(__file__))
    for name, field in (
        ('audit_v789_friendship_visual_supplement_checked', 'allOriginalBodyGroupsBothSlotsPixelAcceptance'),
        ('audit_v791_native_friendship_audio_checked', 'boundedHumanFriendshipAudioAcceptance'),
        ('audit_v794_current_babality_regression_checked', 'boundedCurrentHumanBabalityRegressionAcceptance'),
    ):
        path = root / name / 'verification.json'
        track(path)
        proof = load(path)
        check(proof[field] is True and proof['fullPortAcceptance'] is False
              and proof['fullFinisherAcceptance'] is False, 'Wrong acceptance scope')
        for source, value in proof['checked_inputs'].items():
            track(source, value)
        gates[name] = {'gate': field, 'accepted': True, 'verification_sha256': sha(path)}
    for tool, folder, count in (
        ('test_native_friendship_audio_v792.py', 'audit_v792_native_friendship_audio_units', 22),
        ('test_current_babality_runtime_v795.py', 'audit_v795_current_babality_runtime_units', 7),
    ):
        track(root / 'tools' / tool)
        log = root / folder / 'unit-tests.log'
        track(log)
        text = log.read_text(encoding='utf-8-sig')
        check(f'Ran {count} tests' in text and text.rstrip().endswith('OK'), 'Unit log did not pass')
        gates[folder] = {'test_methods': count, 'passed': True, 'log_sha256': sha(log)}
    candidate = root / 'diagnostic_v786_native_fighter_fade_exclusions'
    build = load(candidate / 'build-info.json')
    track(candidate / 'build-info.json')
    track(candidate / 'mkport_candidate.exe', build['executable_sha256'])
    track(candidate / 'roms/mk2ks/mk2ks.mdata', build['payload_sha256'])
    for path, value in build['input_hashes'].items():
        track(path, value)
    track(root / 'PLAY_LATEST_TEST_BUILD.cmd', '54C83F280033AC81D7FC62E402879F8674F2927A65A517E6FF555BD9D1214784')
    track(root / 'mame-mkp/mkport.exe', '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891')
    output.mkdir(parents=True)
    report = {'scope': __doc__, 'candidate': candidate.name, 'gates': gates, 'checked_inputs': tracked,
              'checked_input_count': len(tracked), 'executable_sha256': build['executable_sha256'],
              'payload_sha256': build['payload_sha256'], 'latest_test_cmd_unchanged': True,
              'fullFinisherAcceptance': False, 'fullPortAcceptance': False,
              'remaining': ['broader finisher inputs/distances/arenas/CPU and alternate/frozen runtime',
                            'current-candidate fatalities and stage finishers',
                            'selection/ladder/names/floor shadows/moves/interruptions/secret stages',
                            'complete unassisted towers/bosses/continues/endings',
                            'final whole-port regression and matching launcher/release ZIP']}
    (output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'candidate': candidate.name, 'checked_input_count': len(tracked),
                      'accepted_bounded_gates': len(gates), 'fullPortAcceptance': False}, indent=2))

if __name__ == '__main__':
    main()
