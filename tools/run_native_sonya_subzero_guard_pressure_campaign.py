"""Complete current campaign; new ordinary guard/early leg inputs at CPU8.

Do not alter native AI, HP, RNG, collision, guest state, campaign/ending/join
or preceding opponents. Bind the entire actual failed retreat and diagnosis.
"""
import code
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
from types import SimpleNamespace
import run_native_sonya_subzero_ring_campaign as original
import run_native_sonya_subzero_retreat_retry_bound_campaign as previous

core = original.core
ROOT, need, sha = original.ROOT, original.need, original.sha
OUT = ROOT/'audit_native_sonya_subzero_guard_pressure_campaign_ram'
SOURCE = ROOT/'audit_native_sonya_subzero_guard_pressure_campaign_source'
INIT = ROOT/'audit_native_sonya_subzero_guard_pressure_campaign_initializer'
OLD_INIT = ROOT/'audit_native_sonya_subzero_guard_pressure_campaign_previous_initializer'
LUA = 'mk2ks_native_paired_stumble_subzero_guard_pressure.lua'
CONTROLLERS = list(dict.fromkeys((LUA,*original.CONTROLLERS)))
RAM = {}


def functions(provider):
    scope = dict(vars(original), __file__=__file__, OUT=OUT, LUA=LUA, CONTROLLERS=CONTROLLERS)
    exec(compile(inspect.getsource(original.functions), __file__+'::whole_original_full_bounded_host', 'exec'), scope)
    return scope['functions'](provider)


def source_guard():
    need(not OUT.exists() and not SOURCE.exists() and not core.base.census.census(),
         'Fresh materially changed physical trial only after exact failed game/RAM retirement')
    paths = [previous.SOURCE/'report.json',
             ROOT/'audit_native_sonya_subzero_retreat_retry_policy_preserved/report.json',
             ROOT/'audit_native_sonya_subzero_retreat_retry_policy_retirement/report.json',
             ROOT/'audit_native_subzero_retreat_retry_preceding_campaign_checked/report.json',
             ROOT/'audit_native_subzero_retreat_retry_loss_diagnosed/report.json']
    old, failed, retired, preceding, diagnosed = [json.loads(path.read_text()) for path in paths]
    need(old['passed'] and failed['preservationPassed'] and not failed['passed'] and retired['passed'] and
         preceding['passed'] and preceding['accepted']['completedOpponents']==11 and
         preceding['accepted']['completeOriginalRows']==785698 and
         len(preceding['allObservedCategoryFaultsRejected'])==48 and
         diagnosed['diagnosisCompleted'] and not diagnosed['gameplayAccepted'] and
         diagnosed['counts']['LOSS']==failed['statistics']['lossesByStage']['11']==32 and
         diagnosed['nativeHumanActionStores']['776']==1196 and
         diagnosed['nativeHumanActionStores']['512']==1025 and
         diagnosed['actualFrozenFields']==10703 and all(row['slot']=='2' for row in diagnosed['allActualWins']),
         'Every actual failed native jump/airkick/freeze and32 full terminal losses retained; not failed activation')
    pins = {}
    for proof in (old, failed, retired, preceding, diagnosed):
        need(not proof['fullPortAcceptance'], 'Whole objective remains unaccepted')
        for path,digest in proof['inputHashes'].items():
            need(sha(path)==digest and (path not in pins or pins[path]==digest), 'Frozen original evidence unchanged: '+path)
            pins[path]=digest
    wrapper = (ROOT/LUA).read_text()
    need("local path='mk2ks_native_paired_stumble_subzero_ring.lua'" in wrapper and
         wrapper.count('ranged=ranged:sub(1,input_begin-1)..physical..ranged:sub(input_end)')==1 and
         'local physical=[=================[' in wrapper and '\n]=================]\n' in wrapper and
         'local after=[===================[' in wrapper and '\n]===================]\n' in wrapper and
         'other.action==0x604 and feedback.last_cpu~=0x604' in wrapper and
         'feedback.guard_until=frame+45' in wrapper and 'ready and gap<115' in wrapper and
         'age>=3 and age<7' in wrapper and 'frame-feedback.last_leg>=32' in wrapper and
         'human.action==0x308 or human.action==0x200' in wrapper and
         ':set_value(' not in wrapper and ':clear_value(' not in wrapper and
         'manager.machine:exit()' not in wrapper,
         'Only visibly owned freeze guard and earlier native leg button edges; isolated nested strings, passive observers retained')
    for name in CONTROLLERS:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',
                           (ROOT/name).read_text()), 'Every loaded source normal controls/passive only: '+name)
    metadata_path = ROOT/core.NAME/'build-info.json'
    metadata = json.loads(metadata_path.read_text(encoding='utf-8-sig'))
    provider = SimpleNamespace(GUEST_SHA=metadata['expected_guest_sha256'],
                               EXE_SHA=metadata['executable_sha256'], PAYLOAD_SHA=metadata['payload_sha256'])
    _, host = functions(provider)
    need("MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='1'" in host and
         "MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000'" in host and "'-str','18100'" in host and
         "'-nocheat'" in host and "'-wavwrite','NUL'" in host and
         len(old['originalNaturalIntegrationRequirements'])==14 and len(old['originalRemainingWorkGroups'])==6,
         'Whole current79-byte candidate/full original tower/boss/ending/fresh join host and original scope')
    for path in (Path(__file__).resolve(), Path(original.__file__), Path(previous.__file__),
                 Path(core.__file__), metadata_path, core.GUARD, *paths, *(ROOT/name for name in CONTROLLERS)):
        pins[str(path.resolve())]=sha(path)
    report = dict(passed=True,sourceOnlyAccepted=True,nativeGameplayAccepted=False,currentCandidate=core.NAME,
        physicalCPUContextChanged=8,
        physicalPolicy='Guard actual freeze startup45 fields, attempt real D/LP+Block leg at gap<115 before native throw spacing. Native contact decides hits. Entire earlier/boss/ending/join/native rules unchanged.',
        wholeGeneratedHostSHA256=hashlib.sha256(host.encode()).hexdigest().upper(),
        originalObservationDeadlineSeconds=18000,wholeExpectedGuestByteDelta=79,boundedOriginalScreens=64,
        originalNaturalIntegrationRequirements=old['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=old['originalRemainingWorkGroups'],inputHashes=pins,
        fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False,artAccepted=False,audioAccepted=False,
        fullPortAcceptance=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    SOURCE.mkdir(); (SOURCE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def run():
    scope = dict(vars(original), __file__=__file__, OUT=OUT,SOURCE=SOURCE,INIT=INIT,OLD_INIT=OLD_INIT,
                 LUA=LUA,CONTROLLERS=CONTROLLERS,RAM=RAM,source_guard=source_guard,functions=functions)
    exec(compile(inspect.getsource(original.run), __file__+'::whole_original_full_current_campaign', 'exec'), scope)
    return scope['run']()


if __name__=='__main__':
    try:
        captured=run()
    except Exception as error:
        folder=OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False,goalStatus='active')
        if folder.exists():
            path=folder/'current_capture_failure.json';need(not path.exists(),'Retain actual frozen outcome')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Complete current Sonya tower; physical guard/early-leg pressure only.',local=dict(RAM=RAM))
