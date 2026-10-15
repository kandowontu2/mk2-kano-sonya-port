"""Full-scope additive native move/floor/shadow checkpoint, never full-port acceptance."""
import ctypes,json,subprocess
from pathlib import Path
from ctypes import wintypes
import native_subzero_legs_context_v4993 as native
ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v5064_normal_subzero_freeze_progress/progress.json'
PROOF=ROOT/'audit_v5090_move_phase_shadow_checked/report.json'
OUT=ROOT/'audit_v5092_move_phase_shadow_progress'

def main():
 need(not OUT.exists(),'Fresh additive full-scope move progress')
 parent=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text())
 need(parent['goalStatus']=='active'and len(parent['remaining'])==5,'All five original unfinished groups retained')
 need(proof['passed']and proof['actualAddedFighterPlayerSlotCases']==4 and proof['actualStockControlCases']==2 and
      proof['actualOrdinaryFields']==6606 and proof['actualFullRGBFields']==128 and
      proof['actualAddedFighterCompressedShadowCopies']==5260 and proof['actualSourceBoundCompressedShadowCopies']==15809 and
      len(proof['actualFaultsRejected'])==180 and proof['entireAddedFighterJumpTrajectoriesEqualStockControl']and
      not proof['fullPortAcceptance']and not proof['nativeFloorShadowCoverageAccepted'],
      'Independently source-bound full current phase matrix, with finite scope intact')
 pins={}
 def pin(p,h=None):
  p=Path(p).resolve();actual=sha(p);need(h is None or actual==h,'Current immutable authoritative input')
  need(str(p)not in pins or pins[str(p)]==actual,'Consistent authoritative pin');pins[str(p)]=actual
 for p in(PARENT,PROOF,Path(__file__),Path(native.__file__)):pin(p)
 for p,h in proof['inputHashes'].items():pin(p,h)
 for name in('mk2ks_move_phase_shadow_v5065.lua','mk2ks_move_phase_shadow_v5075.lua','mk2ks_move_phase_shadow_v5081.lua'):
  pin(ROOT/name)
 for name in('run_move_phase_shadow_v5067.py','run_move_phase_shadow_v5071.py','run_move_phase_shadow_v5077.py',
              'run_move_phase_shadow_v5083.py','verify_move_phase_shadow_v5087.py','verify_move_phase_shadow_v5089.py'):
  pin(ROOT/'tools'/name)
 folders=[ROOT/'audit_v5072_move_phase_kano_p1']
 folders +=[ROOT/f'audit_v5078_move_phase_{f}_p{s}'for f,s in[('kano',1),('kano',2),('sonya',1),('sonya',2),('kitana',1),('liu_kang',2)]]
 folders +=[ROOT/f'audit_v5084_move_phase_{f}_p{s}'for f,s in[('kano',1),('kano',2),('sonya',1),('sonya',2)]]
 evidence=[]
 for folder in folders:
  record=json.loads((folder/'result.json').read_text());guest=json.loads((folder/'guest_memory_proof.json').read_text())
  need(record['nativeExit']==0 and guest['sha256']==native.GUEST_SHA and guest['everyActualByteComparedInRAM'],
       'Each real native cold boot and host reached actual terminal success')
  for p in folder.rglob('*'):
   if p.is_file():pin(p);evidence.append(p)
 need(len(folders)==11,'One initial input diagnostic, six corrected16-stage cases and four expanded24-stage own cases')
 report_folders=[ROOT/'audit_v5069_move_phase_kano_p1_observed',ROOT/'audit_v5073_move_phase_kano_p1_observed']
 report_folders +=[ROOT/f'audit_v5079_move_phase_{f}_p{s}_observed'for f,s in[('kano',1),('kano',2),('sonya',1),('sonya',2),('kitana',1),('liu_kang',2)]]
 report_folders +=[ROOT/f'audit_v5085_move_phase_{f}_p{s}_observed'for f,s in[('kano',1),('kano',2),('sonya',1),('sonya',2)]]
 for folder in[*report_folders,PROOF.parent]:
  for p in folder.rglob('*'):
   if p.is_file():pin(p);evidence.append(p)
 initial=json.loads((report_folders[0]/'report.json').read_text())
 need(not initial['passed']and 'FileNotFoundError'in initial['error'],'Original pre-boot wrong-controller-name failure preserved')
 python=Path(r'C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe')
 failed=subprocess.run([str(python),'-B',str(ROOT/'tools/verify_move_phase_shadow_v5087.py')],cwd=ROOT,text=True,capture_output=True)
 need(failed.returncode==1 and 'Actual-record fault was accepted: wrong_jump_apex'in failed.stderr and
      not (ROOT/'audit_v5088_move_phase_shadow_checked').exists(),'Original weaker plateau check still rejects acceptance; unchanged failed source preserved')
 # Preserve latest public launcher/ZIP and dirty user sources using their current prior pinned values.
 public_names=('PLAY_CURRENT_V1836_CHECKED.cmd','diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
  'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip','mame-mkp/mkport.exe',
  'mame-mkp/src/mame/midway/midtunit_m.cpp','mame-mkp/src/mame/midway/midtunit_v.cpp','mk2/mk2-maincpu.bin')
 for name in public_names:
  p=(ROOT/name).resolve();need(str(p)in parent['newInputHashes'],'Original public/source pin retained');pin(p,parent['newInputHashes'][str(p)])
 native.expected()
 status=subprocess.run(['powershell','-NoProfile','-Command',
  "@(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'mkport_candidate.exe' } | Select-Object ProcessId,ExecutablePath,CommandLine) | ConvertTo-Json -Depth 3 -Compress"],text=True,capture_output=True)
 need(status.returncode==0 and not status.stdout.strip(),'Actual native candidate processes all terminal')
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);allocated=kernel.GetCompressedFileSizeW
 allocated.argtypes=[wintypes.LPCWSTR,ctypes.POINTER(wintypes.DWORD)];allocated.restype=wintypes.DWORD
 disk=logical=0
 for p in set(evidence):
  high=wintypes.DWORD();ctypes.set_last_error(0);low=allocated(str(p),ctypes.byref(high))
  need(low!=0xffffffff or ctypes.get_last_error()==0,'Exact NTFS physical size query')
  disk+=low+(high.value<<32);logical+=p.stat().st_size
 need(all(sha(p)==h for p,h in pins.items()),'Current compiled/source/evidence/public inputs stable')
 record=dict(schema=1,baseFullScopeCheckpoint=parent['baseFullScopeCheckpoint'],
  parentAdditiveJournals=parent['parentAdditiveJournals']+[str(PARENT)],remaining=parent['remaining'],goalStatus='active',
  fullPortAcceptance=False,finishedRelease=False,
  mergeRule='Additive to4557 and every prior checkpoint. Current ordinary human move/jump/ground/shadow matrix adds evidence; none of the five original groups is removed or replaced with passing scenes.',
  previousGoalTurnClassification='progress:5060/5064 independently qualified six real ordinary ice/thaw/control cases, four added player slots,4206 live fields,1044 imported shadow copies and126 faults; exposed original stock raw ice-hand descriptor instead of weakening own compressed stream gates.',
  thisGoalTurnClassification='progress: eleven real native physical cold boots, no game-state writes/proxies. Diagnosed initial three-field simultaneous Down+HP as a rejected input during crouch transition, then native uppercut activates with a real crouch hold and laterHP. Measured actual neutral jump38airfields and95pixels across both new characters/slots and stock controls. Older frame650 marked falling is actually landing; fresh expanded24-field art/shadow controller captures true descending635, apex622, kicks startup/contact/recovery and uppercut startup/strike/recovery. Four full added player-slot contexts plus two stock comparisons independently pass6606livefields/128fullRGBstages/5260imported shadows/15809compressed native copies and180semantic/source record faults. All128accepted image fields visually reviewed in RAM contact sheets, with full-resolution falling and uppercut frames for all four added slots. All original requirements remain open as recorded.',
  checkedPhaseMatrix=str(PROOF),newInputHashes=pins,compiledCandidate=native.NAME,
  executableSHA256=native.EXE_SHA,payloadSHA256=native.PAYLOAD_SHA,initializedGuestSHA256=native.GUEST_SHA,
  newNativeColdBootInstances=11,acceptedAddedFighterPlayerSlotCases=4,acceptedStockControlCases=2,
  actualContiguousLiveFieldsInAcceptedMatrix=6606,actualFullRGBFieldsInAcceptedMatrix=128,
  actualAddedFighterCompressedShadowCopies=5260,actualSourceBoundCompressedShadowCopies=15809,actualSemanticFaultsRejected=180,
  exactEntireAddedJumpTrajectoriesMatchStockKitana=True,originalShadowKernelUnchanged=True,
  actualJumpAirborneFields={'begin':605,'end':642,'count':38,'firstApex':622,'heightPixels':95},
  actualBasicMovePhases=['jump_rise','jump_apex','jump_fall','landing','crouch','uncrouch','stand','high_kick_start','high_kick_contact','high_kick_recovery','low_kick_start','low_kick_contact','low_kick_recovery','block','uppercut_start','uppercut_strike','uppercut_recovery','walk','ready'],
  nativeFloorAnchors={'kano':82,'sonya':81,'kitana':83,'liu_kang':83},
  normalOwnMoveAndGroundingInstancesVerified=True,sampledNativeSourceBoundShadowInstancesVerified=True,
  nativeFloorShadowCoverageAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False,
  actualVisualReview='Native Prison scenes retain true own actors/outfits/palettes/pose groups and floor shadows throughout tested basic moves, both added player slots, natural recovery and final own ready. All accepted128fullRGB fields were held/digested in RAM and inspected in contact sheets; full native falling/uppercut images reviewed for four added slots. Different arena/CPU/repeated/KO/overlap/special-move phases and full renderer/body-pixel/audio/campaign/finisher scope are not inferred as accepted.',
  preservedCounterexamples=[
   '5067 wrong controller basename failed before starting any native process. Report5069 preserved;5071 selects actual5065 source in fresh folders.',
   '5065 initial simultaneous Down+HP900..902 only crouched and never entered uppercut. Native actual fields proved this; no acceptance of that diagnostic as uppercut. Fresh5075 physical Down900..923,HP910..912 genuinely reaches0107launch then0603strike and natural recovery.',
   '5075 all six traces prove650alreadylanded (air605..642), so its air_fall label was false. Fresh5081 retains650aslanding and observes actual descending635/apex622 plus strike/recovery fields. Older stock-label mismatch explicitly recorded in finite proof.',
   '5087 plateau-wide minY check allowed a one-field corrupted622apex because other real apex fields still reached95. Original failed source unchanged and failure reproduced. Fresh5089 adds explicit native first-apex field622=ownfloor-95 and keeps whole actual stock-normalized trajectory comparison. All180real faults rejected.',
   'Original stock Sub-Zero raw ice-hand025816F6 still source/group/digest/geometry checked but its compressed row stepping is explicitly unaccepted. All imported owned normal move parts remain strictly compressed6 and each native copy independently checked.'],
  completedNativeHostHandles=[31169,40960,26344,50506,89892,26781,46087,35222,47491,55650,7517],
  completedVerifierHostHandles=[87216],allRecordedNativeHandlesConsumedTerminalZero=True,candidateProcessesStillRunning=False,
  publicCMDExecutableZIPAndHistoricalInstalledEXEUnchanged=True,dirtyCheckoutUnchanged=True,
  newIsolatedBuildsThisContinuation=0,newPayloadCopiesThisContinuation=0,rawGuestGFXRGBPCMOrWAVFilesWritten=0,
  oldBuildFolderDeletionsThisContinuation=0,currentAddedTraceLogicalBytes=logical,currentAddedTraceAllocatedBytes=disk,
  currentAddedTraceAllocatedMiB=round(disk/(1024**2),2),
  cleanupAccounting='Actual NTFS compressed trace/report inventory measured, no new executable/payload/full build tree. Existing4992 reused, all guest/graphics/RGB/32MiB interleaved source bytes RAM-only, no raw media files. Prior32.49GiB cleanup retained; no retired evidence restored.',
  nextAction='Continue all five original groups. Broaden remaining special moves/body art/grounding/shadows to other native arenas and real CPU/repeated/KO/overlap/contact cases. Continue native Pit/Tomb mirror/branch/victim/audio, all other finishers/victims/morphs/secrets/cinematics, actual natural Kintaro/ShaoKahn campaign clears/own endings/attract, final combined UI/names/audio regression, dependency-aware obsolete-folder cleanup and refreshed final release ZIP. Current native basic-move matrix is not promotion or completion.')
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress compact full-scope checkpoint')
 (OUT/'preserved_apex_plateau_failure.json').write_text(json.dumps(dict(source='tools/verify_move_phase_shadow_v5087.py',exitCode=failed.returncode,stdout=failed.stdout,stderr=failed.stderr),indent=2)+'\n')
 (OUT/'progress.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps(dict(passed=True,path=str(OUT/'progress.json'),goalStatus='active',nativeColdBoots=11,
  verifiedPlayerSlotCases=4,actualImportedShadowCopies=5260,actualFaultsRejected=180,
  newBuilds=0,rawMediaFiles=0,addedTraceAllocatedMiB=record['currentAddedTraceAllocatedMiB'],remaining=record['remaining']),indent=2))

if __name__=='__main__':main()
