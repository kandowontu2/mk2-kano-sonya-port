"""Sequential finite transformed-finisher/fresh-Shang checks; no guest writes."""
import json
from pathlib import Path
import subprocess
import sys

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'

def plan(prefix):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    return [(f'{prefix}_{kind}_rejoin_p{side}',kind,side,
             ['--game','--'+kind,'--finisher-morph','--finisher-rejoin','--sound-candidate',
              *(['--mirror'] if side==2 else [])])
            for kind in ('extract','kiss','laser','bubble') for side in (1,2)]

def run(prefix):
    flags=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform=='win32' else 0
    def check(script,*args):
        result=subprocess.run([sys.executable,str(PORT/script),*args],cwd=PORT,
                              capture_output=True,text=True,creationflags=flags)
        assert result.returncode==0,result.stderr[-2500:]
    fixtures=plan(prefix)
    for index,(name,kind,side,args) in enumerate(fixtures,1):
        folder=BASE/name
        if folder.exists():
            receipt=json.loads((folder/'execution.json').read_text())
            assert receipt['exitCode']==0 and not receipt['timedOut']
            assert receipt['testArguments']==args,'Existing evidence has a different profile'
        else:
            if sys.platform=='win32':
                idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                    'if (Get-Process -Name mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                    capture_output=True,creationflags=flags)
                assert idle.returncode==0,'Existing MAME: do not overlap or terminate it'
            print(f'{index}/{len(fixtures)} START {name}',flush=True)
            subprocess.run([sys.executable,str(BASE/'test_wolf_baseline.py'),name,*args],
                           cwd=BASE,check=True,capture_output=True,creationflags=flags)
        check('qualify_finisher_rejoin.py',name)
        check('qualify_'+kind+'.py',name,str(side),'17' if kind in ('kiss','bubble') else '18')
        print(f'{index}/{len(fixtures)} QUALIFIED {name}',flush=True)
    check('qualify_morph_finisher_rejoin_matrix.py',*[name for name,_,_,_ in fixtures])
    print('Requested finite transformed-finisher/fresh-Shang cases and matrix qualify; full port not certified.',flush=True)

if __name__=='__main__':
    assert len(sys.argv)==2,'Supply an explicit evidence prefix'
    run(sys.argv[1])
