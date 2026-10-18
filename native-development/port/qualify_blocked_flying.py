"""Physical blocked flying kicks; no forced health, states or inputs in RAM."""
import csv
import hashlib
import json
from pathlib import Path
import re
import zipfile
from current_graphics import verify_archive_sockets
from blocked_flying_source import NEW

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
source=(SRC/'MKREACT.ASM').read_text()
assert NEW in source
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
assert 'ks_superk_block_pick' in symbols
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
cases=[]
for actor,label,run,side in ((17,'kano','stock_blockkick_kano185',2),(18,'sonya','stock_blockkick_sonya186',2),
                            (17,'kano','stock_blockkick_kano187',1),(18,'sonya','stock_blockkick_sonya188',1)):
    folder=BASE/run;receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert '--blockkick-victim' in receipt['testArguments']
    assert ('--mirror' in receipt['testArguments'])==(side==1)
    assert ('--sonya' in receipt['testArguments'])==(actor==18)
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    # Verify the victim Block input is explicitly released each field.
    assert "'P2 High Punch','P2 Block','P2 Left'" in observer
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    rows=list(csv.DictReader((folder/'liu_bike.csv').open()))
    assert int(rows[-1]['frame'])==9000
    assert all(row['missing']=='0' and int(row['pc'],16)!=symbols['illegal_opcode']+0x50 for row in rows)
    fight=[row for row in rows if row['mode']=='2']
    # Legacy columns are normalized attacker/victim, not physical sides.
    assert all(row['p1char']=='1' and int(row['p2char'])==actor for row in fight)
    assert {int(row['victimHP']) for row in fight}=={161,154}
    active=[row for row in fight if row['action']=='515']
    assert len(active)==8
    blocked=[row for row in fight if 120<=int(row['fight'])<=240]
    assert blocked and all(row['victimAction']=='1792' for row in blocked)
    assert len({row['p2x'] for row in blocked})==1
    own={address for name,address in symbols.items() if name.startswith(f'ks_{label}_pose_')}
    assert all(int(row['victimShape'],16) in own for row in blocked)
    after=[row for row in fight if 400<int(row['fight'])<600]
    assert after and all(row['action']=='771' and row['victimAction']=='771' for row in after)
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(actor=actor,run=run,victimSide=side,chipDamage=7,
        nativeFlyingKickObserved=True,noHardBranchPushback=True,ownBlockBodyRetained=True,
        blockReleasedAndBothRecovered=True,captureSHA256=sha((folder/'snap/blockkick_140.png').read_bytes())))
report=dict(scope='One blocked Liu Kang flying kick per character and player side',cases=cases,
    programLaneSHA256=[sha(data) for data in lanes],sourceSHA256=sha((SRC/'MKREACT.ASM').read_bytes()),
    explicitOwnIDBlockResponseVerified=True,mirroredSidesVerified=True,
    originalCharacterRuntimeRegressionVerified=False,allBlockHeightsAndInterruptionsVerified=False,
    releaseReady=False,fullPortVerified=False)
(PORT/'BLOCKED_FLYING_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
