"""Original ingestion-table preservation and physical-input regression controls."""
import csv
import json
import re
import struct
import zipfile
from pathlib import Path
from build_inflation_assets import sha
from current_graphics import verify_archive_sockets
from inventory_character_tables import source_tables
from ingestion_contract import extract

PORT = Path(__file__).resolve().parent
BASE = PORT.parent/'baseline'
SRC = BASE/'mk2-rebuild-main/srcp'
original_zip = Path('C:/Users/kando/Downloads/mk2-rebuild-main.zip')
assert sha(original_zip.read_bytes()) == '2EE5C1FAD3122B6A7FE20AEF948CF96E54D4625DA073CA64273372817961A4A5'
preserved = []
with zipfile.ZipFile(original_zip) as archive:
    for filename, labels in (('MKDEATH.ASM', ('kissed_offset', 'kissed_coor_adj')),
                             ('MKDIE.ASM', ('inflate_animations', 'inflate_palettes', 'pop_palettes', 'sucked_in_anis'))):
        key = next(n for n in archive.namelist() if n.lower().endswith('/src/'+filename.lower()))
        original = source_tables(archive.read(key).decode('cp437'))
        current = source_tables((SRC/filename).read_text())
        for label in labels:
            typed = lambda table: [(r['type'], r['values']) for r in table['rows']]
            assert typed(current[label]) == typed(original[label]), label
            preserved.append(label)
lanes = [b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes()
                 for part in ('F8', 'FC')) for lane in range(2)]
program = bytearray(1048576)
program[::2], program[1::2] = lanes
reference = extract()['sequences']


def group_headers(address):
    if not 0xff800000 <= address < 0xffffffff:
        return None
    offset = (address-0xff800000)//8
    headers = []
    for _ in range(8):
        if offset+4 > len(program):
            return None
        image = struct.unpack_from('<I', program, offset)[0]
        if image == 0:
            return headers
        at = (image-0xff800000)//8
        if at < 0 or at+8 > len(program):
            return None
        headers.append(list(struct.unpack_from('<HHhh', program, at)))
        offset += 4
    return None

symbols = {n: int(a, 16) for a, n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',
            (SRC/'MK2P.MAP').read_text())}
own_shapes = {v for n, v in symbols.items() if n.startswith('ks_ing_') and '_pose' in n}
cases = []
for actor, run in ((1, 'stock_ingestion_control_liu269'), (4, 'stock_ingestion_control_kitana270')):
    folder = BASE/run
    receipt = json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode'] == 0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256'] == 'AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert f'--ingestion-control={actor}' in receipt['testArguments']
    assert sha((folder/'autoboot.lua').read_bytes()) == receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane, chip in enumerate(('mk321u54.bin', 'mk321u63.bin')):
            assert archive.read(chip) == lanes[lane]
        verify_archive_sockets(archive)
    with (folder/'bodysuck.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    assert int(rows[-1]['frame']) == 9000
    assert all(r['missing'] == '0' and int(r['pc'], 16) != symbols['illegal_opcode']+0x50 for r in rows)
    fight = [r for r in rows if r['mode'] == '2' and r['p1char'] == '5' and int(r['p2char']) == actor]
    assert len([b for a, b in zip(fight, fight[1:]) if int(a['p2hp']) > 0 and b['p2hp'] == '0']) == 2
    with (folder/'bodysuck_victim.csv').open() as stream:
        victims = list(csv.DictReader(stream))
    assert all(int(r['character']) == actor and int(r['shape'], 16) not in own_shapes for r in victims)
    active = [r for r in victims if r['death'] == '2']
    assert len(active) == 283 and victims[-1]['death'] == '65535'
    expected = reference['liu' if actor == 1 else 'female_ninja']
    shapes = {r['shape']:group_headers(int(r['shape'],16)) for r in active}
    coverage = []
    first_frames = []
    for frame in expected:
        hits = [r for r in active if shapes[r['shape']] == frame['originalHeaders']]
        assert len(hits) >= 4
        coverage.append(len(hits))
        first_frames.append(int(hits[0]['frame']))
    assert any(int(r['flags']) & 0x20 for r in active)
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(actor=actor, run=run, fields=9000, naturalKOs=2,
        nativeFatalityFields=len(active), originalIdentityAndBodyRetained=True,
        nativeIngestionPhaseRows=coverage, phaseFirstFrames=first_frames,
        originalNativeGeometryAndDisappearanceVerified=True))
report = dict(scope='Six unchanged native lookup tables and two original-ingestion controls',
    programLaneSHA256=[sha(data) for data in lanes], cases=cases,
    preservedOriginalTables=preserved, boundedOriginalControlsVerified=True,
    allOriginalCharactersVerified=False, allOriginalIngestionVisualsAccepted=False,
    boundedMileenaAttackerControlsVerified=True, releaseReady=False)
(PORT/'INGESTION_ORIGINAL_CONTROLS.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
