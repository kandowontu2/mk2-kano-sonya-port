"""Read-only combo-queue evidence; distinguish matching inputs from activation."""
import csv
import hashlib
import json
from pathlib import Path
import sys

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest().upper()
for name in sys.argv[1:]:
    run=BASE/name
    receipt=json.loads((run/'execution.json').read_text())
    audit=json.loads((run/'CAMPAIGN_AUDIT.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['gameMemoryWrites'] and not receipt['customDriver']
    assert audit['currentFullROMVerified'] and not audit['illegalOpcodeRecoveryObserved']
    assert sha(run/'autoboot.lua')==receipt['controllerSHA256']
    queue=list(csv.DictReader((run/'damage_queue.csv').open()))
    counter={int(row['frame']):row for row in csv.DictReader((run/'campaign_counter.csv').open())}
    assert queue and all(int(after['frame'])==int(before['frame'])+1 for before,after in zip(queue,queue[1:]))
    evidence=[]
    for row in queue:
        frame=int(row['frame']);state=counter.get(frame)
        if not state or state['hk']!='1':continue
        # Left/right command rows are native sw_down=6, sw_left=7, sw_right=8.
        # The observed interval has the opponent to Sonya's right; verify this
        # from the independent main trace rather than selection-grid order.
        main=next(item for item in csv.DictReader((run/'campaign.csv').open()) if int(item['frame'])>=frame)
        back=7 if int(main['p1x'])<int(main['p2x']) else 8
        actual=[int(row[f'sw{i}']) for i in (1,2,3)]
        expected=[6,back,back]
        elapsed=(int(row['tick'])-int(row['time3']))&65535
        evidence.append(dict(frame=frame,queue=actual,expected=expected,
            patternMatches=actual==expected,oldestAgeTicks=elapsed,within36Ticks=elapsed<=36,
            observedAction=int(state['ownAction']),
            bicycleObservedWithin6Fields=any(int(counter.get(f,{}).get('ownAction',-1))==0x204 for f in range(frame,frame+7))))
    report=dict(scope='Recorded queue at HK input fields, not an entire campaign acceptance gate',
        run=name,events=evidence,anyMatchedPattern=any(row['patternMatches'] for row in evidence),
        anyObservedBicycle=any(int(row['ownAction'])==0x204 for row in counter.values()),
        fullCampaignVerified=False,releaseReady=False)
    report['evidenceSHA256']={path.name:sha(path) for path in
        (run/'damage_queue.csv',run/'campaign_counter.csv',run/'campaign.csv',run/'execution.json',run/'autoboot.lua',Path(__file__))}
    (run/'BIKE_QUEUE_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
