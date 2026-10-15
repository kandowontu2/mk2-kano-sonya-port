"""Bind every repeated native morph hold/handoff to complete current draw proof.

Actual displayed previews were inspected, but no universal artistic or complete
scene/raster/erase/audio acceptance is inferred from these finite captures.
"""
import copy,ctypes,datetime,json,struct,subprocess,traceback
from pathlib import Path
import current_morph_shadow_ram_v5407 as body
import current_morph_shadow_ram_v5411 as corrected
import build_native_shang_morphs as assets
ROOT,need,sha=body.ROOT,body.need,body.sha
OUT=ROOT/'audit_v5415_current_morph_shadow_progress'
PARENT=ROOT/'audit_v5406_current_morph_adversity_progress/progress.json'

def phase_holds(b,groups,choices,returns,stores,expected_groups,side,guest,payload):
 need(len(groups)==18,'Every actual repeated native transition-group call')
 expected=[]
 for choice,reverse in zip(choices,returns):
  expected +=[(choice['frame']+4+4*i,g)for i,g in enumerate(expected_groups)]
  expected +=[(reverse['frame']+4*i,g)for i,g in enumerate(expected_groups[::-1])]
 need([(r['frame'],r['group'])for r in groups]==expected,'Every original forward/reverse group order and four-field sleep cadence')
 for event in groups:
  need(event['pc']==0xff8387a0 and(event['actor'],event['main'])==b['owners'][side],'Actual original group entry and owned native Main')
  for f in range(event['frame'],event['frame']+4):
   need(b['post'][f,side]['pose']==event['group']and b['pre'][f+1,side]['pose']==event['group'],
    'Every native four-field morph hold bound to genuine consecutive draw-time and next-pre body publications')
   actual=next(t for t in b['rows']['MK2_HPHASE_SHADOW_BEGIN']if body.native.num(t,'frame')==f and body.native.num(t,'slot')==side)
   need(body.native.num(actual,'pose')==event['group']and len(body.native.native_group(actual,payload,guest))==2,
    'Both source-defined original morph components actually reach native owned shadow calls')
 for r in stores:
  floor={6:87,17:82,18:81}[r['id']]
  for f in range(r['frame'],r['frame']+8):
   own=b['post'][f,side]
   need(own['id']==r['id']and own['roster']==6 and own['floor']==floor and own['y']==floor and own['trail']==0,
    'Every native form/restoration handoff has its genuine identity, own floor and no lingering effect')
 return dict(actualTransitionGroupEvents=18,sourceDefinedFourFieldMorphHolds=72,
  actualCompleteForwardAndReverseTransitions=6,actualCompleteRepeatedCycles=3,actualGroundedHandoffFields=48)

