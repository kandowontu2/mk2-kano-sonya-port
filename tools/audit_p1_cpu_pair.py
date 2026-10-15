"""Freeze real cold P2-only/native P1 CPU paired contact; never promote release."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import verify_p1_cpu_pair as check
from test_p1_cpu_pair import CASES

ROOT=check.ROOT
OUT=ROOT/'audit_v377_natural_p1_cpu_pair_checked_inputs'
PRIORS=('audit_v363_morph_palette_checked_inputs','audit_v365_stock_reaction_checked_inputs','audit_v372_natural_cpu_pair_checked_inputs')
SCOUTS=('audit_v373_p1_cpu_pair_sonya_boot600','audit_v373_p1_cpu_pair_sonya_boot601',
        'audit_v373_p1_cpu_pair_sonya_boot603','audit_v373_p1_cpu_pair_sonya_boot606',
        'audit_v374_p1_cpu_pair_kano_boot604','audit_v374_p1_cpu_pair_cage_boot604',
        'audit_v374_p1_cpu_pair_cage_boot605','audit_v374_p1_cpu_pair_sub_zero_boot604',
        'audit_v375_p1_cpu_pair_kano_boot604','audit_v375_p1_cpu_pair_cage_boot604',
        'audit_v375_p1_cpu_pair_cage_boot605','audit_v375_p1_cpu_pair_sub_zero_boot604',
        'audit_v376_p1_cpu_pair_kano_boot604','audit_v376_p1_cpu_pair_cage_boot604',
        'audit_v376_p1_cpu_pair_cage_boot605','audit_v376_p1_cpu_pair_sub_zero_boot604')


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def run():
    if OUT.exists():raise SystemExit('Refusing to overwrite evidence')
    last=json.loads((ROOT/PRIORS[-1]/'result.json').read_text())
    if not last['passed']or(last['candidate'],last['executable_sha256'],last['payload_sha256'])!=(check.NAME,check.EXE,check.PAYLOAD):raise SystemExit('Exact previous current-build checkpoint required')
    previous_count=0
    for name in PRIORS:
        manifest=json.loads((ROOT/name/'input_hashes_before.json').read_text())
        for file,expected in manifest.items():
            if digest(Path(file))!=expected:raise SystemExit('Previous frozen input changed: '+file)
        previous_count+=len(manifest)
    files={ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin',ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'mame-mkp/mkport.exe',
           ROOT/'mk2ks_p1_cpu_pair_probe.lua',ROOT/'tools/run_p1_cpu_pair_probe.ps1'}
    for name in PRIORS:files.update((ROOT/name/'result.json',ROOT/name/'input_hashes_before.json'))
    files.update((ROOT/'tools').glob('*.py'))
    folders=[]
    for version,player,boot in CASES:
        folder=ROOT/f'audit_v{version}_p1_cpu_pair_{player}_boot{boot}';folders.append((folder,player))
        files.update(p for p in folder.rglob('*')if p.is_file())
        before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        files.update(Path(file)for file in before)
    build=json.loads((ROOT/check.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    files.update(Path(file)for file in build['input_hashes'])
    for name in SCOUTS:
        folder=ROOT/name
        files.update(p for p in folder.rglob('*')if p.is_file())
    hashes={str(p):digest(p)for p in sorted(files)}
    if hashes[str(ROOT/'PLAY_MK2_KANO_SONYA.cmd')]!='9ECEF168B79FC38E436329973CA4B9A744BB1E9FA9F4F0987E01CD4AABC494E7' or hashes[str(ROOT/'mame-mkp/mkport.exe')]!='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891':raise SystemExit('Production launcher/emulator changed')
    (OUT/'input_sources').mkdir(parents=True)
    (OUT/'input_hashes_before.json').write_text(json.dumps(hashes,indent=2)+'\n')
    for name in ('audit_p1_cpu_pair.py','verify_p1_cpu_pair.py','test_p1_cpu_pair.py','verify_cpu_pair.py','test_cpu_pair.py','verify_restart_pair.py','verify_p2_campaign.py','run_p1_cpu_pair_probe.ps1'):
        shutil.copy2(ROOT/'tools'/name,OUT/'input_sources'/name)
    shutil.copy2(ROOT/'mk2ks_p1_cpu_pair_probe.lua',OUT/'input_sources/mk2ks_p1_cpu_pair_probe.lua')
    total_tests=0
    for pattern,expected in (('test_p1_cpu_pair.py',52),('test_cpu_pair.py',35),('test_restart_pair.py',35)):
        process=subprocess.run([sys.executable,'-m','unittest','discover','-s','tools','-p',pattern],cwd=ROOT,capture_output=True,text=True)
        output=process.stdout+process.stderr;(OUT/(pattern+'.log')).write_text(output)
        if process.returncode or not re.search(rf'Ran {expected} tests',output):raise SystemExit('Reference/mutation checks failed: '+pattern)
        total_tests+=expected
    proofs=[]
    for folder,player in folders:
        proof=check.verify(folder,player)
        (OUT/(folder.name+'.json')).write_text(json.dumps(proof,indent=2)+'\n')
        if not proof['passed']:raise SystemExit(str(proof['errors']))
        proofs.append(proof)
    # Preserve failed/inconclusive scouts without promoting exit zero or an
    # observer COMPLETE marker to independently verified full-pair evidence.
    scouts=[]
    for name in SCOUTS:
        folder=ROOT/name;meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        proof=check.verify(folder,meta['player'])
        if proof['passed']:raise SystemExit('Scout status changed; review explicit scope before accepting '+name)
        scouts.append(dict(case=name,player=meta['player'],independently_passed=False,errors=proof['errors']))
    (OUT/'preserved_unaccepted_scouts.json').write_text(json.dumps(scouts,indent=2)+'\n')
    for file,expected in hashes.items():
        if digest(Path(file))!=expected:raise SystemExit('Input changed during audit: '+file)
    result=dict(passed=True,candidate=check.NAME,executable_sha256=check.EXE,payload_sha256=check.PAYLOAD,
        natural_P1_CPU_cases=len(proofs),completed_CPU_chokes=sum(p['target']=='kano'for p in proofs),
        completed_CPU_legs=sum(p['target']=='sonya'for p in proofs),
        paired_callback_fields=sum(p['paired_fields']for p in proofs),
        original_held_pose_fields=sum(p['held_fields']for p in proofs),victim_flight_fields=sum(p['victim_flight_fields']for p in proofs),
        covered_pairs=[dict(cpu=p['target'],human=p['player'],completed_cycle=p['cycle'],case=folder.name)for p,(folder,_)in zip(proofs,folders)],
        CPU_slot=1,human_slot=2,cold_P2_only_starts=True,assistance='none',new_P1_CPU_reference_mutation_tests=52,
        previous_P2_CPU_reference_mutation_tests=35,historical_human_pair_reference_tests=35,total_tests=total_tests,
        checked_inputs=len(hashes),revalidated_prior_inputs=previous_count,preserved_unaccepted_scouts=len(scouts),
        production_unchanged=True,game_code_changed=False,extra_observed_entries_not_claimed_complete=True,
        scope=check.SCOPE,whole_character_integration_complete=False)
    (OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':run()
