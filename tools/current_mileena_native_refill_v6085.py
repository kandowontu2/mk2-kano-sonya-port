"""Whole original Mileena state gate plus the actual original inter-round refill.

Do not delete FFFF health observations: qualify the complete native sentinel,
4..160 step-two refill, final161 store, exact writer PCs/owner/task/chronology.
"""
import inspect,struct
import current_payload_metadata_context_v5229 as current
import verify_mileena_fixed_runtime_v3829 as original
ROOT,need,sha=current.ROOT,current.need,current.sha

def refill(rows,side,guest):
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();lo,hi=0xff9dec90,0xff9def80
 need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==stock[(lo-0xff800000)//8:(hi-0xff800000)//8],
      'Entire actual original lifebar sentinel/step-two/final161 refill kernel unchanged')
 words={0xff9dec90:0x09c0,0xff9deca0:0xffff,0xff9ded80:0x188a,
        0xff9dee00:0x104a,0xff9dee20:0xff5e,0xff9dee50:0x00a1}
 need(all(struct.unpack_from('<H',guest,(at-0xff800000)//8)[0]==v for at,v in words.items()),
      'Independent source refill initial4/add2/upper161/fullFFFF sentinel constants')
 stores=[r for r in rows if r['tag']=='HEALTH'];start_pc=0xff9dece0 if side==1 else 0xff9ded10
 step_pc=0xff9def40 if side==1 else 0xff9def70
 starts=[(i,r)for i,r in enumerate(stores)if r['pc']==start_pc]
 need(len(starts)==1,'One actual original between-round refill, not arbitrary invalid health admission')
 index,start=starts[0];at=start['frame'];owner,task=start['a8'],start['a13']
 action=next(r for r in rows if r['tag']=='ACTION')
 need(owner==action['actor']and 0x01000000<=task<0x01100000 and
      start['before']==161 and start['after']==65535 and at<action['frame'],
      'Actual native winning actor/refill task and161-to-FFFF sentinel before fatality')
 values=list(range(4,161,2))+[161]
 consumed={index};previous=65535
 for age,value in enumerate(values):
  need(index+age+1<len(stores),'Complete actual refill store chain')
  r=stores[index+age+1]
  need(r['pc']==step_pc and r['frame']==at+age and r['before']==previous and r['after']==value and
       r['a8']==owner and r['a13']==task,
       'Every whole original refill store, previous health, writer PC, physical owner and exact native field')
  consumed.add(index+age+1);previous=value
 for i,r in enumerate(stores):
  need(r['pc']!=0xff838860 and(i in consumed or 0<=r['before']<=161 and 0<=r['after']<=161),
       'Every health observation is valid combat/reset or the fully source-qualified native refill; no cache stores')
 damage=[r for r in stores if r['pc']==0xff836700 and r['after']<r['before']<=161]
 kos=[r['frame']for r in damage if r['after']==0]
 need(len(kos)==2 and kos[0]<at<=at+len(values)-1<kos[1]<action['frame'],
      'Full original refill belongs strictly between the two collision-earned KOs')
 return dict(passed=True,startFrame=at,endFrame=at+len(values)-1,actualStores=len(consumed),
      actor=f'{owner:08X}',main=f'{task:08X}',completeNativeFFFFSentinelAndRefillAccepted=True)

def gate(rows,fighter,side,guest):
 proof=refill(rows,side,guest)
 source=inspect.getsource(original.gate)
 before="all(0<=r['before']<=161 and 0<=r['after']<=161 and r['pc']!=0xff838860 for r in health)"
 need(source.count(before)==1,'Only original bounded-health assertion gets complete source-native refill handling')
 source=source.replace(before,"refill(rows,side,guest)['passed']",1)
 scope=dict(original.gate.__globals__,refill=refill,guest=guest)
 exec(compile(source,__file__+'::entire_original_native_stream_and_cleanup_contract','exec'),scope)
 report=scope['gate'](rows,fighter,side);report['nativeInterRoundRefill']=proof
 return report