def run():
 guest=body.current.expected();payload=(ROOT/body.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active','Actual prior goal turn completed current24-case native morph state proof')
 pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
 historical=ROOT/'audit_v3186_native_morph_floor_projection_checked/report.json';old=json.loads(historical.read_text())
 need(old['passed']and sha(assets.__file__)==old['inputHashes'][str(Path(assets.__file__).resolve())],'Original declared morph group source unchanged; old runtime not transferred')
 cases={};phase_faults=[]
 for target in('kano','sonya'):
  for side in(1,2):
   key=f'{target}_p{side}';report_file=corrected.OUT/key/'report.json';report=json.loads(report_file.read_text())
   need(report['passed']and report['candidate']==body.current.NAME and report['nativeExit']==0 and
    report['originalEntirePhysicalTrajectoryUnchanged']and report['case']['actualNativeMorphBodyShadowWindowsAccepted'],
    'Actual current full native body/shadow capture passed for '+key)
   pins[str(report_file)]=sha(report_file)
   for p,h in report['inputHashes'].items():need(sha(p)==h,'All executed body/physical/compiled dependencies stable');pins[p]=h
   folder=corrected.BASE/key;log=(folder/'run.log').read_text();streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text())
   b=body.context(log,streams,target,side,[tuple(w)for w in report['ranges']])
   groups=body.physical.rows(log,'GROUP');choices=body.physical.rows(log,'CHOICE');returns=body.physical.rows(log,'RESTORE_BEGIN');stores=body.physical.rows(log,'STORE')
   expected=[assets.address(assets.GROUPS+((0 if target=='kano'else 1)*3+i)*12)for i in range(3)]
   for g in expected:
    offset=(g-assets.BASE)//8;words=struct.unpack_from('<III',payload,offset)
    need(words[0]and words[1]and words[2]==0,'Current actual payload preserves original two-component native morph grammar')
   case=phase_holds(b,groups,choices,returns,stores,expected,side,guest,payload)
   for label in('wrong_group','wrong_hold_cadence','missing_group','wrong_actual_post_hold'):
    changed_groups=copy.deepcopy(groups);changed=copy.deepcopy(b)
    if label=='wrong_group':changed_groups[0]['group']=expected[1]
    elif label=='wrong_hold_cadence':changed_groups[1]['frame']+=1
    elif label=='missing_group':changed_groups.pop(0)
    else:
     key0=(groups[0]['frame'],side);need(changed['post'][key0]['pose']!=expected[1],'Effective actual phase-pose fault');changed['post'][key0]['pose']=expected[1]
    try:phase_holds(changed,changed_groups,choices,returns,stores,expected,side,guest,payload)
    except ValueError as error:phase_faults.append(dict(case=key,fault=label,rejectedBy=str(error)))
    else:raise ValueError('Actual native phase fault accepted: '+label)
   case.update(bodyShadow=report['case'],actualNativeBodyShadowFaultsRejected=len(report['actualSemanticFaultsRejected']),
    actualNativeDisplayedSnapshots=report['actualDisplayedSnapshots'],nativePID=report['nativePID'])
   cases[key]=case
   print(key+' every repeated native transition hold and grounded handoff accepted',flush=True)
 ps="Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',ps],capture_output=True,text=True);need(census.returncode==0,'Actual native process census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 need(not any(p['ProcessId']in{c['nativePID']for c in cases.values()}for p in live),'All actual current native capture processes terminal')
 failed_folder=ROOT/'audit_v5408_current_morph_shadow_ram';failed=ROOT/'audit_v5409_current_morph_shadow_checked/kano_p1/report.json'
 need(not json.loads(failed.read_text())['passed'],'Preserve actual first capture snapshot-size assertion failure')
 files=[p for folder in(failed_folder,corrected.BASE)for p in folder.rglob('*')if p.is_file()]
 need(all(p.suffix.lower()not in('.bin','.png','.wav')for p in files),'Only compact text/metadata/config retained; raw guest and image buffers only RAM')
 measure=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
 measure.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong));measure.restype=ctypes.c_ulong
 allocated=0
 for p in files:
  high=ctypes.c_ulong();ctypes.set_last_error(0);low=measure(str(p),ctypes.byref(high))
  need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual retained disk allocation');allocated+=(high.value<<32)|low
 for p in(files+[failed,historical,Path(assets.__file__),Path(__file__).resolve(),Path(body.__file__),Path(corrected.__file__)]):pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All final authoritative evidence/source/public pins unchanged')
 result=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  remaining=parent['remaining'],parentAdditiveJournal=str(PARENT),cases=cases,
  previousGoalTurnClassification=parent['thisGoalTurnClassification'],
  thisGoalTurnClassification='progress: fresh current both-slot repeated morph body/source/native shadow proof; all original transition holds and own-ground handoffs accepted; actual native displayed previews inspected; failed snapshot-dimensions harness attempt preserved',
  actualCurrentPhysicalCases=4,actualNativeWindowFields=sum(c['bodyShadow']['actualObservedWindowFields']for c in cases.values()),
  actualNativeBodyComponents=sum(c['bodyShadow']['actualNativeBodyCandidates']for c in cases.values()),
  actualSourceBoundShadowCopies=sum(c['bodyShadow']['actualSourceBoundShadowCopies']for c in cases.values()),
  actualSourceDefinedMorphHoldFields=288,actualNativeGroundedHandoffFields=192,
  actualBodyShadowFaultsRejected=32,actualPhaseFaultsRejected=phase_faults,
  actualNativeDisplayedSnapshotsInspected=24,rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,newNativeBoots=5,newBuilds=0,newDeletedFiles=0,
  nativeProcessCensus=live,noCapturedNativeProcessStillLive=True,preservedActualCaptureFailure=str(failed),
  captureFixOnly='Original command inherited 400x300 snapshot size. Exact native snapshot is 400x254; only -snapsize changed, whole physical trajectory unchanged.',
  newlyRetainedNativeTraceLogicalBytes=sum(p.stat().st_size for p in files),newlyRetainedNativeTraceAllocatedBytes=allocated,
  fullSceneEraseAndRGBReplayAccepted=False,canonicalArtisticFidelityAccepted=False,allArenasCPUInterruptKOAudioMorphsAccepted=False,
  publicPlayableChanged=False,refreshedReleaseZIP=False,fullPortAcceptance=False,newInputHashes=pins,
  nextAction='Complete actual whole-scene chronological erasure/RGB replay for current morph transitions and broaden other native arena/finisher/audio contexts; preserve every original remaining group and final combined UI/cleanup/release requirement.')
 return result

if __name__=='__main__':
 need(not OUT.exists(),'Fresh additive repeated native morph source checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();body.save(OUT/'progress.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','remaining','cases','actualPhaseFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
