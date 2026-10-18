"""Physical Raiden lightning hits, own palette flashes and stable recovery."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from current_graphics import verify_archive_sockets
from verify_finisher_roms import verify as verify_full_rom

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
frozen=json.loads((PORT/'FROZEN_VICTIM_QUALIFICATION.json').read_text())
assert frozen['frozenVictimBehaviorVerified'] and frozen['programLaneSHA256']==[sha(data) for data in lanes]
for filename,digest in frozen['pins'].items():assert sha(Path(filename).read_bytes())==digest
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
cases=[]
names=sys.argv[1:]
assert len(names)==4 and len(set(names))==4,'Supply four explicit Kano/Sonya cases covering both victim sides'
evidence=[Path(__file__),PORT/'verify_finisher_roms.py',PORT/'FROZEN_VICTIM_QUALIFICATION.json',SRC/'MK2P.MAP']
for index,name in enumerate(names):
    assert name and Path(name).name==name and '/' not in name and '\\' not in name
    actor,label=(17,'kano') if index%2==0 else (18,'sonya')
    folder=BASE/name;receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert '--lightning-victim' in receipt['testArguments']
    assert ('--sonya' in receipt['testArguments'])==(actor==18)
    side=1 if '--mirror' in receipt['testArguments'] else 2
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        verify_full_rom(archive,receipt)
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    rows=list(csv.DictReader((folder/'freeze_palette.csv').open()))
    assert rows and all(int(row['character'])==actor and row['missing']=='0' for row in rows)
    normal=rows[0]['paletteSelector']
    flashes=[row for row in rows if row['paletteSelector']!=normal]
    assert len(flashes)==10 and len({row['paletteSelector'] for row in flashes})==1
    last=int(flashes[-1]['fight'])
    after=[row for row in rows if last+60<int(row['fight'])<last+200]
    assert after and all(row['paletteSelector']==normal and row['action']=='771' for row in after)
    poses={address for symbol,address in symbols.items() if symbol.startswith(f'ks_{label}_pose_')}
    assert all(int(row['shape'],16) in poses for row in flashes)
    trace=list(csv.DictReader((folder/'liu_bike.csv').open()))
    assert int(trace[-1]['frame'])==9000
    fight=[row for row in trace if row['mode']=='2']
    assert all(row['p1char']=='7' and int(row['p2char'])==actor for row in fight)
    assert {int(row['victimHP']) for row in fight}=={161,139}
    assert all(row['missing']=='0' and int(row['pc'],16)!=symbols['illegal_opcode']+0x50 for row in trace)
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(actor=actor,run=name,victimSide=side,nativeDamage=22,paletteFlashFields=10,
        ownBodyRetained=True,normalPaletteRestored=True,postHitStanceObserved=True))
    evidence.extend(folder/item for item in ('execution.json','autoboot.lua','liu_bike.csv','freeze_palette.csv','mame.log'))
    evidence.extend(folder/f'snap/freeze_{tick}.png' for tick in range(160,401,40))
report=dict(scope='Physical Raiden lightning hits against true added fighter IDs',cases=cases,
    programLaneSHA256=[sha(data) for data in lanes],lightningVictimBehaviorVerified=True,
    mirroredSidesVerified=all({case['victimSide'] for case in cases if case['actor']==actor}=={1,2} for actor in (17,18)),allInterruptionAndEdgeCasesVerified=False,
    releaseReady=False,fullPortVerified=False)
assert report['mirroredSidesVerified']
report['currentFull26ROMBytesVerified']=True
report['pins']={str(path):sha(path.read_bytes()) for path in evidence}
(PORT/'LIGHTNING_VICTIM_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
