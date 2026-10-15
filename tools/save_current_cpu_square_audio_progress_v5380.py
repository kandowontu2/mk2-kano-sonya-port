"""Additive CPU Square launch-sound evidence; complete user goal remains active."""
import ctypes,datetime,json,re,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import save_current_cpu_audio_progress_v5326 as scope
import run_current_cpu_square_audio_ram_v5374 as original
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5373_current_cpu_square_scene_progress/progress.json'
PROOF=ROOT/'audit_v5379_current_cpu_square_audio_ram_checked/report.json'
OUT=ROOT/'audit_v5381_current_cpu_square_audio_progress'

def run():
 current.expected();parent=json.loads(PARENT.read_text());report=json.loads(PROOF.read_text())
 need(parent['passed']and parent['remaining']==scope.REMAINING and parent['goalStatus']=='active','Whole original unfinished goal scope retained verbatim')
 need(report['passed']and report['candidate']==current.NAME and report['fullCapturedNaturalCPUSquareLaunchPlaybackAndOwnershipAccepted']and
  report['originalEntireNativeCPUHitPhaseAndMatchStateHealthContractRetained']and report['originalWholeAudioGateRetainedWithSourceExactFirstLoadAndTimer']and
  not report['fullNativeContactDCSWaveformAccepted']and not report['fullPortAcceptance'],'Full actual owned launch playback acceptance, not native contact or complete port acceptance')
 need(report['actualPhysicalTrajectoryRecords']==8848 and report['nativeSoundPortWrites']==249 and len(report['actualPlaybackFaultsRejected'])==8 and
  report['correlation']>.999 and .699<report['gain']<.701 and report['cueSamples']==45512,'Entire actual trajectory/native command inventory and complete source waveform plus eight effective fault tests')
 pins={str(p):sha(p)for p in(PARENT,PROOF,Path(__file__),Path(scope.__file__),Path(original.__file__))}
 for table in(parent['newInputHashes'],report['inputHashes']):
  for p,h in table.items():need(sha(p)==h,'Actual authoritative source/evidence unchanged: '+p);pins[p]=h
 failure=ROOT/'audit_v5376_current_cpu_square_audio_ram_checked/report.json'
 need(not json.loads(failure.read_text())['passed'],'Preserve actual wrong bookkeeping-model failure');pins[str(failure)]=sha(failure)
 folders=[ROOT/f'audit_v{v}_current_cpu_square_audio_ram_{suffix}'for v in(5375,5378)for suffix in('samples','nosamples')]
 captures=[];files=[];compressed=[]
 for folder in folders:
  meta=json.loads((folder/'result.json').read_text());process=json.loads((folder/'process.json').read_text())
  need(meta['exit_code']==0 and meta['candidate']==current.NAME and meta['wholeActualGuestComparedInRAM']and
   meta['rawGuestRGBPCMOrWAVFilesWritten']==0 and (folder/'stderr.log').read_text()=='','Actual complete warning-free natural CPU terminal0 and RAM-only capture')
  need(not any(p.suffix.lower()in('.bin','.png','.wav')for p in folder.rglob('*')if p.is_file()),'No raw native media or guest files persisted')
  log=(folder/'run.log').read_text();need(not re.search(r'hex=|LUA ERROR|stack traceback|Fatal error',log),'No encoded media persisted or native observer error')
  rows=original.records(log,'RESULT');need(len(rows)==1 and rows[0]['frame']=='3623','Whole original1800-field native controller reached its own terminal')
  captures.append(dict(folder=str(folder),pid=process['pid'],command=process['command'],nativeExit=meta['exit_code'],
   actualWholeGuestSHA256=current.GUEST_SHA,mixedPCMUpdates=meta['mixedPCMUpdates'],mixedPCMBytesVerifiedInRAM=meta['mixedPCMBytes']))
  path=(folder/'run.log').resolve();need(path.is_relative_to(ROOT.resolve())and path.parent==folder.resolve(),'Exact validated trace path inside intended workspace')
  before=sha(path);result=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(path)],capture_output=True,text=True)
  need(result.returncode==0 and sha(path)==before,'Lossless trace compression preserves all actual evidence bytes');compressed.append(str(path))
  for p in folder.rglob('*'):
   if p.is_file():files.append(p);pins[str(p)]=sha(p)
 good=ROOT/report['case'];baseline=ROOT/report['baseline']
 channels=original.records((good/'run.log').read_text(),'CHANNEL');owners=original.records((good/'run.log').read_text(),'OWNER')
 first=report['phase']['start']+1
 actual_clear=next(int(r['frame'])for r in owners if r['slot']=='2'and int(r['frame'])>=first and r['actor']=='00000000')
 need(actual_clear==report['ownership']['completedFrame']==2331 and
  all(r['actor']==r['main']=='00000000'and r['health']=='0'for r in owners if r['slot']=='2'and int(r['frame'])>=actual_clear),
  'Actual owner clears at observed completed source frame and never resumes through2600')
 need(len(channels)==1604 and len(owners)==802,'Every actual401-field physical voice/owner callback retained')
 ps="Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',ps],capture_output=True,text=True);need(census.returncode==0,'Authoritative actual native process census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 need(not any(p['ProcessId']==c['pid']for p in live for c in captures),'All four actual captures terminal')
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
  ROOT/'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E'}
 for p,h in public.items():need(sha(p)==h,'Public playable/launcher/ZIP unchanged');pins[str(p)]=h
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);measure=kernel.GetCompressedFileSizeW
 measure.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong));measure.restype=ctypes.c_ulong
 allocated=0
 for p in files:
  high=ctypes.c_ulong();ctypes.set_last_error(0);low=measure(str(p),ctypes.byref(high))
  need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual retained trace allocated byte measurement');allocated+=(high.value<<32)|low
 need(all(sha(p)==h for p,h in pins.items()),'All final authoritative evidence/public/source pins stable')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=scope.REMAINING,
  parentAdditiveJournal=str(PARENT),previousGoalTurnClassification='progress: actual complete source-bound69-field CPU Square scene/erase and displayed RGB accepted; source-qualified working-bitmap capture error corrected, real failures retained.',
  thisGoalTurnClassification='progress: four actual current natural CPU Square cold boots (enabled/disabled pairs); preserved first model failure, source-qualified original device bookkeeping and60Hz disabled-owner lifetime; fresh pair complete cue waveform, actual finite owner/channel cleanup, whole native inputs/RNG/phase/health/state/commands and eight effective corruption tests accepted.',
  currentLaunchAudioReport=str(PROOF),actualNativeBoots=4,captures=captures,phase=report['phase'],
  fullCapturedNaturalCPUSquareLaunchPlaybackAndOwnershipAccepted=True,actualCueSourceSamples=45512,actualCPUChannel=12,
  actualCompiledSample=13,mixedPCMUpdatesPerCapture=367,mixedStereoSamplesPerCapture=352320,
  cueCorrelation=report['correlation'],cueGain=report['gain'],actualOnsetSeconds=report['onsetSeconds'],nativeMarkerSeconds=report['markerSeconds'],
  actualCueCompletedFrame=2331,actualOwnerClearedFrame=actual_clear,actualOwnerAndChannelsFollowedThroughFrame=2600,
  fullPhysicalOwnerFields=802,fullPhysicalChannelFields=1604,entireNativeTrajectoryRecords=8848,entireNativeSoundPortWrites=249,
  actualPlaybackCorruptionsRejected=8,preservedExecutedFailure=str(failure),sourceQualifiedFirstLoadSourceNum=0xffffffff,
  disabledOwnerLifetimeBoundToFirstNative60HzTick=True,wholeNativeHealth=report['wholeNativeHealth'],wholeNativeState=report['wholeNativeState'],
  nativeProcessCensus=live,noCapturedNativeProcessStillLive=True,newRetainedTraceLogicalBytes=sum(p.stat().st_size for p in files),
  newRetainedTraceAllocatedBytes=allocated,exactTraceLogsLZXCompressed=compressed,rawGuestRGBPCMOrWAVFilesWritten=0,
  newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,refreshedReleaseZIP=False,fullNativeContactDCSWaveformAccepted=False,
  allCPUContextsArenasKOOverlapArtAudioAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
  nextAction='Broaden native CPU body/shadow/grounding and whole-scene cleanup to naturally reached arenas and KO/overlap; complete native contact/effect/victim sound fidelity and every other unfinished finisher/morph/secret/cinematic/campaign context. Preserve all five remaining groups and finish with combined selection/ladder/names/audio regression, dependency-aware cleanup and refreshed release ZIP.')

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable additive journal')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','captures','remaining','phase','wholeNativeHealth','wholeNativeState')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
