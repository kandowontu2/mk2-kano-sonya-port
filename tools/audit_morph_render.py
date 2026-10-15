"""Exact palette-fix build, original-art pixels and bounded runtime regressions."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import verify_morph_render as morph
import verify_human_shang as human
import verify_native_shang_roster as cpu
import verify_projectile_render as projectile

ROOT=Path(__file__).resolve().parents[1]
NAME='diagnostic_v357_native_morph_palette'
EXE='4E71EFACF4837B6D32A3FF92BBE9A28B6D56C2AEFD68E165D35D6D14D95383AD'
OUT=ROOT/'audit_v363_morph_palette_checked_inputs'


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def run():
    if OUT.exists():raise SystemExit('Refusing to overwrite evidence')
    build_path=ROOT/NAME/'build-info.json';build=json.loads(build_path.read_text(encoding='utf-8-sig'))
    if (build['name'],build['executable_sha256'],build['payload_sha256'])!=(NAME,EXE,human.PAYLOAD):raise SystemExit('Independently expected matched candidate required')
    core=ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp'
    if digest(core)!='87B5F2953B374D890CC97F041AA450D8E89DAC735C8299BF40F3E491E7E94AEF' or str(core) not in build['input_hashes']:raise SystemExit('Exact checked palette-fix CPU implementation required')
    files={build_path,ROOT/NAME/'mkport_candidate.exe',ROOT/NAME/'roms/mk2ks/mk2ks.mdata',
           ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'mame-mkp/mkport.exe',
           morph.PAYLOAD,projectile.PAYLOAD,ROOT/'mk2ks_morph_render_probe.lua',
           ROOT/'mk2ks_human_shang_probe.lua',ROOT/'tools/run_human_shang_probe.ps1'}
    files.update(Path(p) for p in build['input_hashes']);files.update((ROOT/'tools').glob('*.py'))
    files.update((ROOT/'mk2').rglob('*'));files.update((ROOT/'mk3').rglob('*'))
    folders=[]
    for side in (1,2):
        for target in ('kano','sonya'):
            folders.extend([ROOT/f'audit_v358_fixed_morph_render_{target}_p{side}',
                            ROOT/f'audit_v356_native_morph_render_{target}_p{side}',
                            ROOT/f'audit_v361_palette_fix_projectile_{target}_p{side}'])
        for profile in human.STOCK:folders.append(ROOT/f'audit_v360_palette_fix_p{side}_{profile}')
    for target in ('kano','sonya'):folders.append(ROOT/f'audit_v359_palette_fix_cpu_{target}')
    for folder in folders:files.update(folder.rglob('*'))
    files.update((ROOT/NAME/'input_sources').rglob('*'))
    files={p for p in files if p.is_file()}
    hashes={str(p):digest(p) for p in sorted(files)}
    for file,expected in build['input_hashes'].items():
        if hashes.get(file)!=expected:raise SystemExit('Current build input changed: '+file)
    if hashes[str(ROOT/'PLAY_MK2_KANO_SONYA.cmd')]!='9ECEF168B79FC38E436329973CA4B9A744BB1E9FA9F4F0987E01CD4AABC494E7' or hashes[str(ROOT/'mame-mkp/mkport.exe')]!='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891':raise SystemExit('Production/installed build changed')
    (OUT/'input_sources').mkdir(parents=True)
    (OUT/'input_hashes_before.json').write_text(json.dumps(hashes,indent=2)+'\n')
    for name in ('audit_morph_render.py','verify_morph_render.py','test_morph_render.py','verify_projectile_render.py','verify_projectile_choreography.py','verify_human_shang.py','verify_native_shang_roster.py','test_native_shang_repeat.py'):
        shutil.copy2(ROOT/'tools'/name,OUT/'input_sources'/name)
    tests=0
    for pattern,expected in [('test_morph_render.py',21),('test_projectile_render.py',25),('test_human_shang.py',32),('test_native_shang*.py',54)]:
        process=subprocess.run([sys.executable,'-m','unittest','discover','-s','tools','-p',pattern],cwd=ROOT,capture_output=True,text=True)
        text=process.stdout+process.stderr;(OUT/(pattern.replace('*','all')+'.log')).write_text(text)
        if process.returncode or not re.search(rf'Ran {expected} tests',text):raise SystemExit('Failed expected reference/mutation tests: '+pattern)
        tests+=expected
    render_proofs=[];human_proofs=[];cpu_proofs=[];projectile_proofs=[]
    def save(name,proof):
        (OUT/(name+'.json')).write_text(json.dumps(proof,indent=2)+'\n')
        if not proof['passed']:raise SystemExit(json.dumps(proof.get('errors')))
    for side in (1,2):
        for target in ('kano','sonya'):
            name=f'audit_v358_fixed_morph_render_{target}_p{side}'
            proof=morph.verify(ROOT/name,target,side,candidate=NAME,exe_sha=EXE);save(name,proof);render_proofs.append(proof)
            name=f'audit_v361_palette_fix_projectile_{target}_p{side}'
            folder=ROOT/name;meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
            if (meta.get('exit_code'),meta.get('candidate'),meta.get('scenario'))!=(0,NAME,'block'):raise SystemExit('Actual declared unassisted native projectile regression required')
            proof=projectile.verify(folder,target,side,candidate_name=NAME,exe_sha=EXE,payload_sha=human.PAYLOAD);save(name,proof);projectile_proofs.append(proof)
        for profile in human.STOCK:
            name=f'audit_v360_palette_fix_p{side}_{profile}';target='kano' if profile=='stock_lk' else 'sonya'
            proof=human.verify(ROOT/name,target,side,profile,candidate=NAME,exe_sha=EXE);save(name,proof);human_proofs.append(proof)
    for target in ('kano','sonya'):
        name=f'audit_v359_palette_fix_cpu_{target}'
        proof=cpu.verify(ROOT/name,target,exe_sha=EXE,candidate=NAME);save(name,proof);cpu_proofs.append(proof)
    for file,expected in hashes.items():
        if digest(Path(file))!=expected:raise SystemExit('Input changed during audit: '+file)
    result=dict(passed=True,candidate=NAME,executable_sha256=EXE,payload_sha256=human.PAYLOAD,
                tests=tests,render_cases=len(render_proofs),transition_fields=sum(p['transition_fields'] for p in render_proofs),
                forward_handoff_fields=sum(p['handoff_fields'] for p in render_proofs),restored_handoff_fields=sum(p['restored_handoff_fields'] for p in render_proofs),
                original_component_bitmap_checks=sum(p['native_component_fields'] for p in render_proofs),
                all_sampled_morph_pixels_match=True,display_buffer_delay_fields=2,
                stock_morph_cases=len(human_proofs),cpu_cases=len(cpu_proofs),cpu_form_fields=sum(p['form_fields'] for p in cpu_proofs),
                cpu_morph_cycles=sum(len(p['morph_cycles']) for p in cpu_proofs),
                cpu_post_restore_fields=sum(p['post_restore_fields'] for p in cpu_proofs),
                cpu_assistance='stage14_and_P1_health_fixture',projectile_cases=len(projectile_proofs),
                projectile_component_draws=sum(p['native_component_draws'] for p in projectile_proofs),
                projectile_bitmap_samples=sum(len(p['visual']) for p in projectile_proofs),
                human_and_projectile_memory_assistance='none',checked_inputs=len(hashes),production_unchanged=True,
                scope='all_added_morph_holds_early_body_handoffs_original_pixels_and_current_bounded_human_CPU_projectile_regressions_not_all_game_audio_finishers_or_release',
                whole_character_integration_complete=False)
    (OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':run()
