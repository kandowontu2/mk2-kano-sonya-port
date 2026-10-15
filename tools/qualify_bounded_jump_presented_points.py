"""Require real presentation matches; keep any failing point unaccepted."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_idle_presented_points import check_point

def load(folder):
    rows={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line and '_FAILED ' not in line
        if line.startswith('MK2_HSPECIAL_'):
            rows.setdefault(line.split()[0][13:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return rows

out=sync.ROOT/'audit_bounded_jump_presented_points_checked';assert not out.exists()
results={}
observer=sync.ROOT/'audit_bounded_jump_presented_points_preparation/prepared_observer.lua'
assert 'screen:pixels()' not in observer.read_text()
for fighter,identity in [('kano',17),('sonya',18)]:
    folder=sync.ROOT/f'audit_bounded_{fighter}_jump_presented_points_runtime'
    base=sync.ROOT/f'audit_bounded_{fighter}_jump_shadow_points_runtime'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
    assert terminal['observerSha256']==sync.sha(observer)
    assert not (folder/'stderr.log').read_text().strip()
    rows=load(folder);old=load(base)
    for tag in ('FIELD','INPUT','READY','IDLE_TERMINAL'):assert rows[tag]==old[tag],tag
    fields=[r for r in rows['FIELD'] if r['slot']=='1']
    airborne={r['frame'] for r in fields if r['y']!=r['floor']}
    points=rows['IDLE_VRAM_POINT'];finals=rows['IDLE_ALL_DRAW_FINAL']
    assert len(points)==len(finals) and points
    bad=[]
    for r in points:
        try:check_point(r,identity)
        except AssertionError:bad.append(r)
    badfinal=[r for r in finals if r['match']!='1' or r['final']!=r['actual']]
    own=[r for r in points if r['slot']=='1'];air=[r for r in own if r['source_frame'] in airborne]
    assert air
    results[fighter]=dict(terminal=terminal,points=len(points),ownPoints=len(own),airbornePoints=len(air),
        unresolvedVRAMPoints=bad,unresolvedFinalDrawPoints=badfinal,
        logSHA256=sync.sha(folder/'run.log'),physicalGameplayUnchanged=True)
report=dict(observationVerified=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),
    priorCurrentDrawBitmapMismatchesDoNotEstablishPresentationDefect=True,
    finiteQueryPresentationProven=all(not v['unresolvedVRAMPoints'] and not v['unresolvedFinalDrawPoints'] for v in results.values()),
    entireShadowRasterProven=False,allSlotsAnimationsArenasProven=False,fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:dict(points=v['points'],airbornePoints=v['airbornePoints'],unresolvedVRAM=len(v['unresolvedVRAMPoints']),unresolvedFinal=len(v['unresolvedFinalDrawPoints'])) for k,v in results.items()}))
