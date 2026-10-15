"""Distinct cold confirm264/forward approach then original guard-hold continuation.

CPU remains entirely native. Keep the full generic ungated startup observer,
actual allocation/retirement, whole native state/HP/RNG and callback-distinct
RAM transport. Add passive round-entry rasters, not forced projectile choices.
"""
import inspect,json
from pathlib import Path
import capture_native_selector_cpu_guard_shadow as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
BASE=ROOT/'audit_native_selector_cpu_first_round_projectile_ram'
OUT=ROOT/'audit_native_selector_cpu_first_round_projectile_capture_checked'
LUA=ROOT/'mk2ks_native_selector_cpu_first_round_projectile.lua'
KEY='cpu_kano_p2_first_round_forward_guard_hold_confirm264'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[]
guest=gfx=gfx32=payload=native=None
normalize=prior.normalize
key_selftest=prior.key_selftest


def execute(state):
    parent=ROOT/'audit_native_selector_cpu_sonya_continuous_checkpoint_checked/report.json'
    proof=json.loads(parent.read_text())
    need(proof['passed']and all(sha(p)==h for p,h in proof['inputHashes'].items()),
         'Latest whole blocked-ring checkpoint/full14 requirements unchanged')
    source=inspect.getsource(prior.execute)
    boundary="    boundary=\"    scope.update(KEY=KEY,normalize=normalize)\""
    added="""    source=prior.current.replace(source,"MK2KS_CPU_PAIR_APPROACH='guard_until_close'", "MK2KS_CPU_PAIR_APPROACH='original'")
    source=prior.current.replace(source,"MK2KS_CPU_PAIR_CONFIRM_AGE='265'", "MK2KS_CPU_PAIR_CONFIRM_AGE='264'")
    source=prior.current.replace(source,'sources=[LUA,', "sources=[LUA,ROOT/'mk2ks_native_selector_cpu_guard_shadow.lua',ROOT/'mk2ks_native_selector_cpu_startup_guard.lua',")
"""
    source=prior.prior.current.replace(source,boundary,added+boundary)
    source=prior.prior.current.replace(source,"pins=dict(proof['inputHashes']);",
        "pins=dict(proof['inputHashes']);pins[str(Path(__file__).resolve())]=sha(__file__);")
    scope=dict(vars(prior),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,
        prior=prior.prior,__file__=__file__)
    exec(compile(source,__file__+'::whole_original_collector_distinct_first_round_input_route','exec'),scope)
    report=scope['execute'](state)
    globals().update({k:scope[k]for k in('guest','gfx','gfx32','payload','native')})
    return report
