"""Same retained run: actual ordinary CPU-owned KO, not a victim-thread grab KO.

Retain the first qualifier rejection. Require the independent full health tap
and whole lifetime/health/flags gates; no unknown projectile/actor waiver.
"""
import inspect,json
from pathlib import Path
import qualify_native_selector_cpu_ring_trace as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_selector_cpu_ring_trace_ko_origin_checked'


def execute(actual):
    failed=prior.OUT/'failure.json';failure=json.loads(failed.read_text())
    need(not failure['passed']and failure['error']==
         "ValueError('Final actual victim-thread native KO store precedes last pre-callback; no missing terminal HP execution')",
         'Preserve original exact KO-context rejection')
    source=inspect.getsource(prior.functions)
    before="    scope=dict(vars(owned),ring_check=health.prior.ring_binding(),health_check=health.health_binding())"
    insertion="""    source=current.replace(source,
        \"stores[-1]['a8']==origin['vactor'] and stores[-1]['a13']==origin['vmain']\",
        \"stores[-1]['a8']==origin['actor'] and stores[-1]['a13']==origin['main']\")
    source=current.replace(source,
        \"    health.update(lastActuallyRecordedPost=last-1,lastPreHPZero=True,terminalPostInvented=False,\",
        \"    final_context=health_overlap.rows(text,'HEALTH')[-1]\\n\"
        \"    need((final_context['frame'],final_context['slot'],final_context['before'],final_context['after'],final_context['pc'],final_context['a8'],final_context['a13'])==tuple(stores[-1][k]for k in('frame','slot','before','after','pc','a8','a13'))and final_context['main_owner']==origin['actor']and final_context['shot_owner']==0 and final_context['id']==18 and final_context['at']==0x010602f0 and final_context['mask']==65535 and final_context['writes']==0 and final_context['assistance']=='none','Last actual ordinary CPU KO exactly matches independent owned native health operands')\\n\"
        \"    health.update(lastActuallyRecordedPost=last-1,lastPreHPZero=True,terminalPostInvented=False,\")
"""
    source=prior.current.replace(source,before,insertion+before.replace(
        'scope=dict(vars(owned),','scope=dict(vars(owned),health_overlap=health.prior.repeated_ring.stream.overlap,'))
    scope=dict(vars(prior),OUT=OUT,__file__=__file__)
    exec(compile(source,__file__+'::entire_original_gate_independent_actual_CPU_KO','exec'),scope)
    source=inspect.getsource(prior.execute)
    source=prior.current.replace(source,'for p in(Path(__file__),Path(health.__file__),',
        'for p in(Path(__file__),Path(prior_file),prior_failure,Path(health.__file__),')
    scope.update(prior_file=prior.__file__,prior_failure=failed)
    exec(compile(source,__file__+'::entire_original41_fault_body_health_ring_suite','exec'),scope)
    exec(compile(inspect.getsource(prior.safe_execute),__file__+'::preserve_new_actual_rejection','exec'),scope)
    return scope['safe_execute'](actual)
