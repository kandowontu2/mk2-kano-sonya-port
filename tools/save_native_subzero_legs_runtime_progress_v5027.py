"""Full-scope additive checkpoint: compiled semantic legs and actual native lifecycle/PCM."""
import json,subprocess
from pathlib import Path
import native_subzero_legs_context_v4993 as native

ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v4990_native_subzero_legs_progress/progress.json'
OUT=ROOT/'audit_v5028_native_subzero_legs_runtime_progress'

def main():
 need(not OUT.exists(),'Fresh full-scope additive progress record')
 parent=json.loads(PARENT.read_text());need(parent['goalStatus']=='active'and len(parent['remaining'])==5,'All original requirements remain intact')
 paths=[ROOT/'audit_v5005_native_subzero_legs_matrix_checked/report.json',
        ROOT/'audit_v5026_native_subzero_legs_regression_checked/report.json']
 matrix,cross=[json.loads(p.read_text())for p in paths]
 need(matrix['passed']and matrix['nativeShatterSequenceInstancesVerified']==4
      and matrix['actualSubsequentCPUMatchesVerified']==4 and len(matrix['actualFaultsRejected'])==52,
      'Four genuine native owned-victim lifecycle instances independently verified')
 need(cross['passed']and cross['actualAddedVictimSlotCasesCompared']==4 and cross['actualCurrentPCMContexts']==2
      and cross['actualRepeatedKanoP1ReviewEntireRGBIdentical']and len(cross['actualFaultsRejected'])==10,
      'Actual cross-candidate traces, vocal dispatch and whole mixed PCM independently checked')
 need(not matrix['fullPortAcceptance']and not cross['fullPortAcceptance'],'No narrower result substitutes for full objective')
 pins={}
 def pin(p,h=None):
  p=Path(p).resolve();actual=sha(p);need(h is None or h==actual,'Current immutable authoritative input')
  need(str(p)not in pins or pins[str(p)]==actual,'Consistent current evidence pin');pins[str(p)]=actual
 for p in(PARENT,Path(__file__),Path(native.__file__),*paths):pin(p)
 for report in(matrix,cross):
  for p,h in report['inputHashes'].items():pin(p,h)
 for name in('build_native_subzero_legs_v4991.ps1','run_native_subzero_legs_nextmatch_v5001.py',
              'verify_native_subzero_legs_matrix_v5004.py','run_native_subzero_legs_review_v5007.py',
              'run_native_subzero_legs_dma_pcm_v5013.py','verify_native_subzero_legs_regression_v5017.py',
              'verify_native_subzero_legs_regression_v5019.py','verify_native_subzero_legs_regression_v5021.py',
              'verify_native_subzero_legs_regression_v5023.py','verify_native_subzero_legs_regression_v5025.py'):pin(ROOT/'tools'/name)
 for name in('mk2ks_native_subzero_legs_body_v4997.lua','mk2ks_native_subzero_legs_shatter_v4998.lua',
              'mk2ks_native_subzero_legs_lifecycle_v4999.lua','mk2ks_native_subzero_legs_nextmatch_v5000.lua',
              'mk2ks_native_subzero_legs_reference_pcm_v5011.lua','mk2ks_native_subzero_legs_dma_pcm_v5012.lua'):pin(ROOT/name)
 build=ROOT/native.NAME
 for name in('build-info.json','restoration.json','build.log','mkport_candidate.exe','roms/mk2ks/mk2ks.mdata'):pin(build/name)
 info=json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))
 restored=json.loads((build/'restoration.json').read_text(encoding='utf-8-sig'))
 need(restored['passed']and info['initialized_guest_byte_delta']==92
      and info['payload_sha256']==native.PAYLOAD_SHA and not info['public_build_promoted'],'Actual isolated build and restoration')
 for p,h in restored['restored_actual_preexisting_files'].items():pin(p,h)
 need(not (build/'restoration_backups/mkport.exe').exists(),'Temporary installed-binary backup removed after verified restoration')
 public={
  'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
  'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
  'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
  'mame-mkp/src/mame/midway/midtunit_v.cpp':'8912181C8D7560BFD4974CECFEADD0532A9588A60D8D3FC399D58433EDB37611',
  'mk2/mk2-maincpu.bin':'45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'}
 for p,h in public.items():pin(ROOT/p,h)
 native.expected()
 need(all(sha(p)==h for p,h in pins.items()),'Every current native/build/source/evidence/public input unchanged')
 result=dict(schema=1,baseFullScopeCheckpoint=parent['baseFullScopeCheckpoint'],
  parentAdditiveJournals=parent['parentAdditiveJournals']+[str(PARENT)],remaining=parent['remaining'],
  mergeRule='Additive to4557 and all parents. Compiled semantic legs, actual native four-slot lifecycle, P1 voice/PCM and finite cross-regression add evidence. No Pit/Tomb, moves/art/grounding/floor-shadow, CPU/repeated/KO/overlap, other finisher/victim/morph/secret/cinematic, natural campaign/ending/attract, combined UI/audio, cleanup or final release requirement is removed.',
  goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
  previousGoalTurnClassification='progress: actual stock/DMA and paired PCM proof, built-in semantic legs master and independently qualified staged native data/source (4990).',
  thisGoalTurnClassification='progress: one isolated guarded/restored incremental build. Actual true17/18 native human deep-freeze/shatter in both player slots, own semantic legs, original native effects/win/park/departure and fresh CPU matches verified across four cases. All16 native stages reviewed directly, with one exact repeated KanoP1 review after initial output truncation. New P1 whole PCM identical to both previous sample profiles and actual native male45/female48 branches/dispatch bound to current guest. Four old/new contexts compare18275 actual physical/native rows; only explicit leg pointers and two source-bound mirrored width registers differ. Whole frozen and fresh next-match RGB fields are unchanged.62 altered-record faults rejected. Full objective remains open.',
  newInputHashes=pins,nativeInstanceMatrix=str(paths[0]),crossCandidatePCMAndVocalProof=str(paths[1]),
  compiledCandidate=native.NAME,executableSHA256=native.EXE_SHA,payloadSHA256=native.PAYLOAD_SHA,
  initializedGuestSHA256=native.GUEST_SHA,compiledSourceSHA256='37E02771B1F20CF17D0D619F83033F5FE37FE5B62DCD9519F60872763BE0E57A',
  initializedGuestChangedBytesRelativeTo4926=92,additionalSemanticLegGFXBytes=7032,totalActualOwnGFXBytesComparedInRAM=18976,
  wholeGuestBytesComparedPerActualColdBoot=1048576,newNativeColdBootInstances=7,
  nativeHumanShatterMatrixInstances=4,actualMatrixVictimFields=2550,actualMatrixOpcodePCMaskRecords=88,
  actualMatrixPhysicalCommandComparisons=28,actualMatrixDistinctRGBFields=16,actualNaturalNextCPUMatchesInMatrix=4,
  actualRepeatedKanoP1NextCPUMatchAndEntireRGBVerified=True,
  original69CenterGapGateIntact=True,actualCenterGaps=[62,63],
  ownWholeGroups=['FFD62400','FFD62480'],newSemanticLegGroups=['FFD63400','FFD63460'],
  originalWholeBodyDataStockLegRowsTasksAudioAndCleanupRetained=True,
  actualCompiledUnusedGFXStorageGuardPassed=True,
  finiteNativeLegRuntimeInstancesVerified=True,allNativeLegCasesViewed=True,
  actualCrossCandidatePhysicalNativeRowsCompared=18275,
  actualMirrorCacheSourceCounterexample='A7 changed35->31 for KanoP2 and27->29 for SonyaP2 at the first native park. OriginalFF838830 loads width/height; X-flip pathFF838980/990/9A0 keeps last-part width inA7. Entire existing cache bytes agree old/new; original loopFF8387D0 onward matches original ROM. EntryFF838790 already used the prior Sonya ring-glow router, so claiming entire routine equals unpatched stock was false.',
  actualCurrentMixedPCMContexts=2,currentCompletePCMUpdatesPerCase=354,currentCompletePCMBytesPerCase=1359360,
  currentNonzeroPCMUpdatesPerCase=353,actualCurrentPCMSHA256=[r['wholePCMSHA256']for r in cross['currentMixedPCMAndVocalCases']],
  actualNativeVocalChoices=[r['nativeGenderAndDispatch']for r in cross['currentMixedPCMAndVocalCases']],
  audioScope='TrueKano17/Sonya18 P1 deep freeze through win+180 entire48k stereo PCM agrees with both previous samples-on/off captures. Native male/female branch and voice45/48 dispatch proven. Direct voice sound-primitive/DCS delivery and every other victim/slot/effect/stage/voice are not inferred as accepted.',
  fullShatterArtAndAudioAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False,
  normalHealthFreezeAccepted=False,nativeFloorShadowCoverageAccepted=False,
  actualVisualReview='Dedicated own frozen legs have shaped/chipped icy waist edges and no retained hands in all four real human shatter slot cases. They occupy the owned body floor baseline, remain during the original parked-leg victory loop and disappear naturally in fresh CPU Temple scenes. Original whole frozen bodies and fresh CPU scenes have identical entireRGB digests before/after. General move-phase ground/shadow coverage, wider art/floor fidelity and other arena/CPU/KO/overlap cases remain open.',
  preservedFailedVerifierSources=[
   '5017 parse error else0x; fresh5019 corrected spacing without touching failed source.',
   '5019 correctly rejected two unexpected nativeP2 A7 differences; actual register widths and original cache disassembly were inspected before permitting exactly those bounded differences.',
   '5021 correctly rejected an overbroad original-cache byte equality claim: prior ring-glow entry router already changed6bytes atFF838790. Entire existing old/new cache agrees; original loop startsFF8387D0. Source understanding corrected, not native gameplay code.',
   '5023 unescaped apostrophe parse error; fresh5025 corrected textual literal only. All executed sources preserved; only actual5026 independently passing report is acceptance evidence.'],
  completedNativeHostHandles=[22180,16818,89051,60469,70272,46753,57428],allNativeHostHandlesConsumedTerminalZero=True,
  candidateProcessesStillRunning=False,
  publicCMDExecutableZIPAndHistoricalInstalledEXEUnchanged=True,dirtyCheckoutRestoredAndUnchanged=True,
  newIsolatedBuildsThisContinuation=1,newPayloadCopiesThisContinuation=0,payloadBuildUsesImmutableHardlink=True,
  rawGuestGFXRGBPCMOrWAVFilesWritten=0,oldBuildFolderDeletionsThisContinuation=0,
  temporaryInstalledBinaryBackupRemovedAfterVerifiedRestoration=True,
  cleanupAccounting='Prior32.49GiB reclamation retained. Only one isolated EXE/frozen selected sources, not a full duplicated build tree. Existing shared incremental build reused and actual preexisting files restored. Candidate payload is a verified hardlink to4984, not another copy. All scene/audio/program/GFX buffers RAM-only; small logs/digests compressed. No retired evidence folders restored.',
  nextAction='Continue all five original groups. Next Sub-Zero coverage should exercise ordinary-health freeze/thaw and broader floor/pose/shadow/CPU/KO/overlap instead of treating only the earned finisher as sufficient; finish exact voice delivery/PCM and wider finisher art/arena fidelity as needed. Continue other native victim/finisher/morph/secret/cinematic and Pit/Tomb combinations, actual natural Kintaro/Shao campaign clears/own endings/return-attract, final combined selection/ladder/names/audio, dependency-aware obsolete-build cleanup and refreshed final ZIP. Public build remains unpromoted until whole objective is verified.')
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress full-scope progress')
 (OUT/'progress.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(journal=str(OUT/'progress.json'),pins=len(pins),nativeShatterCases=4,currentPCMContexts=2,
       allOriginalGroupsRetained=len(result['remaining']),fullPortAcceptance=False,goalStatus='active'),indent=2),flush=True)

if __name__=='__main__':main()
