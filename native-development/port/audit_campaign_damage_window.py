"""Qualify the read-only repeat and document why an action tag is not a pose."""
import csv
import hashlib
import json
from pathlib import Path
import zipfile

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
first=BASE/'stock_wolf_game549';observed=BASE/'stock_wolf_game550'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
assert (first/'campaign.csv').read_bytes()==(observed/'campaign.csv').read_bytes()
audit=json.loads((observed/'CAMPAIGN_AUDIT.json').read_text())
assert audit['currentFullROMVerified'] and not audit['illegalOpcodeRecoveryObserved']
receipt=json.loads((observed/'execution.json').read_text())
assert receipt['exitCode']==0 and not receipt['timedOut']
assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
frozen=(observed/'autoboot.lua').read_bytes()
assert sha(frozen)==receipt['controllerSHA256']
# This qualifier concerns fixed historical runs549/550. Instrumentation may
# evolve later; qualify the exact observer frozen with550, never today's file.
marker=b'-- Bounded read-only evidence window; never drives inputs or alters game state.'
assert frozen.count(marker)==1
observer_bytes=marker+frozen.split(marker,1)[1]
observer_sha=sha(observer_bytes)
assert observer_sha=='C834684D44D221508F0D797E11DF7A570A89F0B18D94334174882152AC25817A'
assert b':write_u' not in observer_bytes and b'set_value' not in observer_bytes
source=BASE/'mk2-rebuild-main/srcp/MKDRONE.ASM'
with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as archive:
    original=archive.read('mk2-rebuild-main/src/MKDRONE.ASM').decode('cp437').replace('\r\n','\n')
def rapid(text):return text.split('\ndrone_rfp\n',1)[1].split('\ndrone_flip_kick\n',1)[0]
body=rapid(source.read_text())
assert body==rapid(original)
assert 'calla\tinit_special\n' in body and 'p_action' not in body
objects=list(csv.DictReader((observed/'damage_objects.csv').open()))
processes=list(csv.DictReader((observed/'damage_processes.csv').open()))
assert {int(row['frame']) for row in objects}==set(range(10780,11001))
assert {int(row['frame']) for row in processes}==set(range(10780,11001))
sample=[]
for frame in (10900,10920,10940):
    body_row=next(row for row in objects if int(row['frame'])==frame and row['char']=='11')
    proc=next(row for row in processes if int(row['frame'])==frame and row['pid']=='0002')
    assert proc['object']==body_row['object'] and proc['action']=='0303'
    image=observed/f'snap/damage_{frame:05d}.png'
    assert image.exists()
    sample.append(dict(frame=frame,jaxShape=body_row['shape'],jaxProcessAction=proc['action'],
        screenshotSHA256=sha(image.read_bytes())))
report=dict(scope='One bounded read-only observation repeat, not all incoming-damage correctness',
    baseline=first.name,observation=observed.name,traceByteIdentical=True,
    campaignTraceSHA256=sha((observed/'campaign.csv').read_bytes()),
    observationWindow=[10780,11000],originalRapidPunchRoutinePreserved=True,
    actionTagAloneDoesNotEstablishIdle=True,manuallyInspectedPunchFrames=sample,
    suspectedProjectileBugConfirmed=False,allDamageCausesProven=False,releaseReady=False,
    frozenObserverSHA256=observer_sha)
report['evidenceSHA256']={str(path):sha(path.read_bytes()) for path in
    (observed/'autoboot.lua',source,observed/'damage_objects.csv',observed/'damage_processes.csv',observed/'execution.json',Path(__file__))}
(observed/'DAMAGE_WINDOW_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({key:value for key,value in report.items() if key!='evidenceSHA256'},indent=2))
