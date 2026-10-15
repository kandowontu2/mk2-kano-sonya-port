"""Source-bound paired air-throw trajectories from the eight qualified native runs.

All16 initial paired jumps,10 Kano catch/hold/release/rebound/own-land cycles,
and6 stock Jax own-land/released-living-victim arcs. Every relevant pre/post
field, native instruction/event and fractional landing remainder retained.
No new native run, fitted curve, game write, generic artistic/CPU/arena claim.
Jax's callback invocation ledger and complete carry animation remain open.
"""
import copy,json,struct,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import qualify_current_air_throw_roles_v6051 as captured
import qualify_current_air_cooperative_handoff_v6059 as physical
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v6066_current_air_packed_shadow_checked/report.json'
OUT=ROOT/'audit_v6068_current_air_trajectories_checked'
MASK=0xffffffff
def h(r,k):return int(r[k],16)
def signed(v):return v-0x100000000 if v&0x80000000 else v
def off(at):return(at-0xff800000)//8
def raw_y(base,v,g,t):return(base+v*t+g*t*(t+1)//2)&MASK
def landing_tick(base,v,g,floor):
 for t in range(1,121):
  if signed(raw_y(base,v,g,t))//65536>=floor:return t
 raise ValueError('No natural bounded native landing from source velocity/gravity')

def source_contract(guest,payload):
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();cpp=ROOT/current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
 text=cpp.read_text()
 need('constexpr uint32_t air_poses[10] = {0xfe828e80,0xfe828ec0,0xfe828f00,'in text and
      'write16(kano_air_alignment + fighter * 4, 41);'in text and
      'write16(kano_air_alignment + fighter * 4 + 2, uint16_t(-3));'in text,
      'Frozen compiled own donor pose sequence and signed41/-3 catch alignment')
 need(all(struct.unpack_from('<hh',guest,0xf8080+i*4)==(41,-3)for i in range(19)),
      'Every source-generated real-ID Kano catch alignment row exactly41/-3')
 need(guest[0xffdc0:0xffdc0+17*4]==original[off(0xff8b7d20):off(0xff8b7d20)+17*4]and
      struct.unpack_from('<hhhh',guest,0xffdc0+17*4)==(10,-75,10,-75),
      'Stock Jax original17 alignment rows preserved; actual living Kano/Sonya rows10/-75')
 callback=(0x07a2,0x0220,0x0106,0x4848,0xca04,0x07a0,0x0ea0,0x0106,0xc003,
           0x07a0,0x02d0,0x0106,0x2a00,0xb501,0x0090,0x4020,0xb008,0x0090,0xc080)
 need(struct.unpack_from('<19H',guest,0xfff00)==callback and struct.unpack_from('<I',guest,0xfff00+38)[0]==0xfffc0880,
      'Whole actual callback reads correct player velocity, arithmetic-shifts16 and adds integer X before source-owned pose update')
 pose_groups=(0xff917270,0xff9269b0,0xff930a60,0xff93e270,0xff94de20,0xff94de20,0xff95c2e0,
              0xff96a8d0,0xff97ba70,0xff97ba70,0xff97ba70,0xff993090,0,0,0xff97ba70,0xff97ba70,
              0xff94de20,0xff00f8c0,0xff02f920)
 need(struct.unpack_from('<19I',guest,0xf8160)==pose_groups,'Whole independent native living-victim flight-art table, not proxy standing groups')
 for lo,hi in((0xff876650,0xff876b40),(0xff8da830,0xff8daa40),(0xff8b7f40,0xff8b7fa0)):
  need(guest[off(lo):off(hi)]==original[off(lo):off(hi)],'Complete original jump/stock-flight/Jax coupling instructions unchanged')
 need(struct.unpack_from('<I',guest,0xffeb0+24)[0]==0x30000 and struct.unpack_from('<I',guest,0xffeb0+30)[0]==0 and
      struct.unpack_from('<I',guest,0xffeb0+46)[0]==0xfffff800 and struct.unpack_from('<I',guest,0xffeb0+60)[0]==0xff876660,
      'Exact actual clone initial3pixel horizontal/zero vertical/native callback/no A6-clear entry')
 need(all(t in text for t in('0x09e0, 0xfc00, 0x0001','0x09e0, 0x0400, 0x0001',
      '0x09e1, 0x8000, 0xfffa','0x09e2, 0x7000, 0x0000')),
      'Actual compiled mirrored rebound signed velocities/-5.5 initialVY/.4375 gravity')
 return dict(passed=True,wholeOriginalIntegratorAndStockJaxCouplingByteExact=True,
             callbackIntegerXShiftAndLivingPoseTableSourceQualified=True,
             inputHashes={str(p):sha(p)for p in(cpp,ROOT/'mk2/mk2-maincpu.bin')})

def check(b,guest,payload):
 # Preserve the full actual field/identity/input/health/event/recovery gate;
 # earlier body/clip/source/shadow qualification is hash-bound in run().
 state=physical.state_gate(b,guest,payload);rows=b['rows']
 pre={(int(r['frame']),int(r['slot'])):r for r in rows['MK2_BASIC_FIELD']}
 post={(int(r['frame']),int(r['slot'])):r for r in rows['MK2_HPHASE_POST_FIELD']}
 cases=[];checked=0;callback_fields=0
 def phase(event,end,slot,vx,vy,g,callback=False,pose=None,next_phase=False):
  nonlocal checked
  at=int(event['frame']);x,y=h(event,'xraw'),h(event,'yraw');floor=int(pre[at,slot]['floor'])
  ticks=landing_tick(y,vy,g,floor)
  need(end-at==ticks,'Natural phase endpoint is the first original integer-floor crossing, not fitted to endpoint')
  integer_callback=(vx//65536)*65536 if callback else 0
  for tick in range(ticks+1):
   f=at+tick;r=post[f,slot];raw=raw_y(y,vy,g,tick)
   if tick==ticks:raw=(floor<<16)|(raw&65535)
   need(h(r,'xraw')==(x+(vx+integer_callback)*tick)&MASK and h(r,'yraw')==raw,
        'Every full fractional X/Y native trajectory and preserved landing low16 bits')
   if tick<ticks:
    need(h(r,'vx')==vx&MASK and h(r,'vy')==(vy+g*tick)&MASK and h(r,'gravity')==g and
         (not callback or h(r,'callback')==0xfffff800),'Complete actual phase velocities/gravity/attached callback, not position-only fit')
   elif not next_phase:
    need(h(r,'vx')==h(r,'vy')==h(r,'gravity')==0,'Actual original landing resets all motion; pointer-null not required')
   if pose is not None and tick>0:need(h(r,'pose')==pose,'Every living-victim horizontal knockdown pose, including landing')
   checked+=1
   if tick>0:
    prior=post[f-1,slot];current=pre[f,slot]
    need(all(current[k]==prior[k]for k in('xraw','yraw','vx','vy','gravity','callback','pose')),
         'Every paired pre callback continues exact previous completed draw, no dropped boundary field')
    checked+=1
  return dict(physicsFrame=at,landingFrame=end,slot=slot,sourceInitialVX=vx,sourceInitialVY=vy,sourceGravity=g,
              fullNativeTicks=ticks,callbackIntegerExtraX=integer_callback,landingRawY=h(post[end,slot],'yraw'))
 for cycle,step in enumerate(rows['MK2_BASIC_STEP'],1):
  ev=[r for r in rows['MK2_BASIC_AIR_EVENT']if int(r['cycle'])==cycle and r['driver']=='execute']
  def event(kind,slot):
   found=[r for r in ev if r['kind']==kind and int(r['slot'])==slot]
   need(len(found)==1,'One complete genuine trajectory boundary '+kind);return found[0]
  attacker=int(step['attacker']);victim=3-attacker;catch=event('action',attacker);caught=int(catch['frame']);kano=int(catch['id'])==17
  start=int(step['frame']);direction=1 if h(pre[start,attacker],'xraw')<h(pre[start,victim],'xraw')else-1
  initial=[]
  for s in(1,2):
   jump=next(r for r in ev if r['kind']=='physics'and int(r['slot'])==s and int(r['frame'])==start+4)
   at=int(jump['frame']);base=h(jump,'yraw');x=h(jump,'xraw')
   need(tuple(h(jump,k)for k in('a0','a1','a2','a6'))==(0,0xfff60000,0x8000,0),
        'Both actual initial normal vertical jump arguments and cleared callback')
   for tick in range(1,18):
    for table,f in((post,at+tick),(pre,at+tick+1)):
     r=table[f,s];need(h(r,'yraw')==raw_y(base,-10*65536,32768,tick)and h(r,'xraw')==x and
       h(r,'vy')==(-10*65536+32768*tick)&MASK and h(r,'gravity')==32768 and h(r,'callback')==0,
       'Every source-derived pre-catch fractional paired jump tick');checked+=1
   if s==attacker:need(h(catch,'yraw')==raw_y(base,-10*65536,32768,18),
      'Actual catch instruction executes at exact18th native jump tick before any role-specific Y adjustment')
   initial.append(dict(slot=s,physicsFrame=at,preAndPostTicks=17,originRawY=base))
  phases=[]
  if kano:
   release=event('early_release',attacker);flight=event('own_flight',victim);bounce=event('bounce',victim)
   getup=event('victim_getup',victim);own_land=event('own_landing',attacker)
   need(h(flight,'xraw')==(h(catch,'xraw')+direction*41*65536)&MASK and
        h(flight,'yraw')==(h(catch,'yraw')-3*65536)&MASK,'Whole signed source41/-3 catch alignment, including fractional position')
   for f in range(caught,caught+26):
    r=post[f,attacker];age=f-caught;pose=0xfe828e80 if age<8 else 0xfe828ec0 if age<10 else 0xfe828f00
    need(h(r,'pose')==pose and int(r['action'])==265 and h(r,'xraw')==h(catch,'xraw')and
         h(r,'yraw')==h(catch,'yraw')and h(r,'vx')==h(r,'vy')==h(r,'gravity')==0 and
         h(r,'flags')&16 and h(r,'body')&4,'All26 source-owned catch/throw pose holds, motion freeze and native temporary flags')
    checked+=1
   physics=[r for r in ev if r['kind']=='physics']
   need(len(physics)==5,'Exactly two initial jumps plus victim flight/rebound/own fall; no unobserved extra physics branch')
   first=next(r for r in physics if int(r['slot'])==victim and r['frame']==flight['frame'])
   rebound=next(r for r in physics if int(r['slot'])==victim and r['frame']==bounce['frame'])
   ownfall=next(r for r in physics if int(r['slot'])==attacker and int(r['frame'])>caught)
   need(tuple(h(first,k)for k in('a0','a1','a2','a6'))==(0x30000,0,0xa000,0xfffff800)and
        tuple(h(rebound,k)for k in('a0','a1','a2','a6'))==
         (0x1fc00 if victim==2 else 0x10400,0xfffa8000,0x7000,0xfffff800)and
        tuple(h(ownfall,k)for k in('a0','a1','a2','a6'))==(0,0x20000,0x6000,0)and
        int(ownfall['frame'])==caught+32,'All three actual distinct source-defined physics argument sets and own fall cadence')
   pose=struct.unpack_from('<I',guest,0xf8160+int(flight['id'])*4)[0]
   phases.append(phase(first,int(bounce['frame']),victim,direction*0x30000,0,0xa000,True,pose,True))
   vx=0x1fc00 if victim==2 else-0x10400
   phases.append(phase(rebound,int(getup['frame']),victim,vx,-0x58000,0x7000,True,pose))
   phases.append(phase(ownfall,int(own_land['frame']),attacker,0,0x20000,0x6000))
   callbacks=[r for r in ev if r['kind']=='victim_callback']
   for r in callbacks:
    f=int(r['frame']);current=pre[f,victim];vx=signed(h(current,'vx'));g=h(current,'gravity')
    need(h(r,'xraw')==(h(current,'xraw')+vx)&MASK and
         h(r,'yraw')==(h(current,'yraw')+signed(h(current,'vy'))+g)&MASK and
         h(r,'callback')==h(r,'a6')==0xfffff800,
         'Every callback actually executes after native full motion and before signed-integer extra X/pose update')
    callback_fields+=1
  else:
   need(int(catch['id'])==11 and h(post[caught,attacker],'yraw')==(h(catch,'yraw')+32*65536)&MASK and
        h(post[caught,victim],'xraw')==(h(catch,'xraw')+direction*10*65536)&MASK and
        h(post[caught,victim],'yraw')==(h(post[caught,attacker],'yraw')-75*65536)&MASK,
        'Original Jax-only32pixel lowering and actual living own-ID10/-75 catch alignment')
   physics=[r for r in ev if r['kind']=='physics'];need(len(physics)==4,'Exactly both initial jumps, originalJax fall and released living-victim flight')
   ownfall=next(r for r in physics if int(r['slot'])==attacker and int(r['frame'])>caught)
   victimfall=next(r for r in physics if int(r['slot'])==victim and int(r['frame'])>caught)
   release=event('early_release',attacker);getup=event('victim_getup',victim)
   need(int(ownfall['frame'])==caught+6 and tuple(h(ownfall,k)for k in('a0','a1','a2','a6'))==(0,0x20000,0xa000,0xff8b7f40)and
        tuple(h(victimfall,k)for k in('a0','a1','a2','a6'))==(0x38000,0xfff80000,0xa000,0),
        'Original Jax fall/coupling argument and unmodified original living-victim flight arguments')
   phases.append(phase(ownfall,int(release['frame']),attacker,0,0x20000,0xa000))
   phases.append(phase(victimfall,int(getup['frame']),victim,-direction*0x38000,-0x80000,0xa000))
  cases.append(dict(cycle=cycle,trueAttackerID=int(catch['id']),attackerSlot=attacker,victimSlot=victim,
                    initialPairedJumps=initial,completeCheckedSourcePhases=phases,ownKanoHoldAccepted=kano,
                    exactSourceIntegerCallbackFields=len([r for r in ev if r['kind']=='victim_callback'])))
 return dict(passed=True,fighter=b['fighter'],side=b['side'],victim=b['victim'],cases=cases,
             checkedPreAndPostTrajectoryFields=checked,actualSourceIntegerCallbackFields=callback_fields,
             completeJaxCarryAnimationAndInvocationLedgerAccepted=False,fullPortAcceptance=False)

def mutated(b,tag,index,key,value):
 result=dict(b);result['rows']=dict(b['rows']);result['rows'][tag]=list(b['rows'][tag]);row=dict(result['rows'][tag][index])
 need(row[key]!=value,'Actual trajectory fault changes native record');row[key]=value;result['rows'][tag][index]=row
 return result

def run():
 parent=json.loads(PARENT.read_text());need(parent['passed']and parent['wholePairedAirBodyGroundShadowCleanupAccepted']and
   len(parent['cases'])==8 and parent['actualAirCatches']==16 and len(parent['actualSemanticFaultsRejected'])==65 and
   all(sha(p)==v for p,v in parent['inputHashes'].items()),'Whole actual state/body/clip/source/shadow matrix and all faults retained byte-identical')
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes();source=source_contract(guest,payload)
 pins=dict(source['inputHashes']);pins[str(PARENT)]=sha(PARENT);pins[str(Path(__file__).resolve())]=sha(__file__)
 cases=[];faults=[]
 for fighter,side,victim in captured.MATRIX:
  b=captured.load(fighter,side,victim);case=check(b,guest,payload);cases.append(case)
  catch=next(r for r in b['rows']['MK2_BASIC_AIR_EVENT']if r['kind']=='action');cycle=1;attacker=int(catch['slot'])
  ev=[r for r in b['rows']['MK2_BASIC_AIR_EVENT']if r['cycle']=='1'and r['driver']=='execute']
  role=next(r for r in ev if r['kind']=='own_flight')if int(catch['id'])==17 else next(r for r in ev if r['kind']=='stock_flight')
  f=int(role['frame'])+2;s=int(role['slot']);post=b['rows']['MK2_HPHASE_POST_FIELD']
  index=next(i for i,r in enumerate(post)if(int(r['frame']),int(r['slot']))==(f,s))
  tests=[('one_bit_native_flight_X','xraw',f'{h(post[index],"xraw")^1:08X}'),
         ('one_bit_native_flight_Y','yraw',f'{h(post[index],"yraw")^1:08X}'),
         ('wrong_actual_flight_VY','vy',f'{h(post[index],"vy")^1:08X}'),
         ('wrong_actual_phase_gravity','gravity',f'{h(post[index],"gravity")^1:08X}')]
  for label,key,value in tests:
   changed=mutated(b,'MK2_HPHASE_POST_FIELD',index,key,value)
   try:check(changed,guest,payload)
   except ValueError as error:faults.append(dict(fighter=fighter,side=side,victim=victim,fault=label,rejectedBy=str(error)))
   else:raise ValueError('Actual native trajectory fault accepted: '+label)
  for p,hsh in b['report']['inputHashes'].items():need(sha(p)==hsh,'Every actual capture source immutable');pins[p]=hsh
  for p in(b['report_path'],b['folder']/'run.log'):pins[str(p)]=sha(p)
  print(f'{fighter} P{side}/{victim}: complete source-defined airborne arcs and four actual one-bit phase faults checked',flush=True)
 for p in(Path(captured.__file__).resolve(),Path(physical.__file__).resolve(),ROOT/'tools/verify_restart_airthrow.py'):
  pins[str(p)]=sha(p)
 need(all(sha(p)==v for p,v in pins.items()),'All source/native/accepted/failed evidence immutable')
 return dict(passed=True,candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,payloadSHA256=current.PAYLOAD_SHA,
             parentWholeStateBodyShadowProof=str(PARENT),sourceQualification=source,cases=cases,inputHashes=pins,actualSemanticFaultsRejected=faults,
             trueKanoAirCycles=10,stockJaxLivingOwnVictimCycles=6,actualAirCatches=16,
             checkedPreAndPostTrajectoryFields=sum(c['checkedPreAndPostTrajectoryFields']for c in cases),
             actualSourceIntegerCallbackFields=sum(c['actualSourceIntegerCallbackFields']for c in cases),
             nativeFractionalTrajectoriesAndFloorClampsAccepted=True,completeJaxCarryAnimationAndInvocationLedgerAccepted=False,
             fullArtAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,rawMediaFilesWritten=0,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable whole current-air trajectory proof')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','actualSemanticFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
