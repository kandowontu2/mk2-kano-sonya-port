"""Repair only the prelaunch timing-adapter quote; preserve original failure."""
import inspect
import capture_native_selector_cpu_sonya_continuous_guard as original

ROOT,need,sha=original.ROOT,original.need,original.sha
BASE,OUT,LUA,KEY=original.BASE,original.OUT,original.LUA,original.KEY
RAM_CASES=original.RAM_CASES;NATIVE_HANDLES=original.NATIVE_HANDLES
COMPLETED=original.COMPLETED
guest=gfx=gfx32=payload=native=None


def execute(state):
    need(not BASE.exists()and not OUT.exists()and
         not original.original.prior.prior.current.prior.identity.census(),
         'Failed adapter launched no native game; no replay')
    source=inspect.getsource(original.execute)
    before='"MK2KS_CPU_PAIR_CONFIRM_AGE=\'264\')'
    after='"MK2KS_CPU_PAIR_CONFIRM_AGE=\'264\'")'
    need(source.count(before)==1,'Only generated timing-adapter quote differs')
    source=source.replace(before,after,1)
    scope=dict(vars(original),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_prelaunch_quote_repair','exec'),scope)
    report=scope['execute'](state)
    globals().update({k:scope[k]for k in('guest','gfx','gfx32','payload','native')})
    return report
