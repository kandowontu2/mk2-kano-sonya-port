"""Fresh candidate2753 physical Friendship audio and restriction captures.

Unchanged physical-input strategy; samples off is the sole baseline switch.
This dispatcher cannot accept gameplay, audio fidelity or the whole port.
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT = assembly.ROOT
OUT = ROOT/'audit_v2919_candidate_friendship_audio_dispatch'
PWSH = r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
CASES = [(fighter, side, command, quiet) for fighter in ('kano','sonya') for side in (1,2)
         for command, quiet in (('positive',False),('positive',True),('wrong_command',False),('punch_used',False))]

def leaf(fighter, side, command, quiet):
    return f'audit_v2920_candidate_{fighter}_friendship_{command}_{"quiet" if quiet else "audible"}_p{side}'

def run(case):
    fighter, side, command, quiet = case
    name = leaf(*case)
    cmd = [PWSH,'-NoProfile','-File',str(ROOT/'tools/run_candidate_friendship_audio_v2917.ps1'),
           '-CaseName',name,'-Winner',fighter,'-Side',str(side),'-CommandCase',command]
    if quiet: cmd.append('-NoSamples')
    result = subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    print(name+' runner exit='+str(result.returncode)+' '+result.stdout.strip()+' '+result.stderr.strip(),flush=True)
    return dict(case=name,fighter=fighter,side=side,command=command,quiet=quiet,
                runnerExit=result.returncode,stdout=result.stdout,stderr=result.stderr)

if __name__ == '__main__':
    assembly.need(not OUT.exists() and all(not (ROOT/leaf(*c)).exists() for c in CASES),'Immutable fresh audio captures')
    OUT.mkdir()
    before=assembly.sha(__file__)
    (OUT/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    with ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(run,CASES))
    assembly.need(assembly.sha(__file__)==before,'Executed dispatcher unchanged')
    report=dict(cases=results,allRunnersTerminal=True,allRunnerExitsZero=all(r['runnerExit']==0 for r in results),
                sourceSHA256=before,candidate=assembly.NAME,physicalStrategyUnchanged=True,
                noGuestStateOrRNGInjection=True,independentVerificationPending=True,fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if report['allRunnerExitsZero'] else 1)
