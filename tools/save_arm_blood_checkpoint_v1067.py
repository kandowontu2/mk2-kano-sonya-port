"""Freeze blood correction and explicitly rejected full alternate runtime."""
import json
import shutil
from pathlib import Path
import verify_native_arm_blood_v1064 as normal
import verify_arm_alternate_diagnostic_v1065 as alternate

ROOT=normal.ROOT;OUT=ROOT/'audit_v1067_arm_blood_checkpoint'
if OUT.exists():raise ValueError('Preserve checkpoints')
old_path=ROOT/'audit_v1057_native_regression_checkpoint/checkpoint.json'
old=json.loads(old_path.read_text());pins=dict(old['inputHashes'])
for filename,wanted in pins.items():assert normal.digest(Path(filename))==wanted,filename
normal_path=ROOT/'audit_v1064_native_arm_blood_checked/report.json'
alternate_path=ROOT/'audit_v1065_arm_alternate_palette_diagnostic_checked/report.json'
reports=[json.loads(path.read_text()) for path in (normal_path,alternate_path)]
assert all(r['passed'] and not r['fullPortAccepted'] for r in reports)
assert len(reports[0]['cases'])==4 and len(reports[1]['cases'])==2
assert not reports[1]['naturalAlternateSelectionAccepted'] and not reports[1]['fullAlternateRuntimeAccepted']
for report in reports:
 for filename,wanted in report['inputHashes'].items():
  assert normal.digest(Path(filename))==wanted,filename
  if filename in pins:assert pins[filename]==wanted,filename
  pins[filename]=wanted
review_path=ROOT/'audit_v1066_arm_blood_visual_review/manual-review.json'
review=json.loads(review_path.read_text());assert review['actualScenesManuallyReviewed']==72
assert review['detachedArmAlternateCostumeRuntimeRejected']
units_path=ROOT/'audit_v1069_arm_blood_proof_units/unit-results.json'
units=json.loads(units_path.read_text());assert units['passed'] and units['corruptionChecks']==3
assert normal.digest(ROOT/'mame-mkp/mkport.exe')=='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
assert normal.digest(ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp')=='29A023356C55A7FA89110FA27FDE2B7A6AB49562967D6BD44C5167B40F7AC2EB'
for folder in ('art_native_arm_blood_v1059','audit_v1060_owned_arm_blood_encoding',normal.CANDIDATE,
 'audit_v1064_native_arm_blood_checked','audit_v1065_arm_alternate_palette_diagnostic_checked',
 'audit_v1066_arm_blood_visual_review','audit_v1069_arm_blood_proof_units')+normal.CASES+alternate.CASES:
 for path in (ROOT/folder).rglob('*'):
  if path.is_file():pins[str(path)]=normal.digest(path)
pins[str(old_path)]=normal.digest(old_path)
OUT.mkdir()
for filename in ('tools/build_native_arm_blood_v1060.py','tools/run_native_arm_blood_v1062.ps1',
 'mk2ks_arm_alt_palette_v1063.lua','tools/verify_native_arm_blood_v1064.py',
 'tools/verify_arm_alternate_diagnostic_v1065.py','tools/review_arm_blood_v1066.py',
 'tools/test_arm_blood_proof_v1069.py','tools/save_arm_blood_checkpoint_v1067.py',
 'STATUS_2026-10-03_CURRENT_ARM_BLOOD.md'):
 path=ROOT/filename;frozen=OUT/'input_sources'/filename
 frozen.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,frozen)
 pins[str(path)]=normal.digest(path);pins[str(frozen)]=normal.digest(frozen)
data={'candidate':normal.CANDIDATE,'historicalPinsRevalidated':len(old['inputHashes']),
 'ordinaryRealInputCases':4,'explicitControlledAlternateDiagnostics':2,
 'ordinaryOwnedDMAs':sum(c['ownedDMAs'] for c in reports[0]['cases'].values()),
 'controlledOwnedDMAs':sum(c['ownedDMAs'] for c in reports[1]['cases'].values()),
 'actualScenesManuallyReviewed':72,'sonyaActualPNGsUnchanged':306,
 'bloodPixels':750,'changedIndices':477,'changedPackedBytes':485,
 'corruptionChecks':3,'nativeGameSourceUnchanged':True,'sourceSpritesUnchanged':True,
 'installedExecutableUnchanged':True,'existingLaunchersNotUpdated':True,'releaseZipNotUpdated':True,
 'bloodCorrectionAcceptedInScopedEvidence':True,
 'detachedArmAlternateCostumeFixStillRequired':True,'naturalAlternateSelectionAccepted':False,
 'newCandidateRegressionsAccepted':False,'allStockFatalitiesAccepted':False,'allArenasAccepted':False,
 'fullTowerAccepted':False,'finalCombinedGameplayAndUIAccepted':False,'fullPortAccepted':False,
 'evidencePins':len(pins),'inputHashes':pins}
(OUT/'checkpoint.json').write_text(json.dumps(data,indent=2)+'\n')
for filename,wanted in pins.items():assert normal.digest(Path(filename))==wanted,filename
print(json.dumps({k:v for k,v in data.items() if k!='inputHashes'},indent=2))
