"""Freeze exact natural CPU grab contact evidence; no release promotion."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import verify_cpu_pair as check
from test_cpu_pair import CASES

ROOT=check.ROOT
OUT=ROOT/'audit_v372_natural_cpu_pair_checked_inputs'


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def run():
    if OUT.exists():raise SystemExit('Refusing to overwrite evidence')
    prior=ROOT/'audit_v365_stock_reaction_checked_inputs'
    previous=json.loads((prior/'result.json').read_text())
    if not previous['passed']or(previous['candidate'],previous['executable_sha256'],previous['payload_sha256'])!=(check.NAME,check.EXE,check.PAYLOAD):raise SystemExit('Exact current checkpoint required')
    prior_count=0
    for name in ('audit_v363_morph_palette_checked_inputs','audit_v365_stock_reaction_checked_inputs'):
        manifest=json.loads((ROOT/name/'input_hashes_before.json').read_text())
        for file,expected in manifest.items():
            if digest(Path(file))!=expected:raise SystemExit('Prior exact input changed: '+file)
        prior_count+=len(manifest)
    files={ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin',ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'mame-mkp/mkport.exe',prior/'result.json',prior/'input_hashes_before.json'}
    files.update((ROOT/'tools').glob('*.py'))
    folders=[]
    for name,boot in CASES:
        folder=ROOT/f'audit_v371_cpu_pair_{name}_boot{boot}';folders.append((folder,'liu_kang'if name=='liu'else name))
        files.update(p for p in folder.rglob('*')if p.is_file())
        before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        files.update(Path(file)for file in before)
    build=json.loads((ROOT/check.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    files.update(Path(file)for file in build['input_hashes'])
    for name in ('audit_v285_native_pair_p2_kano','audit_v285_native_pair_p2_sonya','audit_v285_cross_slot_pair_p1_kano','audit_v285_walking_recovery_p1_sonya','audit_v366_cpu_pair_sonya_boot601','audit_v367_cpu_pair_sonya_boot601','audit_v368_cpu_pair_sonya_boot602','audit_v369_cpu_pair_kano_boot601','audit_v370_cpu_pair_sonya_boot601'):
        files.add(ROOT/name/'run.log')
    hashes={str(p):digest(p)for p in sorted(files)}
    if hashes[str(ROOT/'PLAY_MK2_KANO_SONYA.cmd')]!='9ECEF168B79FC38E436329973CA4B9A744BB1E9FA9F4F0987E01CD4AABC494E7' or hashes[str(ROOT/'mame-mkp/mkport.exe')]!='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891':raise SystemExit('Production build changed')
    (OUT/'input_sources').mkdir(parents=True)
    (OUT/'input_hashes_before.json').write_text(json.dumps(hashes,indent=2)+'\n')
    for name in ('audit_cpu_pair.py','verify_cpu_pair.py','test_cpu_pair.py','verify_restart_pair.py','verify_p2_campaign.py','run_cpu_pair_probe.ps1'):
        shutil.copy2(ROOT/'tools'/name,OUT/'input_sources'/name)
    tests=0
    for pattern,expected in (('test_cpu_pair.py',35),('test_restart_pair.py',35)):
        process=subprocess.run([sys.executable,'-m','unittest','discover','-s','tools','-p',pattern],cwd=ROOT,capture_output=True,text=True)
        text=process.stdout+process.stderr;(OUT/(pattern+'.log')).write_text(text)
        if process.returncode or not re.search(rf'Ran {expected} tests',text):raise SystemExit('Reference/mutation tests failed: '+pattern)
        tests+=expected
    proofs=[]
    for folder,player in folders:
        proof=check.verify(folder,player)
        (OUT/(folder.name+'.json')).write_text(json.dumps(proof,indent=2)+'\n')
        if not proof['passed']:raise SystemExit(json.dumps(proof['errors']))
        proofs.append(proof)
    for file,expected in hashes.items():
        if digest(Path(file))!=expected:raise SystemExit('Input changed during audit: '+file)
    result=dict(passed=True,candidate=check.NAME,executable_sha256=check.EXE,payload_sha256=check.PAYLOAD,
        natural_CPU_cases=len(proofs),completed_CPU_chokes=sum(p['target']=='kano'for p in proofs),completed_CPU_legs=sum(p['target']=='sonya'for p in proofs),
        paired_callback_fields=sum(p['paired_fields']for p in proofs),original_held_pose_fields=sum(p['held_fields']for p in proofs),victim_flight_fields=sum(p['victim_flight_fields']for p in proofs),
        covered_pairs=[dict(cpu=p['target'],human=p['player'],completed_cycle=p['cycle'])for p in proofs],
        CPU_slot=2,human_slot=1,assistance='none',new_CPU_mutation_tests=35,historical_pair_reference_tests=35,total_tests=tests,
        checked_inputs=len(hashes),revalidated_prior_inputs=prior_count,production_unchanged=True,
        extra_observed_entries_not_claimed_complete=True,original_descriptor_consumers_checked=True,
        scope=check.SCOPE,whole_character_integration_complete=False)
    (OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':run()
