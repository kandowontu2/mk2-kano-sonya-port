"""Natural tower choices from real selection timing, never prescribed CPU IDs.
Both humans, three nearby actual confirmation ages, unchanged native CPU probe.
"""
import json, subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT=assembly.ROOT
OUT=ROOT/'audit_v2868_native_cpu_timing_dispatch'
CASES=[(p,a) for p in ('kano','sonya') for a in (265,266,267)]
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
def run(case):
    player,age=case;name=f'audit_v2869_native_cpu_human_{player}_confirm{age}'
    command=[PWSH,'-NoProfile','-File',str(ROOT/'tools/run_native_physical_p2_cpu_v2863.ps1'),
        '-CaseName',name,'-Player',player,'-BootFrame','604','-ConfirmAge',str(age),
        '-Approach','guard_until_close','-Seconds','95','-CandidateName',assembly.NAME]
    result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
    print(name+' runner exit='+str(result.returncode)+' '+result.stdout.strip()+' '+result.stderr.strip(),flush=True)
    return dict(case=name,player=player,confirmAge=age,runnerExit=result.returncode,stdout=result.stdout,stderr=result.stderr)
if __name__=='__main__':
    assembly.need(not OUT.exists() and all(not(ROOT/f'audit_v2869_native_cpu_human_{p}_confirm{a}').exists() for p,a in CASES),
                  'Immutable physical timing captures required')
    OUT.mkdir();before=assembly.sha(__file__);(OUT/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,CASES))
    assembly.need(assembly.sha(__file__)==before,'Executed dispatcher never changed')
    report=dict(candidate=assembly.NAME,cases=results,allRunnersTerminal=True,allRunnerExitsZero=all(r['runnerExit']==0 for r in results),
                sourceSHA256=before,CPUChoicesPrescribed=False,naturalConfirmationInputsOnly=True,independentVerificationPending=True,
                fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if report['allRunnerExitsZero'] else 1)
