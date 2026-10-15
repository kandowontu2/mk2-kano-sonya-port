"""True mirror actors, native grab entries/ticks and both actors' recovery."""
import copy,json,re
from pathlib import Path
import verify_native_source_sync as sync

def gate(rows,move,side):
    ident,entry,latency=('17','FFF91400',8) if move=='choke' else ('18','FFF80800',5)
    fields=rows['FIELD'];assert fields
    assert all(r['id']==r['roster']==ident and r['actor']==r['owner'] for r in fields)
    assert len(rows['COMMAND'])==len(rows['RECOVERED'])==2 and rows['RESULT'][0]['completed']=='2'
    entries=[r for r in rows['EVENT'] if r['entry']==entry];assert len(entries)==2
    for cmd,event,recover in zip(rows['COMMAND'],entries,rows['RECOVERED']):
        assert event['actor']==event['a8'] and event['main']==event['a13'] and event['id']==ident
        assert int(event['frame'])-int(cmd['frame'])==latency
        hits=[r for r in rows['HEALTH'] if int(event['frame'])<=int(r['frame'])<=int(recover['frame']) and int(r['after'])<int(r['before'])]
        assert all(r['slot']==str(3-side) and r['pc']=='FF836700' for r in hits)
        assert [int(r['before'])-int(r['after']) for r in hits]==([8]*4 if move=='choke' else [35])
        for slot in ('1','2'):
            settled=next(r for r in fields if r['slot']==slot and r['frame']==recover['frame'])
            assert settled['y']==settled['floor'] and settled['action']=='771'
    for slot in ('1','2'):
        last=[r for r in fields if r['slot']==slot][-1]
        assert last['action']=='771' and last['y']==last['floor']
        assert all(int(last[k],16)==0 for k in ('vx','vy','gravity','trail'))
    return dict(twoMirrorActivations=True,trueMirrorFields=len(fields),bothRecoveredEachCycle=True)

out=sync.ROOT/'audit_bounded_current_mirror_grabs_checked';assert not out.exists();results={}
for move in ('choke','leg'):
    for side in (1,2):
        folder=sync.ROOT/f'audit_bounded_current_mirror_grab_{move}_p{side}_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
        assert not (folder/'stderr.log').read_text().strip()
        rows={}
        for line in (folder/'run.log').read_text().splitlines():
            assert 'hex=' not in line and '[LUA ERROR]' not in line and '_FAILED ' not in line
            if line.startswith('MK2_HSPECIAL_'):rows.setdefault(line.split()[0][13:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        result=gate(rows,move,side);faults=[]
        for key,value in [('id','1'),('owner','00000000')]:
            bad=copy.deepcopy(rows);bad['FIELD'][0][key]=value
            try:gate(bad,move,side)
            except AssertionError:faults.append(key)
            else:raise AssertionError('Fault accepted')
        results[f'{move}P{side}']=dict(result=result,terminal=terminal,rejectedFaults=faults,logSHA256=sync.sha(folder/'run.log'))
report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),
    scope='Four current physical mirror grab contexts, two cycles each, true identities on both sides and native collision/recovery. Not complete mirrors, graphics/audio/victim finishers/CPU/campaign or whole port.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,contexts=4,cycles=8)))
