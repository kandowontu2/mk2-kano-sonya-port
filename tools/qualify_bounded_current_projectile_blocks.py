"""Physical Block, native block action and chip collisions; reject altered facts."""
import copy,json,re
from pathlib import Path
import verify_native_source_sync as sync

def gate(rows,move,side):
    identity,entry=('17','FFFFB000') if move=='knife' else ('18','FFFFB400')
    assert len(rows['COMMAND'])==len(rows['RECOVERED'])==len(rows['FINAL'])==1
    command=int(rows['COMMAND'][0]['frame'])
    events=[r for r in rows['EVENT'] if r['entry']==entry]
    assert len(events)==1
    event=events[0]
    assert event['id']==identity and event['actor']==event['a8'] and event['main']==event['a13']
    assert int(event['frame'])-command==8
    hits=[r for r in rows['HEALTH'] if int(r['after'])<int(r['before'])]
    assert len(hits)==1
    hit=hits[0];at=int(hit['frame'])
    assert hit['slot']==str(3-side) and int(hit['before'])-int(hit['after'])==6 and hit['pc']=='FF836700'
    defense=[r for r in rows['INPUT'] if r['slot']==str(3-side) and r['button']=='Block' and command<=int(r['frame'])<command+220]
    assert [int(r['frame']) for r in defense]==list(range(command,command+220))
    assert any(r['slot']==str(3-side) and r['action']=='1792' and int(r['frame'])==at for r in rows['FIELD'])
    assert rows['DEFENSE_RELEASED'][0]['frame']==str(command+220)
    own=[r for r in rows['FIELD'] if r['slot']==str(side)]
    assert all(r['id']==r['roster']==identity and r['actor']==r['owner'] and r['hp']=='161' for r in own)
    assert int(rows['RECOVERED'][0]['frame'])>=command+221
    for slot in ('1','2'):
        last=[r for r in rows['FIELD'] if r['slot']==slot][-1]
        assert last['y']==last['floor'] and last['action']=='771'
        assert all(int(last[k],16)==0 for k in ('vx','vy','gravity','trail'))
    return dict(nativeBlockCollisionFrame=at,chipDamage=6,ownedFields=len(own),cleanRecovery=True)

out=sync.ROOT/'audit_bounded_current_projectile_blocks_checked';assert not out.exists();results={}
observer=sync.ROOT/'audit_bounded_current_projectile_blocks_preparation/blocks.lua'
for move in ('knife','ring'):
    for side in (1,2):
        folder=sync.ROOT/f'audit_bounded_current_projectile_block_{move}_p{side}_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
        assert terminal['observerSha256']==sync.sha(observer) and not (folder/'stderr.log').read_text().strip()
        rows={}
        for line in (folder/'run.log').read_text().splitlines():
            assert '[LUA ERROR]' not in line and '_FAILED ' not in line and 'hex=' not in line
            if line.startswith('MK2_HSPECIAL_'):
                rows.setdefault(line.split()[0][13:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        result=gate(rows,move,side);faults=[]
        for tag,key,value in [('HEALTH','after','0'),('EVENT','a8','00000000'),('DEFENSE_RELEASED','frame','1')]:
            bad=copy.deepcopy(rows);bad[tag][0][key]=value
            try:gate(bad,move,side)
            except AssertionError:faults.append(tag+'.'+key)
            else:raise AssertionError('Fault not rejected')
        results[f'{move}P{side}']=dict(result=result,terminal=terminal,rejectedFaults=faults,logSHA256=sync.sha(folder/'run.log'))
report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),
    scope='Current private build physical knife/ring block, both slots against Kitana. Native block action, six chip damage and released-defense recovery. Not other blocked specials, all opponents/arenas, raster/audio/CPU/campaign or whole port.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,contexts=4,chipDamage=6)))
