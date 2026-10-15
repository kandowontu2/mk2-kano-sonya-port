"""Freeze full original individual CPU/victim ready handoffs and stock control."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import verify_cpu_recovery as check
from test_cpu_recovery import CASES

ROOT=check.ROOT
OUT=ROOT/'audit_v380_native_cpu_recovery_checked_inputs'
PRIORS=('audit_v363_morph_palette_checked_inputs','audit_v365_stock_reaction_checked_inputs',
        'audit_v372_natural_cpu_pair_checked_inputs','audit_v377_natural_p1_cpu_pair_checked_inputs')


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def run():
    if OUT.exists():raise SystemExit('Refusing to overwrite evidence')
    last=json.loads((ROOT/PRIORS[-1]/'result.json').read_text())
    if not last['passed']or(last['candidate'],last['executable_sha256'],last['payload_sha256'])!=(check.NAME,check.EXE,check.PAYLOAD):raise SystemExit('Exact previous current checkpoint required')
    prior_count=0
    for name in PRIORS:
        manifest=json.loads((ROOT/name/'input_hashes_before.json').read_text())
        for file,expected in manifest.items():
            if digest(Path(file))!=expected:raise SystemExit('Previous input changed: '+file)
        prior_count+=len(manifest)
    files={ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin',ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'mame-mkp/mkport.exe',
           ROOT/'mk2ks_cpu_guard_probe.lua',ROOT/'mk2ks_cpu_recovery_probe.lua',
           ROOT/'tools/run_cpu_guard_probe.ps1',ROOT/'tools/run_cpu_recovery_probe.ps1'}
    files.update((ROOT/'tools').glob('*.py'))
    for name in PRIORS:files.update((ROOT/name/'result.json',ROOT/name/'input_hashes_before.json'))
    for prefix in ('audit_v378_cpu_guard_*','audit_v379_cpu_recovery_*'):
        for folder in ROOT.glob(prefix):
            if not folder.is_dir():continue
            files.update(p for p in folder.rglob('*')if p.is_file())
            before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
            files.update(Path(file)for file in before)
    build=json.loads((ROOT/check.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    files.update(Path(file)for file in build['input_hashes'])
    hashes={str(p):digest(p)for p in sorted(files)}
    if hashes[str(ROOT/'PLAY_MK2_KANO_SONYA.cmd')]!='9ECEF168B79FC38E436329973CA4B9A744BB1E9FA9F4F0987E01CD4AABC494E7'or hashes[str(ROOT/'mame-mkp/mkport.exe')]!='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891':raise SystemExit('Production launcher/emulator changed')
    (OUT/'input_sources').mkdir(parents=True)
    (OUT/'input_hashes_before.json').write_text(json.dumps(hashes,indent=2)+'\n')
    for name in ('audit_cpu_recovery.py','verify_cpu_recovery.py','test_cpu_recovery.py','verify_p1_cpu_pair.py','test_p1_cpu_pair.py',
                 'verify_cpu_pair.py','test_cpu_pair.py','verify_restart_pair.py','verify_p2_campaign.py','run_cpu_recovery_probe.ps1','run_cpu_guard_probe.ps1'):
        shutil.copy2(ROOT/'tools'/name,OUT/'input_sources'/name)
    for name in ('mk2ks_cpu_recovery_probe.lua','mk2ks_cpu_guard_probe.lua'):shutil.copy2(ROOT/name,OUT/'input_sources'/name)
    tests=0
    for pattern,expected in (('test_cpu_recovery.py',63),('test_p1_cpu_pair.py',52),('test_cpu_pair.py',35),('test_restart_pair.py',35)):
        process=subprocess.run([sys.executable,'-m','unittest','discover','-s','tools','-p',pattern],cwd=ROOT,capture_output=True,text=True)
        output=process.stdout+process.stderr;(OUT/(pattern+'.log')).write_text(output)
        if process.returncode or not re.search(rf'Ran {expected} tests',output):raise SystemExit('Reference/mutation checks failed: '+pattern)
        tests+=expected
    proofs=[]
    for player,boot in CASES:
        folder=ROOT/f'audit_v379_cpu_recovery_{player}_boot{boot}';proof=check.verify(folder,player)
        (OUT/(folder.name+'.json')).write_text(json.dumps(proof,indent=2)+'\n')
        if not proof['passed']:raise SystemExit(str(proof['errors']))
        proofs.append(proof)
    stock=check.verify_stock_control(ROOT/'audit_v378_cpu_guard_sonya_boot601')
    (OUT/'original_Baraka_control.json').write_text(json.dumps(stock,indent=2)+'\n')
    if not stock['passed']:raise SystemExit(str(stock['errors']))
    unaccepted=[]
    for player in ('sonya','sub_zero'):
        folder=ROOT/f'audit_v379_cpu_recovery_{player}_boot604';proof=check.verify(folder,player)
        if proof['passed']:raise SystemExit('Unaccepted scout changed; review scope explicitly')
        unaccepted.append(dict(case=folder.name,independently_passed=False,errors=proof['errors']))
    (OUT/'preserved_unaccepted_recovery_scouts.json').write_text(json.dumps(unaccepted,indent=2)+'\n')
    for file,expected in hashes.items():
        if digest(Path(file))!=expected:raise SystemExit('Input changed during audit: '+file)
    result=dict(passed=True,candidate=check.NAME,executable_sha256=check.EXE,payload_sha256=check.PAYLOAD,
        natural_CPU_recovery_cases=len(proofs),completed_CPU_chokes=1,completed_CPU_legs=1,
        paired_callback_fields=sum(p['paired_fields']for p in proofs),original_held_pose_fields=sum(p['held_fields']for p in proofs),
        victim_flight_fields=sum(p['victim_flight_fields']for p in proofs),
        covered_pairs=[dict(cpu=p['target'],human=p['player'],cycle=p['cycle'],own_handoff=p['own_handoff'],victim_handoff=p['victim_handoff'])for p in proofs],
        original_stock_generic_action_setup_cleanup_cycles=stock['native_generic_setup_cleanup_cycles'],
        new_native_recovery_tests=63,previous_P1_CPU_tests=52,previous_P2_CPU_tests=35,historical_human_pair_reference_tests=35,total_tests=tests,
        CPU_slot=1,human_slot=2,assistance='none',checked_inputs=len(hashes),revalidated_prior_inputs=prior_count,
        old_simultaneous_clean_gate_not_waived=True,old_under_300_field_gate_retained=True,
        individual_native_cleanup_and_ready_handoffs_required=True,CPU_later_busy_flags_require_new_original_action_setup=True,
        game_code_changed=False,production_unchanged=True,preserved_unaccepted_recovery_scouts=2,
        scope=check.SCOPE,whole_character_integration_complete=False)
    (OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':run()
