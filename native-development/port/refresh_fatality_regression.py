"""Sequential hidden own-fatality/reselection regressions on the current ROM."""
import importlib
import json
from pathlib import Path
import subprocess
import sys
from qualify_own_fatality_matrix import profile,qualify as matrix

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'

def plan(prefix):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    fixtures=[['--game','--'+kind,*mirror,'--sound-candidate','--finisher-rejoin']
              for mirror in ([],['--mirror']) for kind in ('extract','laser','kiss','bubble')]
    return [(f'{prefix}_{i:02d}',args) for i,args in enumerate(fixtures,1)]

def run(prefix):
    fixtures=plan(prefix)
    assert all(not (BASE/name).exists() for name,_ in fixtures),'Never overwrite runtime evidence'
    flags=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform=='win32' else 0
    for index,(name,args) in enumerate(fixtures,1):
        if sys.platform=='win32':
            idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process -Name mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                capture_output=True,creationflags=flags)
            assert idle.returncode==0,'Existing MAME process: do not overlap or terminate it'
        print(f'{index}/8 START {name}',flush=True)
        subprocess.run([sys.executable,str(BASE/'test_wolf_baseline.py'),name,*args],
                       cwd=BASE,check=True,creationflags=flags)
        rejoin=subprocess.run([sys.executable,str(PORT/'qualify_finisher_rejoin.py'),name],
                              cwd=PORT,capture_output=True,text=True,creationflags=flags)
        assert rejoin.returncode==0,rejoin.stderr[-3000:]
        kind,side,victim=profile(args)
        importlib.import_module('qualify_'+kind).qualify(name,side,victim)
        print(f'{index}/8 QUALIFIED {name}',flush=True)
    result=matrix([name for name,_ in fixtures])
    print(json.dumps(dict(currentFiniteCases=len(result['cases']),
                          allEightCasesPassed=result['allEightCasesPassed'],
                          fullPortVerified=False)),flush=True)

if __name__=='__main__':
    assert len(sys.argv)==2,'Supply a fresh output prefix; existing MAME processes are never interrupted'
    run(sys.argv[1])
