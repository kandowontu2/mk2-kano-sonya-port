"""Lossless compact retained UI/audio text, verify bytes and actual allocation.

No history/source/current ROM/EXE/launcher/release deletion or raw media copies.
Preserve every original remaining scope group and all current acceptance pins.
"""
import ctypes,datetime,json,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5441_current_ui_audio_progress/progress.json'
OUT=ROOT/'audit_v5443_current_ui_audio_storage_progress'
BASES=('audit_v5428_current_ui_audio_ram','audit_v5431_current_ui_audio_ram',
 'audit_v5434_current_ui_audio_ram','audit_v5437_current_ui_audio_ram','audit_v5440_current_ui_audio_ram')

def run():
 current.expected();parent=json.loads(PARENT.read_text())
 need(parent['passed']and parent['currentBothSlotSelectionLadderFirstMatchPixelsAccepted']and
  parent['completeObservedNativeSelectionNamesAudioAccepted']and parent['actualCurrentRAMStatePixelQualificationMethods']>=40,
  'Actual complete current four-context UI/displayed pixels/paired native names audio and effective faults accepted')
 pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
 need(all(sha(p)==h for p,h in pins.items()),'All executed current/source/evidence/public bytes stable before compaction')
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',"Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"],capture_output=True,text=True)
 need(census.returncode==0,'Actual native process census');live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 need(not live,'No native writer remains active during retained trace compaction')
 measure=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
 measure.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong));measure.restype=ctypes.c_ulong
 def allocated(p):
  high=ctypes.c_ulong();ctypes.set_last_error(0);low=measure(str(p),ctypes.byref(high))
  need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual retained NTFS allocated bytes');return(high.value<<32)|low
 files=[];rows=[];native_runs=[]
 for name in BASES:
  base=(ROOT/name).resolve(strict=True);need(base.parent==ROOT.resolve()and not base.is_symlink(),'Exact inspected capture tree inside workspace')
  for folder in base.iterdir():
   need(folder.is_dir()and not folder.is_symlink(),'Actual known capture leaf')
   native_runs.append((str(folder),json.loads((folder/'process.json').read_text())['pid']))
   for p in folder.rglob('*'):
    need(not p.is_symlink(),'No linked retained evidence target')
    if p.is_file():
     need(p.suffix.lower()not in('.bin','.png','.wav','.rgb'),'All guest/display/PCM remained only in RAM');files.append(p)
   path=folder/'run.log';before=allocated(path);digest=sha(path)
   need(str(path)in pins and pins[str(path)]==digest,'Exact immutable terminal native trace pin')
   operation=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(path)],capture_output=True,text=True)
   need(operation.returncode==0 and sha(path)==digest,'Lossless actual trace compression preserves every native record')
   rows.append(dict(path=str(path),logicalBytes=path.stat().st_size,beforeAllocatedBytes=before,afterAllocatedBytes=allocated(path),sha256=digest))
 need(len(native_runs)==23 and len(set(native_runs))==23 and len(rows)==23,
  'All actual fresh capture leaves/process records retained; Windows PID reuse is not mistaken for one boot')
 need(all(sha(p)==h for p,h in pins.items()),'All authoritative guest/source/capture/public bytes unchanged after compaction')
 pins[str(Path(__file__).resolve())]=sha(__file__)
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  remaining=parent['remaining'],parentAdditiveJournal=str(PARENT),cases=parent['cases'],
  previousGoalTurnClassification=parent['previousGoalTurnClassification'],
  thisGoalTurnClassification=parent['thisGoalTurnClassification']+'; every retained text trace losslessly compacted and actual on-disk allocation verified',
  actualCurrentUIStatePixelFaultMethods=parent['actualCurrentRAMStatePixelQualificationMethods'],
  actualCurrentSelectionAudioFaultsRejected=len(parent['actualOriginalSelectionAudioFaultsRejected']),
  completeObservedNativeSelectionNamesAudioAccepted=True,currentBothSlotSelectionLadderFirstMatchPixelsAccepted=True,
  retainedActualNativeBoots=23,retainedTextTraceCount=23,traceCompaction=rows,
  currentTurnRetainedEvidenceLogicalBytes=sum(p.stat().st_size for p in files),
  currentTurnRetainedEvidenceAllocatedBytes=sum(allocated(p)for p in files),
  additionalAllocatedBytesReclaimed=sum(r['beforeAllocatedBytes']-r['afterAllocatedBytes']for r in rows),
  rawGuestRGBPCMOrWAVFilesWritten=0,nativeProcessCensus=live,noNativeProcessStillLive=True,
  newBuilds=0,newDeletedFiles=0,sourceCurrentBuildROMPublicCMDZIPPreserved=True,
  publicPlayableChanged=False,refreshedReleaseZIP=False,allAudioContextsAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
  nextAction=parent['nextAction'])

if __name__=='__main__':
 need(not OUT.exists(),'Fresh additive current native UI/audio storage checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','cases','remaining','traceCompaction')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
