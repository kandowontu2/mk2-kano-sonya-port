"""Current real airborne roles, repeated recovery and whole paired body/shadows.

Eight actual cold-selected human contexts on Dead Pool: Kano versus Kitana,
Sonya and Jax, and living Sonya versus stock Jax, both physical slots. No proxy,
CPU assistance, state scrub, imported raw admission or universal acceptance.
Jax's interrupted guard pulse and unobserved stock callback invocation ledger
remain explicitly incomplete; button labels are not successful guard evidence.
"""
import copy,inspect,json,re,struct,traceback
from collections import defaultdict
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import qualify_current_close_contacts_v6033 as contacts
import native_stock_raw_shadow_scanner_v5315 as stock
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6052_current_air_throw_roles_checked'
MATRIX=tuple((f,s,v)for f,v in(('kano','kitana'),('kano','sonya'),('kano','jax'),('sonya','jax'))for s in(1,2))
VID={'kitana':4,'sonya':18,'jax':11}
RAW={(0x0144ab50,11,40),(0x0170b4f6,11,52),(0x028658f4,11,22),(0x0286c3ac,9,19),
     (0x02a76530,11,16),(0x02ae6e3c,7,24),(0x02b1284e,8,8),(0x02b1ed82,5,9),(0x02d2167a,11,19)}
ADDRESSES=dict(gate=0xff8643e0,action=0xff8b6ff0,alignment=0xfffc0680,early_release=0xfffff980,
 own_flight=0xfffff580,victim_callback=0xfffff800,bounce=0xfffc2000,damage=0xff83a7a0,
 own_landing=0xfffc1c00,victim_getup=0xff8ea320,recovery=0xff861410,stock_flight=0xff8da830,
 handoff=0xff842710,victim_lookup=0xff842d90,animation_lookup=0xff906110,physics=0xff876660)

def h(r,k):return int(r[k],16)
def clean(r):return contacts.clean(r)and int(r['suppression'])==0

