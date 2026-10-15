"""Freeze scoped native arm-rip proof and an explicit historical source transition."""
import hashlib,json,shutil
from pathlib import Path
import verify_native_arm_rip_v1051 as proof
ROOT=proof.ROOT;OUT=ROOT/'audit_v1054_native_arm_rip_checkpoint'
if OUT.exists():raise ValueError('Preserve checkpoints')
digest=proof.digest
driver=ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
historical=ROOT/'audit_v1044_arm_rip_source_transition/input_sources/midtunit_m.cpp'
old=json.loads((ROOT/'audit_v1040_jax_clap_checkpoint/checkpoint.json').read_text())
pins={};transitions=[]
for filename,wanted in old['inputHashes'].items():
 path=Path(filename)
 if path==driver:
  assert digest(historical)==wanted
  pins[str(historical)]=wanted
  transitions.append({'canonical':str(driver),'historicalSource':str(historical),'oldSHA256':wanted,'currentSHA256':digest(driver)})
 else:
  assert digest(path)==wanted,filename
  pins[filename]=wanted
assert len(transitions)==1
source=driver.read_text();before=historical.read_text()
begin=source.index("\t// Jax's native arm rip has three short victim tables")
end=source.index('\t// Every stock head-removal finisher',begin)
assert source[:begin]+source[end:]==before,'Only the new arm-rip data block may differ'
pins[str(driver)]=digest(driver)
report_path=ROOT/'audit_v1051_native_arm_rip_checked/report.json';report=json.loads(report_path.read_text())
assert report['passed'] and not report['fullPortAccepted']
for filename,wanted in report['inputHashes'].items():assert digest(Path(filename))==wanted,filename;pins[filename]=wanted
units=ROOT/'audit_v1053_arm_rip_proof_units/unit-results.json'
assert json.loads(units.read_text())['checksCount']==7
review=ROOT/'audit_v1049_arm_rip_visual_review/manual-review.json'
review_data=json.loads(review.read_text());assert review_data['actualScenesReviewed']==48
pngs=0
for name in ('kano','sonya'):
 for side in (1,2):
  first=ROOT/f'audit_v1046_jax_{name}_p{side}_owned_arms/snap'
  current=ROOT/f'audit_v1050_jax_{name}_p{side}_owned_arms/snap'
  a={str(p.relative_to(first)):p for p in first.rglob('*.png')}
  b={str(p.relative_to(current)):p for p in current.rglob('*.png')}
  assert a.keys()==b.keys()
  for key,path in b.items():assert path.read_bytes()==a[key].read_bytes();pins[str(path)]=digest(path);pngs+=1
assert pngs==616
assert digest(ROOT/'mame-mkp/mkport.exe')=='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
for folder in ('art_native_arm_rip_v1041','audit_v1042_owned_arm_rip_encoding',
 'audit_v1043_owned_arm_rip_encoding','audit_v1044_arm_rip_source_transition',
 'diagnostic_v1044_owned_jax_arm_rip','diagnostic_v1045_owned_jax_arm_rip',proof.CANDIDATE,
 'audit_v1047_native_arm_rip_checked','audit_v1049_arm_rip_visual_review',
 'audit_v1051_native_arm_rip_checked','audit_v1053_arm_rip_proof_units')+proof.CASES:
 for path in (ROOT/folder).rglob('*'):
  if path.is_file():pins[str(path)]=digest(path)
OUT.mkdir();(OUT/'input_sources').mkdir()
sources=('tools/build_native_arm_rip_v1042.py','tools/build_native_arm_rip_v1043.py',
 'mk2ks_stock_fatality_display_v1046.lua','tools/run_stock_fatality_v1046.ps1',
 'tools/run_stock_fatality_v1050.ps1','tools/verify_native_arm_rip_v1047.py',
 'tools/verify_native_arm_rip_v1051.py','tools/review_native_arm_rip_v1049.py',
 'tools/test_native_arm_rip_proof_v1053.py','tools/save_native_arm_checkpoint_v1054.py',
 'STATUS_2026-10-02_CURRENT_JAX_ARMS.md')
for filename in sources:
 path=ROOT/filename;target=OUT/'input_sources'/filename;target.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(path,target);pins[str(path)]=digest(path);pins[str(target)]=digest(target)
stats={'ownedDMAs':sum(c['ownedDMAs'] for c in report['cases'].values()),
 'presentedComponentAndPropSnapshots':sum(len(c['pixelMatches']) for c in report['cases'].values()),
 'currentPhysicalCases':4,'nativeWrapAge':147,'actualScenesManuallyReviewed':48,
 'actualPNGsIdenticalToReviewedCases':pngs,'corruptionAndActualRejectedBuildChecks':7}
data={'candidate':proof.CANDIDATE,'scope':report['scope'],**stats,
 'historicalPinsRevalidated':len(old['inputHashes']),'intentionalSourceTransitions':transitions,
 'installedExecutableUnchanged':True,'existingLaunchersNotUpdated':True,'releaseZipNotUpdated':True,
 'newCandidateRegressionsAccepted':False,'naturalAlternateSelectionAccepted':False,
 'allStockFatalitiesAccepted':False,'allArenasAccepted':False,'fullTowerAccepted':False,
 'finalCombinedGameplayAndUIAccepted':False,'fullPortAccepted':False,
 'evidencePins':len(pins),'inputHashes':pins}
(OUT/'checkpoint.json').write_text(json.dumps(data,indent=2)+'\n')
for filename,wanted in pins.items():assert digest(Path(filename))==wanted,filename
print(json.dumps({k:v for k,v in data.items() if k not in ('inputHashes','intentionalSourceTransitions')},indent=2))
