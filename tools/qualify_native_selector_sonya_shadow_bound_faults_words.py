"""Strengthen low-half callback's whole32-bit pre-value; keep old acceptance gap."""
import inspect
import json
import re
from pathlib import Path
import qualify_native_selector_sonya_shadow_bound_faults as original

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_selector_sonya_shadow_bound_faults_words_checked'
FAIL=original.OUT/'failure.json'


def complete_before(bindings):
    base=original.previous.previous.previous
    source=inspect.getsource(base.horizontal)
    replace=base.prior.phase_source.replace
    source=replace(source,"r['action']==('0303' if f==3191 else '0204' if f<3211 else '0611')",
        "int(r['action'],16) in action_values(text,f,by[f]['action'])")
    source=replace(source,"need(int(r['before'],16)&65535==(values[kind]>>bit)&65535 and",
        "need((bit!=0 or int(r['before'],16)==values[kind]) and int(r['before'],16)&65535==(values[kind]>>bit)&65535 and")
    scope=dict(bindings)
    exec(compile(source,__file__+'::whole32bit_low_before_and_actual_high_target_word','exec'),scope)
    return scope['horizontal']


def execute(state,error):
    need(not FAIL.exists() and str(error)=='Actual corrupted native evidence accepted: velocity_before',
         'Exact original effective counterexample acceptance remains explicit')
    tb=error.__traceback__
    while tb.tb_next:tb=tb.tb_next
    local=tb.tb_frame.f_locals
    need(local['name']=='velocity_before' and len(local['faults'])==8,'Same original failed counterexample run')
    capture=original.previous.previous.previous.capture
    text=capture.RAM_CASES[capture.KEY][1]
    def row(value):
        return next(s for s in value.splitlines() if s.startswith('MK2_SONYA_HORIZONTAL_STORE ') and
                    'frame=3232 ' in s and 'pc=FF805580 ' in s and 'at=010350E0 ' in s)
    actual,mutant=row(text),row(local['bad'])
    need(actual!=mutant and 'before=FFFC0000 ' in actual and 'before=00000000 ' in mutant,
         'Whole32-bit actual current-velocity pre-value changed effectively')
    FAIL.parent.mkdir()
    original.phases.original.capture.choices.current.prior.save(FAIL,dict(passed=False,error=repr(error),
        actualAcceptedCounterexample=mutant,originalActualRow=actual,sourceSHA256=sha(original.__file__),
        wholePreValueValidationAccepted=False,precedingRejectedFaults=local['faults'],fullPortAcceptance=False,newNativeGames=0))
    source=inspect.getsource(original.execute)
    replace=original.phases.original.phase_source.replace
    source=replace(source,"bindings=scope['execute'](state)",
        "bindings=scope['execute'](state)\n    bindings['horizontal']=complete_before(bindings)")
    source=replace(source,"Path(__file__),Path(previous.__file__),Path(phases.__file__),previous.OUT/'report.json',",
        "Path(__file__),Path(original.__file__),FAIL,Path(previous.__file__),Path(phases.__file__),previous.OUT/'report.json',")
    scope=dict(vars(original),original=original,FAIL=FAIL,OUT=OUT,__file__=__file__,complete_before=complete_before)
    exec(compile(source,__file__+'::all_original_native_faults_with_whole_preword_check','exec'),scope)
    return scope['execute'](state)
