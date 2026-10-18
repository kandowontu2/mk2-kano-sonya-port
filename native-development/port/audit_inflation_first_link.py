"""Pin first native inflation link and its observed facing/timing failures."""
import csv
import json
import re
import struct
from pathlib import Path
import zipfile
from build_inflation_assets import sha
from current_graphics import verify_archive_sockets

PORT = Path(__file__).resolve().parent
BASE = PORT.parent/'baseline'
SRC = BASE/'mk2-rebuild-main/srcp'
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
for actor, name, run, capture in (
    (17, 'kano', 'stock_kiss_inflate_kano249', 'kitana_kiss_05645.png'),
    (18, 'sonya', 'stock_kiss_inflate_sonya250', 'kitana_kiss_05633.png')):
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
    fight = [r for r in rows if r['mode'] == '2' and r['p1char'] == '4' and int(r['p2char']) == actor]
    assert len([b for a, b in zip(fight, fight[1:]) if int(a['p2hp']) > 0 and b['p2hp'] == '0']) == 2
    with (folder/'kitana_kiss_victim.csv').open() as stream:
        victims = list(csv.DictReader(stream))
    assert all(int(r['character']) == actor for r in victims)
    coverage = [sum(int(r['shape'], 16) == symbols[f'ks_inf_{name}_pose{i}']
                    for r in victims) for i in range(6)]
    assert all(coverage[:5]) and coverage[5] == 0
    assert victims[-1]['death'] == '65535'
    screenshot = folder/'snap'/capture
    assert screenshot.exists()
    cases.append(dict(actor=actor, run=run, fields=9000, naturalKOs=2,
        phaseRows=coverage, trueIdentityRetained=True,
        ownInflatedBodyAndPaletteVisuallyObserved=True,
        wrongFacingVisuallyObserved=True, popPoseObserved=False,
        popAbsentFromPreCompletionTrace=True, postCompletionRenderingObserved=False,
        captureSHA256=sha(screenshot.read_bytes())))
report = dict(scope='First linked own inflation: facing failure and pre-completion trace only',
    programLaneSHA256=[sha(data) for data in lanes], compiledHeadersVerified=12,
    cases=cases, properOwnInflationFivePhasesObserved=True,
    prematureTransitionConclusionVerified=False,
    fullSequenceAccepted=False, kitanaKissCompatible=False, releaseReady=False)
(PORT/'INFLATION_FIRST_LINK_AUDIT.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
