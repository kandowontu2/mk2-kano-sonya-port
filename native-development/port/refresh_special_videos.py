"""Eight bounded current-ROM special clips, one hidden emulator, encode promptly."""
import json
import subprocess
import sys
from refresh_special_regression import BASE,PORT,verify_case

FLAGS=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform=='win32' else 0

def plan(prefix):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    specs=[('ball',['--special'],0x20b,1,0),('blade',['--blade'],0x117,1,3918),
           ('choke',['--choke'],0x216,1,4108),('leg',['--leg'],0x219,2,4906),
           ('bike',['--bike'],0x204,2,0),('square',['--special','--square'],0x207,2,0),
           ('knife',['--projectiles'],0x211,1,0),('ring',['--projectiles'],0x212,2,0)]
    return [(prefix+'_'+kind,kind,['--game',*profile,'--sound-candidate','--audio','--capture-move',
             f'--capture-action={action:#x}',f'--capture-side={side}',
             f'--capture-not-before={begin}','--capture-min-fields=150'])
            for kind,profile,action,side,begin in specs]

def command(script,*args):
    result=subprocess.run([sys.executable,str(script),*args],cwd=PORT,capture_output=True,
                          text=True,creationflags=FLAGS)
    assert result.returncode==0,(str(script),result.stderr[-3000:])

def main(prefix):
    fixtures=plan(prefix)
    assert all(not (BASE/name).exists() for name,_,_ in fixtures),'Never overwrite evidence'
    completed=[]
    for name,kind,args in fixtures:
        if sys.platform=='win32':
            idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                capture_output=True,creationflags=FLAGS)
            assert idle.returncode==0,'Emulator already running'
        command(BASE/'test_wolf_baseline.py',name,*args)
        verify_case(name,args)
        # Encoder validates clip/ROM/frame/audio decode before deleting only
        # the exact verified BGRA/WAV intermediates in this fresh runtime dir.
        command(PORT/'encode_finisher_capture.py',name)
        command(PORT/'qualify_captured_hit.py',name,kind)
        video=json.loads((BASE/name/'FINISHER_VIDEO.json').read_text())
        completed.append(dict(kind=kind,run=name,file=video['file'],SHA256=video['SHA256']))
        print('QUALIFIED_VIDEO',kind,name,flush=True)
    (PORT/'SPECIAL_VIDEOS_2219.json').write_text(json.dumps(dict(cases=completed,
        allEightCapturedHitIntervalsVerified=True,wholeVideoVisualReviewPassed=False,
        fullPortVerified=False,releaseReady=False),indent=2)+'\n')
    print('Eight current-ROM special clips encoded and captured-hit qualified.',flush=True)

if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
