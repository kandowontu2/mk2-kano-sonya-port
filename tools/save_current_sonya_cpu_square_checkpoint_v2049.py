"""Save current naturally selected P2 Sonya Square Wave evidence, keep full goal active."""
import json,re
from pathlib import Path
import verify_current_sonya_p2_cpu_square_display_v2046 as current
ROOT=current.ROOT
PREVIOUS=ROOT/'audit_v2034_current_sonya_cpu_ring_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2049_current_sonya_cpu_square_checkpoint'
def save():
 prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'and not prior['fullPortAcceptance']
 pins=dict(prior['inputHashes'])
 def pin(file,wanted=None):
  path=Path(file);value=current.state.sha(path)
  assert wanted is None or value==wanted,'Changed evidence '+str(path)
  assert str(path)not in pins or pins[str(path)]==value,'Conflicting source '+str(path)
  pins[str(path)]=value
 pin(PREVIOUS)
 leaves=('audit_v2046_current_sonya_p2_cpu_square_display_kano_checked',
  'audit_v2044_current_sonya_p2_cpu_square_erase_checked',
  'audit_v2047_current_sonya_p2_cpu_square_counterexamples')
 proofs={}
 for leaf in leaves:
  path=ROOT/leaf/'report.json';p=json.loads(path.read_text())
  assert p['passed']and p['candidate']==prior['currentCandidate']and not p['fullPortAcceptance']
  for file,wanted in p['inputHashes'].items():pin(file,wanted)
  pin(path);proofs[leaf]=p
 scene,erase,counter=(proofs[leaf]for leaf in leaves)
 assert scene['sampledFrames']==scene['exactReplayedFrames']==erase['continuousExactPreBuffers']==erase['continuousExactFlips']==84
 assert erase['oneInitialBaseOnly']and not erase['laterBuffersUsedAsAnchors']
 assert not scene['heldOriginalScanouts']and scene['allOriginalBicyclePosesVisible']if 'allOriginalBicyclePosesVisible'in scene else scene['allOriginalSquarePosesVisible']
 assert len(counter['counterexamples'])==41 and all(r['rejected']for r in counter['counterexamples'])
 source=ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp'
 assert re.search(r'#define\s+STBIT_C\s+\(1\s*<<\s*30\)',source.read_text()),'Observed carry bit is actual host CPU source'
 pin(source)
 discoveries={}
 for leaf in('audit_v2037_sonya_p2_cpu_choice_guard_wait_kano','audit_v2048_sonya_p2_cpu_choice_guard_wait_mirror'):
  folder=ROOT/leaf;meta=current.state.matched(folder,pins)
  log=(folder/'run.log').read_text(encoding='utf-8-sig')
  events=current.square.original.rows(log,'EVENT')
  discoveries[leaf]=dict(human=meta['player'],approach=meta['approach'],policy=meta['policy'],terminalExit=meta['exit_code'],
   signatures=[dict(kind=r['kind'],frame=r['frame'],id=r['id'])for r in events if r['kind']in('square','bicycle','ring')],
   fullCaptureAcceptance=(leaf.endswith('_kano')),mirrorContactRenderRecoveryAccepted=False)
 failed=ROOT/'audit_v2043_current_sonya_p2_cpu_square_display_kano_checked/report.json'
 p=json.loads(failed.read_text());assert not p['passed'];pin(failed)
 for name in('tools/current_sonya_cpu_square_contract_v2042.py','tools/verify_current_sonya_p2_cpu_square_display_v2043.py',
  'tools/current_sonya_cpu_square_contract_v2045.py','tools/verify_current_sonya_p2_cpu_square_display_v2046.py',
  'tools/check_current_sonya_p2_cpu_square_erase_v2044.py','tools/test_current_sonya_p2_cpu_square_v2047.py',
  'mk2ks_physical_p2_cpu_square_trace_v2038.lua','mk2ks_physical_p2_cpu_square_display_v2039.lua',
  'tools/run_current_physical_p2_cpu_square_display_v2040.ps1','mk2ks_physical_p2_cpu_choice_trace_v2035.lua',
  'tools/run_current_physical_p2_cpu_choice_v2036.ps1'):
  pin(ROOT/name)
 pin(Path(__file__).resolve())
 for file,wanted in pins.items():assert current.state.sha(file)==wanted,'Changed authoritative input '+file
 return dict(goalStatus='active',objective=prior['objective'],previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='no progress: answered the user status request after checking latest evidence; did not change the playable build or complete another acceptance gate',
  thisGoalTurnClassification='progress: obtained genuine P2 Sonya CPU Square Wave from native RNG under physical human input; all54 active and30 post-regain scanouts/source/FIFO/palettes/shadows/continuous erase pass and all41 corruptions rejected; mirror natural choice discovery retained separately',
  currentCandidate=prior['currentCandidate'],currentCMD=prior['currentCMD'],currentPlaytestZIP=prior['currentPlaytestZIP'],
  gameSourceAndPlayableBytesChangedThisTurn=False,currentP2SonyaSquare=scene['state'],
  totalSampledFrames=scene['sampledFrames'],exactScreenPixels=scene['exactScreenPixels'],exactOwnedPixels=scene['exactOwnedPixels'],
  fullPhysicalPaletteChecks=scene['fullPhysicalPaletteChecks'],sourceBoundProjections=scene['sourceBoundProjections'],
  nativeShadowCopies=scene['nativeShadowCopies'],nativeShiftTransfers=erase['nativeShiftTransfers'],
  originalDonorPieces=scene['originalHeldDonorPieces'],counterexamplesRejected=41,
  acceptedReports={leaf:str(ROOT/leaf/'report.json')for leaf in leaves},
  failedAttemptsPreserved={str(failed):dict(error=p['error'],correction='Fresh2045 adds actual hexadecimal schedule parsing;2046 binds exact1997 extended exit condition. No guest/capture changes or relaxed state/render requirements.')},
  naturalChoiceDiscoveries=discoveries,
  scopeCaveats=[
   'Only one actual P2 Sonya CPU Square MISS against true human P1 Kano at Dead Pool is newly accepted. Hits, blocks, interrupts, mirror and other arenas/audio remain separate gates.',
   'Actual native first RNG result274 fails250; second98 passes400, choosing Square without prescribed CPU ID/action/RNG.',
   'Eight12px rise fields,26flight checks at10px/field, original2px/0.5px drop, first landing2385 and four full landing holds precede clean regained control2389.',
   'All84consecutive scenes2336..2419 are independently source/FIFO/queued-camera/palette/scanout checked. All7225original compressed shadow copies and10668original clear transfers pass from one initial buffer, with no later buffers used as anchors.',
   'Normal control resumes with cleared locks; exact initial ownership and native floor anchors remain stable. No arbitrary Y or camera offset was applied.',
   'Mirror discovery uses alternate costume and naturally chose two bicycle kicks2038/2266 and ring3323, not Square. It is pinned discovery, not acceptance of those contacts or graphics.',
   'New evidence is losslessly NTFS compressed; no old directory, source gameplay, executable, ROM, CMD or playtest ZIP was changed.',
   'The full original natural-in-all-aspects objective is unchanged. Remaining contacts/AI/moves/arenas/audio, finishers/victims/morphs/secrets/cinematics, genuine boss/campaign/own-ending/attract, final cleanup/regression/release remain open.'],
  remaining=prior['remaining'],
  nextAction='Prioritize genuine current-build campaign/boss progression and remaining contact/interrupt/CPU/arena/audio coverage. Keep native Square-hit/block/interrupt and mirror cases separate; finish remaining finishers/victims/morphs/secrets/cinematics, actual boss clears/own endings/attract, dependency-aware obsolete builds and final release regression.',
  inputHashes=pins,allCPUAccepted=False,allRepeatedCPUAccepted=False,allKOCasesAccepted=False,
  allMoveArtGroundShadowAudioAccepted=False,actualFullLadderClearAccepted=False,actualEndingsAccepted=False,
  allFinishersVictimsMorphsSecretsCinematicsAccepted=False,allOldBuildFoldersRemoved=False,finishedRelease=False,fullPortAcceptance=False)
if __name__=='__main__':
 assert not OUT.exists(),'Preserve immutable checkpoint'
 result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k]for k in('goalStatus','totalSampledFrames','nativeShadowCopies','nativeShiftTransfers','counterexamplesRejected','finishedRelease')}),flush=True)

