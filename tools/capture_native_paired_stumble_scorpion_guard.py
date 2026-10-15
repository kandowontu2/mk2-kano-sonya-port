"""Same repaired guest, Scorpion's earlier ranged test priority removed only."""
import code
import inspect
import json
import re
import traceback
from pathlib import Path
import capture_native_paired_stumble_regular_guard as previous
import capture_native_paired_stumble_campaign as core

ROOT, need, sha = core.ROOT, core.need, core.sha
OUT = ROOT / 'audit_native_paired_stumble_scorpion_guard'
OLD_INIT = ROOT / 'audit_native_paired_stumble_scorpion_guard_previous_initializer'
INIT = ROOT / 'audit_native_paired_stumble_scorpion_guard_initializer'
SOURCE = ROOT / 'audit_native_paired_stumble_scorpion_guard_source'
LUA = 'mk2ks_native_paired_stumble_scorpion_guard.lua'
CONTROLLERS = [LUA, *core.CONTROLLERS]
RAM = {}
INSERTION = '''adapted=once(adapted,'replacement=replacement:sub(1,first-1)..changed..replacement:sub(last)',[=[replacement=replacement:sub(1,first-1)..changed..replacement:sub(last)
local range_before="elseif strategy=='guard_punish' and (other.roster==5 or other.roster==10) then"
local range_after="elseif strategy=='guard_punish' and other.roster==5 then"
local range_first,range_last=replacement:find(range_before,1,true)
assert(range_first and not replacement:find(range_before,range_last+1,true),'One assembled Scorpion ranged priority boundary')
replacement=replacement:sub(1,range_first-1)..range_after..replacement:sub(range_last+1)
print('MK2_CURRENT_SCORPION_PHYSICAL_POLICY true_cpu=10 branch_priority_changes=1 timing_changes=0 writes=0 assistance=none')]=])
'''


def source_guard():
    need(not SOURCE.exists(), 'Fresh exact Scorpion physical-policy successor')
    saved_path = ROOT / 'audit_native_regular_guard_losing_scorpion_preserved/report.json'
    retired_path = ROOT / 'audit_native_regular_guard_losing_scorpion_retirement/report.json'
    previous_path = previous.SOURCE / 'report.json'
    fixed_path = ROOT / 'audit_native_paired_stumble_handoff_checked/report.json'
    reports = [json.loads(p.read_text()) for p in (saved_path, retired_path, previous_path, fixed_path)]
    saved, retired, old, fixed = reports
    need(saved['preservationPassed'] and not saved['passed'] and retired['passed'] and
         saved['statistics']['lossesByStage']['9'] >= 30 and saved['statistics']['ownWinReadsByStage']['9'] == 0 and
         saved['statistics']['nativeGlobalCacheFailureRows'] == 0 and
         fixed['passed'] and fixed['finiteNativeSonyaRaidenHandoffAccepted'] and not fixed['fullPortAcceptance'] and
         all(sha(p) == h for report in reports for p, h in report['inputHashes'].items()),
         'Original failed Scorpion policy retired, source pins and repaired guest evidence intact')
    original = (ROOT / previous.LUA).read_text()
    needle = 'local environment=setmetatable({},{__index=_ENV})\n'
    need(original.count(needle) == 1 and (ROOT / LUA).read_text() == original.replace(needle, INSERTION + needle),
         'Entire original wrapper retained with only one late assembled branch-priority insertion')
    for name in CONTROLLERS:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data', (ROOT/name).read_text()),
             'All transitive controls are physical inputs or passive observations only')
    base_path = ROOT / 'mk2ks_sonya_extended_guard_base_ram_v5201.lua'
    ranged = "elseif strategy=='guard_punish' and (other.roster==5 or other.roster==10) then"
    need(base_path.read_text().count(ranged) == 1, 'Exact original ranged branch exists before late assembly')
    need(len(fixed['originalNaturalIntegrationRequirements']) == 14 and len(fixed['originalRemainingWorkGroups']) == 6,
         'Full natural-character objective retained')
    paths = [Path(__file__), Path(previous.__file__), Path(core.__file__), saved_path, retired_path,
             previous_path, fixed_path, core.GUARD, ROOT / previous.LUA, *[ROOT/n for n in CONTROLLERS]]
    SOURCE.mkdir()
    (SOURCE/'report.json').write_text(json.dumps(dict(passed=True, sourceOnlyAccepted=True,
        trueCPUScorpionID=10, physicalBranchPriorityChanges=1, timingChanges=0,
        originalOtherOpponentBranchesPreserved=True, originalBossPhysicalPolicyPreserved=True,
        originalWholeCampaignAndEndingJoinRetained=True, originalObservationDeadlineSeconds=18000,
        unchangedRepairedCandidate=core.NAME,
        originalNaturalIntegrationRequirements=fixed['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=fixed['originalRemainingWorkGroups'], inputHashes={str(p.resolve()):sha(p) for p in paths},
        newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
        nativeGameplayAccepted=False, fullPortAcceptance=False, goalStatus='active'), indent=2)+'\n')


def run():
    scope = dict(vars(core), __file__=__file__, OUT=OUT, OLD_INIT=OLD_INIT, INIT=INIT,
                 SOURCE=SOURCE, LUA=LUA, CONTROLLERS=CONTROLLERS, RAM=RAM, source_guard=source_guard)
    for function in (core.expectation, core.run):
        exec(compile(inspect.getsource(function), __file__+'::whole_repaired_'+function.__name__, 'exec'), scope)
    return scope['run']()


if __name__ == '__main__':
    try: captured = run()
    except Exception as error:
        folder = OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        if folder.exists():
            path = folder / 'current_capture_failure.json'; need(not path.exists(), 'Preserve original actual failure')
            path.write_text(json.dumps(dict(passed=False, error=repr(error), traceback=traceback.format_exc(),
                fullPortAcceptance=False, goalStatus='active'), indent=2)+'\n')
        print(json.dumps(dict(passed=False, error=repr(error), traceback=traceback.format_exc())), flush=True)
    code.interact(banner='Same actual Scorpion guard/leg campaign; full goal remains open.', local=dict(RAM=RAM))
