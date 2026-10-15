"""Native missed Ring: retain original release/lock ledger, distinct flight branch.

Do not substitute the original hit contract or hide a missing impact. Check
every actual flight field and zero owned damage, retirement before recovery,
plus existing complete match/choice/leg/compound state and health evidence.
"""
import inspect,struct
import native_repeated_cpu_ring_contract_v2970 as prior
import verify_current_cpu_leg_square_compound_v6282 as compound
import verify_native_cpu_ring_v2971 as phase

ROOT,need=phase.ROOT,phase.need


def ring_gate(text,guest):
 source=inspect.getsource(prior.verify)
 stop=source.index("    hp=one([r for r in stream.overlap.rows(log,'HEALTH')")
 source=source[:stop]+'''    return dict(start=start,actor=actor,main=main,birth=birth,end=end,child=child,process=process,
                victim=victim,vmain=vmain,ready=ready['frame'],by=by,ring=ring,flags=flags)
'''
 scope=dict(prior.__dict__)
 exec(compile(source,__file__+'::whole_original_parent_release_and_complete_lock_ledger','exec'),scope)
 base=scope['verify'](text,guest,'kano')
 start,birth,end,ready=(base[k]for k in('start','birth','end','ready'))
 child,process=base['child'],base['process'];parent=base['ring'];by=base['by']
 need(birth<end<ready and ready==start+50,'Actual miss child retires before independent original parent recovery')
 children=phase.overlap.rows(text,'CHILD_FIELD')
 need([r['frame']for r in children]==list(range(birth+1,end+1)),'Every miss child callback through actual retirement')
 events=phase.overlap.rows(text,'EVENT');groups=[r for r in events if r['kind']=='group']
 sign=-1 if by[start+1]['facing']&0x10 else 1
 travel=[r for r in groups if r['a8']==child]
 need([r['frame']for r in travel]==list(range(start+16,end,3)) and
      [r['a0']for r in travel]==[prior.original.FLIGHT[18][i%4]for i in range(len(travel))],
      'All cyclic original flight groups and holds; no invented miss-impact poses')
 for i,row in enumerate(travel):
  need((row['a8'],row['a13'],row['main_owner'],row['shot_owner'],row['pc'])==
       (child,process,child,base['actor'],0xff8387a0) and row['vx']==(sign*0x80000)&0xffffffff and
       row['xraw']==(parent['xraw']+sign*(1+i*3)*0x80000)&0xffffffff and row['yraw']==parent['yraw'],
       'Every actual native flight publication owner and fixed-point motion')
 for row in children:
  age=row['frame']-birth-1
  need((row['actor'],row['main'],row['owner'],row['shot_owner'],row['id'],row['type'],row['parameter'])==
       (child,process,child,base['actor'],18,81,0x80000) and row['action']==0 and row['vy']==0 and
       row['pose']==prior.original.FLIGHT[18][max(0,(age-1)//3)%4] and
       row['xraw']==(parent['xraw']+sign*age*0x80000)&0xffffffff and row['yraw']==parent['yraw'] and
       row['vx']==(sign*0x80000)&0xffffffff and row['child_cycle']==parent['cycle'] and row['child_serial']==1,
       'Every precise native missed-flight callback, no impact state or child reuse')
 dead=phase.overlap.rows(text,'RETIRE')[0]
 need(dead['xraw']==(parent['xraw']+sign*(end-birth)*0x80000)&0xffffffff and
      dead['yraw']==parent['yraw'] and dead['action']==0,'Native miss retires on exact next projectile motion step')
 need(not[r for r in phase.overlap.rows(text,'HEALTH')if r['a8']==child and r['before']!=r['after']],
      'Actual missed Ring never damages victim')
 need(not[r for r in phase.ring_contract.original.rows(text,'GUARD')if r['actor']==child],
      'No missing/hidden Ring hit guard branch in this actual miss')
 for f in range(start+1,max(ready,end)+31):
  need(f in by and by[f]['hp']==by[start+1]['hp'] and by[f]['vhp']==by[start+1]['vhp'],
       'Continuous original miss/parent recovery/cleanup health has no fabricated contact')
 return dict(passed=True,start=start,birth=birth,ownReady=ready,retirement=end,lastScene=max(ready,end)+30,
             damage=0,hit=None,missed=True,blocked=False,victim=17,childFields=len(children),impactGroups=0,
             actualFlightGroups=len(travel),actualFlightPoses=len({r['a0']for r in travel}),
             nativeLockAndActionStores=len(base['flags']),allCPUAccepted=False,fullPortAcceptance=False)


def full_phase(text,guest):
 square_gate,_=compound.square_through_handoff()
 complete=compound.gate(text,guest,square_gate)
 ring=ring_gate(text,guest)
 return dict(ring=dict(reached=True,acceptedRings=[ring]),wholeNativeHealth=complete['wholeNativeHealthLedger'],
             wholeNativeState=complete['wholeNativeStateLedger'],compoundLegSquareOrdinary=complete)
