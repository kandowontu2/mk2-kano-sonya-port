"""Finite native action and released-input recovery checks, not raster proof."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
out=sync.ROOT/'audit_bounded_current_basic_controls_checked'
assert not out.exists()
results={}
for move,identity in [('knife','17'),('ring','18')]:
    for side in (1,2):
        folder=sync.ROOT/f'audit_bounded_current_basic_controls_{move}_p{side}_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows={}
        for line in (folder/'run.log').read_text().splitlines():
            assert '[LUA ERROR]' not in line and 'hex=' not in line and '_FAILED ' not in line
            if line.startswith('MK2_HSPECIAL_'):
                rows.setdefault(line.split()[0][13:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        result=rows['RESULT'][0]
        assert result['completed']=='2'
        start=int(result['followup'])
        own=[r for r in rows['FIELD'] if r['slot']==str(side)]
        assert all(r['id']==r['roster']==identity and r['actor']==r['owner'] for r in own)
        for age,action in [(112,257),(176,258),(240,259),(304,260),(368,1792),(416,770),(424,1793)]:
            assert any(start+age<=int(r['frame'])<start+age+24 and int(r['action'])==action for r in own),(move,side,age,action)
        assert any(start+40<=int(r['frame'])<start+100 and int(r['y'])<int(r['floor']) for r in own)
        for slot in (1,2):
            final=[r for r in rows['FIELD'] if r['slot']==str(slot)][-1]
            assert final['y']==final['floor'] and final['action']=='771'
            assert all(int(final[k],16)==0 for k in ('vx','vy','gravity','trail'))
        assert int(rows['FINAL'][0]['frame'])==start+500
        results[f'{move}P{side}']=dict(terminal=terminal,logSHA256=sync.sha(folder/'run.log'),nativeNormalActions=[257,258,259,260,1792,770,1793],jumpObserved=True,bothActorsSettled=True)
report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),scope='Four physical slot cases after projectile recovery: normal HP/LP/HK/LK/block/crouch/crouch-block/jump and final idle. Not collision coverage for all normals, throws, crouching attacks, full raster/audio/all arenas/campaign or release acceptance.',fullGoalComplete=False)
out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,contexts=4,fullGoalComplete=False)))
