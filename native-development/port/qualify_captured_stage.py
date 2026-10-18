"""Qualify the stage actually present in a captured interval."""
import csv
import hashlib
import json
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parent.parent/'baseline'
run=BASE/sys.argv[1];kind=sys.argv[2]
assert kind in ('deadpool','tomb','pit')
video=json.loads((run/'FINISHER_VIDEO.json').read_text())
assert hashlib.sha256(Path(video['file']).read_bytes()).hexdigest().upper()==video['SHA256']
start=video['firstGuestFrame'];end=start+video['frames']
all_rows=list(csv.DictReader((run/'stage.csv').open()))
rows=[row for row in all_rows if start<=int(row['frame'])<end]
assert [int(row['frame']) for row in rows]==list(range(start,end))
environment={int(row['frame']):int(row['background']) for row in csv.DictReader((run/'stage_environment.csv').open())}
assert all(environment[int(row['frame'])]=={'deadpool':0,'tomb':1,'pit':6}[kind] for row in rows)
args=json.loads((run/'execution.json').read_text())['testArguments']
side=2 if '--mirror' in args else 1;other=3-side
actor=18 if '--sonya' in args else 17
assert all(int(row[f'p{side}char'])==actor and int(row[f'p{other}char'])==35-actor for row in rows)
if kind=='deadpool':assert any(int(row[f'p{other}action'])==0x50a for row in rows)
elif kind=='tomb':assert len(rows)==64 and all(row['death']=='8' for row in rows)
else:
    assert len(rows)==266
    assert all(row['death']=='6' for row in rows[:206])
    assert all(row['death']=='65535' for row in rows[206:])
    assert {'2','9','5'}<=set(row['mode'] for row in rows)
if kind!='pit':assert any(int(row['frame'])==end and row['death']=='65535' for row in all_rows)
report=dict(scope='Captured native stage sequence through completion',kind=kind,actor=actor,
    frames=len(rows),correctStageWithinActualClip=True,nativeCompletionImmediatelyAfterClip=kind!='pit',
    nativeCompletionAnd60FieldImpactHoldWithinClip=kind=='pit',
    clipSHA256=video['SHA256'],uppercutStartupIncluded=int(rows[0][f'p{side}action'])==0x107,
    fullVisualAudioAcceptance=False,fullCampaignVerified=False)
(run/'CAPTURED_STAGE_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
