"""Four earned current-ROM lethal finisher clips with native fresh-match checks."""
import csv
import importlib
import json
import subprocess
import sys
from refresh_special_videos import BASE,PORT,FLAGS,command

def plan(prefix):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    return [(prefix+'_'+kind,kind,['--game','--'+kind,'--sound-candidate','--audio',
             '--capture-finish','--finisher-rejoin']) for kind in ('extract','laser','kiss','bubble')]

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
        command(PORT/'qualify_finisher_rejoin.py',name)
        importlib.import_module('qualify_'+kind).qualify(name,1,18 if kind in ('extract','laser') else 17)
        run=BASE/name
        move=json.loads((run/'qualification.json').read_text())
        assert move['currentFull26ROMBytesVerified'] and move['nativeCompletionObserved']
        with (run/'finisher_capture.csv').open() as stream:capture=list(csv.DictReader(stream))
        with (run/(kind+'.csv')).open() as stream:
            active=[row for row in csv.DictReader(stream) if row['mode']=='2' and row['death'] in ('1','2')]
        assert [row['frame'] for row in capture]==[row['frame'] for row in active]
        assert len(capture)==move['nativeActionFields']
        command(PORT/'encode_finisher_capture.py',name)
        video=json.loads((run/'FINISHER_VIDEO.json').read_text())
        completed.append(dict(kind=kind,run=name,file=video['file'],SHA256=video['SHA256'],
            frames=video['frames'],allActiveFinisherFramesCaptured=True,freshCombatFields=600))
        print('QUALIFIED_LETHAL_VIDEO',kind,name,flush=True)
    (PORT/'LETHAL_VIDEOS_2219.json').write_text(json.dumps(dict(cases=completed,
        allFourEarnedNativeFinishersVerified=True,wholeVideoVisualReviewPassed=False,
        fullPortVerified=False,releaseReady=False),indent=2)+'\n')
    print('Four current-ROM earned lethal clips encoded and qualified.',flush=True)

if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
