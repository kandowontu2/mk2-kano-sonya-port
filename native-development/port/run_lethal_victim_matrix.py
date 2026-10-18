"""Earn four native lethals across selectable victims; one hidden emulator only."""
import importlib
import json
import subprocess
import sys
from refresh_special_videos import BASE, PORT, FLAGS, command


def plan(pilot=False):
    victims=(0,) if pilot else (*range(12),17,18)
    return [(f'stock_wolf_2219_lethal_roster_{kind}_{victim}_p{side}',kind,victim,side,
        ['--game','--'+kind,'--sound-candidate','--finisher-rejoin',f'--finisher-victim={victim}']+
        (['--mirror'] if side==2 else []))
        for kind in ('extract','laser','kiss','bubble') for victim in victims for side in (1,2)]


def main(pilot):
    cases=[]
    for name,kind,victim,side,args in plan(pilot):
        run=BASE/name
        if run.exists():
            receipt=json.loads((run/'execution.json').read_text())
            assert receipt['testArguments']==args and receipt['exitCode']==0 and not receipt['timedOut']
        else:
            idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
                'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                capture_output=True,creationflags=FLAGS)
            assert idle.returncode==0,'Existing emulator; no concurrent run allowed'
            command(BASE/'test_wolf_baseline.py',name,*args)
        command(PORT/'qualify_finisher_rejoin.py',name)
        importlib.import_module('qualify_'+kind).qualify(name,side,victim)
        q=json.loads((run/'qualification.json').read_text())
        assert q['currentFull26ROMBytesVerified'] and q['nativeCompletionObserved']
        cases.append(dict(run=name,kind=kind,victim=victim,side=side))
        print('QUALIFIED_LETHAL_VICTIM',kind,victim,side,flush=True)
    report=dict(scope='Finite earned native lethal victim/side cases and fresh-match recovery',
        cases=cases,pilot=pilot,fullPortVerified=False)
    (PORT/('LETHAL_ROSTER_PILOT_2219.json' if pilot else 'LETHAL_ROSTER_2219.json')).write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    assert sys.argv[1:] in (['--pilot'],['--full'])
    main(sys.argv[1]=='--pilot')
