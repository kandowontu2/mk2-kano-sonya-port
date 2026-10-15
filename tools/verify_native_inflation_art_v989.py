"""Real-ID native command, all owned inflation DMA poses and palette evidence.

Retains the original physical/timing/table verifier, adds exact owned-only
guest changes and actual native FIFO/DMA/graphics/ground/palette binding.
Visual fidelity, other fatalities, alternate costumes and full port separate.
"""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
from PIL import Image
import numpy as np
import build_native_inflation_art_v935 as assets
import build_native_pit_fall_v2 as colors
import build_native_death_art_v900 as death
import verify_native_gore_victim_tables_v924 as original
import verify_native_torso_art_v980 as torso

ROOT = Path(__file__).resolve().parents[1]
CASES = tuple(f'audit_v987_kitana_{name}_p{side}_owned_inflation'
              for name in ('kano', 'sonya') for side in (1, 2))
EXE = '885B1A50DB68F6806C8A3B32DA329CAA87CCAC7636ADDB3D0283D83850023D1D'
PAYLOAD = '2679C041539C99F917CE1A9AAADAE455859A20DA5F5CC8AF9FB6013DB6A79F79'
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
    parsed = []
    for match in re.finditer(r'^MK2_STOCK_HEAD_V921_(\w+) (.*)$', text, re.M):
        row = dict(re.findall(r'(\w+)=([^\s]+)', match[2]))
        header = re.match(r'frame=\d+ victim=(kano|sonya) side=[12] killer=kitana writes=0 assistance=none ', match[2])
        row['header_victim'] = header[1] if header else 'invalid'
        parsed.append((match[1], row))
    return parsed


def expected_guest():
    payload = (ROOT / 'diagnostic_v978_owned_torso_invariant_blood/roms/mk2ks/mk2ks.mdata').read_bytes()
    if hashlib.sha256(payload).hexdigest().upper() != PAYLOAD:
        raise ValueError('Exact owned-inflation payload required')
    return torso.expected_guest(payload)


