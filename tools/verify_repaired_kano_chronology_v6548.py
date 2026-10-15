"""Qualify the exact source-derived packed task-ID change, not arbitrary drift.

The terminal capture's overstrict historical-equality rejection remains false.
Every row/field is compared; only one actual P2 knife task ID is expected to
change, derived independently from both whole initialized guest images.
No emulator rerun, guest write, dropped field or rewritten historical report.
"""
import collections,datetime,gzip,json,re,struct,subprocess
from pathlib import Path
import capture_repaired_kano_effects_v6540 as capture
import verify_current_cpu_effect_render_v6354 as counters
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
CASE=capture.FOLDER
OUT=ROOT/'audit_v6549_repaired_kano_chronology_checked'
PREFIXES=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_',
          'MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_','MK2_BLADE_ALLOC_')

def load(folder):
 with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as f:return f.read()

def task_id(guest):
 pointer=struct.unpack_from('<I',guest,capture.candidate.repair.offset(0xff8b5d30))[0]
 packed=struct.unpack_from('<I',guest,capture.candidate.repair.offset(pointer)+17*4)[0]
 return packed>>16

def chronology(actual,wanted,old_id,new_id):
 need(len(actual)==len(wanted)==14238,'Every original chronology row retained exactly once')
 differences=[(i,a,b)for i,(a,b)in enumerate(zip(actual,wanted))if a!=b]
 need(len(differences)==1,'Exactly one source-derived task ID changes; no other trajectory drift')
 index,a,b=differences[0]
 fixed='MK2_KNIFE_PAIR_BLOCK frame=2471 entry=FF837BD0 pc=FF837BE0 actor=010356D0 main=01071960 owner=010356D0 parent=010350A0 decision=1 controls=FFFFFFDF process_slot='
 need(a==fixed+str(new_id)+' writes=0 assistance=none'and
      b==fixed+str(old_id)+' writes=0 assistance=none',
      'Exact actual unchanged native physical block branch/actor/owner with source-derived P2 task ID')
 return dict(index=index,oldRow=b,actualRow=a,oldPackedTaskID=old_id,newPackedTaskID=new_id,
             allOtherRowsAndCharactersExact=True,exactRows=len(actual),noDroppedFields=True)

