"""Twenty fresh native interruption/retry and earned KO/next-round fixtures."""
import json, subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_current_interrupt_and_ko_v824 as interrupt
import verify_current_ko_v1872 as ko

ROOT=assembly.ROOT
OUT=ROOT/'audit_v2852_native_combat_dispatch'
FIXTURES=[('interrupt',*case) for case in interrupt.INT_CASES]+[('ko',*case) for case in ko.CASES]
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'

def run(case):
    kind,move,side,victim=case
    name=f'audit_v2853_{kind}_{move}_p{side}_{victim}'
    command=[PWSH,'-NoProfile','-File',str(ROOT/'tools/run_native_combat_regression_v2850.ps1'),
             '-CaseName',name,'-Kind',kind,'-Move',move,'-Side',str(side),'-Victim',victim]
    result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
    print(name+' runner exit='+str(result.returncode)+' '+result.stdout.strip()+' '+result.stderr.strip(),flush=True)
    return dict(case=name,kind=kind,move=move,side=side,victim=victim,runnerExit=result.returncode,
                stdout=result.stdout,stderr=result.stderr)

if __name__=='__main__':
    assembly.need(len(FIXTURES)==len(set(FIXTURES))==20,'Exact original twenty-fixture inventory')
    assembly.need(not OUT.exists() and all(not(ROOT/f'audit_v2853_{k}_{m}_p{s}_{v}').exists() for k,m,s,v in FIXTURES),
                  'Never overwrite dispatch or actual captures')
    OUT.mkdir();before=assembly.sha(__file__);(OUT/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,FIXTURES))
    assembly.need(assembly.sha(__file__)==before,'Executed dispatcher immutable')
    report=dict(candidate=assembly.NAME,cases=results,allRunnersTerminal=True,
                allRunnerExitsZero=all(r['runnerExit']==0 for r in results),sourceSHA256=before,
                independentVerificationPending=True,fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if report['allRunnerExitsZero'] else 1)
