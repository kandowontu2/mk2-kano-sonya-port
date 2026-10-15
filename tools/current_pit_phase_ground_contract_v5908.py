"""Whole5903 successor: source-native Pit victim floor relocation, not Tomb.

The executed5903failure is preserved. Original Pit reads Main+200, adds400h
and stores Main+200 before its native launch. Require that exact program and
every completed body/queued transform before and after it; never permit an
arbitrary floor offset. All2107movie/2136fault/continuous/shadow gates stay.
"""
import hashlib,inspect,struct
from collections import defaultdict
from types import SimpleNamespace
import current_pit_scene_contract_v5903 as previous
need,ROOT=previous.need,previous.ROOT
source_graphics=previous.source_graphics
native_gate=previous.native_gate
movie_faults=previous.movie_faults
native=previous.native

def phase_ground(scene,guest,side):
 groups=scene.groups;stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 off=lambda a:(a-0xff800000)//8
 need(guest[off(0xff8eb490):off(0xff8eba10)]==stock[off(0xff8eb490):off(0xff8eba10)],
      'Entire original Pit predecessor/one-tick yield/floor relocation/launch program')
 words=(0xb5a0,0x200,0x0b00,0x400,0xb00d,0x200)
 need(guest[off(0xff8eb830):off(0xff8eb890)]==stock[off(0xff8eb830):off(0xff8eb890)]==struct.pack('<6H',*words),
      'Exact original Main+200 read, ADDI400h and Main+200 store')
 bodies=groups['FLOOR_BODY'];physical=[b for b in bodies if b['slot']in(1,2)]
 phases={p['frame']:p for p in groups['FLOOR_PHASE']}
 anchors={17:134,18:135};victim=3-side
 voice=[r for r in groups['FLOOR_PIT_NATIVE']if r['entry']==0xffa12530 and r['a0']==0x1b]
 mode=[r for r in groups['FLOOR_PIT_MODE_STORE']if r['value']==9]
 need(len(voice)==len(mode)==1 and voice[0]['frame']==mode[0]['frame']+1,
      'Original one-tick Pit yield precedes physical victim launch cue')
 launch=voice[0]['frame'];frames={s:[]for s in(1,2)}
 for b in physical:
  s=b['slot'];frames[s].append(b['frame']);p=phases[b['frame']]
  relocated=s==victim and b['frame']>=launch
  wanted=p['stageY']-anchors[b['id']]+(1024 if relocated else 0)
  need(b['floor']==wanted and (not relocated or b['action']==0x503),
       'Every completed physical floor equals original standing anchor or exact native launched-victim400h phase')
  if s==victim:need(b['actor']==voice[0]['a8'] and b['main']==voice[0]['a13'],
                    'Only the actual physical victim owns original floor relocation')
 first=groups['FLOOR_BEGIN'][0]['origin'];retired=groups['FLOOR_PHYSICAL_RETIRED'][0]['frame']
 need(all(frames[s]==list(range(first,retired))for s in(1,2)),
      'Every completed physical floor field before native pointer retirement')
 queue={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']}
 physical_queues=0
 for t in groups['FLOOR_QUEUE_TRANSFORM']:
  q=queue[t['frame'],t['cursor']]
  if q['slot']not in(1,2):continue
  # FIFO publication precedes the same field's completed native floor store.
  relocated=q['slot']==victim and q['frame']>launch
  wanted=t['stageY']-anchors[q['id']]+(1024 if relocated else 0)
  need(t['floor']==q['floor']==wanted,
       'Every physical FIFO floor is exact standing or native launched400h phase, with original publication ordering')
  physical_queues+=1
 return dict(passed=True,actualNativeLaunchFloorStoreFrame=launch,standingAnchors=anchors,
             originalVictimFloorDisplacement=1024,completedPhysicalFloorFields=len(physical),
             physicalFloorBoundProjections=physical_queues,originalProgramWords=words)

def ground_faults(scene,guest,side):
 positive=phase_ground(scene,guest,side);rejected=[]
 def reject(label,changed,code=guest):
  try:phase_ground(changed,code,side)
  except ValueError as error:rejected.append(dict(label=label,rejectedBy=str(error)))
  else:raise ValueError('Actual native Pit floor corruption accepted '+label)
 for address,label in ((0xff8eb830,'floor read opcode'),(0xff8eb860,'native400h addition'),
                       (0xff8eb880,'floor store offset')):
  altered=bytearray(guest);altered[(address-0xff800000)//8]^=1
  reject(label,scene,bytes(altered))
 def copied():return SimpleNamespace(groups=defaultdict(list,{k:[dict(r)for r in rows]for k,rows in scene.groups.items()}))
 bad=copied();next(r for r in bad.groups['FLOOR_BODY']if r['slot']==3-side and
                  r['frame']==positive['actualNativeLaunchFloorStoreFrame'])['floor']+=1
 reject('one-pixel shifted launched victim floor',bad)
 bad=copied();bad.groups['FLOOR_BODY'].remove(next(r for r in bad.groups['FLOOR_BODY']if r['slot']==side))
 reject('omitted completed standing floor field',bad)
 bad=copied();q=next(q for q in bad.groups['FLOOR_QUEUE']if q['slot']==side)
 q['floor']+=1
 reject('one-pixel shifted standing FIFO floor',bad)
 need(len(rejected)==6 and phase_ground(scene,guest,side)==positive,'Whole phase floor positive restored after six actual faults')
 return rejected

source=inspect.getsource(previous.scene_contract)
before=""" anchors={17:134,18:135}
 for t in groups['FLOOR_QUEUE_TRANSFORM']:
  q=queue[t['frame'],t['cursor']]
  if q['slot'] in (1,2):need(t['floor']==q['floor']==t['stageY']-anchors[q['id']],
                             'Physical own native ground anchor remains aligned before cinematic retirement')
"""
need(source.count(before)==1,'One explicit wrongly Tomb-style all-phase floor predicate')
source=source.replace(before," ground=phase_ground(scene,guest,side)\n ground_faults_rejected=ground_faults(scene,guest,side)\n",1)
before=""" need([r['frame']for r in scene.records]==expected and scene.pre_count==len(groups['FLOOR_PRE_FRAME']) and
      scene.flip_count==len(groups['FLOOR_LATCH']) and scene.loads==scene.fills>0 and
      not scene.events and not scene.raw and not scene.rgb and len(scene.counterexamples)==2,
      'Every one-base continuous CPU/DMA/shift/VRAM/palette/RGB field and actual pixel faults retained')
"""
need(source.count(before)==1,'Entire earlier live continuity/negative-fault predicate identified')
# The actual5907failure occurs after this whole predicate succeeds. The
# retrospective path binds the unchanged executed source and that precise
# later error, rather than fabricating raw buffers or negative-test records.
source=source.replace(before,""" need([r['frame']for r in scene.records]==expected,'Every original actual completed scene field retained')
 if getattr(scene,'retainedLivePipelinePassedBeforeErroneousGroundGate',False):
  need(scene.retainedLiveActualPixelFaultGateCompleted and scene.allActualTransportDigestsVerified,
       'Entire earlier live continuity and actual negative/restoration gates succeeded before preserved later post-gate failure')
 else:
"""+'\n'.join(' '+line for line in before.rstrip().splitlines())+'\n',1)
before=" proof.update(nativeShadowCopies=shadows['checked_copies'],actualMovieFaultsRejected=faults,"
need(source.count(before)==1,'Whole original movie/shadow proof output')
source=source.replace(before," proof.update(actualNativePhaseGround=ground,actualNativePhaseGroundFaultsRejected=ground_faults_rejected,nativeShadowCopies=shadows['checked_copies'],actualMovieFaultsRejected=faults,",1)
scope=dict(vars(previous),phase_ground=phase_ground,ground_faults=ground_faults)
exec(compile(source,__file__+'::whole5903_source_native_Pit_floor_phase','exec'),scope)
scene_contract=scope['scene_contract']
CONTRACT_SOURCE_SHA256=hashlib.sha256(source.encode()).hexdigest().upper()
