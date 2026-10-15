"""Current living Kano/Sonya carried-victim choreography in six original Jax throws.

All carried fields, full fixed-point coupling and source-native animation XY
commands are checked through the actual cooperative free-flight handoff. Keep
the whole current air trajectory and paired body/shadow proof hash-bound.
The callback's invocation trace was not recorded: only its source and every
observed coupling effect are qualified, not a fabricated invocation ledger.
"""
import json,struct,traceback
from pathlib import Path
import qualify_current_air_native_phase_scope_v6071 as phase
import qualify_current_air_native_landing_v6069 as native
ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v6072_current_air_native_phase_scope_checked/report.json'
OUT=ROOT/'audit_v6076_current_jax_carried_victims_checked'
MATRIX=(('kano',1),('kano',2),('sonya',1),('sonya',2))
MASK=0xffffffff

def short(v):return(v&65535)-65536 if v&32768 else v&65535
def sequence(at,guest,payload):
 result=[];dx=dy=0
 for i in range(20):
  value=native.word(at,guest,payload);at+=32
  if value==0:return result,at
  if value==4:
   xy=native.word(at,guest,payload);at+=32
   dx+=short(xy);dy+=short(xy>>16)
  else:
   need(value>9,'Only actually represented source-native picture/XY commands')
   result.append(dict(pose=value,dx=dx,dy=dy));dx=dy=0
 raise ValueError('Unterminated original bounded carried-animation sequence')

def root_sequence(table,identity,animation,guest,payload):
 root=native.word(table+identity*32,guest,payload)
 return sequence(native.word(root+animation*32,guest,payload),guest,payload)

def source_contract(guest,payload):
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in((0xff8b6ff0,0xff8b7400),(0xff8b7430,0xff8b7520),
               (0xff8b7560,0xff8b7650),(0xff8b7680,0xff8b7a70),
               (0xff8b7ac0,0xff8b7b40),(0xff8b7f40,0xff8b7fa0),
               (0xff842480,0xff842710),(0xff83cc20,0xff83cd50),
               (0xff8319d0,0xff831ac0)):
  need(guest[native.prior.off(lo):native.prior.off(hi)]==original[native.prior.off(lo):native.prior.off(hi)],
       'Whole original carried-throw/coupling/peer-draw/XY/stop kernels unchanged outside explicitly qualified ID routers')
 need(native.word(0xfffe4400+11*32,guest,payload)==
      struct.unpack_from('<I',original,native.prior.off(0xff906370)+11*4)[0],
      'Jax secondary pose root remains the original character root, not an own-ID replacement')
 own,_=root_sequence(0xfffe4400,11,5,guest,payload)
 need([r['pose']for r in own]==[0xff997400,0xff997480,0xff997520,0xff9975a0,0xff9975a0,0xff9975a0]and
      all(r['dx']==r['dy']==0 for r in own),'Full original six-frame Jax carry/throw poses')
 victims={}
 for identity in(17,18):
  first,at=root_sequence(0xfffe4000,identity,63,guest,payload)
  second,_=sequence(at,guest,payload)
  need(len(first)==5 and len(second)==2 and [r['dy']for r in first]==[0,10,48,0,0]and
       all(r['dx']==0 for r in first+second)and all(r['dy']==0 for r in second)and
       first[0]['pose']==first[1]['pose']==first[2]['pose']and
       [r['pose']for r in second]==[first[3]['pose'],first[0]['pose']],
       'Complete true own-ID main63 carry/release stream and signed source offsets, not observed pose fitting')
  victims[identity]=dict(first=first,second=second)
 return dict(own=own,victims=victims,callbackCopiesWholePeerVY=True,
             actualCallbackInvocationLedgerAccepted=False)

