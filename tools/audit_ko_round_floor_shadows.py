"""Freeze current KO evidence and preserve historical proofs without promoting production."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import verify_ko_round_floor_shadows as v

ROOT=v.ROOT
OUT=ROOT/'audit_v465_ko_round_floor_shadows_checked_inputs'

def previous_inputs():
    prior=ROOT/'audit_v454_unclipped_floor_shadows_checked_inputs'
    manifest=json.loads((prior/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    live=ROOT/'mame-mkp/src/mame/midway/midtunit_v.cpp'
    for path,sha in manifest.items():
        actual=ROOT/v.OLD/'input_sources/midtunit_v.cpp' if Path(path)==live else Path(path)
        v.need(v.digest(actual)==sha,'Previous v454 frozen bytes changed: '+path)
    older=ROOT/'audit_v440_queued_floor_shadows_checked_inputs'
    old_manifest=json.loads((older/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    for path,sha in old_manifest.items():
        actual=older/'input_sources/mame-mkp/src/mame/midway/midtunit_v.cpp' if Path(path)==live else Path(path)
        v.need(v.digest(actual)==sha,'Previous v440 frozen bytes changed: '+path)
    return len(manifest),len(old_manifest)

def run():
    v.need(not OUT.exists(),'Refusing to overwrite evidence')
    preserved,older=previous_inputs()
    proof=v.verify()
    test=subprocess.run([sys.executable,'tools/test_ko_round_floor_shadows.py','-v'],cwd=ROOT,capture_output=True,text=True)
    v.need(test.returncode==0 and re.search(r'Ran 22 tests',test.stdout+test.stderr),'Exact new 22-test suite\n'+test.stdout+test.stderr)
    files={ROOT/'tools/audit_ko_round_floor_shadows.py',ROOT/'tools/verify_ko_round_floor_shadows.py',
           ROOT/'tools/test_ko_round_floor_shadows.py',ROOT/'tools/inspect_ground_presentation.py',
           ROOT/'mame-mkp/src/mame/midway/midtunit_v.h',ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'mame-mkp/mkport.exe',
           ROOT/'WORKSPACE_PNG_DEDUPLICATION_2026-10-01.json',ROOT/'WORKSPACE_PNG_DEDUPLICATION_2026-10-01.jsonl',
           ROOT/'tools/deduplicate_frozen_pngs_2026_10_01.ps1'}
    for name in ('audit_v454_unclipped_floor_shadows_checked_inputs','audit_v440_queued_floor_shadows_checked_inputs'):
        files.update({ROOT/name/'result.json',ROOT/name/'input_hashes_before.json'})
    for folder in ROOT.iterdir():
        if folder.is_dir() and (re.match(r'^audit_v(455|457|458|459|460|462|464)_',folder.name) or folder.name==v.NAME):
            files.update(p for p in folder.rglob('*') if p.is_file())
            manifest=folder/'input_hashes_before.json'
            if manifest.exists():files.update(Path(path) for path in json.loads(manifest.read_text(encoding='utf-8-sig')))
    for version in (11,12,13):
        kind='round' if version==11 else 'foreground'
        files.add(ROOT/f'mk2ks_ko_{kind}_v{version}_probe.lua')
        files.add(ROOT/f'tools/run_ko_{kind}_v{version}_probe.ps1')
    build=json.loads((ROOT/v.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    files.update(Path(path) for path in build['input_hashes'])
    for name in ('mk2.zip','mk3.zip'):
        if (ROOT/'roms'/name).exists():files.add(ROOT/'roms'/name)
    frozen={str(path):v.digest(path) for path in sorted(files)}
    OUT.mkdir()
    for path in files:
        if path.suffix in ('.py','.ps1','.lua','.cpp','.h','.cmd'):
            dest=OUT/'input_sources'/path.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
    (OUT/'input_hashes_before.json').write_text(json.dumps(frozen,indent=2)+'\n')
    (OUT/'tests.log').write_text(test.stdout+test.stderr)
    cmd=ROOT/v.NAME/'PLAY_TEST_BUILD.cmd'
    romcheck=subprocess.run([str(cmd),'-verifyroms'],cwd=ROOT,capture_output=True,text=True)
    v.need(romcheck.returncode==0 and '1 were OK' in romcheck.stdout,'Actual candidate launcher ROM check')
    (OUT/'launcher_verifyroms.log').write_text(romcheck.stdout+romcheck.stderr)
    proof.update(new_tests=22,checked_inputs=len(frozen),prior_v454_inputs_preserved=preserved,prior_v440_inputs_preserved=older,
                 historical_video_sources_verified_from_frozen_copies=True,production_not_promoted=True,
                 prior_suites_not_relabelled_current=True,previous_goal_turn='progress: source mode-5 guard fixed and fresh KO/round-two captures completed',
                 current_test_launcher=str(cmd),video_source_sha256=v.digest(ROOT/'mame-mkp/src/mame/midway/midtunit_v.cpp'),
                 gameplay_source_sha256=v.digest(ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'),
                 video_header_sha256=v.digest(ROOT/'mame-mkp/src/mame/midway/midtunit_v.h'),
                 rejected_observations=['v460 has no per-draw foreground palette provenance across blood color changes',
                                        'v462_sub_zero_p2 log incomplete due disk full; fresh complete v464 replay'],
                 cleanup='5673 hash-identical PNG copies consolidated as NTFS hardlinks; all filenames retained; reported duplicate-copy bytes 291723895, not exact cluster allocation')
    for path,sha in frozen.items():v.need(v.digest(path)==sha,'Input changed during audit: '+path)
    v.need(previous_inputs()==(preserved,older),'Previous manifest inventory changed')
    (OUT/'result.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(proof,indent=2))

if __name__=='__main__':run()
