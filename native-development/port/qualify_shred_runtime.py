"""Finite physical Baraka blade-fury victim/recovery proof."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
from current_graphics import graphics_metadata
PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';BUILD=BASE/'mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
mapping=json.loads((PORT/'generated_reactions/SHRED_SOURCE.json').read_text())
for argument in sys.argv[1:]:
    folder=BASE/argument;receipt=json.loads((folder/'execution.json').read_text())
    assert '--shred-victim' in receipt['testArguments']
    assert receipt['exitCode']==0 and not receipt['timedOut'] and not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
        data=b''.join((BUILD/f'rom/P12{p}.{lane}').read_bytes() for p in ('F8','FC'))
        assert hashlib.sha256(data).hexdigest().upper()==receipt['replacementChips'][chip]
    for chip,digest in graphics_metadata()['sockets'].items():
        assert receipt['replacementChips'][chip]==digest
    actor='sonya' if '--sonya' in receipt['testArguments'] else 'kano';identity=18 if actor=='sonya' else 17
    rows=list(csv.DictReader((folder/'shred.csv').open()))
    assert int(rows[-1]['frame'])==9000 and all(int(r['missing'])==0 for r in rows)
    fight=[r for r in rows if r['mode']=='2' and r['p1selected']=='3' and r['p2selected']==str(identity)]
    active=[r for r in fight if int(r['action'])==0x11d]
    assert len(active)>=30
    poses={symbols[mapping[actor]['nativeToOwnPoseMapping'][f'LKSTUMBLE{i}']] for i in (1,2,3)}
    assert poses<={int(r['victimShape'],16) for r in active}
    assert max(int(r['victimHP']) for r in fight)-min(int(r['victimHP']) for r in fight)==40
    end=max(int(r['fight']) for r in active)
    recovered=[r for r in fight if end+120<=int(r['fight'])<=end+340]
    assert len(recovered)==221
    assert all(r['ownerY']==r['ownerGround'] and r['victimY']==r['victimGround'] for r in recovered)
    assert all(int(r['action'])==0x303 and int(r['victimAction'])==0x303 for r in recovered)
    result=dict(qualified=True,scope='One real-input native Baraka blade fury',victim=actor,
        barakaPlayer=2 if '--mirror' in receipt['testArguments'] else 1,
        nativeActionFields=len(active),ownVictimPosesObserved=3,damage=40,groundedRecoveryObservations=221,
        missingMarkers=0,fullVisualAcceptance=False,fullPortVerified=False)
    (folder/'SHRED_RUNTIME_QUALIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
