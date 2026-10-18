"""Four explicit original-Liu controls; one hidden emulator at a time."""
import subprocess
import sys
from requalify_recorded_finishers import BASE,FLAGS,check

def plan(prefix):
    assert prefix and all(character.isalnum() or character in '_-' for character in prefix)
    return [(f'{prefix}_{family}_p{side}',
             ['--game','--'+family+'-victim','--stock-victim','--sound-candidate','--finisher-rejoin',
              *(['--mirror'] if side==2 else [])]) for family in ('torso','swipe') for side in (1,2)]

def main(prefix):
    fixtures=plan(prefix)
    assert all(not (BASE/name).exists() for name,_ in fixtures),'Never overwrite runtime evidence'
    for name,args in fixtures:
        if sys.platform=='win32':
            result=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process -Name mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                capture_output=True,creationflags=FLAGS)
            assert result.returncode==0,'An emulator is already running'
        result=subprocess.run([sys.executable,str(BASE/'test_wolf_baseline.py'),name,*args],
                              cwd=BASE,capture_output=True,text=True,creationflags=FLAGS)
        assert result.returncode==0,result.stderr[-3000:]
        print('RECORDED',name,flush=True)
    check('qualify_original_torso_controls.py',*[name for name,_ in fixtures])
    print('Four finite original-Liu controls qualify.',flush=True)

if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
