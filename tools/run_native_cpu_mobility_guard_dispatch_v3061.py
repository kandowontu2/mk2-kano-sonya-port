"""Normal physical selection/approach/continuation Square discovery, not forcing.

Existing original/standing-guard/guard-until-close human button policies only.
Native CPU identity, AI move and RNG untouched; genuine misses kept as misses.
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT=assembly.ROOT
OUT=ROOT/'audit_v3062_native_cpu_mobility_guard_dispatch'
CASES=[('new',player,'guard_wait','jump_guard')for player in ('kano','sonya')]
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'

def name(case):
    build,player,approach,policy=case
    return f'audit_v3063_native_cpu_mobility_guard_{build}_{player}_{approach}_{policy}'

def run(case):
    build,player,approach,policy=case;leaf=name(case)
    candidate=assembly.NAME if build=='new'else assembly.prior.NAME
    cmd=[PWSH,'-NoProfile','-File',str(ROOT/'tools/run_native_cpu_mobility_v3026.ps1'),
         '-CaseName',leaf,'-Player',player,'-BootFrame',str(613 if build=='new'else 604),
         '-ConfirmAge','264','-Approach',approach,'-Policy',policy,'-Seconds','95','-CandidateName',candidate]
    result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    print(leaf+' runner exit='+str(result.returncode)+' '+result.stdout.strip()+' '+result.stderr.strip(),flush=True)
    return dict(case=leaf,build=build,player=player,approach=approach,policy=policy,
                candidate=candidate,runnerExit=result.returncode,stdout=result.stdout,stderr=result.stderr)

if __name__=='__main__':
    assembly.need(not OUT.exists() and all(not(ROOT/name(case)).exists()for case in CASES),'Immutable actual native input-only Square discovery')
    OUT.mkdir();before=assembly.sha(__file__);(OUT/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    with ThreadPoolExecutor(max_workers=2)as pool:results=list(pool.map(run,CASES))
    assembly.need(assembly.sha(__file__)==before,'Executed discovery unchanged')
    report=dict(cases=results,allRunnersTerminal=True,allRunnerExitsZero=all(r['runnerExit']==0 for r in results),
        sourceSHA256=before,wholeGuestCapture=True,originalPhysicalDriverUnchanged=True,
        CPUIdentityOrMoveOrRNGPrescribed=False,independentVerificationPending=True,fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if report['allRunnerExitsZero']else 1)
