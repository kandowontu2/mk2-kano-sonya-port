"""Check compiled tackle tables and physical drag/recovery on both sides."""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import zipfile
from verify_finisher_roms import verify as verify_full_rom
from current_graphics import verify_archive_sockets
from dive_alignment_source import POSES,ADJUSTMENTS

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
program=bytearray(1048576);program[::2]=lanes[0];program[1::2]=lanes[1]
offset=lambda name:(symbols[name]-0xff800000)//8
poses=struct.unpack_from('<19H',program,offset('ochar_dived_poses'))
adjust=struct.unpack_from('<38h',program,offset('ochar_dived_adjust'))
assert poses[:17]==(1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1)
assert adjust[:34]==(-64,0,-74,8,-72,0,-72,0,-72,0,-72,0,-72,0,-72,0,
    -72,0,-72,0,-72,0,-80,0,-96,0,-72,-20,-72,0,-72,0,-72,0)
assert poses[17:]==POSES and adjust[34:]==sum(ADJUSTMENTS,())
cases=[]
names=sys.argv[1:]
assert len(names)==4 and len(set(names))==4,'Supply Kano/Sonya victim-side2, then Kano/Sonya victim-side1 cases'
evidence=[Path(__file__),PORT/'verify_finisher_roms.py',PORT/'dive_alignment_source.py',SRC/'MK2P.MAP']
for (actor,label,side),run in zip(((17,'kano',2),(18,'sonya',2),(17,'kano',1),(18,'sonya',1)),names):
    assert run and Path(run).name==run and '/' not in run and '\\' not in run
    folder=BASE/run;receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert '--dive-victim' in receipt['testArguments']
    assert ('--mirror' in receipt['testArguments'])==(side==1)
    assert ('--sonya' in receipt['testArguments'])==(actor==18)
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        verify_full_rom(archive,receipt)
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    trace=list(csv.DictReader((folder/'liu_bike.csv').open()))
    assert int(trace[-1]['frame'])==9000
    assert all(row['missing']=='0' and int(row['pc'],16)!=symbols['illegal_opcode']+0x50 for row in trace)
    fight=[row for row in trace if row['mode']=='2']
    # Probe retains normalized attacker/victim columns when mirrored.
    assert all(row['p1char']=='7' and int(row['p2char'])==actor for row in fight)
    assert {int(row['victimHP']) for row in fight}=={161,131}
    drag=[row for row in fight if 140<=int(row['fight'])<=160]
    assert len(drag)==21 and all(abs(int(row['p1x'])-int(row['p2x']))==72 for row in drag)
    assert abs(int(drag[-1]['p1x'])-int(drag[0]['p1x']))==200
    assert abs(int(drag[-1]['p2x'])-int(drag[0]['p2x']))==200
    own={address for name,address in symbols.items() if name.startswith(f'ks_{label}_pose_')}
    assert all(int(row['victimShape'],16) in own for row in drag)
    after=[row for row in fight if 400<int(row['fight'])<600]
    assert after and all(row['action']=='771' and row['victimAction']=='771' for row in after)
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(actor=actor,run=run,victimSide=side,damage=30,
        sampledDragFields=21,relativeXDistance=72,bothTravelledPixels=200,
        ownBodyRetained=True,bothRecoveredToStance=True,
        screenshotSHA256=sha((folder/'snap/dive_150.png').read_bytes())))
    evidence.extend(folder/item for item in ('execution.json','autoboot.lua','liu_bike.csv','mame.log'))
    evidence.extend(folder/f'snap/dive_{tick}.png' for tick in range(130,351,10))
report=dict(scope='Physical Raiden tackle against both added IDs on both player sides',cases=cases,
    programLaneSHA256=[sha(data) for data in lanes],compiledPoseWords=list(poses),compiledAdjustmentWords=list(adjust),
    damageDragAndRecoveryVerified=True,mirroredSidesVerified=True,visualLineupAccepted=False,
    allBlockingInterruptionsAndEdgeCasesVerified=False,releaseReady=False,fullPortVerified=False)
report['currentFull26ROMBytesVerified']=True
report['pins']={str(path):sha(path.read_bytes()) for path in evidence}
(PORT/'DIVE_VICTIM_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
