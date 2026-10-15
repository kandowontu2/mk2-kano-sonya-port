"""Actual host audio ownership logs and old-build airborne audio baselines."""
import concurrent.futures,subprocess,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
CASES=[(f'audit_v1478_host_launch_{move}_p{side}',move,side,False,'diagnostic_v1473_sonya_launch_audio') for move in ('square','bicycle') for side in (1,2)]+[(f'audit_v1478_baseline_square_air_p{side}','square',side,True,'diagnostic_v1411_native_grab_audio') for side in (1,2)]
def run(case):
    name,move,side,air,candidate=case
    if (ROOT/name).exists():raise RuntimeError('Never overwrite or restart: '+name)
    cmd=[PWSH,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'tools/run_sonya_launch_audio_v1477.ps1'),'-CaseName',name,'-Move',move,'-Side',str(side),'-CandidateName',candidate]
    if air:cmd.append('-Air')
    r=subprocess.run(cmd,capture_output=True,text=True)
    print(json.dumps({'case':name,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr}),flush=True)
    if r.returncode or json.loads((ROOT/name/'result.json').read_text(encoding='utf-8-sig'))['exit_code']:raise RuntimeError(name)
    return name
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,CASES))
    print(json.dumps({'terminal':results}),flush=True)
