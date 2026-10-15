"""Entire Pit continuation with real declared factory sources, not inspect on exec.

Preserve original preboot failure. Dynamic co_filename labels do not identify
the generated function text: inspect returned the parent module docstring.
Use original stored source and exact existing namespace adaptations instead.
"""
import json
from pathlib import Path
import run_native_pit_transition_rejoin as original

ROOT,need,sha,once=original.ROOT,original.need,original.sha,original.once
FAILURE=ROOT/'audit_native_pit_transition_rejoin_kano_p1_checked/report.json'
failed=json.loads(FAILURE.read_text())
need(not failed['passed']and 'Only declared whole capture source adapter leaf ='in failed['error']and
     "inspect.getsource(context['initialize'])"in Path(original.__file__).read_text()and
     not(ROOT/'audit_native_pit_transition_rejoin_kano_p1_ram').exists(),
     'Actual immutable generated-source lookup failure occurred before any native boot')
source=Path(original.__file__).read_text()
source=once(source,"PREFIX='audit_native_pit_transition_rejoin'","PREFIX='audit_native_pit_transition_rejoin_source_bound'")
begin=source.index('    context=previous.functions()')
end=source.index("    factory=once(factory,'    return namespace'",begin)
replacement="""    context=dict(vars(previous.previous),__file__=__file__,__doc__=__doc__,RAM=RAM,paths=paths)
    init=inspect.getsource(previous.previous.initialize)
    init=once(init,"leaf = f'audit_native_current_cross_pit_{fighter}_p{side}_render'",
                   "leaf = f'audit_native_pit_transition_rejoin_source_bound_{fighter}_p{side}'")
    exec(compile(init,__file__+'::entire_real_original_initializer_fresh_paths','exec'),context)
    factory=inspect.getsource(previous.previous.functions)
    factory=once(factory,'namespace = dict(previous.run.__globals__, __file__=__file__, __doc__=__doc__,',
        'namespace = dict({**previous.controls.__globals__, **previous.preflight.__globals__, **previous.run.__globals__}, __file__=__file__, __doc__=__doc__,')
"""
source=source[:begin]+replacement+source[end:]
source=once(source,'    contract_body=inspect.getsource(contract)',
    "    contract_body=previous.previous.contract.executed.source\n"
    "    need(contract.__code__.co_code==previous.previous.contract.executed.scene_contract.__code__.co_code,\n"
    "         'Exact original declared full contract and actual execution bytecode remain identical')")
source=once(source,"    for p in(*LUA,Path(__file__).resolve()):",
    "    for p in(*LUA,Path(__file__).resolve(),original_source_path,failure_path):")
source=once(source,"        text=p.read_text()", "        text=p.read_text()")
scope=dict(__name__=__name__,__file__=__file__,original_source_path=Path(original.__file__),failure_path=FAILURE)
exec(compile(source,__file__+'::whole_original_Pit_continuation_real_declared_sources_only','exec'),scope)
globals().update({k:v for k,v in scope.items()if not k.startswith('__')})
