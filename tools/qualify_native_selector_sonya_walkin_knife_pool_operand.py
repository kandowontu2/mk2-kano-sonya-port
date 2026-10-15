"""Full retained Knife pool proof; distinguish simultaneous later allocations.

Preserve both original host-check rejections. Multiple actual native records
can be allocated in one video field. Select the proven child operand, not all
allocations at its later-reuse frame; both complete masked word stores,
source instructions, actual operand/Main/owner and continuity still required.
"""
import inspect
import json
import traceback
from pathlib import Path
import qualify_native_selector_sonya_walkin_knife_pool as original
import qualify_native_selector_sonya_walkin_knife_pool_context as context

ROOT, need, sha = original.ROOT, original.need, original.sha
OUT = ROOT/'audit_native_selector_sonya_walkin_knife_pool_operand_checked'
CONTEXT_FAILURE = context.OUT/'failure.json'


def typed_pool_stores(records, guest, frame, pc, actor, main, child, pop):
    selected = [r for r in records if original.h(r, 'target') == child]
    return original.pool_stores(selected,guest,frame,pc,actor,main,child,pop)


def execute(state):
    first = json.loads(context.FAILURE.read_text())
    second = json.loads(CONTEXT_FAILURE.read_text())
    need(not first['passed'] and first['error'] == "KeyError('entry')" and not second['passed'] and
         second['error'] == "ValueError('Both consecutive original native low/high free-head stores')",
         'Both actual immutable original host-check rejections retained')
    folder,text,_ = original.capture.RAM_CASES[original.capture.KEY]
    heads = original.rows(text,'MK2_BLADE_ALLOC_HEAD_STORE')
    simultaneous = [r for r in heads if r['frame'] == '2365' and r['pc'] == 'FF809150']
    need(len(simultaneous) > 2 and len({r['target'] for r in simultaneous}) > 1 and
         len([r for r in simultaneous if r['target'] == '01031D10']) == 2,
         'Actual later native field allocates several distinct pool operands')
    lua = (ROOT/'mk2ks_native_selector_cpu_startup_guard.lua').read_text()
    need("log('EVENT',string.format('kind=%s entry=%08X opcode=%04X mask=%04X '" in lua and
         "log('RETIRE',string.format('birth=%d kind=%s original_parent=%08X '" in lua,
         'Original declared complete retirement context and independent opcode EVENT retained')
    gate_source = inspect.getsource(original.gate)
    before = "if k not in ('kind', 'sequence')"
    need(gate_source.count(before) == 1,'Exactly original actual retirement-context shape')
    gate_source = gate_source.replace(before,"if k not in ('kind', 'sequence', 'entry', 'opcode', 'mask')",1)
    source = inspect.getsource(original.execute)
    before = "for path in (Path(__file__).resolve(), PARENT.resolve(),"
    need(source.count(before) == 1,'Whole actual original/source/failure pin inventory')
    source = source.replace(before,
        "for path in (*extra_sources, Path(__file__).resolve(), PARENT.resolve(),",1)
    scope = dict(vars(original),OUT=OUT,__file__=__file__,pool_stores=typed_pool_stores,
        extra_sources=(Path(original.__file__).resolve(),Path(context.__file__).resolve(),
                       context.FAILURE.resolve(),CONTEXT_FAILURE.resolve()))
    exec(compile(gate_source+'\n'+source,__file__+'::whole_original_retirement_context_typed_pool_operand','exec'),scope)
    return scope['execute'](state)


def safe_execute(state):
    try:
        return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual successor rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
