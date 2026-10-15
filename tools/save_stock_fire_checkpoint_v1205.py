"""Freeze current original-fire evidence; retain full official-roster objective."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1205_stock_fire_checkpoint';assert not OUT.exists()
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()
pins={}
def pin(path,wanted=None):
 path=Path(path);actual=digest(path);assert wanted is None or wanted==actual,'Changed evidence '+str(path)
 assert str(path) not in pins or pins[str(path)]==actual
 pins[str(path)]=actual
previous_path=ROOT/'audit_v1182_natural_mirror_finish_checkpoint/checkpoint.json';previous=json.loads(previous_path.read_text())
for file,wanted in previous['inputHashes'].items():pin(file,wanted)
pin(previous_path)
case_keys=(('control_kitana',1),('control_liu',2),('kano',1),('kano',2),('sonya',1),('sonya',2));reports=[]
for name,side in case_keys:
 path=ROOT/f'audit_v1201_fire_{name}_p{side}_render_checked/report.json';report=json.loads(path.read_text());assert report['passed'] and report['stockFireNormalDeadPoolSampledRenderAccepted'] and not report['fullPortAccepted'];reports.append(report);pin(path)
 for file,wanted in report['inputHashes'].items():pin(file,wanted)
controls={r['victimSlot']:r for r in reports if r['trueVictimID'] in (1,4)}
for report in reports:
 assert report['burnGeometry']==controls[report['victimSlot']]['burnGeometry']
 assert report['burnPaletteSamples']==44 and report['postRetirementReplayedSamples']>=8
 assert all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in report['replayed']['records'])
negative_path=ROOT/'audit_v1203_stock_fire_render_corruption_checks/report.json';negative=json.loads(negative_path.read_text());assert negative['passed'] and len(negative['checks'])==9 and negative['inMemoryOnly'] and not negative['actualRuntimeEvidenceChanged'];pin(negative_path)
review_path=ROOT/'audit_v1204_stock_fire_visual_review/review.json';review=json.loads(review_path.read_text());assert review['manualVisualReviewComplete'] and review['sceneCount']==192 and review['currentContinueScreenVisuallyAccepted'];pin(review_path)
for file,wanted in review['inputHashes'].items():pin(file,wanted)
# All attempts, including wrong distance, early command and insufficient
# observers, remain immutable evidence. Never rewrite them into passes.
versions=('audit_v1184_','audit_v1186_','audit_v1188_','audit_v1190_','audit_v1192_','audit_v1194_','audit_v1197_','audit_v1199_','audit_v1200_','audit_v1201_','audit_v1202_','audit_v1203_','audit_v1204_')
for folder in ROOT.iterdir():
 if folder.is_dir() and folder.name.startswith(versions):
  for path in folder.rglob('*'):
   if path.is_file():pin(path)
for path in ROOT.glob('mk2ks_stock_fire*_v*.lua'):pin(path)
for pattern in ('run_stock_fire*.ps1','verify_stock_fire*.py','test_stock_fire*.py','render_stock_fire*.py','save_stock_fire*.py'):
 for path in (ROOT/'tools').glob(pattern):pin(path)
pin(ROOT/'STATUS_2026-10-03_STOCK_SCORPION_FIRE.md')
for filename in ('PLAY_CURRENT_V786_TEST_BUILD.cmd','PLAY_LATEST_TEST_BUILD.cmd','PLAY_MK2_KANO_SONYA.cmd','mame-mkp/mkport.exe','mame-mkp/src/mame/midway/midtunit_m.cpp'):
 path=ROOT/filename;assert str(path) in previous['inputHashes'];pin(path,previous['inputHashes'][str(path)])
record=dict(candidate=previous['candidate'],executableSHA256=previous['executableSHA256'],payloadSHA256=previous['payloadSHA256'],
 historicalPinsRevalidated=len(previous['inputHashes']),currentPhysicalCases=6,currentFreshRenderCases=6,
 exactReplayedFields=sum(r['replayed']['frames'] for r in reports),heldScanoutSamples=sum(len(r['heldScanout']) for r in reports),
 postRetirementReplayedSamples=sum(r['postRetirementReplayedSamples'] for r in reports),actualScenesReviewed=192,renderNegativeChecks=8,
 stockFireNormalDeadPoolSampledRenderAccepted=True,currentContinueScreenVisuallyAccepted=True,
 preservedVerifierExceptions=[{'source':'tools/verify_stock_fire_v1195.py','error':'FileNotFoundError: original graphics chips are in the parent mk2.zip, not roms/mk2ks'},
 {'source':'tools/verify_stock_fire_v1196.py','error':'struct.error: only the first burn descriptor carries the embedded palette pointer; later poses retain the assigned palette'}],
 allFatalityArtAccepted=False,alternateFireVictimsAccepted=False,donorChoreographyAccepted=False,audioAccepted=False,
 allStockFatalitiesAccepted=False,allArenasAccepted=False,allSelectionGraphicsAccepted=False,allFloorShadowsAccepted=False,
 fullPortAccepted=False,goalComplete=False,gameCodeChanged=False,launchersChanged=False,materialDataDeleted=False,inputHashes=pins)
OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(record,indent=2)+'\n')
print('Revalidated',record['historicalPinsRevalidated'],'prior pins; total',len(pins),'current fire sampled gate accepted; full port incomplete')
