"""Finite current split acceptance, stock held-page controls, lossless terminal cleanup.

Preserve every original requirement group. No game/build/package mutation.
"""
import json,subprocess
from datetime import datetime,timezone
from pathlib import Path
import checkpoint_current_kitana_scene_v6121 as storage
ROOT,need,sha,current=storage.ROOT,storage.need,storage.sha,storage.current
PARENT=ROOT/'audit_v6122_current_kitana_native_scene_progress/progress.json'
PROOF=ROOT/'audit_v6131_current_kung_lao_scene_checked/report.json'
PRIOR_STORAGE=ROOT/'audit_v6124_current_kitana_terminal_storage_checked/report.json'
OUT=ROOT/'audit_v6133_current_kung_lao_native_scene_progress'

def run():
 previous=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text())
 need(previous['passed']and previous['goalStatus']=='active'and len(previous['remaining'])==5,'All original requirement groups remain open')
 need(proof['passed']and proof['actualContexts']==6 and proof['ownContexts']==4 and proof['currentStockReferenceContexts']==2 and
      proof['exactNativeFields']==3840 and proof['exactRGBPixels']==390144000 and
      proof['actualSemanticFaultsRejected']==160 and proof['actualNativePixelTargetFaultsRejected']==12 and
      proof['currentSplitConstructorStreamMirrorPaletteStateAndSceneAccepted']and proof['currentStockHeldWinnerPageSemanticsAccepted']and
      not proof['fullAudioAcceptance']and not proof['fullPortAcceptance'],'Full actual split scene/state/FIFO/shadow matrix and corruption tests accepted')
 need(all(sha(p)==h for p,h in proof['inputHashes'].items()),'All actual source/media evidence unchanged')
 current.expected()
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C','Current delivered ZIP unchanged')
 exe=ROOT/current.NAME/'mkport_candidate.exe'
 query="Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq '"+str(exe).replace("'","''")+"' } | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'Real native process census empty before compression')
 targets=[]
 reviews=[]
 for c in proof['cases']:
  need(c['actualWindowsTerminal']['nativeExit']==0,'Real terminal precedes cleanup')
  folder=(ROOT/f"audit_v6126_current_kung_lao_{c['fighter']}_p{c['side']}_native_scene_ram").resolve()
  need(folder.parent==ROOT.resolve(),'Resolved exact capture lies inside user-named workspace')
  review=Path(c['nativeReview']);need(review.is_file()and str(review.resolve())in proof['inputHashes'],'Actual reviewed native sheet hash-bound')
  reviews.append(dict(fighter=c['fighter'],side=c['side'],stockReferenceOnly=c['stockReferenceOnly'],path=str(review),sha256=sha(review)))
  for p in folder.iterdir():
   if p.is_file():
    need(p.suffix in('.json','.log')and str(p.resolve())in proof['inputHashes'],'Only completed hash-bound trace/metadata files')
    targets.append(p)
 before={str(p):storage.allocated(p)for p in targets}
 result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',*[str(p)for p in targets]],capture_output=True,text=True)
 need(result.returncode==0 and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Lossless exact-file LZX preserves all logical bytes')
 after={str(p):storage.allocated(p)for p in targets}
 audit=previous['requirementAudit'];item=next(r for r in audit if r['requirement'].startswith('Natural finishers'))
 item['status']+=' Current Kung Lao vertical split now qualifies four true own-character/physical-slot contexts and two real current stock references: twelve normally earned KOs, whole native constructor/MAIN0/paired animation source, own split stream/secondary actor/mirror/palette/FIFO/projection/grounding/shadow and cleanup. All3840continuous native fields and390144000displayed RGB pixels source-replayed.160actual semantic and12actual native RGB/VRAM target faults rejected. All six actual ten-phase/post-match review sheets visually inspected; no donor/proxy own identity. Stock and own final corpse halves intentionally remain on the native held winner page after pointer retirement without new actor FIFO or new render; no forced screen-clear workaround. Full audio, other finishers/arenas/CPU and final integrated acceptance remain open.'
 item['evidence'].append(dict(path=str(PROOF),sha256=sha(PROOF)))
 return dict(passed=True,observedUTC=datetime.now(timezone.utc).isoformat(),goalStatus='active',
      parentAdditiveJournal=str(PARENT),remaining=previous['remaining'],requirementAudit=audit,
      newInputHashes={str(p):sha(p)for p in(PARENT,PROOF,PRIOR_STORAGE,archive,Path(__file__).resolve(),Path(storage.__file__).resolve())},
      thisTurnClassification='progress: six actual current Kung Lao split scenes, complete state/render matrix and original held-page lifecycle qualified',
      currentOwnContexts=4,currentStockReferenceContexts=2,exactNativeFields=3840,exactRGBPixels=390144000,
      actualSemanticFaultsRejected=160,actualNativePixelTargetFaultsRejected=12,
      finiteTenPhaseAndPostMatchNativeReviewAccepted=True,actualReviewedSheets=reviews,
      terminalOnlyFilesLosslesslyCompressed=len(targets),logicalBytes=sum(p.stat().st_size for p in targets),
      allocatedBytesBefore=sum(before.values()),allocatedBytesAfter=sum(after.values()),
      allocatedBytesReclaimed=sum(before.values())-sum(after.values()),actualBefore=before,actualAfter=after,compressionOutput=result.stdout,
      nativeGameChanges=0,newNativeBootsStarted=6,newBuildCopies=0,newSourceDirectoryCopies=0,rawMediaFilesWritten=0,
      filesDeleted=0,currentReleaseZIPUnchanged=True,fullGoalComplete=False,fullAudioAcceptance=False,fullPortAcceptance=False,
      nextActions=['Exercise current Jax/Subzero native finisher victim consumers',
                   'Complete native finisher/stage audio and broader arena/CPU/KO/overlap coverage',
                   'Run final integrated selection-to-gameplay and matching release audit'])

if __name__=='__main__':
 need(not OUT.exists(),'Fresh full-scope additive split checkpoint')
 report=run();OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('requirementAudit','newInputHashes','actualReviewedSheets','actualBefore','actualAfter','compressionOutput')},indent=2),flush=True)
