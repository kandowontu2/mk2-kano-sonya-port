"""Readonly sampled incoming-hit contexts; action adjacency is not causation."""
import collections
import csv
import json
from pathlib import Path
import sys

BASE=Path(__file__).resolve().parent.parent/'baseline'
for name in sys.argv[1:]:
    folder=BASE/name
    audit=json.loads((folder/'CAMPAIGN_AUDIT.json').read_text())
    assert audit['currentFullROMVerified']
    rows=list(csv.DictReader((folder/'campaign.csv').open()))
    contexts=collections.Counter();examples=[];previous=None
    for row in rows:
        if row['mode']!='2' or row['p2char']!='9':
            previous=None;continue
        if previous and row['round']==previous['round'] and int(row['p1hp'])<int(previous['p1hp']):
            distance=abs(int(previous['p1x'])-int(previous['p2x']))
            key=f"{int(previous['p1action']):04x}/{int(previous['p2action']):04x}"
            contexts[key]+=1
            examples.append(dict(frame=int(row['frame']),damage=int(previous['p1hp'])-int(row['p1hp']),
                                 precedingActions=key,distance=distance))
        previous=row
    print(json.dumps(dict(run=name,sampledIncomingHits=dict(contexts),examples=examples)))
