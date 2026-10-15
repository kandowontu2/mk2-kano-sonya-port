"""One naturally chosen current CPU blade hit and blocked knife lifecycle.

Reuse terminal6303 without another game. Preserve the old two-knife scenario
rejection. Adapt its knife mechanics only to one blocked shot in grab-cycle0,
not its poses, child ownership, guard/input/HP, recovery or retirement rules.
Blade body phases, native state publication/contact/cleanup and trail-pointer
lifetime are checked; full effect allocation/raster/shadow/audio stay open.
"""
import datetime,gzip,inspect,json,struct,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import current_kano_cpu_extended_contract_v6291 as model
import verify_current_existing_cpu_leg_choices_v6274 as faults
from build_native_blade import BODY_GROUPS,X_ADVANCES,POSE_FIELDS

ROOT,need,sha=current.ROOT,current.need,current.sha
CASE=ROOT/'audit_v6303_current_kano_cpu_confirm265_ram'
OUT=ROOT/'audit_v6305_current_kano_cpu_blade_knife_checked'
PARENT=ROOT/'audit_v6299_current_kano_cpu_ball_checked/report.json'


knife=model.bind(model.knife.knives,{
 'assert len(actions)==len(births)==2':'assert len(actions)==len(births)==1',
 "native['mode']==(2 if serial==1 else 7)":"native['mode']==2",
 "child['cycle']==1":"child['cycle']==entry['cycle']==0",
 'damage=22 if serial==1 else 6':'damage=6',
 "assert pressed==(serial==2),'Guard flag alone is not an actually held Block button'":
  "assert pressed,'This actual shot must be physically blocked, not inferred from its guard flag'",
 '(hit+24,m,0xff8b6830,actor,serial,1)':'(hit+24,m,0xff8b6830,actor,serial,entry[\'cycle\'])',
 '(m,a,actor,17,81,0x80000,serial,1,0,2)':'(m,a,actor,17,81,0x80000,serial,entry[\'cycle\'],0,2)',
})


