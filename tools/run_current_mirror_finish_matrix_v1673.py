"""Fresh current cold primary fatalities, both genuine mirror winners."""
import concurrent.futures,json,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_v1673_current_mirror_finish_dispatch'
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
def run(spec):
 fighter,side=spec;case=f'audit_v1672_{fighter}_mirror_finish_winner_p{side}_confirm_p1'
 p=subprocess.run([PWSH,'-NoProfile','-File',str(ROOT/'tools/run_current_natural_mirror_finish_v1671.ps1'),'-CaseName',case,'-Player',fighter,'-Winner',str(side),'-ConfirmFirst','1'],cwd=ROOT,capture_output=True,text=True)
 print(case+' runner='+str(p.returncode)+' '+p.stdout.strip()+' '+p.stderr.strip(),flush=True)
 return dict(case=case,runnerExit=p.returncode,stdout=p.stdout,stderr=p.stderr)
if __name__=='__main__':
 specs=[(f,s)for f in('kano','sonya')for s in(1,2)]
 assert not OUT.exists() and all(not(ROOT/f'audit_v1672_{f}_mirror_finish_winner_p{s}_confirm_p1').exists()for f,s in specs)
 before=Path(__file__).read_bytes();OUT.mkdir();(OUT/Path(__file__).name).write_bytes(before)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:cases=list(pool.map(run,specs))
 assert Path(__file__).read_bytes()==before
 report=dict(candidate='diagnostic_v1597_native_ground_throw',cases=cases,sourceSHA256=hashlib.sha256(before).hexdigest().upper(),allRunnersTerminal=True,allRunnerExitsZero=all(c['runnerExit']==0 for c in cases),independentVerificationPending=True,fullPortAcceptance=False)
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 raise SystemExit(0 if report['allRunnerExitsZero']else 1)
