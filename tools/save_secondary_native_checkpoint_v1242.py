"""Revalidate the entire previous checkpoint and pin new native/human proof."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1242_secondary_native_human_checkpoint';assert not OUT.exists()
pins={}
def digest(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as stream:
  for block in iter(lambda:stream.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest().upper()
def pin(path,wanted=None):
 path=Path(path);key=str(path)
 actual=pins[key] if key in pins else digest(path)
 assert wanted is None or actual==wanted,'Changed evidence '+key
 pins[key]=actual
previous_path=ROOT/'audit_v1228_native_headed_reaction_checkpoint/checkpoint.json';previous=json.loads(previous_path.read_text())
print('Revalidating',len(previous['inputHashes']),'prior evidence pins',flush=True)
for file,wanted in previous['inputHashes'].items():pin(file,wanted)
pin(previous_path)
name=previous['candidate'];build_path=ROOT/name/'build-info.json';build=json.loads(build_path.read_text(encoding='utf-8-sig'));pin(build_path)
assert name=='diagnostic_v1219_owned_native_headed_reaction' and build['executable_sha256']==previous['executableSHA256'] and build['payload_sha256']==previous['payloadSHA256']
pin(ROOT/name/'mkport_candidate.exe',build['executable_sha256']);pin(ROOT/name/'roms/mk2ks/mk2ks.mdata',build['payload_sha256'])
render=[]
for key in ('control_kitana_p1','control_liu_p2','kano_p1','kano_p2','sonya_p1','sonya_p2'):
 path=ROOT/f'audit_v1234_secondary_{key}_render_checked/report.json';report=json.loads(path.read_text());pin(path)
 assert report['passed'] and report['candidate']==name and report['currentSecondarySampledFullNativeRenderAccepted'] and not report['fullPortAccepted']
 assert all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in report['replayed']['records'])
 for file,wanted in report['inputHashes'].items():pin(file,wanted)
 render.append(report)
for key in ('sonya_p1','sonya_p2'):
 path=ROOT/f'audit_v1232_secondary_{key}_render_checked/report.json';report=json.loads(path.read_text());pin(path)
 assert report['passed'] is False and 'Unbound captured graphics region 0x1f2a484' in report['error']
negative_path=ROOT/'audit_v1235_stock_secondary_render_corruption_checks/report.json';negative=json.loads(negative_path.read_text());pin(negative_path)
assert negative['passed'] and len(negative['checks'])==13 and negative['inMemoryOnly'] and not negative['actualRuntimeEvidenceChanged']
review_path=ROOT/'audit_v1239_secondary_native_visual_review/review.json';review=json.loads(review_path.read_text());pin(review_path)
assert review['passed'] and review['manualReviewComplete'] and review['sceneEntriesReviewed']==72 and review['uniqueActualImagesReviewed']==66
for file,wanted in review['inputHashes'].items():pin(file,wanted)
human_path=ROOT/'audit_v1241_current_human_negative_checked/report.json';human=json.loads(human_path.read_text());pin(human_path)
assert human['passed'] and human['candidate']==name and human['positiveCases']==18 and human['negativeCases']==34 and human['current52CaseHumanStateMatrixAccepted'] and not human['fullPortAccepted']
for file,wanted in human['inputHashes'].items():pin(file,wanted)
human_negative_path=ROOT/'audit_v1243_current_human_matrix_corruption_checks/report.json';human_negative=json.loads(human_negative_path.read_text());pin(human_negative_path)
assert human_negative['passed'] and human_negative['testsRun']==9 and human_negative['inMemoryOnly'] and not human_negative['actualRuntimeEvidenceChanged']
for folder in ROOT.iterdir():
 if folder.is_dir() and folder.name.startswith(('audit_v1230_','audit_v1232_','audit_v1234_','audit_v1235_','audit_v1236_','audit_v1237_','audit_v1238_','audit_v1239_','audit_v1240_','audit_v1241_','audit_v1243_')):
  for path in folder.rglob('*'):
   if path.is_file():pin(path)
for filename in ('tools/run_stock_secondary_display_v1230.ps1','mk2ks_stock_secondary_full_display_v1229.lua',
 'tools/inspect_secondary_display_v1231.py','tools/verify_stock_secondary_display_v1232.py',
 'tools/test_stock_secondary_render_v1233.py','tools/verify_stock_secondary_display_v1234.py',
 'tools/test_stock_secondary_render_v1235.py','tools/render_secondary_native_contacts_v1237.py',
 'tools/verify_current_human_moves_v1238.py','tools/save_secondary_native_review_v1239.py',
 'tools/run_current_human_negative_v1240.ps1','tools/verify_current_human_negative_v1241.py',
 'tools/save_secondary_native_checkpoint_v1242.py','tools/test_current_human_matrix_v1243.py',
 'STATUS_2026-10-03_SECONDARY_NATIVE_AND_HUMAN_REGRESSION.md'):
 pin(ROOT/filename)
record=dict(candidate=name,executableSHA256=build['executable_sha256'],payloadSHA256=build['payload_sha256'],
 historicalPinsRevalidated=len(previous['inputHashes']),currentPhysicalSecondaryCases=6,
 exactNativeReplayedFields=sum(r['replayed']['frames'] for r in render),heldScanouts=sum(len(r['heldScanout']) for r in render),
 nativeVictimTorsoPaletteSamples=sum(r['paletteSamples'] for r in render),renderCorruptionCounterexamples=12,
 actualVisualSceneEntriesReviewed=72,uniqueActualImagesReviewed=66,currentHumanPositiveCases=18,currentHumanNegativeCases=34,
 humanPairedFields=human['pairedFields'],humanCorruptionCounterexamples=8,
 wholePayloadIndependentlyReconstructed=True,originalDetachedTorsoOwnershipAccepted=True,
 currentSecondarySampledFullNativeRenderAccepted=True,current52CaseHumanStateMatrixAccepted=True,
 currentKnifeRingPhysicalRegressionAccepted=True,affectedOrdinaryProjectileFullGraphicsRegressionAccepted=False,
 otherPrimary55ConsumersAccepted=False,allFatalityArtAccepted=False,alternateCostumesAccepted=False,
 donorChoreographyAccepted=False,audioAccepted=False,allStockFatalitiesAccepted=False,allArenasAccepted=False,
 allSelectionGraphicsAccepted=False,allFloorShadowsAccepted=False,fullPortAccepted=False,goalComplete=False,
 gameDataChanged=False,compiledCodeChanged=False,launchersChanged=False,materialDataDeleted=False,
 preservedFailedBoundaryReports=['audit_v1232_secondary_sonya_p1_render_checked/report.json','audit_v1232_secondary_sonya_p2_render_checked/report.json'],inputHashes=pins)
assert record['exactNativeReplayedFields']==986 and record['heldScanouts']==16 and record['nativeVictimTorsoPaletteSamples']==542
OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(record,indent=2)+'\n')
print('Checkpoint saved; total pins',len(pins),'986 exact rendered fields +16 held +52 current human cases. Full goal incomplete.',flush=True)
