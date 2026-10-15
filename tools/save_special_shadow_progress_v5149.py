"""Full-scope additive checkpoint for complete repeated-move body/shadow fields."""
import ctypes,json,subprocess
from pathlib import Path
from ctypes import wintypes
import native_subzero_legs_context_v4993 as native
ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v5128_special_repeat_progress/progress.json'
OUT=ROOT/'audit_v5150_special_shadow_progress'
MOVES=('knife','ball','blade','choke','ring','square','bicycle','leg')
OLD_CHECKED={('ball',1),('leg',1),('leg',2),('bicycle',1),('bicycle',2)}
def main():
 need(not OUT.exists(),'Fresh additive full-scope native shadow checkpoint')
 parent=json.loads(PARENT.read_text());need(parent['goalStatus']=='active'and len(parent['remaining'])==5,'All five unfinished scope groups remain verbatim')
 pins={};evidence=[];cases=[];proof_paths=[];rgb_comparisons=[]
 def pin(p,h=None):
  p=Path(p).resolve();actual=sha(p);need(h is None or actual==h,'Actual immutable source/evidence/compiled input');need(str(p)not in pins or pins[str(p)]==actual,'Consistent immutable input');pins[str(p)]=actual
 for p in(PARENT,Path(__file__),Path(native.__file__)):pin(p)
 for move,side,air in[(m,s,False)for m in MOVES for s in(1,2)]+[('square',s,True)for s in(1,2)]:
  version=5148 if air else 5140 if(move,side)in OLD_CHECKED else 5142
  proof_path=ROOT/f'audit_v{version}_special_shadow_{move}_p{side}_checked/report.json'
  proof=json.loads(proof_path.read_text());case=proof['case'];need(proof['passed']and len(proof['actualSemanticFaultsRejected'])==11 and case['entryBodyPublicationProven']and case['everyReadyBodyComponentSourceBound']and not proof['fullPortAcceptance']and not proof['nativeFloorShadowCoverageAccepted'],'Full actual per-field body/native shadow proof, finite scope intact')
  need(case['move']==move and case['side']==side and len(case['state']['cycles'])==2 and case['actualShadowEligibilityCalls']==case['actualContiguousActorFields']and case['actualOwnedShadowComponents']==case['actualNativeBodyCandidates'],'Both complete owned bodies and shadow eligibility calls for every actual field')
  need(case['unattributedOtherObjectShadowCopies']==0,'No effect-object copy misattributed to a fighter')
  if air:need(case['state']['actualSquareContactVerified']and all(t['victimDamage']==27 for t in case['state']['cycles']),'Actual airborne square contacts in both genuine player slots')
  for p,h in proof['inputHashes'].items():pin(p,h)
  for p in proof_path.parent.rglob('*'):
   if p.is_file():pin(p);evidence.append(p)
  proof_paths.append(str(proof_path));cases.append(dict(move=move,side=side,air=air,proof=str(proof_path),case=case))
  current_version,prior_version=(5144,5118)if air else(5134,5102)
  current_folder=ROOT/f'audit_v{current_version}_special_repeat_{move}_p{side}_kitana'
  if air:prior_folder=ROOT/f'audit_v{prior_version}_square_air_repeat_{move}_p{side}_kitana'
  else:prior_folder=ROOT/f'audit_v{prior_version}_special_repeat_{move}_p{side}_kitana'
  current=json.loads((current_folder/'result.json').read_text());prior=json.loads((prior_folder/'result.json').read_text())
  need(current['passed']and current['nativeExit']==0 and current['terminalResult']==prior['terminalResult']and current['actualScenes']==prior['actualScenes'],'Every entire current actual RGB field and real input/entry/recovery chronology byte-exact versus previous actual native run; observer changes no scene')
  pin(prior_folder/'result.json')
  rgb_comparisons.append(dict(move=move,side=side,air=air,completeActualRGBFields=len(current['actualScenes']),allSceneDigestsAndChronologyExactlyPriorNativeRun=True))
  guest=json.loads((current_folder/'guest_memory_proof.json').read_text());gfx=json.loads((current_folder/'gfx_memory_proof.json').read_text())
  need(guest['sha256']==native.GUEST_SHA and guest['everyActualByteComparedInRAM']and gfx['bytes']==18976 and gfx['everyActualByteComparedInRAM'],'Every actual full cold guest/GFX validated in RAM')
  for p in current_folder.rglob('*'):
   if p.is_file():pin(p);evidence.append(p)
  transport=ROOT/f'audit_v{5145 if air else 5135}_special_repeat_{move}_p{side}_kitana_observed/report.json'
  pin(transport);evidence.append(transport)
 need(len(cases)==18 and sum(len(c['case']['state']['cycles'])for c in cases)==36,'Exactly18 real physical cold boots, all eight moves/both slots plus two airborne-square cases')
 for name in('mk2ks_special_shadow_v5131.lua',):pin(ROOT/name)
 for name in('run_special_shadow_v5133.py','verify_special_shadow_v5137.py','verify_special_shadow_v5139.py','verify_special_shadow_v5141.py','run_square_air_shadow_v5143.py','verify_square_air_shadow_v5147.py'):pin(ROOT/'tools'/name)
 # Preserve the exact original failed predicates, without counting exceptions as semantic faults.
 failures=[];python=Path(r'C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe')
 for name,move,side,expected in [('verify_special_shadow_v5137.py','leg',1,'Every current owned shadow stream strictly compressed six-bit'),('verify_special_shadow_v5139.py','square',1,"KeyError: 'MK2_HSPECIAL_HEALTH'")]:
  result=subprocess.run([str(python),'-B',str(ROOT/'tools'/name),'--move',move,'--side',str(side)],cwd=ROOT,text=True,capture_output=True)
  need(result.returncode==1 and expected in result.stderr,'Exact unchanged original failed native proof predicate reproduced')
  failures.append(dict(source=name,exitCode=result.returncode,stdout=result.stdout,stderr=result.stderr))
 for name in('PLAY_CURRENT_V1836_CHECKED.cmd','diagnostic_v1836_ball_register_boundary/mkport_candidate.exe','release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip','mame-mkp/mkport.exe','mame-mkp/src/mame/midway/midtunit_m.cpp','mame-mkp/src/mame/midway/midtunit_v.cpp','mk2/mk2-maincpu.bin'):
  p=(ROOT/name).resolve();need(str(p)in parent['newInputHashes'],'Current parent public/source pin retained');pin(p,parent['newInputHashes'][str(p)])
 native.expected()
 process=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'mkport_candidate.exe' } | Select-Object ProcessId,ExecutablePath) | ConvertTo-Json -Depth 3 -Compress"],capture_output=True,text=True)
 need(process.returncode==0 and not process.stdout.strip(),'All actual native candidate processes terminal')
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);allocated=kernel.GetCompressedFileSizeW;allocated.argtypes=[wintypes.LPCWSTR,ctypes.POINTER(wintypes.DWORD)];allocated.restype=wintypes.DWORD
 disk=logical=0
 for p in set(evidence):
  high=wintypes.DWORD();ctypes.set_last_error(0);low=allocated(str(p),ctypes.byref(high));need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual NTFS compressed allocation')
  disk+=low+(high.value<<32);logical+=p.stat().st_size
 need(all(sha(p)==h for p,h in pins.items()),'Final current source/native/evidence/public pins stable')
 count=lambda key:sum(c['case'][key]for c in cases)
 record=dict(schema=1,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,baseFullScopeCheckpoint=parent['baseFullScopeCheckpoint'],parentAdditiveJournals=parent['parentAdditiveJournals']+[str(PARENT)],remaining=parent['remaining'],newInputHashes=pins,
  mergeRule='Additive to all earlier full-scope checkpoints. These18 real Prison/Kitana instances now close their routine-entry body-publication gap and qualify every field of owned native shadows, not other arenas/CPU/KO/audio or complete native-port fidelity. None of the five original groups is removed.',
  previousGoalTurnClassification='Progress:5128 records18 real repeat-special cold boots,36 native special cycles,20026 post-engine owned actor fields and220 source/semantic faults. Entry-body drawing and five model-unreadable visual sets remained explicitly open.',
  thisGoalTurnClassification='Progress: native read-only body/shadow taps now start before actual draw at every real ready field. Eighteen fresh physical cold boots reproduce all prior complete actual RGB digests and terminal/input/recovery chronology exactly. Independently verified both entire fighter composites and original native shadow projection/quarter-row geometry/pen/cadence/staticGFXROM streams through every ready field, including all36routineentries andpaired/airborne/repeated/controlrecoveryphases. All18 RAM fullphase16 images and complete contact sheets visually inspected, closing previous five unreadable visual-set gaps for equivalent runs.198 genuine entry-body/ownership/eligibility/projection/floor/pen/source/RAM-ROM-stream mutations rejected, no KeyError or no-op counted.',
  compiledCandidate=native.NAME,executableSHA256=native.EXE_SHA,payloadSHA256=native.PAYLOAD_SHA,initializedGuestSHA256=native.GUEST_SHA,checkedCaseReports=proof_paths,verifiedCases=cases,exactPriorActualRGBComparisons=rgb_comparisons,
  newNativeColdBootInstances=18,actualVerifiedSpecialCycles=36,actualContiguousOwnedActorFields=count('actualContiguousActorFields'),actualCompleteRGBFields=sum(c['completeActualRGBFields']for c in rgb_comparisons),actualRoutineEntryBodyFrames=36,actualBodyCandidateParts=count('actualNativeBodyCandidates'),actualOwnedShadowComponents=count('actualOwnedShadowComponents'),actualNativeSourceBoundShadowCopies=count('actualSourceBoundShadowCopies'),actualAddedFighterSourceBoundShadowCopies=count('actualAddedFighterShadowCopies'),actualUniqueStaticROMStreamInstances=count('actualUniqueROMStreams'),actualSemanticFaultsRejected=198,
  everyCurrentEntryBodyPublicationProven=True,everyCurrentOwnedReadyFieldBodyAndShadowVerified=True,allCurrentActualRGBAndChronologyExactlyPriorNativeRuns=True,previousFiveUnreadableVisualSetsReviewedInFreshRAMRuns=True,originalBodyClipAndShadowKernelsUnchanged=True,nativeFloorShadowCoverageAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False,
  nativeShadowScope='All owned true17/18 and stockKitana physical readyfields in all eight moves bothslots repeatedtwice, twoactualairborneSquarecontactcases, nativepairedgrabs/flips/lifts/throws, roll/flight/jump, nativehitreactionandlanding/recovery, finalphysicalwalk/jump/punch. Every eligible nativebody part uses exact source-bound original projection and pen0F0F. All imported six-bit streams strictly compressed, actual immutable GFXROM bytes independently compared to32compiled interleaved ROM lanes. No effect-object shadows, otherarenas,CPU,blocked,KO/overlap,finisher,campaignorvoice scope inferred.',
  preservedCounterexamples=['5137 incorrectly assumed every stock control part was compressed. Actual original Kitana rawhand01457742 is11x6 with6000/6010. Whole original shadowkernel provesB5=h//4=1, soDSJS terminateswithoutcallingrowheader scanner; nativefirstsource is duplicated.5139/5141/5147 acceptonlythat exactsource/size/command rawcontrol, compareallactualROMbytesandtwo nativecopies, and keepallimported streams strictlycompressed. Original Sub-Zero18-high rawicehand from prior checkpoints remains unaccepted; no genericrawstepping relaxation.',
   '5139 copied parsed rows to plain dict, losing empty observedhealth list on actual stationary squarewhiffs. KeyError reproduced and notcounted.5141 retains defaultdict while stillrequiringeveryactualhealthchange beexplainedbynativewrite primitive.',
   'Legacy finite physicalchecker embedded state.entryBodyPublicationUnobservedFrames describes its deliberately filtered old-scope view, not currentunfilteredtap evidence. Top-level case.entryBodyPublicationProven and complete everyfield bodycheck explicitly proveallactualnewentrydraws; immutablehistoricalmissing-entryrecordsremainpreserved.'],
  preservedFailures=failures,completedNativeHostHandles=[97866,69620,29835,32735,39263,57214,24442,57850,12317,52803,36648,1305,10923,97077,56288,67128,11083,93235],completedVerifierHostHandles=[42758,47992,97908,67486,64686,8673,90378,23610,47165,66461,95273,40201,15028,44361,17977,87843,58557,16798],allRecordedNativeHandlesConsumedTerminalZero=True,candidateProcessesStillRunning=False,
  publicCMDExecutableZIPAndHistoricalInstalledEXEUnchanged=True,dirtyCheckoutUnchanged=True,newIsolatedBuildsThisContinuation=0,newPayloadCopiesThisContinuation=0,rawGuestGFXRGBPCMOrWAVFilesWritten=0,oldBuildFolderDeletionsThisContinuation=0,currentTraceLogicalBytes=logical,currentTraceAllocatedBytes=disk,currentTraceAllocatedMiB=round(disk/(1024**2),2),
  cleanupAccounting='All18 current native logs/unique-stream rowproofs/results and18independent reports are NTFScompressed. Fullguest/GFX/RGB/rawinterleavedROM buffers heldonlyinRAM. StaticGFXROM unique streams capturedonce perdescriptor ratherthan persisting redundantrawdata; no newbinary/payload/fullbuildtree. Prior32.49GiB reclaimed remains retained.',
  nextAction='All five original groups stayopen. Move beyond currentPrison/humanKitana cases to realCPU/blocked/KO/overlap/victimmatrix and naturally reached otherarenas; resume genuineKano/Sonya campaign progress after the repairedSub-Zero victims to earnKintaro/ShaoKahn clears/ownendings/attract. Continue Pit/Tomb nativebranch/mirror/victim/audio, otherfinishers/victims/morphs/secrets/cinematics andfinalcombinedselection/ladder/name/audio/launcher regression. Dependency-aware obsolete-build cleanup andrefreshedfinalZIP follow verifiedcombinedstate. Do notpromoteorcompleteon thisboundedshadowmatrix alone.')
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress compact full-scope checkpoint')
 (OUT/'progress.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:record[k]for k in('goalStatus','actualContiguousOwnedActorFields','actualCompleteRGBFields','actualNativeSourceBoundShadowCopies','actualAddedFighterSourceBoundShadowCopies','actualSemanticFaultsRejected','currentTraceAllocatedMiB','remaining')},indent=2))
if __name__=='__main__':main()
