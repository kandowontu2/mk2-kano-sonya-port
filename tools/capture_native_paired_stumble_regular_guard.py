"""Same repaired build; ordinary guard/leg input fallback for regular CPU IDs.

Original earlier opponent-specific branches and boss controls take precedence.
No game AI, health, selection, timing, damage, RNG or victory changes.
"""
import code
import inspect
import json
import re
import traceback
from pathlib import Path
import capture_native_paired_stumble_kung_lao_guard as previous
import capture_native_paired_stumble_campaign as core

ROOT,need,sha=core.ROOT,core.need,core.sha
OUT=ROOT/'audit_native_paired_stumble_regular_guard'
OLD_INIT=ROOT/'audit_native_paired_stumble_regular_guard_previous_initializer'
INIT=ROOT/'audit_native_paired_stumble_regular_guard_initializer'
SOURCE=ROOT/'audit_native_paired_stumble_regular_guard_source'
LUA='mk2ks_native_paired_stumble_regular_guard.lua'
CONTROLLERS=[LUA,*core.CONTROLLERS]
RAM={}


def source_guard():
    need(not SOURCE.exists(),'Fresh ordinary regular-opponent control qualification')
    saved_path=ROOT/'audit_native_kung_lao_guard_losing_baraka_preserved/report.json'
    retired_path=ROOT/'audit_native_kung_lao_guard_losing_baraka_retirement/report.json'
    previous_path=previous.SOURCE/'report.json'
    fixed_path=ROOT/'audit_native_paired_stumble_handoff_checked/report.json'
    reports=[json.loads(p.read_text()) for p in (saved_path,retired_path,previous_path,fixed_path)]
    saved,retired,old,fixed=reports
    need(saved['preservationPassed'] and not saved['passed'] and retired['passed'] and
         saved['statistics']['lossesByStage']['6']>=30 and saved['statistics']['ownWinReadsByStage']['6']==0 and
         fixed['passed'] and fixed['finiteNativeSonyaRaidenHandoffAccepted'] and not fixed['fullPortAcceptance'] and
         all(sha(p)==h for report in reports for p,h in report['inputHashes'].items()),
         'Actual unsuccessful later-ladder controls retired, entire original repaired game and scope retained')
    original=(ROOT/previous.LUA).read_text()
    expected=original
    for before,after in (
        ('(other.roster==18 or other.roster==17 or other.roster==7 or other.roster==0)',
         '((other.roster>=0 and other.roster<=11) or other.roster==14 or other.roster==17 or other.roster==18)'),
        ('other_now.roster~=18 and other_now.roster~=17 and other_now.roster~=7 and other_now.roster~=0',
         '(other_now.roster<0 or other_now.roster>11) and other_now.roster~=14 and other_now.roster~=17 and other_now.roster~=18'),
        ('target_cpu=17,7,0 eligibility_changes=5 observer_changes=1 timing_changes=0',
         'target_cpu=0..11,14,17,18 eligibility_changes=5 observer_changes=1 timing_changes=0')):
        need(expected.count(before)==1,'Exactly one existing eligibility boundary')
        expected=expected.replace(before,after)
    need((ROOT/LUA).read_text()==expected,'Whole original controls byte-identical except regular-opponent eligibility and log label')
    for name in CONTROLLERS:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',(ROOT/name).read_text()),
             'All transitive original controls/passive observers free of guest-state edits')
    included=[*range(12),14,17,18]
    need(12 not in included and 13 not in included and 15 not in included and 16 not in included,
         'Original boss and unsupported-ID paths unchanged')
    need(len(fixed['originalNaturalIntegrationRequirements'])==14 and len(fixed['originalRemainingWorkGroups'])==6,
         'Whole original natural integration objective retained')
    paths=[Path(__file__),Path(previous.__file__),Path(core.__file__),saved_path,retired_path,previous_path,fixed_path,
        core.GUARD,ROOT/previous.LUA,*[ROOT/name for name in CONTROLLERS]]
    SOURCE.mkdir()
    (SOURCE/'report.json').write_text(json.dumps(dict(passed=True,sourceOnlyAccepted=True,
        includedTrueCPUIdentities=included,physicalEligibilityChanges=5,passiveActionEligibilityChanges=1,timingChanges=0,
        originalEarlierOpponentSpecificBranchPriorityPreserved=True,originalBossPhysicalPolicyPreserved=True,
        originalWholeCampaignAndEndingJoinRetained=True,originalObservationDeadlineSeconds=18000,
        unchangedRepairedCandidate=core.NAME,
        originalNaturalIntegrationRequirements=fixed['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=fixed['originalRemainingWorkGroups'],inputHashes={str(p.resolve()):sha(p) for p in paths},
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,nativeGameplayAccepted=False,
        fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')


def run():
    scope=dict(vars(core),__file__=__file__,OUT=OUT,OLD_INIT=OLD_INIT,INIT=INIT,SOURCE=SOURCE,
        LUA=LUA,CONTROLLERS=CONTROLLERS,RAM=RAM,source_guard=source_guard)
    for function in (core.expectation,core.run):
        exec(compile(inspect.getsource(function),__file__+'::whole_repaired_'+function.__name__,'exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try: captured=run()
    except Exception as error:
        folder=OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        if folder.exists():
            path=folder/'current_capture_failure.json';need(not path.exists(),'Preserve original actual native failure')
            path.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
    code.interact(banner='Same actual regular-opponent guard/leg campaign; full goal remains open.',local=dict(RAM=RAM))
