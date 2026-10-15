"""One ordinary physical-priority successor, queued behind current Sonya.

Original whole Kano source/host, early fights, bosses, ending/attract and5900s
limit retained. Clone the original reactive input routine only at Kitana4.
No emulator rebuild/guest edit/health or RNG assistance or narrower goal.
"""
import argparse
import code
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
from types import SimpleNamespace
import prepare_native_kano_paired_stumble_host_checked as previous
import prepare_native_kano_paired_stumble_campaign as original
import retire_native_kano_zoning_losing_kitana as retired

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_kano_kitana_reactive_campaign'
SOURCE=ROOT/'audit_native_kano_kitana_reactive_campaign_source'
INIT=ROOT/'audit_native_kano_kitana_reactive_campaign_initializer'
OLD_INIT=ROOT/'audit_native_kano_kitana_reactive_campaign_previous_initializer'
LUA='mk2ks_native_kano_kitana_reactive_campaign.lua'
CONTROLLERS=[LUA,'mk2ks_native_kano_kitana_reactive_driver.lua',*original.CONTROLLERS]
RAM={}


def functions(provider):
    factory=dict(vars(previous),__file__=__file__,OUT=OUT,RAM=RAM)
    exec(compile(inspect.getsource(previous.functions),__file__+'::whole_original_checked_host_factory','exec'),factory)
    scope,host=factory['functions'](provider)
    scope.update(LUA=LUA,CONTROLLERS=CONTROLLERS)
    return scope,host


def source_guard():
    saved_path=retired.OUT/'report.json';retired_path=retired.RETIRED/'report.json'
    prefix_path=ROOT/'audit_native_kano_prefix_complete_move_inventory_checked/report.json'
    review_path=ROOT/'audit_native_kano_current_selection_snapshot_review/report.json'
    saved,retirement,prefix,review=[json.loads(p.read_text()) for p in (saved_path,retired_path,prefix_path,review_path)]
    need(saved['preservationPassed'] and not saved['passed'] and retirement['passed'] and prefix['passed'] and review['passed'] and
         prefix['finiteCurrentKanoFirstThreeLadderAdvancesAccepted'] and saved['statistics']['lossesByStage']['3']>=30 and
         saved['statistics']['latestNativeField']['stage']=='3' and saved['statistics']['nativeGlobalCacheFailureRows']==0 and
         all(sha(p)==h for report in (saved,retirement,prefix,review) for p,h in report['inputHashes'].items()),
         'Whole original unsuccessful Kitana test retired, all native earned progress and reviewed snapshot retained')
    driver=(ROOT/'mk2ks_native_kano_kitana_reactive_driver.lua').read_text()
    need(driver.count('once(')==3 and 'other.roster==4 then' in driver and
         'local body=source:sub(bodyfirst,finallast)' in driver and 'source:sub(zfirst)' in driver,
         'Exactly one complete existing reactive routine clone and one slot-only precondition, not a new game behavior')
    base=(ROOT/'mk2ks_natural_campaign_shao_knife_retreat_v3510.lua').read_text()
    zoning="   elseif strategy=='zoning' then\n"
    tail='   else\n    -- Read-only feedback: jump from actual grounded state'
    need(base.count(zoning)==base.count(tail)==base.count('    previous_y=human.y\n')==1,
         'Exact whole native ordinary reactive routine retained in immutable original controller')
    for name in CONTROLLERS:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',(ROOT/name).read_text()),
             'All transitive input controls/passive observers are free of guest/health/AI/RNG writes')
    metadata_path=ROOT/original.repaired.NAME/'build-info.json';metadata=json.loads(metadata_path.read_text(encoding='utf-8-sig'))
    scope,host=functions(SimpleNamespace(GUEST_SHA=metadata['expected_guest_sha256'],EXE_SHA=metadata['executable_sha256'],PAYLOAD_SHA=metadata['payload_sha256']))
    need(scope['OUT']==OUT and scope['LUA']==LUA and scope['CONTROLLERS']==CONTROLLERS and
         "MK2KS_CAMPAIGN_OBSERVER_LIMIT='5900'" in host and "'-str','6000'" in host and "'-nocheat'" in host and
         "MK2KS_TEST_FIGHTER='kano',MK2KS_CAMPAIGN_SIDE='1'" in host,
         'Entire original host compiled, exact new passive/Lua route and old cold game/deadline/boss flags')
    paths=[Path(__file__),Path(previous.__file__),Path(original.__file__),Path(retired.__file__),saved_path,retired_path,
           prefix_path,review_path,metadata_path,original.repaired.GUARD,*[ROOT/n for n in CONTROLLERS]]
    report=dict(passed=True,sourceOnlyAccepted=True,wholePythonHostCompiled=True,
        hostSourceSHA256=hashlib.sha256(host.encode()).hexdigest().upper(),trueCPUKitanaID=4,physicalBranchPriorityChanges=1,
        originalReactivePhysicalRoutineByteIdentical=True,timingChanges=0,allEarlierAndOtherOpponentControlsPreserved=True,
        originalBossControlsAndWholeEndingReturnPreserved=True,originalObservationDeadlineSeconds=5900,
        additionalFreshJoinNotInThisOriginalController=True,currentCandidate=original.repaired.NAME,
        originalNaturalIntegrationRequirements=prefix['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=prefix['originalRemainingWorkGroups'],inputHashes={str(p.resolve()):sha(p) for p in paths},
        newBuilds=0,newNativeBoots=0,newROMCopies=0,newRawMedia=0,newZIPs=0,nativeGameplayAccepted=False,fullPortAcceptance=False,goalStatus='active')
    if SOURCE.exists():need(json.loads((SOURCE/'report.json').read_text())==report,'Entire immutable new source/host preflight stays unchanged')
    else:SOURCE.mkdir();(SOURCE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def run():
    scope=dict(vars(original),__file__=__file__,OUT=OUT,SOURCE=SOURCE,INIT=INIT,OLD_INIT=OLD_INIT,
               RAM=RAM,source_guard=source_guard,functions=functions)
    exec(compile(inspect.getsource(original.run),__file__+'::entire_original_current_Kano_capture','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-only',action='store_true');args=parser.parse_args()
    if args.source_only:
        source_guard();print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,wholePythonHostCompiled=True,
            physicalBranchPriorityChanges=1,timingChanges=0,nativeBoots=0,emulatorBuilds=0,fullPortAcceptance=False)),flush=True)
    else:
        try:captured=run()
        except Exception as error:
            folder=OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
            if folder.exists():
                path=folder/'current_capture_failure.json';need(not path.exists(),'Preserve original current successor failure')
                path.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n')
            print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
        code.interact(banner='Same actual current Kano campaign; all natural integration requirements remain open.',local=dict(RAM=RAM))
