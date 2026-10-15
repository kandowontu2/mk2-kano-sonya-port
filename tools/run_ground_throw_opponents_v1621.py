"""All fourteen selectable opponents, both added attackers, both human slots."""
import concurrent.futures,json,subprocess
from pathlib import Path
import verify_native_ground_throw_source_v1598 as current
ROOT=current.ROOT
OUT=ROOT/'audit_v1621_ground_throw_opponents_dispatch'
VICTIMS=('kung_lao','liu_kang','cage','baraka','kitana','mileena','shang_tsung','raiden','sub_zero','reptile','scorpion','jax','kano','sonya')
fixtures=[(f,s,v)for f in('kano','sonya')for s in(1,2)for v in VICTIMS]
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
def run(fixture):
    fighter,side,victim=fixture
    case=f'audit_v1622_{fighter}_throw_p{side}_vs_{victim}'
    runner=ROOT/'tools/run_human_ground_throw_v1601.ps1'
    process=subprocess.run([PWSH,'-NoProfile','-File',str(runner),'-CaseName',case,
       '-Fighter',fighter,'-Side',str(side),'-Victim',victim,'-CandidateName',current.NAME],
       cwd=ROOT,capture_output=True,text=True)
    print(case+' terminal runner='+str(process.returncode)+' '+process.stdout.strip()+' '+process.stderr.strip(),flush=True)
    return dict(case=case,runnerExit=process.returncode,stdout=process.stdout,stderr=process.stderr)
if __name__=='__main__':
    assert len(fixtures)==56 and not OUT.exists()
    assert all(not(ROOT/f'audit_v1622_{f}_throw_p{s}_vs_{v}').exists()for f,s,v in fixtures)
    before=current.prior.sha(__file__);OUT.mkdir()
    (OUT/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    with concurrent.futures.ThreadPoolExecutor(max_workers=1)as pool:results=list(pool.map(run,fixtures))
    assert current.prior.sha(__file__)==before
    report=dict(candidate=current.NAME,cases=results,sourceSHA256=before,allRunnersTerminal=True,
       allRunnerExitsZero=all(r['runnerExit']==0 for r in results),
       independentVerificationPending=True,fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if report['allRunnerExitsZero']else 1)
