"""Normal human walking approach for the four previously unreached CPU pairs.

The original driver/observer/runner are unchanged. Only its existing physical
approach option changes. Native CPU identity and decisions remain unprescribed.
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT=assembly.ROOT
OUT=ROOT/'audit_v2926_native_cpu_close_approach_dispatch'
CASES=[('sonya',613),('kano',613),('sonya',607),('kano',614)]
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'

def run(case):
    player,boot=case
    name=f'audit_v2927_native_cpu_close_human_{player}_boot{boot}'
    cmd=[PWSH,'-NoProfile','-File',str(ROOT/'tools/run_native_physical_p2_cpu_v2863.ps1'),
         '-CaseName',name,'-Player',player,'-BootFrame',str(boot),'-ConfirmAge','264',
         '-Approach','original','-Seconds','95','-CandidateName',assembly.NAME]
    result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    print(name+' runner exit='+str(result.returncode)+' '+result.stdout.strip()+' '+result.stderr.strip(),flush=True)
    return dict(case=name,player=player,bootFrame=boot,confirmAge=264,approach='original',
                runnerExit=result.returncode,stdout=result.stdout,stderr=result.stderr)

if __name__=='__main__':
    assembly.need(not OUT.exists() and all(not(ROOT/f'audit_v2927_native_cpu_close_human_{p}_boot{b}').exists()for p,b in CASES),'Immutable physical approach captures')
    OUT.mkdir();before=assembly.sha(__file__)
    (OUT/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    with ThreadPoolExecutor(max_workers=2)as pool:results=list(pool.map(run,CASES))
    assembly.need(assembly.sha(__file__)==before,'Executed dispatcher unchanged')
    report=dict(candidate=assembly.NAME,cases=results,allRunnersTerminal=True,
                allRunnerExitsZero=all(r['runnerExit']==0 for r in results),sourceSHA256=before,
                originalDriverUnchanged=True,CPUChoicesPrescribed=False,naturalCoinStartSelectionWalkingOnly=True,
                independentVerificationPending=True,fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if report['allRunnerExitsZero']else 1)
