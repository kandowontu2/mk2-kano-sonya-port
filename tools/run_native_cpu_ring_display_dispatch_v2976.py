"""Actual extended CPU matches on isolated candidate and checked control.

Normal cold coins/selection/walking/retreat only. Known natural start timings
are different per build; no CPU identity, AI choice, stage or RNG is forced.
These captures require independent source/phase/cleanup/round verification.
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT=assembly.ROOT
OUT=ROOT/'audit_v2977_native_cpu_ring_display_dispatch'
CASES=[('new','sonya'),('new','kano'),('old','sonya')]
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'

def run(case):
    build,player=case
    name=f'audit_v2978_native_cpu_ring_display_{build}_human_{player}'
    candidate=assembly.NAME if build=='new'else assembly.prior.NAME
    boot,approach=(613,'original')if build=='new'else(604,'guard_until_close')
    cmd=[PWSH,'-NoProfile','-File',str(ROOT/'tools/run_native_cpu_ring_display_v2975.ps1'),
         '-CaseName',name,'-Player',player,'-BootFrame',str(boot),'-ConfirmAge','264',
         '-Approach',approach,'-Policy','retreat','-Seconds','95','-CandidateName',candidate]
    result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    print(name+' runner exit='+str(result.returncode)+' '+result.stdout.strip()+' '+result.stderr.strip(),flush=True)
    return dict(case=name,build=build,player=player,candidate=candidate,bootFrame=boot,approach=approach,
                runnerExit=result.returncode,stdout=result.stdout,stderr=result.stderr)

if __name__=='__main__':
    assembly.need(not OUT.exists() and all(not(ROOT/f'audit_v2978_native_cpu_ring_display_{b}_human_{p}').exists()for b,p in CASES),'Immutable actual extended matches')
    OUT.mkdir();before=assembly.sha(__file__)
    (OUT/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    with ThreadPoolExecutor(max_workers=2)as pool:results=list(pool.map(run,CASES))
    assembly.need(assembly.sha(__file__)==before,'Executed dispatcher unchanged')
    report=dict(cases=results,allRunnersTerminal=True,allRunnerExitsZero=all(r['runnerExit']==0 for r in results),
                sourceSHA256=before,wholeGuestCapture=True,nativeInputDriverUnchanged=True,
                CPUChoicesPrescribed=False,independentVerificationPending=True,fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if report['allRunnerExitsZero']else 1)
