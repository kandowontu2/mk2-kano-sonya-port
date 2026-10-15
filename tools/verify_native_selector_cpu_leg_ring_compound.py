"""Actual current native leg, common victim cleanup, then separate ring hurt.

Do not fabricate COMPLETE or count ring-hit ready as leg-ready. Preserve every
original held-pose/damage/fling invariant, bind direct native cleanup stores,
then prove the whole ring and continuous state/health/body/shadow trace.
"""
import hashlib,inspect,json,struct,traceback
from pathlib import Path
import qualify_native_selector_cpu_ring_trace as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_selector_cpu_leg_ring_compound_checked'
pair=prior.health.prior.pair
owned=prior.health.prior.owned
overlap=prior.health.prior.repeated_ring.stream.overlap


def original_phase_kernel():
    source=inspect.getsource(pair.verify_pair)
    first=source.index('    chain=[r for r in events')
    last=source.index('    def clean(r,prefix):',first)
    body=source[first:last]
    # Entire original action/descriptor, five poses/46 held fields, all35HP,
    # fixed-point fling and gravity checks, with no phase-rule substitutions.
    wrapper='def phase_kernel(log,entry,start,end,done,timeline,by,events,health,spec):\n'
    wrapper+='    errors=[]\n    target="sonya";cycle=entry["cycle"]\n'
    wrapper+='    def need(ok,label):\n        if not ok:errors.append(label)\n'
    wrapper+=body
    wrapper+='    return dict(passed=not errors,errors=errors,held_fields=held_fields,release=release,victim_flight_fields=len(flight),damage=spec["damage"],direction=direction)\n'
    scope=dict(vars(pair))
    exec(compile(wrapper,__file__+'::byte_exact_entire_original_leg_phase_damage_fling_core','exec'),scope)
    return scope['phase_kernel'],hashlib.sha256(body.encode()).hexdigest().upper()


PHASE,PHASE_SHA=original_phase_kernel()


def clean(r,prefix=''):
    vx=r[prefix+'vx'];vx=vx-0x100000000 if vx&0x80000000 else vx
    return (r['vypos'if prefix else'y']==r[prefix+'floor']and
            r[prefix+'vy']==r[prefix+'gravity']==r[prefix+'trail']==0 and
            r[prefix+'flags']&0x1c==r[prefix+'body']&0xc==0 and
            (vx==0 or r[prefix+'action']==0x303 and abs(vx)<=0x30000))


