"""Independent four actual earned native0616 offset regressions, not finishers."""
import copy, hashlib, json, re, struct, subprocess
from pathlib import Path
import run_native_subzero_offset_regression_v4856 as native

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v4914_earned_subzero_offset_matrix_checked'

def parse(log):
 return [dict(re.findall(r'(\w+)=([^\s]+)',line),tag=line.split()[0])
         for line in log.splitlines() if line.startswith(('MK2_EARNED_SUBZERO_','MK2_STOCK_HEAD_V921_'))
         and 'GUEST_DIGEST' not in line]

def verify(guest,rows,log,identity,side):
 def pick(suffix):
  matches=[r for r in rows if r['tag']=='MK2_EARNED_SUBZERO_'+suffix]
  need(len(matches)==1,'Exactly one actual '+suffix)
  return matches[0]
 deep,lookup,body,end,stop=(pick(k) for k in ('DEEP_TASK','MAIN_LOOKUP','BODY_LOOKUP','HOST_EXIT','RESULT'))
 first=int(deep['frame']);last=int(end['frame'])
 actor='01034E90' if side==1 else '010350A0'
 own='FF011F60' if identity==17 else 'FF0320C0'
 stream='FF0048F0' if identity==17 else 'FF0248F0'
 table='FFFD4610' if identity==17 else 'FFFD4620'
 def read(address):
  need(0xff800000<=address<=0xfffffff0 and address%16==0,'Actual guest word bounds')
  return struct.unpack_from('<H',guest,(address-0xff800000)//8)[0]
 traces=[r for r in rows if 'entry' in r and r['tag'].startswith('MK2_EARNED_SUBZERO_')]
 for r in traces:
  address=int(r['entry'],16)
  need(r['writes']=='0' and r['assistance']=='none' and r['identity']==r['roster']==str(identity)
       and r['side']==str(side) and r['actor']==r['owner']==actor and r['hp']=='0',
       'Every actual native record bound to true physical victim and earned zero health')
  need(int(r['pc'],16)==address+16 and r['mask']=='FFFF' and read(address)==int(r['value'],16),
       'Every actual native opcode/PC/mask bound to entire initialized guest')
 need(lookup['frame']==deep['frame'] and lookup['a0']=='00000000' and lookup['a1']==table
      and lookup['a9']=='00000028' and read(int(table,16))==0,
      'Actual dedicated17/18 zero offset, not original overread')
 cache=next(r for r in traces if r['tag'].endswith('CACHE_BEGIN') and r['frame']==deep['frame'])
 need(cache['a0']==own and cache['a9']==stream and cache['action']=='0616',
      'Actual character-owned main40 stream and valid native group cache')
 need(int(body['frame'])==first+56 and body['a9']=='00000160' and body['action']=='0616',
      'Actual unchanged later body lookup56fields after native entry; still clamps to11')
 fields=[r for r in rows if r['tag']=='MK2_EARNED_SUBZERO_FIELD']
 need([int(r['frame'])for r in fields]==list(range(first,last+1)) and last==first+400,
      'Every401 consecutive post-entry native field, exact actual bounded stop')
 for r in fields:
  need(r['actor']==r['owner']==actor and r['identity']==r['roster']==str(identity)
       and r['side']==str(side) and r['hp']=='0' and r['state']=='1' and r['action']=='0616'
       and r['writes']=='0' and r['assistance']=='none','Entire bounded real frozen victim state remains valid')
 need(any(r['pose']==own for r in fields) and fields[-1]['pose']=='FF8C2E10',
      'Own dizzy advances into original Jax body; own frozen-body acceptance explicitly missing')
 results=[r for r in rows if r['tag']=='MK2_STOCK_HEAD_V921_RESULT']
 need(len(results)==1 and results[0]['damage']=='322' and results[0]['wins']=='2'
      and int(results[0]['frame'])==last+1,'Two genuine native earned rounds and terminal result')
 need(stop['deep']==str(first) and stop['uppercut']==stop['completed']=='-1'
      and int(stop['frame'])==last+1,'Finite freeze-only probe, never shatter completion')
 compares=[r for r in rows if r['tag']=='MK2_STOCK_HEAD_V921_COMPARE']
 need(len(compares)==3 and [int(r['wanted'])for r in compares]==([6,7,7] if side==1 else [6,8,8]),
      'Actual mirrored reverse history for Forward Forward Down')
 for r in compares:
  need(r['wanted']==r['actual'] and read(int(r['table'],16)-16)==int(r['wanted'])
       and r['pc']=='FF8777A0','Every actual history comparison independently bound to ROM')
 need('CACHE_OVERWRITE 'not in log and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',log,re.I),
      'No callback errors or global cache overwrite')
 return dict(identity=identity,side=side,nativeEntryFrame=first,bodyLookupFrame=first+56,
             nativeStopFrame=last,actualNativeRecordsBound=len(traces),actualConsecutiveFields=len(fields),
             actualEarnedDamage=322,actualEarnedWins=2,ownDizzyGroup=own,nativeGlobalCacheOverrunRows=0,
             ownFrozenBodyAccepted=False,fullShatterAccepted=False,normalHealthFreezeAccepted=False)

def main():
 need(not OUT.exists(),'Fresh independent matrix proof')
 guest=native.expected();pins={str(Path(__file__).resolve()):sha(Path(__file__))};cases=[];faults=[]
 for fighter,identity in (('kano',17),('sonya',18)):
  for side in (1,2):
   folder=ROOT/f'audit_v4911_subzero_{fighter}_p{side}_earned'
   observed=ROOT/f'audit_v4912_subzero_{fighter}_p{side}_earned_observed/report.json'
   report=json.loads(observed.read_text())
   need(report['passed'] and report['nativeExit']==0 and not report['fullPortAcceptance'],'Actual terminal bounded case')
   proof=json.loads((folder/'guest_memory_proof.json').read_text())
   need(proof['everyActualByteComparedInRAM'] and proof['bytes']==1048576 and proof['sha256']==native.GUEST_SHA
        and proof['executableSHA256']==native.EXE_SHA and proof['rawGuestFilesWritten']==0,'Whole actual cold guest independently compared in RAM')
   meta=json.loads((folder/'result.json').read_text());pins.update(meta['inputHashes'])
   log=(folder/'run.log').read_text();errors=(folder/'stderr.log').read_text()
   need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',errors,re.I),'Actual stderr clean')
   rows=parse(log);positive=verify(guest,rows,log,identity,side);cases.append(positive)
   changes=(('wrong_offset','MAIN_LOOKUP','a0','00002B90'),('wrong_native_row','MAIN_LOOKUP','a1','FF8C28F0'),
            ('wrong_opcode','DEEP_TASK','value','0000'),('proxy_identity','MAIN_LOOKUP','roster','1'),
            ('proxy_body','CACHE_BEGIN','a0','FFFFFFFF'),('uneared_health','MAIN_LOOKUP','hp','161'),
            ('corrupt_state','FIELD','state','1296'),('bad_history','MK2_STOCK_HEAD_V921_COMPARE','actual','5'))
   for label,suffix,key,value in changes:
    altered=copy.deepcopy(rows)
    target=next(r for r in altered if r['tag']==suffix or r['tag']=='MK2_EARNED_SUBZERO_'+suffix)
    target[key]=value
    try:verify(guest,altered,log,identity,side)
    except ValueError as e:faults.append(dict(case=f'{fighter}_p{side}',fault=label,rejectedBy=str(e)))
    else:raise ValueError('Actual fault admitted '+label)
    need(verify(guest,rows,log,identity,side)==positive,'Original actual records restored')
   altered=[r for r in rows if not(r['tag']=='MK2_EARNED_SUBZERO_FIELD'and int(r['frame'])==positive['nativeEntryFrame']+80)]
   try:verify(guest,altered,log,identity,side)
   except ValueError as e:faults.append(dict(case=f'{fighter}_p{side}',fault='missing_actual_field',rejectedBy=str(e)))
   else:raise ValueError('Missing actual field admitted')
   for path in [observed,*[p for p in folder.rglob('*')if p.is_file()]]:pins[str(path.resolve())]=sha(path)
 need(len(cases)==4 and len(faults)==36 and all(sha(p)==h for p,h in pins.items()),'Exact actual matrix and all inputs unchanged')
 result=dict(passed=True,candidate=native.NAME,executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,
             cases=cases,actualFaultsRejected=faults,inputHashes=pins,actualWholeColdGuestComparisons=4,
             nativeGlobalCacheOverrunRows=0,fullPortAcceptance=False,fullShatterAccepted=False,
             ownFrozenBodyAccepted=False,normalHealthFreezeAccepted=False,publicBuildPromoted=False)
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress before evidence')
 (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(passed=True,cases=cases,actualFaultsRejected=len(faults),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
