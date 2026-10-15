"""Controlled native alternate branch proof; NEVER natural-selection acceptance."""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
import numpy as np
from PIL import Image
import verify_native_torso_art_v980 as normal
import check_native_torso_pictures_v981 as pictures

ROOT = normal.ROOT


def rgb555(v):
    channels = [(v >> shift) & 31 for shift in (10, 5, 0)]
    r, g, b = [(x << 3) | (x >> 2) for x in channels]
    return (r << 16) | (g << 8) | b


def verify():
    base = normal.verify()
    errors = [] if base['passed'] else ['Current unassisted normal matrix failed']
    pins = dict(base['inputHashes'])
    cases = {}
    def need(ok, label):
        if not ok:
            errors.append(label)
    assets = normal.assets
    payload = (ROOT / normal.PROFILES['current'][0] / 'roms/mk2ks/mk2ks.mdata').read_bytes()
    donor = (ROOT / 'mk3/mk3-maincpu.bin').read_bytes()
    report = json.loads((ROOT / 'audit_v977_owned_torso_blood_encoding/report.json').read_text())
    poses = report['fighters']['kano']['poses']
    sources = {int(c['graphics'], 16): (pose, c) for pose in poses for c in pose['components']}
    words = struct.unpack_from('<64H', donor, 0x92c3e + 4)
    alternate_rgb = [0] + [rgb555(v) for v in words[:63]]
    for pen in (48, 46, 63):
        value = alternate_rgb[pen]
        r, g, b = value >> 16, value >> 8 & 255, value & 255
        need(r > 40 and r > 2 * g and r > 2 * b, 'Actual alternate blood pens are red')
    for side in (1, 2):
        case = f'audit_v983_cage_kano_p{side}_alt_diagnostic'
        folder = ROOT / case
        result = json.loads((folder / 'result.json').read_text(encoding='utf-8-sig'))
        text = (folder / 'run.log').read_text(encoding='utf-8-sig')
        need(result['assistance'] == 'controlled_alt_flag' and result['exit_code'] == 0
             and result['executable_sha256'] == normal.PROFILES['current'][3]
             and result['payload_sha256'] == normal.PROFILES['current'][4]
             and result['victim_slot'] == side and result['winner_slot'] == 3-side
             and result['player'] == 'kano' and result['killer'] == 'cage'
             and result['command'] == 'ddff_lp' and result['target_gap'] == 64
             and result['seconds'] == 95 and result['cheats_enabled'] is False,
             case + ': explicitly assisted matched diagnostic, not ordinary play')
        for file, expected in result['input_hashes'].items():
            path = Path(file)
            need(path.is_file() and normal.digest(path) == expected, case + ': unchanged frozen diagnostic input')
            pins[file] = expected
        rows = normal.records(text, 'MK2_STOCK_HEAD_V921')
        def items(tag):
            return [r for t, r in rows if t == tag]
        actions, wraps, stop = items('ACTION'), items('WRAP'), items('RESULT')
        need(len(actions) == len(wraps) == len(stop) == 1, case + ': exactly one complete native action')
        if len(actions) != 1 or len(wraps) != 1 or len(stop) != 1:
            continue
        action = actions[0]
        start = int(action['frame'])
        need(action['damage'] == '322' and action['mode'] == '2'
             and items('FIRST_LIVE')[0]['ids'] == '2,17'
             and action['actor'] != action['victim_actor'], case + ': true Cage/Kano owners and IDs')
        collisions = [r for r in items('HEALTH') if r['pc'] == 'FF836700' and int(r['frame']) <= start]
        need(len(collisions) == 10 and sum(int(r['before'])-int(r['after']) for r in collisions) == 322
             and sum(r['after'] == '0' for r in collisions) == 2 and len(items('WIN')) == 2,
             case + ': real collision damage and two KOs')
        writers = {'FF836700', 'FF825930' if side == 1 else 'FF825960',
                   'FF9DECE0' if side == 1 else 'FF9DED10', 'FF9DEF40' if side == 1 else 'FF9DEF70'}
        need(all(r['pc'] in writers for r in items('HEALTH')), case + ': no health injection')
        approach = items('APPROACH')
        need(len(approach) == 1, case + ': physical spacing gate')
        if len(approach) == 1:
            beginning = int(approach[0]['frame'])
            forward = 'Left' if side == 1 else 'Right'
            need(start == beginning+44 and all(any(int(r['frame']) == beginning+age
                 and r['slot'] == str(3-side) and r['button'] == button for r in items('INPUT'))
                 for age, button in ((10,'Down'),(18,'Down'),(26,forward),(34,forward),(42,'Low_Punch'))),
                 case + ': original physical fatality command')
        compared = [r for r in items('COMPARE') if int(r['frame']) == start]
        need(len(compared) == 4 and all(r['wanted'] == r['actual'] for r in compared), case + ': original command parser')
        need(wraps[0]['age'] == '185' and wraps[0]['actor'] == action['actor']
             and int(wraps[0]['frame']) == start+185 and wraps[0]['pc'] == 'FF8CDC50'
             and stop[0]['frame'] == '5198' and stop[0]['damage'] == '322' and stop[0]['wins'] == '2'
             and any(r['mode'] == '3' and int(r['frame']) > start+185 for r in items('MODE')),
             case + ': native completion and continue, no softlock')
        need(not items('CACHE_OVERWRITE') and not any(r['mode'] == '0' and int(r['frame']) > 600 for r in items('MODE'))
             and not re.search(r'\[LUA ERROR\]|fatal error|access violation', text, re.I), case + ': no reset or corruption')
        assists = normal.records(text, 'MK2_CAGE_ALT_V983')
        changes = [r for t,r in assists if t == 'ASSIST']
        finishes = [r for t,r in assists if t == 'RESULT']
        need(len(changes) == len(finishes) == 1, case + ': exactly one declared palette flag assist')
        if len(changes) == 1:
            change = changes[0]
            need(change['actor'] == action['victim_actor'] and change['id'] == '17'
                 and change['side'] == str(side) and int(change['new'],16) == int(change['old'],16)|64
                 and int(change['old'],16)&64 == 0 and int(change['frame']) < start
                 and change['writes'] == '1' and change['natural_selection_verified'] == 'false',
                 case + ': only flag-6 is explicitly assisted')
        need(len(finishes) == 1 and finishes[0]['applied'] == '1' and finishes[0]['writes'] == '1'
             and finishes[0]['natural_selection_verified'] == 'false', case + ': assistance never mislabeled natural')
        palettes = items('PALETTE')
        need(len(palettes) == 2 and all(r['pointer'] == 'FFF8A800' and r['id'] == '17'
             and int(r['flags'],16)&64 for r in palettes), case + ': both native parts select actual alternate record')
        art = normal.records(text, 'MK2_CAGE_TORSO_V979')
        queues = [r for t,r in art if t == 'QUEUE' and int(r['source'],16) in sources]
        dmas = [r for t,r in art if t == 'DMA' and int(r['source'],16) in sources]
        by_fifo = {(r['frame'],r['cursor'],r['source']):r for r in queues}
        seen = set()
        grounded = {5:0,6:0}
        for dma in dmas:
            pose, component = sources[int(dma['source'],16)]
            q = by_fifo.get((dma['frame'],dma['cursor'],dma['source']))
            need(q is not None and dma['queue_match'] == '1', case + ': exact DMA/FIFO binding')
            if q is None:
                continue
            need(q['id'] == '17' and q['owner'] == action['victim_actor']
                 and q['physical'] == action['victim_actor'] and int(q['body'],16)&64
                 and q['pose'] == pose['group'], case + ': true owned alternate section')
            need((q['actor'] != q['physical']) == (pose['pose'] == 6), case + ': independently owned lower stump')
            need([int(dma['width']),int(dma['height'])] == component['size']
                 and int(dma['palette'],16) == int(q['bank'],16)&0x7f00,
                 case + ': actual native descriptor geometry/palette')
            seen.add(pose['pose'])
            if pose['pose'] == 6 or (pose['pose'] == 5 and q['y'] == q['floor']):
                row = int(q['stageY'])+5+int(q['displayY'])-int(q['cameraY'])-1-(int(q['displayY'])&256)
                need((int(dma['y'])&255)+int(dma['height'])-1 == row, case + ': native floor contact')
                grounded[pose['pose']] += 1
        need(seen == {0,1,2,3,5,6} and len(dmas) == len(queues) == 2236
             and grounded[6] == 1092 and grounded[5] > 900, case + ': all dispatched native parts and sustained grounding')
        dumps = [r for t,r in art if t == 'PALETTE_DUMP']
        need(len(dumps) == 12, case + ': every dispatched component has actual palette proof')
        for r in dumps:
            path = folder/r['file']
            need(list(struct.unpack('<64I',path.read_bytes()))[1:] == alternate_rgb[1:],
                 case + ': actual native hardware costume/blood palette')
            pins[str(path)] = normal.digest(path)
        need((folder/'guest_maincpu.bin').read_bytes() == normal.expected_guest(payload), case + ': unchanged whole guest code')
        count = struct.unpack_from('<I',payload,assets.HEADER+8)[0]
        need((folder/'native_torso_gfx.bin').read_bytes() == payload[assets.PIXELS:assets.PIXELS+count], case + ': actual new packed graphics')
        matches = pictures.check_case(case,979,payload,normal.records)
        need(len(matches) == 6 and min((r['score'] for r in matches),default=0) >= 0.5,
             case + ': actual presented alternate-colored section pixels')
        for r in matches:
            pins[r['snapshot']] = normal.digest(Path(r['snapshot']))
        for filename in ('run.log','result.json','guest_maincpu.bin','native_torso_gfx.bin'):
            path = folder/filename
            pins[str(path)] = normal.digest(path)
        cases[case] = dict(nativeDamage=322,nativeWrapAge=185,sectionDMAs=len(dmas),
                           groundedLowerDMAs=grounded[6],groundedUpperDMAs=grounded[5],
                           actualHardwarePaletteDumps=len(dumps),actualPresentedPixelMatches=matches,
                           explicitlyAssistedWrites=1,naturalAlternateSelectionAccepted=False)
    return dict(passed=not errors,errors=sorted(set(errors)),cases=cases,inputHashes=pins,
                scope='Two explicitly assisted Kano native alternate-palette branch cases, Dead Pool only',
                controlledNativeAlternateBloodBranchAccepted=not errors,
                naturalAlternateSelectionAccepted=False,fullAlternateCostumeAcceptance=False,
                allArenasAcceptance=False,fullPortAcceptance=False)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():
        raise ValueError('Preserve alternate diagnostic evidence')
    report=verify()
    args.output.mkdir()
    (args.output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','cases')},indent=2))
    raise SystemExit(0 if report['passed'] else 1)
