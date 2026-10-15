"""Cold native defensive grab regressions, no supplied character/health state."""
import concurrent.futures,json,subprocess
from pathlib import Path
import verify_ring_native_lookup_v1342 as current
ROOT=current.ROOT;NAME='diagnostic_v1411_native_grab_audio';OUT=ROOT/'audit_v1416_grab_defense_dispatch'
FIXTURES=[(m,s,k)for m in ('choke','leg')for s in (1,2)for k in ('block','miss')]+[('leg',s,'duck_block')for s in (1,2)]

def run(fixture):
 move,side,scenario=fixture;case=f'audit_v1417_human_{move}_{scenario}_p{side}'
 command=[r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe','-NoProfile','-File',str(ROOT/'tools/run_current_human_negative_v1240.ps1'),'-CaseName',case,'-Move',move,'-Side',str(side),'-Scenario',scenario,'-CandidateName',NAME]
 result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
 print(case+' runner exit='+str(result.returncode)+' '+result.stdout.strip()+' '+result.stderr.strip(),flush=True)
 return dict(case=case,runnerExit=result.returncode,stdout=result.stdout,stderr=result.stderr)

if __name__=='__main__':
 assert not OUT.exists() and all(not(ROOT/f'audit_v1417_human_{m}_{k}_p{s}').exists()for m,s,k in FIXTURES)
 OUT.mkdir();source=Path(__file__);before=current.digest(source);(OUT/source.name).write_bytes(source.read_bytes())
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:cases=list(pool.map(run,FIXTURES))
 assert current.digest(source)==before
 report=dict(candidate=NAME,cases=cases,sourceSHA256=before,allRunnersTerminal=True,allRunnerExitsZero=all(q['runnerExit']==0 for q in cases),independentVerificationPending=True,fullPortAccepted=False)
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 raise SystemExit(0 if report['allRunnerExitsZero']else 1)
