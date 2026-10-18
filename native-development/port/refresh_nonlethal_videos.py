"""Current earned Friendship/Babality clips with eligibility and recovery checks."""
import csv
import json
import subprocess
import sys
from refresh_nonlethal_regression import plan as regression_plan
from nonlethal_profiles import profile
from refresh_special_videos import BASE,PORT,FLAGS,command

def plan(prefix):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    fixtures=[]
    for _,args,negative in regression_plan(prefix):
        if negative or '--mirror' in args:continue
        kind,actor,side,_=profile(args)
        assert side==1
        fixtures.append((f'{prefix}_{kind}_{actor}',kind,actor,[*args,'--audio','--capture-finish']))
    assert len(fixtures)==4
    return fixtures

def main(prefix):
    fixtures=plan(prefix)
    assert all(not (BASE/name).exists() for name,_,_,_ in fixtures),'Never overwrite evidence'
    completed=[]
    for name,kind,actor,args in fixtures:
        if sys.platform=='win32':
            idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                capture_output=True,creationflags=FLAGS)
            assert idle.returncode==0,'Emulator already running'
        command(BASE/'test_wolf_baseline.py',name,*args)
        command(PORT/'qualify_finisher_rejoin.py',name)
        if kind=='baby':command(PORT/'qualify_baby.py',name,str(actor))
        else:command(PORT/('qualify_kano_friend.py' if actor==17 else 'qualify_sonya_friend.py'),name)
        if kind=='friend' and actor==18:command(PORT/'qualify_friend_lifecycle.py',name)
        run=BASE/name
        proof=json.loads((run/'qualification.json').read_text())
        assert proof['currentFull26ROMBytesVerified']
        with (run/'finisher_capture.csv').open() as stream:capture=list(csv.DictReader(stream))
        with (run/(kind+'.csv')).open() as stream:
            active=[row for row in csv.DictReader(stream) if row['mode']=='2' and row['death'] not in ('0','65535')]
        assert capture and [row['frame'] for row in capture]==[row['frame'] for row in active]
        command(PORT/'encode_finisher_capture.py',name)
        video=json.loads((run/'FINISHER_VIDEO.json').read_text())
        completed.append(dict(kind=kind,actor=actor,run=name,file=video['file'],SHA256=video['SHA256'],
            frames=video['frames'],allActiveFinisherFramesCaptured=True,freshCombatFields=600))
        print('QUALIFIED_NONLETHAL_VIDEO',kind,actor,name,flush=True)
    (PORT/'NONLETHAL_VIDEOS_2219.json').write_text(json.dumps(dict(cases=completed,
        allFourEarnedEligibleSequencesVerified=True,postCompletionLoopsFullyCaptured=False,
        wholeVideoVisualReviewPassed=False,fullPortVerified=False,releaseReady=False),indent=2)+'\n')
    print('Four current-ROM eligible nonlethal clips encoded and qualified.',flush=True)

if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
