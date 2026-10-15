"""Freeze current native stock-reaction cases without promoting the candidate."""
import hashlib
import json
import re
import shutil
import subprocess
import sys

import verify_stock_reaction as check

ROOT=check.ROOT
OUT=ROOT/'audit_v365_stock_reaction_checked_inputs'


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def run():
    if OUT.exists():raise SystemExit('Refusing to overwrite evidence')
    earlier=ROOT/'audit_v363_morph_palette_checked_inputs'
    prior=json.loads((earlier/'result.json').read_text())
    if not prior['passed'] or (prior['candidate'],prior['executable_sha256'],prior['payload_sha256'])!=(check.NAME,check.EXE,check.PAYLOAD):raise SystemExit('Exact completed palette checkpoint required')
    prior_inputs=json.loads((earlier/'input_hashes_before.json').read_text())
    for file,expected in prior_inputs.items():
        from pathlib import Path
        if digest(Path(file))!=expected:raise SystemExit('Earlier current-build checkpoint input changed: '+file)
    files={earlier/'result.json',earlier/'input_hashes_before.json',ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin',ROOT/'tools/audit_stock_reaction.py',ROOT/'tools/verify_stock_reaction.py',ROOT/'tools/test_stock_reaction.py',ROOT/'tools/run_stock_reaction_probe.ps1',ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'mame-mkp/mkport.exe'}
    folders=[]
    for victim in ('kano','sonya','cage'):
        for effect in ('freeze','shock'):
            for side in ((1,) if victim=='cage' else (1,2)):
                folder=ROOT/f'audit_v364_stock_reaction_{victim}_{effect}_p{side}'
                folders.append((folder,victim,effect,side));files.update(p for p in folder.rglob('*') if p.is_file())
    build=json.loads((ROOT/check.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    from pathlib import Path
    files.update(Path(file) for file in build['input_hashes']);files.update(Path(file) for file in json.loads((folders[0][0]/'input_hashes_before.json').read_text(encoding='utf-8-sig')))
    hashes={str(p):digest(p) for p in sorted(files)}
    (OUT/'input_sources').mkdir(parents=True)
    (OUT/'input_hashes_before.json').write_text(json.dumps(hashes,indent=2)+'\n')
    for name in ('audit_stock_reaction.py','verify_stock_reaction.py','test_stock_reaction.py','run_stock_reaction_probe.ps1'):
        shutil.copy2(ROOT/'tools'/name,OUT/'input_sources'/name)
    process=subprocess.run([sys.executable,'-m','unittest','discover','-s','tools','-p','test_stock_reaction.py'],cwd=ROOT,capture_output=True,text=True)
    text=process.stdout+process.stderr;(OUT/'test_stock_reaction.log').write_text(text)
    if process.returncode or not re.search(r'Ran 28 tests',text):raise SystemExit('Expected stock reference/mutation checks failed')
    proofs=[]
    for folder,victim,effect,side in folders:
        proof=check.verify(folder,victim,effect,side)
        (OUT/(folder.name+'.json')).write_text(json.dumps(proof,indent=2)+'\n')
        if not proof['passed']:raise SystemExit(json.dumps(proof['errors']))
        proofs.append(proof)
    for file,expected in hashes.items():
        if digest(Path(file))!=expected:raise SystemExit('Input changed during verification: '+file)
    own=[p for p in proofs if p['victim']!='cage'];stock=[p for p in proofs if p['victim']=='cage']
    result=dict(passed=True,candidate=check.NAME,executable_sha256=check.EXE,payload_sha256=check.PAYLOAD,
        stock_reaction_tests=28,prior_morph_checkpoint_tests=prior['tests'],owned_cases=len(own),stock_control_cases=len(stock),
        owned_fields=sum(p['fields'] for p in own),owned_contacts=sum(p['contacts'] for p in own),
        stock_control_fields=sum(p['fields'] for p in stock),stock_control_contacts=sum(p['contacts'] for p in stock),
        checked_inputs=len(hashes),revalidated_prior_inputs=len(prior_inputs),assistance='none',cheats_enabled=False,
        actual_original_palette_RAM_checked=True,actual_walk_jump_punch_return_checked=True,
        stock_control_custom_name_checks='inapplicable_zero_checks_not_claimed_as_custom_name_success',
        production_unchanged=True,scope=check.SCOPE,whole_character_integration_complete=False)
    (OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':run()