def verify_owned_art(texts, need, summaries, pins, check_files):
    payload_path = ROOT / 'diagnostic_v978_owned_torso_invariant_blood/roms/mk2ks/mk2ks.mdata'
    payload = payload_path.read_bytes()
    # Inflation remains byte-for-byte the accepted v936 allocation. Restore
    # ONLY the separately verified torso allocation and its typed references
    # for this older inflation-only delta test; retain all control tokens.
    prior = (ROOT / 'diagnostic_v936_owned_inflation_art/roms/mk2ks/mk2ks.mdata').read_bytes()
    isolated = bytearray(payload)
    isolated[torso.assets.HEADER:torso.assets.END] = prior[torso.assets.HEADER:torso.assets.END]
    for stream in torso.assets.STREAMS:
        at = death.offset(stream)
        for word in set(torso.assets.GROUP_WORDS) | set(torso.assets.RAW_WORDS):
            isolated[at+word*4:at+word*4+4] = prior[at+word*4:at+word*4+4]
    payload = bytes(isolated)
    base = (ROOT / 'audit_v934_pre_owned_inflation/input_sources/mk2ks.mdata').read_bytes()
    donor = (ROOT / 'mk3/mk3-maincpu.bin').read_bytes()
    encoding = json.loads((ROOT / 'audit_v935_owned_inflation_encoding/report.json').read_text())
    need(hashlib.sha256(base).hexdigest().upper() == assets.SOURCE_SHA, 'Immutable original v918 payload')
    need(payload[:assets.HEADER] == base[:assets.HEADER] and payload[assets.END:] == base[assets.END:],
         'Owned inflation allocation is the only payload change')
    need(base[assets.HEADER:assets.END] == b'\xff' * (assets.END - assets.HEADER), 'Previously empty owned inflation allocation')
    need(struct.unpack_from('<4s13I', payload, assets.HEADER) ==
         (b'KIF1', assets.PIXELS, 162308, assets.GFX, assets.DESCRIPTORS, assets.ROM_DESCRIPTORS,
          12, 20, assets.GROUPS, assets.ROM_GROUPS, assets.PALETTES, assets.STREAMS, 6, 2),
         'Exact native art header and bounded graphics allocation')
    source_records, pen_colors = {}, {}
    for fighter, name in enumerate(('kano', 'sonya')):
        path = ROOT / 'art_native_inflation_v933' / (name + '-inflation.png')
        need(digest(path) == assets.ASSETS[name], 'Selected source artwork immutable: ' + name)
        parts = assets.cells(path)
        factor = assets.HEIGHTS[fighter] / parts[0][1].height
        normal = colors.palette(donor, (0x92bbc, 0x92cf2)[fighter])
        burst = normal.copy()
        burst[59:63] = [(255, 0, 0), (197, 0, 0), (139, 0, 0), (82, 0, 0)]
        stream = struct.unpack_from('<8I', payload, assets.STREAMS + fighter * 32)
        wanted_stream = tuple(address(assets.ROM_GROUPS + (fighter * 6 + pose) * 8) for pose in range(5)) + (0, address(assets.ROM_GROUPS + (fighter * 6 + 5) * 8), 0)
        need(stream == wanted_stream, 'Native five-poses/separator/burst/separator grammar: ' + name)
        for phase, pal in enumerate((normal, burst)):
            record = assets.palette_record(pal)
            at = assets.PALETTES + (fighter * 2 + phase) * 144
            need(payload[at:at + 132] == record, 'Owned costume/blood palette bytes: ' + name)
        for pose, (_, image, _) in enumerate(parts):
            index = fighter * 6 + pose
            at = assets.DESCRIPTORS + index * 20
            width, height, xo, yo, graphic, command, palptr, padding = struct.unpack_from('<4hIHIH', payload, at)
            size = (round(image.width * factor), round(image.height * factor))
            left, top = assets.CENTERS[fighter] - size[0] // 2, assets.FLOORS[fighter] - size[1]
            need((width, height, xo, yo) == (*size, -left, -top), 'Uniform art geometry/own floor anchor: ' + name + str(pose))
            pal = normal if pose < 5 else burst
            selected = 0 if pose < 5 else 1
            need(command == 0x6000 and padding == 0 and palptr == address(assets.ROM_PALETTES[fighter][selected]),
                 'Native six-bit descriptor and character-owned phase palette')
            need(struct.unpack_from('<2I', payload, assets.GROUPS + index * 8) == (address(assets.ROM_DESCRIPTORS + index * 20), 0),
                 'Owned native zero-terminated body group')
            record = encoding['fighters'][name]['frames'][pose]
            pixel_at = assets.PIXELS + graphic // 8 - assets.GFX
            need(graphic % 8 == 0 and assets.PIXELS <= pixel_at < assets.END, 'Owned aligned graphics pointer')
            byte_count = (width * height * 6 + 7) // 8
            raw = death.unpack(payload[pixel_at:pixel_at + byte_count], width * height)
            indices = colors.quantize(image.resize(size, Image.Resampling.LANCZOS), pal)
            need(raw == indices.tobytes(), 'Packed native pixels equal selected PNG conversion: ' + name + str(pose))
            need(record['graphics'] == f'{graphic:08X}' and record['size'] == list(size), 'Encoding report agrees with independently decoded asset')
            # Hardware expands five-bit channels by bit replication, not a
            # floating-point color transform. Ignore pen zero transparency.
            packed = struct.unpack_from('<64H', assets.palette_record(pal), 4)
            pen_colors[graphic] = [0] + [(((((v >> 10) & 31) << 3) | ((v >> 12) & 7)) << 16) |
                                       (((((v >> 5) & 31) << 3) | ((v >> 7) & 7)) << 8) |
                                       (((v & 31) << 3) | ((v >> 2) & 7)) for v in packed[:63]]
            source_records[graphic] = (name, pose, record)
    for case, text in texts.items():
        directory = ROOT / case
        data = json.loads((directory / 'result.json').read_text(encoding='utf-8-sig'))
        name, side = data['player'], data['victim_slot']
        identity = 17 if name == 'kano' else 18
        rows = records(text)
        action = next((r for tag, r in rows if tag == 'ACTION'), None)
        if action is None:
            need(False, case + ': action needed for art binding')
            continue
        start = int(action['frame'])
        arts = [(m[1], dict(re.findall(r'(\w+)=([^\s]+)', m[2])))
                for m in re.finditer(r'^MK2_INFLATION_ART_V938_(\w+) (.*)$', text, re.M)]
        need(bool(arts) and all(r['writes'] == '0' and r['assistance'] == 'none' for tag, r in arts), case + ': read-only native observers')
        def art(tag):
            return [r for t, r in arts if t == tag]
        queues, dmas = art('QUEUE'), art('DMA')
        fifo = {(r['frame'], r['cursor'], r['source']): r for r in queues}
        seen, first_poses, ground_rows = set(), {}, set()
        for q in queues:
            source = int(q['source'], 16)
            bound = source_records.get(source)
            need(bound is not None and bound[0] == name, case + ': every queued sprite is this victim own art')
            if bound is None or bound[0] != name:
                continue
            _, pose, record = bound
            seen.add(pose); first_poses.setdefault(pose, int(q['frame']))
            need(q['actor'] == q['physical'] == q['owner'] == action['victim_actor'] and q['main'] == action['victim_main'] and q['id'] == str(identity),
                 case + ': genuine physical body/owner/ID, no stock substitute or child proxy')
            need(q['pose'] == record['group'], case + ': native actor has correct owned pose group')
            need(q['y'] == q['floor'] and int(q['floor']) == int(q['stageY']) - (134 if name == 'kano' else 135),
                 case + ': original own floor stays fixed')
        for dma in dmas:
            q = fifo.get((dma['frame'], dma['cursor'], dma['source']))
            bound = source_records.get(int(dma['source'], 16))
            need(q is not None and bound is not None and bound[0] == name and dma['queue_match'] == '1', case + ': actual DMA bound to owned FIFO')
            if q is None or bound is None:
                continue
            _, pose, record = bound
            need(dma['fifo_actor'] == dma['fifo_physical'] == action['victim_actor'] and dma['fifo_main'] == action['victim_main'] and dma['fifo_pose'] == record['group'],
                 case + ': physical owned native dispatch')
            need([int(dma['width']), int(dma['height'])] == record['size'] and int(dma['palette'], 16) == (int(q['bank'], 16) & 0x7f00) and
                 int(dma['command'], 16) == (int(q['command'], 16) >> 16), case + ': native dimensions/command/actual palette bank')
            ground = int(q['stageY']) + 5 + int(q['displayY']) - int(q['cameraY']) - 1 - (int(q['displayY']) & 256)
            need((int(dma['y']) & 255) + int(dma['height']) - 1 == ground, case + ': every inflation pose contacts native raster floor')
            ground_rows.add(ground)
        need(seen == set(range(6)) and len(queues) == len(dmas) == 175, case + ': all six genuine native poses rendered')
        ages = (181, 213, 221, 229, 237, 353) if side == 1 else (182, 214, 222, 230, 238, 354)
        need([first_poses.get(pose, -1) - start for pose in range(6)] == list(ages), case + ': unchanged native six-pose choreography')
        # Kitana's kiss task holds the native camera at -8 while this body
        # exists; Reptile's different winner choreography shifts it later.
        # Every QUEUE/DMA above independently checks actual stage/page/camera
        # projection. Do not demand unrelated Reptile-only camera phases.
        need(ground_rows == {228}, case + ': measured native kiss-explosion floor phase')
        snapshots = art('POSE_SNAPSHOT')
        need(len(snapshots) == 6, case + ': actual images for all six displayed poses')
        for snap in snapshots:
            bound = source_records.get(int(snap['source'], 16))
            need(bound is not None and bound[0] == name, case + ': own snapshot source')
            if bound is None:
                continue
            need(int(snap['queued_frame']) == first_poses.get(bound[1]) and int(snap['frame']) == int(snap['queued_frame']) + 1,
                 case + ': snapshot at native next-field presentation, not prior back page')
            path = directory / 'snap' / snap['file']
            need(path.is_file() and Image.open(path).size == (400, 254), case + ': actual six-pose snapshot')
            if check_files and path.is_file(): pins[str(path)] = digest(path)
        palettes = art('PALETTE_DUMP')
        need(len(palettes) == 6, case + ': hardware palette evidence for every pose')
        for r in palettes:
            source = int(r['source'], 16)
            path = directory / r['file']
            need(path.is_file() and path.stat().st_size == 256, case + ': hardware pen dump')
            if path.is_file() and path.stat().st_size == 256:
                actual = struct.unpack('<64I', path.read_bytes())
                need(source in pen_colors and tuple(actual[1:]) == tuple(pen_colors.get(source, [])[1:]), case + ': actual native costume/blood RGB pens')
                if check_files: pins[str(path)] = digest(path)
        gfx = directory / 'native_inflation_gfx.bin'
        need(gfx.read_bytes() == payload[assets.PIXELS:assets.PIXELS + 162308], case + ': initialized native graphics equal all twelve owned sprites')
        stop = art('RESULT')
        need(len(stop) == 1 and int(stop[0]['native_dma']) == 175 and int(stop[0]['first']) == first_poses.get(0) and
             int(stop[0]['last']) == first_poses.get(5, -10) + 2 and int(stop[0]['last']) < 4198,
             case + ': three-field burst then original actor/art retirement before continue')
        if check_files: pins[str(gfx)] = digest(gfx)
        if case in summaries:
            summaries[case].update(ownedPoses=sorted(seen), nativeOwnedDMAs=len(dmas),
                                   poseSnapshots=len(snapshots), hardwarePaletteDumps=len(palettes),
                                   rasterGroundRows=sorted(ground_rows), nativeFirstPoseAges=list(ages))


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
        need(case == f'audit_v987_kitana_{name}_p{side}_owned_inflation', case + ': exact case identity')
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
                               and r.get('header_victim') == name and r.get('side') == str(side)
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
        need(guest == wanted, case + ': whole guest equals five intended table extensions plus only owned inflation assets')
        if check_files:
            for file in ('run.log', 'result.json', 'guest_maincpu.bin', 'native_death_gfx.bin'):
                pins[str(directory / file)] = digest(directory / file)
        summaries[case] = {'victim': name, 'slot': side, 'damage': damage, 'action': start,
                           'nativeCompletionAge': int(wrap['age']), 'snapshots': len(displays),
                           'tableRowsObserved': len(parameters) + len(gore),
                           'nativeTableStabilityAccepted': True, 'ownedInflationArtworkAccepted': False}
    for file in ('mk2ks_stock_head_victim_v921.lua', 'mk2ks_native_inflation_display_v939.lua'):
        source = (ROOT / file).read_text(encoding='utf-8-sig')
        need(not re.search(r'\bp:write_|\.value\s*=(?!=)|load_state|loadstate', source), 'Observers remain read-only: ' + file)
    verify_owned_art(texts, need, summaries, pins, check_files)
    return {'passed': not errors, 'errors': errors, 'fiveNativeVictimTablesAcceptance': not errors,
            'ownedSixPoseInflationNativeRuntimeAcceptance': not errors,
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
