"""Finite grounded requests and observed native vertical kicks, not inferred wins."""
import csv
import json
import subprocess
import sys
from inspect_normal_runtime import BASE, PORT, sha
from refresh_special_videos import FLAGS


def valid_request(row):
    return (row['decision']=='upkick' and 0<=int(row['distance'])<=115 and
        row['ownAction']=='771' and int(row['ownFlags'])&0x1c==0 and
        row['ownHeight']=='0' and int(row['bodyHeight'])>=120 and
        row['buttonTable']==row['stanceTable'] and int(row['ownHP'])>0)


def main(name):
    assert name and all(c.isalnum() or c in '_-' for c in name)
    run=BASE/name
    receipt=json.loads((run/'execution.json').read_text())
    assert '--campaign-kano-kintaro-vertical-kick' in receipt['testArguments']
    subprocess.run([sys.executable,str(PORT/'audit_campaign_run.py'),name],check=True,
                   stdout=subprocess.DEVNULL,creationflags=FLAGS)
    source=(run/'autoboot.lua').read_text()
    branch=source.split("elseif plan=='upkick' then",1)[1].split("elseif plan=='mixkick'",1)[0]
    assert 'planAge>=28 and planAge<=31' in branch or 'planAge>=subBallRecovery.verticalAttackAge' in branch
    assert 'planToward' not in branch
    with (run/'kintaro_vertical.csv').open() as stream:
        requests=[r for r in csv.DictReader(stream) if r['decision']=='upkick']
    assert requests and all(valid_request(r) for r in requests)
    attack_age=10 if '--campaign-kano-kintaro-vertical-early' in receipt['testArguments'] else 28
    assert all(int(r.get('attackAge',28))==attack_age for r in requests)
    with (run/'campaign.csv').open() as stream:
        entries={int(r['frame']) for r in csv.DictReader(stream) if
            r['mode']=='2' and r['p1char']=='17' and r['p2char']=='12' and r['p1action']=='270'}
    observed=[]
    for number,row in enumerate(requests):
        frame=int(row['frame'])
        end=min(frame+attack_age+12,int(requests[number+1]['frame'])-1 if number+1<len(requests) else frame+attack_age+12)
        entry=next((f for f in range(frame+attack_age-4,end+1) if f in entries),None)
        observed.append(dict(requestFrame=frame,distance=int(row['distance']),nativeKickEntryFrame=entry))
    audit=json.loads((run/'CAMPAIGN_AUDIT.json').read_text())
    rounds=[r for r in audit['rounds'] if r['opponent']==12]
    wins=[r for r in audit['nativeWinningRounds'] if r['opponent']==12]
    report=dict(scope='Finite ready vertical-jump requests and sampled native010eh entries; no attributed hit claim',
        cases=observed,requests=len(requests),attackAge=attack_age,observedNativeEntries=sum(r['nativeKickEntryFrame'] is not None for r in observed),
        bossRounds=len(rounds),bestBossHP=min(r['minimumCPUHP'] for r in rounds),nativeBossRoundWins=wins,
        fullPortVerified=False,pins={str(p):sha(p) for p in
            (run/'execution.json',run/'autoboot.lua',run/'kintaro_vertical.csv',run/'campaign.csv')})
    (run/'KINTARO_VERTICAL_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Vertical requests',len(requests),'native entries',report['observedNativeEntries'],
          'best boss HP',report['bestBossHP'],'native round wins',len(wins))


if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
