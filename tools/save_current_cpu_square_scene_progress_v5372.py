"""Additive source-bound scene/erase checkpoint; preserve the entire active goal."""
import ctypes,datetime,json,re,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import save_current_cpu_audio_progress_v5326 as scope
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5356_current_cpu_square_progress/progress.json'
PROOF=ROOT/'audit_v5371_current_cpu_square_scene_ram_checked/report.json'
OUT=ROOT/'audit_v5373_current_cpu_square_scene_progress'

def run():
 current.expected()
 parent=json.loads(PARENT.read_text());report=json.loads(PROOF.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and parent['remaining']==scope.REMAINING,'Original five unfinished groups unchanged')
 need(report['passed']and report['candidate']==current.NAME and report['wholeNativeSceneEraseAndScanoutAccepted']and
  report['originalSnapshotRendererRAMTransport']and report['screenWorkingBitmapNotUsed']and
  report['completeOriginalNativeHUDGoldFaceAndBlackShadowSourceBound']and not report['fullPortAcceptance'],'Complete source-bound original snapshot renderer and whole scene replay, no broad promotion')
 continuous=report['continuous']
 need(continuous['passed']and continuous['oneInitialBaseOnly']and not continuous['laterBuffersUsedAsAnchors']and
  continuous['continuousExactFlips']==69 and len(report['fullRAMRGBBindings'])==69 and report['exactScreenPixels']==7010400 and
  [r['frame']for r in report['fullRAMRGBBindings']]==list(range(2279,2348)),'Every actual native startup/contact/fall/landing/recovery full scanout exact')
 need(len(report['actualRAMFaultsRejected'])==3 and report['originalWholePhysicalTrajectoryUnchanged']and report['actualNativeTerminal']==0,'Three effective actual corruption tests rejected and actual driver terminal0')
 pins={str(p):sha(p)for p in(PARENT,PROOF,Path(__file__),Path(scope.__file__))}
 for table in(parent['newInputHashes'],report['inputHashes']):
  for p,h in table.items():need(sha(p)==h,'Retained authoritative source/evidence unchanged: '+p);pins[p]=h
 # Earlier uncheckpointed attempts remain explicit failures, not erased history.
 failures=[]
 for version in(5359,5362,5365,5368):
  path=ROOT/f'audit_v{version}_current_cpu_square_scene_ram_checked/report.json'
  failure=json.loads(path.read_text());need(not failure['passed'],'Retain actual unsuccessful checker/API attempt')
  failures.append(dict(path=str(path),error=failure['error']));pins[str(path)]=sha(path)
 folders=[ROOT/f'audit_v{v}_current_cpu_square_scene_ram'for v in(5358,5361,5364,5367,5370)]
 captures=[];files=[];compressed=[]
 for folder in folders:
  process=json.loads((folder/'process.json').read_text())
  captures.append(dict(folder=str(folder),pid=process['pid'],command=process['command']))
  need(not any(p.suffix.lower()in('.bin','.png','.wav')for p in folder.rglob('*')if p.is_file()),'No persistent raw media or ROM buffers')
  log=(folder/'run.log').resolve();need(log.is_relative_to(ROOT.resolve())and log.parent==folder.resolve(),'Validated exact in-workspace trace path')
  before=sha(log)
  compressed_result=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(log)],capture_output=True,text=True)
  need(compressed_result.returncode==0 and sha(log)==before,'Actual trace LZX compression preserves every byte and evidence pin');compressed.append(str(log))
  for p in folder.rglob('*'):
   if p.is_file():files.append(p);pins[str(p)]=sha(p)
 good=folders[-1];meta=json.loads((good/'result.json').read_text());log=(good/'run.log').read_text()
 need(meta['exit_code']==0 and meta['candidate']==current.NAME and meta['rawMediaFilesWritten']==0 and
  (good/'stderr.log').read_text()==''and not re.search(r'hex=|LUA ERROR|stack traceback|Fatal error',log),'Actual warning-free native terminal and no raw data persisted')
 diagnostics=json.loads((good/'snapshot_binding_diagnostics.json').read_text())
 need(len(diagnostics)==70 and all(r['mismatchedPixels']==0 and r['actualRGBSHA256']==r['expectedRGBSHA256']for r in diagnostics[:69])and
  diagnostics[-1]['mismatchedPixels']==1,'All69 exact full fields plus actual one-pixel fault rejection')
 ps="Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',ps],capture_output=True,text=True)
 need(census.returncode==0,'Authoritative current native process census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 need(not any(p['ProcessId']==c['pid']for p in live for c in captures),'All actual captured native processes terminal')
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
  ROOT/'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E'}
 for p,h in public.items():need(sha(p)==h,'Public executable/launcher/release unchanged');pins[str(p)]=h
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);measure=kernel.GetCompressedFileSizeW
 measure.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong));measure.restype=ctypes.c_ulong
 allocated=0
 for p in files:
  high=ctypes.c_ulong();ctypes.set_last_error(0);low=measure(str(p),ctypes.byref(high))
  need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual retained trace allocation');allocated+=(high.value<<32)|low
 need(all(sha(p)==h for p,h in pins.items()),'All final authoritative pins stable')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=scope.REMAINING,
  parentAdditiveJournal=str(PARENT),previousGoalTurnClassification='no progress: acknowledgment; revalidated current state and actual process census before next available scene capture',
  thisGoalTurnClassification='progress: traced working-bitmap versus displayed-texture mismatch to unchanged native MAME screen/video implementation; preserved real API guard failure; fresh original physical CPU Square trajectory and complete one-base native erase plus all69 original snapshot-renderer RAM RGB fields now accepted without tolerance or frame substitution.',
  currentSceneReport=str(PROOF),currentWholeSceneEraseAndNativeRGBWindowAccepted=True,sceneWindow=[2279,2347],
  exactNativeScreenPixels=report['exactScreenPixels'],continuousExactPreBuffers=continuous['continuousExactPreBuffers'],
  continuousExactFlips=continuous['continuousExactFlips'],nativeShiftLoads=continuous['shiftLoads'],nativeShiftFills=continuous['shiftFills'],
  nativeShiftTransfers=continuous['nativeShiftTransfers'],directShiftStores=continuous['directShiftStores'],oneInitialBaseOnly=True,
  fullOriginalSnapshotRendererNotWorkingBitmap=True,fullOriginalHUDGoldFaceAndBlackShadowSourceBound=True,
  effectiveActualRAMCorruptionsRejected=3,phase=report['phase'],wholeNativeHealthLedger=report['wholeNativeHealth'],wholeNativeStateLedger=report['wholeNativeState'],
  currentContinuationActualNativeBoots=2,earlierUncheckpointedActualSceneBoots=3,preservedFailures=failures,captures=captures,
  actualSuccessfulNativeExitFrame=3623,boundedRAMPreviewInspected=True,
  previewScope='Eight real full Square/contact/drop/landing/recovery fields; owned bodies and floor shadows present, selection portraits absent. No independent all-pose artistic, other-arena, KO/overlap or audio acceptance inferred.',
  nativeProcessCensus=live,noCapturedNativeProcessStillLive=True,newRetainedTraceLogicalBytes=sum(p.stat().st_size for p in files),
  newRetainedTraceAllocatedBytes=allocated,exactTraceLogsLZXCompressed=compressed,newBuilds=0,newDeletedFiles=0,
  rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,publicPlayableChanged=False,refreshedReleaseZIP=False,
  wholeArtisticFidelityAccepted=False,allCPUContextsArenasKOOverlapArtAudioAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
  nextAction='Full actual native CPU Square owned launch/contact sound with paired RAM-only PCM; broaden native body/shadow/grounding and whole-scene cleanup to naturally reached arenas and KO/overlap, and retain every other unfinished group. No public promotion until combined final regression and dependency-aware cleanup.')

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable additive checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','captures','remaining','phase','wholeNativeHealthLedger','wholeNativeStateLedger')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
