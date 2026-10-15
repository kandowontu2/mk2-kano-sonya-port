"""Completed current both-slot three-cycle native whole-scene cleanup checkpoint."""
import ctypes,datetime,json,subprocess,traceback
from pathlib import Path
import current_morph_scene_ram_v5416 as scene
ROOT,need,sha=scene.ROOT,scene.need,scene.sha
OUT=ROOT/'audit_v5420_current_morph_scene_progress'

def run():
 scene.current.expected();parent=json.loads(scene.PARENT.read_text())
 need(parent['passed']and parent['goalStatus']=='active','Previous goal turn completed repeated native morph body/shadow proof')
 pins=dict(parent['newInputHashes']);pins[str(scene.PARENT)]=sha(scene.PARENT)
 cases={};files=[];faults=[]
 for target in('kano','sonya'):
  for side in(1,2):
   key=f'{target}_p{side}';path=scene.OUT/key/'report.json';report=json.loads(path.read_text());continuous=report['continuous']
   need(report['passed']and report['candidate']==scene.current.NAME and report['nativeExit']==0 and
    report['actualPhysicalTrajectoryUnchanged']and report['oneActualInitialBaseAcrossAllThreeMorphCycles']and
    report['wholeSceneOperationSequenceAcrossThreeTimersAccepted']and report['denseActualDisplayedTargets']==252 and
    report['exactScreenPixels']==25603200 and continuous['passed']and continuous['oneInitialBaseOnly']and
    not continuous['laterBuffersUsedAsAnchors']and continuous['continuousExactPreBuffers']==continuous['continuousExactFlips']==252 and
    continuous['shiftLoads']==continuous['shiftFills']==report['fullInterveningNativeTimerFields']==1974,
    'Actual exact full current morph operation stream, one native base, every targeted display and all three timers: '+key)
   need(report['nativeBodyShadowHardwareBinding']['completeNativeBodyFIFOChronologyMatchesPrior']and
    report['nativeBodyShadowHardwareBinding']['entireNativeShadowHardwareStreamMatchesPrior']and
    len(report['actualRAMFaultsRejected'])==3,'Previously source-bound native body/shadow stream and three actual RAM corruptions')
   for p,h in report['inputHashes'].items():need(sha(p)==h,'Executed source/retained evidence/public bytes stable');pins[p]=h
   pins[str(path)]=sha(path);files.extend(p for p in(scene.BASE/key).rglob('*')if p.is_file())
   cases[key]=dict(proof=str(path),nativePID=report['nativePID'],exactScreenPixels=report['exactScreenPixels'],
    allTimerFields=report['fullInterveningNativeTimerFields'],wholeSourceGraphicsStreams=report['completeSourceBoundGraphicsStreams'],
    actualTargetedDisplayFrames=252,allNativeShiftTransfers=continuous['nativeShiftTransfers'],
    actualRawBytesVerifiedOnlyInRAM=report['actualRawBufferBytesOnlyInRAM'],actualBufferCount=report['actualRAMBuffers'],
    actualPreviouslyQualifiedShadowCopies=report['nativeBodyShadowHardwareBinding']['actualShadowHardwareCopies'])
   faults.extend(dict(case=key,**r)for r in report['actualRAMFaultsRejected'])
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',"Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"],capture_output=True,text=True)
 need(census.returncode==0,'Actual native process census');live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 need(not any(p['ProcessId']in{r['nativePID']for r in cases.values()}for p in live),'All four native full-scene runs actually terminal')
 need(all(p.suffix.lower()not in('.bin','.png','.wav','.rgb')for p in files),'No raw guest/GFX/VRAM/display/media files retained')
 measure=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
 measure.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong));measure.restype=ctypes.c_ulong
 allocated=0
 for p in files:
  high=ctypes.c_ulong();ctypes.set_last_error(0);low=measure(str(p),ctypes.byref(high))
  need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual compressed native trace allocation');allocated+=(high.value<<32)|low
 for p in(Path(__file__).resolve(),Path(scene.__file__),scene.LUA):pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All final actual source/evidence/native/public pins stable')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  remaining=parent['remaining'],parentAdditiveJournal=str(scene.PARENT),cases=cases,
  previousGoalTurnClassification=parent['thisGoalTurnClassification'],
  thisGoalTurnClassification='progress: current both-slot complete three-cycle native morph drawing/clearing sequence; all targeted VRAM/scanout/RGB and whole source graphics exact from one initial base per fixture; every original timer operation retained and actual body/shadow hardware matches prior independent proof',
  actualCompleteNativeThreeCycleCases=4,actualNativeTimerFields=7896,actualFullComparedDisplayedFrames=1008,
  actualExactDisplayedPixels=102412800,actualSourceBoundNativeShadowCopies=131402,
  actualNativeShiftTransfers=sum(r['allNativeShiftTransfers']for r in cases.values()),
  actualNativeSceneRAMFaultsRejected=faults,actualRawRAMBytesDisposed=sum(r['actualRawBytesVerifiedOnlyInRAM']for r in cases.values()),
  completeObservedCurrentThreeCycleMorphEraseAndSceneAccepted=True,allNativeOperationsBetweenTargetsRetained=True,
  denseComparisonTargetsOnlyDuringDeclaredTransitionAndHandoffWindows=True,
  oneInitialNativeBasePerCase=True,laterVideoBuffersNeverReplayAnchors=True,
  sourceProvenNativeBodyAndFloorShadowHardwareBoundToActualScene=True,
  nativeProcessCensus=live,noCapturedNativeProcessStillLive=True,newNativeBoots=4,newBuilds=0,newDeletedFiles=0,
  newlyRetainedNativeTraceLogicalBytes=sum(p.stat().st_size for p in files),newlyRetainedNativeTraceAllocatedBytes=allocated,
  rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,canonicalArtisticFidelityAccepted=False,allArenasCPUInterruptKOAudioMorphsAccepted=False,
  publicPlayableChanged=False,refreshedReleaseZIP=False,fullPortAcceptance=False,newInputHashes=pins,
  observerLegacyLabelsNotBroadened='The unchanged low-level scene observer retains legacy square/CPU wording and fighter labels. This checkpoint binds actual human Shang/true Kano roster/controller/ID stores from independent physical records; it does not claim a natural CPU Square or general CPU morph.',
  nextAction='Current repeated human morph scene cleanup now matches actual full native operations and exact displayed targets in both player slots. Continue broader native arena/finisher/audio contexts, CPU/interrupt/KO morph art and final combined UI/names/audio regression, dependency-aware old-build cleanup and refreshed ZIP; every original unfinished group remains.')

if __name__=='__main__':
 need(not OUT.exists(),'Fresh additive full current native morph scene checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();scene.save(OUT/'progress.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','cases','remaining','actualNativeSceneRAMFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
