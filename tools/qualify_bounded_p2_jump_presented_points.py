"""Verify physical P2 jumps and actual VRAM/presentation; retain predictions."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def load(folder):
    rows={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line and '_FAILED ' not in line
        if line.startswith('MK2_HSPECIAL_'):
            rows.setdefault(line.split()[0][13:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return rows

out=sync.ROOT/'audit_bounded_p2_jump_presented_points_checked';assert not out.exists()
observer=sync.ROOT/'audit_bounded_p2_jump_presented_points_preparation/prepared_observer.lua'
results={}
for fighter,identity in [('kano','17'),('sonya','18')]:
    folder=sync.ROOT/f'audit_bounded_{fighter}_p2_jump_presented_points_runtime'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
    assert terminal['observerSha256']==sync.sha(observer) and terminal['peakWorkingSetBytes']<320*1024**2
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.bin','.png','.wav') for p in folder.rglob('*') if p.is_file())
    rows=load(folder);ready=int(rows['READY'][0]['frame'])
    fields=[r for r in rows['FIELD'] if r['slot']=='2']
    assert len(fields)==240 and all(r['id']==r['roster']==identity and r['actor']==r['owner'] and r['writes']=='0' for r in fields)
    inputs=[(int(r['frame'])-ready,r['slot'],r['button']) for r in rows['INPUT'] if int(r['frame'])>=ready]
    expected=[]
    for start,direction in [(16,None),(96,'Right'),(176,'Left')]:
        for age in range(start,start+4):
            expected.append((age,'2','Up'))
            if direction:expected.append((age,'2',direction))
    assert inputs==expected
    airborne={r['frame'] for r in fields if r['y']!=r['floor']};assert airborne
    assert fields[-1]['y']==fields[-1]['floor'] and fields[-1]['action']=='771'
    points=rows['IDLE_VRAM_POINT'];own=[r for r in points if r['slot']=='2']
    assert own
    for r in points:
        assert r['id']==({'1':'4','2':identity}[r['slot']])
        assert int(r['frame'])==int(r['source_frame'])+1
        assert r['source_vram']==r['display_vram'] and r['vram_rgb']==r['actual'] and r['display_matches']=='1'
    airpoints=[r for r in own if r['source_frame'] in airborne];assert airpoints
    assert any(r['source_vram']=='15' and r['actual']=='000000' for r in airpoints)
    prediction=[r for r in points if r['source_matches']!='1' or r['predicted']!=r['source_vram']]
    results[fighter]=dict(terminal=terminal,ownedActorFields=len(fields),airborneFields=len(airborne),
        physicalInputRequests=len(inputs),presentationQueryPoints=len(points),ownedAirbornePoints=len(airpoints),
        blackAirbornePoints=sum(r['source_vram']=='15' and r['actual']=='000000' for r in airpoints),
        actualPresentationMatchesVRAM=True,landedIdle=True,predictionDiscrepancies=prediction,logSHA256=sync.sha(folder/'run.log'))
report=dict(passedFinitePhysicalPresentation=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),
    scope='P2 neutral/right/left physical jumps against idle P1 Kitana. Sparse source-frame VRAM/displayed RGB matches and black airborne shadow presence. Predictions retained independently. Not entire shadow raster or all arenas.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:dict(airborneFields=v['airborneFields'],blackAirbornePoints=v['blackAirbornePoints'],predictionDiscrepancies=len(v['predictionDiscrepancies'])) for k,v in results.items()}))
