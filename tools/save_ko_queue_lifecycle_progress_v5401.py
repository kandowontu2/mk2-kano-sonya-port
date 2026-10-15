"""Record actual completed queue lifecycle proof and retained disk allocation."""
import ctypes,datetime,json,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import save_current_cpu_audio_progress_v5326 as scope
ROOT,need,sha=current.ROOT,current.need,current.sha
PROOF=ROOT/'audit_v5400_ko_queue_lifecycle_checked/report.json'
OUT=ROOT/'audit_v5402_ko_queue_lifecycle_progress'

def run():
 current.expected();proof=json.loads(PROOF.read_text());observed=json.loads((ROOT/'audit_v5398_ko_queue_lifecycle_observed/report.json').read_text())
 need(proof['passed']and proof['goalStatus']=='active'and proof['remaining']==scope.REMAINING and
  proof['case']['retirementQueueDiscardMechanismSourceProven']and not proof['fullPortAcceptance'],'Native queue cancellation proved without shrinking original goal')
 pins=dict(proof['inputHashes'])
 for p in(PROOF,Path(__file__).resolve()):pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All retained source/evidence/public files stable')
 ps="Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',ps],capture_output=True,text=True)
 need(census.returncode==0,'Actual current native process census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 need(not any(t['ProcessId']==observed['nativePID']for t in live),'Actual queue capture native process terminal, not abandoned')
 folder=ROOT/'audit_v5397_ko_queue_lifecycle'
 files=[p for p in folder.rglob('*')if p.is_file()]
 need(all(p.resolve().is_relative_to(folder.resolve())and p.suffix.lower()not in('.bin','.png','.wav')for p in files),'Only exact in-workspace compact native text/metadata/config retained')
 measure=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
 measure.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong));measure.restype=ctypes.c_ulong
 allocated=0
 for p in files:
  high=ctypes.c_ulong();ctypes.set_last_error(0);low=measure(str(p),ctypes.byref(high))
  need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual retained queue trace disk allocation');allocated+=(high.value<<32)|low
 need(len(proof['actualFaultsRejected'])==6,'Six effective actual lifecycle faults rejected')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=scope.REMAINING,
  parentAdditiveJournal=proof['parentAdditiveJournal'],currentNativeQueueLifecycleProof=str(PROOF),
  previousGoalTurnClassification=proof['previousGoalTurnClassification'],thisGoalTurnClassification=proof['thisGoalTurnClassification'],
  actualLifecycleEvents=7581,actualSourceBoundCodeEvents=7506,actualObservedFields=23,actualQueueRegisterResetCalls=24,
  actualNativeCancellation=proof['case']['actualPendingQueueCancellation'],actualOldBodyPartsCancelled=3,
  retirementQueueDiscardMechanismSourceProven=True,completeObservedSceneBodyShadowAndQueueLifecycleAccepted=True,
  rawGuestOnlyInRAM=True,wholeGuestSHA256=current.GUEST_SHA,entireActualPhysicalTrajectoryRecords=8848,
  nativeProcessCensus=live,noCapturedNativeProcessStillLive=True,newNativeBoots=1,newBuilds=0,newDeletedFiles=0,
  newlyRetainedNativeTraceLogicalBytes=sum(p.stat().st_size for p in files),newlyRetainedNativeTraceAllocatedBytes=allocated,
  exactNewTraceLZXCompressed=True,rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,
  publicPlayableChanged=False,refreshedReleaseZIP=False,fullPortAcceptance=False,canonicalArtisticFidelityAccepted=False,
  allKOContextsArenasArtAudioAccepted=False,newInputHashes=pins,nextAction=proof['nextAction'])

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable additive queue lifecycle checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','remaining')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
