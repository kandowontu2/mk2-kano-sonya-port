"""34 native normal/proximity demonstrations, hidden and encoded one at a time."""
import csv
import json
import subprocess
import sys
from refresh_special_videos import BASE,PORT,FLAGS,command
from qualify_normal_contact import qualify,contact_spec
from qualify_captured_normal import verify_interval

def plan(prefix):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    fixtures=[]
    for actor in (17,18):
        for label,move,gap in (('hp','hp',90),('lp','lp',90),('hk','hk',100),('lk','lk',100),
            ('roundhouse','roundhouse',90),('sweep','sweep',90),('uppercut','uppercut',70),
            ('duckpunch','duckpunch',70),('duckhighkick','duckhighkick',70),('ducklowkick','ducklowkick',70),
            ('jumpkick','jumpkick',70),('jumppunch','jumppunch',70),('flyingkick','flyingkick',180),
            ('flyingpunch','flyingpunch',220 if actor==18 else 180),('knee','hk',70),('elbow','hp',70),('throw','lp',70)):
            action=contact_spec(move,gap,False)[0]
            args=['--game','--normal-moves',f'--normal-case={move}','--normal-attacker=1',
                  f'--normal-gap={gap}',*(['--mirror'] if actor==18 else []),'--sound-candidate','--audio',
                  '--capture-move',f'--capture-action={action:#x}','--capture-side=1','--capture-min-fields=150']
            fixtures.append((f'{prefix}_{actor}_{label}',actor,label,args))
    assert len(fixtures)==34
    return fixtures

def main(prefix):
    fixtures=plan(prefix)
    assert all(not (BASE/name).exists() for name,_,_,_ in fixtures),'Never overwrite evidence'
    results=[]
    for name,actor,label,args in fixtures:
        if sys.platform=='win32':
            idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],capture_output=True,creationflags=FLAGS)
            assert idle.returncode==0,'Existing emulator'
        command(BASE/'test_wolf_baseline.py',name,*args)
        contact=qualify(name);assert contact['actor']==actor and contact['side']==1
        run=BASE/name
        with (run/'finisher_capture.csv').open() as stream:captured=list(csv.DictReader(stream))
        frames=[int(r['frame']) for r in captured]
        assert frames and frames==list(range(frames[0],frames[-1]+1))
        with (run/'normals.csv').open() as stream:
            interval=[r for r in csv.DictReader(stream) if frames[0]<=int(r['frame'])<=frames[-1]]
        assert [int(r['frame']) for r in interval]==frames
        verify_interval(interval,1,contact['actualAction'],contact['damage'])
        # Verify captured contact/recovery BEFORE the encoder removes raw/WAV.
        command(PORT/'encode_finisher_capture.py',name)
        command(PORT/'qualify_captured_normal.py',name)
        video=json.loads((BASE/name/'FINISHER_VIDEO.json').read_text())
        results.append(dict(actor=actor,label=label,run=name,file=video['file'],SHA256=video['SHA256'],frames=video['frames']))
        print('QUALIFIED_NORMAL_VIDEO',actor,label,name,flush=True)
    (PORT/'NORMAL_VIDEOS_2219.json').write_text(json.dumps(dict(cases=results,
        wholeVideoVisualReviewPassed=False,fullPortVerified=False,releaseReady=False),indent=2)+'\n')

if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
