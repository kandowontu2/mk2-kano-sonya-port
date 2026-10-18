"""Finite real-input Shang drain proof, including the native skeleton handoff."""
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
program=bytearray(0x100000);program[::2]=lanes[0];program[1::2]=lanes[1]
def read(a,fmt):return struct.unpack_from('<'+fmt,program,(a-0xff800000)//8)
metadata=json.loads((PORT/'generated_drain/DRAIN_DATA.json').read_text())
for argument in sys.argv[1:]:
    folder=BASE/argument
    receipt=json.loads((folder/'execution.json').read_text())
    assert '--drain-victim' in receipt['testArguments'] and '--stock-victim' not in receipt['testArguments']
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
        assert sha(lanes[lane])==receipt['replacementChips'][chip]
    graphics=graphics_metadata()
    for chip,digest in graphics['sockets'].items():assert receipt['replacementChips'][chip]==digest
    actor='sonya' if '--sonya' in receipt['testArguments'] else 'kano'
    identity=18 if actor=='sonya' else 17
    poses=[symbols[f'ks_dr_{actor}_pose{i}'] for i in range(3)]
    root=symbols[f'ks_{actor}_drain_shrink']
    assert read(symbols['drain_table']+identity*32,'I')==(root,)
    assert read(symbols['alternate_suck_pals']+identity*32,'I')==(symbols[f'ks_{actor}_primary_palette'],)
    assert read(root,'9I')==tuple(poses+[0,poses[1],poses[0],poses[1],poses[2],0])
    for phase,frame in enumerate(metadata['records'][actor]):
        pointer=read(poses[phase],'2I');assert pointer[1]==0
        assert read(pointer[0],'HHhhIHI')==(frame['width'],frame['height'],(-2,-2,-3)[phase],(5,3,1)[phase],
            (0xc00000+frame['packedByteOffset'])*8,0x6000,symbols[f'ks_{actor}_primary_palette'])
    corpse=read(symbols['a_final_drain'],'I')[0]
    rows=list(csv.DictReader((folder/'fan_objects.csv').open()))
    assert rows and all(int(r['character'])==identity and int(r['missing'])==0 for r in rows)
    sequence=[]
    for row in rows:
        shape=int(row['shape'],16)
        assert shape in poses+[corpse]
        if not sequence or sequence[-1]!=shape:sequence.append(shape)
    assert sequence==poses+[poses[1],poses[0],poses[1],poses[2],corpse]
    main=list(csv.DictReader((folder/'fan.csv').open()))
    first=next(r for r in main if r['frame']==rows[0]['frame'])
    expected_y=int(first['ground'])-129-21 # Native Shang origin, main38 adjustment sum.
    assert all(int(r['y'])==expected_y for r in rows)
    assert max(int(r['missing']) for r in main)==0
    assert any(r['death']=='1' for r in rows) and any(r['death']=='65535' for r in rows)
    assert not (folder/'fan_fault.txt').exists()
    result=dict(qualified=True,scope='One real-input native Shang soul drain',victim=actor,
                shangPlayer=2 if '--mirror' in receipt['testArguments'] else 1,
                ownShrinkPhaseObservations=[sum(int(r['shape'],16)==p for r in rows) for p in poses],
                nativeSkeletonObservations=sum(int(r['shape'],16)==corpse for r in rows),
                nativePoseSequenceVerified=True,nativeLiftOriginY=expected_y,
                rightSidePaletteEntryVerified=True,
                nativeCompletionObserved=True,missingMarkers=0,
                alternateCostumeVerified=False,fullVisualAcceptance=False,fullPortVerified=False)
    (folder/'DRAIN_RUNTIME_QUALIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
