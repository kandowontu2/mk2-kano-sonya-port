"""Preserve actual eight-loss miss; add ordinary forward walking at Raiden.

Whole original capture, native victim observer, paid-rejoin/state gates and
bounded losses/RAM remain intact. Only one physical-input prefix changes.
"""
import code
import inspect
import json
import traceback
from pathlib import Path
import run_native_kano_raiden_paired_victim as previous

ROOT, need, sha = previous.ROOT, previous.need, previous.sha
OUT = ROOT / 'audit_native_kano_raiden_paired_victim_approach_ram'
SOURCE = ROOT / 'audit_native_kano_raiden_paired_victim_approach_source'
INIT = ROOT / 'audit_native_kano_raiden_paired_victim_approach_initializer'
OLD_INIT = ROOT / 'audit_native_kano_raiden_paired_victim_approach_previous_initializer'
LUA = 'mk2ks_native_kano_raiden_victim_approach_provenance.lua'
NEW = (LUA, 'mk2ks_native_kano_raiden_victim_approach_cache.lua',
       'mk2ks_native_kano_raiden_victim_approach_driver.lua')
CONTROLLERS = list(dict.fromkeys((*NEW, *previous.CONTROLLERS)))
RAM = {}


def source_guard():
    failed_path = previous.ROOT / 'audit_native_kano_raiden_paired_victim_checked/report.json'
    retired_path = failed_path.parent / 'no_handoff_preservation_and_ram_retirement.json'
    failed, retired = (json.loads(path.read_text()) for path in (failed_path, retired_path))
    need(not failed['passed'] and not failed['intendedKanoRaidenVictimRuntimeAccepted'] and
         len(failed['actualEightNativeLosses']) == 8 and failed['nativeExit'] == 0 and
         retired['passed'] and retired['preservationOnly'] and not retired['originalIntendedVictimTrialAccepted'] and
         retired['originalRAMDictionaryCleared'] and retired['reviewServerClosed'] and
         all(sha(path) == digest for path, digest in retired['inputHashes'].items()),
         'Whole actual no-handoff failure and exact RAM retirement preserved, never promoted')
    driver = (ROOT / previous.NEW[2]).read_text().rstrip()
    needle = '  if winner==0 and human.hp>0 and other.hp>0 and not(stage==2'
    addition = ("  if winner==0 and human.hp>0 and other.hp>0 and stage==2 and other.roster==7 and not rawget(_G,\\'MK2KS_KANO_PAIRED_CALLBACK\\')"
                "then press(human.x<other.x and\\'Right\\'or\\'Left\\')end\\n")
    need(driver.count(needle) == 1 and (ROOT / NEW[2]).read_text().rstrip() == driver.replace(needle, addition + needle, 1),
         'Whole original controller, only ordinary forward walking added before original Raiden no-attack predicate')
    for index, before, after in ((1, previous.NEW[2], NEW[2]), (0, previous.NEW[1], NEW[1])):
        original = (ROOT / previous.NEW[index]).read_text().rstrip()
        need(original.count(before) == 1 and (ROOT / NEW[index]).read_text().rstrip() == original.replace(before, after, 1),
             'Whole original observer/cache layer, exact new driver/observer leaf only')
    body = inspect.getsource(previous.source_guard)
    body = previous.once(body,
        'for path in (Path(__file__).resolve(), Path(prepared.__file__), prefix_path, pit_path, victim_path,',
        'for path in (Path(__file__).resolve(), Path(previous.__file__), failed_path, retired_path, Path(prepared.__file__), prefix_path, pit_path, victim_path,')
    body = previous.once(body,
        'Original first two earned opponents; no attacks against native Raiden until actual Kano handoff, then original controls resume. Cursor route reread before first physical direction.',
        'Original first two earned opponents; ordinary forward walking without attacks against native Raiden until actual Kano handoff, then original controls resume. Cursor route reread before first physical direction.')
    namespace = dict(vars(previous), __file__=__file__, OUT=OUT, SOURCE=SOURCE, NEW=NEW,
                     CONTROLLERS=CONTROLLERS, functions=functions, LUA=LUA, previous=previous,
                     failed_path=failed_path, retired_path=retired_path)
    exec(compile(body, __file__ + '::whole_original_source_guard_plus_actual_failed_trial', 'exec'), namespace)
    return namespace['source_guard']()


def functions(provider):
    namespace = dict(vars(previous), __file__=__file__, OUT=OUT, RAM=RAM, LUA=LUA, CONTROLLERS=CONTROLLERS)
    exec(compile(inspect.getsource(previous.functions), __file__ + '::entire_original_bounded_native_host', 'exec'), namespace)
    return namespace['functions'](provider)


def run():
    namespace = dict(vars(previous), __file__=__file__, OUT=OUT, SOURCE=SOURCE, INIT=INIT,
                     OLD_INIT=OLD_INIT, RAM=RAM, source_guard=source_guard, functions=functions,
                     CONTROLLERS=CONTROLLERS, LUA=LUA)
    exec(compile(inspect.getsource(previous.run), __file__ + '::whole_original_guest_native_trial', 'exec'), namespace)
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
            need(not path.exists(), 'Preserve exact successor failure')
            path.write_text(json.dumps(failure, indent=2) + '\n')
        print(json.dumps(failure, indent=2), flush=True)
    code.interact(banner='Original forward-walking Kano/Raiden victim trial; full goal remains open.', local=dict(RAM=RAM))
