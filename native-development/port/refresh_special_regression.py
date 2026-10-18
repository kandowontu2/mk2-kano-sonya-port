"""Run one hidden stock emulator at a time; qualify all sixteen finite cases."""
import json
from pathlib import Path
import subprocess
import sys
from qualify_special_matrix import qualify as matrix

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'

def plan(prefix):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    fixtures=[['--projectiles'],['--projectiles','--mirror'],
              ['--special'],['--special','--square'],
              ['--special','--mirror'],['--special','--square','--mirror']]
    fixtures += [[flag]+mirror for mirror in ([],['--mirror'])
                 for flag in ('--blade','--choke','--bike','--leg')]
    return [(f'{prefix}_{i:02d}',['--game',*args,'--sound-candidate'])
            for i,args in enumerate(fixtures,1)]

def verify_case(name,args):
    mirror='--mirror' in args
    if '--projectiles' in args:
        from qualify_projectiles import qualify
        return qualify(name,mirror)
    if '--special' in args:
        from qualify_initial_specials import qualify
        square='--square' in args
        side=(1 if mirror else 2) if square else (2 if mirror else 1)
        return qualify(name,side,0x207 if square else 0x20b)
    if '--blade' in args:
        from qualify_blade import qualify
        return qualify(name,mirror)
    if '--choke' in args:
        from qualify_choke import qualify
        return qualify(name,2 if mirror else 1,18)
    if '--bike' in args:
        from qualify_bike import qualify
        return qualify(name,mirror)
    assert '--leg' in args
    from qualify_leg import qualify
    return qualify(name,1 if mirror else 2,17)

def run(prefix):
    fixtures=plan(prefix)
    assert all(not (BASE/name).exists() for name,_ in fixtures), 'Never overwrite runtime evidence'
    flags=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform=='win32' else 0
    for index,(name,args) in enumerate(fixtures,1):
        if sys.platform=='win32':
            idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process -Name mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                capture_output=True,creationflags=flags)
            assert idle.returncode==0,'An existing MAME process is running; do not overlap or terminate it'
        print(f'{index}/14 START {name} '+ ' '.join(args),flush=True)
        subprocess.run([sys.executable,str(BASE/'test_wolf_baseline.py'),name,*args],
                       cwd=BASE,check=True,creationflags=flags)
        verify_case(name,args)
        print(f'{index}/14 QUALIFIED {name}',flush=True)
    result=matrix([name for name,_ in fixtures])
    print(json.dumps(dict(currentFiniteCases=len(result['cases']),
                          allSixteenFiniteCasesPassed=result['allSixteenFiniteCasesPassed'],
                          fullPortVerified=False)),flush=True)

if __name__=='__main__':
    assert len(sys.argv)==2,'Supply a fresh output prefix; emulator must be idle before starting'
    run(sys.argv[1])
