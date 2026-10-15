"""Actual continuous earned-KO/round scene checkpoint; full goal stays active."""
import ctypes,datetime,json,re,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import save_current_cpu_audio_progress_v5326 as scope
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5381_current_cpu_square_audio_progress/progress.json'
PROOF=ROOT/'audit_v5387_current_cpu_ko_round_scene_ram_checked/report.json'
OUT=ROOT/'audit_v5389_current_cpu_ko_round_scene_progress'

def run():
 current.expected();parent=json.loads(PARENT.read_text());report=json.loads(PROOF.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and parent['remaining']==scope.REMAINING,'Preserve original five unfinished groups verbatim')
 need(report['passed']and report['candidate']==current.NAME and report['completeKOToNextRoundNativeSceneEraseAndRGBWindowAccepted']and
  report['everyFrameDoneStateBoundToNextActualNativePreCPUState']and report['originalWholePhysicalTrajectoryUnchanged']and
  report['originalRAMDeltaTransportOnly']and report['transportPreviousBuffersNeverNativeReplayAnchors']and not report['fullPortAcceptance'],
  'Whole actual unassisted KO/rebuild/reveal/next-fight native scene accepted, no broader promotion')
 continuous=report['continuous']
 need(continuous['passed']and continuous['oneInitialBaseOnly']and not continuous['laterBuffersUsedAsAnchors']and
  continuous['continuousExactPreBuffers']==continuous['continuousExactFlips']==340 and
  [r['frame']for r in report['fullRAMRGBBindings']]==list(range(3001,3341))and report['exactScreenPixels']==34544000,
  'Every one-base native pre-pass/display and actual full snapshot-renderer field exact')
 need(report['actualHeldFields']==continuous['continuousExactHeldBuffers']==0 and len(report['actualRAMFaultsRejected'])==3,
  'No held field inferred or accepted without an actual observation; three actual target faults rejected')
 need((report['actualKOFrame'],report['actualNativeRoundResetFrame'],report['nextRoundPreCPUFirstLiveFrame'],report['allModeSceneFields'])==(3021,3208,3306,341),
  'All actual native lifecycle and callback phase boundaries retained')
 pins={str(p):sha(p)for p in(PARENT,PROOF,Path(__file__),Path(scope.__file__))}
 for table in(parent['newInputHashes'],report['inputHashes']):
  for p,h in table.items():need(sha(p)==h,'All retained authoritative input/evidence unchanged: '+p);pins[p]=h
 failure=ROOT/'audit_v5384_current_cpu_ko_round_scene_ram_checked/report.json'
 need(not json.loads(failure.read_text())['passed'],'Preserve actual first recorder failure');pins[str(failure)]=sha(failure)
 folders=[ROOT/f'audit_v{v}_current_cpu_ko_round_scene_ram'for v in(5383,5386)]
 captures=[];files=[];compressed=[];logs=[]
 for folder in folders:
  process=json.loads((folder/'process.json').read_text());text=(folder/'run.log').read_text();logs.append(text)
  rows=[s for s in text.splitlines()if s.startswith('MK2_CPU_PAIR_RESULT ')]
  need(len(rows)==1 and 'frame=3623'in rows[0],'Actual native controller reached original terminal in both attempts')
  need(not any(p.suffix.lower()in('.bin','.png','.wav')for p in folder.rglob('*')if p.is_file())and 'hex='not in text,'No raw native media persisted')
  captures.append(dict(folder=str(folder),pid=process['pid'],command=process['command'],nativeControllerTerminalFrame=3623,successfulObserver=folder==folders[1]))
  path=(folder/'run.log').resolve();need(path.is_relative_to(ROOT.resolve())and path.parent==folder.resolve(),'Exact validated in-workspace trace path')
  before=sha(path);result=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(path)],capture_output=True,text=True)
  need(result.returncode==0 and sha(path)==before,'Trace compression preserves every actual captured byte');compressed.append(str(path))
  for p in folder.rglob('*'):
   if p.is_file():files.append(p);pins[str(p)]=sha(p)
 prefixes=('MK2_CPU_PAIR_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_CPU_CHOICE_','MK2_SQUARE_NATIVE_','MK2_P2CPU_','MK2_SQUARE_BOUNDARY_','MK2_SQUARE_LOCK_')
 select=lambda t:[s for s in t.splitlines()if s.startswith(prefixes)]
 need(select(logs[0])==select(logs[1])and len(select(logs[1]))==8848,'Even first recorder error changed no actual physical/native trajectory record')
 good=folders[-1];meta=json.loads((good/'result.json').read_text())
 need(meta['exit_code']==0 and meta['rawMediaFilesWritten']==0 and (good/'stderr.log').read_text()==''and
  not re.search(r'LUA ERROR|stack traceback|Fatal error',logs[1]),'Actual successful native terminal0 and warning-free complete capture')
 states=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in logs[1].splitlines()if s.startswith('MK2_NAT_CAMPAIGN_FLOOR_STATE ')]
 need(len(states)==341 and {int(s['mode'])for s in states}=={2,5,6,7}and
  next(s for s in states if s['frame']=='3208')['p1']=='00000000'and next(s for s in states if s['frame']=='3208')['p2']=='00000000',
  'Actual original actor retirement/rebuild states retained across every scene field')
 ps="Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',ps],capture_output=True,text=True);need(census.returncode==0,'Authoritative actual native process census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 need(not any(p['ProcessId']==c['pid']for p in live for c in captures),'Both actual captured native processes terminal')
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
  ROOT/'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E'}
 for p,h in public.items():need(sha(p)==h,'Public playable/launcher/release unchanged');pins[str(p)]=h
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);measure=kernel.GetCompressedFileSizeW
 measure.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong));measure.restype=ctypes.c_ulong
 allocated=0
 for p in files:
  high=ctypes.c_ulong();ctypes.set_last_error(0);low=measure(str(p),ctypes.byref(high))
  need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual retained trace allocation');allocated+=(high.value<<32)|low
 need(all(sha(p)==h for p,h in pins.items()),'All final authoritative sources/evidence/public bytes stable')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=scope.REMAINING,
  parentAdditiveJournal=str(PARENT),previousGoalTurnClassification='progress: actual natural CPU Square launch paired RAM waveform, native channel/owner cleanup, entire native inputs/state/HP/commands and eight effective playback corruption tests accepted.',
  thisGoalTurnClassification='progress: actual earned KO3021 through native round rebuild3208/reveal/live3306; preserved initial recorder sandbox failure; fresh exact original physical run now independently passes all340 full displayed fields and one-base native CPU/DMA/shift/pre-pass/flip replay across all four modes. Both actors retire and restart under their real17/18 identities without observer mutation.',
  currentKOToNextRoundSceneReport=str(PROOF),completeKOToNextRoundNativeSceneEraseAndRGBWindowAccepted=True,
  window=[3000,3340],allModeSceneFields=341,actualNativeScreenFields=340,exactNativeScreenPixels=34544000,
  continuousExactPreBuffers=340,continuousExactFlips=340,actualHeldFields=0,heldScanoutContextAccepted=False,
  nativeShiftLoads=continuous['shiftLoads'],nativeShiftFills=continuous['shiftFills'],nativeShiftTransfers=continuous['nativeShiftTransfers'],directShiftStores=continuous['directShiftStores'],
  oneInitialBaseOnly=True,transportDeltaPreviousBuffersNeverNativeReplayAnchors=True,sourceBoundGraphicsStreams=report['completeSourceBoundGraphicsStreams'],
  actualKOFrame=3021,actualBothActorRetirementFrameDone=3208,actualNativeRoundResetFrame=3208,nextRoundPreCPUFirstLiveFrame=3306,
  allFrameDoneStatesBoundToActualNextPreCPUFields=True,wholeNativeHealth=report['wholeNativeHealth'],wholeNativeState=report['wholeNativeState'],
  effectiveActualRAMTargetFaultsRejected=3,entireActualNativeTrajectoryRecords=8848,actualNativeBoots=2,captures=captures,
  preservedExecutedRecorderFailure=str(failure),boundedRAMPreviewInspected=True,
  previewScope='Eight actual KO/winner/retirement/reveal/live fields; own winner name, both old bodies and shadows cleared in blank rebuild field3209, next-round own17/18 sprites and shadows, native Fight text and combat visible. Not independent canonical artistic grounding, all-KO, all-arena or effect/audio fidelity acceptance.',
  nativeProcessCensus=live,noCapturedNativeProcessStillLive=True,newRetainedTraceLogicalBytes=sum(p.stat().st_size for p in files),newRetainedTraceAllocatedBytes=allocated,
  exactTraceLogsLZXCompressed=compressed,rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,newBuilds=0,newDeletedFiles=0,
  publicPlayableChanged=False,refreshedReleaseZIP=False,wholeArtisticFidelityAccepted=False,allKOContextsArenasBodyShadowArtAudioAccepted=False,
  fullPortAcceptance=False,newInputHashes=pins,
  nextAction='Independently bind complete KO/death/reveal/rebuilt-body native source groups, grounding, projection and floor-shadow eligibility/kernel/cleanup across this actual transition, then broader naturally reached arenas and overlap contexts. Preserve every other unfinished group and finish with combined UI/names/audio regression, dependency-aware obsolete-folder cleanup and refreshed ZIP.')

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable additive transition journal')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','captures','remaining','wholeNativeHealth','wholeNativeState')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
