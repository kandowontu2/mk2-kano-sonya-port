"""Four actual current head-clap scenes; preserve full scope and compact terminals."""
import json,subprocess
from datetime import datetime,timezone
from pathlib import Path
import checkpoint_current_kitana_scene_v6121 as storage
ROOT,need,sha,current=storage.ROOT,storage.need,storage.sha,storage.current
PARENT=ROOT/'audit_v6133_current_kung_lao_native_scene_progress/progress.json'
PROOF=ROOT/'audit_v6138_current_jax_clap_scene_checked/report.json'
OUT=ROOT/'audit_v6140_current_jax_clap_native_scene_progress'

def run():
 previous=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text())
 need(previous['passed']and previous['goalStatus']=='active'and len(previous['remaining'])==5,'All original requirement groups remain open')
 need(proof['passed']and proof['actualContexts']==4 and proof['exactNativeFields']==2596 and proof['exactRGBPixels']==263753600 and
      proof['actualSemanticFaultsRejected']==100 and proof['actualNativePixelTargetFaultsRejected']==8 and
      proof['currentEarnedClapStateFullSceneFIFOProjectionGroundingShadowAndCleanupAccepted']and
      not proof['fullAudioAcceptance']and not proof['fullPortAcceptance'],'Complete four-context actual scene/state/FIFO/shadow matrix and108real corruption controls')
 need(all(sha(p)==h for p,h in proof['inputHashes'].items()),'Every actual executed input/native review intact')
 current.expected()
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C','Current delivered ZIP unchanged')
 exe=ROOT/current.NAME/'mkport_candidate.exe'
 query="Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq '"+str(exe).replace("'","''")+"' } | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'Real native emulator census empty before exact terminal compression')
 targets=[];reviews=[]
 for c in proof['cases']:
  need(c['actualWindowsTerminal']['nativeExit']==0,'Actual native exit precedes cleanup')
  folder=(ROOT/f"audit_v6135_current_jax_clap_{c['fighter']}_p{c['side']}_native_scene_ram").resolve()
  need(folder.parent==ROOT.resolve(),'Resolved exact capture inside user-named workspace')
  review=Path(c['nativeReview']);need(review.is_file()and str(review.resolve())in proof['inputHashes'],'Actual reviewed native sheet hash-bound')
  reviews.append(dict(fighter=c['fighter'],side=c['side'],path=str(review),sha256=sha(review)))
  for p in folder.iterdir():
   if p.is_file():
    need(p.suffix in('.json','.log')and str(p.resolve())in proof['inputHashes'],'Only completed already hash-bound traces and metadata')
    targets.append(p)
 before={str(p):storage.allocated(p)for p in targets}
 result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',*[str(p)for p in targets]],capture_output=True,text=True)
 need(result.returncode==0 and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Exact-file LZX preserves all logical native/source/review bytes')
 after={str(p):storage.allocated(p)for p in targets}
 audit=previous['requirementAudit'];item=next(r for r in audit if r['requirement'].startswith('Natural finishers'))
 item['status']+=' Current Jax head-clap now qualifies four true own-character/physical-slot contexts: eight collision-earned KOs, whole original command/health/parser/position-table/completion grammar and unchanged original task except declared19row table. All28owned headless-collapse poses,2596continuous native fields and263753600displayed RGB pixels source-replayed. Complete body FIFO/component/palette/camera/grounding/native compressed-shadow and exact pointer teardown/held-page behavior checked.100actual semantic and8actual native RGB/VRAM target corruptions rejected. All four actual seven-phase/post-match review sheets visually inspected; own bodies and native lifebar names retained without selection overlays or proxy identities. No game edit justified. Stock-reference head-clap page comparison, alternate costumes, full audio, other finishers/arenas/CPU and integrated acceptance remain open.'
 item['evidence'].append(dict(path=str(PROOF),sha256=sha(PROOF)))
 return dict(passed=True,observedUTC=datetime.now(timezone.utc).isoformat(),goalStatus='active',
      parentAdditiveJournal=str(PARENT),remaining=previous['remaining'],requirementAudit=audit,
      newInputHashes={str(p):sha(p)for p in(PARENT,PROOF,archive,Path(__file__).resolve(),Path(storage.__file__).resolve())},
      previousGoalTurnClassification='progress: current Kung Lao split and two stock lifecycle controls qualified',
      thisTurnClassification='progress: four actual current Jax head-clap native scenes, complete original state/FIFO/shadow and finite art review qualified',
      currentOwnContexts=4,exactNativeFields=2596,exactRGBPixels=263753600,actualSemanticFaultsRejected=100,actualNativePixelTargetFaultsRejected=8,
      finiteSevenPhaseAndPostMatchNativeReviewAccepted=True,actualReviewedSheets=reviews,
      terminalOnlyFilesLosslesslyCompressed=len(targets),logicalBytes=sum(p.stat().st_size for p in targets),
      allocatedBytesBefore=sum(before.values()),allocatedBytesAfter=sum(after.values()),allocatedBytesReclaimed=sum(before.values())-sum(after.values()),
      actualBefore=before,actualAfter=after,compressionOutput=result.stdout,nativeGameChanges=0,newNativeBootsStarted=4,
      newBuildCopies=0,newSourceDirectoryCopies=0,rawMediaFilesWritten=0,filesDeleted=0,currentReleaseZIPUnchanged=True,
      fullGoalComplete=False,fullAudioAcceptance=False,fullPortAcceptance=False,
      nextActions=['Exercise current Jax arm-rip/Subzero native finisher victim consumers',
                   'Complete native finisher/stage audio and broader arena/CPU/KO/overlap coverage',
                   'Run final integrated selection-to-gameplay and matching release audit'])

if __name__=='__main__':
 need(not OUT.exists(),'Fresh full-scope additive head-clap checkpoint')
 report=run();OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('requirementAudit','newInputHashes','actualReviewedSheets','actualBefore','actualAfter','compressionOutput')},indent=2),flush=True)
