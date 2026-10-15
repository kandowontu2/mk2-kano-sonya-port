"""Retain exact displayed shadow matches and mismatches during physical jumps."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
out=sync.ROOT/'audit_bounded_jump_shadow_observed';assert not out.exists()
results={}
for fighter,identity in [('kano','17'),('sonya','18')]:
    folder=sync.ROOT/f'audit_bounded_{fighter}_jump_shadow_points_runtime'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
    assert not (folder/'stderr.log').read_text().strip()
    groups={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line and '_FAILED ' not in line
        if line.startswith('MK2_HSPECIAL_'):
            groups.setdefault(line.split()[0][13:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    fields=[r for r in groups['FIELD'] if r['slot']=='1']
    assert len(fields)==240 and all(r['id']==r['roster']==identity and r['actor']==r['owner'] for r in fields)
    ready=int(groups['READY'][0]['frame'])
    actual=[(int(r['frame'])-ready,r['button']) for r in groups['INPUT'] if int(r['frame'])>=ready]
    expected=[]
    for start,direction in [(16,None),(96,'Right'),(176,'Left')]:
        for age in range(start,start+4):
            expected.append((age,'Up'))
            if direction:expected.append((age,direction))
    assert actual==expected
    airborne={int(r['frame']) for r in fields if r['y']!=r['floor']}
    assert airborne
    rows=[r for r in groups['IDLE_SHADOW_DMA'] if r['slot']=='1']
    assert rows and all(r['id']==identity and r['owner']==r['actor'] and r['height']=='1' and int(r['command'],16)&15==8 for r in rows)
    points=[r for r in groups['IDLE_SCANPOINT'] if r['kind']=='shadow' and r['slot']=='1']
    assert points
    for r in points:
        assert r['id']==identity and r['expected']=='000000' and r['palette_index']=='15'
        assert int(r['frame'])==int(r['source_frame'])+1
        assert int(r['match'])==int(r['actual']==r['expected'])
    airpoints=[r for r in points if int(r['source_frame']) in airborne]
    assert airpoints and any(r['match']=='1' for r in airpoints)
    last=fields[-1];assert last['y']==last['floor'] and last['action']=='771'
    results[fighter]=dict(terminal=terminal,physicalInputRequests=len(actual),airborneFields=len(airborne),
        shadowRows=len(rows),sampledPoints=len(points),exactBlackPoints=sum(r['match']=='1' for r in points),
        airbornePoints=len(airpoints),airborneBlackPoints=sum(r['match']=='1' for r in airpoints),
        unresolvedPoints=[r for r in points if r['match']!='1'],landedIdle=True,logSHA256=sync.sha(folder/'run.log'))
report=dict(observationVerified=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),
    scope='Physical neutral/forward/backward jumps in P1 against idle P2 Kitana; sparse displayed native shadow points. Mismatches retained, not automatically waived as occlusion. Not whole raster, both slots, every animation or every arena acceptance.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:{a:b for a,b in v.items() if a in ('airborneFields','airborneBlackPoints','landedIdle')} for k,v in results.items()}))
