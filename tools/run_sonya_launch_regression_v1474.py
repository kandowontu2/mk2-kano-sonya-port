"""Cold real-input launch audio regression, without guest-state assistance."""
import concurrent.futures,subprocess,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
CASES=[(move,side,False) for move in ('square','bicycle','leg','choke') for side in (1,2)]+[('square',side,True) for side in (1,2)]
def run(case):
    move,side,air=case;name=f'audit_v1475_human_launch_{move}'+('_air' if air else '')+f'_p{side}'
    if (ROOT/name).exists():raise RuntimeError('Do not overwrite or restart: '+name)
    cmd=[PWSH,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'tools/run_sonya_launch_audio_v1474.ps1'),'-CaseName',name,'-Move',move,'-Side',str(side)]
    if air:cmd.append('-Air')
    result=subprocess.run(cmd,capture_output=True,text=True)
    print(json.dumps({'case':name,'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr}),flush=True)
    if result.returncode:raise RuntimeError('Failed: '+name)
    metadata=json.loads((ROOT/name/'result.json').read_text(encoding='utf-8-sig'))
    if metadata['exit_code']!=0:raise RuntimeError('Runtime failed: '+name)
    return name
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:cases=list(pool.map(run,CASES))
    print(json.dumps({'terminal_cases':cases,'acceptance':'Independent verification pending'}),flush=True)
