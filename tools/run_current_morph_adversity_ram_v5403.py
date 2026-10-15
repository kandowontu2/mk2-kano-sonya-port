"""Fresh current-build physical morph lifecycle matrix, RAM-only guest transport.

Reuse the immutable full native health/identity/physical-input checker, not its
obsolete executable or disk-capture fixtures. No gameplay or public promotion.
"""
import concurrent.futures,ctypes,datetime,hashlib,json,os,re,struct,subprocess,time,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import verify_morph_adversity_v3235 as old
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=ROOT/'mk2ks_current_morph_adversity_ram_v5403.lua'
BASE=ROOT/'audit_v5404_current_morph_adversity_ram'
OUT=ROOT/'audit_v5405_current_morph_adversity_checked'
JOURNAL=ROOT/'audit_v5406_current_morph_adversity_progress'
PARENT=ROOT/'audit_v5402_ko_queue_lifecycle_progress/progress.json'
CASES=sorted({(t,s,p,'added')for t in('kano','sonya')for s in(1,2)
 for p in('forward','formed','reverse','ko','repeat_morph')}|
 {('kano',s,p,'stock_cage')for s in(1,2)for p in('forward','reverse')})

def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')

def run_case(case,guest):
 target,side,phase,form=case;key=f'{target}_p{side}_{phase}_{form}';folder=BASE/key
 folder.mkdir()
 for name in('cfg','nvram','snap'):(folder/name).mkdir()
 candidate=ROOT/current.NAME
 command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
  '-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none',
  '-nothrottle','-noautoframeskip','-frameskip','0','-str','100','-snapsize','400x300',
  '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),
  '-autoboot_script',str(LUA)]
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_MORPH_CAPTURE_OUT=str(folder),MK2KS_MORPH_ADVERSITY_PHASE=phase,MK2KS_MORPH_ADVERSITY_FORM=form,
  MK2KS_HUMAN_SHANG_SIDE=str(side),MK2KS_HUMAN_SHANG_TARGET=target,MK2KS_HUMAN_SHANG_PROFILE='native')
 captured=None;start=time.time()
 with (folder/'run.log').open('w',encoding='utf-8')as out,(folder/'stderr.log').open('w',encoding='utf-8')as err:
  proc=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
  save(folder/'process.json',dict(pid=proc.pid,command=command,env={k:v for k,v in env.items()if k.startswith('MK2KS_')}))
  print(key+' native PID '+str(proc.pid),flush=True)
  transport_error=None
  for line in proc.stdout:
   if line.startswith('MK2_CURRENT_MORPH_GUEST '):
    try:
     need(captured is None,'Exactly one actual entire guest RAM buffer')
     raw=bytes.fromhex(re.search(r'hex=([0-9a-fA-F]+)',line)[1]);need(raw==guest,'Whole actual initialized guest equals independently reconstructed current source')
     captured=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper());del raw
     out.write('MK2_CURRENT_MORPH_GUEST frame=1 bytes=1048576 sha256='+captured['sha256']+'\n')
    except Exception as error:transport_error=repr(error)
   else:out.write(line)
  code=proc.wait()
 log=(folder/'run.log').read_text();stderr=(folder/'stderr.log').read_text()
 before=sha(folder/'run.log');compressed=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(folder/'run.log')],capture_output=True)
 need(compressed.returncode==0 and sha(folder/'run.log')==before,'Exact native text LZX compressed')
 meta=dict(case=case,candidate=current.NAME,nativePID=proc.pid,nativeExit=code,seconds=time.time()-start,
  guestMemoryProof=captured,transportError=transport_error,assistance='none',cheats=False)
 try:
  need(code==0 and not stderr and captured and not transport_error,'Actual warning-free terminal native run with exact RAM guest')
  need(log.count('MK2_MORPH_GUEST frame=1 bytes=1048576 start=FF800000 stop=100000000 writes=0')==1,'Original full guest observer provenance retained')
  checked=old.verify_log(log,*case);meta.update(passed=True,checked=checked)
 except Exception as error:meta.update(passed=False,error=repr(error),traceback=traceback.format_exc())
 save(folder/'result.json',meta);print(key+' terminal '+str(code)+' checked='+str(meta['passed']),flush=True)
 return key,meta

