"""Dispatch isolated ORIGINAL hardware-only audio probes, not gameplay tests."""
import concurrent.futures, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
COMMANDS=['baseline']+[f'{base+ch:04x}' for base in (0x212,0x2d0,0x898) for ch in range(5)]
def run(command):
    out=ROOT/f'audit_v1468_original_sonya_launch_isolated_{command}'
    if out.exists():raise RuntimeError('Never restart or overwrite an existing capture: '+str(out))
    result=subprocess.run([PWSH,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'tools/run_original_sonya_launch_isolated_v1468.ps1'),'-Command',command],capture_output=True,text=True)
    print(json.dumps({'command':command,'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr}),flush=True)
    if result.returncode:raise RuntimeError('Original probe failed: '+command)
    metadata=json.loads((out/'result.json').read_text(encoding='utf-8-sig'))
    if metadata['exit_code']!=0:raise RuntimeError('Nonterminal original probe: '+command)
    return command
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results=list(pool.map(run,COMMANDS))
    print(json.dumps({'terminal_commands':results,'scope':'DCS_sound_port_only; zero guest RAM writes; not gameplay acceptance'}),flush=True)
