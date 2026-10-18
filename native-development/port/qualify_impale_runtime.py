"""Finite physical Baraka impalement proof on current stock-MAME ROMs."""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
from current_graphics import graphics_metadata

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
BUILD=BASE/'mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
lanes=[b''.join((BUILD/f'rom/P12{p}.{i}').read_bytes() for p in ('F8','FC')) for i in (0,1)]
program=bytearray(0x100000)
program[::2]=lanes[0]
program[1::2]=lanes[1]
def read(a,fmt): return struct.unpack_from('<'+fmt,program,(a-0xff800000)//8)
for argument in sys.argv[1:]:
    folder=BASE/argument
    receipt=json.loads((folder/'execution.json').read_text())
    assert '--impale-victim' in receipt['testArguments'] and '--stock-victim' not in receipt['testArguments']
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
        assert sha(lanes[lane])==receipt['replacementChips'][chip]
    for chip,digest in graphics_metadata()['sockets'].items():
        assert receipt['replacementChips'][chip]==digest
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    actor='sonya' if '--sonya' in receipt['testArguments'] else 'kano'
    identity=18 if actor=='sonya' else 17
    poses=[symbols[f'ks_im_{actor}_pose{i}'] for i in range(3)]
    root=symbols[f'ks_{actor}_impaled']
    assert read(symbols[f'ks_{actor}_anitab1']+59*32,'I')==(root,)
    assert read(root,'21I')==(4,0x0010ffa0,poses[0],4,0xffe80000,poses[0],4,0xffe80000,poses[0],4,0xffe80010,poses[0],0,
        poses[0],poses[1],poses[2],poses[1],poses[0],poses[1],poses[2],0)
    rows=list(csv.DictReader((folder/'fan_objects.csv').open()))
    assert rows and all(int(r['character'])==identity and int(r['missing'])==0 for r in rows)
    assert {int(r['shape'],16) for r in rows}==set(poses)
    records=[]
    for phase,pose in enumerate(poses):
        observed=[r for r in rows if int(r['shape'],16)==pose]
        assert len(observed)>=20
        records.append(dict(phase=phase,observations=len(observed),observedY=sorted({int(r['y']) for r in observed})))
    assert records[0]['observedY']==[20,44,68,92]
    assert records[1]['observedY']==[20]
    assert records[2]['observedY']==list(range(20,35))
    assert any(r['death']=='65535' for r in rows)
    main=list(csv.DictReader((folder/'fan.csv').open()))
    assert max(int(r['missing']) for r in main)==0 and not (folder/'fan_fault.txt').exists()
    assert any(r['death']=='1' for r in main)
    mirrored='--mirror' in receipt['testArguments']
    performer,victim=('p2','p1') if mirrored else ('p1','p2')
    combat=[r for r in main if r[performer+'char']=='3' and int(r[victim+'char'])==identity]
    assert combat and any(r[victim+'hp']=='0' for r in combat)
    result=dict(qualified=True,scope='One physical native Baraka impalement',victim=actor,
        performerPlayer=2 if '--mirror' in receipt['testArguments'] else 1,
        ownPoseObservations=records,nativeTwoPartScriptVerified=True,nativeLiftAndFinalSlideVerified=True,
        nativeCompletionObserved=True,missingMarkers=0,fullVisualAcceptance=False,fullPortVerified=False)
    (folder/'IMPALE_RUNTIME_QUALIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
