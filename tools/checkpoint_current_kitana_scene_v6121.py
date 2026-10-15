"""Current native Kitana victim scenes, full-scope checkpoint and bounded cleanup."""
import ctypes,json,subprocess
from ctypes import wintypes
from datetime import datetime,timezone
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v6105_current_mileena_lifecycle_progress/progress.json'
PROOF=ROOT/'audit_v6117_current_kitana_scene_checked/report.json'
OUT=ROOT/'audit_v6122_current_kitana_native_scene_progress'

def allocated(path):
 kernel=ctypes.WinDLL('kernel32',use_last_error=True)
 query=kernel.GetCompressedFileSizeW;query.argtypes=(wintypes.LPCWSTR,ctypes.POINTER(wintypes.DWORD));query.restype=wintypes.DWORD
 high=wintypes.DWORD();ctypes.set_last_error(0);low=query(str(path),ctypes.byref(high))
 need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual Windows allocated file size available')
 return(high.value<<32)|low

def run():
 previous=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text())
 need(previous['passed']and previous['goalStatus']=='active'and len(previous['remaining'])==5,'Keep every original requirement group open')
 need(proof['passed']and proof['actualContexts']==4 and proof['exactNativeFields']==2948 and
      proof['exactRGBPixels']==299516800 and proof['actualSemanticFaultsRejected']==100 and
      proof['currentEarnedInflationSceneFIFOProjectionGroundingShadowAndEraseAccepted']and
      proof['finiteSixPhaseAndPostRemovalNativeReviewAccepted']and proof['allCurrentNativeRGBFieldsEqualProtectedReference']and
      not proof['fullAudioAcceptance']and not proof['fullPortAcceptance']and
      all(sha(p)==h for p,h in proof['inputHashes'].items()),'Whole current earned native state/pixels/FIFO/shadow/erase matrix and100actual corruptions')
 current.expected()
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C','Delivered current playtest ZIP unchanged')
 exe=ROOT/current.NAME/'mkport_candidate.exe'
 query="Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq '"+str(exe).replace("'","''")+"' } | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'Actual native emulator census empty before exact terminal-only compression')
 targets=[]
 for c in proof['cases']:
  need(c['actualWindowsTerminal']['nativeExit']==0,'Native terminal precedes cleanup')
  folder=(ROOT/f"audit_v6114_current_kitana_{c['fighter']}_p{c['side']}_native_scene_ram").resolve()
  need(folder.parent==ROOT.resolve(),'Exact compression target lies inside user-named workspace')
  for p in folder.iterdir():
   if p.is_file():
    need(p.suffix in('.json','.log')and str(p.resolve())in proof['inputHashes'],'Only already hash-bound terminal traces and metadata')
    targets.append(p)
 before={str(p):allocated(p)for p in targets}
 result=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',*[str(p)for p in targets]],capture_output=True,text=True)
 need(result.returncode==0 and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Exact LZX operation preserves every logical source/native/media evidence hash')
 after={str(p):allocated(p)for p in targets}
 audit=previous['requirementAudit'];item=next(r for r in audit if r['requirement'].startswith('Natural finishers'))
 item['status']+=' Current Kitana kiss/inflation qualifies both true own characters in both physical slots:8normally earned KOs,24owned inflation/burst poses,2948continuous source-replayed native fields,299516800exact displayed pixels, complete native FIFO/projection/floor-shadow rows and no victim/body/shadow residue after teardown. Every current native screen equals the entire protected source-qualified reference; all four existing six-phase/post-removal native review sheets inspected.100actual command/health/table/FIFO/body/shadow/cleanup corruptions rejected. Capture-host ID/process-variable collision is isolated without altering game code or rerunning matches. Full audio, other finishers, broader arena/CPU and integrated release scope remain open.'
 item['evidence'].append(dict(path=str(PROOF),sha256=sha(PROOF)))
 return dict(passed=True,observedUTC=datetime.now(timezone.utc).isoformat(),goalStatus='active',
      parentAdditiveJournal=str(PARENT),remaining=previous['remaining'],requirementAudit=audit,
      newInputHashes={str(PARENT):sha(PARENT),str(PROOF):sha(PROOF),str(archive):sha(archive),str(Path(__file__).resolve()):sha(__file__)},
      previousGoalTurnClassification='progress: current earned Mileena four-context physical lifecycle qualified',
      thisTurnClassification='progress: four genuine current Kitana finisher scenes rendered and complete command/state/FIFO/art/shadow/erase matrix verified',
      actualCurrentKitanaVictimContexts=4,exactNativeFields=2948,exactRGBPixels=299516800,newActualSemanticFaultsRejected=100,
      terminalOnlyFilesLosslesslyCompressed=len(targets),logicalBytes=sum(p.stat().st_size for p in targets),
      allocatedBytesBefore=sum(before.values()),allocatedBytesAfter=sum(after.values()),
      allocatedBytesReclaimed=sum(before.values())-sum(after.values()),compressionOutput=result.stdout,
      nativeGameChanges=0,newNativeBootsStarted=4,newBuildCopies=0,newSourceDirectoryCopies=0,rawMediaFilesWritten=0,
      newNativeReviewCopies=0,filesDeleted=0,currentReleaseZIPUnchanged=True,fullGoalComplete=False,
      nextActions=['Exercise current KungLao/Jax/Subzero native finisher victim consumers',
                   'Complete native finisher/stage voice/audio and broader arena/CPU/KO/overlap coverage',
                   'Run final integrated selection-to-gameplay and matching release audit'])

if __name__=='__main__':
 need(not OUT.exists(),'Fresh additive current native inflation checkpoint')
 report=run();OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('requirementAudit','newInputHashes','compressionOutput')},indent=2))
