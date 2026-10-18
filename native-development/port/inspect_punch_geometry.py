"""Read-only end-of-field collision geometry, not exact CPU strike-check timing."""
import csv
import json
from pathlib import Path
import zipfile
from inspect_normal_runtime import BASE,sha
from verify_finisher_roms import verify

def overlap(attacker,victim):
    x=int(attacker['x']);y=int(attacker['y'])
    left=x-80 if int(attacker['flags'])&16 else x+35
    width=int(victim['right'])-int(victim['left'])
    squeeze=(width>>2)+(width>>3)
    vl=int(victim['left'])+squeeze;vr=int(victim['right'])-squeeze
    return min(left+45,vr)-max(left,vl),min(y+38,int(victim['bottom']))-max(y+8,int(victim['top']))

def main():
    cases=[]
    for side in (1,2):
        run=BASE/f'stock_wolf_2219_hp_geometry_p{side}'
        receipt=json.loads((run/'execution.json').read_text())
        assert receipt['exitCode']==0 and not receipt['timedOut']
        assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
        assert receipt['controllerSHA256']==sha(run/'autoboot.lua')
        with zipfile.ZipFile(run/'roms/mk3.zip') as archive:verify(archive,receipt)
        with (run/'normal_geometry.csv').open() as stream:rows=list(csv.DictReader(stream))
        pairs={}
        for row in rows:pairs.setdefault(int(row['frame']),{})[int(row['side'])]=row
        observations=[]
        for frame,pair in pairs.items():
            a=pair[side];v=pair[3-side]
            if a['action']!='257':continue
            horizontal,vertical=overlap(a,v)
            observations.append(dict(frame=frame,combat=int(a['combat']),horizontal=horizontal,vertical=vertical))
        with (run/'normals.csv').open() as stream:normal=list(csv.DictReader(stream))
        damage=int(normal[0][f'p{3-side}hp'])-int(normal[-1][f'p{3-side}hp'])
        cases.append(dict(side=side,run=run.name,damage=damage,observations=observations,
            firstEndOfFieldOverlap=next((r['combat'] for r in observations if r['horizontal']>0 and r['vertical']>0),None),
            pins={str(p):sha(p) for p in (run/'execution.json',run/'autoboot.lua',run/'normal_geometry.csv',run/'normals.csv')}))
    report=dict(scope='End-of-field multipart geometry using JOY/MKUTIL formulas; CPU strike-check instants not observed',
                cases=cases,exactCauseVerified=False,facingDefectProven=False,fullPortVerified=False)
    path=Path(__file__).parent/'PUNCH_EDGE_GEOMETRY_2219.json'
    path.write_text(json.dumps(report,indent=2)+'\n')
    for case in cases:print(case['side'],'first overlap combat',case['firstEndOfFieldOverlap'],'damage',case['damage'])

if __name__=='__main__':main()
