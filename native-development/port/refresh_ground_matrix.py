"""Ground-family contact matrix: reuse12 pilots, run36 missing role cells."""
import json
import subprocess
import sys
from refresh_special_videos import BASE,PORT,FLAGS,command
from refresh_ground_contact import plan as pilot_plan
from refresh_jump_contact import plan as jump_plan
from qualify_normal_contact import qualify

def plan(prefix,jump=False):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    fixtures=[]
    for actor in (17,18):
        for side in (1,2):
            for _,original in (jump_plan('unused') if jump else pilot_plan('unused')):
                args=[f'--normal-attacker={side}' if arg=='--normal-attacker=1' else arg for arg in original]
                if (actor==18 and side==1) or (actor==17 and side==2):args.append('--mirror')
                move=next(arg.split('=')[1] for arg in args if arg.startswith('--normal-case='))
                spaced=jump and actor==18 and move=='flyingpunch'
                if spaced:args=['--normal-gap=220' if arg=='--normal-gap=180' else arg for arg in args]
                kind='block' if '--normal-block' in args else 'hit'
                reuse=actor==17 and side==1
                if reuse:
                    old='stock_wolf_2219_jump_contact' if jump else ('stock_wolf_2219_ground_contact' if move in ('roundhouse','sweep') else 'stock_wolf_2219_crouch_prepared')
                    name=f'{old}_{move}_{kind}'
                else:name=f'{prefix}_{move}_{actor}_p{side}_'+('220_' if spaced else '')+kind
                fixtures.append((name,args,reuse))
    assert len(fixtures)==(32 if jump else 48)
    return fixtures

def main(prefix,jump=False,resume=False):
    fixtures=plan(prefix,jump)
    assert resume or all((BASE/name).exists()==reuse for name,_,reuse in fixtures),'Never overwrite evidence'
    results=[]
    for name,args,reuse in fixtures:
        existing=BASE/name
        if not reuse and resume and existing.exists():
            receipt=json.loads((existing/'execution.json').read_text())
            assert receipt['testArguments']==args and receipt['exitCode']==0 and not receipt['timedOut']
        if not reuse and not existing.exists():
            if sys.platform=='win32':
                idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                    'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],capture_output=True,creationflags=FLAGS)
                assert idle.returncode==0,'Existing emulator'
            command(BASE/'test_wolf_baseline.py',name,*args)
        report=qualify(name)
        assert report['nativeHitByTagObserved'] is True
        results.append(dict(run=name,**report))
        print('QUALIFIED_CONTACT_MATRIX',name,flush=True)
    output='JUMP_CONTACT_MATRIX_2219.json' if jump else 'GROUND_CONTACT_MATRIX_2219.json'
    (PORT/output).write_text(json.dumps(dict(cases=results,expectedCases=32 if jump else 48,
        allFiniteContactCellsPassed=True,allNormalsVerified=False,fullPortVerified=False),indent=2)+'\n')
    print('CONTACT_MATRIX_COMPLETE',len(results),flush=True)

if __name__=='__main__':
    assert len(sys.argv) in (2,3,4)
    assert all(arg in ('--jump','--resume') for arg in sys.argv[2:])
    assert len(sys.argv[2:])==len(set(sys.argv[2:]))
    main(sys.argv[1],'--jump' in sys.argv,'--resume' in sys.argv)
