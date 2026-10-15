"""Additive current native CPU Kano evidence; retain the entire unfinished goal."""
import ctypes,datetime,json,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import save_current_cpu_audio_progress_v5326 as previous
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5338_current_cpu_kano_choke_progress'
PARENT=previous.OUT/'progress.json'

def run():
 current.expected()
 parent=json.loads(PARENT.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and parent['remaining']==previous.REMAINING,'Whole prior unfinished scope remains active')
 pins={str(PARENT):sha(PARENT),str(Path(__file__).resolve()):sha(__file__),str(Path(previous.__file__).resolve()):sha(previous.__file__)}
 for p,h in parent['newInputHashes'].items():need(sha(p)==h,'Prior authoritative pin unchanged: '+p)
 captures=[];reports=[];files=[]
 for human in('kano','sonya'):
  path=ROOT/f'audit_v5336_current_cpu_kano_terminal_health_shadow_human_{human}_checked/report.json'
  report=json.loads(path.read_text());case=report['case'];health=case['state']['wholeNativeHealthHistory']
  need(report['passed']and report['candidate']==current.NAME and report['currentFiniteCPUChokeBodyNativeShadowsAndCleanupVerified']and
       report['entireNativeBothSlotHealthLedgerReplayed']and report['actualColdTrajectoryUnchanged']and
       report['sourceBoundOriginalPreExecutionExitQualified']and not report['fullPortAcceptance'],'Actual finite CPU acceptance without broad promotion')
  need(len(report['actualSemanticFaultsRejected'])==11 and len(report['actualPhysicalFaultsRejected'])==4,'All15 actual corruptions rejected')
  for p,h in report['inputHashes'].items():need(sha(p)==h,'Current full source/evidence pin unchanged: '+p);pins[p]=h
  pins[str(path)]=sha(path)
  folder=ROOT/f'audit_v5329_current_cpu_kano_choke_human_{human}'
  process=json.loads((folder/'process.json').read_text());meta=json.loads((folder/'result.json').read_text())
  need(meta['exit_code']==0 and (folder/'stderr.log').read_text()==''and not any(p.suffix.lower()in('.bin','.png','.wav')for p in folder.rglob('*')if p.is_file()),'Actual native terminal0 and no raw media files')
  captures.append(dict(folder=str(folder),pid=process['pid'],command=process['command'],nativeExit=0))
  reports.append(dict(human=human,actualCPU=17,report=str(path),damage=case['state']['originalContract']['damage'],
   nativeHealthStores=health['nativeHealthStores'],completeActorFields=case['actualContiguousActorFields'],
   fullNativeBodyParts=case['actualPublishedBodyParts'],nativeShadowCopies=case['actualSourceBoundShadowCopies'],
   terminalPreCallback=health['last'],lastActualDraw=health['renderedLast'],actualFaultsRejected=15))
  files.extend(p for p in folder.rglob('*')if p.is_file())
 ps="Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',ps],capture_output=True,text=True)
 need(census.returncode==0,'Authoritative native process census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 for process in live:need(not any(process['ProcessId']==c['pid']for c in captures),'Captured native PIDs actually terminal')
 public={
  ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
  ROOT/'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'}
 for p,h in public.items():need(sha(p)==h,'Public release unchanged');pins[str(p)]=h
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);measure=kernel.GetCompressedFileSizeW
 measure.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong));measure.restype=ctypes.c_ulong
 allocated=0
 for p in files:
  high=ctypes.c_ulong();ctypes.set_last_error(0);low=measure(str(p),ctypes.byref(high))
  need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual allocated trace bytes');allocated+=(high.value<<32)|low
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),parentAdditiveJournal=str(PARENT),
  goalStatus='active',remaining=previous.REMAINING,previousGoalTurnClassification='no progress: acknowledgment only; existing live checker50459 re-polled to actual terminal0 before further work',
  thisGoalTurnClassification='progress: actual current cross CPU checker reached terminal0; both natural CPU Kano mirror/cross captures now pass original complete physical phase/body/shadow gates and the expanded whole native health ledger; all30 actual corruption tests rejected; evidence and public bytes revalidated.',
  actualColdBootsCovered=2,newColdBootsThisContinuation=0,captures=captures,reports=reports,
  nativeProcessCensus=live,noCapturedNativeProcessStillLive=True,newTraceLogicalBytes=sum(p.stat().st_size for p in files),newTraceAllocatedBytes=allocated,
  visualObservation='Both bounded8-tile RAM previews inspected: dedicated selection icons/poses clear before combat; native bodies and underfoot shadows present. Not an all-screen/art acceptance claim.',
  preservedCheckerFailures=['audit_v5332_current_cpu_kano_choke_human_kano_checked/report.json','audit_v5334_current_cpu_kano_health_shadow_human_kano_checked/report.json'],
  scope='Actual Prison-stage CPU Kano choke and first ordinary follow-up only. Whole damage history includes earlier ordinary attacks. One actual pre-execution exit callback is source-qualified; no invented draw.',
  newBuilds=0,newDeletedFiles=0,rawGuestGFXRGBPCMOrWAVFilesWritten=0,publicPlayableChanged=False,refreshedReleaseZIP=False,
  allCPUContextsArenasKOOverlapArtAudioAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
  nextAction='Current natural CPU Sonya Square full body/shadow/erase and phase/push replay. Continue all five original remaining groups; preserve release until final combined regression.')

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable additive journal')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','captures','remaining')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
