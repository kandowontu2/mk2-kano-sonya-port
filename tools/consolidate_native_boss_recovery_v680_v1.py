"""Freeze bounded original/native boss recovery and failed diagnostic attempts."""
import json
import re
from pathlib import Path
from verify_native_boss_recovery_v680_v1 import ROOT, digest, verify


if __name__ == '__main__':
    out = ROOT / 'audit_v712_native_boss_recovery_checked_inputs'
    if out.exists(): raise ValueError('Do not overwrite evidence')
    cases = sorted(ROOT.glob('audit_v710_boss_stomp_*'))
    reports = [verify(case) for case in cases]
    if len(reports) != 6 or not all(r['passed'] for r in reports):
        raise ValueError(reports)
    for side in (1, 2):
        group = [r for r in reports if r['human_slot'] == side]
        if ({r['player'] for r in group} != {'liu_kang', 'kano', 'sonya'} or
            {(r['native_held_fields'], r['first_movement_age']) for r in group} != {(148 + side, 150 + side)}):
            raise ValueError('Actual stock comparison in both slots required')
    test = ROOT / 'audit_v710_boss_stomp_kano_p2/regressions_v1.log'
    if not re.search(r'Ran 25 tests in [\d.]+s\s+OK\s*$', test.read_text(encoding='utf-8-sig')):
        raise ValueError('Terminal regression result required')
    inputs = {}
    for case in cases:
        result = json.loads((case / 'result.json').read_text(encoding='utf-8-sig'))
        inputs.update(result['input_hashes'])
    for pattern in ('audit_v708_boss_stomp_*', 'audit_v709_boss_stomp_*', 'audit_v710_boss_stomp_*'):
        for folder in ROOT.glob(pattern):
            if not (folder / 'result.json').is_file(): raise ValueError('Nonterminal case: ' + str(folder))
            for file in folder.rglob('*'):
                if file.is_file(): inputs[str(file)] = digest(file)
    for pattern in ('mk2ks_native_boss_recovery_v680_v*.lua', 'tools/*native_boss_recovery_v680_v*.*'):
        for file in ROOT.glob(pattern):
            if file.is_file(): inputs[str(file)] = digest(file)
    for name in ('STATUS_2026-10-02_NATIVE_BOSS_RECOVERY.md',
                 'audit_v684_pit_guest_rom_integrity/diagnostic_v680_native_pit_initial_cache/guest_maincpu.bin',
                 'audit_v707_native_campaign_photos_checked_inputs/verification.json'):
        file = ROOT / name; inputs[str(file)] = digest(file)
    out.mkdir()
    report = dict(passed=True, cases=reports, regression_tests=25, inputHashes=inputs,
                  prior_checkpoint_underlying_files_rechecked_here=False,
                  gameplay_changed=False, release_promoted=False, unassisted_clear_proven=False,
                  fullPortAcceptance=False, scope='Native first Kintaro stomp recovery parity with stock, not a cleared tower')
    (out / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(passed=True, cases=6, tests=25, pinned_inputs=len(inputs), fullPortAcceptance=False), indent=2))
