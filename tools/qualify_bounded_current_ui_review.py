"""Fresh four-slot identity/navigation smoke check with bounded visual receipts.

Screenshots support human review; this gate does not prove blink/animation cadence.
"""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

out=sync.ROOT/'audit_bounded_current_ui_review_checked';assert not out.exists()
results={}
for fighter,identity,neighbor in (('kano','17','1'),('sonya','18','9')):
    for side in (1,2):
        folder=sync.ROOT/f'audit_bounded_current_ui_select_{fighter}_p{side}_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        log=(folder/'run.log').read_text();assert '[LUA ERROR]' not in log
        rows={}
        for line in log.splitlines():
            if line.startswith('MK2_UI_'):
                tag=line.split()[0][7:];rows.setdefault(tag,[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        assert len(rows['RESULT'])==len(rows['LIVE'])==len(rows['EXIT'])==1
        result=rows['RESULT'][0];assert 0<int(result['css'])<int(result['exit'])<int(result['live'])
        fields=rows['FIELD'];assert len(fields)==362
        own=[r for r in fields if int(r['slot'])==side]
        assert len(own)==181 and all(r['roster']==r['id']==identity and r['actor']==r['owner'] and r['state']=='1' for r in own)
        snaps=rows['SNAP'];assert len(snaps)==8
        select=[r for r in snaps if r['scene']=='select']
        assert [r['roster'] for r in select]==[identity,neighbor,identity,identity,identity]
        assert any(r['id']==identity for r in rows['LADDER'])
        assert all(r['css']=='0' for r in rows['OUTSIDE'])
        images={r['file']:sync.sha(folder/'snap'/r['file']) for r in snaps}
        results[f'{fighter}P{side}']=dict(terminal=terminal,firstMatchTrueIdentityFields=len(own),nativeLadderLookup=True,neighborAndReturnSelection=True,imageSHA256=images,logSHA256=sync.sha(folder/'run.log'))
report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),visualReview='Reviewed dedicated top-row selected portraits, P1/P2 numerals and borders, own ladder portraits without CSS poses, Sonya P1 and Kano P2 first match screenshots.',notProven=['Continuous blinking and animation cadence','Every transition field pixel teardown','Exact background/border pixel parity','All arenas/full integration/final release'],fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,contexts=4,firstMatchIdentityFields=724)))
