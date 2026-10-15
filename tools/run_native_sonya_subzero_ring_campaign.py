"""Full current Sonya campaign/ending/fresh join; native Sub-Zero Ring inputs.

Prior actual failed policies and successful earned opponents remain frozen.
Reuse the whole original initializer/host/guest and no-assistance controls.
Only Sub-Zero receives the complete established Ring strategy. All14 natural
integration requirements and6 remaining groups remain the final objective.
"""
import code
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
from types import SimpleNamespace
import capture_native_paired_stumble_campaign as core
import prepare_native_mileena_guard_campaign as previous

ROOT, need, sha = core.ROOT, core.need, core.sha
OUT = ROOT / 'audit_native_sonya_subzero_ring_campaign_ram'
SOURCE = ROOT / 'audit_native_sonya_subzero_ring_campaign_source'
INIT = ROOT / 'audit_native_sonya_subzero_ring_campaign_initializer'
OLD_INIT = ROOT / 'audit_native_sonya_subzero_ring_campaign_previous_initializer'
LUA = 'mk2ks_native_paired_stumble_subzero_ring.lua'
CONTROLLERS = list(dict.fromkeys((LUA, *previous.CONTROLLERS)))
RAM = {}


def once(source, before, after):
    need(source.count(before) == 1, 'Whole original host, one exact boundary: ' + before[:100])
    return source.replace(before, after, 1)


def functions(provider):
    scope, host = core.base.functions(provider)
    host = once(host, 'images=RAM_IMAGES;preview_seen=set();',
                'images=RAM_IMAGES;preview_seen=set();late_stage_seen=set();')
    host = once(host,
        "bool(re.fullmatch(r'campaign_fight_selection\\d+_stage(?:7|8|15|16)\\.png',name)) or",
        "bool(re.fullmatch(r'campaign_fight_selection\\d+_stage(?:7|8|15|16)\\.png',name)) or\n"
        "      (bool(re.fullmatch(r'campaign_fight_selection\\d+_stage(?:11|12|13|14)\\.png',name)) and name.rsplit('_stage',1)[1] not in late_stage_seen) or")
    host = once(host, "preview_seen.add(fields['sha256']);images[name]=image;raw_images[name]=raw",
        "preview_seen.add(fields['sha256']);images[name]=image;raw_images[name]=raw;need(len(images)<=64,'Bounded original campaign rasters held only in RAM')\n"
        "      if re.fullmatch(r'campaign_fight_selection\\d+_stage(?:11|12|13|14)\\.png',name):late_stage_seen.add(name.rsplit('_stage',1)[1])")
    scope.update(__file__=__file__, OUT=OUT, LUA=LUA, CONTROLLERS=CONTROLLERS)
    exec(compile(host, __file__ + '::entire_original_full_host_bounded_late_stage_rasters', 'exec'), scope)
    return scope, host