def health_source(guest,pcs):
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for pc in pcs:
  lo=(pc-128-0xff800000)//8;hi=(pc+128-0xff800000)//8;context=bytearray(original[lo:hi])
  if pc==0xff836700:
   pointer=(0xff836750-0xff800000)//8;table=0xfe100;stock=(0xff8367b0-0xff800000)//8
   need(struct.unpack_from('<I',original,pointer)[0]==0xff8367b0 and struct.unpack_from('<I',guest,pointer)[0]==0xffff0800 and
    guest[table:table+17*4]==original[stock:stock+17*4]and guest[table+17*4:table+19*4]==bytes(8),'Exact original seventeen stock collision callbacks plus two appended native human null rows')
   struct.pack_into('<I',context,pointer-lo,0xffff0800)
  need(guest[lo:hi]==context,'Entire observed native health-write context source-bound unchanged except declared table extension')

def faults(key,meta):
 log=(BASE/key/'run.log').read_text();case=tuple(meta['case']);tests=[]
 # Each fault changes a reached, parsed actual record, never an absent field.
 specs=[('PAIR','floor',lambda v:str(int(v)+1)),('PAIR','state',lambda v:'2'),
  ('CHOICE','id',lambda v:'0'),('RESULT','forms',lambda v:str(int(v)+1)),('HEALTH','after',lambda v:str(int(v)+1))]
 for tag,field,fn in specs:
  lines=log.splitlines();indices=[i for i,line in enumerate(lines)if line.startswith('MK2_HUMAN_SHANG_'+tag+' ')]
  if tag=='PAIR':indices=[i for i in indices if f'slot={case[1]} 'in lines[i]and 'mode=2 'in lines[i]]
  if not indices:continue
  i=indices[0];match=re.search(r'\b'+field+r'=([^\s]+)',lines[i]);need(match is not None,'Fault uses existing reached field')
  old_value=match[1];new_value=fn(old_value);need(new_value!=old_value,'Fault actually changes reached record')
  lines[i]=lines[i][:match.start(1)]+new_value+lines[i][match.end(1):];changed='\n'.join(lines)
  need(changed!=log.strip(),'Effective actual record fault')
  try:old.verify_log(changed,*case)
  except (AssertionError,ValueError,RuntimeError)as error:tests.append(dict(case=key,tag=tag,field=field,rejection=str(error)))
  else:raise AssertionError('Reached '+tag+'/'+field+' fault was accepted')
 need(len(tests)>=4,'Actual case has at least four effective semantic faults rejected')
 return tests

