"""Verify actual linked ladder ROM tables; not earned-campaign proof."""
import hashlib
import json
from pathlib import Path
import re
import struct
import zipfile
from ladder_source import BOTTOM, SPACING
from prepare_game_candidate import ZIP

PORT = Path(__file__).resolve().parent
SRC = PORT.parent / 'baseline/mk2-rebuild-main/srcp'
sha = lambda data: hashlib.sha256(data).hexdigest().upper()
symbols = {name: int(address, 16) for address, name in re.findall(
    r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)', (SRC / 'MK2P.MAP').read_text())}
rom = bytearray(1048576)
for lane in (0, 1):
    rom[lane::2] = b''.join((SRC / f'rom/P12{part}.{lane}').read_bytes() for part in ('F8', 'FC'))


def read(address, size):
    assert address >= 0xff800000 and address + size * 8 <= 0x100000000 and address % 8 == 0
    at = (address - 0xff800000) // 8
    return bytes(rom[at:at + size])


def pointer(address):
    return struct.unpack('<I', read(address, 4))[0]


def local(listing, name):
    return int(re.search(r'^\s+\d+\s+([0-9a-fA-F]{8})\s+' + name + r'\s*$', listing, re.M)[1], 16)


def instruction(listing, asm):
    found = re.findall(r'^\s+\d+\s+([0-9a-fA-F]{8})\s+[0-9a-fA-F]{4}\s+' + asm + r'(?:\s*;[^\n]*)?\s*$', listing, re.M)
    assert found, asm
    return int(found[0], 16)


sel = (SRC / 'MKSEL.LST').read_text()
base = symbols['do_ladder'] - local(sel, 'do_ladder')
table = base + local(sel, 'rom_maps_tbl')
equates = {name: int(value, 16) if suffix else int(value) for name, value, suffix in re.findall(
    r'(?im)^\s*(ft_\w+)\s+\.set\s+(\d[\da-f]*)(h?)\b', (SRC / 'MAINEQU.ASM').read_text())}
with zipfile.ZipFile(ZIP) as archive:
    original_sel = archive.read('mk2-rebuild-main/src/MKSEL.ASM').decode('cp437').replace('\r\n', '\n')
    original_main = archive.read('mk2-rebuild-main/src/MAIN.ASM').decode('cp437').replace('\r\n', '\n')
original_maps = list(re.finditer(r'(?m)^map_([1-6])\t.word[^\n]*(?:\n\t.word[^\n]*)*', original_sel))
assert len(original_maps) == 6
maps = []
for index, match in enumerate(original_maps):
    names = re.findall(r'\.word\s+([^\s;]+)', match.group(0))
    expected = [equates[name] if name != '-1' else -1 for name in names]
    expected[11:11] = [17, 18]
    address = pointer(table + index * 32)
    actual = list(struct.unpack('<18h', read(address, 36)))
    assert actual == expected, (index, actual, expected)
    assert actual[11:14] == [17, 18, equates['ft_smoke']]
    assert actual[14:17] == [equates['ft_st'], equates['ft_goro'], equates['ft_final_boss']]
    maps.append(dict(map=index + 1, address=f'{address:08X}', identities=actual))

spots = [BOTTOM, BOTTOM] + [BOTTOM - (i - 1) * SPACING for i in range(2, 14)]
spots += [spots[-1], BOTTOM - 14 * SPACING, 4]
assert list(struct.unpack('<17h', read(base + local(sel, 'world_y_spots'), 34))) == spots
boxes = [128 + i * SPACING for i in range(16, -1, -1)] + [-1]
assert list(struct.unpack('<18h', read(base + local(sel, 'box_coordinate_table'), 36))) == boxes
portraits = []
for identity, actor in ((17, 'kano'), (18, 'sonya')):
    actual = pointer(base + local(sel, 'mini_mug_table') + identity * 32)
    assert actual == symbols[f'ks_{actor}_ladder']
    portraits.append(dict(identity=identity, address=f'{actual:08X}'))
frames = []
for name in ('smframe1', 'smframe2'):
    address = pointer(base + instruction(sel, r'movi\s+' + name + r',a5') + 16)
    width, height = struct.unpack('<HH', read(address, 4))
    assert height == 51 and SPACING >= height
    frames.append(dict(name=name, width=width, height=height))
assert read(base + instruction(sel, r'cmpi\s+16,a0'), 4) == struct.pack('<HH', 0x0b40, ~16 & 65535)
assert read(base + instruction(sel, r'movi\s+074h,a1'), 4) == struct.pack('<HH', 0x09c1, 116)

main = (SRC / 'MAIN.LST').read_text()
main_base = symbols['end_of_match_chores'] - local(main, 'end_of_match_chores')
tiers = []
for index in range(1, 6):
    match = re.search(rf'diff_min_{index}\n\s*\.word\s+([^;\n]+);[^\n]*\n\s*\.word\s+([^;\n]+)', original_main)
    regular = [int(v.strip()) for v in match[1].split(',')]
    bosses = [int(v.strip()) for v in match[2].split(',')]
    regular[11:11] = [regular[10], regular[10]]
    expected = regular + bosses
    actual = list(struct.unpack('<20H', read(main_base + local(main, f'diff_min_{index}'), 40)))
    assert actual == expected
    tiers.append(actual)
jade = (SRC / 'MKTOAST.LST').read_text()
jade_base = symbols['jade_check'] - local(jade, 'jade_check')
assert read(jade_base + instruction(jade, r'cmpi\s+12,a0'), 4) == struct.pack('<HH', 0x0b40, ~12 & 65535)
assert read(jade_base + instruction(jade, r'movi\s+14,a0'), 4) == struct.pack('<HH', 0x09c0, 14)

report = dict(programSHA256=sha(rom), linkedMaps=maps, cameraY=spots,
              boxY=boxes, ownPortraitPointers=portraits, nativeFrameDimensions=frames,
              difficultyTiers=tiers, jadeTrigger=12, jadeReturn=14, finalBossIndex=16,
              linkedROMTablesVerified=True, allLadderTransitionsRuntimeVerified=False,
              fullCampaignVerified=False, releaseReady=False)
report['evidenceSHA256'] = {name: sha((SRC / name).read_bytes()) for name in (
    'MKSEL.ASM', 'MKSEL.LST', 'MAIN.ASM', 'MAIN.LST', 'MKTOAST.ASM', 'MKTOAST.LST', 'MAINEQU.ASM', 'MK2P.MAP')}
(PORT / 'LADDER_LINK_QUALIFICATION.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'evidenceSHA256'}, indent=2))
