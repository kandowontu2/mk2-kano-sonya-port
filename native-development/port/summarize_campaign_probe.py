"""Describe campaign attempts without converting a clean exit into a win."""
import csv
import json
from pathlib import Path
import sys

BASE=Path(__file__).resolve().parent.parent/'baseline'
for argument in sys.argv[1:]:
    folder=BASE/argument
    rows=list(csv.DictReader((folder/'campaign.csv').open()))
    execution=json.loads((folder/'execution.json').read_text())
    combat=[r for r in rows if r['mode']=='2']
    assert combat, 'No live combat observed'
    target=18 if '--sonya' in execution['testArguments'] else 17
    own=[r for r in combat if int(r['p1char'])==target]
    assert own, 'Requested identity never entered combat'
    result={'actor':'sonya' if target==18 else 'kano','recordedLastFrame':int(rows[-1]['frame']),
            'requestedIdentityEnteredCombat':True,'observedOpponents':sorted({int(r['p2char']) for r in own}),
            'observedLadderPositions':sorted({int(r['map']) for r in own}),
            'actorReachedZeroHealth':any(int(r['p1hp'])==0 for r in own),
            'opponentReachedZeroHealth':any(int(r['p2hp'])==0 for r in own),
            'missingMarkers':max(int(r['missing']) for r in rows),
            'exitCode':execution['exitCode'],'timedOut':execution['timedOut'],
            'campaignCompletionProven':False,'fullPortVerified':False,
            'scope':'Exploratory controller attempt, not campaign acceptance; subsequent attract-mode fights excluded'}
    (folder/'campaign_observation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
