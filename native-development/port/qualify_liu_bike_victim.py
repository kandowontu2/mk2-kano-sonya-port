"""Finite physical-input proof of native Liu Bicycle Kick victim scripts."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from verify_finisher_roms import verify as verify_full_rom

PORT = Path(__file__).resolve().parent
BASE = PORT.parent / 'baseline'
mapping = (BASE / 'mk2-rebuild-main/srcp/MK2P.MAP').read_text()
def symbol(name):
    matches = re.findall(r'\b([0-9a-f]{8})\s+' + re.escape(name) + r'\b', mapping, re.I)
    assert matches, name
    return int(matches[0], 16)

illegal_opcode_recovery=symbol('illegal_opcode')+0x50
names=sys.argv[1:]
assert len(names)==4 and len(set(names))==4,'Supply four explicit own-victim cases covering both sides'
cases=[]
for argument in names:
    assert argument and Path(argument).name==argument and '/' not in argument and '\\' not in argument
    folder = BASE / argument
    rows = list(csv.DictReader((folder / 'liu_bike.csv').open()))
    receipt = json.loads((folder / 'execution.json').read_text())
    assert receipt['exitCode'] == 0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert '--liu-bike-victim' in receipt['testArguments']
    observer=(folder/'autoboot.lua').read_bytes()
    assert hashlib.sha256(observer).hexdigest().upper()==receipt['controllerSHA256']
    assert b':write_u' not in observer and not re.search(rb'\.value\s*=(?!=)',observer)
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:verify_full_rom(archive,receipt)
    assert len(rows) == 9000
    assert all(int(r['missing']) == 0 for r in rows)
    combat = [r for r in rows if int(r['fight']) > 0 and int(r['mode']) == 2]
    target = int(combat[0]['p2char'])
    assert target in (17, 18)
    assert ('--sonya' in receipt['testArguments'])==(target==18)
    assert all(int(r['p1char']) == 1 and int(r['p2char']) == target for r in combat)
    actor = 'kano' if target == 17 else 'sonya'
    sources = ('ff8294a0','ff829500','ff829560','ff829620','ff829680') if target == 17 else ('ff836860','ff8368c0','ff836920','ff8369c0','ff836a00')
    poses = [symbol(f'ks_{actor}_pose_{v}') for v in sources]
    root = symbol(f'ks_{actor}_bike_victim')
    active = [r for r in combat if int(r['action']) == 0x204]
    assert active
    observed = {int(r['victimShape'], 16) for r in active}
    assert set(poses) <= observed
    assert any(root <= int(r['savedA11'], 16) <= root + 5 * 32 for r in active)
    assert min(int(r['victimHP']) for r in active) < int(combat[0]['victimHP'])
    after=[r for r in combat if int(active[-1]['fight'])+120<int(r['fight'])<int(active[-1]['fight'])+220]
    assert len(after)==99 and all(r['action']==r['victimAction']=='771' for r in after)
    assert all(int(r['pc'],16)!=illegal_opcode_recovery for r in rows)
    # Pin the exact native program used by this trace, not merely today's map.
    for lane, chip in ((0, 'mk321u54.bin'), (1, 'mk321u63.bin')):
        data = b''.join((BASE / f'mk2-rebuild-main/srcp/rom/P12{part}.{lane}').read_bytes() for part in ('F8', 'FC'))
        assert hashlib.sha256(data).hexdigest().upper() == receipt['replacementChips'][chip]
    result = {'qualified': True, 'scope': 'Physical charged LK release; native five-pose loop and recovery only',
              'liuPlayer': 2 if '--mirror' in receipt['testArguments'] else 1,
              'victim': actor, 'frames': len(rows), 'nativeBikeActionFields': len(active), 'ownPosesObserved': len(set(poses) & observed),
              'missingMarkers': 0, 'fullPortVerified': False,'currentFull26ROMBytesVerified':True,
              'bothRecoveredToStanceFields':len(after)}
    evidence=[Path(__file__),PORT/'verify_finisher_roms.py',BASE/'mk2-rebuild-main/srcp/MK2P.MAP']
    evidence.extend(folder/item for item in ('execution.json','autoboot.lua','liu_bike.csv','mame.log'))
    evidence.extend(folder/f'snap/liu_bike_{tick}.png' for tick in (260,290,330))
    result['pins']={str(path):hashlib.sha256(path.read_bytes()).hexdigest().upper() for path in evidence}
    (folder / 'liu_bike_qualification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
    cases.append(dict(run=argument,actor=target,victimSide=3-result['liuPlayer'],
                      qualificationSHA256=hashlib.sha256((folder/'liu_bike_qualification.json').read_bytes()).hexdigest().upper()))
assert {(case['actor'],case['victimSide']) for case in cases}=={(actor,side) for actor in (17,18) for side in (1,2)}
(PORT/'LIU_BIKE_VICTIM_QUALIFICATION.json').write_text(json.dumps(dict(cases=cases,
    allFourFiniteCasesPassed=True,currentFull26ROMBytesVerified=True,fullPortVerified=False,releaseReady=False,
    verifierSHA256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest().upper()),indent=2)+'\n')
