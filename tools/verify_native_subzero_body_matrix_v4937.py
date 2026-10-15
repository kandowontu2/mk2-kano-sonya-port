"""Independent actual owned frozen body matrix; full shatter remains unproven."""
import copy, hashlib, json, re, struct, subprocess
from pathlib import Path
import native_subzero_body_context_v4932 as native
import verify_earned_subzero_offset_matrix_v4913 as prior

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v4938_native_subzero_body_matrix_checked'

def verify(guest,rows,log,identity,side):
 def pick(tag):
  matches=[r for r in rows if r['tag']=='MK2_EARNED_SUBZERO_'+tag]
  need(len(matches)==1,'One actual '+tag)
  return matches[0]
 deep,lookup,body,end,stop=(pick(t)for t in ('DEEP_TASK','MAIN_LOOKUP','BODY_LOOKUP','HOST_EXIT','RESULT'))
 first,last=int(deep['frame']),int(end['frame'])
 actor='01034E90'if side==1 else'010350A0'
 dizzy='FF011F60'if identity==17 else'FF0320C0'
 stream='FF0048F0'if identity==17 else'FF0248F0'
 offset='FFFD4610'if identity==17 else'FFFD4620'
 group='FFD62400'if identity==17 else'FFD62480'
 def word(a):
  need(0xff800000<=a<=0xfffffff0 and a%16==0,'Guest word bounds')
  return struct.unpack_from('<H',guest,(a-0xff800000)//8)[0]
 traces=[r for r in rows if 'entry'in r and r['tag'].startswith('MK2_EARNED_SUBZERO_')]
 for r in traces:
  address=int(r['entry'],16)
  need(r['writes']=='0'and r['assistance']=='none'and r['identity']==r['roster']==str(identity)
       and r['side']==str(side)and r['actor']==r['owner']==actor and r['hp']=='0',
       'Actual native trace belongs to earned true victim')
  need(int(r['pc'],16)==address+16 and r['mask']=='FFFF'and word(address)==int(r['value'],16),
       'Every actual opcode/PC/mask matches initialized guest')
 need(lookup['frame']==deep['frame']and lookup['a0']=='00000000'and lookup['a1']==offset
      and lookup['a9']=='00000028'and word(int(offset,16))==0,'Actual dedicated zero main40 offset')
 cache=next(r for r in traces if r['tag'].endswith('CACHE_BEGIN')and r['frame']==deep['frame'])
 need(cache['a0']==dizzy and cache['a9']==stream and cache['action']=='0616','Owned dizzy native cache')
 need(int(body['frame'])==first+56 and int(body['a9'],16)==identity*32 and body['action']=='0616',
      'Actual unclamped true17/18 frozen-body indexing')
 address=0xffd62600+identity*32
 need(struct.unpack_from('<I',guest,(address-0xff800000)//8)[0]==int(group,16),'Native row points to owned body')
 frozen=next(r for r in traces if r['tag'].endswith('CACHE_BEGIN')and int(r['frame'])==first+56)
 need(frozen['a0']==group and frozen['action']=='0616','Actual owned frozen body enters native cache')
 fields=[r for r in rows if r['tag']=='MK2_EARNED_SUBZERO_FIELD']
 need([int(r['frame'])for r in fields]==list(range(first,last+1))and last==first+400,
      'Every401 consecutive actual fields with exact bounded stop')
 for r in fields:
  need(r['actor']==r['owner']==actor and r['identity']==r['roster']==str(identity)and r['side']==str(side)
       and r['hp']=='0'and r['state']=='1'and r['action']=='0616'and r['writes']=='0'and r['assistance']=='none',
       'Entire physical frozen victim state valid')
  if int(r['frame'])>=first+56:need(r['pose']==group,'Every actual frozen body pose is owned; no Jax proxy')
 need(any(r['pose']==dizzy for r in fields),'Actual owned dizzy before freeze conversion')
 results=[r for r in rows if r['tag']=='MK2_STOCK_HEAD_V921_RESULT']
 need(len(results)==1 and results[0]['damage']=='322'and results[0]['wins']=='2'
      and int(results[0]['frame'])==last+1,'Two real native earned rounds')
 need(stop['deep']==str(first)and stop['uppercut']==stop['completed']=='-1'and int(stop['frame'])==last+1,
      'Finite freeze-only result, never inferred shatter')
 history=[r for r in rows if r['tag']=='MK2_STOCK_HEAD_V921_COMPARE']
 need(len(history)==3 and [int(r['wanted'])for r in history]==([6,7,7]if side==1 else[6,8,8]),
      'Actual mirrored physical Forward Forward Down history')
 for r in history:need(r['wanted']==r['actual']and word(int(r['table'],16)-16)==int(r['wanted'])and r['pc']=='FF8777A0',
                       'Each actual history compared to native ROM')
 need('CACHE_OVERWRITE 'not in log and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',log,re.I),
      'No callback errors or global overwrite')
 return dict(identity=identity,side=side,nativeEntryFrame=first,bodyLookupFrame=first+56,nativeStopFrame=last,
             actualNativeRecordsBound=len(traces),actualConsecutiveFields=len(fields),ownFrozenGroup=group,
             actualEarnedDamage=322,actualEarnedWins=2,ownedFrozenBodyInstanceVerified=True,
             fullShatterAccepted=False,normalHealthFreezeAccepted=False,fullArtAcceptance=False)

def main():
 need(not OUT.exists(),'Fresh independent evidence leaf')
 guest=native.expected();gfx=native.expected_gfx();pins={};cases=[];faults=[]
 for fighter,identity in (('kano',17),('sonya',18)):
  for side in(1,2):
   folder=ROOT/f'audit_v4935_subzero_{fighter}_p{side}_earned'
   observed=ROOT/f'audit_v4936_subzero_{fighter}_p{side}_earned_observed/report.json'
   report=json.loads(observed.read_text());meta=json.loads((folder/'result.json').read_text())
   need(report['passed']and report['nativeExit']==0 and not report['fullPortAcceptance'],'Actual terminal case')
   proof=json.loads((folder/'guest_memory_proof.json').read_text())
   need(proof['everyActualByteComparedInRAM']and proof['bytes']==len(guest)and proof['sha256']==native.GUEST_SHA
        and proof['executableSHA256']==native.EXE_SHA and proof['rawGuestFilesWritten']==0,'Whole cold guest RAM proof')
   gp=json.loads((folder/'gfx_memory_proof.json').read_text())
   need(gp==dict(bytes=len(gfx),sha256=hashlib.sha256(gfx).hexdigest().upper(),everyActualByteComparedInRAM=True),
        'Every actual owned GFX byte matched independently')
   log=(folder/'run.log').read_text();rows=prior.parse(log)
   need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',(folder/'stderr.log').read_text(),re.I),'Clean native stderr')
   positive=verify(guest,rows,log,identity,side)
   rgb=json.loads((folder/'rgb_memory_proof.json').read_text())
   need(rgb==report['actualRGBField']and rgb['frame']==positive['nativeEntryFrame']+100 and rgb['width']==400
        and rgb['height']==254 and rgb['bytes']==406400 and len(rgb['sha256'])==64 and rgb['rawMediaFilesWritten']==0,
        'Actual RAM-only RGB field bound to owned native pose time')
   positive['actualRGBSHA256']=rgb['sha256'];cases.append(positive)
   for label,tag,key,value in (
     ('bad_offset','MAIN_LOOKUP','a0','00002B90'),('bad_offset_row','MAIN_LOOKUP','a1','FF8C28F0'),
     ('bad_opcode','DEEP_TASK','value','0000'),('proxy_identity','MAIN_LOOKUP','roster','1'),
     ('invalid_cache','CACHE_BEGIN','a0','FFFFFFFF'),('unearned_health','MAIN_LOOKUP','hp','161'),
     ('bad_state','FIELD','state','1296'),('Jax_index','BODY_LOOKUP','a9','00000160'),
     ('Jax_pose','FIELD','pose','FF8C2E10'),('bad_history','MK2_STOCK_HEAD_V921_COMPARE','actual','5')):
    altered=copy.deepcopy(rows)
    targets=[r for r in altered if r['tag']==tag or r['tag']=='MK2_EARNED_SUBZERO_'+tag]
    target=targets[-1]if label=='Jax_pose'else targets[0];target[key]=value
    try:verify(guest,altered,log,identity,side)
    except ValueError as e:faults.append(dict(case=f'{fighter}_p{side}',fault=label,rejectedBy=str(e)))
    else:raise ValueError('Fault admitted '+label)
   altered=[r for r in rows if not(r['tag']=='MK2_EARNED_SUBZERO_FIELD'and int(r['frame'])==positive['nativeEntryFrame']+80)]
   try:verify(guest,altered,log,identity,side)
   except ValueError as e:faults.append(dict(case=f'{fighter}_p{side}',fault='missing_field',rejectedBy=str(e)))
   else:raise ValueError('Missing actual field admitted')
   pins.update(meta['inputHashes'])
   for path in[observed,*[p for p in folder.rglob('*')if p.is_file()]]:pins[str(path.resolve())]=sha(path)
 for path in[Path(__file__),Path(native.__file__),Path(prior.__file__)]:pins[str(path.resolve())]=sha(path)
 need(len(cases)==4 and len(faults)==44 and all(sha(p)==h for p,h in pins.items()),'All actual cases/faults and immutable inputs')
 result=dict(passed=True,candidate=native.NAME,executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,
             cases=cases,actualFaultsRejected=faults,inputHashes=pins,actualWholeGuestComparisons=4,actualWholeOwnedGFXComparisons=4,
             ownedFrozenBodyInstancesVerified=4,fullPortAcceptance=False,fullShatterAccepted=False,
             legsOnlyRuntimeAccepted=False,fullArtAcceptance=False,normalHealthFreezeAccepted=False,publicBuildPromoted=False)
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress evidence')
 (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(passed=True,cases=cases,actualFaultsRejected=len(faults),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
