"""Bind passive instruction-read observations to actual native punch outcomes."""
import csv
import json
from pathlib import Path
import zipfile
from inspect_normal_runtime import BASE,sha
from inspect_punch_geometry import overlap
from verify_finisher_roms import verify

def main():
    cases=[]
    for side in (1,2):
        run=BASE/f'stock_wolf_2219_hp_strike_entry2_p{side}'
        old=BASE/f'stock_wolf_2219_hp_geometry_p{side}'
        receipt=json.loads((run/'execution.json').read_text())
        assert receipt['exitCode']==0 and not receipt['timedOut']
        assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
        assert receipt['controllerSHA256']==sha(run/'autoboot.lua')
        log=(run/'mame.log').read_text()
        assert 'Fatal error:' not in log and '[LUA ERROR]' not in log
        with zipfile.ZipFile(run/'roms/mk3.zip') as archive:verify(archive,receipt)
        assert (run/'normals.csv').read_bytes()==(old/'normals.csv').read_bytes(),'Tap changed normal trace'
        with (run/'normal_strike_entries.csv').open() as stream:entries=list(csv.DictReader(stream))
        assert len(entries)==6
        assert all(r['actor']=='17' and r['action']=='257' and int(r['side'])==side and
                   (r['xoffset'],r['yoffset'],r['width'],r['height'])==('80','8','45','30') for r in entries)
        observations=[dict(frame=int(r['frame']),horizontal=overlap(r,r)[0],vertical=overlap(r,r)[1]) for r in entries]
        with (run/'normals.csv').open() as stream:rows=list(csv.DictReader(stream))
        damage=int(rows[0][f'p{3-side}hp'])-int(rows[-1][f'p{3-side}hp'])
        positive=sum(r['horizontal']>0 and r['vertical']>0 for r in observations)
        assert (positive,damage)==((1,11) if side==1 else (0,0))
        cases.append(dict(side=side,entries=observations,positiveOverlapChecks=positive,damage=damage,
            identicalNormalTraceWithoutTap=True,pins={str(p):sha(p) for p in
                (run/'execution.json',run/'autoboot.lua',run/'normals.csv',run/'normal_strike_entries.csv')}))
    report=dict(scope='Two edge-spacing punch outcomes explained by actual strike-entry victim geometry',
                cases=cases,noOverlapInMissedPunchChecks=True,nativeHitboxChangeNeededForTheseCases=False,
                allFacingAndReachCasesVerified=False,fullPortVerified=False)
    (Path(__file__).parent/'PUNCH_STRIKE_ENTRY_2219.json').write_text(json.dumps(report,indent=2)+'\n')
    for case in cases:print(case['side'],'checks',len(case['entries']),'positive',case['positiveOverlapChecks'],'damage',case['damage'])

if __name__=='__main__':main()
