"""Representative original-roster controls on the same own-port ROM link."""
import csv
import hashlib
import json
from pathlib import Path
import re
import zipfile
from current_graphics import verify_archive_sockets

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
own_poses={address for name,address in symbols.items() if name.startswith('ks_') and 'pose' in name}
cases=[]
for actor,run,side in ((1,'stock_arms_liu237',2),(1,'stock_arms_liu238',1),
                       (5,'stock_arms_mileena239',2),(5,'stock_arms_mileena240',1)):
    folder=BASE/run;receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert '--arms-victim' in receipt['testArguments']
    assert ('--mirror' in receipt['testArguments'])==(side==1)
    assert ('--stock-victim' in receipt['testArguments'])==(actor==1)
    if actor==5:assert '--arms-control=5' in receipt['testArguments']
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    rows=list(csv.DictReader((folder/'arms.csv').open()))
    assert int(rows[-1]['frame'])==9000
    assert all(row['missing']=='0' and int(row['pc'],16)!=symbols['illegal_opcode']+0x50 for row in rows)
    fight=[row for row in rows if row['mode']=='2' and int(row[f'p{side}char'])==actor and row[f'p{3-side}char']=='11']
    kos=[row for prev,row in zip(fight,fight[1:]) if int(prev[f'p{side}hp'])>0 and row[f'p{side}hp']=='0']
    assert len(kos)==2
    victims=list(csv.DictReader((folder/'arms_victim.csv').open()))
    assert victims and all(int(row['character'])==actor for row in victims)
    assert all(int(row['shape'],16) not in own_poses for row in victims)
    active=[row for row in victims if row['death']=='2'];done=[row for row in victims if row['death']=='65535']
    assert len(active)==147 and len(done)==1
    assert int(done[0]['frame'])==int(active[-1]['frame'])+1
    assert not list(folder.glob('*fault*')) and '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(actor=actor,run=run,victimSide=side,naturalKOs=2,nativeArmRipFields=147,
        completionFrame=int(done[0]['frame']),trueOriginalIDRetained=True,noOwnVictimPoseSubstitution=True))
report=dict(scope='Original Liu Kang and Mileena arm-rip controls on both physical sides',cases=cases,
    programLaneSHA256=[sha(data) for data in lanes],representativeOriginalArmRipControlsVerified=True,
    mirroredSidesVerified=True,allOriginalCharactersVerified=False,allOriginalMovesVerified=False,
    originalPalettePixelAcceptance=False,releaseReady=False,fullPortVerified=False)
(PORT/'ARM_RIP_ORIGINAL_CONTROLS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
