"""Repair only a prelaunch factory marker collision; keep its failed source.

The new whole-Sonya model is needed in the outer phase closure, not inside
the capture factory's original KEY/normalize marker. No native game replay.
"""
import inspect,json
from pathlib import Path
import capture_native_selector_cpu_sonya_startup_guard as original

ROOT,need,sha=original.ROOT,original.need,original.sha
BASE,OUT,LUA,KEY=original.BASE,original.OUT,original.LUA,original.KEY
RAM_CASES=original.RAM_CASES;NATIVE_HANDLES=original.NATIVE_HANDLES
COMPLETED=original.COMPLETED
guest=gfx=gfx32=payload=native=None


def execute(state):
    need(not BASE.exists()and not original.prior.prior.current.prior.identity.census(),
         'Original marker rejection occurred before native launch; not a replay')
    source=inspect.getsource(original.execute)
    before="""    source=prior.current.replace(source,'scope.update(KEY=KEY,normalize=normalize)',
        'scope.update(KEY=KEY,normalize=normalize,whole_sonya=whole_sonya)')
"""
    source=original.prior.prior.current.replace(source,before,'')
    scope=dict(vars(original),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_factory_marker_binding_only','exec'),scope)
    report=scope['execute'](state)
    globals().update({k:scope[k]for k in('guest','gfx','gfx32','payload','native')})
    return report
