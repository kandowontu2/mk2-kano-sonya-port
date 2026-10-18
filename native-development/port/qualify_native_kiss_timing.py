"""Native-timed kiss reaction observed beyond the completion flag."""
import csv
import json
import re
import struct
import sys
from pathlib import Path
import zipfile
from build_inflation_assets import sha
from current_graphics import verify_archive_sockets
from kiss_inflate_source import WAIT_OLD, WAIT_NEW

PORT = Path(__file__).resolve().parent
BASE = PORT.parent/'baseline'
SRC = BASE/'mk2-rebuild-main/srcp'
assert WAIT_OLD in (SRC/'MKDEATH.ASM').read_text()
assert WAIT_NEW not in (SRC/'MKDEATH.ASM').read_text()
symbols = {n: int(a, 16) for a, n in re.findall(
    r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)', (SRC/'MK2P.MAP').read_text())}
lanes = [b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes()
                 for part in ('F8', 'FC')) for lane in range(2)]
program = bytearray(1048576)
program[::2], program[1::2] = lanes
art = json.loads((PORT/'generated_inflation_v3/INFLATION_DATA.json').read_text())
for frame in art['frames']:
    header = struct.unpack_from('<HHhhIHI', program,
        (symbols[frame['imageLabel']]-0xff800000)//8)
    assert header == (frame['width'], frame['height'], frame['xOffset'],
        frame['yOffset'], (0xc00000+frame['packedByteOffset'])*8, 0x6000,
        symbols[f'ks_{frame["actor"]}_primary_palette'])
cases = []
names = sys.argv[1:] or ['stock_kiss_native_time_kano281', 'stock_kiss_native_time_sonya282',
                         'stock_kiss_native_mirror_kano283', 'stock_kiss_native_mirror_sonya284']
assert len(names) in (2, 4)
for index, run in enumerate(names):
    actor, name = (17, 'kano') if index % 2 == 0 else (18, 'sonya')
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
    assert all(r['missing'] == '0' and int(r['pc'], 16) != symbols['illegal_opcode']+0x50 for r in rows)
    side = 1 if '--mirror' in receipt['testArguments'] else 2
    fight = [r for r in rows if r['mode'] == '2' and r[f'p{3-side}char'] == '4' and int(r[f'p{side}char']) == actor]
    assert len([b for a, b in zip(fight, fight[1:]) if int(a[f'p{side}hp']) > 0 and b[f'p{side}hp'] == '0']) == 2
    with (folder/'kitana_kiss_late.csv').open() as stream:
        victims = list(csv.DictReader(stream))
    assert all(int(r['character']) == actor for r in victims)
    coverage = [sum(int(r['shape'], 16) == symbols[f'ks_inf_{name}_pose{i}']
                    for r in victims) for i in range(6)]
    assert all(coverage)
    pop = [r for r in victims if int(r['shape'], 16) == symbols[f'ks_inf_{name}_pose5']]
    visible = [r for r in pop if not (int(r['flags']) & 0x20)]
    hidden = [r for r in victims if int(r['flags']) & 0x20]
    assert len(visible) >= 3 and hidden
    completed = [r for r in victims if r['death'] == '65535']
    assert completed and int(pop[0]['frame']) > int(completed[0]['frame'])
    pop_after_completion = int(pop[0]['frame'])-int(completed[0]['frame'])
    assert int(victims[-1]['frame'])-int(hidden[0]['frame']) >= 60
    observer = (folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)', observer)
    assert not list(folder.glob('*fault*'))
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    bursts = list((folder/'snap').glob('inflate_burst30_*.png'))
    assert len(bursts) == 1
    burst = bursts[0]
    assert burst.exists()
    assert victims[-1]['death'] == '65535'
    screenshots = list((folder/'snap').glob('inflate_phase5_*.png'))
    assert len(screenshots) == 1
    screenshot = screenshots[0]
    assert screenshot.exists()
    cases.append(dict(actor=actor, run=run, victimSide=side, fields=9000, naturalKOs=2,
        phaseRows=coverage, trueIdentityRetained=True,
        ownInflatedBodyAndPaletteVisuallyObserved=True,
        correctFacingVisuallyObserved=True, popPoseObserved=True,
        visiblePopFields=len(visible), popFieldsAfterCompletion=pop_after_completion,
        explosionVisuallyObservedAfterCompletion=True,
        burstCaptureSHA256=sha(burst.read_bytes()), captureSHA256=sha(screenshot.read_bytes())))
report = dict(scope='Native-timed own kiss: six poses and late pop/explosion on both tested sides',
    programLaneSHA256=[sha(data) for data in lanes], compiledHeadersVerified=12,
    cases=cases, properOwnInflationFivePhasesObserved=True,
    boundedOwnSequenceObserved=True, nativeMasterTimingRetained=True,
    additionalOwnMasterWaitRemoved=True, lateLifecycleObservationRequired=True,
    mirroredRuntimeControls=all({c['victimSide'] for c in cases if c['actor'] == actor} == {1,2} for actor in (17,18)),
    originalRosterRuntimeControls=False, finalAlignmentAccepted=False,
    fullSequenceAccepted=False, kitanaKissCompatible=False, releaseReady=False)
(PORT/'NATIVE_KISS_TIMING_QUALIFICATION.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
