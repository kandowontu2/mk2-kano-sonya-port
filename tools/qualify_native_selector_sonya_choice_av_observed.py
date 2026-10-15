"""Qualify actual choices/falls/DAC/ROM/RGB without accepting untraced edges.

The original complete bicycle verifier remains rejected. Its failed horizontal
recurrence is preserved, never waived into complete movement acceptance. This
successor verifies vertical travel, own animation, and original cleanup while
explicitly requiring native boundary/velocity-store provenance next.
"""
import inspect
import json
import sys
from pathlib import Path
import qualify_native_selector_sonya_choice_av_checkpoint as original

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_selector_sonya_choice_av_observed_checked'
FAIL=ROOT/'audit_native_selector_sonya_choice_av_checkpoint_checked/failure.json'


def preserve_failure(error):
    need(not FAIL.exists(),'Preserve original unsuccessful verifier exactly once')
    tb=error.__traceback__
    while tb.tb_next:tb=tb.tb_next
    local=tb.tb_frame.f_locals
    need(tb.tb_frame.f_code.co_name=='advance' and local['a']['frame']==3232 and
         local['b']['frame']==3233 and local['g']==0xa000,'Exact original retained failure')
    need(local['b']['xraw']!=(local['a']['xraw']+local['a']['vx'])&0xffffffff,
         'Original failed horizontal recurrence, not gameplay failure inferred')
    report=dict(passed=False,error=repr(error),originalVerifierSHA256=sha(original.__file__),
                actualPreviousField=local['a'],actualNextField=local['b'],gravity=local['g'],
                originalNativeIdentity=original.capture.NATIVE_HANDLES[original.capture.KEY]['identity'],
                completeBicycleAcceptance=False,fullPortAcceptance=False,newNativeGames=0)
    FAIL.parent.mkdir(exist_ok=False)
    original.capture.choices.current.prior.save(FAIL,report)
    return report


def observed_bicycle(text,guest):
    # Retain every original source/owner/action/lock/pose/vertical/fractional
    # landing assertion. Only the untraced horizontal recurrence is separated
    # from acceptance, rather than relaxing it into a purported whole pass.
    factory=inspect.getsource(original.bicycle_gate)
    marker="    source=phase_source.replace(source,'ledger=ledger,source_gate=source_gate)',"
    additions='''
    before="        assert b['xraw']==(a['xraw']+a['vx'])&0xffffffff and b['vx']==flight['vx']"
    after="        horizontal_observations.append(dict(before=a,after=b,untraced=True))"
    insertion="    scope=dict(bicycle.verify.__globals__,ledger=ledger,source_gate=source_gate,adjacent_finish_operand=adjacent_finish_operand)"
    source=phase_source.replace(source,insertion,
        "    source=replace(source,"+repr(before)+","+repr(after)+")\\n"+
        "    source=replace(source,'adjacent_finish_operand=adjacent_finish_operand)', 'adjacent_finish_operand=adjacent_finish_operand,horizontal_observations=horizontal_observations)')\\n"+insertion)
'''
    factory=original.phase_source.replace(factory,marker,additions+'\n'+marker)
    factory=original.phase_source.replace(factory,'adjacent_finish_operand=boundary.adjacent_finish_operand,__file__=__file__)',
        'adjacent_finish_operand=boundary.adjacent_finish_operand,horizontal_observations=horizontal_observations,__file__=__file__)')
    horizontal=[]
    scope=dict(vars(original),horizontal_observations=horizontal)
    exec(compile(factory,__file__+'::whole_vertical_pose_cleanup_horizontal_not_accepted','exec'),scope)
    result=scope['bicycle_gate'](text,guest)
    need(result['start']==3191 and result['fall']==3210 and result['ready']==3252,
         'Actual owned bicycle chronology')
    need(horizontal and horizontal[0]['after']['frame']==3199 and horizontal[-1]['after']['frame']==3252,
         'Every traveling horizontal recurrence retained as unverified data')
    mismatches=[r for r in horizontal if r['after']['xraw']!=(r['before']['xraw']+r['before']['vx'])&0xffffffff
                or r['after']['vx']!=0xfffc0000]
    need(mismatches and mismatches[0]['after']['frame']==3233,'Native left-edge case not removed from evidence')
    result.update(passed=False,verticalPoseAndNativeCleanupAccepted=True,
                  completeHorizontalPhysicsAccepted=False,directNativeBoundaryVelocityStoresObserved=False,
                  retainedUntracedHorizontalCallbacks=horizontal,horizontalMismatches=mismatches,
                  originalCompleteVerifierFailureSHA256=sha(FAIL),fullPortAcceptance=False)
    return result


def gate(text,guest):
    source=inspect.getsource(original.gate)
    source=original.phase_source.replace(source,'bike=bicycle_gate(text,guest)','bike=observed_bicycle(text,guest)')
    source=original.phase_source.replace(source,'completeActualBicycleMiss=bike',
        'actualBicycleVerticalPoseCleanup=bike,completeBicycleLifecycleAccepted=False')
    scope=dict(vars(original),observed_bicycle=observed_bicycle)
    exec(compile(source,__file__+'::actual_choice_fall_and_explicit_horizontal_gap','exec'),scope)
    return scope['gate'](text,guest)


def execute(state):
    need(FAIL.exists() and not json.loads(FAIL.read_text())['passed'], 'Original rejected full verifier remains false')
    source=inspect.getsource(original.execute)
    source=original.phase_source.replace(source,'finiteBicycleLifecycleAndViewsAccepted=True',
        'finiteBicycleLifecycleAndViewsAccepted=False,bicycleVerticalPoseCleanupAndFiniteViewsAccepted=True')
    source=original.phase_source.replace(source,'ROOT/\'tools/read_native_selector_sonya_choice_av_frames.py\'',
        "Path(original.__file__),FAIL,ROOT/'tools/read_native_selector_sonya_choice_av_frames.py'")
    source=original.phase_source.replace(source,
        "PASS all3 actual Sonya choice branches/full bicycle lifecycle and4views/whole DAC-ROM; zero shadow rows remain explicit gap",
        "PASS all3 actual choices/native falls/vertical poses-cleanup/4views/DAC-ROM; horizontal provenance, shadow observer and mixed PCM remain open")
    scope=dict(vars(original),original=original,gate=gate,OUT=OUT,__file__=__file__)
    exec(compile(source,__file__+'::whole_original_dac_rom_raster_fault_checkpoint','exec'),scope)
    return scope['execute'](state)
