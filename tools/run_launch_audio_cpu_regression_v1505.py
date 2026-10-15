"""Existing genuine CPU routes, new launch-audio candidate; no forced state."""
import concurrent.futures,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
NAME='diagnostic_v1473_sonya_launch_audio'
CASES=[
 ('audit_v1506_cpu_p2_human_kano','tools/run_current_cpu_pair_display_v1438.ps1','kano',604),
 ('audit_v1506_cpu_p2_human_sonya','tools/run_current_cpu_pair_display_v1438.ps1','sonya',604),
 ('audit_v1506_cpu_p1_human_sonya','tools/run_current_cpu_pair_display_v1399.ps1','sonya',605),
 ('audit_v1506_cpu_repeated_p1_human_kano','tools/run_current_cpu_pair_display_v1459.ps1','kano',605)]
def run(job):
 case,runner,player,boot=job
 if(ROOT/case).exists():raise RuntimeError('Never overwrite or restart: '+case)
 r=subprocess.run([PWSH,'-NoProfile','-File',str(ROOT/runner),'-CaseName',case,'-Player',player,'-BootFrame',str(boot),'-CandidateName',NAME],cwd=ROOT,capture_output=True,text=True)
 print(json.dumps(dict(case=case,exit=r.returncode,stdout=r.stdout,stderr=r.stderr)),flush=True)
 if r.returncode or json.loads((ROOT/case/'result.json').read_text(encoding='utf-8-sig'))['exit_code']:raise RuntimeError(case)
 return case
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:results=list(pool.map(run,CASES))
 print(json.dumps(dict(terminal=results,independentVerificationPending=True)),flush=True)
