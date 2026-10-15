"""Full original ordinary-input victim/rejoin trial, shared passive Lua signal.

All previous failures stay frozen. No guest state, AI, health or RNG writes;
no weakening of full-health admission or 500 live native-field checks.
"""
import code
import inspect
import json
import traceback
from pathlib import Path
import run_native_kano_raiden_paired_victim as original

ROOT, need, sha, once = original.ROOT, original.need, original.sha, original.once
OUT = ROOT / 'audit_native_kano_raiden_paired_victim_shared_ram'
SOURCE = ROOT / 'audit_native_kano_raiden_paired_victim_shared_source'
INIT = ROOT / 'audit_native_kano_raiden_paired_victim_shared_initializer'
OLD_INIT = ROOT / 'audit_native_kano_raiden_paired_victim_shared_previous_initializer'
LUA = 'mk2ks_native_kano_raiden_victim_shared_provenance.lua'
NEW = (LUA, 'mk2ks_native_kano_raiden_victim_approach_cache.lua',
       'mk2ks_native_kano_raiden_victim_approach_driver.lua')
CONTROLLERS = list(dict.fromkeys((*NEW, *original.CONTROLLERS)))
RAM = {}


def namespace():
    return dict(vars(original), __file__=__file__, OUT=OUT, SOURCE=SOURCE,
                INIT=INIT, OLD_INIT=OLD_INIT, LUA=LUA, NEW=NEW,
                CONTROLLERS=CONTROLLERS, RAM=RAM, source_guard=source_guard,
                functions=functions)


def functions(provider):
    scope = namespace()
    exec(compile(inspect.getsource(original.functions),
                 __file__ + '::entire_original_native_capture', 'exec'), scope)
    return scope['functions'](provider)


def source_guard():
    receipt_folder = ROOT / 'audit_native_kano_raiden_paired_victim_notification_checked'
    failure_path = receipt_folder / 'failed_full_notification_trial.json'
    retirement_path = receipt_folder / 'single_handoff_and_failed_notification_ram_retirement.json'
    failure, retirement = (json.loads(path.read_text()) for path in (failure_path, retirement_path))
    need(not failure['passed'] and not failure['originalIntendedKanoVictimAndPaidRejoinAccepted'] and
         failure['actualPostStateFields'] == 0 and retirement['passed'] and
         retirement['finiteSingleKanoRaidenNativeHandoffAccepted'] and
         not retirement['originalIntendedPaidRejoinTrialAccepted'] and
         retirement['originalCaptureRAMCleared'] and not retirement['fullPortAcceptance'],
         'Actual native target and failed full notification trial retained, not relabelled')
    prior_pins = {}
    for proof in (failure, retirement):
        for path, digest in proof['inputHashes'].items():
            need(sha(path) == digest and (path not in prior_pins or prior_pins[path] == digest),
                 'All frozen native/failure/source evidence unchanged: ' + path)
            prior_pins[path] = digest
    before = (ROOT / 'mk2ks_native_kano_raiden_victim_approach_provenance.lua').read_text()
    after = (ROOT / LUA).read_text()
    expected = once(before,
        '-- Whole original paired observer, true Kano target and ordinary driver only.',
        '-- Whole original paired observer; explicitly share the passive Lua notification.')
    expected = once(expected,
        "once('pending={frame=frame}','pending={frame=frame};MK2KS_KANO_PAIRED_CALLBACK=frame')",
        '''once('pending={frame=frame}',"pending={frame=frame};rawset(_G,'MK2KS_KANO_PAIRED_CALLBACK',frame)")''')
    need(after == expected, 'Entire original observer, only passive shared setter and explanatory comment')
    body = inspect.getsource(original.source_guard)
    body = once(body, "dofile('mk2ks_native_kano_raiden_victim_driver.lua')",
                "dofile('mk2ks_native_kano_raiden_victim_approach_driver.lua')")
    body = once(body, "'pending={frame=frame};MK2KS_KANO_PAIRED_CALLBACK=frame' in provenance",
                '''"pending={frame=frame};rawset(_G,'MK2KS_KANO_PAIRED_CALLBACK',frame)" in provenance''')
    body = once(body, "    SOURCE.mkdir()",
        "    report['inputHashes'].update(prior_pins)\n"
        "    for path in (failure_path, retirement_path, Path(original_file)):\n"
        "        report['inputHashes'][str(path.resolve())] = sha(path)\n"
        "    report['sharedPassiveLuaSignal'] = True\n"
        "    report['priorFailedFullTrialPreserved'] = True\n"
        "    report['physicalInputPolicy'] = 'Original first two opponents; forward walking without attacks against Raiden until native handoff, then original zoning/paid controls. No guest changes.'\n"
        "    SOURCE.mkdir()")
    scope = namespace()
    scope.update(prior_pins=prior_pins, failure_path=failure_path,
                 retirement_path=retirement_path, original_file=original.__file__)
    exec(compile(body, __file__ + '::entire_original_guard_shared_Lua_setter', 'exec'), scope)
    return scope['source_guard']()


def run():
    scope = namespace()
    exec(compile(inspect.getsource(original.run),
                 __file__ + '::entire_original_guest_and_native_trial', 'exec'), scope)
    return scope['run']()


if __name__ == '__main__':
    try:
        captured = run()
    except Exception as error:
        folder = OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        failure = dict(passed=False, error=repr(error), traceback=traceback.format_exc(),
                       fullPortAcceptance=False, goalStatus='active')
        if folder.exists():
            path = folder / 'current_capture_failure.json'
            need(not path.exists(), 'Keep actual full successor failure intact')
            path.write_text(json.dumps(failure, indent=2) + '\n')
        print(json.dumps(failure, indent=2), flush=True)
    code.interact(banner='Same original full native Kano victim/rejoin trial; no full-port claim.', local=dict(RAM=RAM))
