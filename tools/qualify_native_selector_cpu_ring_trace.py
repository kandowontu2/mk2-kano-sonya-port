"""Current CPU ring/whole-health/flags/body/shadows through real KO observation.

Retain original rejected standalone repeated-leg gate. Never invent COMPLETE:
the leg was followed by a separate ring before victim recovery. Full compound
leg phase acceptance and post-KO game continuation remain required and open.
"""
import inspect,json,re,traceback
from pathlib import Path
from types import SimpleNamespace
import verify_native_kano_laser_cpu_leg_children_health as health
import verify_native_kano_laser_cpu_leg_children_faults as original_faults
import capture_native_selector_special_shadow as current

ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_native_selector_cpu_ring_trace_checked'


def functions():
    owned=health.prior.owned
    source=inspect.getsource(owned.physical)
    first=source.index("    complete=pair.rows(text,'COMPLETE')")
    last=source.index("    stores=pair.rows(text,'HEALTH')",first)
    replacement="""    need(not pair.rows(text,'COMPLETE'),'No completed standalone leg is fabricated')
    terminals=pair.rows(text,'RESULT')
    failed=[dict(re.findall(r'(\\w+)=([^\\s]+)',s))for s in text.splitlines()if s.startswith('MK2_HSPECIAL_FAILED ')]
    phase=[dict(re.findall(r'(\\w+)=([^\\s]+)',s))for s in text.splitlines()if s.startswith('MK2_HPHASE_RESULT ')]
    need(len(terminals)==len(failed)==len(phase)==1 and terminals[0]['frame']==int(phase[0]['frame'])==last+1 and
         int(failed[0]['frame'])==last and failed[0]['reason']=='lost_owned_pair_at_field_done'and
         by[last]['vhp']==0 and terminals[0]['complete_count']==0 and terminals[0]['cycles']==1,
         'Actual source-defined KO observer boundary; no standalone two-pair or post-KO acceptance')
    ring=ring_check(text,guest,'sonya')
    health=health_check(text,guest,ring)
    leg=dict(accepted=False,standaloneRepeatedGateStillRejected=True,compoundPhaseVerificationPending=True)
"""
    source=current.replace(source,source[first:last],replacement)
    source=current.replace(source,
        'return dict(selectedOriginalLeg=leg,wholeNativeHealthHistory=health,',
        'return dict(selectedOriginalLeg=leg,selectedOriginalRing=ring,wholeNativeHealthHistory=health,')
    scope=dict(vars(owned),ring_check=health.prior.ring_binding(),health_check=health.health_binding())
    exec(compile(source,__file__+'::whole_current_pre_health_flag_ledger_explicit_mixed_KO_boundary','exec'),scope)
    physical=scope['physical']
    scope=dict(vars(owned),physical=physical)
    exec(compile(inspect.getsource(owned.binding),__file__+'::entire_original_native_body_shadow_factory','exec'),scope)
    return physical,scope['binding']


