"""Native CPU mobility exploration using only human confirmation timing.

Two genuine cold Kano games, unmodified physical driver, normal human guard
and continuation buttons. Native CPU choice, RNG and state never supplied.
All outcomes remain diagnostic until independently verified.
"""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
ROOT=assembly.ROOT
OUT=ROOT/'audit_v3088_native_cpu_bicycle_contact_dispatch'
CASES=[('new','kano','guard_until_close','jump_guard',613,age)for age in(268,272)]
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
def name(case):
    build,player,approach,policy,boot,age=case
    return f'audit_v3089_native_cpu_bicycle_contact_{player}_{boot}_{age}'
def run(case):
    build,player,approach,policy,boot,age=case;leaf=name(case)
    cmd=[PWSH,'-NoProfile','-File',str(ROOT/'tools/run_native_cpu_mobility_v3026.ps1'),
         '-CaseName',leaf,'-Player',player,'-BootFrame',str(boot),
         '-ConfirmAge',str(age),'-Approach',approach,'-Policy',policy,
         '-Seconds','95','-CandidateName',assembly.NAME]
    result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    print(leaf+' terminal '+str(result.returncode),flush=True)
    return dict(case=leaf,build=build,player=player,approach=approach,policy=policy,
                boot=boot,confirmAge=age,runnerExit=result.returncode,stdout=result.stdout,stderr=result.stderr)
if __name__=='__main__':
    assembly.need(not OUT.exists()and all(not(ROOT/name(c)).exists()for c in CASES),'Immutable new real-input games')
    OUT.mkdir();before=assembly.sha(__file__);(OUT/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    with ThreadPoolExecutor(max_workers=2)as pool:results=list(pool.map(run,CASES))
    assembly.need(assembly.sha(__file__)==before,'Executed dispatcher unchanged')
    report=dict(cases=results,allRunnersTerminal=True,allRunnerExitsZero=all(r['runnerExit']==0 for r in results),
      sourceSHA256=before,wholeGuestCapture=True,originalPhysicalDriverUnchanged=True,
      CPUIdentityOrMoveOrRNGPrescribed=False,independentVerificationPending=True,fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if report['allRunnerExitsZero']else 1)
