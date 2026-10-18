"""Compare raw head contacts to native controls; do not infer physics from counts."""
import csv
import json
import re
import struct
import zipfile
from pathlib import Path
from build_inflation_assets import sha
from current_graphics import verify_archive_sockets

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
program=bytearray(1048576)
program[::2],program[1::2]=lanes


def pointer(address):
    return struct.unpack_from('<I',program,(address-0xff800000)//8)[0]


def block(text,start,end):
    found=re.search(r'(?ms)^'+start+r'\b(.*?)^'+end+r'\b',text)
    assert found
    return found[0]


def canonical(text):
    return [' '.join(line.split(';',1)[0].split()) for line in text.splitlines()
            if line.split(';',1)[0].strip() and not line.lstrip().startswith('*')]


source_blocks=[]
with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as original:
    for filename,start,end in (('MKDIE.ASM','head_grav','exp_burst'),('MKDISP.ASM','anig1','anigx')):
        key=next(n for n in original.namelist() if n.lower().endswith('/src/'+filename.lower()))
        before=block(original.read(key).decode('cp437'),start,end)
        current=block((SRC/filename).read_text(),start,end)
        assert canonical(before)==canonical(current)
        source_blocks.append(dict(file=filename,start=start,end=end,
            currentBlockSHA256=sha(current.encode()),originalInstructionsPreserved=True))
cases=[]
for actor,name in ((17,'stock_raiden_head_kano287'),(18,'stock_raiden_head_sonya288'),
                   (17,'stock_raiden_head_mirror_kano289'),(18,'stock_raiden_head_mirror_sonya290'),
                   (1,'stock_raiden_control_liu291'),(4,'stock_raiden_control_kitana292')):
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    with (folder/'fan_objects.csv').open() as stream:heads=list(csv.DictReader(stream))
    with (folder/'raidenburst.csv').open() as stream:rows=list(csv.DictReader(stream))
    assert int(rows[-1]['frame'])==9000
    assert all(r['missing']=='0' and int(r['pc'],16)!=symbols['illegal_opcode']+0x50 for r in rows)
    side=1 if '--mirror' in receipt['testArguments'] else 2
    fight=[r for r in rows if r['mode']=='2' and int(r[f'p{side}char'])==actor and r[f'p{3-side}char']=='7']
    assert len([b for a,b in zip(fight,fight[1:]) if int(a[f'p{side}hp'])>0 and b[f'p{side}hp']=='0'])==2
    assert len([r for r in fight if r['death']=='2'])==166
    assert heads and len({r['object'] for r in heads})==1
    assert all(int(r['character'])==actor and r['missing']=='0' for r in heads)
    root=pointer(symbols['character_anitabs1']+actor*32)
    script=pointer(root+0x3d*32)
    images=[pointer(script+i*32) for i in range(7)]
    assert {int(r['image'],16) for r in heads}==set(images)
    headers=[struct.unpack_from('<HHhh',program,(image-0xff800000)//8) for image in images]
    ys=[int(r['y'])-65536 if int(r['y'])>=32768 else int(r['y']) for r in heads]
    floor=int(next(r['ground'] for r in rows if r['death']=='2'))-20
    assert ys[0]<0 and max(ys)==floor and ys[-1]==floor
    contacts=sum(a<floor and b==floor for a,b in zip(ys,ys[1:]))
    assert contacts==(4 if actor in (1,17) else 3)
    cases.append(dict(actor=actor,run=name,rawCoordinateContacts=contacts,
        headFrames=7,headerYOffsets=[h[3] for h in headers],finalY=floor,
        traceSHA256=sha((folder/'fan_objects.csv').read_bytes())))
report=dict(scope='Raw coordinate contact difference also occurs in original Liu/Kitana controls',
    programLaneSHA256=[sha(v) for v in lanes],cases=cases,sourceBlocks=source_blocks,
    nativeHeadPhysicsAndAnimationAdjustmentInstructionsPreserved=True,
    rawContactDifferenceNotUniqueToPort=True,
    rawContactCountIsNotProofOfSubroutineInvocationCount=True,
    nativePhysicsChangeJustifiedByTheseCounts=False,
    fullTrajectoryPixelAcceptance=False,releaseReady=False)
(PORT/'HEAD_CONTACT_COMPARISON.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('cases','sourceBlocks')},indent=2))
