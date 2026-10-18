"""Physical charged-HP Raiden shock against both true added fighters."""
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
from shocker_alignment_source import ENTRIES

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline';SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
program=bytearray(1048576);program[::2]=lanes[0];program[1::2]=lanes[1]
table=struct.unpack_from('<19I',program,(symbols['shocker_info']-0xff800000)//8)
assert table[:17]==(0x2303c0e0,0x2303bce0,0x2300c8e0,0x2304c8e0,0x2301c0e0,0x2301c0e0,
    0x2300c0e0,0x2301c0e0,0x2301b8e0,0x2301b8e0,0x2301b8e0,0x2305c0e0,
    0x2301d0e0,0x2301d0e0,0x2301d0e0,0x2301d0e0,0x2301d0e0)
assert table[17:]==ENTRIES
cases=[]
names=sys.argv[1:]
assert len(names)==4 and len(set(names))==4,'Supply Kano/Sonya victim-side2, then Kano/Sonya victim-side1 cases'
evidence=[Path(__file__),PORT/'verify_finisher_roms.py',PORT/'shocker_alignment_source.py',SRC/'MK2P.MAP']
for (actor,label,side),run in zip(((17,'kano',2),(18,'sonya',2),(17,'kano',1),(18,'sonya',1)),names):
    assert run and Path(run).name==run and '/' not in run and '\\' not in run
    folder=BASE/run;receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert '--shock-victim' in receipt['testArguments']
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
    # Probe columns are normalized attacker/victim, not physical sides.
    assert all(row['p1char']=='7' and int(row['p2char'])==actor for row in fight)
    assert {int(row['victimHP']) for row in fight}=={161,129}
    active=[row for row in fight if row['action']=='1027']
    assert len(active)==99 and int(active[-1]['fight'])-int(active[0]['fight'])==98
    after=[row for row in fight if 400<int(row['fight'])<600]
    assert after and all(row['action']=='771' and row['victimAction']=='771' for row in after)
    palettes=list(csv.DictReader((folder/'freeze_palette.csv').open()))
    assert all(int(row['character'])==actor and row['missing']=='0' for row in palettes)
    normal=palettes[0]['paletteSelector']
    flashes=[row for row in palettes if row['paletteSelector']!=normal]
    assert len(flashes)==48 and len({row['paletteSelector'] for row in flashes})==1
    poses={address for symbol,address in symbols.items() if symbol.startswith(f'ks_{label}_pose_')}
    assert all(int(row['shape'],16) in poses for row in flashes)
    assert all(row['paletteSelector']==normal for row in palettes if 400<int(row['fight'])<600)
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(actor=actor,run=run,victimSide=side,damage=32,attackerActiveFields=99,
        frozenPaletteFlashFields=48,ownBodyRetained=True,bothRecoveredToStance=True,
        screenshotSHA256=sha((folder/'snap/shock_200.png').read_bytes())))
    evidence.extend(folder/item for item in ('execution.json','autoboot.lua','liu_bike.csv','freeze_palette.csv','mame.log'))
    evidence.extend(folder/f'snap/shock_{tick}.png' for tick in range(170,331,10))
report=dict(scope='One physical close shock per added fighter on each player side',cases=cases,
    programLaneSHA256=[sha(data) for data in lanes],compiledEntries=[f'{entry:08x}' for entry in table],
    nativeDamagePaletteAndRecoveryVerified=True,mirroredSidesVerified=True,
    allLineupsInterruptionsAndEdgeCasesVerified=False,visualLineupAccepted=False,
    releaseReady=False,fullPortVerified=False)
report['currentFull26ROMBytesVerified']=True
report['pins']={str(path):sha(path.read_bytes()) for path in evidence}
(PORT/'SHOCKER_VICTIM_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
