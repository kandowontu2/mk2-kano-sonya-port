"""Bounded own ingestion frames and native completion, not full visual QA."""
import csv
import json
import re
import struct
import sys
import zipfile
from pathlib import Path
from build_inflation_assets import sha, unpack6
from build_arm_rip_assets import read_pgm
from current_graphics import verify_archive_sockets
from ingestion_source import NEW
from verify_finisher_roms import verify

PORT = Path(__file__).resolve().parent
BASE = PORT.parent/'baseline'
SRC = BASE/'mk2-rebuild-main/srcp'
assert NEW in (SRC/'MKDIE.ASM').read_text()
symbols = {n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',
            (SRC/'MK2P.MAP').read_text())}
lanes = [b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
program = bytearray(1048576)
program[::2],program[1::2] = lanes
folder = PORT/'generated_ingestion'
art = json.loads((folder/'INGESTION_DATA.json').read_text())
packed = (folder/'fighter_ui_finish_ingest_graphics.bin').read_bytes()
assert sha(packed)==art['packedSHA256']
for frame in art['frames']:
    address = symbols[frame['imageLabel']]
    header = struct.unpack_from('<HHhhIHI',program,(address-0xff800000)//8)
    assert header == (frame['width'],frame['height'],frame['xOffset'],frame['yOffset'],
        (0xc00000+frame['packedByteOffset'])*8,0x6000,symbols[f'ks_{frame["actor"]}_primary_palette'])
    w,h,indices = read_pgm(PORT/'assets/ingestion'/frame['file'])
    at = frame['packedByteOffset']
    assert unpack6(packed[at:at+frame['packedBytes']],w*h)==indices
names = sys.argv[1:]
assert len(names) in (2,4) and len(set(names))==len(names), 'Supply explicit distinct current runs'
cases = []
for index,name in enumerate(names):
    assert name and Path(name).name==name and '/' not in name and '\\' not in name
    folder = BASE/name
    receipt = json.loads((folder/'execution.json').read_text())
    actor,label = (18,'sonya') if '--sonya' in receipt['testArguments'] else (17,'kano')
    assert not any(arg.startswith('--ingestion-control=') for arg in receipt['testArguments'])
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert '--body-suck-victim' in receipt['testArguments']
    observer = (folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        verify(archive,receipt)
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
            assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    with (folder/'bodysuck.csv').open() as stream:rows=list(csv.DictReader(stream))
    assert int(rows[-1]['frame'])==9000
    assert all(r['missing']=='0' and int(r['pc'],16)!=symbols['illegal_opcode']+0x50 for r in rows)
    side=1 if '--mirror' in receipt['testArguments'] else 2
    fight=[r for r in rows if r['mode']=='2' and int(r[f'p{side}char'])==actor and r[f'p{3-side}char']=='5']
    assert len([b for a,b in zip(fight,fight[1:]) if int(a[f'p{side}hp'])>0 and b[f'p{side}hp']=='0'])==2
    with (folder/'bodysuck_victim.csv').open() as stream:victims=list(csv.DictReader(stream))
    assert victims and all(int(r['character'])==actor for r in victims)
    active=[r for r in victims if r['death']=='2']
    assert active and victims[-1]['death']=='65535'
    coverage=[]
    for phase in range(8):
        hits=[r for r in active if int(r['shape'],16)==symbols[f'ks_ing_{label}_pose{phase}']]
        assert len(hits)>=4
        coverage.append(len(hits))
    assert all(0xff800000<=int(r['shape'],16)<0xffffffff for r in victims)
    assert any(int(r['flags'])&0x20 for r in active)
    assert not list(folder.glob('*fault*')) and '[LUA ERROR]' not in (folder/'mame.log').read_text()
    captures={}
    for phase in range(8):
        files=list((folder/'snap').glob(f'ingest_phase{phase}_*.png'))
        assert len(files)==1
        captures[files[0].name]=sha(files[0].read_bytes())
    cases.append(dict(actor=actor,run=name,victimSide=side,naturalKOs=2,fields=9000,
        ownPoseRows=coverage,nativeFatalityFields=len(active),nativeDisappearanceAndCompletion=True,
        trueIdentityRetained=True,captures=captures))
assert {c['actor'] for c in cases}=={17,18}, 'Both added victims required'
assert len({(c['actor'],c['victimSide']) for c in cases})==len(cases), 'Duplicate victim/side'
rebuilt=json.loads((PORT/'REBUILT_ROM_SET_QUALIFICATION.json').read_text())
clean_current=rebuilt['allRebuiltROMBytesMatchRuntimeInput'] and all(
    rebuilt['chipSHA256'][chip]==sha(lanes[lane])
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')))
report=dict(scope='Own eight-pose ingestion and native disappearance/completion',
    programLaneSHA256=[sha(data) for data in lanes],cases=cases,compiledHeadersVerified=16,
    allSixBitPixelsMatchEditableSources=True,
    mirroredSidesVerified=all({c['victimSide'] for c in cases if c['actor']==actor}=={1,2} for actor in (17,18)),
    originalRosterControlsVerified=False,finalMouthAlignmentAccepted=False,
    cleanRebuildCurrentLinkVerified=clean_current,bodySuckFullyAccepted=False,releaseReady=False)
evidence=[Path(__file__),PORT/'verify_finisher_roms.py',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
          SRC/'MKDIE.ASM',SRC/'KSINART.ASM',PORT/'ingestion_source.py',
          PORT/'generated_ingestion/INGESTION_DATA.json',
          PORT/'generated_ingestion/fighter_ui_finish_ingest_graphics.bin']
for name in names:
    run=BASE/name
    evidence.extend(run/item for item in ('execution.json','autoboot.lua','bodysuck.csv',
                                         'bodysuck_victim.csv','mame.log'))
report['currentFull26ROMBytesVerified']=True
report['pins']={str(path):sha(path.read_bytes()) for path in evidence}
(PORT/'INGESTION_RUNTIME_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
