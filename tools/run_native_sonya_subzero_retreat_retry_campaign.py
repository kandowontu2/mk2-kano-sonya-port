"""Complete current campaign; source-bound throw evidence informs inputs only.

Earlier retreat/repeated Up edges replace failed38-field waits and Ring startup
only against native SubZero8. Every prior failed outcome, first eleven earned
fights, original native kernels, bosses, ending, fresh join and full goal stay.
"""
import code
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
from types import SimpleNamespace
import run_native_sonya_subzero_forward_jump_bound_campaign as previous

core = previous.original.core
ROOT, need, sha = previous.ROOT, previous.need, previous.sha
OUT = ROOT / 'audit_native_sonya_subzero_retreat_retry_campaign_ram'
SOURCE = ROOT / 'audit_native_sonya_subzero_retreat_retry_campaign_source'
INIT = ROOT / 'audit_native_sonya_subzero_retreat_retry_campaign_initializer'
OLD_INIT = ROOT / 'audit_native_sonya_subzero_retreat_retry_campaign_previous_initializer'
LUA = 'mk2ks_native_paired_stumble_subzero_retreat_retry.lua'
CONTROLLERS = list(dict.fromkeys((LUA, *previous.original.previous.CONTROLLERS)))
RAM = {}


def functions(provider):
    scope = dict(vars(previous), __file__=__file__, OUT=OUT, LUA=LUA, CONTROLLERS=CONTROLLERS)
    exec(compile(inspect.getsource(previous.functions), __file__ + '::whole_original_bounded_full_campaign_host', 'exec'), scope)
    return scope['functions'](provider)