def check(b,guest,payload,source):
 # Complete current living identities/input/health/recovery and free-flight
 # phases retained; body/clip/all shadow rows are pinned through the parent.
 whole=phase.check(b,guest,payload)
 rows=b['rows'];pre={(int(r['frame']),int(r['slot'])):r for r in rows['MK2_BASIC_FIELD']}
 post={(int(r['frame']),int(r['slot'])):r for r in rows['MK2_HPHASE_POST_FIELD']}
 cases=[];fields=0
 for cycle in(1,2):
  events=[r for r in rows['MK2_BASIC_AIR_EVENT']if int(r['cycle'])==cycle and r['driver']=='execute']
  catch=next(r for r in events if r['kind']=='action')
  if int(catch['id'])!=11:continue
  at=int(catch['frame']);att=int(catch['slot']);victim=3-att;identity=int(post[at,victim]['id'])
  flight=next(r for r in events if r['kind']=='stock_flight');end=int(flight['frame'])
  need(end-at in(34,35),'Original damage34 handoff runs actual peer in same/next cooperative field')
  initial=native.prior.h(post[at,victim],'yraw');x=native.prior.h(post[at,victim],'xraw')
  first=source['victims'][identity]['first'];second=source['victims'][identity]['second']
  for age in range(end-at+1):
   f=at+age;r=post[f,victim];own=post[f,att]
   # Callback copies new ownVY after global motion; the victim therefore
   # moves using the previous completed field's copied speed. At own landing
   # both are stopped by the original peer-stop helper before next motion.
   k=min(max(age-6,0),11);n=max(k-1,0)
   y=(initial+0x20000*n+0xa000*n*(n+1)//2+
      (first[1]['dy']*65536 if age>=19 else 0)+
      (first[2]['dy']*65536 if age>=21 else 0))&MASK
   need(native.prior.h(r,'yraw')==y and native.prior.h(r,'xraw')==x,
        'Every full fractional carried-victim XY tick and both actual source-command offsets')
   if age<end-at:
    vy=0x20000+0xa000*k if 7<=age<17 else 0
    need(native.prior.h(r,'vy')==vy and native.prior.h(r,'vx')==0 and native.prior.h(r,'gravity')==0,
         'Every observed peer copied-speed/zero-gravity/carry-stop field')
   if age<23:picture=first[0]['pose']
   elif age<25:picture=first[3]['pose']
   elif age<30:picture=first[4]['pose']
   elif age<32:picture=second[0]['pose']
   elif f<end:picture=second[1]['pose']
   else:picture=first[4]['pose']
   need(native.prior.h(r,'pose')==picture,'Every own-ID carried, paired-release and native free-flight first picture')
   own_index=0 if age<17 else 1 if age<19 else 2 if age<21 else 3
   need(native.prior.h(own,'pose')==source['own'][own_index]['pose']and int(own['action'])==265 and
        native.prior.h(own,'flags')&16 and native.prior.h(own,'body')&4,
        'Every original Jax frozen/coupled-fall/paired-release picture and native action flags')
   fields+=2
   if age>0:
    for slot in(att,victim):
     need(all(pre[f,slot][key]==post[f-1,slot][key]for key in('xraw','yraw','vx','vy','gravity','pose')),
          'Every original paired carry pre/post continuation, no omitted fractional or pose boundary')
     fields+=1
  cases.append(dict(cycle=cycle,attackerID=11,attackerSlot=att,trueLivingVictimID=identity,
      catchFrame=at,freeFlightFrame=end,sourceFirstVictimPose=f'{first[0]["pose"]:08X}',
      nativeCommandYOffsets=[first[1]['dy'],first[2]['dy']],sourceReleaseRawY=y))
 return dict(passed=True,fighter=b['fighter'],side=b['side'],cases=cases,
      pairedCarryPreAndPostFields=fields,wholeEarlierAirTrajectoryGateRetained=whole['passed'],
      actualCallbackInvocationLedgerAccepted=False,fullPortAcceptance=False)

def run():
 parent=json.loads(PARENT.read_text())
 need(parent['passed']and parent['actualAirCatches']==16 and len(parent['actualSemanticFaultsRejected'])==48 and
      all(sha(p)==v for p,v in parent['inputHashes'].items()),'Actual complete current air/state/body/shadow parent immutable')
 guest=native.prior.current.expected();payload=(ROOT/native.prior.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 source=source_contract(guest,payload);cases=[];faults=[];pins=dict(parent['inputHashes'])
 for fighter,side in MATRIX:
  b=native.prior.captured.load(fighter,side,'jax');cases.append(check(b,guest,payload,source))
  event=next(r for r in b['rows']['MK2_BASIC_AIR_EVENT']if r['kind']=='action'and r['id']=='11')
  at=int(event['frame']);victim=3-int(event['slot']);att=3-victim;post=b['rows']['MK2_HPHASE_POST_FIELD']
  for age,slot,key,label in((8,victim,'vy','wrong_whole_copied_VY'),(8,victim,'yraw','wrong_fractional_carried_Y'),
      (19,victim,'yraw','wrong_first_native_XY_offset'),(21,victim,'yraw','wrong_second_native_XY_offset'),
      (23,victim,'pose','wrong_true_victim_release_pose'),(17,att,'pose','wrong_original_Jax_release_pose')):
   index=next(i for i,r in enumerate(post)if(int(r['frame']),int(r['slot']))==(at+age,slot))
   changed=native.prior.mutated(b,'MK2_HPHASE_POST_FIELD',index,key,f'{native.prior.h(post[index],key)^1:08X}')
   try:check(changed,guest,payload,source)
   except ValueError as error:faults.append(dict(fighter=fighter,side=side,fault=label,rejectedBy=str(error)))
   else:raise ValueError('Actual carried-actor semantic corruption accepted: '+label)
  print(f'{fighter} P{side}: full original carried-victim choreography and six actual negative controls checked',flush=True)
 for p in(PARENT,Path(__file__).resolve(),Path(phase.__file__).resolve(),Path(native.__file__).resolve()):pins[str(p)]=sha(p)
 need(sum(len(r['cases'])for r in cases)==6 and len(faults)==24 and all(sha(p)==v for p,v in pins.items()),
      'All six current living-victim carries,24 actual faults and source hashes intact')
 return dict(passed=True,candidate=native.prior.current.NAME,cases=cases,sourceQualification=source,
      actualJaxLivingOwnVictimCycles=6,pairedCarryPreAndPostFields=sum(r['pairedCarryPreAndPostFields']for r in cases),
      inputHashes=pins,actualSemanticFaultsRejected=faults,wholeObservedCarriedVictimChoreographyAccepted=True,
      actualCallbackInvocationLedgerAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False,
      fullPortAcceptance=False,nativeGameChanges=0,newNativeBoots=0,rawMediaFilesWritten=0,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable original carried-victim qualification')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','actualSemanticFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
