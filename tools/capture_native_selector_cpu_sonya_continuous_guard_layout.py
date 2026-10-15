"""Repair exact dofile binding after native39920's pregame adapter failure."""
import inspect,json
import capture_native_selector_cpu_sonya_continuous_guard as original

ROOT,need,sha=original.ROOT,original.need,original.sha
BASE=ROOT/'audit_native_selector_cpu_sonya_continuous_guard_layout_ram'
OUT=ROOT/'audit_native_selector_cpu_sonya_continuous_guard_layout_capture_checked'
LUA=ROOT/'mk2ks_native_selector_cpu_sonya_continuous_guard_bound.lua'
KEY='cpu_sonya_p2_continuous_guard_boot606_confirm264_bound'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[]
guest=gfx=gfx32=payload=native=None


def execute(state):
    rejected=json.loads((original.BASE/original.KEY/'result.json').read_text())
    need(not rejected['passed']and rejected['nativeExit']==3 and not rejected['actualScenes']and
         not rejected['proofs']and original.NATIVE_HANDLES[original.KEY]['process'].poll()==3 and
         not original.original.prior.prior.current.prior.identity.census(),
         'Original native pregame adapter failure preserved; no gameplay replay')
    source=inspect.getsource(original.execute)
    before='"MK2KS_CPU_PAIR_CONFIRM_AGE=\'264\')'
    after='"MK2KS_CPU_PAIR_CONFIRM_AGE=\'264\'")'
    need(source.count(before)==1,'Same proven prelaunch quote repair')
    source=source.replace(before,after,1)
    marker="'mk2ks_native_selector_cpu_sonya_startup_guard_bound.lua')"
    need(source.count(marker)==1,'Full adapted Lua sources pinned')
    source=source.replace(marker,"'mk2ks_native_selector_cpu_sonya_startup_guard_bound.lua','mk2ks_native_selector_cpu_sonya_continuous_guard.lua')",1)
    scope=dict(vars(original),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,__file__=__file__)
    exec(compile(source,__file__+'::whole_original_transport_corrected_native_dofile_binding','exec'),scope)
    report=scope['execute'](state)
    globals().update({k:scope[k]for k in('guest','gfx','gfx32','payload','native')})
    return report
