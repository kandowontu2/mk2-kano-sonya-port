"""Observe missing cross held/random Tomb branches through ordinary input timing.

Whole4455 capture and original1731/3643/4357 health/input/801field/1100cleanup
gates retained, with current5219 guest and actual opposite victim. Every trial
is retained as its observed branch, never relabeled to satisfy a desired case.
Only gzip text/digests are saved; no builds, raw media or source-tree copies.
"""
import argparse,concurrent.futures,datetime,gzip,hashlib,inspect,json,os,re,subprocess,time,traceback
from pathlib import Path
import find_tomb_mirror_native_random_drop_v4455 as original
import current_payload_metadata_context_v5229 as current
import current_cross_tomb_branches_v5837 as native
ROOT,need,sha=current.ROOT,current.need,current.sha
NAME=current.NAME
DRIVER='mk2ks_current_cross_tomb_timing_driver_v5870.lua'
OBSERVER='mk2ks_current_cross_tomb_timing_provenance_v5871.lua'
OUT=ROOT/'audit_v5873_current_cross_tomb_native_timing_search'
DEPENDENCIES=(DRIVER,OBSERVER,'mk2ks_current_stage_ram_driver_v3594.lua','mk2ks_current_stage_provenance_v3595.lua')

def once(code,before,after):
 need(code.count(before)==1,'Exactly declared complete timing capture adaptation: '+before)
 return code.replace(before,after,1)

def preflight():
 current.expected()
 parentpath=ROOT/'audit_v5869_current_cross_pressed_tomb_full_scene_matrix_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and
  parent['actualCurrentBothCharactersBothSlotsCrossPressedTombFullSceneGroundShadowEraseAccepted'],
  'Whole prior current stage/move/UI/ending/campaign evidence and original scope retained')
 old=[l for l in (ROOT/'mk2ks_tomb_mirror_random_timing_driver_ram_v4453.lua').read_text().splitlines()if not l.startswith('--')]
 actual=[l for l in (ROOT/DRIVER).read_text().splitlines()if not l.startswith('--')]
 old.remove("replace('local victim_id=id==17 and 18 or 17','local victim_id=id')")
 old=[l.replace('complete3594_true_mirror_physical_command_delay_4453','complete3594_actual_cross_physical_command_delay_5870')for l in old]
 need(old==actual,'Whole4453 timing driver: only mirror override removed, actual cross selection preserved')
 old=[l for l in (ROOT/'mk2ks_tomb_mirror_random_timing_provenance_ram_v4454.lua').read_text().splitlines()if not l.startswith('--')]
 actual=[l for l in (ROOT/OBSERVER).read_text().splitlines()if not l.startswith('--')]
 need('\n'.join(actual)=='\n'.join(old).replace('mk2ks_tomb_mirror_random_timing_driver_ram_v4453.lua',DRIVER).replace(
  'complete3595_true_mirror_pc_qualified_command_delay_4454','complete3595_actual_cross_pc_qualified_command_delay_5871'),
  'Entire4357 actual branch/PC/actor/Main/continuous motion reads unchanged')
 need(native.state.contract_source==native.state.native.source and
  native.state.check_log is native.state.native.check_log and
  native.branch.source==inspect.getsource(native.original.branch).replace('state=runtime.state','state=cross_state',1).replace(
   "own=17 if fighter=='kano'else 18","own=18 if fighter=='kano'else 17",1),
  'Complete original cross earned and source-qualified unpressed held/drop contract retained')
 fn=inspect.getsource(original.capture)
 need(capture_source==adapt(fn)and capture.__globals__['native']is native and
  capture.__globals__['NAME']==current.NAME and capture.__globals__['__doc__']==__doc__,
  'Entire4455 cold capture retained with declared current namespace and gzip-only sinks')
 return dict(passed=True,sourceOnly=True,physicalCommandWaitOnlyChanged=True,nativeRNGStateUntouched=True,
  originalHealthInput801Field1100CleanupContractRetained=True,driverSHA256=sha(ROOT/DRIVER),
  observerSHA256=sha(ROOT/OBSERVER),completeCaptureSourceSHA256=hashlib.sha256(capture_source.encode()).hexdigest().upper(),
  parentProgress=str(parentpath),parentProgressSHA256=sha(parentpath),remaining=parent['remaining'],
  fullSceneRasterShadowAudioAccepted=False,fullPortAcceptance=False)

