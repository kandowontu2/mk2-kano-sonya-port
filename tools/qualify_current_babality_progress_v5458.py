"""Current22 native Babality matrix, original common code and compact text storage.

Retain executed failed preflights/captures; no guest/raster/audio media restore.
Unchanged source tables alone are not runtime acceptance. All5 scope groups stay.
"""
import ctypes,datetime,json,re,struct,subprocess,traceback
from pathlib import Path
import current_babality_ram_v5455 as captured
ROOT,need,sha=captured.ROOT,captured.need,captured.sha
PARENT=ROOT/'audit_v5457_current_babality_progress/progress.json'
OUT=ROOT/'audit_v5459_current_babality_qualified_progress'
BASES=('audit_v5450_current_babality_ram','audit_v5453_current_babality_ram','audit_v5456_current_babality_ram')

def source_contract(guest):
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();expected=bytearray(original)
 off=captured.off
 struct.pack_into('<I',expected,off(0xff87e250),0xff800000+0xf97a0*8)
 struct.pack_into('<I',expected,off(0xff87eb30),captured.model.v.TABLE)
 ranges=((0xff87e120,0xff87f020),(0xff804040,0xff8046b0),(0xff816820,0xff816930))
 for first,last in ranges:
  need(guest[off(first):off(last)]==expected[off(first):off(last)],
       'Original native common gate/choreography, camera/flip/ADDXY FIFO/DMA and display-flip code; only2 typed Babality table relocations')
 return [dict(first=f'{first:08X}',last=f'{last:08X}',bytes=off(last)-off(first))for first,last in ranges]

