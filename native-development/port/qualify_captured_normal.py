"""Actual native normal-move contact and two-stance recovery inside the MP4."""
import csv
import json
import sys
from pathlib import Path
from inspect_normal_runtime import BASE,sha

def verify_interval(rows,side,action,damage):
    other=3-side
    assert rows and int(rows[0][f'p{side}action'])==action
    assert all(r['mode']=='2' for r in rows)
    assert int(rows[0][f'p{other}hp'])-int(rows[-1][f'p{other}hp'])==damage
    assert rows[-1][f'p{side}action']==rows[-1][f'p{other}action']=='771'
    if action!=0x507:assert any(int(r[f'p{other}hitby'])==action for r in rows)

def main(name):
    assert name and all(c.isalnum() or c in '_-' for c in name)
    run=BASE/name
    contact=json.loads((run/'NORMAL_CONTACT_QUALIFICATION.json').read_text())
    assert not contact['blocking'] and contact['currentFull26ROMBytesVerified']
    video=json.loads((run/'FINISHER_VIDEO.json').read_text())
    assert sha(Path(video['file']))==video['SHA256']
    first=video['firstGuestFrame'];last=first+video['frames']
    with (run/'normals.csv').open() as stream:rows=[r for r in csv.DictReader(stream) if first<=int(r['frame'])<last]
    assert [int(r['frame']) for r in rows]==list(range(first,last))
    verify_interval(rows,contact['side'],contact['actualAction'],contact['damage'])
    report=dict(scope='One actual normal/proximity hit and two-stance recovery within recorded interval',
        actor=contact['actor'],side=contact['side'],action=contact['actualAction'],damage=contact['damage'],
        capturedFrames=len(rows),twoStanceRecoveryObserved=True,clipSHA256=video['SHA256'],
        exactAudioSyncAndEveryFrameVisualAcceptance=False,fullPortVerified=False)
    (run/'CAPTURED_NORMAL_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
