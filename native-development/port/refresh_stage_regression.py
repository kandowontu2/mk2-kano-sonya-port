"""Sequential hidden own-pair native stage/chord/rejoin fixtures."""
from pathlib import Path
import subprocess
import sys
from stage_profiles import profile

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'

def plan(prefix):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    fixtures=[]
    variants=(['--deadpool'],['--stage-rematch'],
              ['--deadpool','--deadpool-no-chord'],['--stage-rematch','--pit-progress','--pit-rejoin'])
    for variant in variants:
        for mirror in ([],['--mirror']):
            for actor in ([],['--sonya']):
                args=['--game','--stage','--own-victim',*variant,*mirror,*actor,'--sound-candidate']
                kind,identity,side=profile(args)
                fixtures.append((f'{prefix}_{kind}_{identity}_p{side}',args))
    return fixtures

def run(prefix):
    fixtures=plan(prefix)
    assert all(not (BASE/name).exists() for name,_ in fixtures),'Never overwrite runtime evidence'
    flags=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform=='win32' else 0
    def check(script,*arguments):
        result=subprocess.run([sys.executable,str(PORT/script),*arguments],cwd=PORT,
                              capture_output=True,text=True,creationflags=flags)
        assert result.returncode==0,result.stderr[-3000:]
    for index,(name,args) in enumerate(fixtures,1):
        kind,actor,_=profile(args)
        if sys.platform=='win32':
            idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process -Name mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                capture_output=True,creationflags=flags)
            assert idle.returncode==0,'Existing MAME process: do not overlap or terminate it'
        print(f'{index}/16 START {name}',flush=True)
        subprocess.run([sys.executable,str(BASE/'test_wolf_baseline.py'),name,*args],
                       cwd=BASE,check=True,creationflags=flags)
        if kind in ('deadpool','negative'):check('qualify_deadpool_runtime.py',name)
        elif kind=='tomb':check('qualify_tomb_stage.py',name,str(actor))
        else:check('qualify_pit_rejoin.py',name,str(actor))
        print(f'{index}/16 QUALIFIED {name}',flush=True)
    check('qualify_stage_positive_matrix.py',*[name for name,_ in fixtures])
    print('All sixteen finite stage/chord/rejoin cases qualified; full port not certified.',flush=True)

if __name__=='__main__':
    assert len(sys.argv)==2,'Supply a fresh evidence prefix'
    run(sys.argv[1])
