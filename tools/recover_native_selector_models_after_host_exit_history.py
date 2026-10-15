"""Scoped recovery with exact historical source relocation, not waived hashes.

Clone model namespaces in RAM; never monkeypatch the preserved modules or
rewrite their sources/results. Only the split verifier's historical source
reads resolve to the three exact backups already verified by source sync.
All original executable/asset/input/whole-model assertions remain in force.
"""
import inspect
import json
import types
from pathlib import Path

import recover_native_selector_models_after_host_exit_parents as prior

ROOT = prior.ROOT
OUT = ROOT / 'audit_native_selector_models_after_host_exit_history'
RAM = {}
cache, namespaces = {}, {}


def scoped(value):
    key = id(value)
    if key in cache:
        return cache[key]
    if isinstance(value, types.ModuleType):
        file = getattr(value, '__file__', None)
        if not file or not Path(file).resolve().is_relative_to(ROOT / 'tools'):
            return value
        clone = types.ModuleType(value.__name__)
        cache[key] = clone
        namespaces[id(vars(value))] = vars(clone)
        for name, item in vars(value).items():
            vars(clone)[name] = scoped(item)
        return clone
    if isinstance(value, types.FunctionType):
        file = Path(value.__code__.co_filename.split('::')[0])
        if not file.is_absolute() or not file.resolve().is_relative_to(ROOT / 'tools'):
            return value
        original = value.__globals__
        fresh = id(original) not in namespaces
        if fresh:
            namespaces[id(original)] = dict(original)
        scope = namespaces[id(original)]
        clone = types.FunctionType(value.__code__, scope, value.__name__, value.__defaults__, value.__closure__)
        clone.__kwdefaults__ = value.__kwdefaults__
        cache[key] = clone
        if fresh:
            for name, item in original.items():
                scope[name] = scoped(item)
        return clone
    return value


def recover():
    original = prior.original
    sync = original.sync
    sync.need(not OUT.exists(), 'Fresh historical-path recovery evidence')
    failure = prior.OUT / 'failure.json'
    failed = json.loads(failure.read_text())
    sync.need(not failed['passed'] and 'verify_native_split_blood_v1133.py' in failed['traceback'],
              'Exact retained first historical source mismatch')
    sync.verify()
    startup = scoped(original.startup)
    import verify_native_split_blood_v1133 as split_original
    split = scoped(split_original)
    paths = {}
    for leaf, digest in sync.OLD.items():
        current = ROOT / 'mame-mkp/src/mame/midway' / leaf
        backup = sync.BACKUP / ('canonical_' + Path(leaf).stem + '_before_sync' + Path(leaf).suffix)
        sync.need(sync.sha(backup) == digest, 'Exact old bytes at declared historical backup')
        paths[current.resolve()] = backup
    def historical_digest(path):
        resolved = Path(path).resolve()
        return sync.sha(paths.get(resolved, resolved))
    split.digest = historical_digest
    source = inspect.getsource(split_original.reconstruct_prior)
    before = "source_path = ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'"
    after = "source_path = ROOT/'audit_native_source_sync/canonical_midtunit_m_before_sync.cpp'"
    sync.need(source.count(before) == 1, 'One historical source-byte read, no removed assertions')
    source = source.replace(before, after, 1)
    exec(compile(source, __file__ + '::exact_old_split_source_read', 'exec'), vars(split))
    source = inspect.getsource(original.recover)
    before = "    wanted = startup.expected(OUT / 'independent_initializer')"
    sync.need(source.count(before) == 1, 'One unchanged complete model call')
    source = source.replace(before, "    (OUT / 'independent_initializer').mkdir()\n" + before, 1)
    scope = dict(vars(original), startup=startup, OUT=OUT, RAM=RAM, __file__=__file__)
    exec(compile(source, __file__ + '::complete_models_exact_historical_paths', 'exec'), scope)
    return scope['recover']()


def safe_recover():
    try:
        report = recover()
        print(json.dumps(dict(passed=True, modelBytes=report['modelBytes'], newNativeGames=0)), flush=True)
        return report
    except Exception as error:
        if OUT.exists():
            path = OUT / 'failure.json'
            assert not path.exists(), 'Preserve actual successor rejection'
            path.write_text(json.dumps(dict(passed=False, error=repr(error),
                traceback=prior.original.traceback.format_exc(), nativeRuntimeAccepted=False,
                newNativeGames=0, fullPortAcceptance=False), indent=2) + '\n')
        print(json.dumps(dict(passed=False, error=repr(error), traceback=prior.original.traceback.format_exc())), flush=True)
        return None


if __name__ == '__main__':
    safe_recover()
    prior.original.code.interact(banner='Scoped recovered models/failure retained; no native game launched.', local=dict(RAM=RAM))
