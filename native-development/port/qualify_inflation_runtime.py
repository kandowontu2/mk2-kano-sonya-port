"""Bounded own inflation, pop and native explosion sequence qualification."""
import csv
import json
import re
import struct
import sys
from pathlib import Path
import zipfile
from build_inflation_assets import sha
from current_graphics import verify_archive_sockets
from verify_finisher_roms import verify

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
names = sys.argv[1:]
assert len(names) in (2, 4) and len(set(names))==len(names), 'Supply explicit distinct current runs'
for index, run in enumerate(names):
    assert run and Path(run).name==run and '/' not in run and '\\' not in run
    folder = BASE/run
    receipt = json.loads((folder/'execution.json').read_text())
    args=receipt['testArguments']
    assert '--kitana-kiss-victim' in args and not any(arg.startswith('--kitkiss-control=') for arg in args)
    actor,name=(18,'sonya') if '--sonya' in args else (17,'kano')
    assert receipt['exitCode'] == 0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256'] == 'AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert sha((folder/'autoboot.lua').read_bytes()) == receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        verify(archive,receipt)
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
    with (folder/'kitana_kiss_victim.csv').open() as stream:
        early_victims = list(csv.DictReader(stream))
    with (folder/'kitana_kiss_late.csv').open() as stream:
        victims = list(csv.DictReader(stream))
    # Native master completion precedes the victim pop/burst. The frozen
    # observer records that continuing object separately, including mode 5.
    assert victims and len({r['object'] for r in victims})==1
    assert int(victims[0]['object'],16)!=0
    assert all(int(b['frame'])==int(a['frame'])+1 for a,b in zip(victims,victims[1:]))
    by_frame={int(r['frame']):r for r in victims}
    overlap=[r for r in early_victims if int(r['frame']) in by_frame]
    assert len(overlap)>=60
    assert all(all(r[key]==by_frame[int(r['frame'])][key] for key in
                   ('character','shape','flags','death')) for r in overlap)
    assert all(int(r['character']) == actor for r in victims)
    coverage = [sum(int(r['shape'], 16) == symbols[f'ks_inf_{name}_pose{i}']
                    for r in victims) for i in range(6)]
    assert all(coverage)
    pop = [r for r in victims if int(r['shape'], 16) == symbols[f'ks_inf_{name}_pose5']]
    visible = [r for r in pop if not (int(r['flags']) & 0x20)]
    hidden = [r for r in victims if int(r['flags']) & 0x20]
    assert len(visible) >= 3 and hidden
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
        ownInflatedBodyAndPaletteVisuallyObserved=False,
        correctFacingVisuallyObserved=False, popPoseObserved=True,
        visiblePopFields=len(visible), lateVictimContinuationObserved=True,
        masterCompletionPrecedesVisiblePop=int(visible[0]['frame'])>int(early_victims[-1]['frame']),
        overlappingEarlyLateRows=len(overlap),
        burstCaptureSHA256=sha(burst.read_bytes()), captureSHA256=sha(screenshot.read_bytes())))
assert {c['actor'] for c in cases}=={17,18}
assert len({(c['actor'],c['victimSide']) for c in cases})==len(cases)
report = dict(scope='Own inflation six poses and native explosion, explicit tested sides',
    programLaneSHA256=[sha(data) for data in lanes], compiledHeadersVerified=12,
    cases=cases, properOwnInflationFivePhasesObserved=True,
    boundedOwnSequenceObserved=True,
    mirroredRuntimeControls=all({c['victimSide'] for c in cases if c['actor'] == actor} == {1,2} for actor in (17,18)),
    originalRosterRuntimeControls=False, finalAlignmentAccepted=False,
    fullSequenceAccepted=False, kitanaKissCompatible=False, releaseReady=False)
paths=[Path(__file__),PORT/'verify_finisher_roms.py',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
       SRC/'MKDIE.ASM',SRC/'MKDEATH.ASM',PORT/'generated_inflation_v3/INFLATION_DATA.json']
for run in names:
    folder=BASE/run
    paths.extend(folder/item for item in ('execution.json','autoboot.lua','kitana_kiss.csv','kitana_kiss_victim.csv','kitana_kiss_late.csv','mame.log'))
    paths.extend(sorted((folder/'snap').glob('*.png')))
report['currentFull26ROMBytesVerified']=True
report['pins']={str(path):sha(path.read_bytes()) for path in paths}
(PORT/'INFLATION_RUNTIME_QUALIFICATION.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
