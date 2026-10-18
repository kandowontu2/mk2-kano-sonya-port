"""Finite Sonya immunity proof plus an original male positive control."""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
from current_graphics import graphics_metadata
PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';BUILD=BASE/'mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
lanes=[b''.join((BUILD/f'rom/P12{p}.{i}').read_bytes() for p in ('F8','FC')) for i in (0,1)]
program=bytearray(0x100000);program[::2]=lanes[0];program[1::2]=lanes[1]
def read(a):return struct.unpack_from('<I',program,(a-0xff800000)//8)[0]
assert read(symbols['ks_sonya_anitab1']+54*32)==read(symbols['ks_sonya_anitab1']+55*32)==symbols['ks_sonya_bike_victim']
for argument in sys.argv[1:]:
    folder=BASE/argument;receipt=json.loads((folder/'execution.json').read_text())
    assert '--nut-victim' in receipt['testArguments']
    male='--stock-victim' in receipt['testArguments']
    sonya='--sonya' in receipt['testArguments'] and not male
    identity=1 if male else (18 if sonya else 17)
    assert receipt['exitCode']==0 and not receipt['timedOut'] and not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
        assert hashlib.sha256(lanes[lane]).hexdigest().upper()==receipt['replacementChips'][chip]
    for chip,digest in graphics_metadata()['sockets'].items():
        assert receipt['replacementChips'][chip]==digest
    rows=list(csv.DictReader((folder/'nut.csv').open()))
    assert int(rows[-1]['frame'])==9000 and all(int(r['missing'])==0 for r in rows)
    fight=[r for r in rows if r['mode']=='2' and r['p1selected']=='2' and r['p2selected']==str(identity)]
    active=[r for r in fight if int(r['action'])==0x10a];assert len(active)>=30
    damage=max(int(r['victimHP']) for r in fight)-min(int(r['victimHP']) for r in fight)
    assert damage==(0 if sonya else 34)
    assert any(int(r['victimAction'])==0x406 for r in fight)==(not sonya)
    if not male and not sonya:
        poses=[symbols[f'ks_nut_kano_pose{i}'] for i in range(2)]
        assert {int(r['victimShape'],16) for r in fight if int(r['victimAction'])==0x406}>=set(poses)
        root=read(symbols['ks_kano_anitab1']+54*32)
        assert root==symbols['ks_kano_nutcrunched']
        assert tuple(read(root+i*32) for i in range(5))==(poses[0],poses[1],0,poses[0],0)
    end=max(int(r['fight']) for r in active)
    recovery=[r for r in fight if end+160<=int(r['fight'])<=end+380]
    assert len(recovery)==221 and all(int(r['action'])==0x303 and int(r['victimAction'])==0x303 for r in recovery)
    assert all(r['ownerY']==r['ownerGround'] and r['victimY']==r['victimGround'] for r in recovery)
    report=dict(qualified=True,victim='liu_positive_control' if male else ('sonya' if sonya else 'kano'),
        cagePlayer=2 if '--mirror' in receipt['testArguments'] else 1,nativeSplitActionFields=len(active),
        observedDamage=damage,groundedRecoveryObservations=221,missingMarkers=0,
        fullVisualAcceptance=False,fullPortVerified=False)
    (folder/'NUT_IMMUNITY_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
