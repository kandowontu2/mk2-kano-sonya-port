"""Actual current close contacts and both throw roles, full paired body/shadows.

Both real own IDs17/18 in both physical slots against Kitana4 on Dead Pool.
Keep the complete original body/clip/FIFO/eligibility/projection/row scanner;
replace only the ordinary finite controller/state gate with this actual program.
No universal arena/CPU/KO, continuous whole-scene/audio or artistic claim.
"""
import copy,inspect,json,re,struct,traceback
from collections import defaultdict
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import qualify_current_basic_kitana_raw_v6021 as earlier
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6034_current_close_contacts_checked'
PHASES=('own_high_punch_block','own_high_kick_block','own_low_kick_crouch_block',
        'stock_high_punch_own_block','own_high_punch_hit','own_ground_throw','stock_ground_throw')

def clean(r):
 return int(r['y'])==int(r['floor'])and all(r[k]=='00000000'for k in('vx','vy','gravity','trail'))and\
        int(r['flags'],16)&0x1c==0 and int(r['body'],16)&0x0c==0 and int(r['action'])==771

def state_gate(b,guest,payload):
 rows=b['rows'];side=b['side'];identity=17 if b['fighter']=='kano'else 18
 finals=rows['MK2_BASIC_RESULT'];need(len(finals)==1,'One current native contact terminal')
 final=finals[0];ready=int(final['ready']);terminal=int(final['terminalAge'])
 need(final['phases']=='7'and final['completed']=='1'and 1200<terminal<2500,'Whole7 interactions and natural queued terminal')
 pres={(int(r['frame'])-ready,int(r['slot'])):r for r in rows['MK2_BASIC_FIELD']}
 posts={(int(r['frame'])-ready,int(r['slot'])):r for r in rows['MK2_HPHASE_POST_FIELD']}
 need(len(pres)==len(rows['MK2_BASIC_FIELD'])==2*(terminal+1)and set(pres)=={(a,s)for a in range(terminal+1)for s in(1,2)}and
      len(posts)==len(rows['MK2_HPHASE_POST_FIELD'])==2*terminal and set(posts)=={(a,s)for a in range(terminal)for s in(1,2)},
      'Every pre/draw-complete/extra queued callback, no discarded victim phases')
 ids={side:identity,3-side:4};anchors={17:134,18:135,4:133}
 owners={s:(posts[0,s]['actor'],posts[0,s]['main'])for s in(1,2)}
 for table in(pres,posts):
  for (age,s),r in table.items():
   need(r['writes']=='0'and r['assistance']=='none'and int(r['mode'])==2 and int(r['stage'])==0 and
        int(r['stageY'])==216 and int(r['id'])==int(r['roster'])==ids[s]and int(r['state'])==1 and
        (r['actor'],r['main'])==owners[s]and r['actor']==r['owner']and 0<int(r['hp'])<=161 and
        int(r['floor'])==216-anchors[ids[s]],'Every stable actual real-ID actor/Main/owner/HP/source floor, including both thrown victims')
 steps=rows['MK2_BASIC_STEP'];recoveries=rows['MK2_BASIC_RECOVERED']
 need(len(steps)==len(recoveries)==7 and tuple(r['phase']for r in steps)==tuple(r['phase']for r in recoveries)==PHASES and
      [int(r['cycle'])for r in steps]==[int(r['cycle'])for r in recoveries]==list(range(1,8)),
      'All seven actual physical phase boundaries and complete paired recovery')
 events=rows['MK2_BASIC_CONTACT'];addresses={0xff8b6bb0,0xff842d90,0xff906110,0xff836150,0xff835e50,0xff835e70,0xff80f6b0}
 for r in events:
  address=int(r['address'],16);s=int(r['slot']);cycle=int(r['cycle']);f=int(r['frame'])-ready
  need(address in addresses and s in(1,2)and 1<=cycle<=7 and r['phase']==PHASES[cycle-1]and
       0<=f<terminal and r['writes']=='0'and r['assistance']=='none'and
       r['a8']==owners[s][0]and r['a13']==owners[s][1]and int(r['id'])==ids[s]and
       int(r['pc'],16)==address+16 and int(r['mask'],16)==65535 and
       int(r['opcode'],16)==struct.unpack_from('<H',guest,(address-0xff800000)//8)[0],
       'Every actual native instruction PC/opcode/register owner bound to whole observed guest, never observer self-read')
 # Complete health chain, not a handful of convenient snapshots.
 stores=rows['MK2_BASIC_HEALTH'];by_store=defaultdict(list);totals={1:0,2:0}
 for r in stores:
  need(r['writes']=='0'and r['assistance']=='none'and int(r['pc'],16)==0xff836700 and int(r['mask'],16)==65535,
       'Every real damage store is original full-word health writer')
  by_store[int(r['frame'])-ready,int(r['slot'])].append(r)
 for age in range(terminal):
  for s in(1,2):
   hp=int(pres[age,s]['hp'])
   for r in by_store[age,s]:
    need(int(r['before'])==hp and 0<int(r['after'])<hp,'Every ordered damage store follows actual previous physical HP')
    totals[s]+=hp-int(r['after']);hp=int(r['after'])
   need(hp==int(posts[age,s]['hp'])==int(pres[age+1,s]['hp']),'Exact pre/store/post/next-callback native HP chain')
 need(len(stores)==7 and sum(len(v)for v in by_store.values())==7,'Exactly one real health contact per declared interaction')
 cases=[]
 for cycle,(step,recovered,label)in enumerate(zip(steps,recoveries,PHASES),1):
  start=int(step['frame'])-ready;end=int(recovered['frame'])-ready
  attacker=3-side if cycle in(4,7)else side;defender=3-attacker
  need(int(step['attacker'])==attacker and int(step['defender'])==defender and 0<int(step['gap'])<=64 and
       abs(int(pres[start,1]['x'])-int(pres[start,2]['x']))==int(step['gap'])and
       clean(pres[start,1])and clean(pres[start,2])and end-start==160 and
       clean(pres[end,1])and clean(pres[end,2]),'Real close approach and160field full clean grounded paired recovery')
  if cycle<7:need(int(steps[cycle]['frame'])>int(recovered['frame']),'Next physical approach starts only after actual prior recovery')
  ev=[r for r in events if int(r['cycle'])==cycle and start<=int(r['frame'])-ready<=end]
  health=[r for r in stores if start<=int(r['frame'])-ready<=end]
  need(len(health)==1 and int(health[0]['slot'])==defender,'Each interaction has one real correctly owned victim damage store')
  dose=int(health[0]['before'])-int(health[0]['after']);contact=int(health[0]['frame'])
  blocked=[r for r in ev if int(r['address'],16)==0xff836150]
  success=[r for r in ev if int(r['address'],16)==0xff835e50]
  throws=[r for r in ev if int(r['address'],16)==0xff8b6bb0]
  if cycle<=4:
   guard=1793 if cycle==3 else 1792
   need(len(blocked)==len(success)==1 and not throws and int(blocked[0]['b2'],16)==int(success[0]['b2'],16)==1 and
        blocked[0]['frame']==success[0]['frame']==str(contact)and int(blocked[0]['slot'])==int(success[0]['slot'])==attacker and
        int(posts[contact-ready,defender]['action'])==guard and dose==6 and
        int(blocked[0]['a7'],16)&255==dose,
        'Actual original B2=1 blocked branch/contact/chip packed descriptor and native guard, not a miss or label')
  elif cycle==5:
   need(not blocked and not throws and len(success)==1 and success[0]['frame']==str(contact)and
        int(success[0]['slot'])==attacker and int(success[0]['b2'],16)==0 and dose==24,
        'Actual distinct unblocked original close strike, not guarded or a throw')
  else:
   victim_index=43 if cycle==6 else 46
   need(not blocked and len(throws)==1 and int(throws[0]['slot'])==attacker and start+20<int(throws[0]['frame'])-ready<start+30,
        'One genuine human throw entry after real forward/LowPunch controls')
   entry=int(throws[0]['frame'])
   lookup=[r for r in ev if r['frame']==str(entry)and int(r['address'],16)==0xff842d90]
   selected=[r for r in ev if r['frame']==str(entry)and int(r['address'],16)==0xff906110 and int(r['slot'])==defender]
   need(len(lookup)==len(selected)==1 and int(lookup[0]['slot'])==attacker and
        int(lookup[0]['a9'],16)==int(selected[0]['a9'],16)==victim_index and dose==(32 if cycle==6 else 30)and
        any(int(posts[a,attacker]['action'])==0x507 for a in range(entry-ready,end))and
        len({posts[a,defender]['pose']for a in range(entry-ready,end)})>=3,
        'Actual own main43 or stock Kitana main46 selection through real victim root, native throw damage and changing paired living poses')
  cases.append(dict(phase=label,cycle=cycle,attackerSlot=attacker,defenderSlot=defender,actualGap=int(step['gap']),
                    start=start,recovered=end,nativeDamage=dose,blockedBranch=cycle<=4,trueThrow=cycle>=6,
                    semanticLivingVictimIndex=43 if cycle==6 else 46 if cycle==7 else None))
 need(totals[side]==36 and totals[3-side]==74 and all(clean(posts[terminal-1,s])for s in(1,2)),
      'Complete final real native stance/floor/velocities/body flags/trail and exact cumulative HP ledger')
 return dict(passed=True,trueIdentity=identity,physicalSlot=side,stage=0,actualInteractions=cases,
             completePreActorFields=len(pres),completePostActorFields=len(posts),nativeHealthStores=7,
             totalDamageByPhysicalSlot=totals,actualBlockedContacts=4,actualUnblockedCloseStrike=1,
             ownAttackerAndLivingVictimThrowRolesAccepted=True,allStrikeHitMissBlockBranchesAccepted=False,fullPortAcceptance=False)

def bindings():
 # Build the already-qualified whole raw-Kitana/source/body/shadow checker,
 # then replace its finite6018 ordinary-state callback, not any native kernel.
 original=earlier.physical.body;source=inspect.getsource(original.check)
 before='  if not c&128:\n'
 after="""  if not c&128 and graphic==0x0144ab50:
   decoded[key]=kitana_raw_starts(graphic,w,h,c,gfx,t)
   continue
  if not c&128:
"""
 need(source.count(before)==1,'Only already-qualified exact stock raw branch retained');source=source.replace(before,after,1)
 first=source.index(' # The older physical/ownership/health checker');last=source.index(" fields=rows['MK2_HPHASE_POST_FIELD']",first)
 source=source[:first]+" state=state_gate(b,guest,payload)\n entry_frames={int(r['frame'])for r in rows['MK2_BASIC_CONTACT']if r['address']=='FF8B6BB0'}\n"+source[last:]
 scope=dict(original.check.__globals__,state_gate=state_gate,kitana_raw_starts=earlier.raw_scanner())
 exec(compile(source,__file__+'::entire_native_body_shadow_kernels_close_contact_physical_gate','exec'),scope)
 return scope['check']

def load(fighter,side):
 folder=ROOT/f'audit_v6031_contacts_{fighter}_p{side}';report_path=ROOT/f'audit_v6032_contacts_{fighter}_p{side}_observed/report.json'
 report=json.loads(report_path.read_text());need(report['passed']and report['nativeExit']==0 and report['candidate']==current.NAME and
      report['executableSHA256']==current.EXE_SHA and report['guestSHA256']==current.GUEST_SHA and report['payloadSHA256']==current.PAYLOAD_SHA,
      'Actual terminal current true-ID close-contact capture')
 text=(folder/'run.log').read_text();need('hex='not in text and (folder/'stderr.log').read_text()==''and 'MK2_BASIC_FAILED'not in text,'No raw buffer persistence or native/controller failure')
 rows=defaultdict(list)
 for line in text.splitlines():
  if line.startswith(('MK2_BASIC_','MK2_HPHASE_')):
   pairs=re.findall(r'(\w+)=([^\s]+)',line);need(len(pairs)==len(dict(pairs)),'Unique real protocol fields');rows[line.split()[0]].append(dict(pairs))
 return dict(fighter=fighter,move='knife'if fighter=='kano'else'ring',side=side,folder=folder,report_path=report_path,report=report,
             rows=rows,streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()))

