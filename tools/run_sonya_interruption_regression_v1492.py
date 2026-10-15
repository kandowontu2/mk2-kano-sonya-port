"""Remaining normal-audio read-only live channel fixtures."""
import concurrent.futures,subprocess,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
CASES=[('square',2),('bicycle',1),('bicycle',2)]
def run(case):
 move,side=case;name=f'audit_v1492_{move}_interruption_p{side}'
 if (ROOT/name).exists():raise RuntimeError('Never overwrite: '+name)
 r=subprocess.run([PWSH,'-NoProfile','-File',str(ROOT/'tools/run_sonya_launch_interruption_v1491.ps1'),'-CaseName',name,'-Move',move,'-Side',str(side)],capture_output=True,text=True)
 print(json.dumps({'case':name,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr}),flush=True)
 if r.returncode or json.loads((ROOT/name/'result.json').read_text(encoding='utf-8-sig'))['exit_code']:raise RuntimeError(name)
 return name
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:results=list(pool.map(run,CASES))
 print(json.dumps({'terminal':results}),flush=True)