def source_guard():
    need(not OUT.exists() and not SOURCE.exists() and not core.base.census.census(),
         'Fresh full campaign after prior exact process/RAM retirement; no live run restarted')
    paths = [ROOT / 'audit_native_mileena_guard_losing_subzero_preserved/report.json',
             ROOT / 'audit_native_mileena_guard_losing_subzero_retirement/report.json',
             ROOT / 'audit_native_mileena_guard_earned_clear_checked/report.json',
             previous.SOURCE / 'report.json',
             ROOT / 'audit_v5686_sonya_p2_subzero_ring_retries_checked/report.json',
             ROOT / 'audit_native_kano_raiden_shared_rejoin_checked/report.json']
    failed, retired, mileena, old, ring, recovery = [json.loads(path.read_text()) for path in paths]
    need(not failed['passed'] and failed['preservationPassed'] and retired['passed'] and
         failed['statistics']['lossesByStage']['11'] == 49 and
         failed['statistics']['ownWinReadsByStage']['11'] == 2 and
         failed['statistics']['nativeGlobalCacheFailureRows'] == 0 and
         mileena['passed'] and mileena['finiteNativeSonyaMileenaClearAccepted'] and
         old['passed'] and ring['passed'] and ring['actualSubZeroAdvanceAccepted'] and
         ring['native']['actualFinalMatchOwnRoundWins'] == 2 and
         ring['native']['actualFinalMatchCpuRoundWins'] == 0 and recovery['passed'] and
         recovery['finiteSingleKanoRaidenVictimAndOrdinaryPaidRecoveryAccepted'],
         'Actual failed current Sub-Zero policy and finite previous native Ring success retained; no cross-build acceptance')
    pins = {}
    for proof in (failed, retired, mileena, old, ring, recovery):
        need(not proof['fullPortAcceptance'], 'Every previous finite scope remains finite')
        for path, digest in proof['inputHashes'].items():
            need(sha(path) == digest and (path not in pins or pins[path] == digest),
                 'All previous native/physical/source evidence immutable: ' + path)
            pins[path] = digest
    wrapper = (ROOT / LUA).read_text()
    need(wrapper.count('ranged=ring_once(') == 3 and
         "replacement=ranged..'\\n'..replacement" in wrapper and
         "ranged,'(other.roster==5 or other.roster==10)','other.roster==8'" in wrapper and
         "ranged,'(target.roster~=5 and target.roster~=10)','target.roster~=8'" in wrapper and
         "ranged,'(target.roster==5 and target.id~=5)','target.id~=8'" in wrapper and
         ':set_value(' not in wrapper and ':clear_value(' not in wrapper and 'manager.machine:exit()' not in wrapper,
         'Complete late original Ring clone, exactly native CPU8 eligibility/observer changes, no direct controls or exits')
    base = (ROOT / 'mk2ks_sonya_extended_guard_base_ram_v5201.lua').read_text()
    begin = base.index("   elseif strategy=='guard_punish' and (other.roster==5 or other.roster==10) then")
    end = base.index("\n   elseif strategy==", begin + 1)
    ranged = base[begin:end]
    for before, after in [('(other.roster==5 or other.roster==10)', 'other.roster==8'),
                          ('(target.roster~=5 and target.roster~=10)', 'target.roster~=8'),
                          ('(target.roster==5 and target.id~=5)', 'target.id~=8')]:
        ranged = once(ranged, before, after)
    need("age>=2 and age<5" in ranged and "age>=7 and age<10" in ranged and
         "age>=8 and age<12" in ranged and "gap<150" in ranged and
         "target.id~=8" in ranged and "target.owner~=target.actor" in ranged,
         'Whole existing Ring timings/retreat/passive actor/Main ownership intact')
    for name in CONTROLLERS:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',
                           (ROOT / name).read_text()), 'Every transitive source is normal input/passive only: ' + name)
    metadata_path = ROOT / core.NAME / 'build-info.json'
    metadata = json.loads(metadata_path.read_text(encoding='utf-8-sig'))
    provider = SimpleNamespace(GUEST_SHA=metadata['expected_guest_sha256'],
                               EXE_SHA=metadata['executable_sha256'], PAYLOAD_SHA=metadata['payload_sha256'])
    _, host = functions(provider)
    need("MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='1'" in host and
         "MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000'" in host and "'-str','18100'" in host and
         "'-nocheat'" in host and "'-wavwrite','NUL'" in host and
         len(old['originalNaturalIntegrationRequirements']) == 14 and len(old['originalRemainingWorkGroups']) == 6,
         'Full original Sonya tower/boss/ending/fresh-join host and18000-second deadline, no audio file copies')
    for path in (Path(__file__).resolve(), Path(core.__file__), Path(previous.__file__),
                 metadata_path, core.GUARD, *paths, *(ROOT / name for name in CONTROLLERS)):
        pins[str(path.resolve())] = sha(path)
    report = dict(passed=True, sourceOnlyAccepted=True, nativeGameplayAccepted=False,
                  currentCandidate=core.NAME, physicalCPUContextChanged=8,
                  physicalPolicy='Whole established Ring spacing/retreat routine takes priority only against native Sub-Zero8; all other opponents, bosses, ending and fresh join retained.',
                  originalObservationDeadlineSeconds=18000, wholeExpectedGuestByteDelta=79,
                  priorFailedCurrentSubZeroPolicyPreserved=True, priorOtherBuildRingNotPromoted=True,
                  boundedOriginalScreens=64, originalNaturalIntegrationRequirements=old['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=old['originalRemainingWorkGroups'], inputHashes=pins,
                  completeOriginalRingBranchSHA256=hashlib.sha256(ranged.encode()).hexdigest().upper(),
                  wholeGeneratedHostSHA256=hashlib.sha256(host.encode()).hexdigest().upper(),
                  fullTowerAccepted=False, endingAccepted=False, freshJoinAccepted=False, audioAccepted=False,
                  fullPortAcceptance=False, newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0, goalStatus='active')
    SOURCE.mkdir(); (SOURCE / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def run():
    scope = dict(vars(core), __file__=__file__, OUT=OUT, SOURCE=SOURCE, INIT=INIT, OLD_INIT=OLD_INIT,
                 LUA=LUA, CONTROLLERS=CONTROLLERS, RAM=RAM, source_guard=source_guard, functions=functions)
    exec(compile(inspect.getsource(core.expectation), __file__ + '::whole_original79_byte_initializer', 'exec'), scope)
    body = once(inspect.getsource(core.run), '    source_guard()', '    guard=source_guard()')
    body = once(body, '    scope, host = base.functions(provider)', '    scope, host = functions(provider)')
    body = once(body, '    return captured',
                "    need(not base.census.census() and all(sha(path)==digest for path,digest in guard['inputHashes'].items()), 'Same original native terminal and all full source pins intact')\n    return captured")
    exec(compile(body, __file__ + '::whole_original_full_native_campaign', 'exec'), scope)
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
    code.interact(banner='Same full current Sonya campaign, native Sub-Zero Ring trial; full goal open.', local=dict(RAM=RAM))