def source_guard():
    need(not OUT.exists() and not SOURCE.exists() and not core.base.census.census(),
         'Fresh input successor only after original failed game/RAM retirement')
    paths = [previous.SOURCE/'report.json',
             ROOT/'audit_native_sonya_subzero_forward_jump_policy_preserved/report.json',
             ROOT/'audit_native_sonya_subzero_forward_jump_policy_retirement/report.json',
             ROOT/'audit_native_subzero_forward_jump_preceding_campaign_checked/report.json',
             ROOT/'audit_native_subzero_forward_jump_loss_diagnosed/report.json',
             ROOT/'audit_native_subzero_forward_jump_native_throws_checked/report.json']
    old, failed, retired, preceding, diagnosed, throws = [json.loads(p.read_text()) for p in paths]
    need(old['passed'] and failed['preservationPassed'] and not failed['passed'] and retired['passed'] and
         preceding['passed'] and preceding['accepted']['completedOpponents'] == 11 and
         preceding['accepted']['completeOriginalRows'] == 785698 and
         len(preceding['allObservedCategoryFaultsRejected']) == 48 and diagnosed['diagnosisCompleted'] and
         diagnosed['counts']['LOSS'] == 37 and all(row['slot']=='2' for row in diagnosed['allActualWins']) and
         throws['passed'] and throws['finiteNativeThrowDiagnosisAccepted'] and
         throws['actualOwnedNativeCpuThrows'] == throws['actualPairedNativeSonyaVictimClears'] == 344 and
         throws['wholeOriginalThrowCaptureJumpAirKickKernelsUnchanged'] and
         len(throws['semanticAndKernelFaultsRejected']) == 21,
         'Actual failed policy and every original native throw/owned victim pair retained; no game patch inferred')
    pins = {}
    for proof in (old,failed,retired,preceding,diagnosed,throws):
        need(not proof['fullPortAcceptance'], 'All finite prerequisites remain finite')
        for path,digest in proof['inputHashes'].items():
            need(sha(path)==digest and (path not in pins or pins[path]==digest), 'All actual prerequisites frozen: '+path)
            pins[path]=digest
    gaps=[abs(int(pair['sameNativeField']['h_x'])-int(pair['sameNativeField']['c_x'])) for pair in throws['nativePairs']]
    need(min(gaps)==61 and max(gaps)==77 and
         all(pair['sameNativeField']['h_y']==pair['sameNativeField']['h_floor'] for pair in throws['nativePairs']),
         'Every observed CPU throw actually began grounded at61..77 spacing, not its later damage/flight coordinates')
    wrapper=(ROOT/LUA).read_text()
    need("local path='mk2ks_native_paired_stumble_subzero_ring.lua'" in wrapper and
         wrapper.count('ranged=ranged:sub(1,input_begin-1)..physical..ranged:sub(input_end)')==1 and
         'human.action==0x308 or human.action==0x200' in wrapper and 'elseif gap<220 then' in wrapper and
         'if frame-rs_jump>=4 then' in wrapper and 'if frame-rs_jump<3 then' in wrapper and
         'if frame-rs_ring>=3 then' in wrapper and "press('Low Punch')" not in wrapper and
         "press('High Punch')" not in wrapper and ':set_value(' not in wrapper and
         ':clear_value(' not in wrapper and 'manager.machine:exit()' not in wrapper,
         'Only early retreat3-on/1-off/native-flight attack/far prepared guard inputs; no guest or terminal writes')
    for name in CONTROLLERS:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',
                           (ROOT/name).read_text()), 'Every loaded source physical/passive only: '+name)
    metadata_path=ROOT/core.NAME/'build-info.json'
    metadata=json.loads(metadata_path.read_text(encoding='utf-8-sig'))
    provider=SimpleNamespace(GUEST_SHA=metadata['expected_guest_sha256'],EXE_SHA=metadata['executable_sha256'],PAYLOAD_SHA=metadata['payload_sha256'])
    _,host=functions(provider)
    need("MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='1'" in host and
         "MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000'" in host and "'-str','18100'" in host and
         "'-nocheat'" in host and "'-wavwrite','NUL'" in host and
         len(old['originalNaturalIntegrationRequirements'])==14 and len(old['originalRemainingWorkGroups'])==6,
         'Entire original tower/boss/ending/fresh join79-byte candidate and full original scope')
    for path in (Path(__file__).resolve(),Path(previous.__file__),Path(core.__file__),metadata_path,core.GUARD,
                 *paths,*(ROOT/name for name in CONTROLLERS)):
        pins[str(path.resolve())]=sha(path)
    report=dict(passed=True,sourceOnlyAccepted=True,nativeGameplayAccepted=False,currentCandidate=core.NAME,
        physicalCPUContextChanged=8, physicalPolicy='Early backward jump retries before native throw spacing; attack attempts require native jump/airkick action; no Ring startup. All preceding/boss/ending/join/native rules retained.',
        originalObservationDeadlineSeconds=18000,wholeExpectedGuestByteDelta=79,boundedOriginalScreens=64,
        priorActualNativeThrows=344,priorNativeThrowStartGap=[61,77],physicalRetreatAttemptGap=220,
        wholeGeneratedHostSHA256=hashlib.sha256(host.encode()).hexdigest().upper(),
        originalNaturalIntegrationRequirements=old['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=old['originalRemainingWorkGroups'],inputHashes=pins,
        fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False,artAccepted=False,audioAccepted=False,
        fullPortAcceptance=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    SOURCE.mkdir();(SOURCE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def run():
    scope=dict(vars(previous),__file__=__file__,OUT=OUT,SOURCE=SOURCE,INIT=INIT,OLD_INIT=OLD_INIT,
               LUA=LUA,CONTROLLERS=CONTROLLERS,RAM=RAM,source_guard=source_guard,functions=functions)
    exec(compile(inspect.getsource(previous.run),__file__+'::whole_original_current_campaign','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try:
        captured=run()
    except Exception as error:
        folder=OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False,goalStatus='active')
        if folder.exists():
            path=folder/'current_capture_failure.json';need(not path.exists(),'Retain original actual outcome')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Same full Sonya campaign; early physical retreat retries, entire goal open.',local=dict(RAM=RAM))
