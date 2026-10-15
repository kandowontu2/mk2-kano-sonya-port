"""Whole current normal-input campaign plus passive actual Shang provenance.

No new game build, changed physical tactic, state/AI/HP/RNG writes or dropped
earlier fights. Preserve the real native failure; source inference isn't a fix.
"""
import code
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
from types import SimpleNamespace
import run_native_sonya_liu_early_leg_campaign as previous

original=previous.original
core=original.core
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_sonya_shang_cache_cause'
SOURCE=ROOT/'audit_native_sonya_shang_cache_cause_source'
INIT=ROOT/'audit_native_sonya_shang_cache_cause_initializer'
OLD_INIT=ROOT/'audit_native_sonya_shang_cache_cause_previous_initializer'
LUA='mk2ks_native_sonya_shang_cache_cause.lua'
CONTROLLERS=list(dict.fromkeys((LUA,*previous.CONTROLLERS)))
RAM={}


def functions(provider):
    scope=dict(vars(original),__file__=__file__,OUT=OUT,LUA=LUA,CONTROLLERS=CONTROLLERS)
    exec(compile(inspect.getsource(original.functions),__file__+'::whole_original_full_bounded_host','exec'),scope)
    scope,host=scope['functions'](provider)
    host=original.once(host,"name.startswith('ending_page') or name.startswith('postjoin_')",
        "name.startswith('shang_victim_provenance_') or name.startswith('ending_page') or name.startswith('postjoin_')")
    exec(compile(host,__file__+'::whole_original_host_plus_bounded_actual_victim_rasters','exec'),scope)
    return scope,host


def source_guard():
    need(not OUT.exists() and not SOURCE.exists() and not core.base.census.census(),
         'One fresh passive cause replay only after exact failed game/RAM retirement')
    paths=[previous.SOURCE/'report.json',ROOT/'audit_native_liu_early_leg_preceding_campaign_checked/report.json',
           ROOT/'audit_native_liu_early_leg_earned_clear_checked/report.json',
           ROOT/'audit_native_sonya_shang_cache_failure_preserved/report.json',
           ROOT/'audit_native_sonya_shang_cache_failure_retirement/report.json',
           ROOT/'audit_native_sonya_shang_cache_failure_postread_bound_diagnosed/report.json']
    old,prefix,liu,failed,retired,diagnosed=[json.loads(p.read_text()) for p in paths]
    need(old['passed'] and prefix['passed'] and prefix['accepted']['completeOriginalRows']==1001809 and
         prefix['accepted']['completedOpponents']==12 and len(prefix['allObservedCategoryFaultsRejected'])==56 and
         liu['passed'] and liu['finiteNativeSonyaLiuClearAccepted'] and liu['completeTargetRows']==8150 and
         liu['accepted']['ownSuccessfulRoundFrames']==[392352,393931] and len(liu['semanticFaultsRejected'])==69 and
         failed['preservationPassed'] and not failed['passed'] and failed['actualGlobalStores']==146 and
         failed['actualCorruptingNativeFrame']==480976 and retired['passed'] and
         diagnosed['diagnosisCompleted'] and not diagnosed['runtimeRootCauseResolved'] and
         not diagnosed['actualLookupCallerWitnessCaptured'] and diagnosed['bothFailedDiagnosesPreserved'],
         'Whole prior thirteen regular earned opponents and real later corruption/inferred unresolved lookup retained')
    pins={}
    for proof in (old,prefix,liu,failed,retired,diagnosed):
        need(not proof['fullPortAcceptance'],'Original whole-port scope stays open')
        for p,h in proof['inputHashes'].items():
            need(sha(p)==h and (p not in pins or pins[p]==h),'Every frozen executed source/outcome unchanged: '+p);pins[p]=h
    text=(ROOT/LUA).read_text()
    need(text.count("dofile('mk2ks_native_paired_stumble_liu_early_leg.lua')")==1 and
         text.count('install_read_tap')==1 and text.count('install_write_tap')==1 and
         'assert(#taps==16' in text and 'ring_size=4096' in text and
         "{0xff8cb010,'caller_input'}" in text and "{0xff83b840,'index_cell'}" in text and
         "{0xff83b850,'index_result'}" in text and "{0xff83bb50,'animation_token_consumed'}" in text and
         'peek(cpu.A9.value-32)' in text and "p:read_u16(ha+0x1f0)~=18" in text and
         "p:read_u16(ca+0x1f0)~=6" in text and ':set_value(' not in text and ':clear_value(' not in text and
         'manager.machine:exit()' not in text,
         'Fifteen exact native read locations/one passive first-store tap; actual slot actor/Main roles and post-read token')
    for name in CONTROLLERS:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',(ROOT/name).read_text()),
             'Every actual transitive source remains physical input/passive observation only')
    metadata_path=ROOT/core.NAME/'build-info.json';metadata=json.loads(metadata_path.read_text(encoding='utf-8-sig'))
    provider=SimpleNamespace(GUEST_SHA=metadata['expected_guest_sha256'],EXE_SHA=metadata['executable_sha256'],PAYLOAD_SHA=metadata['payload_sha256'])
    _,host=functions(provider)
    need("MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='1'" in host and
         "MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000'" in host and "'-str','18100'" in host and
         "'-nocheat'" in host and "'-wavwrite','NUL'" in host and
         len(old['originalNaturalIntegrationRequirements'])==14 and len(old['originalRemainingWorkGroups'])==6,
         'Whole original current79-byte guest, full tower/boss/ending/fresh join, original deadline and scope')
    for p in (Path(__file__).resolve(),Path(previous.__file__),Path(original.__file__),Path(core.__file__),
              metadata_path,core.GUARD,*paths,*(ROOT/n for n in CONTROLLERS)):
        pins[str(p.resolve())]=sha(p)
    report=dict(passed=True,sourceOnlyAccepted=True,nativeCauseAccepted=False,currentCandidate=core.NAME,
        wholePreviousPhysicalInputsUnchanged=True,passiveReadLocations=15,passiveFirstGlobalStoreTap=1,
        maximumRetainedProvenanceRows=4096,maximumAdditionalVictimRasters=8,boundedOriginalScreens=64,
        expectedCompletePriorThirteenRows=1009959,precedingExclusiveNativeBoundary=394481,
        originalObservationDeadlineSeconds=18000,wholeExpectedGuestByteDelta=79,
        wholeGeneratedHostSHA256=hashlib.sha256(host.encode()).hexdigest().upper(),
        originalNaturalIntegrationRequirements=old['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=old['originalRemainingWorkGroups'],inputHashes=pins,
        nativeGameplayAccepted=False,fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False,
        artAccepted=False,audioAccepted=False,fullPortAcceptance=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    SOURCE.mkdir();(SOURCE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def run():
    scope=dict(vars(original),__file__=__file__,OUT=OUT,SOURCE=SOURCE,INIT=INIT,OLD_INIT=OLD_INIT,
               LUA=LUA,CONTROLLERS=CONTROLLERS,RAM=RAM,source_guard=source_guard,functions=functions)
    exec(compile(inspect.getsource(original.run),__file__+'::whole_original_full_campaign_plus_passive_cause','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try:captured=run()
    except Exception as error:
        folder=OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False,goalStatus='active')
        if folder.exists():
            p=folder/'current_capture_failure.json';need(not p.exists(),'Keep original actual trial outcome');p.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Same whole current physical campaign; passive actual Shang lookup cause.',local=dict(RAM=RAM))
