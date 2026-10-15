"""Source-bound owned CPU Sonya rendering with pending damage-Main ownership explicit.

Preserve both repeated-game failures AND the stronger whole-HP-context failure.
The original complete selected leg and unchanged native body/shadow model are
independent of the missing extra-Main provenance. Value/PC replay below is an
inventory, NOT acceptance of that unidentified damage process or mixed moves.
"""
import copy
import inspect
import json
import re
import traceback
from pathlib import Path
import verify_native_kano_laser_cpu_leg_owned_trace as original

ROOT,need,sha,once,base=original.ROOT,original.need,original.sha,original.once,original.base
OUT=ROOT/'audit_native_kano_laser_cpu_leg_render_inventory_checked'


def health_inventory(text,guest):
    health_source=original.capture.previous.complete_health.whole_health
    source=inspect.getsource(health_source)
    source=once(source,'p=prior.cpu.original','p=pair')
    source=once(source,"assert set(posts)=={(f,s)for f in range(first,last+1)for s in(1,2)},'Both complete draw-time physical slots'",
                "assert set(posts)=={(f,s)for f in range(first,last)for s in(1,2)},'Every real post field before recorded KO exit; no invented post'")
    source=once(source,'for frame in range(first,last+1):','for frame in range(first,last):')
    before="assert h['a8']in(r['actor'],r['vactor'])and h['a13']in(r['main'],r['vmain']),'Only actual executing CPU/human Main, no foreign actor aliases'"
    after="""assert h['a8']in(r['actor'],r['vactor']),'Actual HP store has an observed real fighter register'
    if h['a13']not in(r['main'],r['vmain']):
     assert 0x01000000<=h['a13']<0x01100000,'Unidentified Main must still be an actual RAM address, never accepted as proven owner'
     pending.append(dict(frame=frame,physicalSlot=slot,a8=hex(h['a8']),unidentifiedMain=hex(h['a13']),before=h['before'],after=h['after'],ownershipAccepted=False))"""
    source=once(source,before,after)
    source=once(source,'count=0;totals={1:0,2:0}','count=0;totals={1:0,2:0};pending=[]')
    source=once(source,'everyOrdinaryPairedAndPostRecoveryHealthStoreReplayed=True,',
                'everyRecordedHPValueAndInstructionReplayed=True,allDamageMainContextsAccepted=False,pendingDamageMainContexts=pending,')
    scope=dict(health_source.__globals__,pair=original.pair)
    exec(compile(source,__file__+'::complete_HP_value_PC_inventory_NOT_unidentified_Main_acceptance','exec'),scope)
    result=scope['whole_health'](text,guest)
    need(len(result['pendingDamageMainContexts'])==1 and not result['allDamageMainContextsAccepted'],
         'Exact observed extra-Main gap remains unaccepted; no arbitrary alias waiver')
    return result


def physical(text,guest):
    source=inspect.getsource(original.physical)
    source=once(source,'health=whole_health_factory()(text,guest)','health=health_inventory(text,guest)')
    scope=dict(original.physical.__globals__,health_inventory=health_inventory)
    exec(compile(source,__file__+'::whole_native_identity_selected_leg_flags_with_separate_HP_value_inventory','exec'),scope)
    result=scope['physical'](text,guest)
    result.update(allDamageMainContextsAccepted=False,mixedFollowupsAccepted=False,
                  preservedStrongerOwnershipFailure=str(original.OUT/'failure.json'))
    return result


def binding(guest):
    source=inspect.getsource(original.binding)
    scope=dict(original.binding.__globals__,physical=physical)
    exec(compile(source,__file__+'::whole_unmodified_native_body_shadow_model_full_actual_pre_frame_range','exec'),scope)
    return scope['binding'](guest)


def run(actual,guarded):
    failure=json.loads((original.OUT/'failure.json').read_text())
    need(not failure['passed'] and failure['error']=="AssertionError('Only actual executing CPU/human Main, no foreign actor aliases')",
         'Preserve exact stronger HP-process-context rejection')
    source=inspect.getsource(original.run)
    source=once(source,'wholeNativeHealthAndBothSlotFlagsVerified=True,',
                'wholeNativeHPValueLedgerAndBothSlotFlagsVerified=True,allDamageMainContextsAccepted=False,')
    source=once(source,'Path(capture.previous.complete_health.__file__),actual.OUT/\'failure.json\',guarded.OUT/\'failure.json\'',
                'Path(capture.previous.complete_health.__file__),Path(original.__file__),original.OUT/\'failure.json\',actual.OUT/\'failure.json\',guarded.OUT/\'failure.json\'')
    scope=dict(original.run.__globals__,OUT=OUT,binding=binding,physical=physical,__file__=__file__,original=original)
    exec(compile(source,__file__+'::entire_native_render_and_all_42_faults_with_pending_extra_Main_explicit','exec'),scope)
    scope['run'](actual,guarded)


def execute(actual,guarded):
    try:run(actual,guarded)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual render-inventory rejection');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                                        allDamageMainContextsAccepted=False,fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
