"""Freeze current bounded proofs without narrowing the full port objective."""
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_v1146_split_blood_and_mirror_checkpoint'
PREVIOUS=ROOT/'audit_v1126_owned_split_checkpoint/checkpoint.json'
if OUT.exists():raise ValueError('Never replace checkpoint evidence')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
pins={}
def pin(filename,wanted=None):
 path=Path(filename);actual=digest(path)
 assert wanted is None or actual==wanted,'Changed evidence '+str(path)
 assert str(path) not in pins or pins[str(path)]==actual,'Conflicting evidence '+str(path)
 pins[str(path)]=actual
previous=json.loads(PREVIOUS.read_text())
for filename,wanted in previous['inputHashes'].items():pin(filename,wanted)
pin(PREVIOUS)
reports=(
 ROOT/'audit_v1133_owned_split_blood_normal_checked/report.json',
 ROOT/'audit_v1135_controlled_split_alternate_checked/report.json',
 ROOT/'audit_v1137_actual_split_blood_pixels/report.json',
 ROOT/'audit_v1138_owned_split_blood_corruption_checks/report.json',
 ROOT/'audit_v1140_split_blood_actual_visual_review/review.json',
 ROOT/'audit_v1141_native_regressions_after_split_blood_checked/report.json',
 ROOT/'audit_v1144_natural_mirror_selection_checked/report.json',
 ROOT/'audit_v1147_natural_mirror_actual_visual_review/review.json',
)
data=[json.loads(path.read_text()) for path in reports]
assert data[0]['passed'] and len(data[0]['cases'])==4
assert data[1]['passed'] and len(data[1]['cases'])==4 and data[1]['controlledAlternateBranchAccepted'] and not data[1]['naturalAlternateSelectionAccepted']
assert data[2]['passed'] and data[2]['sceneCount']==136
assert data[3]['passed'] and len(data[3]['checks'])==13 and data[3]['runtimeEvidenceModified'] is False
assert data[4]['manualVisualReviewComplete'] and data[4]['sceneCount']==136
assert data[5]['passed'] and len(data[5]['cases'])==20
assert data[6]['passed'] and len(data[6]['cases'])==6 and data[6]['naturalMirrorAlternateSelectionAccepted']
assert data[7]['observedNaturalMirrorVisualReviewPassed'] and data[7]['sceneCount']==30
assert all(not r['fullPortAccepted'] for r in data)
for path,report in zip(reports,data):
 pin(path)
 for filename,wanted in report.get('inputHashes',{}).items():pin(filename,wanted)
candidate='diagnostic_v1130_owned_split_invariant_blood'
info_path=ROOT/candidate/'build-info.json'
info=json.loads(info_path.read_text(encoding='utf-8-sig'))
assert info['no_recompile_claimed']
for filename,wanted in info['input_hashes'].items():pin(filename,wanted)
for path in (info_path,ROOT/candidate/'mkport_candidate.exe',ROOT/candidate/'roms/mk2ks/mk2ks.mdata',
 ROOT/'STATUS_2026-10-03_SPLIT_BLOOD_AND_NATURAL_MIRRORS.md',ROOT/'mame-mkp/mkport.exe',
 ROOT/'PLAY_CURRENT_V786_TEST_BUILD.cmd',ROOT/'PLAY_LATEST_TEST_BUILD.cmd',ROOT/'PLAY_MK2_KANO_SONYA.cmd'):
 pin(path)
assert digest(ROOT/'mame-mkp/mkport.exe')=='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
tools=('tools/build_native_split_blood_v1128.py','tools/assemble_native_split_blood_candidate_v1129.ps1',
 'tools/run_native_split_blood_v1131.ps1','mk2ks_split_controlled_alt_v1132.lua',
 'tools/verify_native_split_blood_v1133.py','tools/verify_native_split_alt_v1135.py',
 'tools/run_native_regressions_v1136.ps1','tools/check_split_blood_pixels_v1137.py',
 'tools/test_native_split_blood_v1138.py','tools/save_split_blood_visual_review_v1140.py',
 'tools/verify_native_regressions_v1141.py','mk2ks_natural_mirror_v1142.lua',
 'tools/run_natural_mirror_v1143.ps1','tools/verify_natural_mirror_v1144.py',
 'tools/render_natural_mirror_review_v1145.py','tools/save_natural_mirror_visual_review_v1147.py',
 'tools/save_split_blood_checkpoint_v1146.py')
OUT.mkdir()
for filename in tools:
 path=ROOT/filename;pin(path)
 target=OUT/'input_sources'/filename;target.parent.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(path,target);pin(target)
record=dict(candidate=candidate,executableSHA256=info['executable_sha256'],payloadSHA256=info['payload_sha256'],
 historicalPinsRevalidated=len(previous['inputHashes']),currentNormalSplitCases=4,currentControlledAlternateSplitCases=4,
 actualSplitScenesReviewed=136,currentEstablishedNormalVictimRegressions=20,corruptionChecks=12,
 naturalMirrorCases=6,actualMirrorScenesReviewed=30,naturalMirrorAlternateSelectionAccepted=True,
 naturalAlternateFatalitiesAccepted=False,allStockFatalitiesAccepted=False,allArenasAccepted=False,
 allSelectionGraphicsAccepted=False,allFloorShadowsAccepted=False,fullPortAccepted=False,goalComplete=False,
 scope='Current normal/explicit controlled split, twenty normal Dead Pool victim regressions, and genuine cold same-character mirror selection only',
 launchersChanged=False,materialDataDeleted=False,inputHashes=pins)
(OUT/'checkpoint.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='inputHashes'},indent=2))
print('Pinned files:',len(pins))
