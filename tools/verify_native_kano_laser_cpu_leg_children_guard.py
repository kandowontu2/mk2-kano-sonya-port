"""Whole existing leg/ring/health/shadow gates on the fresh guard_wait trace.

Separate immutable outputs; same original contracts and actual 35+11 faults.
Change the damage counterexample to six when actual full damage is twenty-two,
so it is a genuine corruption rather than a no-op. Never assume full contact.
"""
import inspect
import json
from pathlib import Path
from types import SimpleNamespace
import verify_native_kano_laser_cpu_leg_children_health as health
import verify_native_kano_laser_cpu_leg_children_faults as faults
import seal_native_kano_laser_cpu_leg_children_review as review

ROOT,need,sha,once,base=health.ROOT,health.need,health.sha,health.once,health.base
HEALTH=ROOT/'audit_native_kano_laser_cpu_leg_children_guard_health_checked'
FAULTS=ROOT/'audit_native_kano_laser_cpu_leg_children_guard_faults_checked'
REVIEW=ROOT/'audit_native_kano_laser_cpu_leg_children_guard_review'
VIEWED=[998,1174,1288,1816,1914,1944,1948,1952,1956,2275,2305,2309,2313,2317,2369,2415,2537,2567,2571,2575,2579]


def qualify(actual):
    scope=dict(vars(health),OUT=HEALTH,__file__=__file__)
    source=inspect.getsource(health.execute)
    # Exact full functions, with only the output path/current adapter pin rebound.
    exec(compile(source,__file__+'::whole_child_health_qualification_fresh_original_guard_route','exec'),scope)
    scope['execute'](actual)


def counterexamples(actual):
    accepted=json.loads((HEALTH/'report.json').read_text())
    need(accepted['passed'],'Actual guard route must pass the whole original positive first')
    ring=accepted['case']['state']['selectedOriginalRing']['acceptedRings'][0]
    need(not ring['blocked'] and ring['damage']==22,
         'Actually observed native full-damage branch, not a strategy-name assumption')
    rebound_health=SimpleNamespace(**dict(vars(health),OUT=HEALTH))
    scope=dict(vars(faults),health=rebound_health,OUT=FAULTS,__file__=__file__)
    exec(compile(inspect.getsource(faults.binding),__file__+'::whole_child_owned_physical_binding','exec'),scope)
    source=inspect.getsource(faults.run)
    source=once(source,
                "('native_ring_damage_amount_wrong',mutate('MK2_CPU_OVERLAP_HEALTH','a10','00000016',child_hp))",
                "('native_ring_damage_amount_wrong',mutate('MK2_CPU_OVERLAP_HEALTH','a10','00000006',child_hp))")
    source=once(source,'Path(__file__),Path(health.__file__),accepted_path,Path(original_phase.__file__)',
                'Path(__file__),Path(fault_source_file),Path(health.__file__),accepted_path,Path(original_phase.__file__)')
    scope.update(fault_source_file=faults.__file__)
    exec(compile(source,__file__+'::whole_35_actual_child_phase_guard_HP_counterexamples_full_damage','exec'),scope)
    exec(compile(inspect.getsource(faults.execute),__file__+'::immutable_fresh_guard_fault_result','exec'),scope)
    scope['execute'](actual)


def seal(actual):
    rebound_health=SimpleNamespace(**dict(vars(health),OUT=HEALTH))
    rebound_faults=SimpleNamespace(**dict(vars(faults),health=rebound_health,OUT=FAULTS))
    scope=dict(vars(review),faults=rebound_faults,OUT=REVIEW,VIEWED=VIEWED,__file__=__file__)
    source=inspect.getsource(review.run)
    source=once(source,"print(json.dumps(dict(passed=True,actualMixedRingDamage=6,nativeHPStores=25,",
                "print(json.dumps(dict(passed=True,actualMixedRingDamage=22,nativeHPStores=13,")
    source=once(source,'Path(__file__),qualification_path,faults_path,actual.OUT',
                'Path(__file__),Path(review_source_file),qualification_path,faults_path,actual.OUT')
    scope.update(review_source_file=review.__file__)
    exec(compile(source,__file__+'::whole_original_native_RAM_review_fresh_full_damage_guard_route','exec'),scope)
    scope['run'](actual)
