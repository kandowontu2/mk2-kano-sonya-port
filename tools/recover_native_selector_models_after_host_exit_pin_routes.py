"""Explicit expected-hash routing in scoped historical model namespaces.

An old source pin resolves only when BOTH its exact canonical path and hash
match the declared source-sync migration. Current pins and all other inputs
keep their original paths. No hash assertion is removed or fabricated.
"""
import inspect
import json
import linecache
import re
import types
from pathlib import Path

import recover_native_selector_models_after_host_exit_history_reads as prior

ROOT = prior.ROOT
OUT = ROOT / 'audit_native_selector_models_after_host_exit_pin_routes'
RAM = {}
ROUTES = []
failed = json.loads((prior.OUT / 'failure.json').read_text())
assert not failed['passed'] and 'Actual dirty checkout/historical installed executable restored' in failed['error']


def relocate_models(startup, sync, cache):
    canonical = ROOT / 'mame-mkp/src/mame/midway'
    def historical_pin_path(path, expected):
        resolved = Path(path).resolve()
        for leaf, old_hash in sync.OLD.items():
            if resolved == (canonical / leaf).resolve() and expected == old_hash:
                backup = sync.BACKUP / ('canonical_' + Path(leaf).stem + '_before_sync' + Path(leaf).suffix)
                sync.need(sync.sha(backup) == old_hash, 'Exact historical input bytes independently verified')
                row = dict(original=str(resolved), preserved=str(backup), expectedSHA256=old_hash)
                if row not in ROUTES:
                    ROUTES.append(row)
                return backup
        return path
    # Only cloned expected-model functions are adapted; preserved modules stay
    # untouched. Subsequent inspect/exec operations see this exact successor
    # source through linecache, rather than an unrelated original file line.
    for module in tuple(cache.values()):
        if not isinstance(module, types.ModuleType):
            continue
        for name, fn in tuple(vars(module).items()):
            if not isinstance(fn, types.FunctionType) or name not in ('expected', 'expected_guest', 'expectation', 'reconstruct', 'reconstruct_prior'):
                continue
            try:
                text = inspect.getsource(fn)
            except (OSError, TypeError):
                continue
            pattern = r'\bsha\((\w+)\)\s*==\s*(\w+)'
            changed, count = re.subn(pattern, r'sha(historical_pin_path(\1,\2))==\2', text)
            if not count:
                continue
            namespace = fn.__globals__
            namespace['historical_pin_path'] = historical_pin_path
            filename = '<exact_historical_pin_route:' + module.__name__ + ':' + name + '>'
            linecache.cache[filename] = (len(changed), None, changed.splitlines(True), filename)
            local = dict(namespace)
            exec(compile(changed, filename, 'exec'), local)
            generated = local[name]
            replacement = types.FunctionType(generated.__code__, namespace, name, generated.__defaults__, generated.__closure__)
            replacement.__kwdefaults__ = generated.__kwdefaults__
            vars(module)[name] = replacement
    return historical_pin_path


scope = dict(prior.scope, OUT=OUT, RAM=RAM, cache={}, namespaces={}, __file__=__file__,
             relocate_models=relocate_models)
scope['scoped'] = types.FunctionType(prior.prior.scoped.__code__, scope, 'scoped')
source = prior.source
marker = '    source = inspect.getsource(original.recover)'
assert source.count(marker) == 1
source = source.replace(marker, '    relocate_models(startup, sync, cache)\n' + marker, 1)
exec(compile(source, __file__ + '::complete_models_explicit_expected_pin_paths', 'exec'), scope)
exec(compile(inspect.getsource(prior.prior.safe_recover), __file__ + '::preserve_actual_pin_route_recovery', 'exec'), scope)
safe_recover = scope['safe_recover']

if __name__ == '__main__':
    safe_recover()
    prior.prior.prior.original.code.interact(banner='Expected-pin routes retained; no native game launched.', local=dict(RAM=RAM))
