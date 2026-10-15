"""Distinct physical guard-from-start route; ungated projectile provenance.

Reuse the entire latest terminal-first transport/state collector and actual
callback keys. CPU decisions remain native. New startup observer is passive;
its records require separate ownership/lifetime/contact qualification.
"""
import inspect,json
from pathlib import Path
import capture_native_selector_cpu_guard_shadow as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
BASE=ROOT/'audit_native_selector_cpu_startup_guard_ram'
OUT=ROOT/'audit_native_selector_cpu_startup_guard_capture_checked'
LUA=ROOT/'mk2ks_native_selector_cpu_startup_guard.lua'
KEY='cpu_kano_p2_guard_from_start_confirm265'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[]
guest=gfx=gfx32=payload=native=None
normalize=prior.normalize
key_selftest=prior.key_selftest


def execute(state):
    parent=ROOT/'audit_native_selector_cpu_guard_checkpoint_checked/report.json'
    proof=json.loads(parent.read_text())
    need(proof['passed']and all(sha(p)==h for p,h in proof['inputHashes'].items()),
         'Previous finite guard checkpoint remains unchanged, not full port acceptance')
    source=inspect.getsource(prior.execute)
    boundary="    boundary=\"    scope.update(KEY=KEY,normalize=normalize)\""
    added="""    source=prior.current.replace(source,"MK2KS_CPU_PAIR_APPROACH='guard_until_close'", "MK2KS_CPU_PAIR_APPROACH='guard_wait'")
    source=prior.current.replace(source,'sources=[LUA,', "sources=[LUA,ROOT/'mk2ks_native_selector_cpu_guard_shadow.lua',")
"""
    source=prior.prior.current.replace(source,boundary,added+boundary)
    source=prior.prior.current.replace(source,"pins=dict(proof['inputHashes']);", 
        "pins=dict(proof['inputHashes']);pins[str(Path(__file__).resolve())]=sha(__file__);")
    scope=dict(vars(prior),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,
        prior=prior.prior,__file__=__file__)
    exec(compile(source,__file__+'::whole_callback_collector_distinct_startup_guard_inputs','exec'),scope)
    report=scope['execute'](state)
    globals().update({k:scope[k]for k in('guest','gfx','gfx32','payload','native')})
    return report