def blade_source(guest):
 def check(at,words):
  need(struct.unpack_from('<'+'H'*len(words),guest,(at-0xff800000)//8)==tuple(words),
       'Independently authored whole blade program '+hex(at))
 def movi(n,v):return [0x09e0+n,v&65535,v>>16&65535]
 def call(v):return [0x0d5f,v&65535,v>>16]
 def branch(v):return [0xc080,v&65535,v>>16]
 def cooperate(v):return [0x0147,0x0b07,0x0060,0xa2ec,*branch(v)]
 words=movi(1,0x117)+call(0xff877ba0)+movi(0,0xc8)+call(0xffa12530)
 words+=movi(9,0xfff8e800)+movi(0,2)+cooperate(0xff83c340)
 words+=movi(0,0xfff8e400)+call(0xff835440)+movi(0,0x618)+[0xb00d,0x1f0]
 words+=movi(0,4)+cooperate(0xff83c340)+movi(0,8)+call(0xff80dcc0)
 words+=movi(0,4)+cooperate(0xff83c340)+call(0xff83efd0)+branch(0xff861350)
 check(0xfff8cc00,words)
 check(0xfff8d800,[0xa30f,0x9725,*call(0xff83ada0),0x4d00,0x09af,0x0100,0x4d01,
                  *call(0xff83e8f0),*call(0xff8093e0),0x4c0a,*movi(0,0x51),0xb20a,0xc0,0xb34d,0x190,0x0960])
 check(0xfff8e000,[0xb7aa,0x190,0x4d2b,*call(0xff840b60),0x4d69,0x4d40,0x4d01,*branch(0xff83e8f0)])
 check(0xfff8e400,[109,20,75,67,0x1901,0x1a03,0,0,1])
 script=bytearray()
 def long(v):script.extend(struct.pack('<I',v))
 for i,delta in enumerate(X_ADVANCES):
  if delta:long(3);script.extend(struct.pack('<H',delta))
  long(6);long(0xfff8e000 if i else 0xfff8d800);long(0xfff8f800+i*20*8);long(BODY_GROUPS[i])
  if i in(4,7,9):long(0)
 offset=(0xfff8e800-0xff800000)//8
 need(guest[offset:offset+len(script)]==script,'Entire native blade ten-pose/effect/advance script')
 words=movi(0,1)+call(0xff9a5b00)+movi(0,0x44)+call(0xffa12530)
 words+=movi(5,0xff8d4c10)+movi(6,1)+call(0xff8d49d0)+call(0xffa11fd0)
 words+=movi(0,0x503)+[0xb00d,0x1f0]+movi(9,35)+call(0xff83c100)
 words+=movi(0,0x60000)+call(0xff876be0)+movi(0,8)+call(0xff80dcc0)
 words+=movi(0,0x40000)+call(0xff876be0)+movi(9,0x40023)+cooperate(0xff83bfc0)+branch(0xff861350)
 check(0xfff90000,words)


def gate(text,guest):
 inventory=model.verify(text,guest)
 need([(r['move'],r['frame'])for r in inventory['nativeChoices']]==[('blade',1871),('knife',2442)],
      'Both actual naturally chosen routes, not another scenario')
 model.knife.source(text,guest);blade_source(guest)
 shots=knife(text,guest)
 fields=model.original.pair.rows(text,'FIELD');by={r['frame']:r for r in fields}
 events=model.knife.overlap.rows(text,'EVENT')
 entry=model.knife.one([r for r in events if r['kind']=='blade'],'One actual CPU blade entry')
 start=entry['frame'];actor,main=entry['a8'],entry['a13'];ready=start+sum(POSE_FIELDS)
 first=by[start+1];sign=-1 if first['facing']&16 else 1;trail=first['trail']
 need((entry['entry'],entry['pc'],entry['id'],entry['main_owner'],entry['action'])==
      (0xfff8cc00,0xfff8cc10,17,actor,0x303),'Actual source-native blade entry under walking CPU Main')
 need(0x01000000<=trail<0x01100000 and trail not in(actor,main,first['vactor'],first['vmain']),
      'Distinct attached blade effect, not either character or Main')
 at=start+1;advance=0
 coordinate=lambda v:((v>>16)&65535)-65536 if v&0x80000000 else(v>>16)&65535
 for group,hold,delta in zip(BODY_GROUPS,POSE_FIELDS,X_ADVANCES):
  advance+=delta
  for frame in range(at,at+hold):
   r=by[frame]
   need((r['actor'],r['main'],r['owner'],r['id'],r['roster'],r['vid'],r['vroster'],r['state'],r['vstate'],r['mode'])==
        (actor,main,actor,17,17,17,17,0,1,2),'Actual two native Kano identities/roles throughout blade')
   need((r['x'],r['y'],r['vxpos'],r['vypos'])==tuple(coordinate(r[k])for k in('xraw','yraw','vxraw','vyraw')),
        'Every raw/integer body coordinate bound')
   need(r['pose']==group and r['xraw']==(first['xraw']+sign*(advance<<16))&0xffffffff and
        r['yraw']==first['yraw']==first['floor']<<16 and r['floor']==r['stage_floor']-134 and
        r['vx']==r['vy']==r['gravity']==0 and r['trail']==trail,
        'Every blade body pose, authored hold/advance and grounded attached effect')
   need(r['action']==(0x117 if frame<=start+10 else 0x618)and r['flags']&0x1c==16 and r['body']&12==4,
        'Every startup/recovery field has its own native action and fresh locks')
  at+=hold
 health=[r for r in model.knife.overlap.rows(text,'HEALTH')if start<=r['frame']<=ready and r['before']!=r['after']]
 hit=model.knife.one(health,'One actual blade contact');contact=hit['frame']
 need((contact,hit['slot'],hit['at'],hit['pc'],hit['a8'],hit['a13'],hit['a10'],hit['mask'],hit['before']-hit['after'])==
      (start+10,1,0x010602f0,0xff836700,actor,main,26,65535,26),'Actual own native 26-damage blade hit')
 decision=model.knife.one([r for r in model.knife.rows(text,'BLOCK')if r['frame']==contact and r['decision']in(0,1)],
                         'Actual native blade guard branch')
 need((decision['actor'],decision['main'],decision['owner'],decision['decision'],decision['entry'],decision['pc'])==
      (actor,main,actor,0,0xff837ae0,0xff837af0),'Actual unblocked blade decision')
 for frame in range(start+1,ready+2):
  need(by[frame]['hp']==first['hp']and by[frame]['vhp']==first['vhp']-(26 if frame>contact else 0),
       'No hidden interruption or unlogged extra blade damage')
 for target,process,slot,prefix in((actor,main,2,''),(first['vactor'],first['vmain'],1,'v')):
  regain=model.knife.one([r for r in events if r['kind']=='regain'and r['a8']==target and contact<r['frame']<=ready],
                        'Actual individual blade actor recovery')
  need(regain['frame']==ready and regain['a13']==process and regain['pc']==0xff861510 and
       regain['action']==0 and regain['flags']&0x1c==0 and regain['body']&12==0 and
       regain['vx']==regain['vy']==regain['gravity']==regain['trail']==0 and regain['yraw']==regain['floor']<<16,
       'Original owning ready clears grounded actor and attached effect')
  model.knife.cleanup_store(text,guest,dict(actor=target,main=process),ready,slot)
  after=by[ready+1]
  need(after[prefix+'action']==0x303 and after[prefix+'flags']&0x1c==0 and after[prefix+'body']&12==0 and
       after[prefix+'vy']==after[prefix+'gravity']==after[prefix+'trail']==0,'Next real callback remains detached and recovered')
 flags=model.knife.P.flag_rows(text)
 for kind,pc,before,after in(('action',0xff877bc0,0x303,0x117),('body',0xff838cf0,entry['body'],entry['body']|4),
                            ('flags',0xff877d50,entry['flags'],entry['flags']|16),('action',0xfff8ce40,0x117,0x618)):
  frame=contact if pc==0xfff8ce40 else start
  q=model.knife.one([r for r in flags if r['slot']==2 and r['frame']==frame and r['kind']==kind and r['pc']==pc],
                   'Individual native blade publication/lock/recovery store')
  need((q['actor'],q['main'],q['a8'],q['a13'],q['before'],q['after'])==(actor,main,actor,main,before,after),
       'Fresh native setup, never residual previous-action locks')
 return dict(nativeStateHealthAndChoices=inventory,blade=dict(start=start,contact=contact,damage=26,ownReady=ready,
             victimReady=ready,bodyFields=sum(POSE_FIELDS),poseGroups=len(BODY_GROUPS),attachedPointer=trail,
             fullEffectAllocationRetirementTapAcceptance=False),knives=shots,
             artShadowAudioAcceptance=False,allCPUAccepted=False,fullPortAcceptance=False)


def main():
 need(not OUT.exists(),'Never overwrite executed qualification')
 report=json.loads((CASE/'result.json').read_text());terminal=json.loads((CASE/'native_terminal.json').read_text())
 need(report['passed']and report['nativeExit']==0 and terminal['naturalTerminal']and terminal['exitCode']==0,
      'Same actual capture already naturally terminal')
 need(not faults.census.prior.census(),'Actual native census empty; no additional replay')
 pins=dict(report['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'All executed input sources unchanged')
 with gzip.open(CASE/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
 guest=current.expected();positive=gate(text,guest)
 def mutate(tag,key,value,where):return faults.mutate_field(text,tag,key,value,lambda r:all(r.get(k)==str(v)for k,v in where.items()))
 trials=[
  ('blade_pose',mutate('MK2_CPU_PAIR_FIELD','pose','00000000',{'frame':1874})),
  ('blade_advance',mutate('MK2_CPU_PAIR_FIELD','xraw','00000000',{'frame':1876})),
  ('blade_height',mutate('MK2_CPU_PAIR_FIELD','yraw','00000000',{'frame':1878})),
  ('blade_trail_lost',mutate('MK2_CPU_PAIR_FIELD','trail','00000000',{'frame':1884})),
  ('blade_recovery_state',mutate('MK2_CPU_PAIR_FIELD','action','279',{'frame':1886})),
  ('blade_damage',mutate('MK2_CPU_OVERLAP_HEALTH','a10','00000019',{'frame':1881})),
  ('blade_guard_branch',mutate('MK2_KNIFE_PAIR_BLOCK','decision','1',{'frame':1881,'decision':0})),
  ('blade_ready_trail',mutate('MK2_CPU_OVERLAP_EVENT','trail','01030000',{'frame':1909,'kind':'regain'})),
  ('blade_setup_owner',mutate('MK2_CPU_PAIR_FLAG','a8','01000000',{'frame':1871,'kind':'body'})),
  ('knife_child_parent',mutate('MK2_CPU_OVERLAP_CHILD','shot_owner','01000000',{'frame':2445})),
  ('knife_child_pose',mutate('MK2_CPU_OVERLAP_CHILD_FIELD','pose','00000000',{'frame':2448})),
  ('knife_flight_speed',mutate('MK2_CPU_OVERLAP_CHILD_FIELD','vx','FFF00000',{'frame':2466})),
  ('knife_hit_damage',mutate('MK2_CPU_OVERLAP_HEALTH','a10','00000016',{'frame':2471})),
  ('knife_guard_main',mutate('MK2_KNIFE_PAIR_TESTED','loaded_main','01000000',{'frame':2471})),
  ('knife_false_button',mutate('MK2_KNIFE_PAIR_BLOCK','controls','FFFFFFFF',{'frame':2471,'decision':2})),
  ('knife_impact_pose',mutate('MK2_CPU_OVERLAP_CHILD_FIELD','pose','00000000',{'frame':2473})),
  ('knife_early_retire',mutate('MK2_CPU_OVERLAP_RETIRE','frame','2494',{'frame':2495})),
  ('knife_body_pose',mutate('MK2_KNIFE_PAIR_FIELD','pose','00000000',{'frame':2450,'slot':2})),
  ('knife_ready_lock',mutate('MK2_CPU_OVERLAP_EVENT','body','0056',{'frame':2491,'kind':'regain'})),
  ('native_rng_threshold',mutate('MK2_CPU_CHOICE_EVENT','a0','000000FB',{'kind':'first_call'})),
  ('native_round_refill',mutate('MK2_CPU_ROUND_HEALTH','after','160',{'mode':6,'slot':1})),
 ]
 rejected=[]
 for label,bad in trials:
  need(bad!=text,'Actual record changed '+label)
  try:gate(bad,guest)
  except(AssertionError,ValueError,KeyError,IndexError)as error:rejected.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Accepted actual blade/knife fault: '+label)
 need(gate(text,guest)==positive,'Untouched positive restored after every fault')
 parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active','Full objective remains active')
 for path in(PARENT,Path(__file__),Path(model.__file__),Path(model.knife.__file__),ROOT/'tools/build_native_blade.py',
             *(p for p in CASE.rglob('*')if p.is_file())):pins[str(path.resolve())]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'All native and independent source evidence unchanged')
 result=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=current.NAME,
             goalStatus='active',parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],case=positive,
             actualFaultsRejected=rejected,inputHashes=pins,scope=__doc__,newNativeBoots=0,newBuilds=0,newZIPs=0,newRawMedia=0,
             fullPortAcceptance=False,fullGoalComplete=False,preservedOriginalStandaloneKnifeScenarioRejection=True,
             previousGoalTurnClassification='progress: current native ball and full state/HP qualification',
             thisGoalTurnClassification='progress: same naturally terminal blade/blocked-knife full body/contact/recovery and knife-child phases; actual record faults',
             nextAction='Remaining effect artwork/floor-shadows/audio and broader mixed CPU continuations; no repeat solely for these accepted motion phases')
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
      'Only exact lossless report compression')
 print(json.dumps(dict(passed=True,blade=positive['blade'],knives=positive['knives'],actualFaultsRejected=len(rejected),newBuilds=0)),flush=True)


if __name__=='__main__':
 try:main()
 except Exception as error:
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
