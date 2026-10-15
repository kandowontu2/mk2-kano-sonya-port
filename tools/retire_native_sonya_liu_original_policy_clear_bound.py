"""Whole preservation successor with its clear-receipt path locally bound.

The executed stop helper stays frozen. Before executing prepare, bind its
receipt path inside the nested preservation namespace instead of relying on
an outer Python local. No gameplay, inventory or acceptance gate changes.
"""
import inspect
import retire_native_sonya_liu_original_policy as previous

ROOT,need,sha = previous.ROOT,previous.need,previous.sha


def scope():
    return dict(previous.scope(),__file__=__file__)


def prepare(ram):
    body=inspect.getsource(previous.prepare)
    body=previous.original.once(body,
        '"clear_path,OUT/\'original_executed_sources.json.gz\',Path(__file__).resolve()):bound[str(p)]=sha(p)\\\")"',
        '"(ROOT/\'audit_native_subzero_guard_pressure_earned_clear_phase_bound_checked/report.json\'),OUT/\'original_executed_sources.json.gz\',Path(__file__).resolve()):bound[str(p)]=sha(p)\\\")"')
    bound=dict(vars(previous),__file__=__file__,scope=scope)
    exec(compile(body,__file__+'::whole_original_preservation_with_nested_clear_path_bound','exec'),bound)
    return bound['prepare'](ram)


def retire():
    bound=dict(vars(previous),__file__=__file__,scope=scope)
    exec(compile(inspect.getsource(previous.retire),__file__+'::whole_original_exact_retirement','exec'),bound)
    return bound['retire']()


if __name__=='__main__':
    retire()
