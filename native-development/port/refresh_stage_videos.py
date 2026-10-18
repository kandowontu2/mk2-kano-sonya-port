"""Fresh own-pair stage demonstrations; immutable evidence, stock emulator."""
import csv
import json
import subprocess
import sys
from refresh_stage_regression import plan as regression_plan
from stage_profiles import profile
from refresh_special_videos import BASE, PORT, FLAGS, command

def plan(prefix,pit_only=False):
    fixtures=[]
    for name,args in regression_plan(prefix):
        kind,actor,side=profile(args)
        if side!=1 or kind=='negative':continue
        if pit_only and kind!='pit':continue
        background={'deadpool':0,'tomb':1,'pit':6}[kind]
        fixtures.append((name,kind,actor,[*args,'--audio','--capture-finish',f'--capture-background={background}']))
    assert len(fixtures)==(2 if pit_only else 6)
    return fixtures

def verify_capture(run,kind):
    with (run/'finisher_capture.csv').open() as stream:capture=list(csv.DictReader(stream))
    with (run/'stage_environment.csv').open() as stream:environment={int(r['frame']):r for r in csv.DictReader(stream)}
    frames=[int(r['frame']) for r in capture]
    assert frames and frames==list(range(frames[0],frames[-1]+1))
    background={'deadpool':0,'tomb':1,'pit':6}[kind]
    assert all(int(environment[f]['background'])==background for f in frames),'Captured wrong arena'
    if kind=='pit':
        with (run/'pit_objects.csv').open() as stream:objects=list(csv.DictReader(stream))
        proof=json.loads((run/'qualification.json').read_text())
        first=int(objects[0]['frame'])-proof['nativeLaunchToFallFields']
        assert frames==list(range(first,first+proof['nativePitActionFields']+60)),'Incomplete Pit cinematic capture'

def main(prefix,pit_only=False):
    fixtures=plan(prefix,pit_only)
    assert all(not (BASE/name).exists() for name,_,_,_ in fixtures),'Never overwrite evidence'
    completed=[]
    for name,kind,actor,args in fixtures:
        if sys.platform=='win32':
            idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                capture_output=True,creationflags=FLAGS)
            assert idle.returncode==0,'Emulator already running'
        command(BASE/'test_wolf_baseline.py',name,*args)
        if kind=='deadpool':command(PORT/'qualify_deadpool_runtime.py',name)
        elif kind=='tomb':command(PORT/'qualify_tomb_stage.py',name,str(actor))
        else:command(PORT/'qualify_pit_rejoin.py',name,str(actor))
        verify_capture(BASE/name,kind)
        command(PORT/'encode_finisher_capture.py',name)
        video=json.loads((BASE/name/'FINISHER_VIDEO.json').read_text())
        completed.append(dict(kind=kind,actor=actor,run=name,file=video['file'],
            SHA256=video['SHA256'],frames=video['frames']))
        print('QUALIFIED_STAGE_VIDEO',kind,actor,name,flush=True)
    (PORT/('PIT_VIDEOS_2219.json' if pit_only else 'STAGE_VIDEOS_2219.json')).write_text(json.dumps(dict(cases=completed,
        wholeVideoVisualReviewPassed=False,fullPortVerified=False,releaseReady=False),indent=2)+'\n')
    print(f'{len(fixtures)} current-ROM native stage clips encoded and qualified.',flush=True)

if __name__=='__main__':
    assert len(sys.argv) in (2,3)
    assert len(sys.argv)==2 or sys.argv[2]=='--pit-only'
    main(sys.argv[1],len(sys.argv)==3)
