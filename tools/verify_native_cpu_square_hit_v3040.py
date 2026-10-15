"""Source-bound actual native CPU Square hit and separate victim recovery.

Original normal-input path duplicated byte-identically with native full render
observation. Full state/HP ledgers and complete actual contact phase checks.
No stock substitution, idle-tail, full arena/CPU/KO/audio or public promotion.
"""
import json,sys,traceback
from pathlib import Path
import verify_native_cpu_square_inventory_v2998 as inventory
import native_cpu_square_hit_contract_v3037 as phase

ROOT=inventory.ROOT;OUT=ROOT/'audit_v3041_native_cpu_square_hit_checked';need=inventory.need
CASE='audit_v3035_native_cpu_square_hit_new_kano_guard_until_close_jump_guard'

def verify():
    pins={};folder=ROOT/CASE
    log,guest,value=inventory.capture(folder,'new','kano','guard_until_close','jump_guard',pins)
    typed=phase.verify(log,guest,'kano')
    prior=ROOT/'audit_v3029_native_cpu_mobility_new_kano_guard_until_close_jump_guard'
    old=(prior/'run.log').read_text(encoding='utf-8-sig')
    prefixes=('MK2_CPU_PAIR_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_CPU_CHOICE_','MK2_SQUARE_NATIVE_','MK2_P2CPU_')
    actual=[r for r in log.splitlines()if r.startswith(prefixes)];expected=[r for r in old.splitlines()if r.startswith(prefixes)]
    need(actual==expected and value['health']['allModePhysicalFields']==3602 and value['stateLedger']['liveFields']>0,
         'Entire actual ordinary/signature/CPU/RNG/round/health/state trajectory unchanged by full drawing observation')
    proof_path=ROOT/'audit_v3039_native_cpu_mobility_inventory_checked/report.json';proof=json.loads(proof_path.read_text())
    need(proof['passed']and proof['actualCandidateSquareContact']and proof['actualSquareContactDamage']==27,
         'Independent actual naturally selected native contact inventory')
    for file,wanted in proof['inputHashes'].items():
        need(file not in pins or pins[file]==wanted,'Consistent immutable native hit fixture');pins[file]=wanted
    pins[str(proof_path)]=inventory.assembly.sha(proof_path)
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools')and Path(file).suffix=='.py':pins[str(Path(file).resolve())]=inventory.assembly.sha(file)
    for file,wanted in pins.items():need(inventory.assembly.sha(file)==wanted,'Actual immutable hit source/capture '+file)
    value.update(case=CASE,player='kano',build='new',phase=typed,originalPhysicalAndNativeEventsUnchanged=True,actualOriginalEvents=len(actual))
    return dict(passed=True,cases={'new_kano':value},actualPhysicalFixtures=1,actualDamage=27,
      actualWholeSourceStateHealthAccepted=True,actualNativeHitAndSeparateRecoveriesAccepted=True,
      gameChanged=False,allCPUOrHitContextsOrArenasKOAudioAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual CPU Square hit evidence')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