def gate(text,guest,qualified_ring):
    fields=pair.rows(text,'FIELD');by={r['frame']:r for r in fields}
    entries=pair.rows(text,'ENTRY');events=pair.rows(text,'EVENT');stores=pair.rows(text,'HEALTH');flags=pair.flag_rows(text)
    need(len(entries)==1 and not pair.rows(text,'COMPLETE'),'Actual one leg entry, no invented standalone completion')
    entry=entries[0];cycle,start=entry['cycle'],entry['frame'];spec=pair.SPECS['sonya']
    need(entry['id']==entry['vid']==entry['roster']==entry['vroster']==18 and
         entry['owner']==entry['actor']and entry['vowner']==entry['vactor']and
         (entry['state'],entry['vstate'],entry['cpu_slot'],entry['human_slot'],entry['mode'])==(0,1,2,1,2),
         'Actual native CPU/human Sonya, both separate real owners/physical roles')
    own=pair.rows(text,'OWN_REGAIN');late_victim=pair.rows(text,'VICTIM_REGAIN')
    need(len(own)==len(late_victim)==1 and own[0]['cycle']==late_victim[0]['cycle']==cycle,
         'Original actual owning and later ring-hurt handoffs retained')
    ring=qualified_ring['acceptedRings'][0];own_at=own[0]['frame']
    action=[r for r in flags if r['slot']==1 and r['kind']=='action'and start<r['frame']<ring['hit']and
            r['pc']==0xff83edd0 and(r['before'],r['after'])==(0x506,0)]
    need(len(action)==1,'One original victim airborne-task cleanup before separate ring impact')
    victim_at=action[0]['frame'];end=victim_at+1
    need(start<own_at<ring['start']<victim_at<ring['hit']<late_victim[0]['frame'],
         'Leg-own cleanup, actual new ring, direct leg-victim cleanup, separate ring-hit recovery in native order')
    timeline=[r for r in fields if start<r['frame']<=end]
    need(len(timeline)==end-start and {r['frame']for r in timeline}==set(range(start+1,end+1)),
         'Every true paired/startup/release/flight/common-cleanup callback remains present')
    for r in [entry,*timeline]:
        need(all(r[k]==entry[k]for k in('actor','main','vactor','vmain','owner','vowner','id','vid','roster','vroster','schedule','stage'))and
             (r['state'],r['vstate'],r['mode'],r['cpu_slot'],r['human_slot'],r['writes'],r['assistance'])==(0,1,2,2,1,0,'none')and
             r['floor']==r['vfloor']==r['stage_floor']-135,
             'Every original native owner/identity/floor/state through leg handoff is source consistent')
    phase=PHASE(text,entry,start,end,by[end],timeline,{r['frame']:r for r in timeline},events,stores,spec)
    need(phase['passed'],str(phase['errors']))
    need(phase['held_fields']==46 and phase['damage']==35 and phase['victim_flight_fields']==23 and
         own_at-phase['release']==10,'Entire source-native leg hold/35HP/23-field gravity/own recovery')
    for slot,prefix,at in ((2,'',own_at),(1,'v',victim_at)):
        actor,main=entry[prefix+'actor'],entry[prefix+'main']
        for kind,offset,pc,mask in (('action',0x1f0,0xff83edd0,None),('body',0x160,0xff83eeb0,0xc),('flags',0x210,0xff83efc0,0x14)):
            actual=[r for r in flags if r['slot']==slot and r['kind']==kind and r['frame']==at and r['pc']==pc]
            need(actual,'Each real actor clears action/body/Main through original common native cleanup')
            for r in actual:
                target=actor if kind=='body'else main;instruction=(pc-32-0xff800000)//8
                need((r['actor'],r['main'],r['a8'],r['a13'],r['id'],r['state'],r['at'])==
                     (actor,main,actor,main,18,0 if slot==2 else 1,target+offset)and
                     (r['op0'],r['op1'])==struct.unpack_from('<HH',guest,instruction)and
                     (r['writes'],r['assistance'],r['cpu_slot'],r['human_slot'])==(0,'none',2,1)and
                     r['after']==(0 if mask is None else r['before']&(~mask&65535)),
                     'Exact actual cleanup owner/instruction/operand/mask, not a coincidental clean callback')
        need(clean(by[at+1],prefix)and by[at+1][prefix+'action']!=(spec['state']if slot==2 else spec['victim_state']),
             'First post-cleanup native callback is grounded and detached for its own actor')
    need(clean(own[0])and own[0]['action']==0 and own[0]['vx']==0,
         'Real leg CPU ready entry exactly returns grounded stationary native ownership')
    landing=next(r for r in timeline if r['frame']>phase['release']and r['vgravity']==0)
    last_air=by[landing['frame']-1]
    need(landing['frame']==phase['release']+24 and landing['vypos']==landing['vfloor']and
         landing['vvx']==landing['vvy']==landing['vgravity']==0 and last_air['vgravity']==0x8000 and
         ((last_air['vyraw']+last_air['vvy']+0x8000)&0xffffffff)>=landing['vfloor']<<16,
         'Actual native flight crosses floor then clamps/stops, not an unexplained skipped airborne field')
    need(clean(by[victim_at+1],'v')and by[victim_at+1]['vaction']==0 and
         all(clean(by[f],'v')and by[f]['vaction']==0 and by[f]['vhp']==entry['vhp']-35
             for f in range(victim_at+1,ring['hit']+1)),
         'Every actual leg-victim detached field before the NEW child-owned ring contact')
    incomplete=pair.rows(text,'INCOMPLETE');terminal=pair.rows(text,'RESULT')
    need(len(incomplete)==len(terminal)==1 and incomplete[0]['frame']==late_victim[0]['frame']+1 and
         terminal[0]['complete_count']==0 and terminal[0]['cycles']==1 and
         incomplete[0]['vhp']==entry['vhp']-35-ring['damage'],
         'Original standalone observer accumulated both distinct real attacks; its rejection stays unchanged')
    # Second hurt-task release must also execute the original common cleanup,
    # now after ring impact, on the same original victim Main.
    hurt_end=late_victim[0]['frame']
    need(clean(late_victim[0],'v')and late_victim[0]['vaction']==0 and
         clean(by[hurt_end+1],'v')and by[hurt_end+1]['vhp']==entry['vhp']-35-ring['damage'],
         'Separate ring victim hurt cleanup returns grounded/detached ordinary control')
    need(ring['ownReady']==hurt_end+2 and clean(by[ring['ownReady']+1]),
         'Ring-own recovery is independently clean; no borrowed leg idle-tail assumption')
    return dict(passed=True,originalLegPhaseKernelSHA256=PHASE_SHA,leg=phase,
        actualLegOwnHandoff=own_at,actualDirectLegVictimCleanup=victim_at,actualLegLanding=landing['frame'],
        actualRingStart=ring['start'],actualRingContact=ring['hit'],actualRingVictimHandoff=hurt_end,
        actualRingOwnHandoff=ring['ownReady'],standaloneRepeatedGateStillRejected=True,
        fabricatedCompleteRecords=0,allCPUContextsAccepted=False,fullPortAcceptance=False)


