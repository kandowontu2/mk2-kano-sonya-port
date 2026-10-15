"""Whole failed forward-jump host successor; only nested Lua reader corrected."""
import code
import inspect
import json
import traceback
from pathlib import Path
import run_native_sonya_subzero_forward_jump_campaign as original

ROOT, need, sha = original.ROOT, original.need, original.sha
OUT = ROOT / 'audit_native_sonya_subzero_forward_jump_bound_campaign_ram'
SOURCE = ROOT / 'audit_native_sonya_subzero_forward_jump_bound_campaign_source'
INIT = ROOT / 'audit_native_sonya_subzero_forward_jump_bound_campaign_initializer'
OLD_INIT = ROOT / 'audit_native_sonya_subzero_forward_jump_bound_campaign_previous_initializer'
LUA = 'mk2ks_native_paired_stumble_subzero_forward_jump_bound.lua'
CONTROLLERS = list(dict.fromkeys((LUA, *original.CONTROLLERS)))
RAM = {}


def boot_pins():
    paths = [ROOT / 'audit_native_subzero_forward_jump_boot_failure_preserved/report.json',
             ROOT / 'audit_native_subzero_forward_jump_boot_failure_retired/report.json']
    failed, retired = [json.loads(path.read_text()) for path in paths]
    need(failed['preservationPassed'] and not failed['passed'] and failed['originalNativeExit'] == 3 and
         failed['actualGuestNotVerified'] and retired['passed'] and retired['retirementOnlyAccepted'],
         'Original actual frame-zero loader failure still failed and exact RAM producer retired')
    pins = {}
    for proof in (failed, retired):
        for path, digest in proof['inputHashes'].items():
            need(sha(path) == digest and (path not in pins or pins[path] == digest), 'Whole failed boot pins unchanged')
            pins[path] = digest
    wrapper = (ROOT / LUA).read_text()
    need(wrapper.count('source=source:sub(1,a-1)..after..source:sub(b+1)') == 1 and
         "local path='mk2ks_native_paired_stumble_subzero_forward_jump.lua'" in wrapper and
         "local common_file=assert(io.open('mk2ks_natural_campaign_shao_ring_retreat_v3485.lua','rb'))" in wrapper and
         ':set_value(' not in wrapper and ':clear_value(' not in wrapper and 'manager.machine:exit()' not in wrapper,
         'One reader binding only; entire original physical feedback and passive/native guards unchanged')
    for path in (Path(original.__file__), *paths): pins[str(path.resolve())] = sha(path)
    return pins


def functions(provider):
    scope = dict(vars(original), __file__=__file__, OUT=OUT, LUA=LUA, CONTROLLERS=CONTROLLERS)
    exec(compile(inspect.getsource(original.functions), __file__ + '::whole_original_full_host', 'exec'), scope)
    return scope['functions'](provider)


def source_guard():
    scope = dict(vars(original), __file__=__file__, original=original, OUT=OUT, SOURCE=SOURCE,
                 LUA=LUA, CONTROLLERS=CONTROLLERS, functions=functions, boot_pins=boot_pins)
    body = original.previous.once(inspect.getsource(original.source_guard),
        '    pins = {}', '    pins = boot_pins()')
    body = original.previous.once(body, '    wrapper = (ROOT / LUA).read_text()',
                                  '    wrapper = (ROOT / original.LUA).read_text()')
    body = original.previous.once(body, 'report = dict(passed=True, sourceOnlyAccepted=True,',
                                  'report = dict(loaderBindingOnlyChanged=True, originalFailedBootPreserved=True, passed=True, sourceOnlyAccepted=True,')
    exec(compile(body, __file__ + '::whole_original_guard_plus_real_failed_boot', 'exec'), scope)
    return scope['source_guard']()


def run():
    scope = dict(vars(original), __file__=__file__, OUT=OUT, SOURCE=SOURCE, INIT=INIT, OLD_INIT=OLD_INIT,
                 LUA=LUA, CONTROLLERS=CONTROLLERS, RAM=RAM, source_guard=source_guard, functions=functions)
    exec(compile(inspect.getsource(original.run), __file__ + '::whole_original_native_campaign', 'exec'), scope)
    return scope['run']()


if __name__ == '__main__':
    try:
        captured = run()
    except Exception as error:
        folder = OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        failure = dict(passed=False, error=repr(error), traceback=traceback.format_exc(),
                       fullPortAcceptance=False, goalStatus='active')
        if folder.exists():
            path = folder / 'current_capture_failure.json'; need(not path.exists(), 'Preserve actual outcome')
            path.write_text(json.dumps(failure, indent=2) + '\n')
        print(json.dumps(failure, indent=2), flush=True)
    code.interact(banner='Same full current Sonya campaign; original physical jump feedback with bound reader.', local=dict(RAM=RAM))
