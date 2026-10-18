"""Physical deep-freeze/shatter completion, not final ice-art acceptance."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from current_graphics import verify_archive_sockets
from verify_finisher_roms import verify as verify_full_rom
from superfreeze_source import NEW_STUN,NEW_ICE,NEW_LOOP,NEW_LEGS
from leg_ground_source import HELPER,OWN_LEG_EXTENT
from PIL import Image

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
death_source=(SRC/'MKDEATH.ASM').read_text()
assert death_source.count('\tcallr ks_ground_own_legs\n')==4 and HELPER in death_source
assert all(block in death_source.replace('\tcallr ks_ground_own_legs\n','') for block in (NEW_STUN,NEW_ICE,NEW_LOOP,NEW_LEGS))
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
assert 'ks_shatter_own_legs' in symbols
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
cases=[]
names=sys.argv[1:]
assert len(names)==4 and len(set(names))==4,'Supply four explicit Kano/Sonya cases covering both victim sides'
evidence=[Path(__file__),PORT/'verify_finisher_roms.py',PORT/'superfreeze_source.py',PORT/'leg_ground_source.py',
          PORT/'generated_torso/TORSO_DATA.json',SRC/'MKDEATH.ASM',SRC/'MK2P.MAP']
for index,run in enumerate(names):
    assert run and Path(run).name==run and '/' not in run and '\\' not in run
    actor,label=(17,'kano') if index%2==0 else (18,'sonya')
    side=2 if index<2 else 1
    folder=BASE/run;receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert all(flag in receipt['testArguments'] for flag in ('--superfreeze-victim','--shatter-followup'))
    assert ('--mirror' in receipt['testArguments'])==(side==1)
    assert ('--sonya' in receipt['testArguments'])==(actor==18)
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        verify_full_rom(archive,receipt)
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    rows=list(csv.DictReader((folder/'superfreeze.csv').open()))
    assert int(rows[-1]['frame'])==9000
    assert all(row['missing']=='0' and int(row['pc'],16)!=symbols['illegal_opcode']+0x50 for row in rows)
    fight=[row for row in rows if row['mode']=='2' and int(row[f'p{side}char'])==actor and row[f'p{3-side}char']=='8']
    kos=[row for prev,row in zip(fight,fight[1:]) if int(prev[f'p{side}hp'])>0 and row[f'p{side}hp']=='0']
    assert len(kos)==2
    victims=list(csv.DictReader((folder/'superfreeze_victim.csv').open()))
    assert victims and all(int(row['character'])==actor for row in victims)
    frozen=[row for row in victims if row['action']=='1558']
    assert 130<=len(frozen)<=150
    assert all(int(row['frame'])>int(kos[-1]['frame']) for row in frozen)
    own={address for name,address in symbols.items() if name.startswith(f'ks_{label}_pose_')}
    assert all(int(row['shape'],16) in own for row in frozen)
    started=[row for row in victims if row['death']=='2'];done=[row for row in victims if row['death']=='65535']
    assert len(started)==65 and len(done)==1
    assert int(done[0]['frame'])==int(started[-1]['frame'])+1
    legs=symbols[f'ks_tr_{label}_pose6']
    legrows=[row for row in started if int(row['shape'],16)==legs]
    assert len(legrows)>=30 and int(done[0]['shape'],16)==legs
    record=json.loads((PORT/'generated_torso/TORSO_DATA.json').read_text())['records'][label][6]
    leg_path=PORT/'assets/torso'/record['file']
    assert sha(leg_path.read_bytes())==record['fileSHA256']
    with Image.open(leg_path) as image:bounds=image.getbbox()
    assert bounds is not None and bounds[3]-record['yOffset']==OWN_LEG_EXTENT
    byframe={int(row['frame']):row for row in rows}
    for sample in [*legrows,done[0]]:
        main=byframe[int(sample['frame'])]
        assert main[f'p{side}shape']==sample['shape']
        assert int(main[f'p{side}y'])+OWN_LEG_EXTENT==int(main['ground'])
    assert not list(folder.glob('*fault*'))
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(actor=actor,run=run,victimSide=side,naturalKOs=2,frozenFields=len(frozen),
        nativeFatalityFields=len(started),nativeCompletionFrame=int(done[0]['frame']),
        ownLegs=f'{legs:08x}',ownLegsFields=len(legrows),trueIdentityRetained=True,
        ownLegOpaqueGroundDelta=0))
    evidence.append(leg_path)
    evidence.extend(folder/item for item in ('execution.json','autoboot.lua','superfreeze.csv','superfreeze_victim.csv','mame.log'))
    captures=list((folder/'snap').glob('superfreeze_*.png'))
    assert captures,'Missing sampled finisher captures'
    evidence.extend(captures)
report=dict(scope='Two physical round wins, deep freeze and shatter on both player sides',cases=cases,
    programLaneSHA256=[sha(data) for data in lanes],nativeShatterCompletionVerified=True,
    mirroredSidesVerified=True,finalIceArtworkAccepted=False,originalRosterRuntimeRegressionVerified=False,
    allTimingAndInterruptionCasesVerified=False,releaseReady=False,fullPortVerified=False)
report['currentFull26ROMBytesVerified']=True
report['pins']={str(path):sha(path.read_bytes()) for path in evidence}
(PORT/'SHATTER_VICTIM_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
