"""Finite native Jax back-break proof; does not certify full port/style acceptance."""
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
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
metadata=json.loads((PORT/'generated_backbreak/BACKBREAK_DATA.json').read_text())
lanes=[b''.join((BUILD/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in (0,1)]
program=bytearray(0x100000);program[::2]=lanes[0];program[1::2]=lanes[1]
def words(address,count):return struct.unpack_from('<'+'I'*count,program,(address-0xff800000)//8)
for argument in sys.argv[1:]:
    folder=BASE/argument;receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
        assert hashlib.sha256(lanes[lane]).hexdigest().upper()==receipt['replacementChips'][chip]
    current_graphics=graphics_metadata()
    current_prefix=(PORT/'generated_torso/fighter_ui_finish_torso_graphics.bin').read_bytes()
    assert current_graphics['prefixSHA256']==hashlib.sha256(current_prefix).hexdigest().upper()
    assert current_prefix.startswith((PORT/'generated_backbreak/fighter_ui_finish_backbreak_graphics.bin').read_bytes())
    for chip,digest in current_graphics['sockets'].items():assert receipt['replacementChips'][chip]==digest
    actor='sonya' if '--sonya' in receipt['testArguments'] else 'kano';identity=18 if actor=='sonya' else 17
    poses=[symbols[f'ks_bk_{actor}_pose{i}'] for i in range(3)]
    root=symbols[f'ks_{actor}_back_broke']
    assert words(symbols[f'ks_{actor}_anitab1']+63*32,1)==(root,)
    assert words(root,13)==(poses[0],4,10<<16,poses[0],4,48<<16,poses[0],poses[1],poses[2],0,poses[1],poses[0],0)
    for pose,frame in zip(poses,metadata['records'][actor]):
        pointer,terminator=words(pose,2);assert terminator==0
        w,h,x,y,sag,control,palette=struct.unpack_from('<HHhhIHI',program,(pointer-0xff800000)//8)
        assert (w,h,x,y)==(frame['width'],frame['height'],frame['xOffset'],frame['yOffset'])
        assert sag==(0xc00000+frame['packedByteOffset'])*8 and control==0x6000
        assert palette==symbols[f'ks_{actor}_primary_palette']
    rows=list(csv.DictReader((folder/'backbreak.csv').open()))
    assert len(rows)==9000 and all(int(r['missing'])==0 for r in rows)
    combat=[r for r in rows if r['mode']=='2' and int(r['fight'])>0]
    assert all(int(r['p1char'])==11 and int(r['p2char'])==identity for r in combat)
    assert all(int(r['pc'],16)>=0xff800000 and int(r['pc'],16)!=symbols['illegal_opcode']+0x50 for r in combat)
    active=[r for r in combat if int(r['action'])==0x109];assert active
    assert set(poses)<={int(r['victimShape'],16) for r in active}
    first=int(active[0]['fight']);last=int(active[-1]['fight'])
    window=[r for r in combat if first<=int(r['fight'])<=last+180]
    assert int(active[0]['victimHP'])-min(int(r['victimHP']) for r in window)==32
    settled=[r for r in combat if last+180<=int(r['fight'])<=last+400]
    assert len(settled)>=200
    assert all(r['ownerY']==r['ownerGround'] and r['victimY']==r['victimGround'] and int(r['action'])!=0x109 for r in settled)
    edgeProof=None
    if '--throw-front-edge' in receipt['testArguments']:
        setup=json.loads((folder/'backbreak_edge_setup.json').read_text())
        assert setup['stationaryFieldsWhileAwayHeld']>=30 and not setup['guestWrites']
        assert first>setup['fight'] and active[0]['edgeReady']=='1'
        right=setup['ownerX']<setup['victimX']
        assert all((int(r['p2x'])<=setup['victimX'] if right else int(r['p2x'])>=setup['victimX']) for r in settled)
        edgeProof={'physicalSetup':setup,'releasedWithinObservedFrontBoundary':True}
    result={'qualified':True,'scope':'One physical Jax back-break against an added victim; native completion and recovery only',
            'jaxPlayer':2 if '--mirror' in receipt['testArguments'] else 1,
            'victim':actor,'frames':len(rows),'nativeActionFields':len(active),'ownPosesObserved':3,'damage':32,
            'settledGroundedObservations':len(settled),'missingMarkers':0,'fullVisualAcceptance':False,'fullPortVerified':False}
    if edgeProof:result['frontEdgeProof']=edgeProof
    (folder/'backbreak_runtime_qualification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
