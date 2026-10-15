"""Same retained Knife: match retirement context separately from opcode header.

Preserve the original host-check KeyError. The actual Lua RETIRE record logs
context() without EVENT's entry/opcode/mask header; those three fetched fields
remain independently validated on the corresponding actual EVENT. All actual
retirement context fields, ownership, native pool and mechanics gates remain.
"""
import inspect
import json
from pathlib import Path
import qualify_native_selector_sonya_walkin_knife_pool as original

ROOT, need, sha = original.ROOT, original.need, original.sha
OUT = ROOT/'audit_native_selector_sonya_walkin_knife_pool_context_checked'
FAILURE = original.OUT/'failure.json'


def execute(state):
    failure = json.loads(FAILURE.read_text())
    need(not failure['passed'] and failure['error'] == "KeyError('entry')" and
         'all(retire[k] == event[k]' in failure['traceback'],
         'Actual original retirement-header host-check rejection preserved')
    lua = (ROOT/'mk2ks_native_selector_cpu_startup_guard.lua').read_text()
    need("log('EVENT',string.format('kind=%s entry=%08X opcode=%04X mask=%04X '" in lua and
         "log('RETIRE',string.format('birth=%d kind=%s original_parent=%08X '" in lua,
         'Actual immutable observer declares distinct EVENT header and complete RETIRE context')
    scope = dict(vars(original), OUT=OUT, __file__=__file__)
    gate_source = inspect.getsource(original.gate)
    before = "if k not in ('kind', 'sequence')"
    need(gate_source.count(before) == 1, 'Only actual opcode-header/retirement-context shape differs')
    gate_source = gate_source.replace(before, "if k not in ('kind', 'sequence', 'entry', 'opcode', 'mask')", 1)
    source = inspect.getsource(original.execute)
    before = "for path in (Path(__file__).resolve(), PARENT.resolve(),"
    need(source.count(before) == 1, 'Pin entire original failed source and immutable actual rejection')
    source = source.replace(before,
        "for path in (Path(original_source).resolve(), Path(failure_path).resolve(), Path(__file__).resolve(), PARENT.resolve(),", 1)
    scope.update(original_source=original.__file__, failure_path=FAILURE)
    exec(compile(gate_source+'\n'+source, __file__+'::whole_original_gate_actual_retirement_context', 'exec'), scope)
    return scope['execute'](state)


def safe_execute(state):
    try:
        return execute(state)
    except Exception as error:
        import traceback
        need(not OUT.exists(), 'Preserve actual successor rejection')
        OUT.mkdir(); (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