def qualified_meta():
 proof=json.loads((OUT/'report.json').read_text())
 need(proof['passed']and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Exact additive task-ID qualification intact')
 meta=json.loads((CASE/'result.json').read_text());terminal=json.loads((CASE/'native_terminal.json').read_text())
 # New in-memory evidence view only. The captured failed JSON stays untouched.
 meta['continuousRender']=proof['continuousRender']
 return meta,terminal,proof

def main():
 need(not OUT.exists()and not capture.original.terminal.process_tools.census(),'Fresh qualifier; actual native process terminal')
 meta=json.loads((CASE/'result.json').read_text());terminal=json.loads((CASE/'native_terminal.json').read_text())
 need(meta['passed']is False and meta['error']=="ValueError('Whole actual input/AI/RNG/health/state/pool chronology unchanged')"and
      terminal['naturalTerminal']and terminal['exitCode']==meta['nativeExit']==0 and not terminal['observationErrors']and
      not(CASE/'stderr.log').read_text().strip()and meta['proof']['everyActualByteComparedInRAM']and
      meta['proof']['sha256']==capture.candidate.GUEST_SHA,'Exact terminal capture and complete native guest proof; original rejection preserved')
 pins=dict(meta['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Actual executed inputs unchanged')
 baseline=ROOT/'audit_v6342_current_cpu_blade_allocation_ram'
 previous=json.loads((ROOT/'audit_v6344_current_cpu_blade_allocation_checked/report.json').read_text())
 need(previous['passed']and previous['inputHashes'][str(baseline/'run.log.gz')]==sha(baseline/'run.log.gz'),'Independent original complete allocation trajectory remains pinned')
 text=load(CASE);old=load(baseline)
 actual=[l for l in text.splitlines()if l.startswith(PREFIXES)]
 wanted=[capture.word_to_digest(l)for l in old.splitlines()if l.startswith(PREFIXES)]
 old_id=task_id(capture.candidate.old.expected());new_id=task_id(capture.candidate.expected())
 need((old_id,new_id)==(0xcb0c,0x0800),'Actual old instruction overread vs independently constructed ordinary player-two task family')
 observer=ROOT/'mk2ks_physical_p2_cpu_knife_trace_v1955.lua'
 need('p:read_u16(m+0x20)'in observer.read_text(),'process_slot is actual native task identity, not roster/proxy selection')
 positive=chronology(actual,wanted,old_id,new_id)
 faults=[]
 index=positive['index']
 for label,key,value in [('wrong task ID','process_slot','51980'),('wrong controls','controls','FFFFFFFF'),
                         ('wrong parent','parent','00000000'),('wrong decision','decision','0')]:
  bad=list(actual);bad[index]=re.sub(r'\b'+key+r'=\S+',key+'='+value,bad[index],count=1)
  try:chronology(bad,wanted,old_id,new_id)
  except(ValueError,AssertionError)as e:faults.append(dict(kind=label,rejectedBy=str(e)))
  else:raise ValueError('False task/physical chronology accepted '+label)
 for label,bad in [('missing callback',actual[:index]+actual[index+1:]),('duplicate callback',actual[:index]+[actual[index]]+actual[index:])]:
  try:chronology(bad,wanted,old_id,new_id)
  except(ValueError,AssertionError)as e:faults.append(dict(kind=label,rejectedBy=str(e)))
  else:raise ValueError('False callback cardinality accepted')
 need(chronology(actual,wanted,old_id,new_id)==positive,'Untouched full positive restored')
 words=sum(bool(re.search(r'\bdata=[0-9A-F]{4}(?=\s)',l))for l in old.splitlines()if l.startswith(PREFIXES))
 need(words==3326,'All original two-byte allocator words compared cryptographically')
 # Reuse the whole original operation-count derivation, bound to this capture.
 import inspect
 source=inspect.getsource(counters.transport_contract)
 start=source.index(' # Recover counters');stop=source.index('\n return meta,terminal,',start)
 namespace=dict(counters.__dict__,meta=meta,terminal=terminal,current=text,
                prior=type('CurrentRecords',(),{'CASE':CASE,'model':counters.prior.model}))
 exec(compile('def derive():\n'+source[start:stop]+'\n return meta["continuousRender"]\n',__file__+'::whole_original_operation_counters','exec'),namespace)
 render=namespace['derive']()
 records=json.loads((CASE/'continuous_scene_records.json').read_text())
 oldrecords=ROOT/'audit_v6349_current_cpu_effect_render_ram/continuous_scene_records.json'
 need(records==json.loads(oldrecords.read_text()),'Every full641-field RGB/native body/effect/shadow scene exactly matches original')
 need(meta['independentSemantics']['blade']['bodyFields']==38 and len(meta['independentSemantics']['knives'])==1,
      'Whole original phase gate completed before overstrict task-ID comparison')
 for p in [Path(__file__),Path(counters.__file__),Path(capture.__file__),observer,baseline/'run.log.gz',oldrecords,
           *(p for p in CASE.rglob('*')if p.is_file())]:pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All actual native and independent source evidence intact')
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
             candidate=capture.candidate.NAME,originalCapturePassed=False,originalCaptureRejectionPreserved=True,
             exactSourceDerivedChronology=positive,numericWordsCryptographicallyCompared=words,
             everyContinuousNativeSceneRecordIdenticalToPrior=True,continuousRender=render,
             actualFaultsRejected=faults,inputHashes=pins,newNativeBoots=0,newBuilds=0,newRawMedia=0,
             fullPortAcceptance=False,scope=__doc__)
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact report compression')
 print(json.dumps(dict(passed=True,exactRows=len(actual),changedTaskID=new_id,fields=641,actualFaultsRejected=len(faults))),flush=True)

if __name__=='__main__':main()
