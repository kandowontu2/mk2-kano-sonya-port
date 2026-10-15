"""Successor for a prelaunch harness namespace collision; game code unchanged.

Create the whole native bindings while human still names its checker module,
then bind the physical controller's human label. Preserve all original gates.
"""
import inspect, json, traceback
from pathlib import Path
import capture_native_selector_cpu_choke_retained as prior

ROOT, need, sha = prior.ROOT, prior.need, prior.sha
BASE, OUT = prior.BASE, prior.OUT
CPU_CASES, CPU_HANDLES = {}, {}


def execute(state):
    need(not BASE.exists() and not OUT.exists() and not prior.CPU_HANDLES,
         'Prior namespace rejection happened before any native dispatch')
    rejected = ROOT/'audit_native_selector_cpu_choke_prelaunch_rejection'
    need(not rejected.exists(), 'Preserve the original prelaunch rejection')
    rejected.mkdir()
    prior.current.prior.save(rejected/'report.json', dict(
        passed=False, nativeLaunched=False, phase='whole_original_bindings',
        error='TypeError: vars() argument must have __dict__ attribute',
        cause='Physical human label replaced checker module before bindings',
        inputHashes={str(Path(prior.__file__).resolve()): sha(prior.__file__)},
        fullPortAcceptance=False))
    source = inspect.getsource(prior.execute)
    source = prior.current.replace(source,
        "scoped=namespace['functions']();scoped['capture'].__globals__['human']='kano'",
        "scoped=namespace['functions']()")
    source = prior.current.replace(source,
        "native,_,_,decode=base.bindings(guest,build);check=bindings('kano')",
        "native,_,_,decode=base.bindings(guest,build);check=bindings('kano')\n"
        "    scoped['capture'].__globals__['human']='kano'")
    namespace = dict(vars(prior), CPU_CASES=CPU_CASES, CPU_HANDLES=CPU_HANDLES,
                     __file__=__file__)
    exec(compile(source, __file__+'::whole_prior_harness_correct_binding_order', 'exec'), namespace)
    try:
        return namespace['execute'](state)
    except Exception as error:
        failure = ROOT/'audit_native_selector_cpu_choke_bound_failure'
        need(not failure.exists(), 'Never overwrite this successor rejection')
        failure.mkdir()
        prior.current.prior.save(failure/'report.json', dict(
            passed=False, error=repr(error), traceback=traceback.format_exc(),
            retainedNativeHandles=list(CPU_HANDLES),
            inputHashes={str(Path(__file__).resolve()):sha(__file__),
                         str(Path(prior.__file__).resolve()):sha(prior.__file__)},
            fullPortAcceptance=False, goalStatus='active'))
        raise
