"""Finite Kano P1 crouching/back-direction hit and appropriate-block pilots."""
import json
import subprocess
import sys
from refresh_special_videos import BASE,PORT,FLAGS,command
from qualify_normal_contact import qualify

def plan(prefix,crouch_only=False):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    fixtures=[]
    for move,gap,low in (('roundhouse',90,False),('sweep',90,True),('uppercut',70,False),
                         ('duckpunch',70,True),('duckhighkick',70,True),('ducklowkick',70,True)):
        if crouch_only and move in ('roundhouse','sweep'):continue
        for blocking in (False,True):
            name=f'{prefix}_{move}_'+('block' if blocking else 'hit')
            args=['--game','--normal-moves',f'--normal-case={move}','--normal-attacker=1',
                  f'--normal-gap={gap}','--sound-candidate',*(['--normal-block'] if blocking else []),
                  *(['--normal-low-block'] if blocking and low else [])]
            fixtures.append((name,args))
    return fixtures

def main(prefix,crouch_only=False):
    fixtures=plan(prefix,crouch_only)
    assert all(not (BASE/name).exists() for name,_ in fixtures),'Never overwrite evidence'
    results=[]
    for name,args in fixtures:
        if sys.platform=='win32':
            idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],capture_output=True,creationflags=FLAGS)
            assert idle.returncode==0,'Existing emulator'
        command(BASE/'test_wolf_baseline.py',name,*args)
        results.append(dict(run=name,**qualify(name)))
        print('QUALIFIED_GROUND_CONTACT',name,flush=True)
    (PORT/('CROUCH_CONTACT_PILOTS_2219.json' if crouch_only else 'GROUND_CONTACT_PILOTS_2219.json')).write_text(json.dumps(dict(cases=results,
        fullActorSideMatrixVerified=False,allNormalsVerified=False,fullPortVerified=False),indent=2)+'\n')

if __name__=='__main__':
    assert len(sys.argv) in (2,3)
    assert len(sys.argv)==2 or sys.argv[2]=='--crouch-only'
    main(sys.argv[1],len(sys.argv)==3)
