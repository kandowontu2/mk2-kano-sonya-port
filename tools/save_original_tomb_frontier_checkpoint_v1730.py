"""Preserve full goal and current accepted proof; original Tomb variant identified."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1730_original_tomb_frontier_checkpoint'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb')as stream:
  for b in iter(lambda:stream.read(1048576),b''):h.update(b)
 return h.hexdigest().upper()
if __name__=='__main__':
 assert not OUT.exists();pins={}
 def pin(p,h=None):
  p=Path(p);key=str(p.resolve())
  if key not in pins:pins[key]=sha(p)
  assert h is None or h.upper()==pins[key],'Changed evidence '+key
 priorpath=ROOT/'audit_v1725_current_babality_arena_checkpoint/checkpoint.json';pin(priorpath)
 prior=json.loads(priorpath.read_text());assert prior['goalStatus']=='active'
 proofpath=ROOT/'audit_v1726_original_tomb_drop_checked/report.json';pin(proofpath)
 proof=json.loads(proofpath.read_text());assert proof['passed']and proof['originalRandomTombDropCauseAccepted']and not proof['heldPredicateChanged']
 for p,h in proof['inputHashes'].items():pin(p,h)
 cleanpath=ROOT/'audit_v1729_completed_capture_log_compression/report.json';pin(cleanpath)
 clean=json.loads(cleanpath.read_text(encoding='utf-8-sig'));assert clean['passed']and clean['allContentHashesUnchanged']and clean['deletedFiles']==0
 for r in clean['files']:assert r['shaBefore']==r['shaAfter'];pin(r['path'],r['shaAfter'])
 for p,h in {
  'diagnostic_v1597_native_ground_throw/mkport_candidate.exe':'9D2E9849CA3A98AA06018DB2EF3EE65397A5C9EC95C466CFD999C9091237B695',
  'diagnostic_v1597_native_ground_throw/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
  'PLAY_CURRENT_V1597_TEST_BUILD.cmd':'85962962ADA430B706B4052A28A8809D1E53EF3D98FE3C44831D709898375DAB'}.items():pin(ROOT/p,h)
 pin(__file__)
 report={k:v for k,v in prior.items()if k not in('inputHashes','pendingCase')}
 report.update(thisGoalTurnClassification='progress: current Babality and four nine-arena sampled gates accepted; native scaling source-model verified; 20-case stage regression dispatched and original random Tomb exception causally proved; further lossless disk reclamation',
  originalRandomTombDropCauseAccepted=True,currentFullStageMatrixAccepted=False,
  tombException='Original MK2 random threshold 50, actual random result 25, unpressed native controls, original 128-field hold +112-field slow fall +native gravity/floor landing. Not a port fault. Historical hold-only matrix still preserved as failed; combined hold/drop matrix proof remains next.',
  pendingCaptures=[],cleanupAllocatedBytesReclaimed=prior['cleanupAllocatedBytesReclaimed']+clean['reclaimedBytes'],
  cleanupAdditionalBytesReclaimedThisTurn=clean['reclaimedBytes'],deletedFilesThisTurn=0,allOldBuildFoldersRemoved=False,
  nextAction='Complete independent combined held/drop stage matrix acceptance while retaining all other original state/retirement predicates; then broader cinematic/move-phase/campaign progression work.',
  inputHashes=pins,previousCheckpointSHA=pins[str(priorpath.resolve())],fullPortAcceptance=False)
 report['acceptedReports']=dict(prior['acceptedReports']);report['acceptedReports']['audit_v1726_original_tomb_drop_checked']=dict(reportSHA=pins[str(proofpath.resolve())],scope=proof['scope'],fullPortAcceptance=False)
 OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(saved=str(OUT/'checkpoint.json'),pins=len(pins),additionalReclaimedBytes=clean['reclaimedBytes'],totalReclaimedBytes=report['cleanupAllocatedBytesReclaimed'],goalStatus='active',fullStageMatrixAccepted=False,fullPortAcceptance=False),indent=2))
