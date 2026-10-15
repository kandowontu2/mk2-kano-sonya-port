"""Preserve the original pre-mix textual-count rejection; exact two uses.

The original bicycle-volume fault expression uses its contribution twice,
not three times. Retain every original mixer, clock, DAC/ROM and fault gate.
"""
import inspect
import json
import traceback
from pathlib import Path
import qualify_native_selector_sonya_repeated_cue_pcm as original

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_selector_sonya_repeated_cue_pcm_bound_checked'
FAIL=original.OUT/'failure.json'


def execute(state):
    rejected=json.loads(FAIL.read_text())
    need(not rejected['passed'] and rejected['error']=="ValueError('Whole original bicycle volume fault remains present')",
         'Actual original pre-mix binding rejection retained')
    scope=dict(vars(original),OUT=OUT,__file__=__file__)
    source=inspect.getsource(original.bindings)
    before='source.count(old)==3'
    need(source.count(before)==1,'Only exact literal occurrence count changes')
    exec(compile(source.replace(before,'source.count(old)==2',1),__file__+'::original_bicycle_volume_fault_two_uses','exec'),scope)
    source=inspect.getsource(original.execute)
    before='paths=(Path(__file__),PARENT,'
    after='paths=(Path(__file__),Path(original.__file__),FAIL,PARENT,'
    need(source.count(before)==1,'Pin original failed binding and its source')
    scope['original']=original;scope['FAIL']=FAIL
    exec(compile(source.replace(before,after,1),__file__+'::whole_original_repeated_cue_PCM','exec'),scope)
    return scope['execute'](state)


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        if not OUT.exists():OUT.mkdir()
        need(not (OUT/'failure.json').exists(),'Preserve original successor rejection')
        original.geometry.coverage.original.phases.original.capture.choices.current.prior.save(OUT/'failure.json',
            dict(passed=False,goalStatus='active',error=repr(error),traceback=traceback.format_exc(),
                 newNativeGames=0,fullPortAcceptance=False))
        raise
