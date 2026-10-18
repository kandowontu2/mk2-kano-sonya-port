"""Native frozen palette table and physical Sub-Zero victim checks."""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
from current_graphics import verify_archive_sockets
from verify_finisher_roms import verify as verify_full_rom
import zipfile

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
program=bytearray(1048576);program[::2]=lanes[0];program[1::2]=lanes[1]
offset=lambda address:(address-0xff800000)//8
entries=struct.unpack_from('<19I',program,offset(symbols['ochar_froze_pals']))
results=[]
names=sys.argv[1:]
assert len(names)==4 and len(set(names))==4,'Supply four explicit Kano/Sonya cases covering both victim sides'
evidence=[Path(__file__),PORT/'verify_finisher_roms.py',SRC/'MK2P.MAP',PORT/'generated_frozen/KSICEPAL.ASM']
for index,run in enumerate(names):
    assert run and Path(run).name==run and '/' not in run and '\\' not in run
    actor,label=(17,'kano') if index%2==0 else (18,'sonya')
    expected=symbols[f'ks_{label}_frozen_palette'];assert entries[actor]==expected
    count=struct.unpack_from('<H',program,offset(expected))[0];assert count==65
    colors=struct.unpack_from('<65H',program,offset(expected)+2);assert colors[0]==0
    assert all(value==0 or (value&31)>=(value>>5&31)>=(value>>10&31) for value in colors)
    folder=BASE/run;receipt=json.loads((folder/'execution.json').read_text())
    assert ('--sonya' in receipt['testArguments'])==(actor==18)
    assert '--freeze-victim' in receipt['testArguments']
    side=1 if '--mirror' in receipt['testArguments'] else 2
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
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
    # The probe's legacy p1/p2 columns normalize attacker/victim in mirrors.
    assert fight and all(row['p1char']=='8' and int(row['p2char'])==actor for row in fight)
    rows=list(csv.DictReader((folder/'freeze_palette.csv').open()))
    assert rows and all(int(row['character'])==actor and row['missing']=='0' for row in rows)
    frozen=[row for row in rows if row['action']=='1025'];assert len(frozen)==160
    first,last=int(frozen[0]['fight']),int(frozen[-1]['fight'])
    assert last-first+1==len(frozen)
    before=[row for row in rows if int(row['fight'])<first]
    after=[row for row in rows if last<int(row['fight'])<last+80]
    assert before and after and all(row['action']=='771' for row in after)
    normal=before[-1]['paletteSelector'];assert {row['paletteSelector'] for row in after}=={normal}
    assert len({row['paletteSelector'] for row in frozen})==1 and frozen[0]['paletteSelector']!=normal
    poses={address for name,address in symbols.items() if name.startswith(f'ks_{label}_pose_')}
    assert all(int(row['shape'],16) in poses for row in frozen)
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    results.append(dict(actor=actor,run=run,victimSide=side,compiledPaletteAddress=f'{expected:08x}',
        frozenFields=160,ownBodyRetained=True,paletteChangedAndRestored=True,nativeThawToStance=True))
    evidence.extend(folder/item for item in ('execution.json','autoboot.lua','liu_bike.csv','freeze_palette.csv','mame.log'))
    evidence.extend(folder/f'snap/freeze_{tick}.png' for tick in range(160,401,40))
both_sides=all({case['victimSide'] for case in results if case['actor']==actor}=={1,2} for actor in (17,18))
assert both_sides,'Both own characters must be tested on both victim sides'
report=dict(scope='Native frozen table IDs17/18 and physical Sub-Zero ice hits',cases=results,
    programLaneSHA256=[sha(data) for data in lanes],sourceSHA256=sha((PORT/'generated_frozen/KSICEPAL.ASM').read_bytes()),
    frozenVictimBehaviorVerified=True,lightningCoveredByThisTest=False,mirroredSidesVerified=both_sides,
    visualTintAccepted=False,allCharacterTablesSafe=False,releaseReady=False,fullPortVerified=False)
report['currentFull26ROMBytesVerified']=True
report['pins']={str(path):sha(path.read_bytes()) for path in evidence}
(PORT/'FROZEN_VICTIM_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
