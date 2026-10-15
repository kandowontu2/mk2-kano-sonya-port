"""Whole failed retreat host successor; only nested string delimiters changed."""
import code
import inspect
import json
import traceback
from pathlib import Path
import run_native_sonya_subzero_retreat_retry_campaign as original

ROOT, need, sha = original.ROOT, original.need, original.sha
OUT = ROOT/'audit_native_sonya_subzero_retreat_retry_bound_campaign_ram'
SOURCE = ROOT/'audit_native_sonya_subzero_retreat_retry_bound_campaign_source'
INIT = ROOT/'audit_native_sonya_subzero_retreat_retry_bound_campaign_initializer'
OLD_INIT = ROOT/'audit_native_sonya_subzero_retreat_retry_bound_campaign_previous_initializer'
LUA = 'mk2ks_native_paired_stumble_subzero_retreat_retry_bound.lua'
CONTROLLERS = list(dict.fromkeys((LUA,*original.CONTROLLERS)))
RAM = {}


def failed_boot_pins():
    paths=[ROOT/'audit_native_subzero_retreat_retry_boot_failure_preserved/report.json',
           ROOT/'audit_native_subzero_retreat_retry_boot_failure_retired/report.json']
    failed,retired=[json.loads(path.read_text()) for path in paths]
    need(failed['preservationPassed'] and not failed['passed'] and failed['originalNativeExit']==3 and
         failed['actualGuestNotVerified'] and retired['passed'] and retired['retirementOnlyAccepted'],
         'Actual pre-game nested delimiter failure retained and exact original RAM parent retired')
    pins={}
    for proof in (failed,retired):
        for path,digest in proof['inputHashes'].items():
            need(sha(path)==digest and (path not in pins or pins[path]==digest),'Every actual failed boot/source unchanged')
            pins[path]=digest
    wrapper=(ROOT/LUA).read_text()
    need("local path='mk2ks_native_paired_stumble_subzero_retreat_retry.lua'" in wrapper and
         wrapper.count("once('local physical=[==[','local physical=[=================[')")==1 and
         wrapper.count("once('\\n]==]\\nranged=','\\n]=================]\\nranged=')")==1 and
         ':set_value(' not in wrapper and ':clear_value(' not in wrapper and 'manager.machine:exit()' not in wrapper,
         'Exactly two matching delimiters corrected; all ordinary feedback/native rules unchanged')
    for path in (Path(original.__file__),*paths):pins[str(path.resolve())]=sha(path)
    return pins


def functions(provider):
    scope=dict(vars(original),__file__=__file__,OUT=OUT,LUA=LUA,CONTROLLERS=CONTROLLERS)
    exec(compile(inspect.getsource(original.functions),__file__+'::whole_original_full_host','exec'),scope)
    return scope['functions'](provider)


def source_guard():
    body=inspect.getsource(original.source_guard)
    once=original.previous.original.previous.once
    body=once(body,'    pins = {}','    pins = failed_boot_pins()')
    body=once(body,'    wrapper=(ROOT/LUA).read_text()','    wrapper=(ROOT/original.LUA).read_text()')
    body=once(body,'report=dict(passed=True,sourceOnlyAccepted=True,',
                   'report=dict(delimiterBindingOnlyChanged=True,actualFailedBootPreserved=True,passed=True,sourceOnlyAccepted=True,')
    scope=dict(vars(original),__file__=__file__,original=original,OUT=OUT,SOURCE=SOURCE,LUA=LUA,
               CONTROLLERS=CONTROLLERS,functions=functions,failed_boot_pins=failed_boot_pins)
    exec(compile(body,__file__+'::whole_original_source_guard_and_actual_failed_boot','exec'),scope)
    return scope['source_guard']()


def run():
    scope=dict(vars(original),__file__=__file__,OUT=OUT,SOURCE=SOURCE,INIT=INIT,OLD_INIT=OLD_INIT,
               LUA=LUA,CONTROLLERS=CONTROLLERS,RAM=RAM,source_guard=source_guard,functions=functions)
    exec(compile(inspect.getsource(original.run),__file__+'::whole_original_full_native_campaign','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try:
        captured=run()
    except Exception as error:
        folder=OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False,goalStatus='active')
        if folder.exists():
            path=folder/'current_capture_failure.json';need(not path.exists(),'Retain actual original outcome')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Same complete Sonya campaign; early retreat physical retry with isolated string binding.',local=dict(RAM=RAM))