def execute(actual):
    need(not OUT.exists()and not current.prior.identity.census(),'Original actual native terminal; fresh independent retained qualification')
    physical,binding=functions();check=binding(actual.guest)
    b=health.prior.owned.load(actual,actual.KEY)
    need(len(b['report']['proofs'])==5 and actual.NATIVE_HANDLES[actual.KEY]['process'].poll()==0 and
         all(sha(p)==h for p,h in b['report']['inputHashes'].items()),
         'Same actual current native terminal and complete current/limited byte proofs; source immutable')
    case=check(b,actual.guest,actual.payload,actual.gfx32)
    channels=current.prior.channels_gate(b['cpuLog'],health.prior.pair.rows(b['cpuLog'],'RESULT')[0]['frame'])
    body_faults=current.prior.shadow_faults(dict(b,report=dict(b['report'],sourceBoundBodyShadowSemantics=case)),
                                         actual.guest,actual.payload,actual.gfx32,check)
    # Preserve exactly the original 35 effective mutation definitions. The five
    # leg-phase faults remain for the separate unaccepted leg compound contract;
    # all thirty ring/health/flags faults apply here, unchanged except the actual
    # full damage counterexample (22 -> 6), which must not be a no-op.
    source=inspect.getsource(original_faults.run)
    first=source.index('    trials=[');last=source.index('    faults=[]',first)
    block=source[first:last]
    block=current.replace(block,
        "('native_ring_damage_amount_wrong',mutate('MK2_CPU_OVERLAP_HEALTH','a10','00000016',child_hp))",
        "('native_ring_damage_amount_wrong',mutate('MK2_CPU_OVERLAP_HEALTH','a10','00000006',child_hp))")
    wrapper='def original_mutations():\n'+block+'    return trials\n'
    text=b['cpuLog'];positive=case['state'];ring=positive['selectedOriginalRing']['acceptedRings'][0]
    overlap=health.prior.repeated_ring.stream.overlap;child=overlap.rows(text,'CHILD')[0]
    owned=health.prior.owned
    def remove(tag,predicate=lambda r:True):
        line=next(s for s in text.splitlines()if s.startswith(tag+' ')and predicate(dict(re.findall(r'(\w+)=([^\s]+)',s))))
        return text.replace(line+'\n','',1)
    fault_scope=dict(vars(original_faults),text=text,positive=positive,ring=ring,child=child,
        selected=1,cycle=lambda r:r['cycle']=='1',child_hp=lambda r:int(r['a8'],16)==child['a8'],remove=remove,
        mutate=lambda tag,key,value,predicate=lambda r:True:owned.mutate_line(text,tag,key,value,predicate))
    exec(compile(wrapper,__file__+'::all_original35_observed_mutations','exec'),fault_scope)
    mutations=fault_scope['original_mutations']()
    need(len(mutations)==35 and all(label.startswith('native_leg_')for label,_ in mutations[:5]),
         'Original five leg tests explicitly remain pending, not relabeled as ring passes')
    rejected=[]
    for label,changed in mutations[5:]:
        need(changed!=text,'Actual observed corruption, not no-op')
        try:physical(changed,actual.guest)
        except(ValueError,AssertionError)as error:rejected.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual ring/health/state corruption admitted: '+label)
        print(label+': rejected',flush=True)
    need(len(rejected)==30 and len(body_faults)==11 and check(b,actual.guest,actual.payload,actual.gfx32)==case,
         'All41 applicable original native/body faults; complete positive restored')
    pins=dict(b['report']['inputHashes'])
    for p in(Path(__file__),Path(health.__file__),Path(health.prior.__file__),Path(owned.__file__),
             Path(original_faults.__file__),Path(health.prior.repeated_ring.__file__),
             Path(health.prior.repeated_ring.original.__file__),Path(health.prior.pair.__file__),
             Path(current.prior.shadow.__file__),actual.OUT/'failure.json',*tuple(p for p in b['folder'].rglob('*')if p.is_file())):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Actual immutable source/evidence conserved')
    OUT.mkdir();value=dict(passed=True,candidate=actual.native.NAME,key=actual.KEY,case=case,
        originalBodyShadowFaultsRejected=body_faults,originalRingHealthFlagFaultsRejected=rejected,
        originalFiveLegPhaseFaultsStillPending=[label for label,_ in mutations[:5]],
        passiveSoundChannels=channels,inputHashes=pins,exactMemoryProofs=b['report']['proofs'],
        actualNativeIdentity=actual.NATIVE_HANDLES[actual.KEY]['identity'],
        originalRepeatedGateStillRejected=True,compoundLegPhaseAcceptance=False,fullKOTransitionAccepted=False,
        allCPUContextsAccepted=False,allArenasAccepted=False,fullRasterAcceptance=False,fullAudioAcceptance=False,
        fullPortAcceptance=False,goalStatus='active',newNativeBoots=0,newBuilds=0,newROMCopies=0,newRawMedia=0,
        publicPlayableChanged=False)
    current.prior.save(OUT/'report.json',value)
    print(json.dumps(dict(passed=True,nativeHealthStores=31,actualApplicableFaults=41,fullPortAcceptance=False)),flush=True)
    return value


def safe_execute(actual):
    try:return execute(actual)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual qualifier rejection');OUT.mkdir()
        current.prior.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
             fullPortAcceptance=False,newNativeBoots=0,goalStatus='active'))
        raise
