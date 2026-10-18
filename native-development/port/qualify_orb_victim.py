"""Finite Reptile orb victim proof, pinned to the tested native program."""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
BUILD=BASE/'mk2-rebuild-main/srcp'
symbols={}
for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text()):
    symbols[name]=int(address,16)
lanes=[b''.join((BUILD/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in (0,1)]
program=bytearray(0x100000)
program[::2]=lanes[0];program[1::2]=lanes[1]
def longs(address,count):
    return struct.unpack_from('<'+'I'*count,program,(address-0xff800000)//8)

for case in sys.argv[1:]:
    folder=BASE/case
    receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
        assert hashlib.sha256(lanes[lane]).hexdigest().upper()==receipt['replacementChips'][chip]
    rows=list(csv.DictReader((folder/'liu_bike.csv').open()))
    assert len(rows)==9000 and all(int(r['missing'])==0 for r in rows)
    combat=[r for r in rows if r['mode']=='2' and 0<int(r['fight'])<600]
    target=int(combat[0]['p2char']);assert target in (17,18)
    assert all(int(r['p1char'])==9 and int(r['p2char'])==target for r in combat)
    actor='kano' if target==17 else 'sonya'
    names=('ff82aa60','ff82aaa0','ff82ab40','ff82ab80') if target==17 else ('ff83adc0','ff83ae00','ff83aec0','ff83af20')
    poses=[symbols[f'ks_{actor}_pose_{name}'] for name in names]
    root=symbols[f'ks_{actor}_banged']
    assert longs(symbols[f'ks_{actor}_anitab1']+58*32,1)==(root,)
    assert longs(root,5)==tuple(poses+[0])
    observed=[int(r['victimShape'],16) for r in combat]
    positions=[observed.index(pose) for pose in poses]
    assert positions==sorted(positions) and len(set(positions))==4
    assert min(int(r['victimHP']) for r in combat)<int(combat[0]['victimHP'])
    assert any(int(r['fight'])>500 and int(r['victimShape'],16) not in poses for r in combat)
    result={'qualified':True,'scope':'Native four-pose orb knockback, real damage and subsequent animation recovery; not full-port acceptance',
            'victim':actor,'attackerPlayer':2 if '--mirror' in receipt['testArguments'] else 1,
            'frames':len(rows),'ownPosesInOrder':4,'missingMarkers':0,'fullPortVerified':False}
    (folder/'orb_qualification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
