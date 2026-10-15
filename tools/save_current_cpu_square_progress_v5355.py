"""Additive current CPU Square/earned-round checkpoint, entire goal remains active."""
import ctypes,datetime,json,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import save_current_cpu_audio_progress_v5326 as scope
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5340_current_cpu_kano_choke_progress/progress.json'
PROOF=ROOT/'audit_v5354_current_cpu_sonya_square_shadow_checked/report.json'
OUT=ROOT/'audit_v5356_current_cpu_square_progress'
def run():
 current.expected()
 parent=json.loads(PARENT.read_text());report=json.loads(PROOF.read_text())
 need(parent['passed']and parent['remaining']==scope.REMAINING and parent['goalStatus']=='active','Whole original five unfinished groups retained')
 need(report['passed']and report['fullNativeSquareHitPhaseBodyShadowAccepted']and report['whole1800FieldNativeMatchStateHealthAccepted']and
  not report['currentWholeSceneEraseAccepted']and not report['fullPortAcceptance'],'Actual finite phase/body/shadow and whole native state/HP without erase/full-port promotion')
 pins={str(p):sha(p)for p in(PARENT,PROOF,Path(__file__))}
 for table in(parent['newInputHashes'],report['inputHashes']):
  for p,h in table.items():need(sha(p)==h,'All authoritative input/evidence pins unchanged: '+p);pins[p]=h
 # The independent graphics interleaver uses the earlier native inventory.
 # Bind it to the entire current compiled ROM lane declaration, not a sampled sprite.
 rel='input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
 old=ROOT/'diagnostic_v2753_native_friendship_palette'/rel
 new=ROOT/current.NAME/rel
 def declaration(p):return p.read_text().split('ROM_START( mk2ks )',1)[1].split('ROM_END',1)[0].split('ROM_REGION( 0x2000000, "gfxrom", ROMREGION_ERASE00 )',1)[1]
 need(declaration(old)==declaration(new),'Entire source-bound graphics ROM lane declaration unchanged')
 for p in(old,new):pins[str(p)]=sha(p)
 need(len(report['actualSemanticFaultsRejected'])==11 and len(report['actualPhysicalFaultsRejected'])==3,'All14 real observation corruptions rejected')
 folders=[ROOT/'audit_v5345_current_cpu_sonya_square_human_kano',ROOT/'audit_v5351_current_cpu_sonya_square_human_kano']
 captures=[];files=[]
 for folder in folders:
  process=json.loads((folder/'process.json').read_text());captures.append(dict(folder=str(folder),pid=process['pid'],command=process['command']))
  need(not any(p.suffix.lower()in('.bin','.png','.wav')for p in folder.rglob('*')if p.is_file()),'No raw media or ROM buffers persisted')
  for p in folder.rglob('*'):
   if p.is_file():files.append(p);pins[str(p)]=sha(p)
 # Compress only two exact disposable trace logs. File bytes and all hashes stay identical.
 compressed=[]
 for folder in folders:
  path=(folder/'run.log').resolve();need(path.is_relative_to(ROOT.resolve())and path.parent==folder.resolve(),'Exact in-workspace trace target')
  before=sha(path)
  command=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(path)],capture_output=True,text=True)
  need(command.returncode==0 and sha(path)==before,'Trace compression preserves exact accepted evidence bytes');compressed.append(str(path))
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',"Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"],capture_output=True,text=True)
 need(census.returncode==0,'Actual native process census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 for p in live:need(not any(p['ProcessId']==c['pid']for c in captures),'Both actual native processes terminal')
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);measure=kernel.GetCompressedFileSizeW
 measure.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong));measure.restype=ctypes.c_ulong
 allocated=0
 for path in files:
  high=ctypes.c_ulong();ctypes.set_last_error(0);low=measure(str(path),ctypes.byref(high))
  need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual new retained trace allocation');allocated+=(high.value<<32)|low
 need(all(sha(p)==h for p,h in pins.items()),'All evidence/public pins stable after compression')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=scope.REMAINING,
  parentAdditiveJournal=str(PARENT),previousGoalTurnClassification='no progress: acknowledgment; polled existing live50459 to actual terminal0',
  thisGoalTurnClassification='progress: two real current natural CPU Square runs; retained first actual observer-imposed normal KO abort, corrected observation only, second entire original1800-field native driver finished. Source-bound Square contact/body/shadows and whole native health/state/earned KO/reset now independently accepted.',
  currentCPUReport=str(PROOF),phase=report['phase'],wholeNativeHealthLedger=report['health'],wholeNativeStateLedger=report['stateLedger'],
  finiteNativeBodyShadowFields=report['finiteBodyShadowWindow'],nativeShadowCopies=report['case']['actualSourceBoundShadowCopies'],
  actualNegativeTestsRejected=14,entireCompiledGraphicsLaneInventoryUnchanged=True,
  preservedObserverFailure='audit_v5346_current_cpu_sonya_square_observed/report.json',
  preservedPreLaunchHostFailures=['audit_v5343_current_cpu_sonya_square_observed/report.json','audit_v5349_current_cpu_sonya_square_observed/report.json'],
  actualNativeBootsThisContinuation=2,successfulOriginalCPUExitFrame=3623,actualEarnedKOFrame=3021,actualOriginalRoundResetFrame=3208,
  captures=captures,nativeProcessCensus=live,noCapturedNativeProcessStillLive=True,
  boundedRAMPreviewInspected=True,previewScope='Selection art cleared before combat and own bodies/floor shadows present. Bounded automatic8-tile sheet did not include Square poses; exact finite native body/shadow source replay covers those phases, not independent artistic/whole-raster acceptance.',
  newRetainedTraceLogicalBytes=sum(p.stat().st_size for p in files),newRetainedTraceAllocatedBytes=allocated,
  exactTraceLogsLZXCompressed=compressed,newBuilds=0,newDeletedFiles=0,rawGuestGFXRGBPCMOrWAVFilesWritten=0,
  publicPlayableChanged=False,refreshedReleaseZIP=False,currentWholeSceneEraseAccepted=False,
  fullArtAcceptance=False,allCPUContextsArenasKOOverlapArtAudioAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
  nextAction='Current CPU Square full native continuous scene/erase RAM proof and owned contact DCS audio; extend source-bound KO/round-transition body/shadow cleanup and native floor grounding to other naturally reached arenas. Preserve all five original remaining groups; no release promotion until combined final regression.')
if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable additive journal')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','captures','remaining','wholeNativeHealthLedger','phase')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
