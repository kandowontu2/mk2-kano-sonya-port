"""Freeze actual current own ending pages after explicit assisted diagnostic setup."""
import json
import re
from verify_current_ending_presentation_v680_v1 import ROOT, CONTROL, GUEST, ORACLE, digest, verify


if __name__=='__main__':
    out=ROOT/'audit_v719_current_ending_presentation_checked_inputs'
    if out.exists(): raise ValueError('Do not overwrite evidence')
    cases=[ROOT/'audit_v716_current_ending_kano_p1']+sorted(ROOT.glob('audit_v717_current_ending_*'))
    reports=[verify(folder) for folder in cases]
    if len(reports)!=4 or not all(r['passed'] for r in reports): raise ValueError(reports)
    if {(r['player'],r['human_slot']) for r in reports}!={('kano',1),('kano',2),('sonya',1),('sonya',2)}:
        raise ValueError('Both actual physical slots required')
    for player in ('kano','sonya'):
        group=[r for r in reports if r['player']==player]
        for page in (1,2):
            images=[p for r in group for p in r['rendered_photos'] if p['file'].startswith('ending_page'+str(page))]
            if len(images)!=4 or len({p['sha256'] for p in images})!=1:
                raise ValueError('Full actual page differs by slot/early-late: '+player+str(page))
    text=(CONTROL/'regressions_v1.log').read_text(encoding='utf-8-sig')
    if not re.search(r'Ran 24 tests in [\d.]+s\s+OK\s*$',text): raise ValueError('Terminal24tests required')
    inputs={}
    for folder in cases+[CONTROL]:
        result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        inputs.update(result['input_hashes'])
    previous=ROOT/'audit_v707_native_campaign_photos_checked_inputs/verification.json'
    prior_inputs=json.loads(previous.read_text())['inputHashes']
    lookup={str(__import__('pathlib').Path(k).resolve()).lower():v for k,v in prior_inputs.items()}
    for file in ORACLE.glob('*'):
        if file.is_file():
            sha=digest(file)
            if lookup.get(str(file.resolve()).lower())!=sha: raise ValueError('Original photo oracle changed: '+str(file))
            inputs[str(file)]=sha
    attempts=[]
    for pattern in ('audit_v711_boss_play_*','audit_v713_boss_play_*','audit_v714_boss_evade_*',
                    'audit_v715_current_ending_*','audit_v716_current_ending_*','audit_v717_current_ending_*',
                    'audit_v718_current_ending_*'):
        for folder in ROOT.glob(pattern):
            result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
            if result['exit_code']!=0: raise ValueError('Nonterminal capture: '+str(folder))
            attempts.append(folder.name)
            for file in folder.rglob('*'):
                if file.is_file(): inputs[str(file)]=digest(file)
    for pattern in ('mk2ks_current_ending_presentation_v680_v*.lua','mk2ks_native_boss_play_v680_v*.lua',
                    'tools/*current_ending_presentation_v680_v*.*','tools/run_native_boss_play_v680_v*.ps1'):
        for file in ROOT.glob(pattern):
            if file.is_file(): inputs[str(file)]=digest(file)
    for file in (GUEST,ROOT/'STATUS_2026-10-02_CURRENT_ENDING_PRESENTATION.md',
                 ROOT/'audit_v712_native_boss_recovery_checked_inputs/verification.json',previous):
        inputs[str(file)]=digest(file)
    report=dict(passed=True,ending_cases=reports,original_stock_control=CONTROL.name,regression_tests=24,
                visible_photo_pixels=sum(p['compared_visible_pixels'] for r in reports for p in r['rendered_photos']),
                stock_frame_overpaint_pixels=sum(p['stock_frame_overpaint_pixels_compared'] for r in reports for p in r['rendered_photos']),
                full_rendered_pages_equal_between_slots=True,story_text_visually_reviewed=True,text_pixel_oracle=False,
                attempted_captures=sorted(attempts),prior_manifest_underlying_inputs_rechecked_here=False,
                gameplay_changed=False,release_promoted=False,audio_fidelity_accepted=False,
                unassisted_clear_proven=False,fullPortAcceptance=False,inputHashes=inputs,
                scope='Actual own ending pages and return after explicitly assisted combat; no unassisted bosses/tower, complete cinematic/audio or full-port acceptance')
    out.mkdir();(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','ending_cases')},indent=2))
    print('Pinned inputs:',len(inputs))
