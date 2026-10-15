"""Full current campaign; change only ordinary CPU1 controls after twelve wins.

The complete successful CPU8 inputs, native game, AI, HP, collision, RNG,
initializer, tower, bosses, ending, fresh join and bounded RAM capture stay.
"""
import code
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
from types import SimpleNamespace
import run_native_sonya_subzero_guard_pressure_campaign as previous

original = previous.original
core = original.core
ROOT, need, sha = original.ROOT, original.need, original.sha
OUT = ROOT/'audit_native_sonya_liu_early_leg_campaign_ram'
SOURCE = ROOT/'audit_native_sonya_liu_early_leg_campaign_source'
INIT = ROOT/'audit_native_sonya_liu_early_leg_campaign_initializer'
OLD_INIT = ROOT/'audit_native_sonya_liu_early_leg_campaign_previous_initializer'
LUA = 'mk2ks_native_paired_stumble_liu_early_leg.lua'
CONTROLLERS = list(dict.fromkeys((LUA,*previous.CONTROLLERS)))
RAM = {}


def functions(provider):
    scope = dict(vars(original), __file__=__file__, OUT=OUT, LUA=LUA, CONTROLLERS=CONTROLLERS)
    exec(compile(inspect.getsource(original.functions), __file__+'::whole_original_full_bounded_host', 'exec'), scope)
    return scope['functions'](provider)


def source_guard():
    need(not OUT.exists() and not SOURCE.exists() and not core.base.census.census(),
         'Fresh CPU1-only input trial after original failed game/RAM retirement')
    paths = [previous.SOURCE/'report.json',
             ROOT/'audit_native_subzero_guard_pressure_preceding_campaign_checked/report.json',
             ROOT/'audit_native_subzero_guard_pressure_earned_clear_phase_bound_checked/report.json',
             ROOT/'audit_native_sonya_liu_original_policy_preserved/report.json',
             ROOT/'audit_native_sonya_liu_original_policy_retirement/report.json',
             ROOT/'audit_native_sonya_liu_original_policy_loss_diagnosed/report.json']
    old, preceding, cleared, failed, retired, diagnosed = [json.loads(path.read_text()) for path in paths]
    need(old['passed'] and preceding['passed'] and preceding['accepted']['completedOpponents']==11 and
         preceding['accepted']['completeOriginalRows']==785698 and
         cleared['passed'] and cleared['finiteNativeSonyaSubZeroClearAccepted'] and
         cleared['accepted']['ownSuccessfulRoundFrames']==[388387,390990] and
         cleared['accepted']['actualOwnedLegEntries']==392 and
         failed['preservationPassed'] and not failed['passed'] and retired['passed'] and
         failed['statistics']['lossesByStage']['12']==143 and
         failed['statistics']['ownWinReadsByStage']['12']==4 and
         diagnosed['diagnosisCompleted'] and not diagnosed['gameplayAccepted'] and
         diagnosed['counts']['SPECIAL']==797,
         'Entire earlier eleven/SubZero earned clear and actual 143-loss/four-round Liu failure retained')
    pins = {}
    for proof in (old, preceding, cleared, failed, retired, diagnosed):
        need(not proof['fullPortAcceptance'], 'Full natural-integration objective remains open')
        for path,digest in proof['inputHashes'].items():
            need(sha(path)==digest and (path not in pins or pins[path]==digest), 'All frozen evidence unchanged: '+path)
            pins[path]=digest
    wrapper = (ROOT/LUA).read_text()
    need("local path='mk2ks_native_paired_stumble_subzero_guard_pressure.lua'" in wrapper and
         "replacement=ranged..'\\n'..liu_range..'\\n'..replacement" in wrapper and
         wrapper.count("liu_range=ring_once(")==7 and
         "tostring(observed_main)..':liu1'" in wrapper and
         wrapper.count("'liu_early_leg_inputs'")==2 and
         ':set_value(' not in wrapper and ':clear_value(' not in wrapper and
         'manager.machine:exit()' not in wrapper,
         'Whole original SubZero branch retained; isolated true CPU1 clone/history/tap keys, no freeze ordinal inference')
    for name in CONTROLLERS:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',
                           (ROOT/name).read_text()), 'Every loaded controller physical inputs/passive reads only: '+name)
    metadata_path = ROOT/core.NAME/'build-info.json'
    metadata = json.loads(metadata_path.read_text(encoding='utf-8-sig'))
    provider = SimpleNamespace(GUEST_SHA=metadata['expected_guest_sha256'],
                               EXE_SHA=metadata['executable_sha256'], PAYLOAD_SHA=metadata['payload_sha256'])
    _, host = functions(provider)
    need("MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='1'" in host and
         "MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000'" in host and "'-str','18100'" in host and
         "'-nocheat'" in host and "'-wavwrite','NUL'" in host and
         len(old['originalNaturalIntegrationRequirements'])==14 and len(old['originalRemainingWorkGroups'])==6,
         'Whole current79-byte candidate/full tower/boss/ending/fresh join host and original scope')
    for path in (Path(__file__).resolve(), Path(previous.__file__), Path(original.__file__),
                 Path(core.__file__), metadata_path, core.GUARD, *paths, *(ROOT/name for name in CONTROLLERS)):
        pins[str(path.resolve())]=sha(path)
    report = dict(passed=True,sourceOnlyAccepted=True,nativeGameplayAccepted=False,currentCandidate=core.NAME,
        physicalCPUContextChanged=1,successfulEarlierTwelvePhysicalInputsRetained=True,
        precedingExclusiveNativeBoundary=391498,expectedCompleteEarlierTwelveRows=1001809,
        physicalPolicy='CPU1-only clone attempts genuine Down/LP+Block leg at gap115 with native readiness/flight/anti-air observations. Original CPU8 branch and all earlier inputs retained. No CPU1 freeze ordinal inference. Native contact alone decides hit.',
        passiveTapKeysSeparatedByCPUContext=True,
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
            path=folder/'current_capture_failure.json';need(not path.exists(),'Preserve original actual outcome')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Complete current Sonya campaign; CPU1-only earlier normal leg inputs.',local=dict(RAM=RAM))
