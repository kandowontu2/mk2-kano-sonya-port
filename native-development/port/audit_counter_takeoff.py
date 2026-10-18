"""Distinguish requested buttons from observed native jumps; no win inference."""
import csv
import hashlib
import json
from pathlib import Path
import sys

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
for name in sys.argv[1:]:
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['gameMemoryWrites'] and not receipt['customDriver']
    assert hashlib.sha256((folder/'autoboot.lua').read_bytes()).hexdigest().upper()==receipt['controllerSHA256']
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    rows=list(csv.DictReader((folder/'campaign_counter.csv').open()))
    assert rows
    jumps=[row for row in rows if int(row['ownAction']) in (0x308,0x30b)]
    jump_starts=[row for previous,row in zip(rows,rows[1:])
                 if int(row['ownAction']) in (0x308,0x30b) and
                    (int(previous['ownAction']) not in (0x308,0x30b) or int(row['frame'])!=int(previous['frame'])+1)]
    kicks=[row for row in rows if row['hk']=='1']
    report=dict(run=name,scope='Physical counter-policy input/state diagnosis, not campaign acceptance',
        observations=len(rows),upFields=sum(row['up']=='1' for row in rows),
        requestedKickFields=len(kicks),nativeJumpFields=len(jumps),nativeJumpEpisodes=len(jump_starts),
        requestedKickFieldsDuringNativeJump=sum(int(row['ownAction']) in (0x308,0x30b) for row in kicks),
        nativeFlyingKickFields=sum(int(row['ownAction'])==0x200 for row in rows),
        heightRange=[min(int(row['ownHeight']) for row in rows),max(int(row['ownHeight']) for row in rows)],
        controllerSHA256=receipt['controllerSHA256'],fullCampaignVerified=False)
    report['evidenceSHA256']={path.name:hashlib.sha256(path.read_bytes()).hexdigest().upper()
        for path in (folder/'campaign_counter.csv',folder/'execution.json',Path(__file__))}
    (folder/'COUNTER_TAKEOFF_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
