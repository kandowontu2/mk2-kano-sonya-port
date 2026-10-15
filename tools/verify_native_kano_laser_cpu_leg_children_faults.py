"""Actual leg, ring-child, guard and complete native ledger counterexamples.

No gameplay replay or modified guest state. Change one real observation at a
time; require a semantic assertion, never count a parser exception as success.
"""
import inspect
import json
import re
import traceback
from pathlib import Path
import verify_native_kano_laser_cpu_leg_children_health as health
import verify_native_cpu_ring_v2971 as original_phase

prior=health.prior
owned=prior.owned
ROOT,need,sha,base=health.ROOT,health.need,health.sha,health.base
OUT=ROOT/'audit_native_kano_laser_cpu_leg_children_faults_checked'


def binding():
    scope=dict(vars(prior),whole_health_with_child=health.health_binding())
    exec(compile(inspect.getsource(prior.physical_binding),
                 __file__+'::whole_child_owned_physical_positive_and_faults','exec'),scope)
    return scope['physical_binding']()


def run(actual):
    need(not OUT.exists() and not base.identity.census(),'Same actual native terminal; no new gameplay')
    accepted_path=health.OUT/'report.json'
    accepted=json.loads(accepted_path.read_text())
    need(accepted['passed'] and accepted['wholeNativeHealthAndBothSlotFlagsVerified'] and
         len(accepted['actualOriginalBodyShadowFaultsRejected'])==11 and
         all(sha(p)==h for p,h in accepted['inputHashes'].items()),
         'Actual full child-owned health/body/shadow positive conserved')
    original_phase.phase_contract_source()
    text=actual.RAM_CASES[actual.KEY][1]
    physical=binding();positive=physical(text,actual.guest)
    selected=positive['selectedOriginalLeg']['cycle']
    ring=positive['selectedOriginalRing']['acceptedRings'][0]
    overlap=prior.repeated_ring.stream.overlap
    child=overlap.rows(text,'CHILD')[0]
    mutate=lambda tag,key,value,predicate=lambda r:True:owned.mutate_line(text,tag,key,value,predicate)
    def remove(tag,predicate=lambda r:True):
        line=next(s for s in text.splitlines()if s.startswith(tag+' ')and predicate(dict(re.findall(r'(\w+)=([^\s]+)',s))))
        return text.replace(line+'\n','',1)
    cycle=lambda r:r['cycle']==str(selected)
    child_hp=lambda r:int(r['a8'],16)==child['a8']
    trials=[
        ('native_leg_step_missing',remove('MK2_CPU_PAIR_EVENT',lambda r:cycle(r)and r['kind']=='step')),
        ('native_leg_entry_missing',remove('MK2_CPU_PAIR_ENTRY',cycle)),
        ('native_leg_victim_ready_missing',remove('MK2_CPU_PAIR_VICTIM_REGAIN',cycle)),
        ('native_leg_victim_ready_busy',mutate('MK2_CPU_PAIR_VICTIM_REGAIN','vflags','0015',cycle)),
        ('native_leg_held_pose_wrong',mutate('MK2_CPU_PAIR_FIELD','vpose','00000000',lambda r:cycle(r)and r['vaction']==str(prior.pair.SPECS['sonya']['victim_state']))),
        ('live_ring_entry_independent_slot_missing',remove('MK2_RING_PAIR_FIELD',lambda r:int(r['frame'])==ring['start']and r['slot']=='1')),
        ('live_ring_entry_independent_owner_wrong',mutate('MK2_RING_PAIR_FIELD','owner','01000000',lambda r:int(r['frame'])==ring['start'])),
        ('native_ring_child_birth_missing',remove('MK2_CPU_OVERLAP_CHILD')),
        ('native_ring_child_birth_late',mutate('MK2_CPU_OVERLAP_CHILD','frame',str(ring['birth']+1))),
        ('native_ring_child_parent_wrong',mutate('MK2_CPU_OVERLAP_CHILD','shot_owner','01000000')),
        ('native_ring_child_Main_wrong',mutate('MK2_CPU_OVERLAP_CHILD','a13','01000000')),
        ('native_ring_retirement_missing',remove('MK2_CPU_OVERLAP_RETIRE')),
        ('native_ring_retirement_late',mutate('MK2_CPU_OVERLAP_RETIRE','frame',str(ring['retirement']+1))),
        ('native_ring_retirement_serial_wrong',mutate('MK2_CPU_OVERLAP_RETIRE','child_serial','99')),
        ('native_ring_live_child_at_terminal',mutate('MK2_CPU_OVERLAP_RESULT','live_children','1')),
        ('native_ring_child_field_missing',remove('MK2_CPU_OVERLAP_CHILD_FIELD')),
        ('native_ring_child_pose_wrong',mutate('MK2_CPU_OVERLAP_CHILD_FIELD','pose','00000000')),
        ('native_ring_child_geometry_wrong',mutate('MK2_CPU_OVERLAP_CHILD_FIELD','xraw','00000000')),
        ('native_ring_child_parameter_wrong',mutate('MK2_CPU_OVERLAP_CHILD_FIELD','parameter','00000000')),
        ('native_ring_flight_group_wrong',mutate('MK2_CPU_OVERLAP_EVENT','a0','00000000',lambda r:r['kind']=='group')),
        ('native_ring_guard_victim_Main_wrong',mutate('MK2_RING_PAIR_GUARD','vmain','01000000',lambda r:int(r['actor'],16)==child['a8'])),
        ('native_ring_loaded_guard_wrong',mutate('MK2_RING_PAIR_TESTED','tested_flags','00000000',lambda r:int(r['actor'],16)==child['a8'])),
        ('native_ring_physical_Block_wrong',mutate('MK2_RING_PAIR_BLOCK','controls','00000000',lambda r:int(r['frame'])==ring['hit']and r['decision']=='2')),
        ('native_ring_damage_amount_wrong',mutate('MK2_CPU_OVERLAP_HEALTH','a10','00000016',child_hp)),
        ('native_ring_damage_Main_owner_wrong',mutate('MK2_CPU_OVERLAP_HEALTH','main_owner','01000000',child_hp)),
        ('native_ring_damage_parent_wrong',mutate('MK2_CPU_OVERLAP_HEALTH','shot_owner','01000000',child_hp)),
        ('native_ring_damage_address_wrong',mutate('MK2_CPU_OVERLAP_HEALTH','at','01060EC0',child_hp)),
        ('native_ring_damage_mask_wrong',mutate('MK2_CPU_OVERLAP_HEALTH','mask','00FF',child_hp)),
        ('independent_damage_context_missing',remove('MK2_CPU_OVERLAP_HEALTH',child_hp)),
        ('paired_damage_executing_actor_wrong',mutate('MK2_CPU_PAIR_HEALTH','a8','01000000',child_hp)),
        ('whole_pre_floor_wrong',mutate('MK2_CPU_PAIR_FIELD','floor','999')),
        ('whole_native_HP_before_wrong',mutate('MK2_CPU_PAIR_HEALTH','before','160')),
        ('current_CPU_store_instruction_wrong',mutate('MK2_CPU_PAIR_FLAG','op0','FFFF',lambda r:r['slot']=='2')),
        ('current_human_store_instruction_wrong',mutate('MK2_CPU_PAIR_FLAG','op0','FFFF',lambda r:r['slot']=='1')),
        ('last_actual_post_field_missing',remove('MK2_HPHASE_POST_FIELD',lambda r:int(r['frame'])==positive['wholeNativeHealthHistory']['lastActuallyRecordedPost']))]
    faults=[]
    for label,changed in trials:
        need(changed!=text,'Fault changes one actual observed record')
        try:physical(changed,actual.guest)
        except(ValueError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native ownership/choreography/health fault accepted: '+label)
    need(len(faults)==35 and physical(text,actual.guest)==positive,
         'All 35 actual counterexamples rejected and whole physical positive restored')
    pins=dict(accepted['inputHashes'])
    for p in (Path(__file__),Path(health.__file__),accepted_path,Path(original_phase.__file__)):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every executed immutable native/source/evidence pin conserved')
    OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,candidate=actual.native.NAME,key=actual.KEY,
        actualNativeOwnershipPhaseGuardHealthFaultsRejected=faults,originalBodyShadowFaults=11,
        wholePositiveRestored=True,originalLegPhaseFunctionByteExact=True,originalCompleteRingPhaseContractRetained=True,
        finiteMixedRingOwnershipVerified=True,wholeRepeatedTrialStillRejected=True,
        fullKOTransitionAccepted=False,allCPUContextsAccepted=False,allArenasAccepted=False,
        fullVisualTimelineAccepted=False,fullAudioAcceptance=False,fullPortAcceptance=False,
        inputHashes=pins,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active',scope=__doc__))
    print(json.dumps(dict(passed=True,actualPhaseOwnershipGuardHealthFaults=len(faults),originalBodyShadowFaults=11,
                         fullPortAcceptance=False)),flush=True)


def execute(actual):
    try:run(actual)
    except Exception as error:
        need(not OUT.exists(),'Preserve actually executed native counterexample failure');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                                        fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
