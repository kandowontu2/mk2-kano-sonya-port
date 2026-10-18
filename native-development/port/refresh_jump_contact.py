"""Eight physical Kano P1 jumping-contact pilots; not an all-role matrix."""
import json
import subprocess
import sys
from refresh_special_videos import BASE,PORT,FLAGS,command
from qualify_normal_contact import qualify

def plan(prefix):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    return [(f'{prefix}_{move}_'+('block' if blocking else 'hit'),
             ['--game','--normal-moves',f'--normal-case={move}','--normal-attacker=1',
              f'--normal-gap={gap}','--sound-candidate',*(['--normal-block'] if blocking else [])])
            for move,gap in (('jumpkick',70),('jumppunch',70),('flyingkick',180),('flyingpunch',180))
            for blocking in (False,True)]

def main(prefix):
    fixtures=plan(prefix)
    assert all(not (BASE/name).exists() for name,_ in fixtures),'Never overwrite evidence'
    results=[]
    for name,args in fixtures:
        if sys.platform=='win32':
            idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],capture_output=True,creationflags=FLAGS)
            assert idle.returncode==0,'Existing emulator'
        command(BASE/'test_wolf_baseline.py',name,*args)
        results.append(dict(run=name,**qualify(name)))
        print('QUALIFIED_JUMP_CONTACT',name,flush=True)
    (PORT/'JUMP_CONTACT_PILOTS_2219.json').write_text(json.dumps(dict(cases=results,
        fullActorSideMatrixVerified=False,allNormalsVerified=False,fullPortVerified=False),indent=2)+'\n')

if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
