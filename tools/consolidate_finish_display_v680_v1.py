"""Freeze the exact bounded current fatality presentation evidence."""
import hashlib
import json
import re
from pathlib import Path
import numpy as np
from PIL import Image
from verify_native_candidate_v680 import ROOT,NAME


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def need(ok,label):
    if not ok:raise ValueError(label)


if __name__=='__main__':
    out=ROOT/'audit_v692_finish_display_checked_inputs'
    need(not out.exists(),'Do not overwrite evidence')
    folder=ROOT/'audit_v691_finish_retirement_sonya_raiden'
    report_path=folder/'verification_v6.json'
    proof=json.loads(report_path.read_text())
    need(proof['passed'] and not proof['fullPortAcceptance'],'Exact bounded report, not full goal acceptance')
    inputs=proof['inputHashes'].copy()
    for name,sha in inputs.items():need(digest(Path(name))==sha,'Actual verified input changed: '+name)
    regression=folder/'regression_v1.log'
    text=regression.read_text(encoding='utf-8-sig')
    need(re.search(r'Ran 28 tests in [\d.]+s\s+OK\s*$',text) and 'FAILED' not in text,'All28 terminal regression tests')
    current=json.loads((ROOT/'audit_v685_pit_initial_cache_checked_inputs/verification.json').read_text())
    # Recheck every prior frozen input, not just current executable identity.
    for name,sha in current['inputHashes'].items():
        need(digest(Path(name))==sha,'Prior accepted checkpoint changed: '+name)
        inputs[name]=sha
    pairs=[ROOT/'audit_v691_finish_retirement_kano_sonya/snap/display_4236.png',
           ROOT/'audit_v691_finish_retirement_sonya_raiden/snap/display_4260.png']
    arrays=[np.asarray(Image.open(p).convert('RGB')) for p in pairs]
    need(arrays[0].shape==(254,400,3) and np.array_equal(*arrays),
         'Fixed last new-scene screenshots must be whole-image identical, no best-frame search')
    need(all(c['replayed']['frames']==224 and len(c['held_transition_scanout'])==5 and
             c['post_transition_replayed_samples']==20 and not c['fatalityAcceptance']
             for c in proof['cases'].values()),'All actual samples and explicit scope boundaries')
    # Inventory rejected/diagnostic runs without upgrading them to passes.
    evidence=[ROOT/n for n in ('audit_v686_native_finish_kano_sonya','audit_v686_native_finish_sonya_raiden',
              'audit_v687_finish_display_kano_sonya','audit_v687_finish_display_sonya_raiden',
              'audit_v688_finish_display_kano_sonya','audit_v688_finish_display_sonya_raiden',
              'audit_v689_finish_single_sonya_raiden','audit_v690_finish_retirement_kano_sonya',
              'audit_v690_finish_retirement_sonya_raiden',*proof['cases'])]
    for path in evidence:
        for file in path.rglob('*'):
            if file.is_file():inputs[str(file)]=digest(file)
    for file in (ROOT/'tools').iterdir():
        if file.is_file() and (file.name.startswith(('verify_finish_display_v680_','test_finish_display_v680_',
                    'inspect_finish_display_v680_','run_finish_display_v680_','consolidate_finish_display_v680_'))):
            inputs[str(file)]=digest(file)
    for file in ROOT.glob('mk2ks_finish_display_v680_*.lua'):inputs[str(file)]=digest(file)
    status=ROOT/'STATUS_2026-10-02_INDIVIDUAL_FATALITY_DISPLAY.md';inputs[str(status)]=digest(status)
    inputs[str(regression)]=digest(regression);inputs[str(report_path)]=digest(report_path)
    out.mkdir()
    result=dict(passed=True,candidate=NAME,verified_P1_cases=2,genuine_rounds=4,
                original_damage_events=20,replayed_display_fields=448,
                exact_VRAM_words=448*512*512,exact_displayed_pixels=448*400*254,
                held_transition_scanout_fields=10,regression_tests=28,
                native_pointer_retirement_fields={n:c['native_teardown_frame'] for n,c in proof['cases'].items()},
                fixed_last_new_scene_identical_pixels=400*254,
                prior_checkpoint_inputs_unchanged=len(current['inputHashes']),inputHashes=inputs,
                gameplay_changed=False,release_promoted=False,fatalityAcceptance=False,fullPortAcceptance=False,
                scope='Two current P1 actual fatality choreography/effect/rendered samples and native retirement; not all slots/victims/finishers/art/audio/campaigns')
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='inputHashes'},indent=2))
