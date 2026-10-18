"""Prove the captured interval contains a real hit, not another test's hit."""
import csv
import hashlib
import json
from pathlib import Path
import sys

BASE=Path(__file__).resolve().parent.parent/'baseline'
run=BASE/sys.argv[1];kind=sys.argv[2]
side,damage,hold,length={'ball':(1,24,None,0),'blade':(1,26,None,0),'choke':(1,32,0x217,69),'leg':(2,35,0x21a,46),
                        'bike':(2,22,None,0),'square':(2,27,None,0),
                        'knife':(1,22,None,0),'ring':(2,22,None,0)}[kind]
video=json.loads((run/'FINISHER_VIDEO.json').read_text())
clip=Path(video['file'])
assert hashlib.sha256(clip.read_bytes()).hexdigest().upper()==video['SHA256']
start=video['firstGuestFrame'];end=start+video['frames']
csv_kind={'ball':'special','square':'special','knife':'projectiles','ring':'projectiles'}.get(kind,kind)
rows=[row for row in csv.DictReader((run/(csv_kind+'.csv')).open()) if start<=int(row['frame'])<end]
assert [int(row['frame']) for row in rows]==list(range(start,end))
other=3-side
assert int(rows[0][f'p{other}hp'])-int(rows[-1][f'p{other}hp'])==damage
if hold is not None:assert sum(int(row[f'p{side}action'])==hold for row in rows)==length
pulses=[int(before[f'p{other}hp'])-int(after[f'p{other}hp']) for before,after in zip(rows,rows[1:])
        if int(after[f'p{other}hp'])<int(before[f'p{other}hp'])]
assert pulses==([8]*4 if kind=='choke' else [damage])
assert rows[-1][f'p{side}action']=='771'
report=dict(scope='Actual captured hit/hold interval, not all move cases',kind=kind,
    frames=len(rows),damageObserved=damage,pulses=pulses,holdFields=length,
    performerReturnedToStance=True,victimReturnedToStance=rows[-1][f'p{other}action']=='771',
    clipSHA256=video['SHA256'],completeRecoveryVideoQualified=rows[-1][f'p{other}action']=='771',
    fullPortVerified=False)
(run/'CAPTURED_HIT_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
