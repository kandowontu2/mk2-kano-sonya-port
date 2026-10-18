"""Finite logged escape-input evidence; intervals are not claimed complete phases."""
import csv
import json
import subprocess
import sys
from inspect_normal_runtime import BASE, PORT, sha
from refresh_special_videos import FLAGS


def escape_intervals(rows):
    groups=[]
    previous=None
    for row in rows:
        frame=int(row['frame'])
        assert previous is None or frame>previous
        if previous is None or frame!=previous+1:groups.append([])
        groups[-1].append(row)
        previous=frame
    result=[]
    for group in groups:
        up=next((r for r in group if r['up']=='1'),None)
        result.append(dict(firstFrame=int(group[0]['frame']),lastFrame=int(group[-1]['frame']),
            fields=len(group),firstHeight=int(group[0]['ownHeight']),
            firstUpFrame=int(up['frame']) if up else None,
            oldAirThenGroundedUp=bool(int(group[0]['ownHeight'])>0 and up and
                int(up['frame'])>int(group[0]['frame']) and up['ownHeight']=='0'),
            observedAirAfterUp=bool(up and any(int(r['frame'])>int(up['frame']) and
                int(r['ownHeight'])>0 for r in group))))
    return result


def main(name):
    assert name and all(c.isalnum() or c in '_-' for c in name)
    run=BASE/name
    receipt=json.loads((run/'execution.json').read_text())
    assert '--campaign-kano-kintaro-stomp-refresh' in receipt['testArguments']
    subprocess.run([sys.executable,str(PORT/'audit_campaign_run.py'),name],check=True,
                   stdout=subprocess.DEVNULL,creationflags=FLAGS)
    with (run/'stomp_escape.csv').open() as stream: intervals=escape_intervals(csv.DictReader(stream))
    refreshed=[r for r in intervals if r['oldAirThenGroundedUp']]
    assert refreshed, 'No old-air/ground/new-Up case observed; refresh remains unproved'
    with (run/'campaign.csv').open() as stream: rows=list(csv.DictReader(stream))
    damage=[]
    for before,after in zip(rows,rows[1:]):
        if not (before['mode']==after['mode']=='2' and before['p2char']==after['p2char']=='12' and
                (before['attempt'],before['round'])==(after['attempt'],after['round'])):continue
        delta=int(before['p1hp'])-int(after['p1hp'])
        if delta>0 and before['p2action']=='1031':
            damage.append(dict(frame=int(after['frame']),HPDrop=delta))
    audit=json.loads((run/'CAMPAIGN_AUDIT.json').read_text())
    report=dict(scope='Contiguous logged escape intervals and pre-drop action tags, not causal attack attribution',
        intervals=intervals,oldAirThenGroundedUpCases=refreshed,
        preDropStompTagDamageWindows=damage,
        nativeBossRoundWins=[r for r in audit['nativeWinningRounds'] if r['opponent'] in (12,13)],
        fullPortVerified=False,pins={str(p):sha(p) for p in
            (run/'execution.json',run/'autoboot.lua',run/'stomp_escape.csv',run/'campaign.csv')})
    (run/'STOMP_REFRESH_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Old-air/new-Up cases',len(refreshed),'followed by observed air',sum(r['observedAirAfterUp'] for r in refreshed),
          'pre-drop stomp-tag windows',len(damage),'native boss round wins',len(report['nativeBossRoundWins']))


if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
