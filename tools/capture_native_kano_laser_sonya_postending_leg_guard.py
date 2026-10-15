"""Same current Sonya earned ending/fresh Kano join, CPU-Kano physical tactic.

Only the ordinary test input policy changes. Full original campaign remains
required; a failed physical controller never becomes a game fix or clear.
"""
import code
import gzip
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
import capture_native_kano_laser_sonya_postending as prior
import seal_native_kano_laser_sonya_policy_failure as failed

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_kano_laser_sonya_postending_leg_guard'
INIT=ROOT/'audit_native_kano_laser_sonya_postending_leg_guard_initializer_source'
SOURCE=ROOT/'audit_native_kano_laser_sonya_postending_leg_guard_source'
LUA='mk2ks_native_kano_laser_sonya_postending_leg_guard.lua'
CONTROLLERS=[LUA,*prior.CONTROLLERS]
RAM={}


def adapted_base():
    original=(ROOT/'mk2ks_sonya_extended_guard_base_ram_v5201.lua').read_text()
    start="elseif strategy=='guard_punish' and other.roster==18 then"
    end="elseif strategy=='zoning' or strategy=='guard_punish' then"
    need(original.count(start)==1 and original.count(end)==1,'Unique entire original mirror leg input branch')
    first=original.index(start);last=original.index(end,first);branch=original[first:last]
    need(branch.count('other.roster==18')==5 and branch.count('other_now.roster~=18')==1,
         'Exactly original five physical predicates plus one read-only action observer')
    changed=branch.replace('other.roster==18','(other.roster==18 or other.roster==17)').replace(
        'other_now.roster~=18','other_now.roster~=18 and other_now.roster~=17')
    need(changed.replace('(other.roster==18 or other.roster==17)','other.roster==18').replace(
        'other_now.roster~=18 and other_now.roster~=17','other_now.roster~=18')==branch,
        'Whole original guard/leg algorithms, actual edges, native readiness/recovery/state and every other roster behavior unchanged')
    return original[:first]+changed+original[last:],branch,changed


def source_guard():
    need(not SOURCE.exists(),'Fresh declared physical-controller source proof')
    previous=json.loads((prior.SOURCE/'report.json').read_text())
    preservation=json.loads((failed.OUT/'report.json').read_text())
    retirement=json.loads((failed.RETIRED/'report.json').read_text())
    need(previous['passed'] and previous['sourceOnlyAccepted'] and
         preservation['failedPhysicalControllerOutcomePreserved'] and preservation['actualPaidLosses']==26 and
         not preservation['gameplayAccepted'] and retirement['passed'] and
         all(sha(p)==h for p,h in previous['inputHashes'].items()) and
         all(sha(p)==h for p,h in preservation['inputHashes'].items()),
         'Original actual failed campaign terminal/preserved; no restart of a live handle or relabeling failure')
    base,before,after=adapted_base()
    wrapper=(ROOT/LUA).read_text()
    need(wrapper.count("branch:gsub('other%.roster==18','(other.roster==18 or other.roster==17)')")==1 and
         wrapper.count("changed:gsub('other_now%.roster~=18','other_now.roster~=18 and other_now.roster~=17')")==1 and
         wrapper.count("local path='mk2ks_native_kano_laser_sonya_postending.lua'")==1 and
         ':set_value(' not in wrapper and ':clear_value(' not in wrapper and
         'manager.machine:exit()' not in wrapper,
         'Actual scoped loader applies precisely the two independently reconstructed substitutions')
    for name in CONTROLLERS:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat',(ROOT/name).read_text()),
             'Every current transitive input/observer file remains guest-write-free')
    paths=[Path(__file__),Path(prior.__file__),Path(failed.__file__),prior.SOURCE/'report.json',
           failed.OUT/'report.json',failed.RETIRED/'report.json',*[ROOT/n for n in CONTROLLERS]]
    SOURCE.mkdir()
    with gzip.open(SOURCE/'declared_physical_controller_expansion.json.gz','wt',encoding='utf-8') as stream:
        json.dump(dict(wholeAdaptedGuardBase=base,wholeOriginalMirrorBranch=before,wholeCPUKanoBranch=after),stream)
    report=dict(passed=True,sourceOnlyAccepted=True,nativeGameplayAccepted=False,
        declaredChange='Ordinary mirror guard/leg policy also used against true CPU Kano17; one passive action observer includes Kano',
        wholeOriginalNonKanoControllerBehaviorUnchanged=True,actualPhysicalInputAlgorithmsUnchanged=True,
        changedNativeExecutable=False,changedGuest=False,changedCPUAI=False,changedHealth=False,
        changedLadder=False,changedRNG=False,changedEndingOrJoin=False,
        wholeAdaptedGuardBaseSHA256=hashlib.sha256(base.encode()).hexdigest().upper(),
        originalObservationDeadlineSeconds=18000,originalNaturalIntegrationRequirements=previous['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=previous['originalRemainingWorkGroups'],
        inputHashes={str(p.resolve()):sha(p) for p in [*paths,SOURCE/'declared_physical_controller_expansion.json.gz']},
        fullPortAcceptance=False,goalStatus='active',newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    (SOURCE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def run():
    scope=dict(vars(prior),__file__=__file__,OUT=OUT,INIT=INIT,SOURCE=SOURCE,LUA=LUA,
               CONTROLLERS=CONTROLLERS,RAM=RAM,source_guard=source_guard)
    for function in (prior.expectation,prior.functions,prior.run):
        source=inspect.getsource(function)
        exec(compile(source,__file__+'::whole_original_current_'+function.__name__,'exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try: captured=run()
    except Exception as error:
        folder=OUT if OUT.exists() else SOURCE
        if folder.exists():
            p=folder/'current_capture_failure.json';need(not p.exists(),'Preserve exact actual new policy failure')
            p.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
    code.interact(banner='Same actual current CPU-Kano leg/guard campaign; full ending and fresh join remain required.',local=dict(RAM=RAM))
