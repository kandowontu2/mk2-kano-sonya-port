"""Inspect actual normal-move responses; requested inputs alone never pass."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from verify_finisher_roms import verify

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
EXPECTED=dict(hp=0x101,lp=0x102,hk=0x103,lk=0x104,roundhouse=0x105,sweep=0x106,
              uppercut=0x107,jumpkick=0x10e,jumppunch=0x118,duckpunch=0x119,
              duckhighkick=0x113,ducklowkick=0x11a,flyingkick=0x200,flyingpunch=0x201)

def cells(rows,actors=(17,18)):
    result=[]
    for name,action in EXPECTED.items():
        window=[r for r in rows if r['case']==name]
        for side,actor in enumerate(actors,1):
            active=[r for r in window if int(r[f'p{side}action'])==action]
            recovery=[r for r in window if int(r['age'])>=90 and int(r[f'p{side}action'])==0x303]
            result.append(dict(case=name,side=side,actor=actor,expectedAction=action,
                observedActionFields=len(active),observedDistinctShapes=len({r[f'p{side}shape'] for r in active}),
                lateStanceFields=len(recovery),actionAndLateRecoveryObserved=bool(active and recovery)))
    return result

def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest().upper()

def main(name):
    assert name and all(c.isalnum() or c in '_-' for c in name)
    run=BASE/name
    receipt=json.loads((run/'execution.json').read_text())
    assert '--normal-moves' in receipt['testArguments'] and '--game' in receipt['testArguments']
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['controllerSHA256']==sha(run/'autoboot.lua')
    observer=(run/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    log=(run/'mame.log').read_text()
    assert '[LUA ERROR]' not in log and 'Fatal error:' not in log
    with zipfile.ZipFile(run/'roms/mk3.zip') as archive:verify(archive,receipt)
    with (run/'normals.csv').open() as stream:rows=list(csv.DictReader(stream))
    assert rows and all(r['missing']=='0' for r in rows)
    actors=(18,17) if '--mirror' in receipt['testArguments'] else (17,18)
    assert all(r['p1selected']==r['p1char']==str(actors[0]) and r['p2selected']==r['p2char']==str(actors[1]) for r in rows)
    assert max(int(r['combat']) for r in rows)>=1800,'Controller did not finish all requests'
    results=cells(rows,actors)
    report=dict(scope='Finite standing/duck/jump action and late-stance observations, not damage/all-frame visual proof',
                cases=results,all28ActionRecoveryCellsObserved=all(r['actionAndLateRecoveryObserved'] for r in results),
                currentFull26ROMBytesVerified=True,fullPortVerified=False,
                pins={str(p):sha(p) for p in (run/'execution.json',run/'autoboot.lua',run/'normals.csv',Path(__file__))})
    (run/'NORMAL_MOVE_OBSERVATIONS.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Observed action/recovery cells:',sum(r['actionAndLateRecoveryObserved'] for r in results),'/28')
    for r in results:
        if not r['actionAndLateRecoveryObserved']:print('UNPROVEN',r)

if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