def run():
 guest=captured.current.expected();parent=json.loads(PARENT.read_text())
 need(parent['passed']and parent['currentBabalityMatrixAccepted']and parent['goalStatus']=='active','Actual complete current22-context matrix accepted')
 pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
 need(all(sha(p)==h for p,h in pins.items()),'All current/source/public and executed evidence pins stable')
 ranges=source_contract(guest);source_faults=[]
 for label,address in(('native gate opcode',0xff87e120),('native performer consumer',0xff87e250),
   ('native victim consumer',0xff87eb30),('native camera SUBXY',0xff804150),
   ('native display ADDXY',0xff804400),('native display-flip opcode',0xff8168d0)):
  changed=bytearray(guest);changed[captured.off(address)]^=1
  try:source_contract(changed)
  except ValueError as error:source_faults.append(dict(label=label,address=f'{address:08X}',rejectedBy=str(error)))
  else:raise ValueError('Actual source contract counterexample accepted: '+label)
 cases=[]
 for spec in captured.SPECS:
  winner,victim,side,command=spec;key=f'{winner}_vs_{victim}_p{side}_{command}'
  folder=captured.BASE/key;case=json.loads((folder/'result.json').read_text())
  need(case['passed']and case['candidate']==captured.current.NAME and case['nativeExit']==0 and
       (case['winner'],case['victim'],case['side'],case['command'])==spec,'Exact actual current physical fixture result')
  need(case['inputHashes']==json.loads((folder/'input_hashes_before.json').read_text())and
       all(pins.get(p)==h for p,h in case['inputHashes'].items()),'Original actual execution inputs bound to accepted matrix')
  log=(folder/'run.log').read_text();rows=captured.model.v.records(log)
  captured.runtime(rows,spec,parent['independentOriginalROMBabyReference'])
  need(len(case['actualDisplayHeaders'])==94 and len(case['nativeProjectionAndScanout'])==3,
       'Complete94 displayed targets;3 entire native scanouts independently pixel-exact')
  need(sum(r['pixels']for r in case['nativeProjectionAndScanout'])==304800 and
       len(case['nativeProjectionAndScanout'][0]['effectiveActualScanoutRAMFaults'])==3,'Effective original full scanout RAM fault qualification')
  expected_faults=14 if command=='positive'else 5
  need(len(case['effectiveActualRecordAndRAMPixelFaults'])==expected_faults,'Effective same-path original native record/pixel qualification')
  cases.append({k:case[k]for k in('winner','victim','side','command','nativePID','nativeExit','nativeResult',
    'originalBabyArtPaletteFloorChecks','nativeProjectionAndScanout','effectiveActualRecordAndRAMPixelFaults')})
 first=captured.BASE/'kano_vs_sonya_p1_positive';canonical=(first/'run.log').read_text()
 physical=lambda log:[line for line in log.splitlines()if line.startswith('MK2_NATIVE_BABY_')]
 pictures=lambda log:[line for line in log.splitlines()if line.startswith('MK2_BRAM_RGB_DIGEST ')]
 corrected=[]
 for name in BASES[:2]:
  folder=ROOT/name/'kano_vs_sonya_p1_positive';log=(folder/'run.log').read_text()
  need(physical(log)==physical(canonical)and pictures(log)==pictures(canonical),
       'Every original controller record and all94 actual displayed buffer digests identical across corrected observers')
  corrected.append(dict(folder=str(folder),wholeOriginalControllerTrajectoryByteExact=True,whole94ActualDisplayedBuffersSHA256Exact=True,
   acceptedAsDifferentGameplay=False,errorWasObserverCoordinateContract=True))
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',
  "Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"],capture_output=True,text=True)
 need(census.returncode==0,'Actual native process census');live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 need(not live,'Every actual native run terminal before evidence compaction')
 measure=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
 measure.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong));measure.restype=ctypes.c_ulong
 def allocated(p):
  high=ctypes.c_ulong();ctypes.set_last_error(0);low=measure(str(p),ctypes.byref(high))
  need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual NTFS file allocation');return(high.value<<32)|low
 files=[];traces=[];native_runs=[]
 for name in BASES:
  base=(ROOT/name).resolve(strict=True);need(base.parent==ROOT.resolve()and not base.is_symlink(),'Exact scoped retained capture directory')
  for folder in base.iterdir():
   need(folder.is_dir()and not folder.is_symlink(),'Exact unlinked native capture leaf')
   native_runs.append((str(folder),json.loads((folder/'process.json').read_text())['pid']))
   for p in folder.rglob('*'):
    need(not p.is_symlink(),'No linked evidence target')
    if p.is_file():need(p.suffix.lower()not in('.bin','.png','.wav','.rgb'),'No raw guest/display/audio media persisted');files.append(p)
   log=folder/'run.log';before=allocated(log);digest=sha(log)
   cp=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(log)],capture_output=True,text=True)
   need(cp.returncode==0 and sha(log)==digest,'Lossless terminal text trace compression, including failed observer captures')
   traces.append(dict(file=str(log),logicalBytes=log.stat().st_size,beforeAllocatedBytes=before,afterAllocatedBytes=allocated(log),sha256=digest))
 need(len(native_runs)==24 and len(set(native_runs))==24,'All24 actual boot contexts accounted, including2 preserved observer failures')
 for name in('audit_v5448_current_babality_progress','audit_v5451_current_babality_progress','audit_v5454_current_babality_progress'):
  p=ROOT/name/'progress.json';old=json.loads(p.read_text());need(not old['passed'],'Preserved unsuccessful observer/reference contract attempt');pins[str(p)]=sha(p);files.append(p)
 for path in(ROOT/'tools/current_babality_ram_v5449.py',ROOT/'mk2ks_current_babality_ram_v5449.lua',Path(__file__).resolve()):pins[str(path)]=sha(path)
 for p in files:pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All authoritative current/source/public/evidence bytes unchanged after qualification/compaction')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
  parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['previousGoalTurnClassification'],
  thisGoalTurnClassification=parent['thisGoalTurnClassification']+'; original native common code and6 effective source faults; full native camera/flip/display-origin binding; failed observers proven pixel/control identical; all retained text compacted',
  cases=cases,currentBabalityMatrixAccepted=True,sourceQualifiedOriginalNativeCode=ranges,effectiveSourceCounterexamples=source_faults,
  positivePhysicalCases=14,negativePhysicalCases=8,stockVictimControls=2,actualBothSlotTrueMirrorCases=4,
  actualDisplayedFrameCallbacks=2068,exactWholeNativeDisplayedScanoutPixels=6705600,exactOriginalBabyArtSamples=42,
  effectiveActualRuntimeAndRAMPixelFaults=236,effectiveActualScanoutRAMFaults=66,effectiveNativeSourceFaults=6,
  preservedFailedObserverPixelAndControllerBindings=corrected,retainedActualNativeBoots=24,rawGuestRGBPCMOrWAVFilesWritten=0,
  retainedEvidenceLogicalBytes=sum(p.stat().st_size for p in files),retainedEvidenceAllocatedBytes=sum(allocated(p)for p in files),
  additionalAllocatedBytesReclaimed=sum(r['beforeAllocatedBytes']-r['afterAllocatedBytes']for r in traces),traceCompaction=traces,
  nativeProcessCensus=live,noNativeProcessStillLive=True,newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,refreshedReleaseZIP=False,
  allFinisherContextsAccepted=False,allArenasAccepted=False,audioAccepted=False,continuousWholeSceneRasterAccepted=False,
  fullPortAcceptance=False,newInputHashes=pins,nextAction=parent['nextAction'])

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable complete Babality qualification checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();captured.save(OUT/'progress.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','newInputHashes','remaining','traceCompaction')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
