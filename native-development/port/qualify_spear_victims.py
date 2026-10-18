"""Pin native spear table, physical hits and recovery on both player sides."""
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
from spear_alignment_source import ALIGNMENTS

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
program=bytearray(1048576);program[::2]=lanes[0];program[1::2]=lanes[1]
table=struct.unpack_from('<19H',program,(symbols['spear_adjustments']-0xff800000)//8)
assert table[:17]==(0x70,0x77,0x74,0x75,0x75,0x75,0x75,0x7c,0x7c,0x7c,0x80,0x7c,0x88,0x88,0x7c,0x7c,0x7c)
assert table[17:]==ALIGNMENTS
cases=[]
names=sys.argv[1:]
assert len(names)==4 and len(set(names))==4,'Supply Kano/Sonya victim-side2, then Kano/Sonya victim-side1 runs'
evidence=[Path(__file__),PORT/'verify_finisher_roms.py',PORT/'spear_alignment_source.py',SRC/'MK2P.MAP']
for (actor,label,side),name in zip(((17,'kano',2),(18,'sonya',2),(17,'kano',1),(18,'sonya',1)),names):
    assert name and Path(name).name==name and '/' not in name and '\\' not in name
    folder=BASE/name;receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert '--spear-victim' in receipt['testArguments']
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
    # The probe normalizes legacy p1/p2 columns to attacker/victim even
    # when their physical player sides are mirrored.
    assert all(row['p1char']=='10' and int(row['p2char'])==actor for row in fight)
    assert {int(row['victimHP']) for row in fight}=={161,153}
    hit=[row for row in fight if row['victimAction']=='1541']
    expected_fields=110 if side==1 else 111
    assert len(hit)==expected_fields and int(hit[-1]['fight'])-int(hit[0]['fight'])==expected_fields-1
    poses={address for symbol,address in symbols.items() if symbol.startswith(f'ks_{label}_pose_')}
    assert all(int(row['victimShape'],16) in poses for row in hit)
    distances=[abs(int(row['p1x'])-int(row['p2x'])) for row in hit]
    assert distances[0]==208 and distances[-1]==64
    after=[row for row in fight if int(hit[-1]['fight'])<int(row['fight'])<int(hit[-1]['fight'])+100]
    assert after and all(row['victimAction']=='771' for row in after)
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    captures={str(tick):sha((folder/f'snap/spear_{tick}.png').read_bytes()) for tick in (160,180,200,300)}
    cases.append(dict(actor=actor,run=name,victimSide=side,damage=8,hitAndStunFields=len(hit),
        initialDistance=208,finalDistance=64,ownBodyRetained=True,recoveredToStance=True,captureSHA256=captures))
    evidence.extend(folder/item for item in ('execution.json','autoboot.lua','liu_bike.csv','mame.log'))
report=dict(scope='One physical Scorpion spear per character on each player side',cases=cases,
    programLaneSHA256=[sha(data) for data in lanes],compiledAlignmentWords=list(table),
    nativeHitPullStunRecoveryVerified=True,mirroredSidesVerified=True,
    allPosesDistancesAndInterruptionsVerified=False,releaseReady=False,fullPortVerified=False)
report['currentFull26ROMBytesVerified']=True
report['pins']={str(path):sha(path.read_bytes()) for path in evidence}
(PORT/'SPEAR_VICTIM_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
