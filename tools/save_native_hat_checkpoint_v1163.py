"""Revalidate prior pins and freeze the current bounded native hat evidence."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_v1163_native_hat_checkpoint'
assert not OUT.exists(), 'Preserve checkpoints'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
pins={}
def pin(path,wanted=None):
 path=Path(path);actual=digest(path)
 assert wanted is None or actual==wanted, 'Changed evidence '+str(path)
 assert str(path) not in pins or pins[str(path)]==actual
 pins[str(path)]=actual
previous_path=ROOT/'audit_v1146_split_blood_and_mirror_checkpoint/checkpoint.json'
previous=json.loads(previous_path.read_text())
for filename,wanted in previous['inputHashes'].items():pin(filename,wanted)
pin(previous_path)
for folder in ('audit_v1158_native_hat_kill_checked','audit_v1160_native_hat_corruption_checks','audit_v1162_native_hat_visual_review'):
 path=ROOT/folder/('review.json' if 'visual_review' in folder else 'report.json')
 data=json.loads(path.read_text());assert data.get('passed',data.get('observedNativeHatVisualReviewPassed',False))
 assert not data['fullPortAccepted'];pin(path)
 for filename,wanted in data.get('inputHashes',{}).items():pin(filename,wanted)
failed=ROOT/'audit_v1157_native_hat_kill_checked/report.json'
assert not json.loads(failed.read_text())['passed'];pin(failed)
for folder in ROOT.iterdir():
 if folder.is_dir() and (folder.name.startswith('audit_v1150_') or folder.name.startswith('audit_v1152_')):
  for path in folder.rglob('*'):
   if path.is_file():pin(path)
for file in ('mk2ks_stock_hat_inputs_v1148.lua','mk2ks_stock_hat_display_v1149.lua',
 'mk2ks_stock_hat_trace_v1151.lua','mk2ks_stock_hat_inputs_v1153.lua',
 'mk2ks_stock_hat_display_v1154.lua','mk2ks_stock_hat_trace_v1155.lua',
 'tools/run_stock_hat_v1150.ps1','tools/run_stock_hat_v1156.ps1',
 'tools/verify_native_hat_kill_v1157.py','tools/verify_native_hat_kill_v1158.py',
 'tools/test_native_hat_kill_v1160.py','tools/render_native_hat_review_v1161.py',
 'tools/save_native_hat_visual_review_v1162.py','tools/save_native_hat_checkpoint_v1163.py',
 'audit_v1161_native_hat_actual_contacts/inventory.json','STATUS_2026-10-03_CURRENT_NATIVE_HAT_KILL.md'):
 pin(ROOT/file)
record=dict(candidate=previous['candidate'],executableSHA256=previous['executableSHA256'],
 payloadSHA256=previous['payloadSHA256'],historicalPinsRevalidated=len(previous['inputHashes']),
 normalNativeHatCases=6,ownedCharacterSlotsVerified=4,actualScenesReviewed=128,
 corruptionChecks=8,genuineNativeHatKillAccepted=True,naturalAlternateFatalitiesAccepted=False,
 allStockFatalitiesAccepted=False,allArenasAccepted=False,allSelectionGraphicsAccepted=False,
 allFloorShadowsAccepted=False,fullPortAccepted=False,goalComplete=False,
 gameCodeChanged=False,launchersChanged=False,materialDataDeleted=False,inputHashes=pins)
OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(record,indent=2)+'\n')
print('Prior pins revalidated:',record['historicalPinsRevalidated'],'New total:',len(pins))
