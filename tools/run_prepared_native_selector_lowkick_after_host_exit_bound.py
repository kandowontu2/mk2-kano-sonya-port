"""Expose the complete prepared namespace; preserve first pre-launch failure."""
import inspect
import json
from types import SimpleNamespace

import run_prepared_native_selector_lowkick_after_host_exit as prior

OUT = prior.ROOT / 'audit_native_selector_lowkick_after_host_exit_bound_capture_checked'
failure = prior.OUT / 'failure.json'
failed = json.loads(failure.read_text())
assert not failed['passed'] and "has no attribute 'LUA'" in failed['error']
scope = dict(vars(prior), OUT=OUT, __file__=__file__)
source = inspect.getsource(prior.execute)
marker = "for file in (Path(__file__), parent, prepared.OUT / 'report.json', prepared.LUA,"
assert source.count(marker) == 1
source = source.replace(marker, "for file in (Path(__file__), prior_source, first_failure, parent, prepared.OUT / 'report.json', prepared.LUA,", 1)
scope.update(prior_source=prior.Path(prior.__file__), first_failure=failure)
exec(compile(source, __file__ + '::whole_original_capture_complete_prepared_namespace', 'exec'), scope)
exec(compile(inspect.getsource(prior.safe_execute), __file__ + '::preserve_actual_bound_capture', 'exec'), scope)


def run(prepared):
    complete = SimpleNamespace(**(dict(vars(prepared.prior)) | dict(vars(prepared))))
    return scope['safe_execute'](complete)
