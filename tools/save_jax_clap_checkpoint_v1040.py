"""Freeze the exact Jax-only source transition and scoped verified evidence."""
import hashlib
import json
import shutil
from pathlib import Path
import verify_jax_clap_positions_v1036 as proof

ROOT=proof.ROOT;OUT=ROOT/'audit_v1040_jax_clap_checkpoint'
if OUT.exists():raise ValueError('Preserve checkpoints')
old=json.loads((ROOT/'audit_v1017_owned_rolling_heads_checkpoint/checkpoint.json').read_text())
driver=ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
old_driver=ROOT/'audit_v1017_owned_rolling_heads_checkpoint/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
pins={};transitions=[]
for filename,wanted in old['inputHashes'].items():
    path=Path(filename)
    if path==driver:
        assert proof.digest(old_driver)==wanted
        pins[str(old_driver)]=wanted
        transitions.append({'canonical':str(path),'historicalSource':str(old_driver),'oldSHA256':wanted,'currentSHA256':proof.digest(driver)})
    else:
        assert proof.digest(path)==wanted,filename
        pins[filename]=wanted
assert len(transitions)==1
current=driver.read_text();historical=old_driver.read_text()
begin=current.index("\t// Jax's head clap uses packed signed X/Y offsets")
end=current.index('\t// The shared native inflation/explosion victim task',begin)
assert current[:begin]+current[end:]==historical,'Unrelated source change'
info=json.loads((ROOT/proof.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
for filename,wanted in info['input_hashes'].items():
    assert proof.digest(Path(filename))==wanted,filename
    pins[filename]=wanted
for folder in ('audit_v1036_jax_clap_grounding_checked','audit_v1034_baraka_after_jax_clap_checked'):
    path=ROOT/folder/'report.json';report=json.loads(path.read_text());assert report['passed'] and not report['fullPortAccepted']
    for filename,wanted in report['inputHashes'].items():
        assert proof.digest(Path(filename))==wanted,filename
        pins[filename]=wanted
    pins[str(path)]=proof.digest(path)
units=ROOT/'audit_v1039_jax_clap_proof_units/unit-results.json'
assert json.loads(units.read_text())['corruptionAndActualRejectedBuildChecks']==7
pngs=0
for name in ('kano','sonya'):
    for side in (1,2):
        current_snap=ROOT/f'audit_v1034_baraka_{name}_p{side}_jax_clap_grounding_regression/snap'
        old_snap=ROOT/f'audit_v1004_baraka_{name}_p{side}_owned_rolling_head/snap'
        current_files={str(p.relative_to(current_snap)):p for p in current_snap.rglob('*.png')}
        old_files={str(p.relative_to(old_snap)):p for p in old_snap.rglob('*.png')}
        assert set(current_files)==set(old_files)
        for relative,path in current_files.items():
            assert path.read_bytes()==old_files[relative].read_bytes()
            pins[str(path)]=proof.digest(path);pngs+=1
assert pngs==504
assert proof.digest(ROOT/'mame-mkp/mkport.exe')=='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
review=json.loads((ROOT/'audit_v1033_jax_clap_visual_review/manual-review.json').read_text())
assert review['actualScenesReviewed']==48 and review['normalDeadPoolJaxPrimaryPositionsAndOwnedCollapseAccepted']
OUT.mkdir();(OUT/'input_sources').mkdir()
sources=('mk2ks_stock_fatality_v1020.lua','mk2ks_stock_fatality_display_v1020.lua',
 'mk2ks_stock_fatality_v1021.lua','mk2ks_stock_fatality_display_v1021.lua',
 'tools/run_stock_fatality_v1020.ps1','tools/run_stock_fatality_v1021.ps1',
 'tools/audit_native_split_arm_references_v1022.py','tools/build_native_candidate_v1024.ps1',
 'tools/verify_jax_clap_positions_v1030.py','tools/verify_jax_clap_positions_v1036.py',
 'tools/review_jax_clap_grounding_v1033.py','tools/verify_baraka_after_jax_clap_v1034.py',
 'tools/test_jax_clap_proof_v1037.py','tools/test_jax_clap_proof_v1039.py',
 'tools/save_jax_clap_checkpoint_v1040.py','STATUS_2026-10-02_CURRENT_JAX_CLAP.md')
for relative in sources:
    path=ROOT/relative;destination=OUT/'input_sources'/relative
    destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,destination)
    pins[str(path)]=proof.digest(path);pins[str(destination)]=proof.digest(destination)
for folder in ('audit_v1020_jax_kano_p1_clap_scout','audit_v1021_jax_liu_kang_p2_arms_reference',
 'audit_v1021_jax_sonya_p2_arms_table_trace','audit_v1021_kung_lao_liu_kang_p2_slice_reference',
 'audit_v1021_kung_lao_sonya_p2_slice_table_trace','audit_v1022_native_split_arm_references',
 'audit_v1033_jax_clap_visual_review','audit_v1037_jax_clap_proof_units',
 'audit_v1039_jax_clap_proof_units','diagnostic_v1024_native_jax_clap_positions',proof.CANDIDATE):
    for path in (ROOT/folder).rglob('*'):
        if path.is_file():pins[str(path)]=proof.digest(path)
for case in proof.CASES:
    for path in (ROOT/case).rglob('*'):
        if path.is_file():pins[str(path)]=proof.digest(path)
data={'candidate':proof.CANDIDATE,'executableSHA256':info['executable_sha256'],
 'payloadSHA256':info['payload_sha256'],'driverSHA256':proof.digest(driver),
 'scope':'8 current normal Dead Pool physical cases: Jax primary positions/owned grounded collapse and Baraka rolling-head regressions',
 'historicalPinsRevalidated':len(old['inputHashes']),'intentionalSourceTransitions':transitions,
 'currentPhysicalCases':8,'jaxGroundedBodyDMAs':2256,'jaxActualPosePictures':28,
 'jaxActualScenesManuallyReviewed':48,'barakaOwnedDMAs':4364,'barakaUnchangedActualPNGs':504,
 'corruptionAndActualRejectedCandidateChecks':7,'installedExecutableUnchanged':True,
 'existingLaunchersNotUpdated':True,'releaseZipNotUpdated':True,
 'kungLaoSplitStillIncomplete':True,'jaxArmRipStillIncomplete':True,
 'naturalAlternateSelectionAccepted':False,'allStockFatalitiesAccepted':False,
 'allArenasAccepted':False,'fullTowerAccepted':False,'finalCombinedGameplayAndUIAccepted':False,
 'fullPortAccepted':False,'evidencePins':len(pins),'inputHashes':pins}
(OUT/'checkpoint.json').write_text(json.dumps(data,indent=2)+'\n')
for filename,wanted in pins.items():assert proof.digest(Path(filename))==wanted,filename
print(json.dumps({k:v for k,v in data.items() if k not in ('inputHashes','intentionalSourceTransitions')},indent=2))
