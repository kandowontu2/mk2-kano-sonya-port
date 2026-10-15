"""Freeze the new rendering checkpoint, without relabeling old suites current."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import verify_unclipped_floor_shadows as v

ROOT=v.ROOT
OUT=ROOT/'audit_v454_unclipped_floor_shadows_checked_inputs'

def run():
    v.need(not OUT.exists(),'Refusing to overwrite evidence')
    prior=ROOT/'audit_v440_queued_floor_shadows_checked_inputs'
    old=json.loads((prior/'input_hashes_before.json').read_text())
    historical_source=ROOT/'mame-mkp/src/mame/midway/midtunit_v.cpp'
    old_source_copy=prior/'input_sources/mame-mkp/src/mame/midway/midtunit_v.cpp'
    for path,sha in old.items():
        actual=old_source_copy if Path(path)==historical_source else Path(path)
        v.need(v.digest(actual)==sha,'Previous frozen input changed: '+path)
    proof=v.verify()
    test=subprocess.run([sys.executable,'tools/test_unclipped_floor_shadows.py'],cwd=ROOT,capture_output=True,text=True)
    v.need(test.returncode==0 and re.search(r'Ran 32 tests',test.stdout+test.stderr),
           'Exact new 32-test suite\n'+test.stdout+test.stderr)
    files={ROOT/'tools/audit_unclipped_floor_shadows.py',ROOT/'tools/verify_unclipped_floor_shadows.py',
           ROOT/'tools/inspect_ground_presentation.py',ROOT/'tools/test_unclipped_floor_shadows.py',
           ROOT/'mame-mkp/src/mame/midway/midtunit_v.h',ROOT/'PLAY_MK2_KANO_SONYA.cmd',
           ROOT/'mame-mkp/mkport.exe',prior/'result.json',prior/'input_hashes_before.json'}
    # Preserve failed observers, rejected partial attempts, and their exact evidence.
    for folder in ROOT.iterdir():
        if not folder.is_dir():continue
        if re.match(r'^audit_v(441|442|443|445|446|448|449|450|451|452|453)_',folder.name) or folder.name in {
            'diagnostic_v444_complete_body_floor_shadow',v.NAME}:
            files.update(p for p in folder.rglob('*') if p.is_file())
            manifest=folder/'input_hashes_before.json'
            if manifest.exists():files.update(Path(p) for p in json.loads(manifest.read_text(encoding='utf-8-sig')))
    for p in ROOT.glob('mk2ks_ground_presentation*probe.lua'):files.add(p)
    for p in ROOT.glob('mk2ks_reaction_foreground*probe.lua'):files.add(p)
    for p in (ROOT/'tools').glob('run_ground_presentation*probe.ps1'):files.add(p)
    for p in (ROOT/'tools').glob('run_reaction*probe.ps1'):files.add(p)
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
    proof.update(new_tests=32,prior_frozen_inputs_preserved=len(old),prior_live_video_source_intentionally_updated_and_original_copy_verified=True,checked_inputs=len(frozen),
                 gameplay_source_sha256=v.digest(ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'),
                 video_source_sha256=v.digest(ROOT/'mame-mkp/src/mame/midway/midtunit_v.cpp'),
                 video_header_sha256=v.digest(ROOT/'mame-mkp/src/mame/midway/midtunit_v.h'),
                 production_not_promoted=True,prior_suites_not_relabelled_current=True,
                 rejected_attempts_preserved=['v441_v442_uppercut_misses','v444_VRAM_mask_loses_offscreen_rows',
                   'v449_Sonya_wrong_boot_for_exact_replay','v452_foreground_observer_wrong_stock_graphics_bank'],
                 findings='All imported body dimensions now project from complete ROM-decoded queued components; actual foreground-chain/blood DMA and native draw order distinguish occlusion from missing silhouette.',
                 current_test_launcher=str(ROOT/v.NAME/'PLAY_TEST_BUILD.cmd'))
    for path,sha in frozen.items():v.need(v.digest(path)==sha,'Input changed while freezing: '+path)
    for path,sha in old.items():
        actual=old_source_copy if Path(path)==historical_source else Path(path)
        v.need(v.digest(actual)==sha,'Previous evidence changed while freezing: '+path)
    (OUT/'result.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(proof,indent=2))

if __name__=='__main__':run()
