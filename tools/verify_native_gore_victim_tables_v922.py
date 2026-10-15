"""Verify five real-ID table repairs, not inflation artwork or the whole port."""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CASES = tuple(f'audit_v921_kitana_{name}_p{side}_native_gore'
              for name in ('kano', 'sonya') for side in (1, 2))
EXE = 'B36C121BDDDBD30EE977098329BEF48FAFEF4F3164F8CA126D5D81DD42A7F8CE'
PAYLOAD = 'CC4F29043DE71AEEB0820D15E5A449A14073CDFBFA3F58B756751C92073964DF'
BASE_SHA = '0C0DB53A638195D139A19944A7AE8C3821EA9D2DDE5DBA3F17BFE2430EA9AB08'
PARAMETERS = ((0xff8cd3b0, 0xff8cc790, 0xfd680, 0x40),
              (0xff8cd2f0, 0xff8ccc80, 0xfd6c0, 0xffb7))
GORE = ((0xff9ed0f0, 0xff9ec840, 0xfac40),
        (0xff9eca40, 0xff9ec8b0, 0xfac90),
        (0xff9ecc30, 0xff9ecbd0, 0xface0))
STREAMS = ((0xff9f0f80, 0xfad40), (0xff9f1a00, 0xfad60))
PALETTES = (((0xffaf84a0, 0xfae00), (0xffaf6c60, 0xfae90)),
            ((0xffaf8880, 0xfaf20), (0xffaf7070, 0xfafb0)))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def offset(address):
    return (address - 0xff800000) // 8


def address(at):
    return 0xff800000 + at * 8


def records(text):
    return [(m[1], dict(re.findall(r'(\w+)=([^\s]+)', m[2])))
            for m in re.finditer(r'^MK2_STOCK_HEAD_V921_(\w+) (.*)$', text, re.M)]


def expected_guest():
    base_path = ROOT / 'audit_v904_sonya_p2_native_death_grounding/guest_maincpu.bin'
    if digest(base_path) != BASE_SHA:
        raise ValueError('Accepted v901 guest reference changed')
    base = base_path.read_bytes()
    result = bytearray(base)
    for source, operand, destination, value in PARAMETERS:
        if struct.unpack_from('<I', base, offset(operand))[0] != source:
            raise ValueError('Original short word-table consumer changed')
        result[destination:destination + 34] = base[offset(source):offset(source) + 34]
        struct.pack_into('<2H', result, destination + 34, value, value)
        struct.pack_into('<I', result, offset(operand), address(destination))
    for source, operand, destination in GORE:
        if struct.unpack_from('<I', base, offset(operand))[0] != source:
            raise ValueError('Original short pointer-table consumer changed')
        result[destination:destination + 68] = base[offset(source):offset(source) + 68]
        struct.pack_into('<I', result, offset(operand), address(destination))
    for fighter, (source, destination) in enumerate(STREAMS):
        result[destination:destination + 32] = base[offset(source):offset(source) + 32]
        struct.pack_into('<I', result, GORE[0][2] + (17 + fighter) * 4, address(destination))
        for phase, (palette, target) in enumerate(PALETTES[fighter]):
            count = struct.unpack_from('<I', base, offset(palette))[0]
            if count != (61, 64)[phase]:
                raise ValueError('Native provisional inflation palette layout changed')
            size = 4 + count * 2
            result[target:target + size] = base[offset(palette):offset(palette) + size]
            struct.pack_into('<I', result, GORE[1 + phase][2] + (17 + fighter) * 4, address(target))
    return bytes(result)


