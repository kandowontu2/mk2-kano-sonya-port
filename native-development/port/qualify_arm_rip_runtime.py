"""Limited physical arm-rip completion and own-frame coverage, not visual QA."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import struct
import zipfile
from current_graphics import verify_archive_sockets
from arm_rip_source import DEATH,BLOOD,GUSH_NEW
from verify_finisher_roms import verify

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
assert all(new in (SRC/'MKDEATH.ASM').read_text() for old,new in DEATH)
assert all(new in (SRC/'MKBLOOD.ASM').read_text() for old,new in BLOOD)
assert GUSH_NEW in (SRC/'MKBLOOD.ASM').read_text()
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
program=bytearray(1048576);program[::2]=lanes[0];program[1::2]=lanes[1]
art=json.loads((PORT/'generated_arm_rip/ARM_RIP_DATA.json').read_text())
for frame in art['frames']:
    address=symbols[frame['imageLabel']]
    header=struct.unpack_from('<HHhhIHI',program,(address-0xff800000)//8)
    assert header==(frame['width'],frame['height'],frame['xOffset'],frame['yOffset'],
        (0xc00000+frame['packedByteOffset'])*8,0x6000,symbols[f"ks_{frame['actor']}_primary_palette"])
names=sys.argv[1:];assert len(names) in (2,4) and len(set(names))==len(names), 'Supply explicit distinct current runs'
cases=[]
for index,name in enumerate(names):
    assert name and Path(name).name==name and '/' not in name and '\\' not in name
    folder=BASE/name;receipt=json.loads((folder/'execution.json').read_text())
    actor,label=(18,'sonya') if '--sonya' in receipt['testArguments'] else (17,'kano')
    assert '--stock-victim' not in receipt['testArguments']
    assert not any(arg.startswith('--arms-control=') for arg in receipt['testArguments'])
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert '--arms-victim' in receipt['testArguments']
    assert ('--sonya' in receipt['testArguments'])==(actor==18)
    side=1 if '--mirror' in receipt['testArguments'] else 2
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        verify(archive,receipt)
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    rows=list(csv.DictReader((folder/'arms.csv').open()))
    assert int(rows[-1]['frame'])==9000
    assert all(row['missing']=='0' and int(row['pc'],16)!=symbols['illegal_opcode']+0x50 for row in rows)
    fight=[row for row in rows if row['mode']=='2' and int(row[f'p{side}char'])==actor and row[f'p{3-side}char']=='11']
    kos=[row for previous,row in zip(fight,fight[1:]) if int(previous[f'p{side}hp'])>0 and row[f'p{side}hp']=='0']
    assert len(kos)==2
    active=[row for row in fight if row['death']=='2'];done=[row for row in fight if row['death']=='65535']
    assert len(active)==147 and done and int(done[0]['frame'])==int(active[-1]['frame'])+1
    objects=list(csv.DictReader((folder/'fan_objects.csv').open()))
    coverage={}
    for role in ('body_pose','arm_frame'):
        for phase in range(5):
            address=symbols[f'ks_ar_{label}_{role}{phase}']
            hits=[row for row in objects if int(row['shape'],16)==address or int(row['image'],16)==address]
            assert hits and all(row['missing']=='0' for row in hits)
            if role=='body_pose':assert all(int(row['character'])==actor for row in hits)
            else:assert len({row['object'] for row in hits})==2
            coverage[f'{role}{phase}']=len(hits)
    assert not list(folder.glob('*fault*')) and '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(actor=actor,run=name,victimSide=side,naturalKOs=2,nativeFatalityFields=147,
        completionFrame=int(done[0]['frame']),ownBodyPhases=5,ownDetachedArmPhases=5,
        detachedArmObjectCount=2,trueVictimIDRetained=True,observedPhaseRows=coverage))
assert {case['actor'] for case in cases}=={17,18}
assert len({(case['actor'],case['victimSide']) for case in cases})==len(cases)
report=dict(scope='Physical Jax arm-rip activation, all own phases and native completion',cases=cases,
    programLaneSHA256=[sha(data) for data in lanes],nativeCompletionWithoutRecoveryVerified=True,
    compiledOwnHeadersVerified=20,
    mirroredSidesVerified=all({case['victimSide'] for case in cases if case['actor']==actor}=={1,2} for actor in (17,18)),
    alignmentAndBloodPlacementAccepted=False,originalCharacterRuntimeRegressionVerified=False,
    cleanRebuildCurrentLinkVerified=False,releaseReady=False,fullPortVerified=False)
paths=[Path(__file__),PORT/'verify_finisher_roms.py',PORT/'arm_rip_source.py',
       SRC/'MK2P.OUT',SRC/'MK2P.MAP',SRC/'MKDEATH.ASM',SRC/'MKDIE.ASM',
       SRC/'MKBLOOD.ASM',SRC/'KSARART.ASM',PORT/'generated_arm_rip/ARM_RIP_DATA.json']
for name in names:
    folder=BASE/name
    paths.extend(folder/item for item in ('execution.json','autoboot.lua','arms.csv','fan_objects.csv','mame.log'))
    paths.extend(sorted((folder/'snap').glob('*.png')))
report['currentFull26ROMBytesVerified']=True
report['pins']={str(path):sha(path.read_bytes()) for path in paths}
(PORT/'ARM_RIP_RUNTIME_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