def run():
 guest=current.expected();parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active','Authoritative active parent checkpoint')
 pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
 historical=json.loads((ROOT/'audit_v3236_morph_adversity_checked/report.json').read_text())
 need(historical['passed'],'Original physical lifecycle checker actually qualified')
 for file in(Path(old.__file__),Path(old.human.__file__)):
  need(sha(file)==historical['inputHashes'][str(file.resolve())],'Original qualified checker source unchanged')
 for file in(LUA,Path(__file__).resolve(),Path(current.__file__),Path(old.__file__),Path(old.human.__file__),
  ROOT/'mk2ks_morph_adversity_v3226.lua',ROOT/'mk2ks_morph_adversity_v3215.lua',ROOT/'audit_v3236_morph_adversity_checked/report.json'):
  pins[str(file.resolve())]=sha(file)
 for file in(LUA,ROOT/'mk2ks_morph_adversity_v3226.lua',ROOT/'mk2ks_morph_adversity_v3215.lua'):
  need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(',file.read_text()),'Observer and original controller never mutate guest identity/HP/CPU/RNG/state')
 need(all(sha(p)==h for p,h in pins.items()),'Every retained authoritative build/source/evidence/public pin stable before native matrix')
 need(not BASE.exists()and not OUT.exists()and not JOURNAL.exists(),'Fresh immutable matrix and proof paths')
 BASE.mkdir();save(BASE/'input_hashes_before.json',pins)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
  futures=[pool.submit(run_case,case,guest)for case in CASES];cases=dict(f.result()for f in concurrent.futures.as_completed(futures))
 need(all(sha(p)==h for p,h in pins.items()),'Every retained authoritative source and public artifact unchanged after matrix')
 failures={k:v['error']for k,v in cases.items()if not v['passed']}
 report=dict(passed=not failures,candidate=current.NAME,physicalCases=len(cases),cases=cases,failures=failures,
  newNativeBoots=24,newBuilds=0,rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,wholeGuestSHA256=current.GUEST_SHA,
  inputHashes=pins,goalStatus='active',remaining=parent['remaining'],fullPortAcceptance=False,
  directArtShadowEraseArenaAudioAndCPUAcceptance=False)
 if not failures:
  pcs={pc for v in cases.values()for pc in v['checked']['nativeHealthWriterPCs']};health_source(guest,pcs)
  for side in(1,2):
   for phase in('forward','reverse'):
    a=cases[f'kano_p{side}_{phase}_added']['checked'];b=cases[f'kano_p{side}_{phase}_stock_cage']['checked']
    need(all(a[k]==b[k]for k in('originalNativeIDStores','actualOwnDamageWrites','actualNormalAttackEdges'))and
     a['summary'].get('forwardCancelledBeforeIDStore')==b['summary'].get('forwardCancelledBeforeIDStore')and
     a['summary'].get('reverseInterruptedAndRetried')==b['summary'].get('reverseInterruptedAndRetried'),'Current added and stock physical cancellation/retry semantics match')
  report.update(completeCallbackFields=sum(v['checked']['callbackFields']for v in cases.values()),
   fullCallbackPhysicalPublications=sum(v['checked']['pairedPhysicalFields']+v['checked']['actualMissingPostmatchPublications']for v in cases.values()),
   actualFaultsRejected=[f for k,v in cases.items()for f in faults(k,v)],nativeHealthWriterPCs=sorted(pcs),
   currentBothSidesMorphInterruptionHitRepeatAndKORestoreAccepted=True)
 OUT.mkdir();save(OUT/'report.json',report)
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',"Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"],capture_output=True,text=True)
 need(census.returncode==0,'Actual native process census');live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 need(not any(p['ProcessId']in{v['nativePID']for v in cases.values()}for p in live),'Every captured native process actually terminal')
 files=[p for p in BASE.rglob('*')if p.is_file()]
 need(not any(p.suffix.lower()in('.bin','.png','.wav')for p in files),'No raw guest or media files written')
 measure=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
 measure.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong));measure.restype=ctypes.c_ulong
 allocated=0
 for p in files:
  high=ctypes.c_ulong();ctypes.set_last_error(0);low=measure(str(p),ctypes.byref(high))
  need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual retained native trace allocation');allocated+=(high.value<<32)|low
 for p in files+[OUT/'report.json',LUA,Path(__file__).resolve()]:pins[str(p.resolve())]=sha(p)
 JOURNAL.mkdir();save(JOURNAL/'progress.json',dict(passed=True,goalStatus='active',remaining=parent['remaining'],
  observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),parentAdditiveJournal=str(PARENT),currentMorphProof=str(OUT/'report.json'),
  previousGoalTurnClassification='no progress: acknowledgement only; authoritative checkpoint remains v5402 native queue proof',
  thisGoalTurnClassification='progress: fresh current-build 24-case physical morph matrix; actual failures retained'if failures else
   'progress: fresh current-build 24-case physical morph matrix, full paired state/health/inputs and source-bound stock comparison accepted',
  newNativeBoots=24,newBuilds=0,newDeletedFiles=0,nativeProcessCensus=live,noCapturedNativeProcessStillLive=True,
  actualMatrixAccepted=not failures,actualFailures=failures,rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,
  newlyRetainedNativeTraceLogicalBytes=sum(p.stat().st_size for p in files),newlyRetainedNativeTraceAllocatedBytes=allocated,
  publicPlayableChanged=False,refreshedReleaseZIP=False,fullPortAcceptance=False,newInputHashes=pins,
  nextAction='Investigate actual current morph failures without relaxing native semantics.'if failures else
   'Broaden current morph move-phase art/shadow/cleanup and native stage/finisher contexts; retain all unfinished scope and final combined UI/audio/release work.'))
 return report,allocated

if __name__=='__main__':
 try:
  report,allocated=run();print(json.dumps(dict(passed=report['passed'],physicalCases=report['physicalCases'],failures=report['failures'],
   completeCallbackFields=report.get('completeCallbackFields'),actualFaultsRejected=len(report.get('actualFaultsRejected',[])),
   retainedAllocatedBytes=allocated,fullPortAcceptance=False),indent=2),flush=True)
 except Exception as error:
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
  if not OUT.exists():OUT.mkdir();save(OUT/'report.json',report)
  print(json.dumps(report,indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
