"""Run 52 cold real-input fixtures in isolated PowerShell/emulator processes."""
import concurrent.futures,json,subprocess
from pathlib import Path
import verify_ring_native_lookup_v1342 as current
ROOT=current.ROOT
OUT=ROOT/'audit_v1364_human_matrix_dispatch'
MOVES=('knife','ball','blade','choke','ring','square','bicycle','leg')
fixtures=[(m,s,None,False)for m in MOVES for s in(1,2)]
fixtures += [('square',s,None,True)for s in(1,2)]
fixtures += [(m,s,k,False)for m in MOVES for s in(1,2)for k in('block','miss')]
fixtures += [('leg',s,'duck_block',False)for s in(1,2)]

def run(fixture):
    move,side,scenario,air=fixture
    suffix=move+('_air'if air else '_'+scenario if scenario else '')
    case=f'audit_v1365_human_{suffix}_p{side}'
    runner=ROOT/'tools'/('run_current_human_negative_v1240.ps1'if scenario else 'run_current_human_special_v820.ps1')
    command=[r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(runner),
             '-CaseName',case,'-Move',move,'-Side',str(side),'-CandidateName',current.CANDIDATE]
    if scenario:command+=['-Scenario',scenario]
    if air:command+=['-Air']
    process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
    print(case+' runner exit='+str(process.returncode)+' '+process.stdout.strip()+' '+process.stderr.strip(),flush=True)
    return dict(case=case,runnerExit=process.returncode,stdout=process.stdout,stderr=process.stderr)

if __name__=='__main__':
    assert not OUT.exists(),'Refusing to overwrite dispatch evidence'
    assert all(not(ROOT/f'audit_v1365_human_{m+("_air"if a else "_"+k if k else "")}_p{s}').exists()for m,s,k,a in fixtures)
    OUT.mkdir()
    source=Path(__file__);before=current.digest(source)
    (OUT/source.name).write_bytes(source.read_bytes())
    with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
        results=list(pool.map(run,fixtures))
    assert before==current.digest(source),'Executed driver changed'
    report=dict(candidate=current.CANDIDATE,sourceSHA256=before,cases=results,
                allRunnersTerminal=True,allRunnerExitsZero=all(r['runnerExit']==0 for r in results),
                independentVerificationPending=True,fullPortAccepted=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if report['allRunnerExitsZero']else 1)
