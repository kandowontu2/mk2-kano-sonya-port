"""Save bounded clean human uppercut render/shadow progress; full port remains active."""
import json
from pathlib import Path
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
PREVIOUS=ROOT/'audit_v2150_current_human_uppercut_progress_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2173_current_uppercut_render_shadow_checkpoint'
def save():
 prior=json.loads(PREVIOUS.read_text())
 assert prior['goalStatus']=='active'and prior['fullPortAcceptance']is False
 pins=dict(prior['inputHashes'])
 def pin(path,wanted=None):
  path=str(Path(path).resolve());actual=launch.sha(path)
  assert wanted is None or actual==wanted,'Changed checkpoint dependency '+path
  assert path not in pins or pins[path]==actual,'Conflicting checkpoint dependency '+path
  pins[path]=actual
 def accept(path):
  path=Path(path);r=json.loads(path.read_text())
  assert r['passed']and r['fullPortAcceptance']is False
  for file,wanted in r['inputHashes'].items():pin(file,wanted)
  pin(path);return r
 pin(PREVIOUS);pin(__file__)
 cases={}
 for case in ('kano_p1','kano_p2','sonya_p1','sonya_p2'):
  smoke_path=ROOT/f'audit_v2155_current_uppercut_{case}_checked/report.json'
  initial_path=ROOT/f'audit_v2160_current_uppercut_{case}_full_render_checked/report.json'
  latest_path=ROOT/f'audit_v2170_current_uppercut_{case}_shadow_pose_checked/report.json'
  negative_path=ROOT/f'audit_v2162_current_uppercut_{case}_render_counterexamples/report.json'
  smoke=accept(smoke_path);initial=accept(initial_path);latest=accept(latest_path);negative=accept(negative_path)
  assert smoke['boundedCleanUppercutAccepted']and smoke['humanUppercutAction']=='0107'
  assert initial['state']==latest['state']and latest['state']['nativeContactDamage']==40
  assert latest['unchangedPhysicalControl']and latest['boundedUppercutPhaseRenderAccepted']
  assert latest['interPassEraseAcceptance']and latest['continuousErase']['oneInitialBaseOnly']
  assert latest['continuousErase']['laterBuffersUsedAsAnchors']is False
  assert latest['exactConsecutiveScanouts']==latest['exactNativeReplayedPasses']
  assert not latest['heldOriginalScanouts']and latest['sourceBoundNativeClippedParts']==0
  assert negative['rejectedSpecificCounterexamples']==12 and negative['finalUnmockedFullReplayPassed']
  cases[case]=dict(smokeReport=str(smoke_path),firstFullRenderReport=str(initial_path),
   currentDrawtimeRenderReport=str(latest_path),renderCounterexampleReport=str(negative_path),
   state=latest['state'],sourceExactScanouts=latest['exactConsecutiveScanouts'],
   sourceExactScreenPixels=latest['exactConsecutiveScanouts']*400*254,
   nativeShadowCopies=latest['nativeShadowCopies'],nativeShadowComponents=latest['nativeShadowComponents'],
   originalContinuousClear=latest['continuousErase'],fullOwnedPaletteChecks=latest['fullOwnedPaletteChecks'],
   rejectedSpecificRenderCounterexamples=12,ordinaryWalkJumpPunchFollowupAccepted=True,
   allMoveArenaGroundShadowAudioAccepted=False)
 own_path=ROOT/'audit_v2172_current_uppercut_drawtime_shadow_coverage/report.json'
 own=accept(own_path)
 assert own['rejectedSpecificCounterexamples']==24 and own['totalOwnShadowCopies']==31545
 for case,row in own['cases'].items():
  assert row['everyActualOwnShadowPoseComponentProjected']and row['rejectedSpecificCounterexamples']==6
  assert row['ownShadowCopies']==cases[case]['nativeShadowCopies']
  cases[case]['actualDrawtimeShadowCoverage']=row
 failed_path=ROOT/'audit_v2164_current_uppercut_owned_shadow_coverage/report.json'
 failed=json.loads(failed_path.read_text());assert failed['passed']is False
 assert 'Every actual own visible body component' in failed['error']
 pin(failed_path);pin(ROOT/'tools/verify_current_uppercut_owned_shadow_coverage_v2163.py')
 expected={
  ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 for path,wanted in expected.items():pin(path,wanted)
 for file,wanted in pins.items():assert launch.sha(file)==wanted,'Changed carried accepted evidence '+file
 launch.module_pins(pins)
 prior.update(previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='no progress: status-only response; revalidated current smoke and checkpoint before taking the next safe full-phase action',
  thisGoalTurnClassification='progress: all four clean human uppercuts,514consecutive source-exact scanouts,31545own shadow transfers,continuous original clear,48specific render counterexamples and24actual-drawtime shadow counterexamples; corrected invalid queued-body/direct-shadow timing assumption using new read-only pose observations',
  currentCleanHumanUppercutCases=cases,currentUppercutDrawtimeShadowReport=str(own_path),
  currentUppercutSourceExactScanouts=sum(c['sourceExactScanouts']for c in cases.values()),
  currentUppercutSourceExactScreenPixels=sum(c['sourceExactScreenPixels']for c in cases.values()),
  currentUppercutNativeOwnedShadowCopies=sum(c['nativeShadowCopies']for c in cases.values()),
  currentUppercutSpecificRenderCounterexamples=48,currentUppercutSpecificDrawtimeShadowCounterexamples=24,
  supersededUppercutShadowTimingAssumption=dict(failedReport=str(failed_path),
   reason='Queued body pose and direct-shadow cache pose can differ during actual animation transitions. A same-field one-to-one queued-part assumption was invalid.2171/2172instead binds every shadow part to the actual pose/body/facing read at each native shadow DMA. No missing shadow is inferred from mismatching queued-body part counts.',
   actualReplacementReport=str(own_path),failedCheckNotAccepted=True),
  gameSourceAndPlayableBytesChangedThisTurn=False,obsoleteFoldersDeletedThisTurn=False,
  newCaptureLeavesNTFSCompressed=True,
  nextAction='Use the independently proven clean human Down/HP timing and actual107action observations to improve real-input boss tactics, prove both full campaigns throughKintaro/ShaoKahn and own endings/attract, while completing broader ordinary/special move-phase grounding/shadows across arenas, CPU/repeated/KO/overlap cases and all remaining finishers/victims/morphs/secrets/cinematics/audio. Then final combined UI regression,dependency-aware cleanup and refreshed release. The four clean DeadPool uppercut cases do not certify all moves,arenas,audio or artistic poses.',
  inputHashes=pins,goalStatus='active',finishedRelease=False,fullPortAcceptance=False)
 assert len(prior['remaining'])>=5 and not prior['actualFullLadderClearAccepted']and not prior['actualEndingsAccepted']
 return prior
if __name__=='__main__':
 assert not OUT.exists(),'Immutable checkpoint'
 report=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',cleanHumanUppercutCases=4,
  sourceExactScanouts=report['currentUppercutSourceExactScanouts'],
  sourceExactScreenPixels=report['currentUppercutSourceExactScreenPixels'],
  actualOwnShadowTransfers=report['currentUppercutNativeOwnedShadowCopies'],
  specificRenderCounterexamples=48,specificDrawtimeShadowCounterexamples=24,
  gameBytesChanged=False,actualFullLadderClearAccepted=False,actualEndingsAccepted=False,finishedRelease=False,fullPortAcceptance=False),indent=2))
