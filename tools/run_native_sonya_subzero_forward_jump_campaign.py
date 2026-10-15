"""Whole current campaign with existing forward jump-kick inputs at SubZero.

All real failed Ring outcomes stay failed. No AI, damage, native state,
schedule, guest, ending, join or earlier-opponent policy changes.
"""
import code
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
from types import SimpleNamespace
import run_native_sonya_subzero_ring_campaign as previous

core = previous.core
ROOT, need, sha = previous.ROOT, previous.need, previous.sha
OUT = ROOT / 'audit_native_sonya_subzero_forward_jump_campaign_ram'
SOURCE = ROOT / 'audit_native_sonya_subzero_forward_jump_campaign_source'
INIT = ROOT / 'audit_native_sonya_subzero_forward_jump_campaign_initializer'
OLD_INIT = ROOT / 'audit_native_sonya_subzero_forward_jump_campaign_previous_initializer'
LUA = 'mk2ks_native_paired_stumble_subzero_forward_jump.lua'
CONTROLLERS = list(dict.fromkeys((LUA, *previous.CONTROLLERS,
                                 'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua')))
RAM = {}


def functions(provider):
    scope = dict(vars(previous), __file__=__file__, OUT=OUT, LUA=LUA, CONTROLLERS=CONTROLLERS)
    exec(compile(inspect.getsource(previous.functions), __file__ + '::whole_original_bounded_campaign_host', 'exec'), scope)
    return scope['functions'](provider)


def source_guard():
    need(not OUT.exists() and not SOURCE.exists() and not core.base.census.census(),
         'Fresh successor only after actual failed trial terminal/RAM retirement')
    paths = [previous.SOURCE / 'report.json',
             ROOT / 'audit_native_sonya_subzero_ring_policy_preserved/report.json',
             ROOT / 'audit_native_sonya_subzero_ring_policy_retirement/report.json',
             ROOT / 'audit_native_subzero_ring_preceding_campaign_checked/report.json',
             ROOT / 'audit_native_subzero_ring_loss_diagnosed/report.json']
    old, failed, retired, preceding, diagnosed = [json.loads(path.read_text()) for path in paths]
    need(old['passed'] and failed['preservationPassed'] and not failed['passed'] and retired['passed'] and
         preceding['passed'] and preceding['accepted']['completedOpponents'] == 11 and
         diagnosed['diagnosisCompleted'] and not diagnosed['gameplayAccepted'] and
         diagnosed['counts']['SPECIAL'] == 442 and len(diagnosed['allActualLosses']) == 37 and
         all(row['slot'] == '2' for row in diagnosed['allActualWins']),
         'Actual unsuccessful Ring activation/37 paid losses retained; prior eleven fights not weakened')
    pins = {}
    for proof in (old, failed, retired, preceding, diagnosed):
        need(not proof['fullPortAcceptance'], 'All finite earlier evidence stays finite')
        for path, digest in proof['inputHashes'].items():
            need(sha(path) == digest and (path not in pins or pins[path] == digest),
                 'Every actual earlier source/outcome unchanged: ' + path)
            pins[path] = digest
    wrapper = (ROOT / LUA).read_text()
    need(wrapper.count('local feedback=common:sub(') == 1 and
         "local path='mk2ks_native_paired_stumble_subzero_ring.lua'" in wrapper and
         "ranged=ranged:sub(1,input_begin-1)" in wrapper and
         "..feedback..'\\n'..ranged:sub(input_end)" in wrapper and
         ':set_value(' not in wrapper and ':clear_value(' not in wrapper and 'manager.machine:exit()' not in wrapper,
         'One whole existing input feedback clone, passive observers and earlier campaign retained')
    common = (ROOT / 'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua').read_text()
    begin = common.index('    -- Read-only feedback: jump from actual grounded state')
    end = common.index('    previous_y=human.y', begin) + len('    previous_y=human.y')
    feedback = common[begin:end]
    need("if gap<115 and height<90 and(age>=9 or descending)then" in feedback and
         "elseif cpu_height>12 and gap<105 then" in feedback and "elseif gap<47 then" in feedback and
         "elseif frame-last_jump>=38 then" in feedback,
         'Entire original actual-height forward jump/contact/anti-air/close uppercut/block timings unchanged')
    for name in CONTROLLERS:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',
                           (ROOT / name).read_text()), 'All transitive controllers are physical/passive: ' + name)
    metadata_path = ROOT / core.NAME / 'build-info.json'
    metadata = json.loads(metadata_path.read_text(encoding='utf-8-sig'))
    provider = SimpleNamespace(GUEST_SHA=metadata['expected_guest_sha256'],
                               EXE_SHA=metadata['executable_sha256'], PAYLOAD_SHA=metadata['payload_sha256'])
    _, host = functions(provider)
    need("MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='1'" in host and
         "MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000'" in host and "'-str','18100'" in host and
         "'-nocheat'" in host and "'-wavwrite','NUL'" in host and
         len(old['originalNaturalIntegrationRequirements']) == 14 and len(old['originalRemainingWorkGroups']) == 6,
         'Complete original tower/endings/fresh join/79-byte candidate and all14 requirements/six groups')
    for path in (Path(__file__).resolve(), Path(previous.__file__), Path(core.__file__), metadata_path,
                 core.GUARD, *paths, *(ROOT / name for name in CONTROLLERS)):
        pins[str(path.resolve())] = sha(path)
    report = dict(passed=True, sourceOnlyAccepted=True, nativeGameplayAccepted=False,
                  currentCandidate=core.NAME, physicalCPUContextChanged=8,
                  physicalPolicy='Only native SubZero8: whole original forward jumpkick/contact/uppercut/block feedback replaces failed Ring controls; passive observers and all earlier/boss/ending/join branches retained.',
                  completeOriginalFeedbackSHA256=hashlib.sha256(feedback.encode()).hexdigest().upper(),
                  wholeGeneratedHostSHA256=hashlib.sha256(host.encode()).hexdigest().upper(),
                  originalObservationDeadlineSeconds=18000, wholeExpectedGuestByteDelta=79,
                  originalNaturalIntegrationRequirements=old['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=old['originalRemainingWorkGroups'], inputHashes=pins,
                  fullTowerAccepted=False, endingAccepted=False, freshJoinAccepted=False, audioAccepted=False,
                  fullPortAcceptance=False, newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0, goalStatus='active')
    SOURCE.mkdir(); (SOURCE / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def run():
    scope = dict(vars(previous), __file__=__file__, OUT=OUT, SOURCE=SOURCE, INIT=INIT, OLD_INIT=OLD_INIT,
                 LUA=LUA, CONTROLLERS=CONTROLLERS, RAM=RAM, source_guard=source_guard, functions=functions)
    exec(compile(inspect.getsource(previous.run), __file__ + '::whole_original_native_campaign', 'exec'), scope)
    return scope['run']()


if __name__ == '__main__':
    try:
        captured = run()
    except Exception as error:
        folder = OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        failure = dict(passed=False, error=repr(error), traceback=traceback.format_exc(),
                       fullPortAcceptance=False, goalStatus='active')
        if folder.exists():
            path = folder / 'current_capture_failure.json'; need(not path.exists(), 'Keep original actual outcome')
            path.write_text(json.dumps(failure, indent=2) + '\n')
        print(json.dumps(failure, indent=2), flush=True)
    code.interact(banner='Same complete current Sonya campaign; native SubZero forward jump trial, full objective open.', local=dict(RAM=RAM))
