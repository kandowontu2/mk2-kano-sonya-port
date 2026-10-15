"""Preserve the second exact historical source-byte comparison as well."""
import inspect
import json
import types
from pathlib import Path

import recover_native_selector_models_after_host_exit_history as prior

ROOT = prior.ROOT
OUT = ROOT / 'audit_native_selector_models_after_host_exit_history_reads'
RAM = {}
failed = json.loads((prior.OUT / 'failure.json').read_text())
assert not failed['passed'] and 'line 252' in failed['traceback']
scope = dict(vars(prior), OUT=OUT, RAM=RAM, cache={}, namespaces={}, __file__=__file__)
scope['scoped'] = types.FunctionType(prior.scoped.__code__, scope, 'scoped')
source = inspect.getsource(prior.recover)
marker = "    exec(compile(source, __file__ + '::exact_old_split_source_read', 'exec'), vars(split))"
addition = '''
    body = inspect.getsource(split_original.reconstruct)
    needle = "ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'"
    sync.need(body.count(needle) == 1, 'Exact second historical source read; all comparisons retained')
    body = body.replace(needle, "ROOT/'audit_native_source_sync/canonical_midtunit_m_before_sync.cpp'", 1)
    exec(compile(body, __file__ + '::exact_old_split_whole_source_comparison', 'exec'), vars(split))
'''
assert source.count(marker) == 1
source = source.replace(marker, marker + '\n' + addition, 1)
exec(compile(source, __file__ + '::two_exact_historical_source_reads', 'exec'), scope)
exec(compile(inspect.getsource(prior.safe_recover), __file__ + '::preserve_actual_recovery', 'exec'), scope)
safe_recover = scope['safe_recover']

if __name__ == '__main__':
    safe_recover()
    prior.prior.original.code.interact(banner='Both exact source reads scoped; no native game launched.', local=dict(RAM=RAM))
