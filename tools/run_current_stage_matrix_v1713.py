"""Fresh current genuine earned stage command/rejection matrix, no assists."""
import concurrent.futures,subprocess,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_v1713_current_stage_dispatch'
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
SPECS=[(w,s,label,a,c)for w in ('kano','sonya')for s in (1,2)for label,a,c in
 [('tomb',1,'positive'),('pit',6,'positive'),('wrong',1,'wrong_command'),('far',1,'far'),('arena0',0,'positive')]]
def run(spec):
 w,s,label,a,c=spec;case=f'audit_v1714_{w}_{label}_p{s}'
 p=subprocess.run([PWSH,'-NoProfile','-File',str(ROOT/'tools/run_current_stage_performer_v1712.ps1'),
  '-CaseName',case,'-Winner',w,'-Side',str(s),'-Arena',str(a),'-CommandCase',c,'-Seconds','900'],
  cwd=ROOT,capture_output=True,text=True)
 print(case+' runner='+str(p.returncode)+' '+p.stdout.strip()+' '+p.stderr.strip(),flush=True)
 return dict(case=case,runnerExit=p.returncode,stdout=p.stdout,stderr=p.stderr)
if __name__=='__main__':
 assert not OUT.exists()and all(not(ROOT/f'audit_v1714_{w}_{label}_p{s}').exists()for w,s,label,a,c in SPECS)
 original=Path(__file__).read_bytes();OUT.mkdir();(OUT/Path(__file__).name).write_bytes(original)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:cases=list(pool.map(run,SPECS))
 assert Path(__file__).read_bytes()==original
 report=dict(candidate='diagnostic_v1597_native_ground_throw',cases=cases,sourceSHA256=hashlib.sha256(original).hexdigest().upper(),
  allRunnersTerminal=True,allRunnerExitsZero=all(r['runnerExit']==0 for r in cases),independentVerificationPending=True,fullPortAcceptance=False)
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 raise SystemExit(0 if report['allRunnerExitsZero']else 1)
