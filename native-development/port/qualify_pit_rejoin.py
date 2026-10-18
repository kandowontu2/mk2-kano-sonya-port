"""Actual post-Pit rejoin and cleared drawing shapes, not allocator/audio proof."""
import csv
import json
from pathlib import Path
import runpy
import sys

HERE=Path(__file__).resolve().parent
# Re-run the unchanged cinematic scope on the same ROM/controller evidence.
core=runpy.run_path(str(HERE/'qualify_pit_runtime.py'),run_name='__main__')
run=core['run'];sha=core['sha'];actor=core['actor'];victim=core['victim']
side=core['side'];other=3-side
assert '--pit-rejoin' in core['args']
rows=list(csv.DictReader((run/'pit_retention.csv').open()))
assert rows and all(r['missing']=='0' for r in rows)
assert [int(r['frame']) for r in rows]==list(range(int(rows[0]['frame']),int(rows[-1]['frame'])+1))
objects=list(csv.DictReader((run/'pit_objects.csv').open()))
last_body=int(objects[-1]['frame'])
after=[r for r in rows if int(r['frame'])>last_body]
assert after and all(r['pitObjects']=='0' for r in after)
assert int(after[0]['frame'])==last_body+1
fresh=[r for r in after if r['mode']=='2' and r['background']=='7' and r[f'p{side}char']==str(actor)
       and r[f'p{other}char']==str(victim) and int(r['p1hp'])>0 and int(r['p2hp'])>0 and r['death']=='0']
assert fresh and fresh[0]['p1hp']==fresh[0]['p2hp']=='161'
first=int(fresh[0]['frame']);last=int(rows[-1]['frame'])
assert last==first+600
window=[r for r in rows if int(r['frame'])>=first]
assert len(window)==601 and all(r['pitObjects']=='0' for r in window)
assert any(int(r[f'p{other}hp'])<161 for r in fresh),'Real controller-driven combat did not resume'
assert len(fresh)>=300
captures=sorted((run/'snap').glob('after_pit_*.png'));assert captures
report=dict(scope='actual physical rejoin after native Pit; cleared own Pit drawing shapes through next match',
            actorID=actor,physicalActorSide=side,victimID=victim,lastPitShapeFrame=last_body,firstClearedFrame=int(after[0]['frame']),
            nextMatchFrame=first,checkedThroughFrame=last,nextMatchObservedFields=601,
            activeCombatObservations=len(fresh),freshMatchStartedWithFullHealth=True,
            actualCombatDamageObserved=True,noRetainedPitDrawingShapes=True,missingRootMarkers=0,
            allocatorPaletteAndProcessLifetimeQualified=False,mirroredRoleCase=side==2,
            fullSinglePlayerCampaignQualified=False,fullPortVerified=False,releaseReady=False)
paths=[run/'qualification.json',run/'pit_retention.csv',run/'pit_objects.csv',run/'execution.json',
       run/'autoboot.lua',HERE/'qualify_pit_runtime.py',Path(__file__)]+captures
report['pins']={str(p):sha(p) for p in paths}
(run/'cleanup_qualification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='pins'},indent=2))
