"""Preserve old failures and current bounded implementation/state/visual pass."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1228_native_headed_reaction_checkpoint';assert not OUT.exists()
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()
pins={}
def pin(path,wanted=None):
 path=Path(path);actual=digest(path);assert wanted is None or wanted==actual,'Changed evidence '+str(path)
 assert str(path) not in pins or pins[str(path)]==actual;pins[str(path)]=actual
previous_path=ROOT/'audit_v1216_stock_secondary_checkpoint/checkpoint.json';previous=json.loads(previous_path.read_text())
for file,wanted in previous['inputHashes'].items():pin(file,wanted)
pin(previous_path)
name='diagnostic_v1219_owned_native_headed_reaction';build_path=ROOT/name/'build-info.json';build=json.loads(build_path.read_text(encoding='utf-8-sig'));pin(build_path)
for file,wanted in build['input_hashes'].items():pin(file,wanted)
pin(ROOT/name/'mkport_candidate.exe',build['executable_sha256']);pin(ROOT/name/'roms/mk2ks/mk2ks.mdata',build['payload_sha256'])
assert build['executable_sha256']==previous['executableSHA256'] and build['payload_sha256']!=previous['payloadSHA256']
encoding_path=ROOT/'audit_v1221_native_headed_reaction_encoding_checked/report.json';encoding=json.loads(encoding_path.read_text());pin(encoding_path)
assert encoding['passed'] and encoding['candidate']==name and encoding['wholePayloadIndependentlyReconstructed'] and encoding['actualChangedBytes']==57 and encoding['allOtherPayloadBytesUnchanged'] and not encoding['gameInstructionsChanged']
for file,wanted in encoding['inputHashes'].items():pin(file,wanted)
state_path=ROOT/'audit_v1222_stock_secondary_state_checked/report.json';state=json.loads(state_path.read_text());pin(state_path)
assert state['passed'] and state['candidate']==name and state['stockScorpionSecondaryNormalDeadPoolPhysicalStateAccepted'] and len(state['cases'])==6 and not state['fullPortAccepted'] and not state['fullScreenDMAReplayAccepted']
for file,wanted in state['inputHashes'].items():pin(file,wanted)
negative_path=ROOT/'audit_v1224_stock_secondary_state_corruption_checks/report.json';negative=json.loads(negative_path.read_text());pin(negative_path)
assert negative['passed'] and len(negative['checks'])==10 and negative['inMemoryOnly'] and not negative['actualRuntimeEvidenceChanged']
review_path=ROOT/'audit_v1227_stock_secondary_visual_review/review.json';review=json.loads(review_path.read_text());pin(review_path)
assert review['passed'] and review['manualVisualReviewComplete'] and review['sceneCount']==102 and review['candidate']==name and review['allFiveHeadedBodyPosesActuallyDraw'] and not review['fullScreenDMAReplayAccepted']
for file,wanted in review['inputHashes'].items():pin(file,wanted)
for folder in ROOT.iterdir():
 if folder.is_dir() and folder.name.startswith(('audit_v1217_','audit_v1220_','audit_v1221_','audit_v1222_','audit_v1223_','audit_v1224_','audit_v1225_','audit_v1227_')):
  for path in folder.rglob('*'):
   if path.is_file():pin(path)
for filename in ('encode_native_headed_reaction_v1217.py','assemble_native_headed_reaction_v1218.ps1',
 'verify_native_headed_reaction_v1221.py','verify_stock_scorpion_secondary_v1222.py',
 'render_stock_secondary_contacts_v1223.py','test_stock_secondary_state_v1224.py',
 'save_stock_secondary_review_v1225.py','save_stock_secondary_review_v1227.py',
 'save_native_headed_reaction_checkpoint_v1228.py'):pin(ROOT/'tools'/filename)
pin(ROOT/'STATUS_2026-10-03_HEADED_REACTION_FIXED.md')
for filename in ('PLAY_CURRENT_V786_TEST_BUILD.cmd','PLAY_LATEST_TEST_BUILD.cmd','PLAY_MK2_KANO_SONYA.cmd','mame-mkp/mkport.exe','mame-mkp/src/mame/midway/midtunit_m.cpp'):
 path=ROOT/filename;assert str(path) in previous['inputHashes'];pin(path,previous['inputHashes'][str(path)])
record=dict(candidate=name,executableSHA256=build['executable_sha256'],payloadSHA256=build['payload_sha256'],
 previousCandidate=previous['candidate'],previousPayloadSHA256=previous['payloadSHA256'],historicalPinsRevalidated=len(previous['inputHashes']),
 currentPhysicalCases=6,actualScenesReviewed=102,stateNegativeChecks=9,actualChangedPayloadBytes=57,
 wholePayloadIndependentlyReconstructed=True,correctedHeadedReactionBlocks=6,gameDataChanged=True,compiledCodeChanged=False,
 stockScorpionSecondaryNormalDeadPoolPhysicalStateAccepted=True,correctedHeadedBodyReactionVisuallyAccepted=True,
 currentContinueScreenVisuallyAccepted=True,allFiveHeadedBodyPosesActuallyDraw=True,originalStockByteIdenticalCaptures=124,
 historicalFailedAppearancePreserved=True,preservedReviewPhaseAssertionException='audit_v1225_stock_secondary_review_exception/report.json',
 currentSecondaryFullScreenDMAReplayAccepted=False,allFatalityArtAccepted=False,alternateCostumesAccepted=False,
 affectedOrdinaryProjectileRegressionAccepted=False,otherPrimary55ConsumersAccepted=False,
 donorChoreographyAccepted=False,audioAccepted=False,allStockFatalitiesAccepted=False,allArenasAccepted=False,
 allSelectionGraphicsAccepted=False,allFloorShadowsAccepted=False,fullPortAccepted=False,goalComplete=False,
 launchersChanged=False,materialDataDeleted=False,inputHashes=pins)
OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(record,indent=2)+'\n')
print('Revalidated',record['historicalPinsRevalidated'],'prior pins; total',len(pins),
      'new headed-body data correction + six physical cases +102 actual reviewed scenes accepted; full port incomplete',flush=True)
