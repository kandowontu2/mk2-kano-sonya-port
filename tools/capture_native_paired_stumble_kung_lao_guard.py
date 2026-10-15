"""Same repaired build; ordinary Kung Lao guard/leg physical eligibility only."""
import code
import inspect
import json
import re
import traceback
from pathlib import Path
import capture_native_paired_stumble_raiden_guard as template
import capture_native_paired_stumble_campaign as core

ROOT, need, sha = core.ROOT, core.need, core.sha
OUT = ROOT / 'audit_native_paired_stumble_kung_lao_guard'
OLD_INIT = ROOT / 'audit_native_paired_stumble_kung_lao_guard_previous_initializer'
INIT = ROOT / 'audit_native_paired_stumble_kung_lao_guard_initializer'
SOURCE = ROOT / 'audit_native_paired_stumble_kung_lao_guard_source'
LUA = 'mk2ks_native_paired_stumble_kung_lao_guard.lua'
CONTROLLERS = [LUA, *core.CONTROLLERS]
RAM = {}


def source_guard():
    need(not SOURCE.exists(), 'Fresh physical Kung Lao source qualification')
    saved_path = ROOT / 'audit_native_raiden_guard_losing_kung_lao_preserved/report.json'
    retired_path = ROOT / 'audit_native_raiden_guard_losing_kung_lao_retirement/report.json'
    prior_path = ROOT / 'audit_native_paired_stumble_raiden_guard_ready_source/report.json'
    accepted_path = ROOT / 'audit_native_paired_stumble_handoff_checked/report.json'
    saved, retired, previous, accepted = [json.loads(p.read_text()) for p in (saved_path,retired_path,prior_path,accepted_path)]
    need(saved['preservationPassed'] and not saved['passed'] and retired['passed'] and
         saved['statistics']['lossesByStage']['4'] >= 70 and saved['statistics']['ownWinReadsByStage']['4'] == 0 and
         accepted['passed'] and accepted['finiteNativeSonyaRaidenHandoffAccepted'] and not accepted['fullPortAcceptance'] and
         all(sha(p)==h for report in (saved,retired,previous,accepted) for p,h in report['inputHashes'].items()),
         'Actual unsuccessful Kung Lao policy retired, finite repaired native handoff and original full scope preserved')
    original = (ROOT / template.LUA).read_text()
    expected = original
    changes = (
        ('(other.roster==18 or other.roster==17 or other.roster==7)',
         '(other.roster==18 or other.roster==17 or other.roster==7 or other.roster==0)'),
        ('other_now.roster~=18 and other_now.roster~=17 and other_now.roster~=7',
         'other_now.roster~=18 and other_now.roster~=17 and other_now.roster~=7 and other_now.roster~=0'),
        ('target_cpu=17,7 eligibility_changes=5 observer_changes=1 timing_changes=0',
         'target_cpu=17,7,0 eligibility_changes=5 observer_changes=1 timing_changes=0'))
    for before,after in changes:
        need(expected.count(before)==1, 'Exactly one existing physical eligibility boundary')
        expected = expected.replace(before,after)
    need((ROOT / LUA).read_text() == expected,
         'Complete wrapper byte-identical except five assembled physical eligibility predicates and one passive observer eligibility')
    for name in CONTROLLERS:
        text = (ROOT / name).read_text()
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',text),
             'All transitive controls/passive observers free of guest state edits')
    need(len(accepted['originalNaturalIntegrationRequirements'])==14 and len(accepted['originalRemainingWorkGroups'])==6,
         'Original complete natural integration scope remains open')
    paths=[Path(__file__),Path(template.__file__),Path(core.__file__),saved_path,retired_path,prior_path,accepted_path,
           core.GUARD,ROOT/template.LUA,*[ROOT/name for name in CONTROLLERS]]
    SOURCE.mkdir()
    (SOURCE/'report.json').write_text(json.dumps(dict(passed=True,sourceOnlyAccepted=True,
        includedTrueCPUIdentities=[17,18,7,0],newPhysicalOpponent=0,physicalEligibilityChanges=5,
        passiveActionEligibilityChanges=1,timingChanges=0,originalObservationDeadlineSeconds=18000,
        originalWholeCampaignAndEndingJoinRetained=True,unchangedRepairedCandidate=core.NAME,
        originalNaturalIntegrationRequirements=accepted['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=accepted['originalRemainingWorkGroups'],inputHashes={str(p.resolve()):sha(p) for p in paths},
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,nativeGameplayAccepted=False,
        fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')


def run():
    scope=dict(vars(core),__file__=__file__,OUT=OUT,OLD_INIT=OLD_INIT,INIT=INIT,SOURCE=SOURCE,
        LUA=LUA,CONTROLLERS=CONTROLLERS,RAM=RAM,source_guard=source_guard)
    for function in (core.expectation,core.run):
        exec(compile(inspect.getsource(function),__file__+'::whole_repaired_'+function.__name__,'exec'),scope)
    return scope['run']()


if __name__ == '__main__':
    try:
        captured=run()
    except Exception as error:
        folder=OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        if folder.exists():
            path=folder/'current_capture_failure.json'; need(not path.exists(),'Preserve original actual failure')
            path.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
    code.interact(banner='Same actual Kung Lao physical guard/leg run; full integration remains open.',local=dict(RAM=RAM))
