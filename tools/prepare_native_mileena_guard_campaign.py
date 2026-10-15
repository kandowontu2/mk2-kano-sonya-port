"""One physical branch successor, queued behind the actual current Kano game.

The repaired guest, all earlier opponent inputs, boss policies, complete
Sonya ending/fresh-Kano-join and original 18000-second limit stay intact.
Source-only preparation is not native gameplay or whole-port acceptance.
"""
import argparse
import code
import inspect
import json
import re
import traceback
from pathlib import Path
import capture_native_paired_stumble_scorpion_guard as previous
import capture_native_paired_stumble_campaign as core
import retire_native_scorpion_guard_losing_mileena as retirement

ROOT, need, sha = core.ROOT, core.need, core.sha
OUT = ROOT/'audit_native_paired_stumble_mileena_guard'
SOURCE = ROOT/'audit_native_paired_stumble_mileena_guard_source'
INIT = ROOT/'audit_native_paired_stumble_mileena_guard_initializer'
OLD_INIT = ROOT/'audit_native_paired_stumble_mileena_guard_previous_initializer'
LUA = 'mk2ks_native_paired_stumble_mileena_guard.lua'
CONTROLLERS = [LUA,*previous.CONTROLLERS]
RAM = {}


def source_guard():
    saved_path = retirement.OUT/'report.json'
    retired_path = retirement.RETIRED/'report.json'
    scorpion_path = ROOT/'audit_native_scorpion_guard_complete_inventory_checked/report.json'
    previous_path = previous.SOURCE/'report.json'
    saved,retired,scorpion,old = [json.loads(p.read_text()) for p in (saved_path,retired_path,scorpion_path,previous_path)]
    need(saved['preservationPassed'] and not saved['passed'] and retired['passed'] and scorpion['passed'] and
         scorpion['finiteNativeSonyaScorpionClearAccepted'] and old['passed'] and
         saved['statistics']['lossesByStage']['10']>=30 and saved['statistics']['ownWinReadsByStage']['10']==0 and
         saved['statistics']['nativeGlobalCacheFailureRows']==0 and
         all(sha(p)==h for report in (saved,retired,scorpion,old) for p,h in report['inputHashes'].items()),
         'Entire genuine unsuccessful Mileena policy retired; earlier native Scorpion clear and all source pins conserved')
    wrapper = (ROOT/LUA).read_text()
    need(wrapper.count('once(')==3 and "other.roster==5 then" in wrapper and "and false then" in wrapper and
         "assert(load(source" in wrapper and "read('a')" in wrapper,
         'Whole immutable earlier wrapper loaded, exactly one late branch and one reporting label changed')
    original = (ROOT/previous.LUA).read_text()
    need(original.count('local range_after="elseif strategy==\'guard_punish\' and other.roster==5 then"')==1,
         'Exact assembled remaining Mileena priority boundary')
    for name in CONTROLLERS:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',(ROOT/name).read_text()),
             'All transitive inputs remain physical buttons or passive observations only')
    paths = [Path(__file__),Path(previous.__file__),Path(core.__file__),Path(retirement.__file__),
             saved_path,retired_path,scorpion_path,previous_path,core.GUARD,*[ROOT/n for n in CONTROLLERS]]
    report = dict(passed=True,sourceOnlyAccepted=True,trueCPUMileenaID=5,
        physicalBranchPriorityChanges=1,timingChanges=0,earlierScorpionPhysicalPolicyPreserved=True,
        allEarlierOpponentsAndBossesPreserved=True,wholeOriginalCampaignEndingAndFreshJoinRetained=True,
        originalObservationDeadlineSeconds=18000,currentCandidate=core.NAME,
        originalNaturalIntegrationRequirements=old['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=old['originalRemainingWorkGroups'],
        inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newNativeBoots=0,
        newROMCopies=0,newRawMedia=0,newZIPs=0,nativeGameplayAccepted=False,fullPortAcceptance=False,goalStatus='active')
    if SOURCE.exists():
        need(json.loads((SOURCE/'report.json').read_text())==report,'Immutable entire successor source preflight unchanged')
    else:
        SOURCE.mkdir();(SOURCE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def run():
    scope = dict(vars(core),__file__=__file__,OUT=OUT,SOURCE=SOURCE,INIT=INIT,OLD_INIT=OLD_INIT,
                 LUA=LUA,CONTROLLERS=CONTROLLERS,RAM=RAM,source_guard=source_guard)
    for function in (core.expectation,core.run):
        exec(compile(inspect.getsource(function),__file__+'::entire_original_repaired_'+function.__name__,'exec'),scope)
    return scope['run']()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-only',action='store_true');args=parser.parse_args()
    if args.source_only:
        proof=source_guard()
        print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,physicalBranchPriorityChanges=1,timingChanges=0,
                              nativeBoots=0,emulatorBuilds=0,fullPortAcceptance=False)),flush=True)
    else:
        try: captured=run()
        except Exception as error:
            folder=OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
            if folder.exists():
                path=folder/'current_capture_failure.json';need(not path.exists(),'Preserve original successor outcome')
                path.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n')
            print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
        code.interact(banner='Same actual whole Sonya campaign/ending/fresh join; full goal open.',local=dict(RAM=RAM))
