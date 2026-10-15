"""Real child-covered Sonya leg/ring trace, not two clean pairs or full port.

Preserve the complete repeated ring flight/impact/guard/retirement contract.
Bind its already-live entry to the original independent ring actor observer
and the actual paired callback, instead of requiring an unloaded old observer.
Replay all real health stores with independently witnessed fighter OR exact
allocated ring-child ownership. Never alias a projectile to either fighter.
"""
import inspect
import json
import re
import traceback
from pathlib import Path
import verify_native_kano_laser_cpu_leg_owned_trace as owned
import native_repeated_cpu_ring_contract_v2970 as repeated_ring

ROOT,need,sha,once,base=owned.ROOT,owned.need,owned.sha,owned.once,owned.base
pair=owned.pair
OUT=ROOT/'audit_native_kano_laser_cpu_leg_children_owned_checked'


def ring_binding():
    source=inspect.getsource(repeated_ring.verify)
    first=source.index("    startup=[r for r in stream.rounds.rows(log,'FIELD')if r['frame']==start]")
    last=source.index('    for frame in range(start+1,start+52):',first)
    replacement="""    # This exact trial is already live; no mode7 callback is invented.
    need(start in by,'Actual already-live ring-entry paired callback exists')
    boundary=by[start]
    need((boundary['mode'],boundary['state'],boundary['vstate'],boundary['stage'],boundary['schedule'],
          boundary['actor'],boundary['main'],boundary['owner'],boundary['id'],boundary['vid'])==
         (2,0,1,0,initial['schedule'],actor,main,actor,18,stream.pair.HUMANS[player]),
         'Complete actual paired mode/role/arena/identity context at live ring entry')
    startup=[r for r in original.rows(log,'FIELD')if r['frame']==start]
    need(len(startup)==2 and {r['slot']for r in startup}=={1,2},
         'Both independently observed actual native ring-entry actors')
    for row in startup:
        slot=row['slot'];prefix='v'if slot==1 else''
        a,m=(victim,vmain)if slot==1 else(actor,main)
        identity=stream.pair.HUMANS[player]if slot==1 else 18
        need((row['actor'],row['main'],row['owner'],row['id'])==(a,m,a,identity),
             'Independent live entry-boundary physical actor and Main identity')
        need(all(row[k]==boundary[prefix+k]for k in
                 ('pose','action','xraw','yraw','floor','flags','body','vx','vy','gravity','trail')),
             'Every independent native entry actor word agrees with actual paired callback')
        need(row['stage_floor']==boundary['stage_floor'] and row['writes']==0 and row['assistance']=='none',
             'Independent entry observer has same actual arena ground, no guest assistance')
    native_mode7=False

"""
    source=once(source,source[first:last],replacement)
    scope=dict(vars(repeated_ring))
    exec(compile(source,__file__+'::whole_original_ring_exact_independent_live_entry','exec'),scope)
    return scope['verify']


def whole_health_with_child(text,guest,ring):
    overlap=repeated_ring.stream.overlap
    paired=pair.rows(text,'HEALTH');contexts=overlap.rows(text,'HEALTH')
    need(len(paired)==len(contexts)>0,'Every actual damage tap independently witnessed by both observers')
    keys=('frame','slot','at','before','after','mask','pc','a8','a13','a10')
    authority={}
    born=repeated_ring.one(overlap.rows(text,'CHILD'),'One independently allocated ring child')
    dead=repeated_ring.one(overlap.rows(text,'RETIRE'),'One independently retired ring child')
    fields=pair.rows(text,'FIELD');by={r['frame']:r for r in fields}
    need(ring['reached'] and len(ring['acceptedRings'])==1,'Entire real child lifetime contract accepted first')
    accepted=ring['acceptedRings'][0]
    child_stores=0
    for h,c in zip(paired,contexts):
        need(all(h[k]==c[k]for k in keys),'Same actual HP store, instruction, operands and execution order')
        r=by[h['frame']]
        fighters={(r['actor'],r['main']),(r['vactor'],r['vmain'])}
        executing=(h['a8'],h['a13'])
        if executing in fighters:
            need(c['main_owner']==h['a8'] and c['id']==18,
                 'Actual executing fighter process owns its exact fighter, not cross-product aliases')
        else:
            need(executing==(born['a8'],born['a13']) and born['frame']<=h['frame']<dead['frame'] and
                 (c['main_owner'],c['shot_owner'],c['id'],c['cycle'],c['serial'])==
                 (born['a8'],r['actor'],18,born['cycle'],born['serial']) and
                 h['frame']==accepted['hit'] and h['slot']==1 and
                 h['before']-h['after']==h['a10']==accepted['damage'],
                 'Actual allocated ring child and owned CPU parent cause exactly the independently proven contact damage')
            child_stores+=1
        key=tuple(h[k]for k in keys)
        need(key not in authority,'No duplicated damage authorization record')
        authority[key]=executing
    need(child_stores==1,'Exactly the real independently proven ring child damage store')

    def authorized(h,r,slot):
        return tuple(h[k]for k in keys)in authority and h['slot']==slot

    original=owned.capture.previous.complete_health
    source=inspect.getsource(original.whole_health)
    source=once(source,'p=prior.cpu.original','p=pair')
    source=once(source,
        "assert set(posts)=={(f,s)for f in range(first,last+1)for s in(1,2)},'Both complete draw-time physical slots'",
        "assert set(posts)=={(f,s)for f in range(first,last)for s in(1,2)},'Every actual post before source-defined KO observer exit; terminal post not fabricated'")
    source=once(source,'for frame in range(first,last+1):','for frame in range(first,last):')
    source=once(source,
        "assert h['a8']in(r['actor'],r['vactor'])and h['a13']in(r['main'],r['vmain']),'Only actual executing CPU/human Main, no foreign actor aliases'",
        "assert authorized(h,r,slot),'Exact independently observed executing fighter OR allocated/contact-verified/retired ring child; no unknown actor aliases'")
    scope=dict(original.whole_health.__globals__,pair=pair,authorized=authorized)
    exec(compile(source,__file__+'::whole_original_HP_replay_with_actual_child_lifetime_authority','exec'),scope)
    report=scope['whole_health'](text,guest)
    report.update(independentlyMatchedDamageContexts=len(contexts),actualOwnedRingDamageStores=child_stores,
                  unknownActorAliasesAccepted=False)
    return report


