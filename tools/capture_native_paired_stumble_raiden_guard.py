"""Same repaired executable and original campaign; ordinary Raiden guard/legs.

Only five physical branch eligibility predicates and one passive CPU-action
eligibility include Raiden7. All other opponent clones, controls and deadlines
remain unchanged; source-only proof is not campaign acceptance.
"""
import code
import inspect
import json
import re
import traceback
from pathlib import Path
import capture_native_paired_stumble_campaign as prior

ROOT, need, sha = prior.ROOT, prior.need, prior.sha
OUT = ROOT / 'audit_native_paired_stumble_raiden_guard'
OLD_INIT = ROOT / 'audit_native_paired_stumble_raiden_guard_previous_initializer'
INIT = ROOT / 'audit_native_paired_stumble_raiden_guard_initializer'
SOURCE = ROOT / 'audit_native_paired_stumble_raiden_guard_source'
LUA = 'mk2ks_native_paired_stumble_raiden_guard.lua'
CONTROLLERS = [LUA, *prior.CONTROLLERS]
RAM = {}


def source_guard():
    need(not SOURCE.exists(), 'Fresh ordinary physical-policy qualification')
    accepted_path = ROOT / 'audit_native_paired_stumble_handoff_checked/report.json'
    retired_path = ROOT / 'audit_native_paired_stumble_handoff_retirement/report.json'
    accepted = json.loads(accepted_path.read_text())
    retired = json.loads(retired_path.read_text())
    failed_path = prior.OUT / 'explicit_unsuccessful_physical_policy_stop.json'
    failed = json.loads(failed_path.read_text())
    need(accepted['passed'] and accepted['finiteNativeSonyaRaidenHandoffAccepted'] and
         not accepted['fullTowerAccepted'] and retired['passed'] and
         failed['physicalPolicyUnsuccessful'] and failed['observedLossesByStage']['2'] == 43 and
         failed['ownNativeWinReadsByStage']['2'] == 0 and
         all(sha(p) == h for p,h in accepted['inputHashes'].items()),
         'Actual old native handoff fix, failed tactics and exact original retirement retained')
    for name in CONTROLLERS:
        text = (ROOT / name).read_text()
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',text),
             'All original controls/passive observers and new read-only loader have no game-state edits')
    wrapper = (ROOT / LUA).read_text()
    observer = (ROOT / prior.LUA).read_text()
    need(wrapper.count('adapted=once(') == 3 and
         "'(other.roster==18 or other.roster==17 or other.roster==7)'" in wrapper and
         "'other_now.roster~=18 and other_now.roster~=17 and other_now.roster~=7'" in wrapper and
         "'target_cpu=17,7 eligibility_changes=5 observer_changes=1 timing_changes=0'" in wrapper and
         "read('mk2ks_native_paired_stumble_campaign.lua')" in wrapper and
         ':set_value(' not in wrapper and ':clear_value(' not in wrapper and
         'manager.machine:exit()' not in wrapper and 'assert(#taps==3' in observer,
         'Late assembled physical policy eligibility only, unchanged native observer and original exits')
    paths = [Path(__file__),Path(prior.__file__),accepted_path,retired_path,failed_path,
             prior.GUARD,*[ROOT/n for n in CONTROLLERS]]
    SOURCE.mkdir()
    (SOURCE / 'report.json').write_text(json.dumps(dict(passed=True,sourceOnlyAccepted=True,
        originalWholeCampaignAndOtherOpponentClonesRetained=True,
        physicalEligibilityChanges=5,passiveActionEligibilityChanges=1,timingChanges=0,
        includedTrueCPUIdentities=[17,18,7],originalObservationDeadlineSeconds=18000,
        unchangedRepairedCandidate=prior.NAME,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        originalNaturalIntegrationRequirements=accepted['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=accepted['originalRemainingWorkGroups'],
        inputHashes={str(p.resolve()):sha(p) for p in paths},
        nativeGameplayAccepted=False,fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')


def run():
    scope = dict(vars(prior),__file__=__file__,OUT=OUT,OLD_INIT=OLD_INIT,INIT=INIT,SOURCE=SOURCE,
                 LUA=LUA,CONTROLLERS=CONTROLLERS,RAM=RAM,source_guard=source_guard)
    for function in (prior.expectation,prior.run):
        exec(compile(inspect.getsource(function),__file__+'::whole_repaired_'+function.__name__,'exec'),scope)
    return scope['run']()


if __name__ == '__main__':
    try:
        captured = run()
    except Exception as error:
        folder = OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        if folder.exists():
            path = folder / 'current_capture_failure.json'; need(not path.exists(),'Preserve actual original failure')
            path.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
    code.interact(banner='Same actual Raiden guard/leg campaign handle; full goal remains open.',local=dict(RAM=RAM))
