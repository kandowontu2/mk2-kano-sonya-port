"""Different actual selection timing; do not replay/relabel original mixed run.

Boot606 and confirm264 are real button timing only. Native ladder/opponent,
RNG, HP, action, positions, Main and child state are never supplied by host.
Same corrected full observer, terminal-first RAM transport and independent
entire1800-field state/HP/native Sonya choice model.
"""
import inspect,json
from pathlib import Path
import capture_native_selector_cpu_sonya_startup_guard_layout as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
BASE=ROOT/'audit_native_selector_cpu_sonya_confirm264_ram'
OUT=ROOT/'audit_native_selector_cpu_sonya_confirm264_capture_checked'
LUA=prior.LUA
KEY='cpu_sonya_p2_guard_from_start_boot606_confirm264'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[]
guest=gfx=gfx32=payload=native=None


def execute(state):
    previous=json.loads((prior.BASE/prior.KEY/'result.json').read_text())
    need(not previous['passed']and previous['nativeExit']==0 and
         previous['error']=="ValueError('Actual original-derived Sonya stage-zero tower and unchanged true roster')"and
         prior.NATIVE_HANDLES[prior.KEY]['process'].poll()==0 and
         not prior.original.prior.prior.current.prior.identity.census(),
         'Original actual Sonya-human/Kano-CPU scenario mismatch stays rejected; no runtime replay')
    source=inspect.getsource(prior.execute)
    marker="    source=inspect.getsource(original.execute)"
    extra='''
    change="    source=prior.current.replace(source,\\\"MK2KS_TEST_FIGHTER='kano'\\\", \\\"MK2KS_TEST_FIGHTER='sonya'\\\")"
    timing="    source=prior.current.replace(source,\\\"MK2KS_TEST_BOOT_FRAME='605'\\\", \\\"MK2KS_TEST_BOOT_FRAME='606'\\\")\\n    source=prior.current.replace(source,\\\"MK2KS_CPU_PAIR_CONFIRM_AGE='265'\\\", \\\"MK2KS_CPU_PAIR_CONFIRM_AGE='264'\\\")"
    source=original.prior.prior.current.replace(source,change,change+'\\n'+timing)
'''
    source=prior.original.prior.prior.current.replace(source,marker,marker+extra)
    scope=dict(vars(prior),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,
        __file__=__file__)
    exec(compile(source,__file__+'::whole_original_observer_distinct_physical_timing','exec'),scope)
    report=scope['execute'](state)
    globals().update({k:scope[k]for k in('guest','gfx','gfx32','payload','native')})
    return report
