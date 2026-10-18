"""Four earned Jax head-clap victims/reselections on current stock ROMs."""
import subprocess
import sys
from refresh_freeze_regression import plan as freeze_plan
from requalify_recorded_finishers import BASE,FLAGS,check

def plan(prefix):
    return [(name,['--clap-victim' if arg=='--freeze-victim' else arg for arg in args]+['--finisher-rejoin'])
            for name,args in freeze_plan(prefix)]

def main(prefix):
    fixtures=plan(prefix)
    assert all(not (BASE/name).exists() for name,_ in fixtures),'Never overwrite runtime evidence'
    for name,args in fixtures:
        if sys.platform=='win32':
            idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process -Name mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                capture_output=True,creationflags=FLAGS)
            assert idle.returncode==0,'An emulator is already running'
        result=subprocess.run([sys.executable,str(BASE/'test_wolf_baseline.py'),name,*args],
                              cwd=BASE,capture_output=True,text=True,creationflags=FLAGS)
        assert result.returncode==0,result.stderr[-3000:]
        check('qualify_clap_runtime.py',name)
        print('QUALIFIED',name,flush=True)
    check('qualify_clap_runtime.py',*[name for name,_ in fixtures])
    print('Four current-ROM earned Jax clap cases qualify.',flush=True)

if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
