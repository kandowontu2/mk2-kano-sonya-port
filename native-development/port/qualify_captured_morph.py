"""Actual clip interval: Shang -> true added identity -> Shang, with own move."""
import csv
import hashlib
import json
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parent.parent/'baseline'
run=BASE/sys.argv[1];target=int(sys.argv[2]);assert target in (17,18)
video=json.loads((run/'FINISHER_VIDEO.json').read_text())
assert hashlib.sha256(Path(video['file']).read_bytes()).hexdigest().upper()==video['SHA256']
start=video['firstGuestFrame'];end=start+video['frames']
rows=[row for row in csv.DictReader((run/'morph.csv').open()) if start<=int(row['frame'])<end]
assert [int(row['frame']) for row in rows]==list(range(start,end))
assert all(row['mode']=='2' and row['p1selected']=='6' for row in rows)
assert rows[0]['p1char']==rows[-1]['p1char']=='6'
assert set(int(row['p1char']) for row in rows)=={6,target}
assert sum(int(row['p1char'])==target for row in rows)==524
action=0x211 if target==17 else 0x212
assert any(int(row['p1char'])==target and int(row['action'])==action for row in rows)
assert int(rows[0]['victimHP'])-int(rows[-1]['victimHP'])==22
report=dict(scope='One actual morph/own-projectile/automatic-return video interval',target=target,
    frames=len(rows),trueIdentityFields=524,selectionRemainsShang=True,
    transformedProjectileDamage=22,automaticReturnWithinClip=True,clipSHA256=video['SHA256'],
    finalVisualAudioAcceptance=False,fullPortVerified=False)
(run/'CAPTURED_MORPH_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
