"""Normal standing-guard/neutral human continuation; native CPU unconstrained.

Full observer stack/guest build unchanged. Only real human buttons after
natural grab recovery differ. No character/move/RNG/health/state prescriptions.
"""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
ROOT=assembly.ROOT;OUT=ROOT/'audit_v3122_native_cpu_human_close_dispatch'
CASES=[('kano','guard_wait','jump_hold'),('kano','guard_until_close','approach_hold')]
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
def name(case):
    player,approach,policy=case
    return f'audit_v3123_native_cpu_human_close_{player}_{approach}_{policy}'
def run(case):
    player,approach,policy=case;leaf=name(case)
    result=subprocess.run([PWSH,'-NoProfile','-File',str(ROOT/'tools/run_native_cpu_human_close_v3120.ps1'),
      '-CaseName',leaf,'-Player',player,'-BootFrame','613','-ConfirmAge','264',
      '-Approach',approach,'-Policy',policy,'-Seconds','95','-CandidateName',assembly.NAME],
      cwd=ROOT,capture_output=True,text=True)
    print(leaf+' terminal '+str(result.returncode),flush=True)
    return dict(case=leaf,player=player,approach=approach,policy=policy,
      runnerExit=result.returncode,stdout=result.stdout,stderr=result.stderr)
if __name__=='__main__':
    assembly.need(not OUT.exists()and all(not(ROOT/name(c)).exists()for c in CASES),'Immutable real human hold cases')
    OUT.mkdir();before=assembly.sha(__file__);(OUT/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    with ThreadPoolExecutor(max_workers=2)as pool:results=list(pool.map(run,CASES))
    assembly.need(assembly.sha(__file__)==before,'Executed dispatch preserved')
    report=dict(cases=results,allRunnersTerminal=True,allRunnerExitsZero=all(r['runnerExit']==0 for r in results),
      sourceSHA256=before,originalNativeObserverBodiesUnchanged=True,onlyPhysicalHumanButtonsChanged=True,
      CPUIdentityOrMoveOrRNGPrescribed=False,independentVerificationPending=True,fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if report['allRunnerExitsZero']else 1)
