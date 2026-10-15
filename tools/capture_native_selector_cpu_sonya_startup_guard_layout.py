"""Repair the proven pregame observer-layout error, never relabel native39088.

Its actual exit3 and zero gameplay/byte/scene records remain rejected. Same
original physical input strategy with corrected passive source layout; this
is a new test of a repaired observer, not a timeout or rejected-game replay.
"""
import inspect,json
from pathlib import Path
import capture_native_selector_cpu_sonya_startup_guard as original

ROOT,need,sha=original.ROOT,original.need,original.sha
BASE=ROOT/'audit_native_selector_cpu_sonya_startup_guard_layout_ram'
OUT=ROOT/'audit_native_selector_cpu_sonya_startup_guard_layout_capture_checked'
LUA=ROOT/'mk2ks_native_selector_cpu_sonya_startup_guard_bound.lua'
KEY='cpu_sonya_p2_guard_from_start_confirm265_bound_layout'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[]
guest=gfx=gfx32=payload=native=None


def execute(state):
    old_folder=original.BASE/original.KEY
    rejection=json.loads((old_folder/'result.json').read_text())
    need(not rejection['passed']and rejection['nativeExit']==3 and
         not rejection['proofs']and not rejection['actualScenes']and
         original.NATIVE_HANDLES[original.KEY]['process'].poll()==3 and
         not original.prior.prior.current.prior.identity.census(),
         'Exact original pregame observer rejection remains terminal3, not gameplay acceptance')
    source=inspect.getsource(original.execute)
    before="""    source=prior.current.replace(source,'scope.update(KEY=KEY,normalize=normalize)',
        'scope.update(KEY=KEY,normalize=normalize,whole_sonya=whole_sonya)')
"""
    source=original.prior.prior.current.replace(source,before,'')
    before='    scope=dict(vars(prior),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,'
    source=original.prior.prior.current.replace(source,before,
        "    sonya_lua += [ROOT/name for name in('mk2ks_native_selector_cpu_sonya_base_expanded.lua','mk2ks_native_selector_cpu_sonya_guard_bound.lua','mk2ks_native_selector_cpu_sonya_startup_guard.lua')]\n"+before)
    scope=dict(vars(original),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,
        __file__=__file__)
    exec(compile(source,__file__+'::whole_original_host_marker_and_passive_layout_binding_repairs','exec'),scope)
    report=scope['execute'](state)
    globals().update({k:scope[k]for k in('guest','gfx','gfx32','payload','native')})
    return report
