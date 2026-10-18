"""Sequential hidden current-ROM morph/projectile and late-throw expiry cases."""
from pathlib import Path
import subprocess
import sys

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'

def plan(prefix,ball_only=False,all_specials=False):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    assert not (ball_only and all_specials)
    cases=[]
    modes=(('ball',['--morph-ball']),) if ball_only else (('special',['--morph-specials']),('late',['--morph-throws','--morph-late-throw']))
    if all_specials:
        modes=tuple((kind,['--morph-'+flag]) for kind,flag in
                    (('special','specials'),('ball','ball'),('square','square'),
                     ('melee','melee'),('grapples','grapples')))
    for kind,extra in modes:
        for side,mirror in ((1,[]),(2,['--mirror'])):
            cases.append((f'{prefix}_{kind}_p{side}',['--game','--morph',*extra,*mirror,'--sound-candidate']))
    return cases

def run(prefix,ball_only=False,all_specials=False):
    fixtures=plan(prefix,ball_only,all_specials)
    assert all(not (BASE/name).exists() for name,_ in fixtures),'Never overwrite runtime evidence'
    flags=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform=='win32' else 0
    def check(script,*arguments):
        result=subprocess.run([sys.executable,str(PORT/script),*arguments],cwd=PORT,
                              capture_output=True,text=True,creationflags=flags)
        assert result.returncode==0,result.stderr[-3000:]
    for index,(name,args) in enumerate(fixtures,1):
        if sys.platform=='win32':
            idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process -Name mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                capture_output=True,creationflags=flags)
            assert idle.returncode==0,'Existing MAME process: do not overlap or terminate it'
        print(f'{index}/{len(fixtures)} START {name}',flush=True)
        subprocess.run([sys.executable,str(BASE/'test_wolf_baseline.py'),name,*args],
                       cwd=BASE,check=True,creationflags=flags)
        check('qualify_morph.py',name)
        print(f'{index}/{len(fixtures)} QUALIFIED {name}',flush=True)
    if not ball_only:
        check('qualify_morph_art_trace.py',*[name for name,args in fixtures if '--morph-specials' in args])
    print('Requested finite morph cases qualified; full port not certified.',flush=True)

if __name__=='__main__':
    assert len(sys.argv) in (2,3),'Supply a fresh prefix and optional --ball-only or --all-specials'
    option=sys.argv[2] if len(sys.argv)==3 else ''
    assert option in ('','--ball-only','--all-specials')
    run(sys.argv[1],option=='--ball-only',option=='--all-specials')
