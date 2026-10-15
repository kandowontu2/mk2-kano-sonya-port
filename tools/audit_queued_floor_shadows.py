"""Freeze the new rendering checkpoint, without relabeling old suites current."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import verify_queued_floor_shadows as v

ROOT=v.ROOT
OUT=ROOT/'audit_v440_queued_floor_shadows_checked_inputs'

def run():
    v.need(not OUT.exists(),'Refusing to overwrite evidence')
    prior=ROOT/'audit_v425_native_ui_flow_checked_inputs'
    old=json.loads((prior/'input_hashes_before.json').read_text())
    for path,sha in old.items():v.need(v.digest(path)==sha,'Frozen previous input changed: '+path)
    proof=v.verify()
    test=subprocess.run([sys.executable,'tools/test_queued_floor_shadows.py'],cwd=ROOT,capture_output=True,text=True)
    v.need(test.returncode==0 and re.search(r'Ran 22 tests',test.stdout+test.stderr),
           'Exact new 22-test suite\n'+test.stdout+test.stderr)
    files={ROOT/'tools/audit_queued_floor_shadows.py',ROOT/'tools/verify_queued_floor_shadows.py',
           ROOT/'tools/inspect_ground_presentation.py',ROOT/'tools/test_queued_floor_shadows.py',
           ROOT/'mame-mkp/src/mame/midway/midtunit_v.h',ROOT/'PLAY_MK2_KANO_SONYA.cmd',
           ROOT/'mame-mkp/mkport.exe',prior/'result.json',prior/'input_hashes_before.json'}
    # Preserve failed observers, rejected partial attempts, and their exact evidence.
    for folder in ROOT.iterdir():
        if not folder.is_dir():continue
        if re.match(r'^audit_v(426|427|428|431|432|435|436|438|439)_',folder.name) or folder.name in {
            'diagnostic_v429_queued_native_floor_shadow','diagnostic_v430_queued_native_floor_shadow',
            'diagnostic_v433_camera_native_floor_shadow','diagnostic_v434_camera_native_floor_shadow',v.NAME}:
            files.update(p for p in folder.rglob('*') if p.is_file())
            manifest=folder/'input_hashes_before.json'
            if manifest.exists():files.update(Path(p) for p in json.loads(manifest.read_text(encoding='utf-8-sig')))
    for p in ROOT.glob('mk2ks_ground_presentation*probe.lua'):files.add(p)
    for p in (ROOT/'tools').glob('run_ground_presentation*probe.ps1'):files.add(p)
    build=json.loads((ROOT/v.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    files.update(Path(p) for p in build['input_hashes'])
    for name in ('mk2.zip','mk3.zip'):
        p=ROOT/'roms'/name
        if p.exists():files.add(p)
    frozen={str(p):v.digest(p) for p in sorted(files)}
    sources=OUT/'input_sources';sources.mkdir(parents=True)
    for p in files:
        if p.suffix in ('.lua','.ps1','.py','.cpp','.h','.cmd'):
            destination=sources/p.relative_to(ROOT)
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,destination)
    (OUT/'input_hashes_before.json').write_text(json.dumps(frozen,indent=2)+'\n')
    (OUT/'tests.log').write_text(test.stdout+test.stderr)
    proof.update(new_tests=22,previous_frozen_inputs_unchanged=len(old),checked_inputs=len(frozen),
                 gameplay_source_sha256=v.digest(ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'),
                 video_source_sha256=v.digest(ROOT/'mame-mkp/src/mame/midway/midtunit_v.cpp'),
                 video_header_sha256=v.digest(ROOT/'mame-mkp/src/mame/midway/midtunit_v.h'),
                 production_not_promoted=True,prior_283_tests_not_relabelled_current=True,
                 rejected_attempts_preserved=['v426_no_ready_observer','v429_const_build_failure',
                   'v430_ambiguous_walk_component_partial_shadow','v433_disk_full_build_failure',
                   'v434_regular_pose_only_missing_mode7_round_intro'],
                 findings='Queued DMA can outlive the actor cache pose; native camera floor transform removes the lookup race. Modes 2/3/7 plus real Main ownership and palette bound the projection.',
                 current_test_launcher=str(ROOT/v.NAME/'PLAY_TEST_BUILD.cmd'))
    for path,sha in {**old,**frozen}.items():v.need(v.digest(path)==sha,'Input changed while freezing: '+path)
    (OUT/'result.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(proof,indent=2))

if __name__=='__main__':run()
