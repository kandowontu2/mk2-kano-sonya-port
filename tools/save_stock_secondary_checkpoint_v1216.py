"""Freeze the passing state gate AND failed actual appearance; goal incomplete."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1216_stock_secondary_checkpoint';assert not OUT.exists()
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()
pins={}
def pin(path,wanted=None):
 path=Path(path);actual=digest(path);assert wanted is None or wanted==actual,'Changed evidence '+str(path)
 assert str(path) not in pins or pins[str(path)]==actual
 pins[str(path)]=actual
previous_path=ROOT/'audit_v1205_stock_fire_checkpoint/checkpoint.json';previous=json.loads(previous_path.read_text())
for file,wanted in previous['inputHashes'].items():pin(file,wanted)
pin(previous_path)
state_path=ROOT/'audit_v1212_stock_secondary_state_checked/report.json';state=json.loads(state_path.read_text())
assert state['passed'] and state['stockScorpionSecondaryNormalDeadPoolPhysicalStateAccepted'] and len(state['cases'])==6 and not state['fullPortAccepted'] and not state['fullScreenDMAReplayAccepted']
pin(state_path)
for file,wanted in state['inputHashes'].items():pin(file,wanted)
negative_path=ROOT/'audit_v1214_stock_secondary_state_corruption_checks/report.json';negative=json.loads(negative_path.read_text())
assert negative['passed'] and len(negative['checks'])==10 and negative['inMemoryOnly'] and not negative['actualRuntimeEvidenceChanged']
pin(negative_path)
review_path=ROOT/'audit_v1215_stock_secondary_visual_review/review.json';review=json.loads(review_path.read_text())
assert not review['passed'] and review['manualVisualReviewComplete'] and review['sceneCount']==102 and not review['stockScorpionSecondaryNormalDeadPoolAppearanceAccepted']
assert sum(not c['naturalSecondaryAppearanceAccepted'] for c in review['cases'])==4
pin(review_path)
for file,wanted in review['inputHashes'].items():pin(file,wanted)
for folder in ROOT.iterdir():
 if folder.is_dir() and folder.name.startswith(('audit_v1207_','audit_v1209_','audit_v1211_','audit_v1212_','audit_v1213_','audit_v1214_','audit_v1215_')):
  for path in folder.rglob('*'):
   if path.is_file():pin(path)
for path in ROOT.glob('mk2ks_stock_scorpion_secondary*_v*.lua'):pin(path)
for pattern in ('run_stock_scorpion_secondary*.ps1','verify_stock_scorpion_secondary*.py','test_stock_secondary*.py','render_stock_secondary*.py','save_stock_secondary*.py'):
 for path in (ROOT/'tools').glob(pattern):pin(path)
pin(ROOT/'tools/build_mk2ks_mk3.py');pin(ROOT/'STATUS_2026-10-03_STOCK_SCORPION_SECONDARY_FAILURE.md')
for filename in ('PLAY_CURRENT_V786_TEST_BUILD.cmd','PLAY_LATEST_TEST_BUILD.cmd','PLAY_MK2_KANO_SONYA.cmd','mame-mkp/mkport.exe','mame-mkp/src/mame/midway/midtunit_m.cpp'):
 path=ROOT/filename;assert str(path) in previous['inputHashes'];pin(path,previous['inputHashes'][str(path)])
record=dict(candidate=previous['candidate'],executableSHA256=previous['executableSHA256'],payloadSHA256=previous['payloadSHA256'],
 historicalPinsRevalidated=len(previous['inputHashes']),currentPhysicalCases=6,actualScenesReviewed=102,stateNegativeChecks=9,
 stockScorpionSecondaryNormalDeadPoolPhysicalStateAccepted=True,stockScorpionSecondaryNormalDeadPoolAppearanceAccepted=False,
 verifiedImplementationDefect=review['failure'],nextRequiredImplementation=review['nextRequiredFix'],
 failedAppearanceCases=4,preservedFailedPhysicalAttempts=3,preservedPassingEarlierAttempt=1,
 fullScreenSecondaryDMAReplayAccepted=False,allFatalityArtAccepted=False,alternateCostumesAccepted=False,
 donorChoreographyAccepted=False,audioAccepted=False,allStockFatalitiesAccepted=False,allArenasAccepted=False,
 allSelectionGraphicsAccepted=False,allFloorShadowsAccepted=False,fullPortAccepted=False,goalComplete=False,
 gameCodeChanged=False,launchersChanged=False,materialDataDeleted=False,inputHashes=pins)
OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(record,indent=2)+'\n')
print('Revalidated',record['historicalPinsRevalidated'],'prior pins; total',len(pins),
      'secondary physical state passes; four true-victim appearances FAIL; next step is implementation, not more acceptance claims',flush=True)
