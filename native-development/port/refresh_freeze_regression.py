"""Four explicit current-ROM ice-hit/thaw cases, hidden and sequential."""
import subprocess
import sys
from requalify_recorded_finishers import BASE,FLAGS,check

def plan(prefix):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    return [(f'{prefix}_{actor}_p{side}',
             ['--game','--freeze-victim',*(['--sonya'] if actor==18 else []),
              *(['--mirror'] if side==1 else []),'--sound-candidate'])
            for side in (2,1) for actor in (17,18)]

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
        print('RECORDED',name,flush=True)
    check('qualify_frozen_victims.py',*[name for name,_ in fixtures])
    print('Four current-ROM freeze/thaw cases qualify.',flush=True)

if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
