"""Independent native earned shatter/own legs/next CPU-match instances, not full art/audio."""
import copy,hashlib,json,re,struct,subprocess
from pathlib import Path
import native_subzero_legs_context_v4993 as native
import verify_earned_subzero_offset_matrix_v4913 as parser

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v5005_native_subzero_legs_matrix_checked'

def verify(guest,rows,log,identity,side,scenes):
 prefix='MK2_EARNED_SUBZERO_'
 def pick(tag):
  found=[r for r in rows if r['tag']==prefix+tag]
  need(len(found)==1,'Exactly one actual '+tag)
  return found[0]
 deep,body,hit,punch,fracture,legs,wrap,end=(pick(t)for t in('DEEP_TASK','BODY_LOOKUP','SHATTER_ENTRY','HUMAN_PUNCH','FRACTURE_ENTRY','LEGS_LOOKUP','WIN_WRAP','LIFECYCLE_END'))
 first,impact,last=int(deep['frame']),int(fracture['frame']),int(end['natural'])
 victim='01034E90'if side==1 else'010350A0';winner='010350A0'if side==1 else'01034E90'
 whole='FFD62400'if identity==17 else'FFD62480';lower='FFD63400'if identity==17 else'FFD63460'
 dizzy='FF011F60'if identity==17 else'FF0320C0';offset='FFFD4610'if identity==17 else'FFFD4620'
 def word(a):
  need(a%16==0 and 0xff800000<=a<=0xfffffff0,'Guest opcode bounds')
  return struct.unpack_from('<H',guest,(a-0xff800000)//8)[0]
 def dword(a):return struct.unpack_from('<I',guest,(a-0xff800000)//8)[0]
 traces=[r for r in rows if 'entry'in r and r['tag'].startswith(prefix)and first<=int(r['frame'])<last]
 for r in traces:
  pc=int(r['entry'],16)
  need(r['writes']=='0'and r['assistance']=='none'and r['identity']==str(identity)and r['side']==str(side),
       'Actual native physical trace without assistance')
  need(int(r['pc'],16)==pc+16 and r['mask']=='FFFF'and word(pc)==int(r['value'],16),'Actual native opcode/PC/mask equals whole initialized guest')
  rid=int(r.get('id',r.get('roster','-1')))
  need(rid in(identity,8)and r['actor']==r['owner']==(victim if rid==identity else winner),
       'Native branch bound to true victim or opposing Sub-Zero')
  if 'hp'in r:need(r['hp']=='0'and r['roster']==str(identity),'Genuine earned zero-health victim')
 need(int(body['frame'])==first+56 and int(body['a9'],16)==identity*32 and body['action']=='0616','Actual true frozen body index')
 main_rows=[r for r in traces if r['tag']==prefix+'MAIN_LOOKUP']
 need(len(main_rows)==1,'Exactly one native finisher main40 lookup in victim lifetime')
 main=main_rows[0]
 need(main['a0']=='00000000'and main['a1']==offset and word(int(offset,16))==0,'Actual native dedicated zero main40 offset')
 need(dword(0xff8c26c0)==0xffd62600 and dword(0xffd62600+identity*32)==int(whole,16),
      'Actual whole-body ROM consumer/row is owned')
 need(hit['id']==punch['id']=='8'and hit['frame']==punch['frame']and hit['entry']=='FF8C0D90'and punch['entry']=='FF8C1180',
      'Actual human branch, not CPU special/proxy action')
 need(fracture['id']==legs['id']==str(identity)and fracture['action']==legs['action']=='0408'
      and fracture['frame']==legs['frame']and fracture['pose']==legs['pose']==whole
      and int(legs['a9'],16)==identity*32,'Actual native fracture and true legs index')
 need(dword(0xff8c3090)==0xffd62a00 and dword(0xffd62a00+identity*32)==int(lower,16),
      'Actual native legs consumer/row is owned')
 caches=[r for r in traces if r['tag']==prefix+'CACHE_BEGIN']
 need(any(r['a0']==dizzy and int(r['frame'])==first and r['action']=='0616'for r in caches),'Native own dizzy cache')
 need(any(r['a0']==whole and int(r['frame'])==first+56 and r['action']=='0616'for r in caches),'Native own frozen-body cache')
 need(any(r['a0']==lower and int(r['frame'])==impact and r['action']=='0408'for r in caches),'Native own two-leg cache')
 parks=[r for r in traces if r['tag']==prefix+'NATIVE_PARK']
 need(parks and int(parks[0]['frame'])==impact and all(r['pose']==lower and r['action']=='0408'for r in parks)
      and all(int(b['frame'])-int(a['frame'])==64 for a,b in zip(parks,parks[1:])),
      'Original native64-field parked-leg loop, not supposed immediate actor removal')
 sound,emitter,effect=(pick(t)for t in('SOUND_CALL','ICE_EMITTER','EFFECT_SPAWN'))
 need(sound['a0']=='000000D8'and all(int(r['frame'])==impact for r in(sound,emitter,effect)),
      'Actual original fracture sound call and emitter/effect entry times')
 ex=pick('ICE_EMITTER_EXTRA');fx=pick('EFFECT_SPAWN_EXTRA')
 need(ex['a11']=='00080008'and fx['a7']=='FF9EE3A0'and ex['palette']==fx['palette']=='0404',
      'Actual native ice emitter and effect task with actual ice palette bank')
 fields=[r for r in rows if r['tag']==prefix+'FIELD'and first<=int(r['frame'])<last]
 need([int(r['frame'])for r in fields]==list(range(first,last)),'Every actual physical victim field through natural departure')
 for r in fields:
  f=int(r['frame'])
  need(r['actor']==r['owner']==victim and r['identity']==r['roster']==str(identity)and r['side']==str(side)
       and r['writes']=='0'and r['assistance']=='none'and r['hp']=='0'and r['state']in('1','2'),
       'All genuine physical victim fields remain valid until departure')
  if first+56<=f<impact:need(r['pose']==whole and r['action']in('0616','0408'),'Owned whole body until native fracture')
  if f>=impact:need(r['pose']==lower and r['action']=='0408','Owned parked two-leg body through departure')
 histories=[r for r in rows if r['tag']=='MK2_STOCK_HEAD_V921_COMPARE']
 need(len(histories)==7 and [int(r['wanted'])for r in histories]==([6,7,7,7,7,6,7]if side==1 else[6,8,8,8,8,6,8]),
      'Actual mirrored FFD freeze and FDFF shatter reverse histories')
 for r in histories:need(r['wanted']==r['actual']and word(int(r['table'],16)-16)==int(r['wanted'])and r['pc']=='FF8777A0',
                         'Each physical native command comparison bound to ROM')
 gates=[r for r in rows if r['tag']=='MK2_STOCK_HEAD_V921_GATE']
 need(len(gates)==1 and gates[0]['limit']=='69'and int(gates[0]['distance'])<=69 and gates[0]['frame']==hit['frame'],
      'Original native69 center-gap gate actually passed; never widened')
 result=[r for r in rows if r['tag']=='MK2_STOCK_HEAD_V921_RESULT']
 need(len(result)==1 and result[0]['damage']=='322'and result[0]['wins']=='2'and result[0]['action']==hit['frame']
      and result[0]['wrap']==wrap['frame'],'Actual two earned rounds, finisher and win completion')
 need(int(end['fracture'])==impact and end['wrap']==wrap['frame']and int(end['frame'])>last
      and end['mode']=='2'and end['winner_state']=='1'and end['enemy_state']=='0'
      and end['winner_id']=='8'and int(end['enemy_id'])<=18 and end['winner_hp']==end['enemy_hp']=='161'
      and end['winner_actor']==end['winner_owner']and end['enemy_actor']==end['enemy_owner']
      and end['enemy_actor']!=victim and end['winner_pose']not in(whole,lower)and end['enemy_pose']not in(whole,lower),
      'Actual subsequent native CPU match, distinct valid actors and fresh health/poses')
 need([r['frame']for r in scenes]==[first+100,impact+20,int(wrap['frame'])+150,int(end['frame'])]
      and all(r['width']==400 and r['height']==254 and r['bytes']==406400 and r['rawMediaFilesWritten']==0 for r in scenes),
      'Actual four native RGB stages independently bound to physical events')
 need('CACHE_OVERWRITE 'not in log and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',log,re.I),'No errors or global overrun')
 return dict(identity=identity,side=side,nativeFreezeFrame=first,nativeHumanShatterFrame=int(hit['frame']),
             nativeFractureFrame=impact,nativeWinFrame=int(wrap['frame']),naturalDepartureFrame=last,
             actualNextCPUMatchFrame=int(end['frame']),actualConsecutiveVictimFields=len(fields),
             actualNativeOpcodesBound=len(traces),actualPhysicalHistoryComparisons=7,nativeGateLimit=69,
             actualNativeGateDistance=int(gates[0]['distance']),ownWholeGroup=whole,ownLegsGroup=lower,
             originalNativeParkIterations=len(parks),nativeSequenceInstanceVerified=True,
             ownedLegsRuntimeInstanceVerified=True,actualSubsequentMatchVerified=True,
             actualRGBFields=scenes,fullArtAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False)

def main():
 need(not OUT.exists(),'Fresh independent native shatter matrix')
 guest=native.expected();gfx=native.expected_gfx();pins={};cases=[];faults=[]
 for fighter,identity in(('kano',17),('sonya',18)):
  for side in(1,2):
   folder=ROOT/f'audit_v5002_subzero_{fighter}_p{side}_lifecycle'
   observed=ROOT/f'audit_v5003_subzero_{fighter}_p{side}_lifecycle_observed/report.json'
   report=json.loads(observed.read_text());meta=json.loads((folder/'result.json').read_text())
   need(report['passed']and report['nativeExit']==0 and not report['fullPortAcceptance'],'Actual consumed successful terminal lifecycle case')
   g=json.loads((folder/'guest_memory_proof.json').read_text());x=json.loads((folder/'gfx_memory_proof.json').read_text())
   need(g['everyActualByteComparedInRAM']and g['bytes']==1048576 and g['sha256']==native.GUEST_SHA
        and g['executableSHA256']==native.EXE_SHA and g['rawGuestFilesWritten']==0,'Every actual cold guest byte compared in RAM')
   need(x==dict(bytes=len(gfx),sha256=hashlib.sha256(gfx).hexdigest().upper(),everyActualByteComparedInRAM=True),'All actual native own GFX bytes compared in RAM')
   log=(folder/'run.log').read_text();rows=parser.parse(log);scenes=json.loads((folder/'rgb_memory_proofs.json').read_text())
   need(scenes==report['actualScenes']and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',(folder/'stderr.log').read_text(),re.I),'Exact RGB evidence and clean stderr')
   cases.append(verify(guest,rows,log,identity,side,scenes))
   for label,tag,key,value in(
    ('wrong_opcode','SHATTER_ENTRY','value','0000'),('proxy_victim','FRACTURE_ENTRY','id','1'),
    ('proxy_whole_index','BODY_LOOKUP','a9','00000160'),('proxy_legs_index','LEGS_LOOKUP','a9','00000160'),
    ('wrong_sound','SOUND_CALL','a0','00000000'),('wrong_emitter','ICE_EMITTER_EXTRA','a11','00000000'),
    ('wrong_effect','EFFECT_SPAWN_EXTRA','a7','00000000'),('wrong_palette','ICE_EMITTER_EXTRA','palette','0000'),
    ('invalid_park_pose','NATIVE_PARK','pose','FFFFFFFF'),('bad_next_owner','LIFECYCLE_END','enemy_owner','00000000'),
    ('fake_next_health','LIFECYCLE_END','enemy_hp','0'),('weakened_gate','MK2_STOCK_HEAD_V921_GATE','limit','85')):
    changed=copy.deepcopy(rows);target=next(r for r in changed if r['tag']==tag or r['tag']=='MK2_EARNED_SUBZERO_'+tag);target[key]=value
    try:verify(guest,changed,log,identity,side,scenes)
    except ValueError as e:faults.append(dict(case=f'{fighter}_p{side}',fault=label,rejectedBy=str(e)))
    else:raise ValueError('Fault admitted '+label)
   changed=[r for r in rows if r['tag']!='MK2_EARNED_SUBZERO_LEGS_LOOKUP']
   try:verify(guest,changed,log,identity,side,scenes)
   except ValueError as e:faults.append(dict(case=f'{fighter}_p{side}',fault='missing_native_legs_entry',rejectedBy=str(e)))
   else:raise ValueError('Missing actual native legs entry admitted')
   pins.update(meta['inputHashes'])
   for p in[observed,*[p for p in folder.rglob('*')if p.is_file()]]:pins[str(p.resolve())]=sha(p)
 for p in(Path(__file__),Path(native.__file__),Path(parser.__file__)):pins[str(p.resolve())]=sha(p)
 need(len(cases)==4 and len(faults)==52 and all(sha(p)==h for p,h in pins.items()),'Actual four cases/faults and immutable executed evidence')
 result=dict(passed=True,candidate=native.NAME,executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,
  cases=cases,actualFaultsRejected=faults,inputHashes=pins,nativeShatterSequenceInstancesVerified=4,
  ownedFrozenLegsRuntimeInstancesVerified=4,actualSubsequentCPUMatchesVerified=4,
  fullArtAcceptance=False,fullAudioAcceptance=False,normalHealthFreezeAccepted=False,fullPortAcceptance=False,publicBuildPromoted=False)
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress before evidence')
 (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(passed=True,cases=cases,actualFaultsRejected=len(faults),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
