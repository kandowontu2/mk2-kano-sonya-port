"""Freeze the exact human-morph checkpoint and ordinary mobility regressions."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import verify_human_shang as human
import verify_native_shang_roster as cpu
import verify_current_mobility as mobility
from test_human_shang import cases

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_v354_human_morph_checked_inputs'


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def run():
    if OUT.exists():raise SystemExit('Refusing to overwrite evidence')
    build_path=ROOT/human.CANDIDATE/'build-info.json'
    build=json.loads(build_path.read_text(encoding='utf-8-sig'))
    if (build['name'],build['executable_sha256'],build['payload_sha256'])!=(human.CANDIDATE,human.EXE,human.PAYLOAD):
        raise SystemExit('Exact independently expected candidate required')
    files={build_path,ROOT/human.CANDIDATE/'mkport_candidate.exe',ROOT/human.CANDIDATE/'roms/mk2ks/mk2ks.mdata',
           ROOT/'mk2ks_human_shang_probe.lua',ROOT/'tools/run_human_shang_probe.ps1',
           ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'mame-mkp/mkport.exe',ROOT/'mk2/mk2-maincpu.bin'}
    files.update(Path(file) for file in build['input_hashes'])
    files.update((ROOT/'tools').glob('*.py'))
    files.update((ROOT/'mk3').glob('*'))
    human_cases=list(cases());cpu_cases=[];mobility_cases=[]
    if len(human_cases)!=36:raise SystemExit('Complete 36-case physical input matrix required')
    for name,_,_,_ in human_cases:files.update((ROOT/name).rglob('*'))
    for target in ('kano','sonya'):
        folder=ROOT/f'audit_v351_cpu_{target}_human_bindings';cpu_cases.append((folder,target));files.update(folder.rglob('*'))
        for side in (1,2):
            for scenario in ('hit','block','miss'):
                folder=ROOT/f'audit_v353_human_binding_mobility_p{side}_{target}_{scenario}'
                mobility_cases.append((folder,target,side,scenario));files.update(folder.rglob('*'))
    files={p for p in files if p.is_file()}
    hashes={str(path):digest(path) for path in sorted(files)}
    for file,expected in build['input_hashes'].items():
        if hashes.get(file)!=expected:raise SystemExit('Current build input changed: '+file)
    if hashes[str(ROOT/'PLAY_MK2_KANO_SONYA.cmd')]!='9ECEF168B79FC38E436329973CA4B9A744BB1E9FA9F4F0987E01CD4AABC494E7' or hashes[str(ROOT/'mame-mkp/mkport.exe')]!='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891':
        raise SystemExit('Production/installed build unexpectedly changed')
    (OUT/'input_sources').mkdir(parents=True)
    (OUT/'input_hashes_before.json').write_text(json.dumps(hashes,indent=2)+'\n')
    for file in (Path(__file__),ROOT/'tools/verify_human_shang.py',ROOT/'tools/test_human_shang.py',ROOT/'tools/verify_native_shang_roster.py'):
        shutil.copy2(file,OUT/'input_sources'/file.name)
    tests=0
    for pattern,expected in [('test_human_shang.py',32),('test_native_shang*.py',37),('test_current_mobility.py',12)]:
        process=subprocess.run([sys.executable,'-m','unittest','discover','-s','tools','-p',pattern],cwd=ROOT,capture_output=True,text=True)
        output=process.stdout+process.stderr
        (OUT/(pattern.replace('*','all')+'.log')).write_text(output)
        if process.returncode or not re.search(rf'Ran {expected} tests',output):raise SystemExit('Failed expected mutation/reference tests: '+pattern)
        tests+=expected
    proofs=[]
    def save(name,proof):
        (OUT/(name+'.json')).write_text(json.dumps(proof,indent=2)+'\n')
        if not proof['passed']:raise SystemExit(json.dumps(proof))
        proofs.append(proof)
    for name,target,side,profile in human_cases:save(name,human.verify(ROOT/name,target,side,profile))
    human_proofs=proofs[:]
    for folder,target in cpu_cases:save(folder.name,cpu.verify(folder,target,exe_sha=human.EXE,candidate=human.CANDIDATE))
    cpu_proofs=proofs[len(human_proofs):]
    for folder,target,side,scenario in mobility_cases:save(folder.name,mobility.verify(folder,target,side,scenario,human.CANDIDATE,human.EXE,human.PAYLOAD))
    mobility_proofs=proofs[len(human_proofs)+len(cpu_proofs):]
    for file,expected in hashes.items():
        if digest(Path(file))!=expected:raise SystemExit('Input changed during audit: '+file)
    result=dict(passed=True,candidate=human.CANDIDATE,executable_sha256=human.EXE,payload_sha256=human.PAYLOAD,
                tests=tests,human_cases=len(human_proofs),human_gameplay_fields=sum(p['gameplay_fields'] for p in human_proofs),
                human_form_fields=sum(p['form_fields'] for p in human_proofs),human_memory_assistance='none',
                cpu_cases=len(cpu_proofs),cpu_form_fields=sum(p['form_fields'] for p in cpu_proofs),cpu_assistance='stage14_and_P1_health_fixture',
                mobility_cases=len(mobility_proofs),joined_fields=sum(p['joined']['joined_fields'] for p in mobility_proofs),
                checked_inputs=len(hashes),production_unchanged=True,whole_character_integration_complete=False,
                scope='36_native_human_morph_inputs_2_assisted_CPU_morph_regressions_12_unassisted_mobility_contacts_not_all_game_art_audio_finishers_or_release')
    (OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':run()
