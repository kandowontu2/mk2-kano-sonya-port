"""Limited own-body deep-freeze proof; does not qualify the shatter fatality."""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import zipfile
from current_graphics import verify_archive_sockets
from superfreeze_source import NEW_STUN,NEW_ICE,NEW_LOOP

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
source=(SRC/'MKDEATH.ASM').read_text()
assert all(block in source for block in (NEW_STUN,NEW_ICE,NEW_LOOP))
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
assert 'ks_superfreeze_own_ice' in symbols
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
program=bytearray(1048576);program[::2]=lanes[0];program[1::2]=lanes[1]
cases=[]
for actor,label,run in ((17,'kano','stock_superfreeze_kano193'),(18,'sonya','stock_superfreeze_sonya194')):
    folder=BASE/run;receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert '--superfreeze-victim' in receipt['testArguments']
    assert ('--sonya' in receipt['testArguments'])==(actor==18)
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    rows=list(csv.DictReader((folder/'superfreeze.csv').open()))
    assert int(rows[-1]['frame'])==9000
    assert all(row['missing']=='0' and int(row['pc'],16)!=symbols['illegal_opcode']+0x50 for row in rows)
    fight=[row for row in rows if row['mode']=='2' and row['p1char']=='8' and int(row['p2char'])==actor]
    kos=[row for prev,row in zip(fight,fight[1:]) if int(prev['p2hp'])>0 and row['p2hp']=='0']
    assert len(kos)==2 and int(kos[1]['frame'])>int(kos[0]['frame'])
    victims=list(csv.DictReader((folder/'superfreeze_victim.csv').open()))
    assert victims and all(int(row['character'])==actor for row in victims)
    frozen=[row for row in victims if row['action']=='1558']
    assert len(frozen)==227 and int(frozen[-1]['frame'])-int(frozen[0]['frame'])==226
    pose=struct.unpack_from('<I',program,(symbols[f'ks_{label}_main_28']-0xff800000)//8)[0]
    assert all(int(row['shape'],16)==pose for row in frozen)
    final=frozen[-100:]
    assert len({row['palette'] for row in final})==1 and final[0]['palette']!=victims[0]['palette']
    assert all(row['death']=='0' for row in frozen) # Freeze alone is NOT completed shatter.
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(actor=actor,run=run,naturalKOs=2,frozenFields=227,
        ownPose=f'{pose:08x}',trueIdentityRetained=True,finalFrozenPaletteStable=True))
report=dict(scope='Two natural round wins then native deep freeze, player-two victims only',cases=cases,
    programLaneSHA256=[sha(data) for data in lanes],ownBodyFreezeVerified=True,
    mirroredSidesVerified=False,shatterFollowUpVerified=False,finalIceArtworkAccepted=False,
    originalRosterRuntimeRegressionVerified=False,releaseReady=False,fullPortVerified=False)
(PORT/'SUPERFREEZE_VICTIM_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
