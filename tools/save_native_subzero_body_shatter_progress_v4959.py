"""Additive full-scope checkpoint: own frozen-body data and actual native shatter instances."""
import json,subprocess
from pathlib import Path
import native_subzero_body_context_v4932 as native

ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v4919_earned_subzero_matrix_progress/progress.json'
OUT=ROOT/'audit_v4960_native_subzero_body_shatter_progress'

def main():
 need(not OUT.exists(),'Fresh full-scope additive journal')
 parent=json.loads(PARENT.read_text());need(parent['goalStatus']=='active'and len(parent['remaining'])==5,'Entire original five groups retained')
 paths=[ROOT/'audit_v4931_native_subzero_bodies_source_checked/report.json',
        ROOT/'audit_v4938_native_subzero_body_matrix_checked/report.json',
        ROOT/'audit_v4958_native_subzero_shatter_matrix_checked/report.json']
 source,body,shatter=[json.loads(p.read_text())for p in paths]
 need(all(r['passed']for r in(source,body,shatter))and body['ownedFrozenBodyInstancesVerified']==4
      and shatter['nativeShatterSequenceInstancesVerified']==4 and shatter['actualSubsequentCPUMatchesVerified']==4
      and not body['fullPortAcceptance']and not shatter['fullPortAcceptance'],'Independent actual narrow instance checks only')
 pins={}
 def pin(path,wanted=None):
  path=Path(path).resolve();h=sha(path);need(wanted is None or h==wanted,'Exact current source/native evidence')
  need(str(path)not in pins or pins[str(path)]==h,'Consistent evidence pin');pins[str(path)]=h
 for p in(PARENT,Path(__file__),*paths,Path(native.__file__)):pin(p)
 for report in(body,shatter):
  for p,h in report['inputHashes'].items():pin(p,h)
 for name in('asset_v4928_native_subzero_bodies','source_v4922_native_subzero_bodies'):
  for p in(ROOT/name).rglob('*'):
   if p.is_file():pin(p)
 for name in('build_native_subzero_bodies_v4920.py','build_native_subzero_bodies_v4927.py',
  'qualify_native_subzero_bodies_v4923.py','qualify_native_subzero_bodies_v4930.py','build_native_subzero_bodies_v4925.ps1',
  'run_native_subzero_body_probe_v4934.py','verify_native_subzero_body_matrix_v4937.py',
  'run_native_subzero_shatter_probe_v4940.py','run_native_subzero_shatter_lifecycle_v4944.py',
  'run_native_subzero_shatter_transition_v4948.py','run_native_subzero_shatter_nextmatch_v4952.py',
  'verify_native_subzero_shatter_matrix_v4955.py','verify_native_subzero_shatter_matrix_v4957.py'):pin(ROOT/'tools'/name)
 for name in('mk2ks_native_subzero_body_probe_v4933.lua','mk2ks_native_subzero_shatter_probe_v4939.lua',
  'mk2ks_native_subzero_shatter_lifecycle_v4943.lua','mk2ks_native_subzero_shatter_transition_v4947.lua',
  'mk2ks_native_subzero_shatter_nextmatch_v4951.lua'):pin(ROOT/name)
 build=ROOT/native.NAME
 for name in('build-info.json','restoration.json','build.log','mkport_candidate.exe','roms/mk2ks/mk2ks.mdata'):pin(build/name)
 native.expected()
 retained=[]
 for cap,obs,cases in((4941,4942,[('sonya',1)]),(4945,4946,[('sonya',1)]),
                      (4949,4950,[(f,s)for f in('kano','sonya')for s in(1,2)])):
  for fighter,side in cases:
   suffix='earned'if cap==4941 else'lifecycle'
   folder=ROOT/f'audit_v{cap}_subzero_{fighter}_p{side}_{suffix}'
   report_path=ROOT/f'audit_v{obs}_subzero_{fighter}_p{side}_{suffix}_observed/report.json'
   report=json.loads(report_path.read_text());meta=json.loads((folder/'result.json').read_text())
   if cap==4949:need(not report['passed']and 'LIFECYCLE_END'in report['error'],'Failed subsequent-phase gate retained honestly')
   for p,h in meta['inputHashes'].items():pin(p,h)
   for p in[report_path,*[p for p in folder.rglob('*')if p.is_file()]]:pin(p)
   retained.append(dict(report=str(report_path),passed=report['passed'],nativeExit=meta['nativeExit'],
                        fullPortAcceptance=False,scope='finite probe or failed transition gate, not full finisher acceptance'))
 public={
  'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
  'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
  'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
  'mk2/mk2-maincpu.bin':'45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'}
 for p,h in public.items():pin(ROOT/p,h)
 report=dict(schema=1,baseFullScopeCheckpoint=parent['baseFullScopeCheckpoint'],
  parentAdditiveJournals=parent['parentAdditiveJournals']+[str(PARENT)],
  mergeRule='Additive to4557 and all parents. Native own frozen-body and human shatter instance evidence is new; no original Pit/Tomb, move-phase art/grounding/floor-shadow, CPU/repetition/KO/overlap, other victims/finishers/morphs/secrets/cinematics, natural campaign endings, combined UI/audio regression, cleanup or final-release requirement is removed.',
  remaining=parent['remaining'],goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
  previousGoalTurnClassification='no progress: acknowledgement only; current executed state revalidated before continuing.',
  thisGoalTurnClassification='progress: consumed three remaining own-body native handles; independently verified all four actual owned frozen-body instances. Real earned human native shatter now runs for true17/18 in both slots, passes original69 center-gap gate with actual62/63 gaps, renders dedicated two-leg groups, executes original soundD8/ice emitter/effect/64-field park/win sequence, then naturally enters a distinct fresh CPU match. Independent whole-ROM/GFX and physical-event checks verify88 native opcode/PC/mask records,2550 consecutive victim fields,28 real history comparisons,16 RGB stages and reject52 altered-record negative faults. All gameplay/source/build/public bytes remained immutable during these tests. Full art/audio and every original requirement remain open.',
  newInputHashes=pins,sourceDataQualification=str(paths[0]),ownedFrozenBodyMatrix=str(paths[1]),nativeShatterInstanceMatrix=str(paths[2]),
  compiledCandidate=native.NAME,executableSHA256=native.EXE_SHA,initializedGuestSHA256=native.GUEST_SHA,
  payloadSHA256='08D87AC46142687CEE2A13A81F4C7B78268C8AA99D3020F3AF21693058F00C08',
  compiledSourceSHA256='FC2BC39BA3E6A5F8EE34E07605C0713F9FA916CB8FD9BBA79931339C109DB590',
  addedBodyData=dict(originalStockWholeRows0Through11Preserved=True,rows12Through16RetainOldJaxFallback=True,
    allStockLegRows0Through16Preserved=True,allOtherUnsignedWholeIdentitySemanticsPreserved=True,
    dedicatedTrue17And18WholeAndLegsGroups=True,guestChangedBytes=273,ownedGFXBytes=11944,
    originalPalette='FFB06AE0',nativeTaskCacheAudioAndCleanupCodeUntouched=True),
  actualOwnedBodyCases=body['cases'],actualNativeShatterCases=shatter['cases'],
  sourceNegativeFaults=13,ownedBodyRecordNegativeFaults=44,shatterRecordNegativeFaults=52,
  nativeShatterSequenceInstancesVerified=4,ownedFrozenLegsRuntimeInstancesVerified=4,actualSubsequentCPUMatchesVerified=4,
  fullShatterArtAndAudioAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False,
  normalHealthFreezeAccepted=False,nativeFloorShadowCoverageAccepted=False,
  correctedSourceUnderstanding=dict(nativeParkEntry='FF841EC0',nativeParkMeaning='MOVI40/CALLAFF80DCC0/JRback: original infinite64-field sleep loop, not actor retirement. Native frozen legs remain intentionally until scene transition.',
    oldApproachFailureRootCauseQualified=False,currentApproach='Starting ordinary walking at deep+60 reaches actual62/63 center gap; no jump actually needed. Native69 distance gate unchanged. Earlier85-gap stall cause not claimed.',
    transitionGateCorrection='Original two-human-state1 gate was invalid after genuine native loser departure: winner state1, new CPU enemy state0. Fresh4951 requires actual mode2, valid linked physical actors, real winner8, full fresh161 health and nonfrozen/legs poses; actual rendered next arena was inspected.'),
  actualVisualReview='All four actual freeze/fracture/victory/next-match RGB sequences viewed directly in RAM. Own frozen costumes and remaining legs are present, and old bodies/debris are absent from next match. Horizontal dark cutline on frozen legs still needs stock-reference/pixel-level fidelity comparison; do not declare full finisher art accepted. Normal floor-shadow coverage remains open.',
  retainedFiniteOrFailedReports=retained,
  preservedCorrections=['4920 parse failure corrected only in fresh4927; source qualification4923 fault-scope failure corrected in fresh4930.',
   '4955 uniqueness incorrectly included later CPU main40 animation lookups; fresh4957 requires exactly one actual main40 in the proven finisher victim lifetime. Both executed sources retained.'],
  publicCMDExecutableZIPAndHistoricalInstalledEXEUnchanged=True,dirtyCheckoutRestoredAndStillUnchanged=True,
  isolatedNewBuildsSinceParent=1,newBuildsThisContinuation=0,newPayloadCopiesSinceParent=1,
  payloadBuildUsesImmutableHardlink=True,rawGuestGFXRGBPCMOrWAVFilesWritten=0,newDeletionsThisContinuation=0,
  cleanupAccounting='Preserve prior32.49GiB reclaimed. Reuse one immutable4926 candidate; no new builds/candidate copies for these regressions. New runtime evidence is compressed small logs/digest JSON; actual scene/guest/GFX bytes remain RAM-only. No restoration of retired historical build folders.',
  nextAction='Continue original full scope. For this finisher, compare native stock frozen-leg rendering/cutline, bind actual palette/pixels/gore effects and mixed PCM/audio/cleanup fidelity; verify normal-health freeze separately. Continue all other native victim/finisher/morph/secret/cinematic, move-art/grounding/floor-shadow/CPU/KO/overlap, Pit/Tomb, natural Kintaro/Shao campaign clears/own endings/attract, combined selection/ladder/names/audio, dependency-aware cleanup and final refreshed ZIP gates before public promotion.')
 need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'Exact current evidence and full original scope')
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress additive journal')
 (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(journal=str(OUT/'progress.json'),newPins=len(pins),nativeShatterInstances=4,actualNextCPUMatches=4,fullPortAcceptance=False,goalStatus='active'),indent=2),flush=True)

if __name__=='__main__':main()