def execute(actual,ring_receipt):
    need(not OUT.exists()and not prior.current.prior.identity.census(),'Same original terminal trace; no gameplay replay')
    ring_path=ROOT/'audit_native_selector_cpu_ring_trace_ko_origin_checked/report.json'
    receipt=json.loads(ring_path.read_text())
    need(receipt['passed']and all(sha(p)==h for p,h in receipt['inputHashes'].items()),'Whole current ring/health/flags/body/shadows source proof conserved')
    text=actual.RAM_CASES[actual.KEY][1];qualified_ring=receipt['case']['state']['selectedOriginalRing']
    positive=gate(text,actual.guest,qualified_ring);faults=[]
    mutation=lambda tag,key,value,predicate=lambda r:True:owned.mutate_line(text,tag,key,value,predicate)
    def remove(tag,predicate=lambda r:True):
        line=next(s for s in text.splitlines()if s.startswith(tag+' ')and predicate(dict(prior.re.findall(r'(\w+)=([^\s]+)',s))))
        return text.replace(line+'\n','',1)
    tests=[('native_leg_step_missing',remove('MK2_CPU_PAIR_EVENT',lambda r:r['kind']=='step')),
        ('native_leg_entry_missing',remove('MK2_CPU_PAIR_ENTRY')),
        ('native_leg_victim_ready_missing',remove('MK2_CPU_PAIR_VICTIM_REGAIN')),
        ('native_leg_victim_ready_busy',mutation('MK2_CPU_PAIR_VICTIM_REGAIN','vflags','0015')),
        ('native_leg_held_pose_wrong',mutation('MK2_CPU_PAIR_FIELD','vpose','00000000',lambda r:r['vaction']=='273')),
        ('leg_descriptor_wrong',mutation('MK2_CPU_PAIR_EVENT','word','0072',lambda r:r['kind']=='attack')),
        ('leg_release_damage_wrong',mutation('MK2_CPU_PAIR_EVENT','a10','00000022',lambda r:r['kind']=='damage')),
        ('leg_fling_gravity_wrong',mutation('MK2_CPU_PAIR_EVENT','a2','00006000',lambda r:r['kind']=='fling')),
        ('own_leg_handoff_busy',mutation('MK2_CPU_PAIR_OWN_REGAIN','body','00000056')),
        ('direct_victim_cleanup_missing',remove('MK2_CPU_PAIR_FLAG',lambda r:r['slot']=='1'and r['frame']==str(positive['actualDirectLegVictimCleanup'])and r['kind']=='action')),
        ('direct_victim_cleanup_wrong_actor',mutation('MK2_CPU_PAIR_FLAG','a8','010350A0',lambda r:r['slot']=='1'and r['frame']==str(positive['actualDirectLegVictimCleanup']))),
        ('direct_victim_cleanup_wrong_word',mutation('MK2_CPU_PAIR_FLAG','op0','FFFF',lambda r:r['slot']=='1'and r['frame']==str(positive['actualDirectLegVictimCleanup']))),
        ('leg_gravity_field_wrong',mutation('MK2_CPU_PAIR_FIELD','vvy','00000000',lambda r:r['frame']=='2270')),
        ('leg_post_cleanup_busy',mutation('MK2_CPU_PAIR_FIELD','vflags','00000005',lambda r:r['frame']==str(positive['actualDirectLegVictimCleanup']+1))),
        ('leg_landing_not_grounded',mutation('MK2_CPU_PAIR_FIELD','vypos','80',lambda r:r['frame']==str(positive['actualLegLanding']))),
        ('ring_hurt_regain_not_grounded',mutation('MK2_CPU_PAIR_VICTIM_REGAIN','vypos','80')),
        ('post_ring_own_handoff_busy',mutation('MK2_CPU_PAIR_FIELD','body','00000056',lambda r:r['frame']==str(positive['actualRingOwnHandoff']+1)))]
    for label,changed in tests:
        need(changed!=text,'Effective native compound counterexample')
        try:gate(changed,actual.guest,qualified_ring)
        except(ValueError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('False native compound evidence admitted: '+label)
        print(label+': rejected',flush=True)
    need(gate(text,actual.guest,qualified_ring)==positive and len(faults)==17,'All17 leg/compound faults; exact positive restored')
    pins=dict(receipt['inputHashes'])
    for p in(Path(__file__),Path(pair.__file__),ring_path,ROOT/'audit_native_selector_cpu_checkpoint_checked/report.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All actual original immutable evidence conserved')
    OUT.mkdir();value=dict(passed=True,candidate=actual.native.NAME,actualOriginalNativePID=5408,
        actualNativeCompoundLegToRing=positive,additionalActualFaultsRejected=faults,
        previousRingBodyHealthFlagsFaultsRejected=41,inputHashes=pins,
        originalStandaloneRepeatedGateStillRejected=True,newNativeBoots=0,newBuilds=0,newROMCopies=0,newRawMedia=0,
        allCPUContextsAccepted=False,fullKOTransitionAccepted=False,fullAudioAcceptance=False,fullRasterAcceptance=False,
        fullPortAcceptance=False,publicPlayableChanged=False,goalStatus='active')
    prior.current.prior.save(OUT/'report.json',value)
    print(json.dumps(dict(passed=True,legFields=46,legDamage=35,additionalFaults=17,nativeReplay=False)),flush=True)
    return value


def safe_execute(actual,ring_receipt):
    try:return execute(actual,ring_receipt)
    except Exception as error:
        need(not OUT.exists(),'Preserve actually executed native compound rejection');OUT.mkdir()
        prior.current.prior.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
             fullPortAcceptance=False,newNativeBoots=0,goalStatus='active'))
        raise
