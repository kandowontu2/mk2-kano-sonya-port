"""Finite original-Liu controls for the gated detached-leg helper."""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import zipfile
from verify_finisher_roms import verify
from fresh_victim_match import verify_folder
from native_lk_poses import resolve

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest().upper()
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
poses=resolve(symbols,(SRC/'MKLK.LST').read_text())
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in (0,1)]
program=bytearray(1048576);program[::2]=lanes[0];program[1::2]=lanes[1]
for slot,label in ((57,'a_torso_ripped'),(65,'a_swipe_torso')):
    assert struct.unpack_from('<I',program,(symbols['lk_anitab1']-0xff800000)//8+slot*4)[0]==poses[label]
names=sys.argv[1:];assert len(names)==len(set(names))==4
cases=[]
for name in names:
    assert name and Path(name).name==name and '/' not in name and '\\' not in name
    folder=BASE/name;receipt=json.loads((folder/'execution.json').read_text())
    args=receipt['testArguments'];swipe='--swipe-victim' in args
    assert '--stock-victim' in args and '--finisher-rejoin' in args
    assert swipe != ('--torso-victim' in args) and '--sonya' not in args
    assert receipt['exitCode']==0 and not receipt['timedOut'] and not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert sha(folder/'autoboot.lua')==receipt['controllerSHA256']
    observer=(folder/'autoboot.lua').read_text();assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:verify(archive,receipt)
    rows=list(csv.DictReader((folder/'fan.csv').open()));objects=list(csv.DictReader((folder/'fan_objects.csv').open()))
    side=2 if '--mirror' in args else 1;owner=f'p{side}';victim=f'p{3-side}';actor=10 if swipe else 2
    active=min(int(row['frame']) for row in rows if row['death']==('2' if swipe else '1'))
    fight=[row for row in rows if row['mode']=='2' and int(row['frame'])<=active]
    assert fight and all(row[owner+'char']==str(actor) and row[victim+'char']=='1' for row in fight)
    kos=[row for previous,row in zip(fight,fight[1:]) if int(previous[victim+'hp'])>0 and row[victim+'hp']=='0'];assert len(kos)==2
    assert objects and all(row['character']=='1' and row['missing']=='0' for row in objects)
    legs=[row for row in objects if int(row['shape'],16)==poses['LKDEADLEG1']]
    upper=[row for row in objects if int(row['shape'],16)==poses['LKRIPTORSO6']]
    assert len(legs)>=200 and len(upper)>=200
    assert len({(row['object'],row['x'],row['y']) for row in legs})==1
    assert any(row['death']=='65535' for row in legs) and all(row['missing']=='0' for row in rows)
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    fresh=verify_folder(folder,rows,side,actor,1)
    evidence=[Path(__file__),PORT/'native_lk_poses.py',PORT/'fresh_victim_match.py',PORT/'verify_finisher_roms.py',
              SRC/'MKLK.LST',SRC/'MKLK.ASM',SRC/'MK2P.MAP',SRC/'MKDEATH.ASM']
    evidence.extend(folder/item for item in ('execution.json','autoboot.lua','fan.csv','fan_objects.csv','finisher_rejoin_events.csv','finisher_cleanup.csv','mame.log'))
    evidence.extend((folder/'snap').glob('fan_*.png'))
    cases.append(dict(run=name,performer=actor,performerSide=side,victim=1,legObservations=len(legs),upperObservations=len(upper),
                      originalLegY=int(legs[0]['y']),**fresh,pins={str(path):sha(path) for path in evidence}))
assert {(case['performer'],case['performerSide']) for case in cases}=={(actor,side) for actor in (2,10) for side in (1,2)}
report=dict(scope='Cage/Scorpion fatalities against original Liu, both sides, current-ROM finite controls',
    cases=cases,allFourFiniteOriginalControlsPassed=True,allOriginalFightersAndGoroVerified=False,fullPortVerified=False,releaseReady=False)
(PORT/'ORIGINAL_TORSO_CONTROL_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({key:value for key,value in report.items() if key!='cases'},indent=2))
