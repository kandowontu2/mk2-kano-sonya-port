"""Additive full-goal checkpoint; physical normal ice and actual source-bound shadows."""
import hashlib,json,subprocess
from pathlib import Path
import native_subzero_legs_context_v4993 as native

ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v5028_native_subzero_legs_runtime_progress/progress.json'
CHECKED=ROOT/'audit_v5060_normal_subzero_freeze_shadow_checked/report.json'
OUT=ROOT/'audit_v5062_normal_subzero_freeze_progress'

def main():
 need(not OUT.exists(),'Fresh additive complete-scope checkpoint')
 parent=json.loads(PARENT.read_text());checked=json.loads(CHECKED.read_text())
 need(parent['goalStatus']=='active'and len(parent['remaining'])==5,'All original unfinished scope remains intact')
 need(checked['passed']and checked['actualOrdinaryHealthCases']==6 and checked['actualAddedFighterPlayerSlotCases']==4 and
      checked['actualStockControlCases']==2 and checked['actualOrdinaryFields']==4206 and
      checked['actualSourceBoundCompressedShadowCopies']==3112 and checked['actualAddedFighterCompressedShadowCopies']==1044 and
      len(checked['actualFaultsRejected'])==126 and checked['repeatedSonyaP1AllFourEntireRGBFieldsIdentical'],
      'Actual independently source-bound finite ordinary ice/shadow matrix')
 need(not checked['fullPortAcceptance']and not checked['nativeFloorShadowCoverageAccepted']and
      not checked['normalHealthFreezeCoverageAccepted'],'Finite matrix does not replace the full requirement')
 pins={}
 def pin(p,h=None):
  p=Path(p).resolve();actual=sha(p);need(h is None or actual==h,'Current authoritative immutable input')
  need(str(p)not in pins or pins[str(p)]==actual,'Consistent immutable pin');pins[str(p)]=actual
 for p in(PARENT,CHECKED,Path(__file__),Path(native.__file__)):pin(p)
 for p,h in checked['inputHashes'].items():pin(p,h)
 for name in('run_normal_subzero_freeze_v5033.py','run_normal_subzero_freeze_projection_v5039.py',
              'run_normal_subzero_freeze_projection_v5045.py','run_normal_subzero_freeze_review_v5053.py',
              'verify_normal_subzero_freeze_shadow_v5057.py','verify_normal_subzero_freeze_shadow_v5059.py'):
  pin(ROOT/'tools'/name)
 for name in('mk2ks_normal_subzero_freeze_v5031.lua','mk2ks_normal_subzero_freeze_projection_v5037.lua',
              'mk2ks_normal_subzero_freeze_projection_v5043.lua','mk2ks_stock_fatality_v1021.lua'):pin(ROOT/name)
 failed=[]
 for fighter,side in [('kano',1),('kano',2),('sonya',1),('sonya',2)]:
  folder=ROOT/f'audit_v5040_normal_subzero_{fighter}_p{side}'
  path=ROOT/f'audit_v5041_normal_subzero_{fighter}_p{side}_observed/report.json';record=json.loads(path.read_text())
  need(not record['passed']and record['error']=="ValueError('Native compressed six-bit fighter shadow stream')",
       'Preserve all four real strict collector counterexamples')
  pin(path)
  for p in folder.rglob('*'):
   if p.is_file():pin(p)
  failed.append(str(path))
 ordinary=ROOT/'audit_v5035_normal_subzero_sonya_p1_observed/report.json';pin(ordinary)
 for p in(ROOT/'audit_v5034_normal_subzero_sonya_p1').rglob('*'):
  if p.is_file():pin(p)
 # Reproduce unchanged executed5057's rejected NO-OP mutation (stock Liu already ID1).
 # This verifier launches no native process and creates no accepted output on failure.
 python=Path(r'C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe')
 error=subprocess.run([str(python),'-B',str(ROOT/'tools/verify_normal_subzero_freeze_shadow_v5057.py')],cwd=ROOT,text=True,capture_output=True)
 need(error.returncode==1 and 'Actual-record fault was accepted: proxy_identity'in error.stderr and
      not (ROOT/'audit_v5058_normal_subzero_freeze_shadow_checked').exists(),
      'Unchanged failed verifier still refuses acceptance; no accepted fault evidence fabricated')
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
 # The recorded handles were all consumed with terminal exit codes, not inferred from files.
 # Independently check real process state before recording the checkpoint.
 ps=subprocess.run(['powershell','-NoProfile','-Command',
  "@(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'mkport_candidate.exe' } | Select-Object ProcessId,ExecutablePath,CommandLine) | ConvertTo-Json -Depth 3 -Compress"],
  text=True,capture_output=True)
 need(ps.returncode==0 and not ps.stdout.strip(),'No live native candidate process remains')
 need(all(sha(p)==h for p,h in pins.items()),'All authoritative current inputs stable')
 report=dict(schema=1,baseFullScopeCheckpoint=parent['baseFullScopeCheckpoint'],
  parentAdditiveJournals=parent['parentAdditiveJournals']+[str(PARENT)],remaining=parent['remaining'],
  goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
  mergeRule='Additive to4557 and every parent. Finite ordinary freeze/thaw/controls and native source-bound shadow evidence only. None of the five original unfinished groups is deleted, weakened or replaced with passing cases.',
  previousGoalTurnClassification='progress: frozen-leg lifecycle checkpoint5028 and initial real Sonya ordinary-health freeze/thaw/control evidence5034/5035 changed the next action. The subsequent thank-you acknowledgement itself made no additional progress.',
  thisGoalTurnClassification='progress: re-polled actual29259 to terminal failure, checked real native process state, retained four original schema failures. Diagnosed source-proven stock Sub-Zero raw hand at025816F6/6000 or6010, kept its compressed stepping explicitly unaccepted. Fresh strict source-bound imported-stream collector5043/5045 and seven actual physical ordinary ice runs. Independently reconstructed all32 compiled original/imported graphics ROM lanes in RAM. Verified six cases/four added player slots/two stock controls,4206 live fields,160 original frozen fields per case, native human D,F,LP task13 branch, natural own palette restoration, movement and punch recovery. Verified1044 imported own shadow copies/3112 complete compressed copies with exact ROM-group/cache ownership/world-camera/native-B7/quarter-height row sources/pen/PC and full bounds.126 actual semantic/source record faults rejected. Repeated SonyaP1 four entireRGB fields identical and all four directly viewed after the first tool output truncated. No game code changes/build/raw media files/public promotion.',
  newInputHashes=pins,checkedOrdinaryFreezeAndShadowMatrix=str(CHECKED),compiledCandidate=native.NAME,
  executableSHA256=native.EXE_SHA,payloadSHA256=native.PAYLOAD_SHA,initializedGuestSHA256=native.GUEST_SHA,
  nativeColdBootInstancesThisContinuation=8,normalHealthFreezeThawAndControlsInstancesVerified=True,
  actualAddedFighterSlotInstances=4,actualStockControlInstances=2,actualOrdinaryLiveFields=4206,
  sampledNativeSourceBoundShadowInstancesVerified=True,actualAddedFighterShadowCopies=1044,
  actualCompressedShadowCopies=3112,actualSemanticFaultsRejected=126,
  actualNativeIcePath='Original human Sub-Zero LowPunch command pathFF866410 -> FF86F9D0 -> FF86FE30 -> FF8A5900 shared original special implementation, projectile13. Actual ID8/human selection retained; no fabricated proxy, register/health/position or RNG write.',
  ordinaryVictimSemantics='True17/18 own regular poses and blue0505 palette for160fields, full161health, natural own normal palette and physical move/punch recovery. Ordinary0401 ice is not the deep0616/shatter finisher and never substituted with a frozen-death master.',
  originalDirectShadowKernelUnchanged=True,normalHealthFreezeCoverageAccepted=False,nativeFloorShadowCoverageAccepted=False,
  fullArtAcceptance=False,fullAudioAcceptance=False,
  actualVisualReview='Kano/Sonya P1 andP2 before/ice/wait/post-controls directly reviewed from actual full RAM RGB. Same native scene shows own outfits/blue freeze/palette restoration and floor shadow geometry. Stock KitanaP1 and LiuP2 are physical comparison cases. SonyaP1 fresh review5054 is byte-identical across all four fields to5046, correcting first tool-output truncation. Unsampled phases/arenas/CPU/repeated/KO/overlap coverage is not inferred.',
  stockRawCounterexample='Original Sub-Zero ice-hand descriptorFF980B70 component0: graphic025816F6,width11,height18,command6000/6010. Source ROM-group and actual graphics-byte digest/native projected geometry/count/pen checked. Original hardcoded compressed6 row scanner on this raw stock part retained, not claimed as compressed/source-stepping acceptance. All actual imported own components still strictly compressed6 and every native row checked against independently interleaved source ROMs.',
  preservedFailedCollectorReports=failed,
  preservedFailedVerifier='5057 negative proxy_identity mutation set stock Liu ID1 to1 and therefore made no fault. Original failing source unchanged; unchanged failure reproduced in preserved_noop_fault_failure.json. Fresh5059 changes the injected ID only to an actually different identity, every six case rejects21 real faults; no requirement weakened.',
  collectorDigestLogCompatibility='5045 emitted a literal backslash-n after PART_DIGEST, merging the first next DMA tag on that text line. Independent parser splits exactly that emitted tag separator, preserving actual DMA records;5053 fresh review fixes formatting only. Never restores or writes raw buffers.',
  completedNativeHostHandles=[29259,45495,80713,26118,94190,69164,84860],
  terminalFailedNativeHostHandles=[29259],terminalZeroNativeHostHandles=[45495,80713,26118,94190,69164,84860],
  terminalDirectHostCases=['kanoP1_5046','kanoP1_5040_failure','kanoP2_5040_failure','sonyaP2_5040_failure'],
  candidateProcessesStillRunning=False,publicCMDExecutableZIPAndHistoricalInstalledEXEUnchanged=True,
  dirtyCheckoutUnchanged=True,newIsolatedBuildsThisContinuation=0,newPayloadCopiesThisContinuation=0,
  rawGuestGFXRGBPCMOrWAVFilesWritten=0,oldBuildFolderDeletionsThisContinuation=0,
  cleanupAccounting='Reuse4992 without new binary, payload or full build tree. Actual guest/normal sprite GFX/RGB and independently interleaved32MiB GFX exist only in RAM. Only compact compressed traces/digests/checkpoints added; prior32.49GiB cleanup retained. No retired evidence restored.',
  nextAction='Keep all five original groups. Broaden real ordinary special/floor-shadow coverage through jumping/crouching/attacks/CPU/repeated/KO/overlap and other arenas, not only four idle/ice checkpoints. Continue native Pit/Tomb mirror/branch/victim/audio, full art/grounding, all other finisher/victim/morph/secret/cinematic, actual natural Kintaro/Shao campaign clears/own endings/attract, final combined selection/ladder/names/audio regression, dependency-aware obsolete-folder cleanup and refreshed final release ZIP. Do not promote public playtest from this finite matrix alone.')
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed progress proof')
 (OUT/'preserved_noop_fault_failure.json').write_text(json.dumps(dict(source='tools/verify_normal_subzero_freeze_shadow_v5057.py',exitCode=error.returncode,stdout=error.stdout,stderr=error.stderr),indent=2)+'\n')
 (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=True,path=str(OUT/'progress.json'),goalStatus='active',actualNativeCaseCount=6,
  actualImportedShadowCopies=1044,actualFaultsRejected=126,newBuilds=0,newRawMediaFiles=0,originalRemainingGroups=report['remaining']),indent=2))

if __name__=='__main__':main()