def verify(texts=None, check_files=True, guests=None):
    texts = ({case: (ROOT / case / 'run.log').read_text(encoding='utf-8-sig') for case in CASES}
             if texts is None else texts)
    errors, summaries, pins = [], {}, {}
    wanted = expected_guest()

    def need(condition, message):
        if not condition:
            errors.append(message)

    need(set(texts) == set(CASES), 'All four real-ID/physical-slot cases required')
    for case, text in texts.items():
        directory = ROOT / case
        result = json.loads((directory / 'result.json').read_text(encoding='utf-8-sig'))
        name, side = result['player'], result['victim_slot']
        identity = 17 if name == 'kano' else 18
        need(case == f'audit_v921_kitana_{name}_p{side}_native_gore', case + ': exact case identity')
        need(result['exit_code'] == 0 and result['winner_slot'] == 3 - side and result['seconds'] == 95
             and result['assistance'] == 'none' and result['cheats_enabled'] is False,
             case + ': physical-input cold completion')
        need(result['killer'] == 'kitana' and result['command'] == 'ffdf_lk_release'
             and result['target_gap'] == 64, case + ': actual selected native command scenario')
        need(result['executable_sha256'] == EXE and result['payload_sha256'] == PAYLOAD,
             case + ': exact matched experimental build')
        if check_files:
            for filename, expected in result['input_hashes'].items():
                path = Path(filename)
                need(path.is_file() and digest(path) == expected, 'Frozen input changed: ' + filename)
                pins[filename] = expected
        need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at', text, re.I),
             case + ': no runtime errors')
        rows = records(text)
        need(bool(rows) and all(r.get('writes') == '0' and r.get('assistance') == 'none'
                               and r.get('victim') == name and r.get('side') == str(side)
                               and r.get('killer') == 'kitana' for _, r in rows),
             case + ': consistent true physical identity')

        def items(tag):
            return [r for t, r in rows if t == tag]

        actions, wraps = items('ACTION'), items('WRAP')
        need(len(actions) == len(wraps) == 1, case + ': one original action and native completion')
        if len(actions) != 1 or len(wraps) != 1:
            continue
        action, wrap = actions[0], wraps[0]
        start = int(action['frame'])
        need(action['damage'] == '322' and action['mode'] == '2'
             and action['actor'] != action['victim_actor'] and action['main'] != action['victim_main'],
             case + ': distinct owners and two real native KOs')
        live = items('FIRST_LIVE')
        need(len(live) == 1 and live[0]['ids'] == f'4,{identity}' and live[0]['own'] == action['actor']
             and live[0]['victim'] == action['victim_actor'], case + ': true Kitana and victim, no proxy')
        damage, collisions = 0, []
        writers = {0xff836700, 0xff825930 if side == 1 else 0xff825960,
                   0xff9dece0 if side == 1 else 0xff9ded10, 0xff9def40 if side == 1 else 0xff9def70}
        for row in items('HEALTH'):
            pc, before, after = int(row['pc'], 16), int(row['before']), int(row['after'])
            need(pc in writers, case + ': original physical health writers only')
            if pc == 0xff836700 and int(row['frame']) <= start:
                need(0 <= after <= before <= 161, case + ': native collision damage bounds')
                damage += before - after
                collisions.append(row)
        need(damage == 322 and len(collisions) == 10 and sum(r['after'] == '0' for r in collisions) == 2,
             case + ': independently observed 322 damage and two KOs')
        need(not items('CACHE_OVERWRITE'), case + ': no body-cache write into player globals')
        need(not any(r['mode'] == '0' and int(r['frame']) > 600 for r in items('MODE')),
             case + ': no native reset after gameplay')
        need(int(wrap['age']) == 276 and int(wrap['frame']) == start + 276 and wrap['pc'] == 'FF8CDC50'
             and wrap['actor'] == action['actor'] and wrap['main'] == action['main'],
             case + ': exact native winner completion')
        inputs, approach = items('INPUT'), items('APPROACH')
        need(len(approach) == 1, case + ': physical approach exists')
        if len(approach) == 1:
            beginning = int(approach[0]['frame'])
            own = str(3 - side)
            forward = 'Right' if side == 2 else 'Left'
            expected_commands = [(beginning + age, button) for age, button in
                                 ((10, forward), (18, forward), (26, 'Down'), (34, forward))]
            need(all(any(int(r['frame']) == frame and r['button'] == button and r['slot'] == own
                         for r in inputs) for frame, button in expected_commands)
                 and start == beginning + 44, case + ': genuine Forward Forward Down Forward release command')
            held = {int(r['frame']) for r in inputs if r['slot'] == own and r['button'] == 'Low_Kick'}
            need(all(frame in held for frame in range(beginning - 60, beginning + 42))
                 and all(frame not in held for frame in range(beginning + 42, start + 1)),
                 case + ': actual continuous hold and button release')
        compared = [r for r in items('COMPARE') if int(r['frame']) == start]
        need(len(compared) == 4 and all(r['wanted'] == r['actual'] for r in compared),
             case + ': native command parser accepted four direction-history entries')
        parameters = items('PARAMETER')
        need(len(parameters) == 2, case + ': both native word-table consumers observed')
        for source, operand, destination, value in PARAMETERS:
            observed = [r for r in parameters if int(r['operand'], 16) == operand]
            need(len(observed) == 1 and int(observed[0]['table'], 16) == address(destination)
                 and int(observed[0]['at'], 16) == address(destination) + identity * 16
                 and int(observed[0]['value'], 16) == value and observed[0]['row'] == str(identity)
                 and observed[0]['actor'] == action['victim_actor'] and observed[0]['main'] == action['victim_main']
                 and observed[0]['pc'] == 'FF82EE10', case + ': exact own-ID timing/position row')
        gore = items('GORE_ROW')
        need(len(gore) == 6, case + ': all three native pointer reads, both bus halves')
        for _, operand, destination in GORE:
            observed = sorted([r for r in gore if int(r['operand'], 16) == operand], key=lambda r: int(r['half']))
            pointer = struct.unpack_from('<I', wanted, destination + identity * 4)[0]
            need(len(observed) == 2 and [r['half'] for r in observed] == ['0', '1']
                 and all(int(r['table'], 16) == address(destination)
                         and int(r['at'], 16) == address(destination) + identity * 32 + half * 16
                         and int(r['value'], 16) == (pointer >> (16 * half)) & 0xffff
                         and int(r['mask'], 16) == 0xffff and r['row'] == str(identity)
                         and r['actor'] == action['victim_actor'] and r['main'] == action['victim_main']
                         and r['pc'] == 'FF83B850' for half, r in enumerate(observed)),
                 case + ': genuine independent inflation stream/palette rows')
        need(any(r['mode'] == '3' and int(r['frame']) > start + 276 for r in items('MODE')),
             case + ': real terminal continue screen, not merely process exit')
        terminal = items('RESULT')
        need(len(terminal) == 1 and terminal[0]['damage'] == '322' and terminal[0]['wins'] == '2'
             and int(terminal[0]['action']) == start and int(terminal[0]['wrap']) == start + 276
             and int(terminal[0]['frame']) == 5198, case + ': full terminal continuation')
        displays = items('DISPLAY')
        need([int(r['age']) for r in displays] == list(range(0, 601, 10)), case + ': full snapshot chronology')
        for age in range(0, 601, 10):
            picture = directory / 'snap' / f'stock_head_{start}_{age:03d}.png'
            need(picture.is_file() and Image.open(picture).size == (400, 254), case + ': actual native snapshot ' + str(age))
            if check_files and picture.is_file():
                pins[str(picture)] = digest(picture)
        guest = ((directory / 'guest_maincpu.bin').read_bytes() if guests is None else guests[case])
        need(guest == wanted, case + ': whole guest equals only five intended table extensions')
        if check_files:
            for file in ('run.log', 'result.json', 'guest_maincpu.bin', 'native_death_gfx.bin'):
                pins[str(directory / file)] = digest(directory / file)
        summaries[case] = {'victim': name, 'slot': side, 'damage': damage, 'action': start,
                           'nativeCompletionAge': int(wrap['age']), 'snapshots': len(displays),
                           'tableRowsObserved': len(parameters) + len(gore),
                           'nativeTableStabilityAccepted': True, 'ownedInflationArtworkAccepted': False}
    for file in ('mk2ks_stock_head_victim_v921.lua', 'mk2ks_stock_head_display_v921.lua'):
        source = (ROOT / file).read_text(encoding='utf-8-sig')
        need(not re.search(r'\bp:write_|\.value\s*=(?!=)|load_state|loadstate', source), 'Observers remain read-only: ' + file)
    return {'passed': not errors, 'errors': errors, 'fiveNativeVictimTablesAcceptance': not errors,
            'ownedInflationArtworkAcceptance': False, 'cageTorsoArtworkAcceptance': False,
            'fullPortAcceptance': False, 'alternatePaletteRuntimeAcceptance': False,
            'allStockFatalitiesAcceptance': False, 'cases': summaries, 'pins': pins}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Refuse to overwrite evidence')
    report = verify()
    args.output.mkdir(parents=True)
    (args.output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ('passed', 'errors', 'fiveNativeVictimTablesAcceptance', 'fullPortAcceptance')}))
    raise SystemExit(0 if report['passed'] else 1)
