"""Pin physical Mileena body-suck failures; never qualify completion alone."""
import csv
import json
import re
import zipfile
from pathlib import Path
from build_inflation_assets import sha
from current_graphics import verify_archive_sockets
from inventory_character_tables import source_tables

PORT = Path(__file__).resolve().parent
BASE = PORT.parent/'baseline'
SRC = BASE/'mk2-rebuild-main/srcp'
table = source_tables((SRC/'MKDIE.ASM').read_text())['sucked_in_anis']
assert sum(len(r['values']) for r in table['rows']) == 12
symbols = {n: int(a, 16) for a, n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',
            (SRC/'MK2P.MAP').read_text())}
lanes = [b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes()
                 for part in ('F8', 'FC')) for lane in range(2)]
cases = []
for actor, run in ((17, 'stock_body_suck_charge_kano263'), (18, 'stock_body_suck_charge_sonya264')):
    folder = BASE/run
    receipt = json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode'] == 0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256'] == 'AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert sha((folder/'autoboot.lua').read_bytes()) == receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane, chip in enumerate(('mk321u54.bin', 'mk321u63.bin')):
            assert archive.read(chip) == lanes[lane]
        verify_archive_sockets(archive)
    with (folder/'bodysuck.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    fight = [r for r in rows if r['mode'] == '2' and r['p1char'] == '5' and int(r['p2char']) == actor]
    assert len([b for a, b in zip(fight, fight[1:]) if int(a['p2hp']) > 0 and b['p2hp'] == '0']) == 2
    with (folder/'bodysuck_victim.csv').open() as stream:
        victims = list(csv.DictReader(stream))
    assert victims and all(int(r['character']) == actor for r in victims)
    illegal = sum(int(r['pc'], 16) == symbols['illegal_opcode']+0x50 for r in rows)
    invalid_shapes = sorted({r['shape'] for r in victims if not 0xff800000 <= int(r['shape'],16) < 0xffffffff})
    if actor == 17:
        assert illegal == 1 and int(rows[-1]['frame']) == 5540
    else:
        assert not illegal and '25293b3a' in invalid_shapes and victims[-1]['death'] == '65535'
    cases.append(dict(actor=actor, run=run, naturalKOs=2,
        lastField=int(rows[-1]['frame']), illegalRecoveryRows=illegal,
        invalidShapePointers=invalid_shapes, completionObserved=victims[-1]['death']=='65535',
        traceSHA256=sha((folder/'bodysuck_victim.csv').read_bytes()), behaviorPassed=False))
report = dict(scope='Mileena body-suck malformed own victim reaction reproduction',
    programLaneSHA256=[sha(data) for data in lanes], cases=cases,
    sourceAnimationTableEntries=12, requiredTrueIDCapacity=19,
    earlier261And262ActivatedStabbingInstead=True,
    properOwnIngestionAnimationRequired=True, completionDoesNotProveCompatibility=True,
    bodySuckCompatible=False, gameCodeChanged=False, releaseReady=False)
(PORT/'BODY_SUCK_FAILURE_AUDIT.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
