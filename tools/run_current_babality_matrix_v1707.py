"""Fresh current unassisted Babality positive, rejection and stock-control matrix."""
import concurrent.futures,subprocess,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1707_current_babality_dispatch'
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
SPECS=[(w,v,label,s,c)for w,v in(('kano','sonya'),('sonya','kano'))for label,s,c in
 ((w+'_babality',1,'positive'),(w+'_babality',2,'positive'),(w+'_wrong',1,'wrong_direction'),(w+'_punch',2,'punch_used'))]
SPECS += [('kitana','liu_kang','stock_liu',s,'positive')for s in(1,2)]
def run(spec):
 winner,victim,label,side,command=spec;case=f'audit_v1706_{label}_p{side}'
 p=subprocess.run([PWSH,'-NoProfile','-File',str(ROOT/'tools/run_current_babality_v1705.ps1'),
  '-CaseName',case,'-Winner',winner,'-Victim',victim,'-Side',str(side),'-CommandCase',command,'-Seconds','95'],
  cwd=ROOT,capture_output=True,text=True)
 print(case+' runner='+str(p.returncode)+' '+p.stdout.strip()+' '+p.stderr.strip(),flush=True)
 return dict(case=case,runnerExit=p.returncode,stdout=p.stdout,stderr=p.stderr)
if __name__=='__main__':
 assert not OUT.exists()and all(not(ROOT/f'audit_v1706_{label}_p{s}').exists()for w,v,label,s,c in SPECS)
 original=Path(__file__).read_bytes();OUT.mkdir();(OUT/Path(__file__).name).write_bytes(original)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:cases=list(pool.map(run,SPECS))
 assert Path(__file__).read_bytes()==original
 report=dict(candidate='diagnostic_v1597_native_ground_throw',cases=cases,
  sourceSHA256=hashlib.sha256(original).hexdigest().upper(),allRunnersTerminal=True,
  allRunnerExitsZero=all(r['runnerExit']==0 for r in cases),independentVerificationPending=True,fullPortAcceptance=False)
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 raise SystemExit(0 if report['allRunnerExitsZero']else 1)
