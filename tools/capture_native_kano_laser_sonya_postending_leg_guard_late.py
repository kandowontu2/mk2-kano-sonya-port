"""Preserved pre-frame failure corrected only by late physical-policy assembly."""
import code
import gzip
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
import capture_native_kano_laser_sonya_postending_leg_guard as prior
import seal_native_sonya_leg_guard_loader_failure as rejected

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_kano_laser_sonya_postending_leg_guard_late'
INIT=ROOT/'audit_native_kano_laser_sonya_postending_leg_guard_late_initializer_source'
SOURCE=ROOT/'audit_native_kano_laser_sonya_postending_leg_guard_late_source'
LUA='mk2ks_native_kano_laser_sonya_postending_leg_guard_late.lua'
CONTROLLERS=[LUA,*prior.prior.CONTROLLERS]
RAM={}


def source_guard():
    need(not SOURCE.exists(),'Fresh corrected late-assembly source proof')
    failure=json.loads((rejected.OUT/'report.json').read_text())
    oldguard=json.loads((prior.SOURCE/'report.json').read_text())
    need(failure['failedLoaderPreserved'] and failure['nativeExit']==3 and not failure['actualGuestAccepted'] and
         all(sha(p)==h for p,h in failure['inputHashes'].items()) and oldguard['passed'] and
         all(sha(p)==h for p,h in oldguard['inputHashes'].items()),
         'Exact original source/loader failure terminal and preserved before correction')
    expected,before,after=prior.adapted_base()
    wrapper=(ROOT/LUA).read_text();base=(ROOT/'mk2ks_sonya_extended_guard_base_ram_v5201.lua').read_text()
    hook=wrapper.split('local hook=[==[\n',1)[1].split('\n]==]',1)[0]
    needle='once(original,replacement)'
    need(base.count(needle)==1 and wrapper.count("local needle='once(original,replacement)'")==1 and
         wrapper.count("branch:gsub('other%.roster==18','(other.roster==18 or other.roster==17)')")==1 and
         wrapper.count("changed:gsub('other_now%.roster~=18','other_now.roster~=18 and other_now.roster~=17')")==1 and
         wrapper.count("local path='mk2ks_native_kano_laser_sonya_postending.lua'")==1 and
         'replacement=replacement:sub(1,first-1)..changed..replacement:sub(last)' in hook,
         'Same exact five physical predicates/one observer change, only after opponent copies assembled')
    assembled=base.replace(needle,hook+'\n'+needle,1)
    need(assembled.replace(hook+'\n'+needle,needle,1)==base and
         assembled.index("elseif strategy=='guard_punish' and other.roster==18 then")<assembled.index(hook),
         'Entire original guard base and mirror template preserved for every earlier opponent loader')
    need(':set_value(' not in wrapper and ':clear_value(' not in wrapper and 'manager.machine:exit()' not in wrapper,
         'Scoped loader only, no direct input/state/AI/health/RNG or terminal substitution')
    for name in CONTROLLERS:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat',(ROOT/name).read_text()),
             'Complete transitive physical/read-only source inventory')
    paths=[Path(__file__),Path(prior.__file__),Path(rejected.__file__),rejected.OUT/'report.json',
           prior.SOURCE/'report.json',*[ROOT/n for n in CONTROLLERS]]
    SOURCE.mkdir()
    with gzip.open(SOURCE/'declared_late_physical_expansion.json.gz','wt',encoding='utf-8') as stream:
        json.dump(dict(originalGuardBase=base,guardBaseWithLateHook=assembled,independentFinalMirrorBranch=after,
                       independentMirrorAdaptedGuardBase=expected),stream)
    report=dict(passed=True,sourceOnlyAccepted=True,nativeGameplayAccepted=False,
        loaderCorrection='Same declared CPU Kano input tactic delayed until unchanged opponent-specific copies have been assembled',
        wholeOriginalTemplateBeforeOpponentCopiesUnchanged=True,originalPhysicalTimingsUnchanged=True,
        physicalEligibilityChanges=5,passiveObserverEligibilityChanges=1,originalObservationDeadlineSeconds=18000,
        independentExpectedMirrorBranchNormalizedTextSHA256=hashlib.sha256(after.encode()).hexdigest().upper(),
        originalNaturalIntegrationRequirements=oldguard['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=oldguard['originalRemainingWorkGroups'],
        inputHashes={str(p.resolve()):sha(p) for p in [*paths,SOURCE/'declared_late_physical_expansion.json.gz']},
        changedNativeExecutable=False,changedGuest=False,changedCPUAI=False,changedHealth=False,changedLadder=False,changedRNG=False,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,fullPortAcceptance=False,goalStatus='active')
    (SOURCE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def run():
    base=prior.prior
    scope=dict(vars(base),__file__=__file__,OUT=OUT,INIT=INIT,SOURCE=SOURCE,LUA=LUA,
               CONTROLLERS=CONTROLLERS,RAM=RAM,source_guard=source_guard)
    for function in (base.expectation,base.functions,base.run):
        exec(compile(inspect.getsource(function),__file__+'::whole_current_'+function.__name__,'exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try: captured=run()
    except Exception as error:
        folder=OUT if OUT.exists() else SOURCE
        if folder.exists():
            p=folder/'current_capture_failure.json';need(not p.exists(),'Preserve actual exact late-assembly failure')
            p.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
    code.interact(banner='Same actual late-bound physical Sonya campaign; full earned ending and fresh Kano join still required.',local=dict(RAM=RAM))