def run():
 need(not OUT.exists(),'Fresh immutable full current close contact qualification')
 prior_path=ROOT/'audit_v6022_current_ordinary_kitana_raw_checked/report.json';prior=json.loads(prior_path.read_text())
 need(prior['passed']and all(sha(p)==h for p,h in prior['inputHashes'].items()),'Retain full qualified original ordinary/native body-shadow evidence')
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 pins={str(Path(__file__).resolve()):sha(__file__),str(prior_path):sha(prior_path)}
 body=earlier.physical.body;gfx=body.reconstruct(pins);own=current.expected_gfx()
 gfx[0x1fa0000:0x1fa0000+11944]=own[:11944];gfx[0x1fa4000:0x1fa4000+7032]=own[11944:]
 for header,magic in((0x1c0000,b'KFX1'),(0x1c1000,b'KPI1'),(0x1c2000,b'KPJ1'),(0x1d0000,b'KBL1')):
  need(payload[header:header+4]==magic,'Actual runtime graphics patch header');source,count,dest=struct.unpack_from('<III',payload,header+4)
  need(source+count<=len(payload)and dest+count<=len(gfx),'Whole source-bounded payload graphics patch');gfx[dest:dest+count]=payload[source:source+count]
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in((0xff801070,0xff8017b0),(0xff804160,0xff804430),(0xff835410,0xff836720),(0xff837900,0xff837be0)):
  need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==original[(lo-0xff800000)//8:(hi-0xff800000)//8],
       'Whole original native body/shadow/collision/block/health/guard kernel unchanged')
 check=bindings();cases=[];faults=[]
 for fighter in('kano','sonya'):
  for side in(1,2):
   b=load(fighter,side);case=check(b,guest,payload,gfx);case['fighter']=fighter
   for p,h in b['report']['inputHashes'].items():need(sha(p)==h,'Every actual executed source/compiled dependency stable');pins[p]=h
   for p in b['folder'].rglob('*'):
    if p.is_file():pins[str(p)]=sha(p)
   pins[str(b['report_path'])]=sha(b['report_path'])
   tests=[('proxy_ID','MK2_HPHASE_POST_FIELD','id','1'),('wrong_floor','MK2_HPHASE_POST_FIELD','floor','999'),
          ('wrong_owner','MK2_HPHASE_POST_FIELD','owner','01000000'),('missing_hp_store','MK2_BASIC_HEALTH','after','160'),
          ('wrong_body_source','MK2_HPHASE_CANDIDATE','source','00000000'),('wrong_shadow_owner','MK2_HPHASE_SHADOW_BEGIN','owner','01000000'),
          ('projection_shift','MK2_HPHASE_PROJECTION','dy','999'),('wrong_shadow_x','MK2_HPHASE_SHADOW_DMA','x','999'),
          ('wrong_shadow_pen','MK2_HPHASE_SHADOW_DMA','color','0101'),('wrong_shadow_row','MK2_HPHASE_SHADOW_DMA','source','00000001')]
   for label,tag,key,value in tests:
    changed=copy.deepcopy(b);need(changed['rows'][tag][0][key]!=value,'Actual changed record, no no-op mutation');changed['rows'][tag][0][key]=value
    try:check(changed,guest,payload,gfx)
    except ValueError as error:faults.append(dict(fighter=fighter,side=side,fault=label,rejectedBy=str(error)))
    else:raise ValueError('Actual native semantic fault accepted: '+label)
   for label,predicate,key,value in(
    ('block_as_miss',lambda r:r['address']=='FF836150','b2','00000000'),
    ('throw_wrong_living_victim_row',lambda r:r['address']=='FF842D90'and r['cycle']=='6','a9','0000003C'),
    ('throw_wrong_stock_victim_root',lambda r:r['address']=='FF906110'and r['cycle']=='7'and r['a9']=='0000002E','a8','01000000')):
    changed=copy.deepcopy(b);row=next(r for r in changed['rows']['MK2_BASIC_CONTACT']if predicate(r));need(row[key]!=value,'Actual branch/throw fault changes record');row[key]=value
    try:check(changed,guest,payload,gfx)
    except ValueError as error:faults.append(dict(fighter=fighter,side=side,fault=label,rejectedBy=str(error)))
    else:raise ValueError('Actual native branch/throw fault accepted: '+label)
   changed=copy.deepcopy(b);changed['streams'][0]['sha256']='0'*64
   try:check(changed,guest,payload,gfx)
   except ValueError as error:faults.append(dict(fighter=fighter,side=side,fault='wrong_actual_ROM_stream',rejectedBy=str(error)))
   else:raise ValueError('Actual complete graphics source fault accepted')
   cases.append(case);print(fighter+' P'+str(side)+':7 actual contacts/throw roles; every body/shadow field and14 faults qualified',flush=True)
 for p in(Path(earlier.__file__).resolve(),Path(body.__file__).resolve(),ROOT/'tools/verify_move_phase_shadow_v5089.py',ROOT/'tools/native_stock_raw_shadow_scanner_v5315.py'):
  pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All current/failed/accepted executed evidence bytes immutable')
 return dict(passed=True,candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,payloadSHA256=current.PAYLOAD_SHA,
             cases=cases,actualSemanticFaultsRejected=faults,inputHashes=pins,actualBlockedContacts=16,actualUnblockedCloseStrikes=4,
             actualOwnAttackerThrows=4,actualOwnLivingVictimThrows=4,actualActorFields=sum(c['actualContiguousActorFields']for c in cases),
             nativeBodyCandidates=sum(c['actualNativeBodyCandidates']for c in cases),nativeShadowCopies=sum(c['actualSourceBoundShadowCopies']for c in cases),
             wholePairedGroundingBodyAndNativeShadowCleanupAccepted=True,allStrikeHitMissBlockBranchesAccepted=False,
             continuousWholeSceneRGBReplayAccepted=False,allArenaCPURepeatedKOOverlapAccepted=False,
             fullArtAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable full current contact matrix')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected','cases')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
