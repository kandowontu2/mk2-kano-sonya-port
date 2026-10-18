"""Bounded own dizzy-guard smoke tests, not completed kiss qualification."""
import csv
import hashlib
import json
from pathlib import Path
import zipfile
from current_graphics import verify_archive_sockets
from kiss_setup_source import NEW

PORT = Path(__file__).resolve().parent
BASE = PORT.parent/'baseline'
SRC = BASE/'mk2-rebuild-main/srcp'
sha = lambda data: hashlib.sha256(data).hexdigest().upper()
assert NEW in (SRC/'MKDEATH.ASM').read_text()
lanes = [b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes()
                 for part in ('F8', 'FC')) for lane in range(2)]
cases = []
for actor, run in ((17, 'stock_kiss_setup_kano247'),
                   (18, 'stock_kiss_setup_sonya248')):
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
    with (folder/'kitana_kiss.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    assert int(rows[-1]['frame']) == 9000
    assert all(row['missing'] == '0' for row in rows)
    fight = [r for r in rows if r['mode'] == '2' and r['p1char'] == '4'
             and int(r['p2char']) == actor]
    kos = [b for a, b in zip(fight, fight[1:]) if int(a['p2hp']) > 0 and b['p2hp'] == '0']
    assert len(kos) == 2
    with (folder/'kitana_kiss_victim.csv').open() as stream:
        victims = list(csv.DictReader(stream))
    assert victims and all(int(r['character']) == actor for r in victims)
    active = [r for r in victims if r['death'] == '2']
    assert active and any(r['death'] == '65535' for r in victims)
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(actor=actor, run=run, fields=9000, naturalKOs=2,
        nativeFatalityFields=len(active), nativeCompletionObserved=True,
        executionSHA256=sha((folder/'execution.json').read_bytes()),
        victimTraceSHA256=sha((folder/'kitana_kiss_victim.csv').read_bytes())))
report = dict(scope='Dizzy-offset guard build and physical-input smoke only',
    programLaneSHA256=[sha(data) for data in lanes], cases=cases,
    sourceSHA256=sha((SRC/'MKDEATH.ASM').read_bytes()),
    originalRosterRuntimeControls=False, mirroredRuntimeControls=False,
    properOwnInflationArtVerified=False, kissAlignmentAccepted=False,
    kitanaKissCompatible=False, releaseReady=False)
(PORT/'KISS_SETUP_AUDIT.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
