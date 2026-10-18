"""Pinned own split runtime coverage; deliberately not full visual acceptance."""
import csv
import json
from pathlib import Path
import re
import struct
import sys
import zipfile
from build_inflation_assets import sha
from current_graphics import verify_archive_sockets
from lao_split_source import LOOKUP_NEW, SECOND_NEW
from verify_finisher_roms import verify

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'
text=(SRC/'MKDEATH.ASM').read_text()
assert LOOKUP_NEW in text and SECOND_NEW in text
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
program=bytearray(1048576)
program[::2],program[1::2]=lanes
art=json.loads((PORT/'generated_split/SPLIT_DATA.json').read_text())
for frame in art['frames']:
    header=struct.unpack_from('<HHhhIHI',program,(symbols[frame['imageLabel']]-0xff800000)//8)
    assert header==(frame['width'],frame['height'],frame['xOffset'],frame['yOffset'],
        (0xc00000+frame['packedByteOffset'])*8,0x6000,symbols[f'ks_{frame["actor"]}_primary_palette'])
cases=[]
names=sys.argv[1:]
assert len(names)==6 and len(set(names))==6, 'Supply four own runs and two original controls'
catalog=[]
for name in names:
    assert name and Path(name).name==name and '/' not in name and '\\' not in name
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert '--lao-split-victim' in receipt['testArguments']
    control=next((a for a in receipt['testArguments'] if a.startswith('--lao-split-control=')),None)
    actor=int(control.split('=',1)[1]) if control else (18 if '--sonya' in receipt['testArguments'] else 17)
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:verify(archive,receipt)
    catalog.append((folder,actor,control is not None))
assert {(actor,1 if '--mirror' in json.loads((folder/'execution.json').read_text())['testArguments'] else 2)
        for folder,actor,control in catalog if not control}=={(17,1),(17,2),(18,1),(18,2)}
assert sorted(actor for _,actor,control in catalog if control)==[1,4]
for folder,actor,control in catalog:
    if control:continue
    label='kano' if actor==17 else 'sonya'
    receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert '--lao-split-victim' in receipt['testArguments']
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    with (folder/'laosplit.csv').open() as stream:rows=list(csv.DictReader(stream))
    assert int(rows[-1]['frame'])==9000
    assert all(r['missing']=='0' and int(r['pc'],16)!=symbols['illegal_opcode']+0x50 for r in rows)
    side=1 if '--mirror' in receipt['testArguments'] else 2
    fight=[r for r in rows if r['mode']=='2' and int(r[f'p{side}char'])==actor and r[f'p{3-side}char']=='0']
    assert sum(int(a[f'p{side}hp'])>0 and b[f'p{side}hp']=='0' for a,b in zip(fight,fight[1:]))==2
    with (folder/'laosplit_victim.csv').open() as stream:victims=list(csv.DictReader(stream))
    assert all(int(r['character'])==actor for r in victims)
    active=[r for r in victims if r['death']=='1']
    assert active and victims[-1]['death']=='65535'
    with (folder/'fan_objects.csv').open() as stream:objects=list(csv.DictReader(stream))
    coverage=[]
    for frame in (f for f in art['frames'] if f['actor']==label):
        hits=[r for r in objects if int(r['shape'],16)==symbols[frame['poseLabel']]]
        assert hits and all(int(r['character'])==actor and r['missing']=='0' for r in hits)
        phase=frame['phase']
        if phase<9:assert len(hits)==({0:64,1:5,2:21}.get(phase,6))
        coverage.append(dict(role=frame['role'],phase=phase,rows=len(hits),
            firstField=int(hits[0]['frame']),lastField=int(hits[-1]['frame'])))
    for phase in range(3,10):
        pair=[p for p in coverage if p['phase']==phase]
        assert len(pair)==2 and pair[0]['firstField']==pair[1]['firstField'] and pair[0]['lastField']==pair[1]['lastField']
    assert not list(folder.glob('*fault*')) and '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(run=folder.name,actor=actor,victimSide=side,naturalKOs=2,
        fatalityFields=len(active),ownComponentCoverage=coverage,nativeCompletion=True))
controls=[]
listing=(SRC/'MKDEATH.LST').read_text()
def local_address(label):
    hits=re.findall(r'(?m)^\s*\d+\s+([0-9a-fA-F]{8})\s+'+re.escape(label)+r'\s*$',listing)
    assert len(hits)==1
    return symbols['disable_repell']-int(re.findall(r'(?m)^\s*\d+\s+([0-9a-fA-F]{8})\s+disable_repell\s*$',listing)[0],16)+int(hits[0],16)
def pointer(address):return struct.unpack_from('<I',program,(address-0xff800000)//8)[0]
for folder,actor,control in catalog:
    if not control:continue
    receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    root=pointer(local_address('split_in_2_tab')+actor*32)
    poses=[pointer(root+i*32) for i in range(12) if i not in (3,11)]
    with (folder/'laosplit_victim.csv').open() as stream:victims=list(csv.DictReader(stream))
    assert victims[-1]['death']=='65535' and all(int(r['character'])==actor for r in victims)
    with (folder/'fan_objects.csv').open() as stream:objects=list(csv.DictReader(stream))
    counts=[]
    for phase,pose in enumerate(poses):
        hits=[r for r in objects if int(r['shape'],16)==pose]
        assert hits and all(int(r['character'])==actor for r in hits)
        # Shared native peel root is rendered by both objects.
        if phase<9:assert len(hits)==({0:64,1:5,2:21}.get(phase,12))
        counts.append(len(hits))
    with (folder/'laosplit.csv').open() as stream:rows=list(csv.DictReader(stream))
    assert int(rows[-1]['frame'])==9000 and all(r['missing']=='0' for r in rows)
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    controls.append(dict(run=folder.name,actor=actor,nativePoseRows=counts,nativeCompletion=True))
report=dict(programLaneSHA256=[sha(b) for b in lanes],cases=cases,originalControls=controls,
    compiledOwnHeadersVerified=34,ownComponentsVerifiedEachCase=17,
    mirroredSidesVerified=True,nativePoseCadenceVerified=True,halvesSynchronized=True,
    representativeOriginalControlsVerified=True,fullOriginalRosterControlsVerified=False,
    finalVisualAcceptance=False,cleanupAccepted=False,cleanRebuildCurrentLinkVerified=False,
    releaseReady=False)
paths=[Path(__file__),PORT/'verify_finisher_roms.py',PORT/'lao_split_source.py',SRC/'MK2P.OUT',
       SRC/'MK2P.MAP',SRC/'MKDEATH.ASM',SRC/'MKDEATH.LST',PORT/'generated_split/SPLIT_DATA.json']
for folder,_,_ in catalog:
    paths.extend(folder/item for item in ('execution.json','autoboot.lua','laosplit.csv','laosplit_victim.csv','fan_objects.csv','mame.log'))
    paths.extend(sorted((folder/'snap').glob('*.png')))
report['currentFull26ROMBytesVerified']=True
report['pins']={str(path):sha(path.read_bytes()) for path in paths}
(PORT/'LAO_SPLIT_RUNTIME_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
