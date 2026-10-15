"""Freeze scoped native costume proof without claiming full port completion."""
import json
import shutil
from pathlib import Path
import verify_native_arm_palette_v1074 as normal
import verify_arm_palette_controlled_v1083 as alternate
import verify_arm_palette_stock_v1079 as stock

ROOT=normal.ROOT;OUT=ROOT/'audit_v1090_arm_palette_checkpoint'
if OUT.exists():raise ValueError('Preserve checkpoints')
prior_path=ROOT/'audit_v1067_arm_blood_checkpoint/checkpoint.json'
prior=json.loads(prior_path.read_text());pins=dict(prior['inputHashes'])
driver=ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
archive=ROOT/'audit_v1070_arm_palette_source_transition/input_sources/midtunit_m.cpp'
old_hash='29A023356C55A7FA89110FA27FDE2B7A6AB49562967D6BD44C5167B40F7AC2EB'
new_hash='1DF1D1217776DBC3830F00ED078589A925A81F7C356F8EADE117907711A68CF6'
assert normal.digest(driver)==new_hash and normal.digest(archive)==old_hash
transition_count=0
for filename,wanted in pins.items():
    if Path(filename)==driver:
        assert wanted==old_hash;transition_count+=1
    else:assert normal.digest(Path(filename))==wanted,filename
assert transition_count==1
pins[str(driver)]=new_hash;pins[str(archive)]=old_hash
report_paths=[ROOT/name for name in (
    'audit_v1074_native_arm_palette_checked/report.json',
    'audit_v1083_arm_palette_controlled_checked/report.json',
    'audit_v1079_arm_palette_stock_checked/report.json',
    'audit_v1087_arm_rng_differential_checked/report.json')]
reports=[json.loads(p.read_text()) for p in report_paths]
assert all(r['passed'] and not r.get('errors',[]) and not r['fullPortAccepted'] for r in reports)
assert [len(r['cases']) for r in reports]==[4,4,2,4]
assert not reports[1]['naturalAlternateSelectionAccepted']
assert reports[3]['historicalWholeImageEqualityRejected'] and not reports[3]['arbitraryVisualDifferencesExempted']
for report in reports:
    for filename,wanted in report['inputHashes'].items():
        assert normal.digest(Path(filename))==wanted,filename
        if filename in pins:assert pins[filename]==wanted,filename
        pins[filename]=wanted
review_path=ROOT/'audit_v1088_arm_palette_visual_review/manual-review.json'
review=json.loads(review_path.read_text());assert review['actualScenesManuallyReviewed']==120
assert review['controlledBodyAndBothDetachedArmCostumesMatch'] and not review['fullPortAccepted']
units_path=ROOT/'audit_v1089_arm_rng_proof_units/unit-results.json'
units=json.loads(units_path.read_text());assert units['passed'] and units['corruptionChecks']==4
assert not units['filesModifiedByFixtures']
visual_pins=json.loads((ROOT/'audit_v1088_arm_palette_visual_review/inputHashes.json').read_text())
for filename,wanted in visual_pins.items():
    assert normal.digest(Path(filename))==wanted,filename
    pins[filename]=wanted
assert normal.digest(ROOT/'mame-mkp/mkport.exe')=='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
pair_cases=tuple(f'audit_v1086_jax_{n}_p{s}_{version}_rng'
                 for n in ('kano','sonya') for s in (1,2) for version in ('old','new'))
folders=(normal.CANDIDATE,'audit_v1070_arm_palette_source_transition',
         'audit_v1074_native_arm_palette_checked','audit_v1083_arm_palette_controlled_checked',
         'audit_v1079_arm_palette_stock_checked','audit_v1080_arm_palette_visual_review',
         'audit_v1087_arm_rng_differential_checked','audit_v1088_arm_palette_visual_review',
         'audit_v1089_arm_rng_proof_units')+normal.CASES+alternate.CASES+stock.CASES+pair_cases
for folder in folders:
    for path in (ROOT/folder).rglob('*'):
        if path.is_file():pins[str(path)]=normal.digest(path)
for path in report_paths+[prior_path,review_path,units_path]:pins[str(path)]=normal.digest(path)
OUT.mkdir()
sources=('tools/run_native_arm_palette_v1072.ps1','mk2ks_arm_palette_trace_v1073.lua',
         'tools/verify_native_arm_palette_v1074.py','tools/verify_arm_palette_controlled_v1075.py',
         'tools/verify_arm_palette_controlled_v1083.py','mk2ks_stock_fatality_v1077.lua',
         'mk2ks_stock_fatality_display_v1077.lua','mk2ks_arm_palette_stock_trace_v1078.lua',
         'tools/run_arm_palette_stock_v1078.ps1','tools/verify_arm_palette_stock_v1079.py',
         'tools/review_arm_palette_v1080.py','tools/review_arm_palette_v1084.py',
         'mk2ks_arm_rng_trace_v1085.lua','tools/run_arm_rng_diagnostic_v1086.ps1',
         'tools/verify_arm_rng_differential_v1087.py','tools/review_arm_palette_v1088.py',
         'tools/test_arm_rng_proof_v1089.py','tools/save_arm_palette_checkpoint_v1090.py',
         'STATUS_2026-10-03_CURRENT_ARM_PALETTE.md')
for filename in sources:
    path=ROOT/filename;frozen=OUT/'input_sources'/filename
    frozen.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,frozen)
    pins[str(path)]=normal.digest(path);pins[str(frozen)]=normal.digest(frozen)
data={'candidate':normal.CANDIDATE,'historicalPinsRevalidated':len(prior['inputHashes']),
      'intentionalSourceTransitions':[{'path':str(driver),'before':old_hash,'after':new_hash,
                                      'exactOriginalSourcePreservedAt':str(archive)}],
      'ordinaryRealInputCases':4,'explicitControlledAlternateDiagnostics':4,
      'genuineMileenaStockRegressions':2,'oldNewPairedRealInputRuns':8,
      'pairedScenePNGsCompared':sum(c['actualPNGsCompared']for c in reports[3]['cases'].values()),
      'readOnlyReplayPNGsExact':sum(sum(c['readOnlyReplayPNGsExact'])for c in reports[3]['cases'].values()),
      'originalRNGCallsIndependentlyReconstructed':sum(sum(c['originalRNGCalls'])for c in reports[3]['cases'].values()),
      'actualScenesManuallyReviewed':120,'corruptionChecks':4,
      'bloodOnlyVisualVariationExplained':True,'historicalWholeImageEqualityClaimRejected':True,
      'nativeDetachedArmAlternatePaletteAcceptedInControlledScope':True,
      'originalMileenaOverrideAcceptedInScopedEvidence':True,
      'sourceArtworkAndPayloadUnchanged':True,'installedExecutableUnchanged':True,
      'existingLaunchersNotUpdated':True,'releaseZipNotUpdated':True,'noDeletionOccurred':True,
      'naturalAlternateSelectionAccepted':False,'allStockFatalitiesAccepted':False,
      'establishedTwentyRegressionsOnThisCandidateAccepted':False,
      'allArenasAccepted':False,'fullTowerAccepted':False,
      'finalCombinedGameplayAndUIAccepted':False,'fullPortAccepted':False,
      'evidencePins':len(pins),'inputHashes':pins}
(OUT/'checkpoint.json').write_text(json.dumps(data,indent=2)+'\n')
for filename,wanted in pins.items():assert normal.digest(Path(filename))==wanted,filename
print(json.dumps({k:v for k,v in data.items()if k!='inputHashes'},indent=2))
