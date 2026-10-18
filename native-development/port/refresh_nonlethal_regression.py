"""Sequential hidden current-ROM nonlethal positives and punch-ineligible commands."""
from pathlib import Path
import subprocess
import sys
from nonlethal_profiles import profile

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'

def plan(prefix):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    fixtures=[]
    for negative in (False,True):
        index=0
        for mirror in ([],['--mirror']):
            for base in (['--friend','--kano'],['--friend'],['--baby','--own-victim'],['--baby','--own-victim','--sonya']):
                index+=1
                args=['--game',*base,*mirror,'--sound-candidate']
                if negative:args+=['--punch-wins']
                else:
                    args+=['--finisher-rejoin']
                    if '--friend' in args and '--kano' not in args:args+=['--friend-lifecycle']
                fixtures.append((f'{prefix}_{"neg" if negative else "pos"}_{index:02d}',args,negative))
    return fixtures

def run(prefix):
    fixtures=plan(prefix)
    assert all(not (BASE/name).exists() for name,_,_ in fixtures),'Never overwrite runtime evidence'
    flags=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform=='win32' else 0
    def check(script,*arguments):
        result=subprocess.run([sys.executable,str(PORT/script),*arguments],cwd=PORT,
                              capture_output=True,text=True,creationflags=flags)
        assert result.returncode==0,result.stderr[-3000:]
    for index,(name,args,negative) in enumerate(fixtures,1):
        kind,actor,_,_=profile(args,negative)
        if sys.platform=='win32':
            idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process -Name mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                capture_output=True,creationflags=flags)
            assert idle.returncode==0,'Existing MAME process: do not overlap or terminate it'
        print(f'{index}/16 START {name}',flush=True)
        subprocess.run([sys.executable,str(BASE/'test_wolf_baseline.py'),name,*args],
                       cwd=BASE,check=True,creationflags=flags)
        if not negative:check('qualify_finisher_rejoin.py',name)
        if kind=='baby':check('qualify_baby.py',name,str(actor))
        else:check('qualify_kano_friend.py' if actor==17 else 'qualify_sonya_friend.py',name)
        if kind=='friend' and actor==18 and not negative:check('qualify_friend_lifecycle.py',name)
        print(f'{index}/16 QUALIFIED {name}',flush=True)
    for negative,script in ((False,'qualify_nonlethal_matrix.py'),(True,'qualify_negative_nonlethal_matrix.py')):
        check(script,*[name for name,_,mode in fixtures if mode==negative])
    print('All eight positive and eight punch-ineligible finite cases qualified; full port not certified.',flush=True)

if __name__=='__main__':
    assert len(sys.argv)==2,'Supply a fresh evidence prefix'
    run(sys.argv[1])
