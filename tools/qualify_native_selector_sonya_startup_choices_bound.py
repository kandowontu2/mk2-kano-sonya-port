"""Same terminal AI data; supply original whole choice model's guest argument.

Keep the real first checker TypeError. No native replay or source/branch/RNG
rule change: entire original gate and all twelve counterexamples are retained.
"""
import inspect
import json
from pathlib import Path
import qualify_native_selector_sonya_startup_choices as original

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_selector_sonya_startup_choices_bound_checked'


def execute(state):
    failed=original.OUT/'failure.json';failure=json.loads(failed.read_text())
    need(not failure['passed']and failure['error']==
         'TypeError("choice_gate() missing 1 required positional argument: \'guest\'")',
         'Preserve actual original host model-argument rejection')
    scope=dict(vars(original),OUT=OUT,__file__=__file__,original_source=original.__file__,original_failure=failed)
    source=inspect.getsource(original.gate)
    before='choices=binding(schedule)(events)'
    need(source.count(before)==1,'Only missing whole original guest argument corrected')
    source=source.replace(before,'choices=binding(schedule)(events,guest)',1)
    exec(compile(source,__file__+'::whole_original_choice_gate_guest_argument','exec'),scope)
    source=inspect.getsource(original.execute)
    before='for p in (Path(__file__),Path(original.__file__),Path(capture.__file__),path,'
    after='for p in (Path(__file__),Path(original_source),original_failure,Path(original.__file__),Path(capture.__file__),path,'
    need(source.count(before)==1,'Explicit failed checker and exact source pin preservation')
    source=source.replace(before,after,1)
    exec(compile(source,__file__+'::whole_original_actual_choice_and_twelve_fault_suite','exec'),scope)
    exec(compile(inspect.getsource(original.safe_execute),__file__+'::preserve_actual_successor_rejection','exec'),scope)
    return scope['safe_execute'](state)
