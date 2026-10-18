"""Bounded sampled paired move against a genuine campaign CPU opponent."""
import csv
import hashlib
import json
from pathlib import Path
import sys

BASE=Path(__file__).resolve().parent.parent/'baseline'
for name in sys.argv[1:]:
    run=BASE/name
    audit=json.loads((run/'CAMPAIGN_AUDIT.json').read_text())
    assert audit['actor']==18 and audit['currentFullROMVerified']
    assert audit['missingMarkers']==0 and not audit['illegalOpcodeRecoveryObserved']
    rows=list(csv.DictReader((run/'campaign.csv').open()))
    fight=[row for row in rows if row['mode']=='2' and row['p2char']=='9']
    paired=[row for row in fight if row['p1action']=='538']
    assert len(paired)==23
    first,last=int(paired[0]['frame']),int(paired[-1]['frame'])
    assert [int(row['frame']) for row in paired]==list(range(first,last+1,2))
    assert all(row['p2action']=='539' and row['p1char']=='18' for row in paired)
    assert len({row['p1hp'] for row in paired})==1
    drops=[(int(row['frame']),int(previous['p2hp'])-int(row['p2hp']))
           for previous,row in zip(fight,fight[1:])
           if first<=int(row['frame'])<=first+50 and int(row['p2hp'])<int(previous['p2hp'])]
    assert len(drops)==1 and drops[0][1]==35
    assert first+46<=drops[0][0]<=first+48
    assert any(row['p1action']=='771' and drops[0][0]<int(row['frame'])<first+200 for row in fight)
    report=dict(scope='One sampled Sonya leg catch against campaign CPU Reptile',
        run=name,pairedSamples=23,sampleIntervalFields=2,firstPairedFrame=first,
        victimActionMatched=True,playerHealthStableDuringHold=True,releaseDamage=35,
        playerReturnedToStance=True,fullCampaignVerified=False,allCPUInteractionsVerified=False,
        traceSHA256=hashlib.sha256((run/'campaign.csv').read_bytes()).hexdigest().upper())
    (run/'CPU_LEG_SAMPLE.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
