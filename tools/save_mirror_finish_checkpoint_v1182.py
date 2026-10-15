"""Freeze current natural mirror evidence without claiming full-port completion."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1182_natural_mirror_finish_checkpoint'
assert not OUT.exists(),'Preserve checkpoints'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
pins={}
def pin(path,wanted=None):
 path=Path(path);actual=digest(path)
 assert wanted is None or actual==wanted,'Changed evidence '+str(path)
 assert str(path) not in pins or pins[str(path)]==actual
 pins[str(path)]=actual
previous_path=ROOT/'audit_v1163_native_hat_checkpoint/checkpoint.json'
previous=json.loads(previous_path.read_text())
for file,wanted in previous['inputHashes'].items():pin(file,wanted)
pin(previous_path)
reports=[ROOT/'audit_v1169_natural_mirror_finish_checked/report.json',
 ROOT/'audit_v1171_natural_mirror_finish_corruption_checks/report.json',
 ROOT/'audit_v1172_natural_mirror_finish_visual_review/review.json',
 ROOT/'audit_v1180_natural_mirror_render_corruption_checks/report.json',
 ROOT/'audit_v1181_current_mirror_render_visual_review/review.json']
reports += [ROOT/f'audit_v1179_{name}_mirror_finish_p{side}_render_checked/report.json' for name in ('kano','sonya') for side in (1,2)]
data=[json.loads(path.read_text()) for path in reports]
assert data[0]['passed'] and len(data[0]['cases'])==4
assert data[1]['passed'] and len(data[1]['checks'])==8 and not data[1]['actualRuntimeEvidenceChanged']
assert data[2]['manualVisualReviewComplete'] and data[2]['sceneCount']==124
assert data[3]['passed'] and len(data[3]['checks'])==9 and not data[3]['actualRuntimeEvidenceChanged']
assert data[4]['manualVisualReviewComplete'] and data[4]['sceneCount']==128 and data[4]['currentContinueScreenVisuallyAccepted']
assert all(r['passed'] and r['replayed']['frames']==165 and r['postTransitionReplayedSamples']==10 for r in data[5:])
assert all(not r['fullPortAccepted'] for r in data)
for path,report in zip(reports,data):
 pin(path)
 for file,wanted in report.get('inputHashes',{}).items():pin(file,wanted)
for folder in ('audit_v1168_natural_mirror_finish_checked','audit_v1175_sonya_mirror_finish_p2_render_checked'):
 path=ROOT/folder/'report.json';assert not json.loads(path.read_text())['passed'];pin(path)
for folder in ROOT.iterdir():
 if folder.is_dir() and (folder.name.startswith('audit_v1165_') or folder.name.startswith('audit_v1174_')):
  for path in folder.rglob('*'):
   if path.is_file():pin(path)
for filename in ('mk2ks_natural_mirror_finish_v1164.lua','mk2ks_natural_mirror_finish_v1166.lua',
 'mk2ks_natural_mirror_finish_display_v1173.lua','mk2ks_natural_mirror_finish_display_v1176.lua',
 'tools/run_natural_mirror_finish_v1165.ps1','tools/run_natural_mirror_finish_v1167.ps1',
 'tools/verify_natural_mirror_finish_v1168.py','tools/verify_natural_mirror_finish_v1169.py',
 'tools/render_natural_mirror_finish_v1170.py','tools/test_natural_mirror_finish_v1171.py',
 'tools/save_natural_mirror_finish_visual_review_v1172.py',
 'tools/run_natural_mirror_finish_display_v1174.ps1','tools/verify_natural_mirror_finish_display_v1175.py',
 'tools/run_natural_mirror_finish_display_v1177.ps1','tools/verify_natural_mirror_finish_display_v1179.py',
 'tools/test_natural_mirror_render_v1180.py','tools/save_mirror_render_review_v1181.py',
 'tools/save_mirror_finish_checkpoint_v1182.py','audit_v1170_natural_mirror_finish_contacts/inventory.json',
 'STATUS_2026-10-03_CURRENT_NATURAL_MIRROR_FINISHERS.md'):
 pin(ROOT/filename)
record=dict(candidate=previous['candidate'],executableSHA256=previous['executableSHA256'],payloadSHA256=previous['payloadSHA256'],
 historicalPinsRevalidated=len(previous['inputHashes']),naturalMirrorFinisherCases=4,
 freshMirrorRenderCases=4,exactReplayedFields=660,heldScanoutSamples=10,
 postRetirementReplayedSamples=40,actualScenesReviewed=128,stateNegativeChecks=7,renderNegativeChecks=8,
 naturalMirrorSampledRenderAccepted=True,allFatalityArtAccepted=False,donorChoreographyAccepted=False,
 audioAccepted=False,allStockFatalitiesAccepted=False,allArenasAccepted=False,
 allSelectionGraphicsAccepted=False,allFloorShadowsAccepted=False,fullPortAccepted=False,
 goalComplete=False,gameCodeChanged=False,launchersChanged=False,materialDataDeleted=False,inputHashes=pins)
OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(record,indent=2)+'\n')
print('Revalidated',record['historicalPinsRevalidated'],'prior pins; total',len(pins),'full port incomplete')
