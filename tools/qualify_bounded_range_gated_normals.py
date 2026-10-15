"""Actual normal native damage, true identities and settled recovery."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
out=sync.ROOT/'audit_bounded_range_gated_normals_checked'
assert not out.exists()
results={}
for move,identity in [('knife','17'),('ring','18')]:
 for side in (1,2):
    folder=sync.ROOT/f'audit_bounded_range_gated_normals_{move}_p{side}_runtime'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
    assert not (folder/'stderr.log').read_text().strip()
    rows={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line and '_FAILED ' not in line and 'hex=' not in line
        if line.startswith('MK2_HSPECIAL_'):
            rows.setdefault(line.split()[0][13:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    commands=rows['NORMAL_COMMAND'];recoveries=rows['NORMAL_RECOVERED']
    assert len(commands)==len(recoveries)==4 and rows['RESULT'][0]['completed']=='2'
    own=[r for r in rows['FIELD'] if r['slot']==str(side)]
    assert all(r['id']==r['roster']==identity and r['actor']==r['owner'] for r in own)
    damage={}
    for index,(command,recovery,action) in enumerate(zip(commands,recoveries,[257,258,259,260]),1):
        assert command['index']==recovery['index']==str(index) and int(command['gap'])<=48
        begin=int(command['frame']);end=int(recovery['frame'])
        assert end>=begin+100
        assert any(begin<=int(r['frame'])<end and int(r['action'])==action for r in own)
        hits=[r for r in rows['HEALTH'] if r['slot']==str(3-side) and begin<=int(r['frame'])<end and int(r['after'])<int(r['before'])]
        assert hits and all(r['pc']=='FF836700' for r in hits),(move,side,index)
        damage[str(index)]=sum(int(r['before'])-int(r['after']) for r in hits)
    for slot in (1,2):
        final=[r for r in rows['FIELD'] if r['slot']==str(slot)][-1]
        assert final['y']==final['floor'] and final['action']=='771'
        assert all(int(final[k],16)==0 for k in ('vx','vy','gravity','trail'))
    results[f'{move}P{side}']=dict(terminal=terminal,damageHP_LP_HK_LK=damage,commands=commands,recoveries=recoveries,logSHA256=sync.sha(folder/'run.log'))
report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),scope='Four true-ID physical slot cases versus Kitana, four standing normals with actual collision/damage and both-actor recovery. Not crouching/air/throw/block-hit/all-victim/raster/audio or full release acceptance.',fullGoalComplete=False)
out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,contexts=4,normalContacts=16,fullGoalComplete=False)))
