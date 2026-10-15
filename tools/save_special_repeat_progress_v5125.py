"""Additive full-scope checkpoint: physical repeated moves, not final acceptance."""
import ctypes,json,subprocess
from pathlib import Path
from ctypes import wintypes
import native_subzero_legs_context_v4993 as native
ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v5092_move_phase_shadow_progress/progress.json'
PROOFS=[ROOT/'audit_v5116_special_repeat_checked/report.json',ROOT/'audit_v5124_square_air_repeat_checked/report.json']
OUT=ROOT/'audit_v5126_special_repeat_progress'
def main():
 need(not OUT.exists(),'Fresh additive full-scope progress')
 parent=json.loads(PARENT.read_text());proofs=[json.loads(p.read_text())for p in PROOFS]
 need(parent['goalStatus']=='active'and len(parent['remaining'])==5,'All five original unfinished scope groups retained')
 need(proofs[0]['passed']and proofs[0]['actualCases']==16 and proofs[0]['actualVerifiedSpecialCycles']==32 and proofs[0]['actualContiguousPostFields']==17806 and proofs[0]['sourceBoundBodyCandidates']==1016 and len(proofs[0]['actualSemanticFaultsRejected'])==194,'All eight moves both real player slots, strict ring glow and194 semantic counterexamples')
 need(proofs[1]['passed']and proofs[1]['actualCases']==2 and proofs[1]['actualVerifiedSpecialCycles']==4 and proofs[1]['actualContiguousPostFields']==2220 and proofs[1]['sourceBoundBodyCandidates']==130 and len(proofs[1]['actualSemanticFaultsRejected'])==26 and all(c['actualSquareContactVerified']and all(a['victimDamage']==27 for a in c['cycles'])for c in proofs[1]['cases']),'Four real airborne square-wave hits, source-bound bodies and26 counterexamples')
 need(all(not p['fullPortAcceptance']and not p['fullArtAcceptance']and not p['nativeFloorShadowCoverageAccepted']and not p['fullAudioAcceptance']for p in proofs),'Bounded test evidence never promoted to full acceptance')
 pins={};evidence=[]
 def pin(p,h=None):
  p=Path(p).resolve();actual=sha(p);need(h is None or actual==h,'Actual immutable compiled/source/evidence input');need(str(p)not in pins or pins[str(p)]==actual,'Consistent current pin');pins[str(p)]=actual
 for p in(PARENT,*PROOFS,Path(__file__),Path(native.__file__)):pin(p)
 for proof in proofs:
  for p,h in proof['inputHashes'].items():pin(p,h)
 for name in('mk2ks_special_repeat_v5093.lua','mk2ks_special_repeat_v5099.lua'):pin(ROOT/name)
 for number in(5095,5101):pin(ROOT/f'tools/run_special_repeat_v{number}.py')
 for number in(5105,5107,5109,5113,5115):pin(ROOT/f'tools/verify_special_repeat_v{number}.py')
 for name in('run_square_air_repeat_v5117.py','verify_square_air_repeat_v5121.py','verify_square_air_repeat_v5123.py'):pin(ROOT/'tools'/name)
 folders=[]
 for prefix in('audit_v5096_special_repeat_','audit_v5097_special_repeat_','audit_v5102_special_repeat_','audit_v5103_special_repeat_','audit_v5118_square_air_repeat_','audit_v5119_square_air_repeat_'):
  folders.extend(p for p in ROOT.glob(prefix+'*')if p.is_dir())
 for folder in[*folders,ROOT/'audit_v5114_special_repeat_checked',*(p.parent for p in PROOFS)]:
  for p in folder.rglob('*'):
   if p.is_file():pin(p);evidence.append(p)
 native_folders=[f for f in folders if f.name.startswith(('audit_v5102_','audit_v5118_'))]
 need(len(native_folders)==18,'Exactly18 fresh real native cold boots; prior9 separately inspected, not recounted')
 for folder in native_folders:
  result=json.loads((folder/'result.json').read_text());guest=json.loads((folder/'guest_memory_proof.json').read_text());gfx=json.loads((folder/'gfx_memory_proof.json').read_text())
  need(result['nativeExit']==0 and guest['sha256']==native.GUEST_SHA and guest['everyActualByteComparedInRAM']and gfx['bytes']==18976 and gfx['everyActualByteComparedInRAM'],'Every fresh boot actually terminated with fully checked cold guest/GFX')
 failures=[];python=Path(r'C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe')
 for name,expected in [('verify_special_repeat_v5105.py',"KeyError: 'move'"),('verify_special_repeat_v5107.py','Both entire genuine body composites evaluated in every sampled field'),('verify_special_repeat_v5109.py','No KO, replacement palette or external health restoration'),('verify_square_air_repeat_v5121.py','Actual semantic fault accepted: missing_physical_command')]:
  result=subprocess.run([str(python),'-B',str(ROOT/'tools'/name)],cwd=ROOT,text=True,capture_output=True)
  need(result.returncode==1 and expected in result.stderr,'Original failed observer/verifier source and actual predicate failure reproduced')
  failures.append(dict(source=name,exitCode=result.returncode,stdout=result.stdout,stderr=result.stderr))
 blade=json.loads((ROOT/'audit_v5097_special_repeat_blade_p1_kitana_observed/report.json').read_text())
 need(not blade['passed']and 'Actual own before/entry/recovery RGB captured for both cycles'in blade['error'],'Original blade-label collision evidence preserved, never passed retroactively')
 public_names=('PLAY_CURRENT_V1836_CHECKED.cmd','diagnostic_v1836_ball_register_boundary/mkport_candidate.exe','release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip','mame-mkp/mkport.exe','mame-mkp/src/mame/midway/midtunit_m.cpp','mame-mkp/src/mame/midway/midtunit_v.cpp','mk2/mk2-maincpu.bin')
 for name in public_names:
  p=(ROOT/name).resolve();need(str(p)in parent['newInputHashes'],'Original public/source pin retained');pin(p,parent['newInputHashes'][str(p)])
 native.expected()
 process=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'mkport_candidate.exe' } | Select-Object ProcessId,ExecutablePath) | ConvertTo-Json -Depth 3 -Compress"],capture_output=True,text=True)
 need(process.returncode==0 and not process.stdout.strip(),'Actual native processes terminal, no phantom active wait')
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);allocated=kernel.GetCompressedFileSizeW;allocated.argtypes=[wintypes.LPCWSTR,ctypes.POINTER(wintypes.DWORD)];allocated.restype=wintypes.DWORD
 disk=logical=0
 for p in set(evidence):
  high=wintypes.DWORD();ctypes.set_last_error(0);low=allocated(str(p),ctypes.byref(high));need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual NTFS allocation read')
  disk+=low+(high.value<<32);logical+=p.stat().st_size
 need(all(sha(p)==h for p,h in pins.items()),'Final compiled/evidence/public source pins unchanged')
 record=dict(schema=1,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,baseFullScopeCheckpoint=parent['baseFullScopeCheckpoint'],parentAdditiveJournals=parent['parentAdditiveJournals']+[str(PARENT)],remaining=parent['remaining'],
  mergeRule='Additive to all prior full-scope checkpoints. No requirement removed, no passing current subset redefines official/native game fidelity.',
  previousGoalTurnClassification='No progress: the previous acknowledgement turn only replied to thanks. Current continuation revalidated real terminal reports/process absence and proceeded with18 fresh physical cold boots and independent proofs.',
  thisGoalTurnClassification='Progress: corrected the blade observer recovery-label collision without changing game code. Executed all eight specials twice in both real player slots and verified32 native routine entries/recoveries,17806 complete post-engine actor fields,294 RAM RGB samples and1016 source-bound body candidates. Added two physical airborne-Kitana square cases: four actual27-damage air hits,2220 post-fields,38 RGB samples,130 source-bound body candidates and full natural recovery/ordinary movement+jump+punch. Strict current proof rejects220 actual semantic-record faults. Full scope remains open.',
  checkedRepeatMatrix=str(PROOFS[0]),checkedAirborneSquareInstances=str(PROOFS[1]),newInputHashes=pins,compiledCandidate=native.NAME,executableSHA256=native.EXE_SHA,payloadSHA256=native.PAYLOAD_SHA,initializedGuestSHA256=native.GUEST_SHA,
  newNativeColdBootInstances=18,previousColdBootReportsExamined=9,actualVerifiedSpecialCycles=36,actualContiguousPostEngineActorFields=20026,actualFullRGBFields=332,sourceBoundSampledBodyCandidates=1146,actualSemanticFaultsRejected=220,
  nativeRoutineEntriesAndBothCleanRecoveryStatesVerified=True,trueActorIDs17And18NeverProxied=True,physicalFollowupMovementJumpPunchVerified=True,stationarySquareWhiffInstancesVerified=True,airborneSquareHitInstancesVerified=True,
  entryFrameBodyPublicationUnproven=True,entryObservationExplanation='Entry marker is assigned by actual routine instruction tap after the native frame body draw. All36 entryRGB fields are real full native scene captures but their body publication provenance was not observed. All other296 sampled fields bind both complete owned terminated descriptors and exact original clipping/flip/display/FIFO publications. Do not infer entry art acceptance; next observer must start body taps before draw.',
  actualVisualReview='Native RAM contact sheets actually inspected for13 current ground-case sets: P1knife/ball/blade/choke/ring/square/leg and P2knife/ball/blade/choke/ring/leg. Images for P1bicycle/P2square/P2bicycle and both airborne square cases were not model-readable in tool output; their actual RGB transport hashes and source/state traces are checked, but their visual review remains open. No persistent raw PNG/RGB/guest/GFX/PCM files.',
  fullArtAcceptance=False,nativeFloorShadowCoverageAccepted=False,fullAudioAcceptance=False,
  preservedCounterexamples=['Original5095blade observer had two actual clean recoveries but phase40 overwrote both recoveredRGB labels. Actualgame execution successful; host correctlyfailed. Fresh5099 protects existing semantic marks and reruns18cases; no game patch.',
   '5105 incorrectly required move/side on cold GUEST/GFX digest tags; KeyError preserved and not counted as semantic rejection. Fresh5107 distinguishes those exact noncase tags.',
   '5107 expected body tap records at late-marked routine-entry frames. Actual missing record pairs are exactly the two entry frames percase. They are explicitly unproven in5115/5123; no broad art or renderer claim.',
   '5109 incorrectly treated source-defined Sonya ring charge glow as a replacement palette. Actual compiled router permits firstfour charge poses only, then restores own costume.5115 allows only those four poses with native bank0404/action4 and requires clean own palette at bothrecoveries/final. Two new uncharged-glow faults rejected; no broad palette relaxation.',
   '5113 allowed the uncharged release pose as a possible lagged glow, although actual samples and compiled router onlyusefourchargeposes. Original finite proof retained; strict5115 removes that allowance and rejects actual glows-on-uncharged-pose mutations.',
   '5121air-negative changed the firstcommand INPUT toUp, but thatfirstINPUTwasalreadythevictimUp. Original no-op fault rejected acceptance;5123 selects real attacker input and rejects it plus missingactualairbornecontact. No no-op or KeyError counted among220semanticfaults.'],
  preservedFailures=failures,completedNativeHostHandles=[38352,54542,65305,61113,69007,13150,56652,17045,26578,7134,77650,76434,6189,78542,61797,74069,70896,57013],completedVerifierHostHandles=[14780,36834],allRecordedNativeHandlesConsumedTerminalZero=True,candidateProcessesStillRunning=False,
  publicCMDExecutableZIPAndHistoricalInstalledEXEUnchanged=True,dirtyCheckoutUnchanged=True,newIsolatedBuildsThisContinuation=0,newPayloadCopiesThisContinuation=0,rawGuestGFXRGBPCMOrWAVFilesWritten=0,oldBuildFolderDeletionsThisContinuation=0,
  inspectedTraceLogicalBytes=logical,inspectedTraceAllocatedBytes=disk,inspectedTraceAllocatedMiB=round(disk/(1024**2),2),cleanupAccounting='Compressed trace/report allocation includes prior9boot evidence plus current18boots. No new binary/full build tree/payload copies/raw media. Prior32.49GiB cleanup remains retained; no retired data restored.',
  nextAction='Keep all five original groups. Start source/body observation before draw to close routine-entry provenance; review five currently unreadable visual sets in fresh RAM-only previews; extend repeated specials to actual native floor-shadow rows, other arenas, CPU, blocked, KO and overlap/victim cases. Continue broader Pit/Tomb branches/victims/audio, all finishers/victims/morphs/secrets/cinematics, genuine Kintaro/ShaoKahn campaign clears/own endings/attract, final combined UI/names/audio regression and dependency-aware obsolete-build cleanup/refreshed release ZIP. Do not promote current public launcher merely on this bounded32+4cycle check.')
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress compact checkpoint')
 (OUT/'progress.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(dict(passed=True,path=str(OUT/'progress.json'),goalStatus='active',actualVerifiedSpecialCycles=36,actualSemanticFaultsRejected=220,newBuilds=0,rawMediaFiles=0,inspectedTraceAllocatedMiB=record['inspectedTraceAllocatedMiB'],remaining=record['remaining']),indent=2))
if __name__=='__main__':main()