def physical_binding():
    source=inspect.getsource(owned.physical)
    source=once(source,'    health=whole_health_factory()(text,guest)',
                "    ring=ring_check(text,guest,'sonya')\n    health=whole_health_with_child(text,guest,ring)")
    source=once(source,'return dict(selectedOriginalLeg=leg,wholeNativeHealthHistory=health,',
                'return dict(selectedOriginalLeg=leg,selectedOriginalRing=ring,wholeNativeHealthHistory=health,')
    scope=dict(vars(owned),ring_check=ring_binding(),whole_health_with_child=whole_health_with_child)
    exec(compile(source,__file__+'::whole_original_actual_CPU_trace_with_proven_child_health','exec'),scope)
    return scope['physical']


def run(actual):
    need(not OUT.exists() and not base.identity.census(),'Same actual native terminal; no replay')
    b=owned.load(actual,actual.KEY)
    need(all(sha(p)==h for p,h in b['report']['inputHashes'].items()),'Every actually executed candidate and observer unchanged')
    physical=physical_binding()
    scope=dict(vars(owned),physical=physical)
    exec(compile(inspect.getsource(owned.binding),__file__+'::whole_original_body_shadow_binding_with_child_owned_health','exec'),scope)
    check=scope['binding'](actual.guest)
    case=check(b,actual.guest,actual.payload,actual.gfx32)
    passive=base.channels_gate(b['cpuLog'],pair.rows(b['cpuLog'],'RESULT')[0]['frame'])
    faults=base.shadow_faults(dict(b,report=dict(b['report'],sourceBoundBodyShadowSemantics=case)),
                            actual.guest,actual.payload,actual.gfx32,check)
    need(len(faults)==11,'Entire original eleven body/shadow/ROM faults retained')
    need(check(b,actual.guest,actual.payload,actual.gfx32)==case,'Complete positive restored after faults')
    pins=dict(b['report']['inputHashes'])
    for p in (Path(__file__),Path(owned.__file__),Path(repeated_ring.__file__),
              Path(repeated_ring.original.__file__),Path(pair.__file__),Path(base.shadow.__file__),
              actual.OUT/'failure.json',*tuple(p for p in b['folder'].rglob('*')if p.is_file())):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All candidate/source/evidence remain immutable')
    OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,candidate=actual.native.NAME,case=case,
        actualOriginalBodyShadowFaultsRejected=faults,passiveSoundChannels=passive,inputHashes=pins,
        wholeRepeatedTrialStillRejected=True,finiteMixedRingOwnershipVerified=True,
        everyActualOwnedBodyShadowCallSourceBound=True,wholeNativeHealthAndBothSlotFlagsVerified=True,
        fullKOTransitionAccepted=False,allCPUContextsAccepted=False,allArenasAccepted=False,
        fullVisualTimelineAccepted=False,fullAudioAcceptance=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active',scope=__doc__))
    print(json.dumps(dict(passed=True,ring=case['state']['selectedOriginalRing'],
                         originalBodyShadowFaults=len(faults),fullPortAcceptance=False)),flush=True)


def execute(actual):
    try:run(actual)
    except Exception as error:
        need(not OUT.exists(),'Preserve actually executed child qualification failure');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                                        fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
