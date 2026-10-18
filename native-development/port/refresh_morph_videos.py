"""Current Shang morph/projectile/automatic-return demonstration clips."""
import json
import subprocess
import sys
from refresh_special_videos import BASE, PORT, FLAGS, command

def plan(prefix):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    return [(f'{prefix}_{actor}',actor,['--game','--morph','--morph-specials',
        *(['--mirror','--capture-side=2','--capture-not-before=4500'] if actor==18 else ['--capture-side=1']),
        '--capture-move','--capture-action=0x404','--audio','--sound-candidate']) for actor in (17,18)]

def main(prefix):
    fixtures=plan(prefix)
    assert all(not (BASE/name).exists() for name,_,_ in fixtures),'Never overwrite evidence'
    completed=[]
    for name,actor,args in fixtures:
        if sys.platform=='win32':
            idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                capture_output=True,creationflags=FLAGS)
            assert idle.returncode==0,'Emulator already running'
        command(BASE/'test_wolf_baseline.py',name,*args)
        command(PORT/'qualify_morph.py',name)
        command(PORT/'encode_finisher_capture.py',name)
        command(PORT/'qualify_captured_morph.py',name,str(actor))
        video=json.loads((BASE/name/'FINISHER_VIDEO.json').read_text())
        completed.append(dict(actor=actor,run=name,file=video['file'],SHA256=video['SHA256'],
            frames=video['frames'],capturedTrueIdentityProjectileAndAutomaticReturn=True))
    command(PORT/'qualify_morph_art_trace.py',*[name for name,_,_ in fixtures])
    (PORT/'MORPH_VIDEOS_2219.json').write_text(json.dumps(dict(cases=completed,
        wholeVideoVisualReviewPassed=False,fullPortVerified=False,releaseReady=False),indent=2)+'\n')
    print('Two current-ROM morph/projectile/automatic-return clips qualified.',flush=True)

if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
