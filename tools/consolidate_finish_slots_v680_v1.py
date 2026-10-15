"""Pin the bounded both-slot finish proof while preserving all prior evidence."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def need(ok, label):
    if not ok:
        raise ValueError(label)


def digest(path):
    hasher = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            hasher.update(block)
    return hasher.hexdigest().upper()


def checked(inputs, records):
    for name, sha in records.items():
        path = Path(name)
        need(digest(path) == sha.upper(), 'Verified input changed: ' + name)
        need(name not in inputs or inputs[name] == sha.upper(), 'Checkpoint conflict: '+name)
        inputs[name] = sha.upper()


if __name__ == '__main__':
    out = ROOT/'audit_v704_finish_slots_checked_inputs'
    need(not out.exists(), 'Do not overwrite evidence')
    report_path = ROOT/'audit_v695_finish_p1_sonya_mirror/verification_v11.json'
    proof = json.loads(report_path.read_text(encoding='utf-8-sig'))
    need(proof['passed'] and not proof['fullPortAcceptance'], 'Bounded current v11 report')
    cases = proof['cases']
    expected = {
        'audit_v693_finish_p2_kano_sonya': (2, [18,17]),
        'audit_v693_finish_p2_sonya_raiden': (2, [7,18]),
        'audit_v694_finish_p2_kano_subzero': (2, [8,17]),
        'audit_v694_finish_p2_sonya_mirror': (2, [18,18]),
        'audit_v695_finish_p1_kano_subzero': (1, [17,8]),
        'audit_v695_finish_p1_sonya_mirror': (1, [18,18]),
    }
    need(set(cases) == set(expected), 'Exact six declared cases')
    inputs = {}
    checked(inputs, proof['inputHashes'])
    prior_path = ROOT/'audit_v692_finish_display_checked_inputs/verification.json'
    prior = json.loads(prior_path.read_text(encoding='utf-8-sig'))
    need(prior['passed'] and not prior['fullPortAcceptance'], 'Prior bounded checkpoint')
    checked(inputs, prior['inputHashes'])
    for name, (side, ids) in expected.items():
        case = cases[name]
        result = json.loads((ROOT/name/'result.json').read_text(encoding='utf-8-sig'))
        need(case['passed'] and case['human_slot'] == side and case['ids'] == ids and
             case['replayed']['frames'] == 224 and len(case['held_transition_scanout']) == 5 and
             not case['fatalityAcceptance'] and not case['fullPortAcceptance'], 'Case contract: '+name)
        need(result['passed'] and result['human_slot'] == side and result['assistance'] == 'none' and
             not result['cheats_enabled'] and result['exit_code'] == 0, 'Actual terminal capture: '+name)
        checked(inputs, result['input_hashes'])
    regression = ROOT/'audit_v696_finish_slots_regressions/regression_v2.log'
    text = regression.read_text(encoding='utf-8-sig')
    need(re.search(r'Ran 25 tests in [\d.]+s\s+OK\s*$',text) and 'FAILED' not in text,
         'All 25 tests must be terminal')
    palette_entries = sum(c['palette']['checked_palette_entries'] for c in cases.values())
    need(palette_entries == 35008, 'Exact applicable original/own palette entries')
    for folder in [*(ROOT/n for n in cases), ROOT/'audit_v696_finish_slots_regressions']:
        for path in folder.rglob('*'):
            if path.is_file(): inputs[str(path)] = digest(path)
    tools = ('verify_finish_display_v680_', 'test_finish_slots_v680_',
             'consolidate_finish_slots_v680_', 'run_finish_display_v680_',
             'verify_unassisted_finish_v680_')
    for path in (ROOT/'tools').iterdir():
        if path.is_file() and path.name.startswith(tools): inputs[str(path)] = digest(path)
    for pattern in ('mk2ks_finish_display_v680_*.lua','mk2ks_unassisted_finish_v680_*.lua'):
        for path in ROOT.glob(pattern): inputs[str(path)] = digest(path)
    for path in (report_path, prior_path, ROOT/'STATUS_2026-10-02_FATALITY_BOTH_SLOTS.md'):
        inputs[str(path)] = digest(path)
    out.mkdir()
    result = dict(passed=True, candidate='diagnostic_v680_native_pit_initial_cache',
                  cases=list(cases), prior_P1_cases_preserved=2,
                  prior_checkpoint_inputs_unchanged=len(prior['inputHashes']),
                  drawing_passes=1344, VRAM_words=1344*512*512,
                  displayed_pixels=1344*400*254, held_transition_samples=30,
                  native_palette_entries=palette_entries, regression_tests=25,
                  inputHashes=inputs, gameplay_changed=False, release_promoted=False,
                  fatalityAcceptance=False, fullPortAcceptance=False,
                  scope='Six physical-slot fatality sample/ancestry/palette/retirement cases; not all finishers, victims, art, audio or campaigns')
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='inputHashes'},indent=2))
    print('Pinned inputs:', len(inputs))
