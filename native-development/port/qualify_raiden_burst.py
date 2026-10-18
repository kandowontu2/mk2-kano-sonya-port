"""Physical Raiden explosion and late-render capture evidence, not full QA."""
import csv
import json
import re
import sys
import zipfile
from pathlib import Path
from build_inflation_assets import sha
from current_graphics import verify_archive_sockets
from verify_finisher_roms import verify

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
cases=[]
names=sys.argv[1:]
assert len(names) in (2,4) and len(set(names))==len(names), 'Supply explicit distinct current runs'
for index,name in enumerate(names):
    assert name and Path(name).name==name and '/' not in name and '\\' not in name
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    actor,label=(18,'sonya') if '--sonya' in receipt['testArguments'] else (17,'kano')
    assert not any(a.startswith('--raiden-burst-control=') for a in receipt['testArguments'])
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert '--raiden-burst-victim' in receipt['testArguments']
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        verify(archive,receipt)
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    with (folder/'raidenburst.csv').open() as stream:rows=list(csv.DictReader(stream))
    assert int(rows[-1]['frame'])==9000
    assert all(r['missing']=='0' and int(r['pc'],16)!=symbols['illegal_opcode']+0x50 for r in rows)
    side=1 if '--mirror' in receipt['testArguments'] else 2
    fight=[r for r in rows if r['mode']=='2' and r[f'p{3-side}char']=='7' and int(r[f'p{side}char'])==actor]
    assert len([b for a,b in zip(fight,fight[1:]) if int(a[f'p{side}hp'])>0 and b[f'p{side}hp']=='0'])==2
    with (folder/'raidenburst_victim.csv').open() as stream:victims=list(csv.DictReader(stream))
    assert all(int(r['character'])==actor for r in victims)
    active=[r for r in victims if r['death']=='2']
    assert len(active)==166 and victims[-1]['death']=='65535'
    assert any(int(r['flags'])&0x20 for r in active)
    completion=int(victims[-1]['frame'])
    captures={}
    for age in (60,120,180,240,320,400):
        files=list((folder/'snap').glob(f'raiden_age{age}_*.png'))
        assert len(files)==1
        frame=int(files[0].stem.rsplit('_',1)[1])
        assert frame==int(active[0]['frame'])+age
        captures[str(age)]=dict(file=files[0].name,SHA256=sha(files[0].read_bytes()),
            afterCompletionFlag=frame>completion)
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    with (folder/'fan_objects.csv').open() as stream:heads=list(csv.DictReader(stream))
    assert heads and len({r['object'] for r in heads})==1
    assert all(int(r['character'])==actor and r['missing']=='0' for r in heads)
    assert int(heads[0]['frame'])>completion
    for phase in range(7):
        assert any(int(r['image'],16)==symbols[f'ks_hd_{label}_frame{phase}'] for r in heads)
    signed=lambda value:value-65536 if value>=32768 else value
    ys=[signed(int(r['y'])) for r in heads]
    floor=int(next(r['ground'] for r in fight if r['death']=='2'))-20
    assert ys[0]<0 and max(ys)==floor and ys[-1]==floor
    landings=sum(a<floor and b==floor for a,b in zip(ys,ys[1:]))
    cases.append(dict(actor=actor,run=name,victimSide=side,fields=9000,naturalKOs=2,nativeFatalityFields=166,
        headObjectCount=1,ownHeadFramesObserved=7,headLandingCount=landings,
        fourCoordinateContactsObserved=landings==4,
        headTraceSHA256=sha((folder/'fan_objects.csv').read_bytes()),
        nativeCompletionObserved=True,lateHeadVisibleInReviewedAge240Capture=False,
        captures=captures))
assert {c['actor'] for c in cases}=={17,18}
assert len({(c['actor'],c['victimSide']) for c in cases})==len(cases)
report=dict(scope='Raiden explosion and delayed own-head identity/frame coverage; raw contacts measured, not invocation count',
    programLaneSHA256=[sha(v) for v in lanes],cases=cases,
    effectsContinueAfterNativeCompletionFlag=True,
    mirroredSidesVerified=all({c['victimSide'] for c in cases if c['actor']==actor}=={1,2} for actor in (17,18)),
    originalRosterControlsVerified=False,completeHeadTrajectoryVerified=False,
    finalVisualAcceptance=False,releaseReady=False)
paths=[Path(__file__),PORT/'verify_finisher_roms.py',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
       SRC/'MKDEATH.ASM',SRC/'MKDISP.ASM']
for name in names:
    folder=BASE/name
    paths.extend(folder/item for item in ('execution.json','autoboot.lua','raidenburst.csv','raidenburst_victim.csv','fan_objects.csv','mame.log'))
    paths.extend(sorted((folder/'snap').glob('*.png')))
report['currentFull26ROMBytesVerified']=True
report['pins']={str(path):sha(path.read_bytes()) for path in paths}
(PORT/'RAIDEN_BURST_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
