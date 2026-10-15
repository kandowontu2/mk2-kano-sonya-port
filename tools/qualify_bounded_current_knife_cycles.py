"""Current private executable: two physical knife cycles and settled recovery."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
out=sync.ROOT/'audit_bounded_current_knife_cycles_checked';assert not out.exists()
results={}
for side in (1,2):
    folder=sync.ROOT/f'audit_bounded_current_special_cycles_knife_p{side}_runtime'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
    assert not (folder/'stderr.log').read_text().strip()
    rows={}
    for line in (folder/'run.log').read_text().splitlines():
        assert 'hex=' not in line and '[LUA ERROR]' not in line and '_FAILED ' not in line
        if line.startswith('MK2_HSPECIAL_'):
            rows.setdefault(line.split()[0][13:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    assert len(rows['COMMAND'])==len(rows['RECOVERED'])==2
    assert rows['RESULT'][0]['completed']=='2' and len(rows['FINAL'])==1
    events=[r for r in rows['EVENT'] if r['entry']=='FFFFB000']
    assert {r['attempt'] for r in events}=={'1','2'}
    assert all(r['id']=='17' and r['actor']==r['a8'] and r['main']==r['a13'] and r['pc']=='FFFFB010' for r in events)
    fields=rows['FIELD'];own=[r for r in fields if r['slot']==str(side)]
    assert own and all(r['id']==r['roster']=='17' and r['actor']==r['owner'] and r['hp']=='161' for r in own)
    damage=[r for r in rows['HEALTH'] if r['slot']==str(3-side) and int(r['after'])<int(r['before'])]
    assert len(damage)==2 and all(int(r['before'])-int(r['after'])==22 and r['pc']=='FF836700' for r in damage)
    last=own[-1];assert last['y']==last['floor'] and last['action']=='771'
    assert all(int(last[k],16)==0 for k in ('vx','vy','gravity','trail'))
    results[f'P{side}']=dict(terminal=terminal,physicalCommands=2,ownedNativeEntries=len(events),nativeDamagePerCycle=22,
        trueIdentityFields=len(own),settledIdle=True,logSHA256=sync.sha(folder/'run.log'))
report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),
    scope='Current private executable, Kano knife two physical cycles in each slot versus Kitana, collision damage and ordinary follow-up/idle. Not full eight-move matrix, art/audio/CPU/arena or full-port acceptance.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,contexts=2,cycles=4)))
