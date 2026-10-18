"""Sixteen finite knee/high-kick contact cells, reusing four immutable pilots."""
import json
import subprocess
import sys
from refresh_special_videos import BASE,PORT,FLAGS,command
from qualify_normal_contact import qualify

def plan(prefix,basic=False):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    fixtures=[]
    for actor in (17,18):
        for side in (1,2):
            mirror=(side==1 and actor==18) or (side==2 and actor==17)
            variants=(('hp',70),('hp',90),('lp',70),('lp',90),('lk',100)) if basic else (('hk',70),('hk',100))
            for move,gap in variants:
                for blocking in (False,True):
                    kind='block' if blocking else 'hit'
                    reuse=actor==17 and side==1 and gap!=90
                    if reuse:
                        suffix='pilot' if gap==70 or move=='lk' else 'gap100'
                        name=f'stock_wolf_2219_normal_basic_{move}_{kind}_{suffix}' if basic else f'stock_wolf_2219_normal_hk_{kind}_{suffix}'
                    else:name=f'{prefix}_{move}_{actor}_p{side}_{gap}_{kind}' if basic else f'{prefix}_{actor}_p{side}_{gap}_{kind}'
                    args=['--game','--normal-moves',f'--normal-case={move}',f'--normal-attacker={side}',
                          *([f'--normal-gap={gap}'] if gap!=70 else []),*(['--mirror'] if mirror else []),
                          *(['--normal-block'] if blocking else []),'--sound-candidate']
                    fixtures.append((name,args,reuse))
    return fixtures

def main(prefix,basic=False,resume=False):
    fixtures=plan(prefix,basic)
    assert resume or all((BASE/name).exists()==reuse for name,_,reuse in fixtures),'Never overwrite evidence'
    results=[]
    for name,args,reuse in fixtures:
        existing=BASE/name
        if not reuse and resume and existing.exists():
            receipt=json.loads((existing/'execution.json').read_text())
            assert receipt['testArguments']==args,'Existing evidence profile mismatch'
            assert receipt['exitCode']==0 and not receipt['timedOut']
        if not reuse and not existing.exists():
            if sys.platform=='win32':
                idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                    'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],capture_output=True,creationflags=FLAGS)
                assert idle.returncode==0,'Existing emulator'
            command(BASE/'test_wolf_baseline.py',name,*args)
        report=qualify(name);results.append(dict(run=name,**report))
        print('QUALIFIED_NORMAL_CONTACT',name,flush=True)
    output='BASIC_NORMAL_CONTACT_MATRIX_2219.json' if basic else 'NORMAL_CONTACT_MATRIX_2219.json'
    (PORT/output).write_text(json.dumps(dict(cases=results,
        allFiniteContactCasesPassed=True,expectedCases=40 if basic else 16,
        allNormalsVerified=False,fullPortVerified=False),indent=2)+'\n')
    print('CONTACT_MATRIX_COMPLETE',len(results),flush=True)

if __name__=='__main__':
    assert len(sys.argv) in (2,3,4)
    assert all(arg in ('--basic','--resume') for arg in sys.argv[2:])
    assert len(sys.argv[2:])==len(set(sys.argv[2:]))
    main(sys.argv[1],'--basic' in sys.argv,'--resume' in sys.argv)
