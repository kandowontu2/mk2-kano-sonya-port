"""Additive full-scope current shatter checkpoint; exact terminal compression.

Four genuine current earned freeze/shatter/next-match runs and all16 actual
native panels reviewed. Sparse pixels are not continuous raster/FIFO/shadow or
audio proof. Retain all original requirement groups and failed host checks.
"""
import json,subprocess
from datetime import datetime,timezone
from pathlib import Path
import checkpoint_current_kitana_scene_v6121 as storage
ROOT,need,sha,current=storage.ROOT,storage.need,storage.sha,storage.current
PARENT=ROOT/'audit_v6152_current_jax_arms_native_scene_progress/progress.json'
PROOF=ROOT/'audit_v6175_current_subzero_shatter_checked/report.json'
OUT=ROOT/'audit_v6169_current_subzero_shatter_progress'

def run():
 previous=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text())
 need(previous['passed']and previous['goalStatus']=='active'and len(previous['remaining'])==5,'Original complete port scope remains active')
 need(proof['passed']and proof['candidate']==current.NAME and proof['executableSHA256']==current.EXE_SHA and
      proof['guestSHA256']==current.GUEST_SHA and len(proof['cases'])==4 and proof['actualConsecutiveVictimFields']==2550 and
      proof['actualSemanticFaultsRejected']==88 and proof['actualNativePanelFaultsRejected']==8 and
      proof['actualNativeRefillStores']==648 and proof['actualNativeReviewPanels']==16 and proof['actualEventRGBPixels']==1625600 and
      proof['completeOriginalStateMatrixRetained']and proof['allNativeReviewPanelsActualPixelBound']and
      not proof['continuousNativeSceneReplayAccepted']and not proof['nativeFloorShadowCoverageAccepted']and
      not proof['normalHealthFreezeAccepted']and not proof['fullArtAcceptance']and not proof['fullAudioAcceptance']and
      not proof['fullPortAcceptance'],'Finite current native whole-state/event-pixel/refill/next-match matrix, without broader claims')
 pins={str(p.resolve()):sha(p)for p in(PARENT,PROOF,Path(__file__),Path(storage.__file__))}
 for p,h in proof['inputHashes'].items():need(sha(p)==h,'All actual current/protected source and native observations intact');pins[p]=h
 current.expected()
 failures=[]
 for version,reason in [(6167,'Wrong actual current report path before matrix execution'),
                        (6171,'Old single-refill check used on a recording containing next-CPU second refill'),
                        (6173,'Nested source pin scope omitted precursor variables after native/state/pixel checks')]:
  p=ROOT/f'audit_v{version}_current_subzero_shatter_checked/report.json';r=json.loads(p.read_text())
  need(not r['passed']and not r['fullPortAcceptance'],'Keep exact failed host-harness report, no native restart or predicate deletion')
  pins[str(p.resolve())]=sha(p)
  failures.append(dict(report=str(p),reason=reason,nativeGameFailure=False,nativeBootsRestarted=0))
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C','Actual current delivered release unchanged');pins[str(archive)]=sha(archive)
 exe=ROOT/current.NAME/'mkport_candidate.exe'
 query="Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq '"+str(exe).replace("'","''")+"' } | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'Actual current native process census empty before bounded terminal compression')
 targets=[]
 for c in proof['cases']:
  need(c['actualWindowsTerminal']['nativeExit']==0 and c['allOriginalNativeRowsAndFourRGBEventsEqualProtectedBaseline']and
       c['actualNativeReviewPanels']==4 and c['nativeInterRoundRefill']['totalActualRefillStores']==162 and
       c['nativeInterRoundRefill']['completeNextCPURefillAccepted'],'Every real native terminal, complete baseline comparison and both refills')
  folder=(ROOT/f"audit_v6164_current_subzero_{c['fighter']}_p{c['side']}_lifecycle").resolve()
  need(folder.parent==ROOT.resolve(),'Exact resolved terminal target in user-named workspace')
  for p in folder.iterdir():
   if p.is_file()and p.suffix in('.json','.log'):
    need(str(p.resolve())in pins,'Only exact already hash-bound terminal records compressed')
    targets.append(p)
 before={str(p):storage.allocated(p)for p in targets}
 result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',*[str(p)for p in targets]],capture_output=True,text=True)
 need(result.returncode==0 and all(sha(p)==h for p,h in pins.items()),'Exact lossless terminal compression preserves every source and observation')
 after={str(p):storage.allocated(p)for p in targets}
 audit=previous['requirementAudit'];item=next(r for r in audit if r['requirement'].startswith('Natural finishers'))
 item['status']+=' Current Sub-Zero earned freeze-and-shatter qualifies both true own characters in both physical slots: eight collision-earned KOs, genuine FFD-HK and FDFF-HP histories, original69center-gap gate, dedicated own MAIN40 row, frozen-body/semantic-leg groups and ice palette/emitter/sound-call task, original64field parked-leg loop,2550consecutive actual victim fields through natural departure and four subsequent CPU matches with fresh161health/valid actors. Both complete81store physical-slot refill chains in each recording qualified,648stores total. Every native/input/state/effect/lifecycle trace row and all16actual event-bound complete RGB fields equal the protected semantic-leg native baseline.88actual state/refill and8actual native panel corruption checks rejected; all16whole native panels visibly reviewed and pixel-bound. Three host harness failures retained: wrong report path, single-refill assumption, missing nested source-pin variable; no native rerun or guest/game edit. Sparse freeze/fracture/victory/next-match raster review only: continuous native scene/FIFO/grounding/floor-shadow, normal-health freeze, complete finisher audio, wider arenas/CPU/overlap/cinematic consumers and integrated full release remain unproven.'
 item['evidence'].append(dict(path=str(PROOF),sha256=sha(PROOF)))
 return dict(passed=True,observedUTC=datetime.now(timezone.utc).isoformat(),goalStatus='active',parentAdditiveJournal=str(PARENT),
   remaining=previous['remaining'],requirementAudit=audit,newInputHashes=pins,
   previousGoalTurnClassification='no progress: gratitude-only reply; revalidated authoritative inputs and no prior live native run before starting new work',
   thisTurnClassification='progress: four actual current earned shatter/next-match contexts and complete whole-state/reference/refill/pixel controls qualified',
   actualCurrentVictimContexts=4,actualNormallyEarnedKOs=8,actualConsecutiveVictimFields=2550,actualNextCPUMatches=4,
   actualNativeRefillStores=648,actualNativeReviewPanelsViewedAndPixelBound=16,actualEventRGBPixels=1625600,
   actualSemanticFaultsRejected=88,actualNativePanelFaultsRejected=8,failedHostChecksRetained=failures,
   terminalOnlyFilesLosslesslyCompressed=len(targets),logicalBytes=sum(p.stat().st_size for p in targets),
   allocatedBytesBefore=sum(before.values()),allocatedBytesAfter=sum(after.values()),allocatedBytesReclaimed=sum(before.values())-sum(after.values()),
   actualBefore=before,actualAfter=after,compressionOutput=result.stdout,
   newNativeBootsStarted=4,nativeGameChanges=0,newBuildCopies=0,newSourceDirectoryCopies=0,rawMediaFilesWritten=0,filesDeleted=0,
   currentReleaseZIPUnchanged=True,continuousNativeSceneReplayAccepted=False,nativeFloorShadowCoverageAccepted=False,
   normalHealthFreezeAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,fullGoalComplete=False,
   nextActions=['Complete current Sub-Zero continuous native scene/FIFO/ground/floor-shadow and original finisher audio',
                'Cover remaining cinematic/arena/CPU/overlap consumers without proxies or forced transitions',
                'Final integrated selection/ladder/names/moves/audio regression and matching release/cleanup audit'])

if __name__=='__main__':
 need(not OUT.exists(),'Fresh full-scope current shatter checkpoint')
 report=run();OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('requirementAudit','newInputHashes','actualBefore','actualAfter','compressionOutput')},indent=2),flush=True)