def state_gate(b,guest,payload):
 rows=b['rows'];side=b['side'];identity=17 if b['fighter']=='kano'else 18
 ids={side:identity,3-side:VID[b['victim']]};anchors={17:134,18:135,4:133,11:139}
 final=rows['MK2_BASIC_RESULT'];need(len(final)==1,'One actual current airborne terminal')
 final=final[0];ready=int(final['ready']);terminal=int(final['terminalAge'])
 need(final['phases']=='2'and final['completed']=='1'and 800<terminal<1200,'Both actual air catches and paired normal followups completed')
 pre={(int(r['frame']),int(r['slot'])):r for r in rows['MK2_BASIC_FIELD']}
 post={(int(r['frame']),int(r['slot'])):r for r in rows['MK2_HPHASE_POST_FIELD']}
 need(len(pre)==len(rows['MK2_BASIC_FIELD'])==2*(terminal+1)and set(pre)=={(f,s)for f in range(ready,ready+terminal+1)for s in(1,2)}and
      len(post)==len(rows['MK2_HPHASE_POST_FIELD'])==2*terminal and set(post)=={(f,s)for f in range(ready,ready+terminal)for s in(1,2)},
      'All pre/draw-complete paired fields plus exact extra queued-exit callback, no dropped victim/entry fields')
 owners={s:(pre[ready,s]['actor'],pre[ready,s]['main'])for s in(1,2)}
 for table in(pre,post):
  for (f,s),r in table.items():
   raw=h(r,'yraw');integer=(raw>>16)-65536 if raw&0x80000000 else raw>>16
   need(r['writes']=='0'and r['assistance']=='none'and int(r['mode'])==2 and int(r['stage'])==0 and int(r['stageY'])==216 and
        int(r['id'])==int(r['roster'])==ids[s]and int(r['state'])==1 and (r['actor'],r['main'])==owners[s]and
        r['owner']==r['actor']and 0<int(r['hp'])<=161 and int(r['floor'])==216-anchors[ids[s]]and integer==int(r['y']),
        'Every true owned living actor/Main/roster, independent source floor, whole fractional Y and healthy native state')
 # Every health transition, including real ordinary return-punch interruptions.
 stores=rows['MK2_BASIC_HEALTH'];by=defaultdict(list);totals={1:0,2:0}
 for r in stores:
  need(r['writes']=='0'and r['assistance']=='none'and h(r,'pc')==0xff836700 and h(r,'mask')==65535,
       'Only genuine original full-word health stores')
  by[int(r['frame']),int(r['slot'])].append(r)
 for f in range(ready,ready+terminal):
  for s in(1,2):
   hp=int(pre[f,s]['hp'])
   for r in by[f,s]:
    need(int(r['before'])==hp and 0<int(r['after'])<hp,'Every ordered actual damage store has exact previous physical HP')
    totals[s]+=hp-int(r['after']);hp=int(r['after'])
   need(hp==int(post[f,s]['hp'])==int(pre[f+1,s]['hp']),'Complete pre/store/post/next-callback HP chain')
 need(sum(len(v)for v in by.values())==len(stores),'No out-of-capture discarded damage store')
 events=rows['MK2_BASIC_AIR_EVENT']
 for r in events:
  kind=r['kind'];s=int(r['slot']);at=ADDRESSES.get(kind);f=int(r['frame'])
  need(at is not None and s in(1,2)and ready<=f<ready+terminal and r['writes']=='0'and r['assistance']=='none'and
       (r['actor'],r['main'])==owners[s]and r['owner']==r['actor']==r['a8']and int(r['id'])==ids[s]and
       (kind=='gate'or r['a13']==owners[s][1])and h(r,'address')==at and h(r,'pc')==at+16 and h(r,'mask')==65535 and
       h(r,'opcode')==struct.unpack_from('<H',guest,(at-0xff800000)//8)[0],
       'Actual instruction PC/opcode/mask and complete owned registers, native input-event task allowed only at real gate')
 boundaries=[rows[k]for k in('MK2_BASIC_STEP','MK2_BASIC_RECOVERED','MK2_BASIC_FOLLOWUP','MK2_BASIC_CYCLE_DONE')]
 need(all(len(t)==2 and [int(r['cycle'])for r in t]==[1,2]for t in boundaries),'All repeated real air and full followup boundaries')
 inputs=defaultdict(list)
 for r in rows['MK2_BASIC_INPUT']:
  need(r['writes']=='0'and r['assistance']=='none','Human controls only, no processor/cache/RNG/state assignments')
  inputs[int(r['frame']),int(r['slot'])].append(r['button'])
 cases=[];guard_successes=0;interrupted=[]
 for cycle,(step,recovered,follow,done)in enumerate(zip(*boundaries),1):
  start,end,begin,finish=(int(r['frame'])for r in(step,recovered,follow,done))
  attacker=3-side if ids[3-side]==11 and(identity==18 or cycle==2)else side;victim=3-attacker;kano=ids[attacker]==17
  need(int(step['attacker'])==attacker and int(step['attackerID'])==ids[attacker]and int(step['victimID'])==ids[victim]and
       0<int(step['gap'])<=64 and abs(int(pre[start,1]['x'])-int(pre[start,2]['x']))==int(step['gap'])and
       all(clean(pre[start,s])and clean(pre[end,s])and clean(pre[finish,s])for s in(1,2))and
       end-start==180 and begin==end+16 and finish==begin+160,'Actual physical spacing and complete paired recovery, no pointer-null shortcut')
  if cycle==2:need(start>int(boundaries[3][0]['frame']),'Repeated catch only after complete previous normal followup')
  ev=[r for r in events if int(r['cycle'])==cycle]
  def one(kind,slot):
   found=[r for r in ev if r['kind']==kind and int(r['slot'])==slot and start<=int(r['frame'])<end]
   need(len(found)==1,'One true air role '+kind);return found[0]
  catch=one('action',attacker);caught=int(catch['frame']);release=one('early_release',attacker)
  damage=one('damage',attacker);land=one('victim_getup',victim);handoff=one('handoff',attacker);lookup=one('victim_lookup',attacker)
  need(caught==start+22==int(recovered['catch'])and int(release['frame'])==caught+(8 if kano else 17)and
       int(damage['frame'])==caught+(25 if kano else 34)and h(damage,'a0')==(16 if kano else 32)and
       damage['a10']==owners[victim][0]and h(lookup,'a9')==63 and int(lookup['frame'])==int(release['frame']),
       'Actual distinct Kano/Jax native airborne catch, timed release, living victim main63 and correctly owned damage')
  real_stores=[r for r in stores if start<=int(r['frame'])<end]
  need(len(real_stores)==1 and real_stores[0]['frame']==damage['frame']and int(real_stores[0]['slot'])==victim and
       int(real_stores[0]['before'])-int(real_stores[0]['after'])==(16 if kano else 32),
       'Air damage helper causes exactly one original health store, not a nominal action label')
  selected=[r for r in ev if r['kind']=='animation_lookup'and int(r['slot'])==victim and
            int(r['frame'])==int(lookup['frame'])and h(r,'a9')==63]
  need(len(selected)==1,'Main63 resolves through actual living victim animation root')
  need(any(r['kind']=='gate'and r['frame']==catch['frame']and int(r['slot'])==attacker for r in ev),
       'Physical airborne Block reaches original real input-event eligibility gate')
  need(all(any(r['kind']=='recovery'and int(r['slot'])==s and caught<int(r['frame'])<end for r in ev)for s in(1,2)),
       'Both actual native tasks execute recovery before readiness')
  callbacks=[r for r in ev if r['kind']=='victim_callback']
  if kano:
   flight=one('own_flight',victim);bounce=one('bounce',victim);ownland=one('own_landing',attacker)
   need(int(handoff['frame'])==int(release['frame'])and h(handoff,'a7')==0xfffff580 and
        int(flight['frame'])in(int(release['frame']),int(release['frame'])+1)and
        callbacks and all(int(r['slot'])==victim and h(r,'callback')==h(r,'a6')==0xfffff800 for r in callbacks)and
        [int(r['frame'])for r in callbacks]==list(range(int(flight['frame'])+1,int(land['frame'])+1))and
        int(bounce['y'])==int(bounce['floor'])and int(ownland['y'])==int(ownland['floor']),
        'Every consecutive actual Kano victim callback, native bounce/own landing and retirement at getup')
  else:
   flight=one('stock_flight',victim)
   need(not callbacks and not any(r['kind']in('own_flight','bounce','own_landing')for r in ev)and
        handoff['frame']==damage['frame']==flight['frame']and h(handoff,'a7')==0xff8da830,
        'Stock Jax takes original native living-victim flight, not the Kano custom path')
  # Check every declared physical input field. The capture logs actual pulses.
  for age in range(181):
   for s in(1,2):
    expected=(['Up']if age<3 else[])+(['Block']if s==attacker and 20<=age<26 else[])
    need(inputs[start+age,s]==expected,'Exact physical paired Up and attacker Block, no hidden extra move controls')
  walks=[];jumps=[];guards=[]
  for s in(1,2):
   direction='Right'if int(pre[begin,s]['x'])<int(pre[begin,3-s]['x'])else'Left'
   for age in range(161):
    expected=([direction]if age<8 else[])+(['Up']if 40<=age<43 else[])+(['High_Punch']if 112<=age<115 else[])+(['Block']if 136<=age<142 else[])
    need(inputs[begin+age,s]==expected,'Complete exact paired ordinary physical followup pulses')
   displacement=h(post[begin+18,s],'xraw')-h(pre[begin,s],'xraw')
   need(displacement!=0 and (displacement>0)==(direction=='Right'),'Ordinary real forward walk moves each recovered actor')
   walks.append(dict(slot=s,actualSignedRawXDisplacement=displacement))
   physics=[r for r in ev if r['kind']=='physics'and int(r['slot'])==s and begin<=int(r['frame'])<finish]
   need(len(physics)==1,'Exactly one real ordinary post-throw physics entry per actor');p=physics[0];at=int(p['frame'])
   need(at==begin+44 and tuple(h(p,k)for k in('a0','a1','a2','a3','a6','a9'))==(0,0xfff60000,0x8000,4,0,6),
        'Original normal vertical jump explicitly clears A6, not lingering callback execution')
   base=h(p,'yraw')
   for table,offset in((pre,2),(post,1)):
    for tick in range(1,39):
     r=table[at+offset+tick-1,s]
     need(h(r,'yraw')==(base-10*65536*tick+32768*tick*(tick+1)//2)&0xffffffff and
          h(r,'vy')==(-10*65536+tick*32768)&0xffffffff and h(r,'gravity')==32768 and
          h(r,'callback')==h(r,'vx')==0 and int(r['action'])==779,
          'Every fractional native normal jump tick, exact original integrator and callback reset in both pre/post streams')
   need(any(clean(post[f,s])for f in range(at+40,begin+112)),'Actual normal landing and stance before next punch')
   jumps.append(dict(slot=s,physicsFrame=at,originRawY=base,checkedPreTicks=38,checkedPostTicks=38,callbackResetProven=True))
   attack={int(post[f,s]['action'])for f in range(begin+112,begin+136)}
   need(attack&{257,276},'Actual native high punch or close elbow activates after air-throw recovery')
   guard={int(post[f,s]['action'])for f in range(begin+136,begin+156)}
   activated=1792 in guard
   if activated:guard_successes+=1
   else:
    ordinary=[r for r in stores if begin+112<=int(r['frame'])<begin+136 and int(r['slot'])==s]
    need(ids[s]==11 and len(ordinary)==1 and int(ordinary[0]['before'])-int(ordinary[0]['after'])==24 and
         1283 in guard and clean(pre[finish,s]),'Unsuccessful Jax guard pulse is real24damage interruption followed by native recovery, not credited as blocking')
    interrupted.append(dict(cycle=cycle,slot=s,nativeHealthStore=ordinary[0],observedActions=sorted(guard)))
   guards.append(dict(slot=s,actualGuardActivated=activated,observedNativeActions=sorted(guard)))
  cases.append(dict(cycle=cycle,attackerSlot=attacker,trueAttackerID=ids[attacker],livingVictimSlot=victim,trueVictimID=ids[victim],
                    catchFrame=caught,nativeAirDamage=16 if kano else 32,actualVictimCallbacks=len(callbacks),
                    fullyRecoveredFrame=end,ordinaryWalk=walks,exactOrdinaryJumps=jumps,ordinaryGuards=guards))
 need(all(clean(pre[ready+terminal,s])and clean(post[ready+terminal-1,s])for s in(1,2)),
      'Final paired native floor/stance/velocities/body/trail/suppression cleanup')
 expected_totals={side:64 if identity==18 else 32 if ids[3-side]==11 else 0,
                  3-side:48 if identity==18 else 51 if ids[3-side]==11 else 32}
 need(totals==expected_totals,'Entire actual air and ordinary-contact cumulative HP ledger')
 return dict(passed=True,trueIdentity=identity,physicalSlot=side,victim=b['victim'],stage=0,actualAirCycles=cases,
             completePreActorFields=len(pre),completePostActorFields=len(post),nativeHealthStores=len(stores),
             totalDamageByPhysicalSlot=totals,actualOrdinaryGuardActivations=guard_successes,interruptedGuardPulses=interrupted,
             actualKanoVictimCallbackInvocationRetirementAccepted=True,stockJaxCallbackInvocationLedgerAccepted=False,
             bothNormalJumpCallbackResetsAccepted=True,allGuardPulsesActivated=False,fullPortAcceptance=False)

def raw_scanner():
 source=inspect.getsource(stock.stock_raw_starts)
 before='graphic==0x0251f2dc and width==10 and height==48'
 need(source.count(before)==1,'One finite stock descriptor guard adaptation only')
 source=source.replace(before,'(graphic,width,height)in RAW',1)
 scope=dict(stock.stock_raw_starts.__globals__,RAW=RAW)
 exec(compile(source,__file__+'::entire_original_signed_header_scanner','exec'),scope)
 return scope['stock_raw_starts']

def bindings():
 body=contacts.earlier.physical.body;source=inspect.getsource(body.check)
 before='  if not c&128:\n'
 after="""  if not c&128 and (graphic,w,h)in RAW:
   decoded[key]=raw_starts(graphic,w,h,c,gfx,t)
   continue
  if not c&128:
"""
 need(source.count(before)==1,'Exact finite stock-only raw admission; all compressed and full source gates retained');source=source.replace(before,after,1)
 first=source.index(' # The older physical/ownership/health checker');last=source.index(" fields=rows['MK2_HPHASE_POST_FIELD']",first)
 source=source[:first]+" state=state_gate(b,guest,payload)\n entry_frames={int(r['frame'])for r in rows['MK2_BASIC_AIR_EVENT']if r['kind']=='action'}\n"+source[last:]
 before='ids={side:identity,3-side:4}'
 need(source.count(before)==1,'Only actual selected counterpart identity map changes');source=source.replace(before,"ids={side:identity,3-side:VID[b['victim']]}",1)
 scope=dict(body.check.__globals__,RAW=RAW,VID=VID,state_gate=state_gate,raw_starts=raw_scanner())
 exec(compile(source,__file__+'::whole_body_clip_fifo_shadow_source_projection_every_row','exec'),scope)
 return scope['check']

def load(fighter,side,victim):
 folder=ROOT/f'audit_v6049_air_{fighter}_p{side}_{victim}';path=ROOT/f'audit_v6050_air_{fighter}_p{side}_{victim}_observed/report.json'
 report=json.loads(path.read_text());need(report['passed']and report['nativeExit']==0 and report['candidate']==current.NAME and
   report['executableSHA256']==current.EXE_SHA and report['guestSHA256']==current.GUEST_SHA and report['payloadSHA256']==current.PAYLOAD_SHA,
   'Actual current matched executable/payload/guest terminal0 air capture')
 terminal=json.loads((folder/'native_terminal.json').read_text());process=json.loads((folder/'process.json').read_text())
 need(terminal['nativeExit']==0 and terminal['pid']==process['pid']==report['actualWindowsIdentity']['ProcessId']and
      terminal['actualWindowsIdentity']==process['actualWindowsIdentity']==report['actualWindowsIdentity'],
      'Terminal persisted before postassertions, bound to full actual Windows creation/executable/command identity')
 text=(folder/'run.log').read_text();need('hex='not in text and (folder/'stderr.log').read_text()==''and
   not re.search('LUA ERROR|stack traceback|fatal error|access violation|MK2_BASIC_FAILED',text,re.I),'No native/observer failure or raw-buffer persistence')
 rows=defaultdict(list)
 for line in text.splitlines():
  if line.startswith(('MK2_BASIC_','MK2_HPHASE_')):
   pairs=re.findall(r'(\w+)=([^\s]+)',line);need(len(pairs)==len(dict(pairs)),'Unique actual protocol fields');rows[line.split()[0]].append(dict(pairs))
 return dict(fighter=fighter,victim=victim,move='knife'if fighter=='kano'else'ring',side=side,folder=folder,
             report_path=path,report=report,rows=rows,streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()))

def run():
 prior=ROOT/'audit_v6036_current_native_contact_relocation_checked/report.json';p=json.loads(prior.read_text())
 need(p['passed']and all(sha(f)==v for f,v in p['inputHashes'].items()),'Complete previously accepted real close-contact and native source evidence intact')
 scanner=ROOT/'audit_v5316_original_stock_raw_shadow_scanner_source_checked/report.json';s=json.loads(scanner.read_text())
 need(s['passed']and s['originalUnconditionalHeaderAndSignedWidthAdvanceQualified']and all(sha(f)==v for f,v in s['inputHashes'].items()),
      'Whole independently disassembled original signed unconditional shadow scanner source still qualified')
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 pins={str(p):sha(p)for p in(Path(__file__).resolve(),prior,scanner)}
 body=contacts.earlier.physical.body;gfx=body.reconstruct(pins);own=current.expected_gfx()
 gfx[0x1fa0000:0x1fa0000+11944]=own[:11944];gfx[0x1fa4000:0x1fa4000+7032]=own[11944:]
 for header,magic in((0x1c0000,b'KFX1'),(0x1c1000,b'KPI1'),(0x1c2000,b'KPJ1'),(0x1d0000,b'KBL1')):
  need(payload[header:header+4]==magic,'Whole actual RAM GFX patch header');src,count,dest=struct.unpack_from('<III',payload,header+4)
  need(src+count<=len(payload)and dest+count<=len(gfx),'Independent full GFX payload patch source bound');gfx[dest:dest+count]=payload[src:src+count]
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in((0xff801070,0xff8017b0),(0xff804160,0xff804430),(0xff876650,0xff876b40),(0xff837900,0xff837be0)):
  need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==original[(lo-0xff800000)//8:(hi-0xff800000)//8],
       'Whole original native body/shadow/jump integration/guard kernels byte-exact')
 at=(0xff876860-0xff800000)//8
 need(guest[at:at+4]==bytes.fromhex('cdb29002'),'Original jump stores cleared A6 into shared main290; scalar retained pointer is not active execution')
 original_heights=struct.unpack_from('<17H',original,(0xff908010-0xff800000)//8)
 operand=(0xff907f70-0xff800000)//8;root=struct.unpack_from('<I',guest,operand)[0]
 need(struct.unpack_from('<19H',guest,(root-0xff800000)//8)==original_heights+(134,135),
      'All17 original floor anchors unchanged, appended own body extensions134/135')
 check=bindings();cases=[];faults=[]
 for fighter,side,victim in MATRIX:
  b=load(fighter,side,victim);case=check(b,guest,payload,gfx);case.update(fighter=fighter,victim=victim)
  need(case['unattributedOtherObjectShadowCopies']==0,'Every native shadow copy attributed; no silently excluded effect rows')
  for path,digest in b['report']['inputHashes'].items():need(sha(path)==digest,'All actual executed dependencies immutable');pins[path]=digest
  for path in(b['report_path'],*(f for f in b['folder'].rglob('*')if f.is_file())):pins[str(path)]=sha(path)
  for label,tag,key,value in(
    ('proxy_identity','MK2_HPHASE_POST_FIELD','id','1'),('wrong_floor','MK2_HPHASE_POST_FIELD','floor','999'),
    ('wrong_real_air_damage','MK2_BASIC_HEALTH','after','160'),('wrong_actual_callback','MK2_BASIC_AIR_EVENT','a6','01000000')):
   changed=copy.deepcopy(b)
   index=next(i for i,r in enumerate(changed['rows'][tag])if r.get('kind')=='physics')if label=='wrong_actual_callback'else 0
   row=changed['rows'][tag][index];need(row[key]!=value,'Actual state fault changes observed data');row[key]=value
   try:state_gate(changed,guest,payload)
   except ValueError as error:faults.append(dict(fighter=fighter,side=side,victim=victim,fault=label,rejectedBy=str(error)))
   else:raise ValueError('Actual state semantic fault accepted: '+label)
  for label,tag,key,value in(
    ('wrong_entry_body','MK2_HPHASE_CANDIDATE','source','00000000'),('wrong_shadow_owner','MK2_HPHASE_SHADOW_BEGIN','owner','01000000'),
    ('wrong_projection','MK2_HPHASE_PROJECTION','dy','999'),('wrong_native_shadow_row','MK2_HPHASE_SHADOW_DMA','source','00000001')):
   changed=copy.deepcopy(b);index=next(i for i,r in enumerate(changed['rows'][tag])if int(r['frame'])in case['actualRoutineEntryFrames'])if label=='wrong_entry_body'else 0
   row=changed['rows'][tag][index];need(row[key]!=value,'Actual body/shadow fault changes data');row[key]=value
   try:check(changed,guest,payload,gfx)
   except ValueError as error:faults.append(dict(fighter=fighter,side=side,victim=victim,fault=label,rejectedBy=str(error)))
   else:raise ValueError('Actual body/shadow semantic fault accepted: '+label)
  cases.append(case);print(f'{fighter} P{side} / {victim}: both actual air roles, exact paired normal jumps and every body/shadow row checked',flush=True)
 for path in(Path(body.__file__).resolve(),Path(contacts.__file__).resolve(),Path(stock.__file__).resolve(),ROOT/'tools/verify_move_phase_shadow_v5089.py'):
  pins[str(path)]=sha(path)
 need(all(sha(path)==v for path,v in pins.items()),'All actual native/failed/source/current/package evidence remains immutable')
 return dict(passed=True,candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,payloadSHA256=current.PAYLOAD_SHA,
  cases=cases,inputHashes=pins,actualSemanticFaultsRejected=faults,actualAirCatches=16,
  actualActorFields=sum(c['actualContiguousActorFields']for c in cases),nativeBodyCandidates=sum(c['actualNativeBodyCandidates']for c in cases),
  nativeShadowCopies=sum(c['actualSourceBoundShadowCopies']for c in cases),actualOrdinaryGuardActivations=sum(c['state']['actualOrdinaryGuardActivations']for c in cases),
  interruptedGuardPulses=sum(len(c['state']['interruptedGuardPulses'])for c in cases),exactPairedOrdinaryJumpTicks=8*2*2*38*2,
  wholePairedAirBodyGroundShadowCleanupAccepted=True,stockJaxCallbackInvocationLedgerAccepted=False,allGuardPulsesActivated=False,
  allArenaCPURepeatedKOOverlapAccepted=False,continuousWholeSceneRGBReplayAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False,
  fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable whole airborne qualification')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected','cases')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