def adapt(code):
 code=once(code,"'36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982'",repr(current.EXE_SHA))
 code=once(code,"'91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24'",repr(current.PAYLOAD_SHA))
 code=once(code,'actual3836 compiled source','actual5219 compiled source')
 start=code.index('    frozen={}\n')
 stop=code.index("    (folder/'input_hashes_before.json')",start)
 code=code[:start]+"    frozen={str(p):str(p)for p in files if p.suffix in('.lua','.py','.ps1','.json')}\n"+code[stop:]
 code=once(code,"errors='strict') as process:","errors='strict',creationflags=subprocess.CREATE_NO_WINDOW) as process:")
 code=once(code,'dict(pid=process.pid,command=command)',
  'dict(pid=process.pid,command=command,startedUnix=time.time(),hostPID=os.getpid(),hostSource=__file__)')
 code=once(code,"with (folder/'run.log').open('w',encoding='utf-8') as log:",
  "with gzip.open(folder/'run.log.gz','wt',encoding='utf-8') as log:")
 code=once(code,"    log=(folder/'run.log').read_text();errors=(folder/'stderr.log').read_text()",
  "    with gzip.open(folder/'run.log.gz','rt')as reader:log=reader.read()\n    errors=(folder/'stderr.log').read_text()")
 code=once(code,'    checked=native.branch(log,guest,fighter,side)',
  "    checked=native.branch(log,guest,fighter,side)\n    earned_faults=native.state.actual_faults(log,fighter,side,guest)\n    branch_faults=native.faults(log,guest,fighter,side)\n    config=[dict(re.findall(r'(\\w+)=([^\\s]+)',l))for l in log.splitlines()if l.startswith('MK2_TOMB_TIMING_CONFIGURATION ')]\n    need(config==[dict(delay=str(delay),writes='0',assistance='none')],'Actual declared ordinary physical timing only')")
 code=once(code,'       originalEarnedContractPassed=True,noForcedNativeState=True,fullPortAcceptance=False)',
  '       originalEarnedContractPassed=True,actualEarnedFaultsRejected=earned_faults,actualBranchFaultsRejected=branch_faults,noForcedNativeState=True,fullPortAcceptance=False)')
 return code

capture_source=adapt(inspect.getsource(original.capture))
capture_scope=dict(vars(original),__file__=__file__,__doc__=__doc__,native=native,NAME=NAME,
 DRIVER=DRIVER,OBSERVER=OBSERVER,OUT=OUT,DEPENDENCIES=DEPENDENCIES,gzip=gzip,time=time)
exec(compile(capture_source,__file__+'::whole4455_actual_current_cross_timing','exec'),capture_scope)
capture=capture_scope['capture'];capture.source=capture_source

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True)
 parser.add_argument('--first',type=int,required=True);parser.add_argument('--last',type=int,required=True)
 parser.add_argument('--wanted',choices=('held','drop'),required=True)
 args=parser.parse_args();need(1<=args.first<=args.last<=80,'Finite ordinary input delay interval')
 report_path=OUT/f'search_{args.fighter}_p{args.side}_{args.first:02d}_{args.last:02d}_{args.wanted}.json'
 need(not report_path.exists(),'Fresh immutable search range')
 proof=preflight();guest=current.expected();OUT.mkdir(exist_ok=True)
 need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
  'Compress bounded text before native runs')
 trials=[]
 for first in range(args.first,args.last+1,4):
  delays=list(range(first,min(first+4,args.last+1)))
  need(all(not(OUT/f'{args.fighter}_p{args.side}_delay{d:02d}').exists()for d in delays),'Never restart actual executed trial')
  with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
   results=list(pool.map(lambda d:capture(args.fighter,args.side,d,guest),delays))
  for r in results:
   trials.append(r)
   print(json.dumps(dict(fighter=args.fighter,side=args.side,delay=r['physicalDelay'],
    nativeRandom=r['nativeBranch']['actualNativeRandomValue'],actualNativeDrop=r['nativeBranch']['nativeDrop'],
    originalEarnedContractPassed=True)),flush=True)
  if any(r['nativeBranch']['nativeDrop']==(args.wanted=='drop')for r in results):break
 found=[r for r in trials if r['nativeBranch']['nativeDrop']==(args.wanted=='drop')]
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  sourcePreflight=proof,actualTrials=trials,wantedNativeBranch=args.wanted,matchingActualBranches=found,
  requestedNativeBranchObserved=bool(found),allStartedRunsActuallyTerminal=True,
  searchNotStatisticalRNGOrAIClaim=True,fullSceneRasterShadowAudioAccepted=False,
  allCurrentCrossHeldPressedRandomContextsAccepted=False,fullPortAcceptance=False,
  rawNativeGuestRGBVRAMPCMFilesWritten=0,newBuilds=0,publicPlayableChanged=False)
 report_path.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(report=str(report_path),actualTrials=len(trials),wanted=args.wanted,matched=len(found)),indent=2),flush=True)

if __name__=='__main__':main()
