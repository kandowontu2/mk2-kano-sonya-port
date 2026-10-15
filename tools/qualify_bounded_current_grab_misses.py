"""Far grab whiffs must leave both identities/health/control intact."""
import copy,json,re
from pathlib import Path
import verify_native_source_sync as sync

def gate(rows,move,side):
    ident,entry,latency=('17','FFF91400',8) if move=='choke' else ('18','FFF80800',5)
    assert len(rows['COMMAND'])==len(rows['RECOVERED'])==len(rows['FINAL'])==1
    command=rows['COMMAND'][0];base=int(command['frame']);assert int(command['gap'])>=150
    entries=[r for r in rows['EVENT'] if r['entry']==entry];assert len(entries)==1
    event=entries[0];assert event['id']==ident and event['actor']==event['a8'] and event['main']==event['a13']
    assert int(event['frame'])-base==latency
    assert not rows.get('HEALTH',[])
    fields=rows['FIELD'];assert fields and all(r['hp']=='161' and r['actor']==r['owner'] for r in fields)
    own=[r for r in fields if r['slot']==str(side)]
    assert all(r['id']==r['roster']==ident for r in own)
    recovery=int(rows['RECOVERED'][0]['frame']);assert recovery>=base+221
    followup=int(rows['RESULT'][0]['followup']);assert followup==recovery+16
    assert any(r['y']!=r['floor'] and int(r['frame'])>=followup+40 for r in own)
    assert any(r['action']=='257' and int(r['frame'])>=followup+112 for r in own)
    assert len({r['x'] for r in own if followup<=int(r['frame'])<followup+30})>1
    for slot in ('1','2'):
        last=[r for r in fields if r['slot']==slot][-1]
        assert last['y']==last['floor'] and last['action']=='771'
        assert all(int(last[k],16)==0 for k in ('vx','vy','gravity','trail'))
    return dict(gap=int(command['gap']),nativeEntry=int(event['frame']),noContactDamage=True,ordinaryWalkJumpPunch=True,cleanFinalBothActors=True)

out=sync.ROOT/'audit_bounded_current_grab_misses_checked';assert not out.exists();results={}
for move in ('choke','leg'):
    for side in (1,2):
        folder=sync.ROOT/f'audit_bounded_current_grab_miss_{move}_p{side}_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
        assert not (folder/'stderr.log').read_text().strip()
        rows={}
        for line in (folder/'run.log').read_text().splitlines():
            assert 'hex=' not in line and '[LUA ERROR]' not in line and '_FAILED ' not in line
            if line.startswith('MK2_HSPECIAL_'):
                rows.setdefault(line.split()[0][13:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        result=gate(rows,move,side);faults=[]
        for tag,key,value in [('FIELD','hp','0'),('FIELD','owner','00000000'),('COMMAND','gap','1')]:
            bad=copy.deepcopy(rows);bad[tag][0][key]=value
            try:gate(bad,move,side)
            except AssertionError:faults.append(tag+'.'+key)
            else:raise AssertionError('Fault accepted')
        results[f'{move}P{side}']=dict(result=result,terminal=terminal,rejectedFaults=faults,logSHA256=sync.sha(folder/'run.log'))
report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),
    scope='Four current-build physical far choke/leg whiffs versus Kitana, followed by actual ordinary walk/jump/punch and both-actor idle. Not universal miss/CPU/arena/art/audio/campaign acceptance.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,contexts=4)))
