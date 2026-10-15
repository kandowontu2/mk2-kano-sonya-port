"""Entire forward-walking trial, correct one obsolete exact cache-leaf guard."""
import code
import inspect
import json
import traceback
from pathlib import Path
import run_native_kano_raiden_paired_victim_approach as failed

ROOT, need, sha, once = failed.ROOT, failed.need, failed.sha, failed.previous.once
OUT = ROOT / 'audit_native_kano_raiden_paired_victim_approach_bound_ram'
SOURCE = ROOT / 'audit_native_kano_raiden_paired_victim_approach_bound_source'
INIT = ROOT / 'audit_native_kano_raiden_paired_victim_approach_bound_initializer'
OLD_INIT = ROOT / 'audit_native_kano_raiden_paired_victim_approach_bound_previous_initializer'
LUA, NEW, CONTROLLERS = failed.LUA, failed.NEW, failed.CONTROLLERS
RAM = {}


def source_guard():
    preflight_path = ROOT / 'audit_native_kano_raiden_paired_victim_approach_preflight_failure/failure.json'
    preflight = json.loads(preflight_path.read_text())
    need(not preflight['passed'] and not preflight['nativeBootOccurred'] and preflight['originalRAMWasEmpty'] and
         preflight['originalFailure']['error'] == "ValueError('Whole existing native cache observer, one driver leaf only')" and
         all(sha(path) == digest for path, digest in preflight['inputHashes'].items()),
         'Actual entire preboot guard failure frozen; no gameplay failure or native restart')
    source = inspect.getsource(failed.source_guard)
    boundary = "    body = previous.once(body,\n        'for path in (Path(__file__).resolve(), Path(prepared.__file__), prefix_path, pit_path, victim_path,'"
    correction = "    body = previous.once(body, \"dofile('mk2ks_native_kano_raiden_victim_driver.lua')\", \"dofile('mk2ks_native_kano_raiden_victim_approach_driver.lua')\")\n"
    source = once(source, boundary, correction + boundary)
    source = once(source,
        'for path in (Path(__file__).resolve(), Path(previous.__file__), failed_path, retired_path, Path(prepared.__file__), prefix_path, pit_path, victim_path,',
        'for path in (Path(__file__).resolve(), Path(failed_file), preflight_path, Path(previous.__file__), failed_path, retired_path, Path(prepared.__file__), prefix_path, pit_path, victim_path,')
    source = once(source,
        'failed_path=failed_path, retired_path=retired_path)',
        'failed_path=failed_path, retired_path=retired_path, failed_file=failed_file, preflight_path=preflight_path)')
    namespace = dict(vars(failed), __file__=__file__, OUT=OUT, SOURCE=SOURCE, functions=functions,
                     failed_file=failed.__file__, preflight_path=preflight_path)
    exec(compile(source, __file__ + '::entire_original_guard_exact_current_cache_leaf', 'exec'), namespace)
    return namespace['source_guard']()


def functions(provider):
    namespace = dict(vars(failed), __file__=__file__, OUT=OUT, RAM=RAM)
    exec(compile(inspect.getsource(failed.functions), __file__ + '::same_original_native_host', 'exec'), namespace)
    return namespace['functions'](provider)


def run():
    namespace = dict(vars(failed), __file__=__file__, OUT=OUT, SOURCE=SOURCE, INIT=INIT, OLD_INIT=OLD_INIT,
                     RAM=RAM, source_guard=source_guard, functions=functions)
    exec(compile(inspect.getsource(failed.run), __file__ + '::whole_original_native_trial', 'exec'), namespace)
    return namespace['run']()


if __name__ == '__main__':
    try:
        captured = run()
    except Exception as error:
        folder = OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        failure = dict(passed=False, error=repr(error)[:4096], traceback=traceback.format_exc(),
                       fullPortAcceptance=False, goalStatus='active')
        if folder.exists():
            path = folder / 'current_capture_failure.json'
            need(not path.exists(), 'Preserve actual original bound-successor failure')
            path.write_text(json.dumps(failure, indent=2) + '\n')
        print(json.dumps(failure, indent=2), flush=True)
    code.interact(banner='Original exact-leaf forward-walking native victim trial; full goal remains open.', local=dict(RAM=RAM))
