"""Independent physical/native-DMA proof for owned Cage victim body sections.

Does not accept alternate costumes, all arenas, unused native poses or the
whole port. First v954 geometry is intentionally rejected for floor contact.
"""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
from PIL import Image
import numpy as np
import build_native_torso_art_v977 as assets
import build_native_pit_fall_v2 as colors
import build_native_death_art_v900 as death
import verify_native_inflation_art_v941 as previous
import check_native_torso_pictures_v981 as pictures

ROOT = assets.ROOT
PROFILES = {
    'first': ('diagnostic_v954_owned_cage_torso_art', 955, 'audit_v952_owned_torso_encoding',
              '2C5DDA6ADBED05577D9593DAA8918137F4FB2E4AC8EE9236104B91A55AE75D1B',
              '4C3846424CE5F439738E48A7FD5731E6722C4CE2DB1DF9F4EAB26EEDAED42E86'),
    'current': ('diagnostic_v978_owned_torso_invariant_blood', 979, 'audit_v977_owned_torso_blood_encoding',
                '885B1A50DB68F6806C8A3B32DA329CAA87CCAC7636ADDB3D0283D83850023D1D',
                '2679C041539C99F917CE1A9AAADAE455859A20DA5F5CC8AF9FB6013DB6A79F79')}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def records(text, prefix):
    result = []
    for match in re.finditer(r'^' + re.escape(prefix) + r'_(\w+) (.*)$', text, re.M):
        row = dict(re.findall(r'(\w+)=([^\s]+)', match[2]))
        if prefix == 'MK2_STOCK_HEAD_V921':
            # FIRST_LIVE's actor address also has the key "victim". Bind
            # the scenario header separately, never conflate those fields.
            header = re.match(r'frame=\d+ victim=(kano|sonya) side=[12] killer=cage writes=0 assistance=none ', match[2])
            row['header_victim'] = header[1] if header else 'invalid'
        result.append((match[1], row))
    return result


def expected_guest(payload):
    guest = bytearray(previous.expected_guest())
    guest[assets.ROM_DESCRIPTORS:assets.ROM_DESCRIPTORS + 560] = payload[assets.DESCRIPTORS:assets.DESCRIPTORS + 560]
    guest[assets.ROM_GROUPS:assets.ROM_GROUPS + 168] = payload[assets.GROUPS:assets.GROUPS + 168]
    return bytes(guest)


def verify(texts=None, check_files=True, profile='current'):
    candidate, version, encoded, executable_sha, payload_sha = PROFILES[profile]
    cases = tuple(f'audit_v{version}_cage_{name}_p{side}_owned_torso' for name in ('kano', 'sonya') for side in (1, 2))
    if texts is None:
        texts = {case: (ROOT / case / 'run.log').read_text(encoding='utf-8-sig') for case in cases}
    errors, pins, summaries = [], {}, {}
    def need(ok, label):
        if not ok:
            errors.append(label)
    payload = (ROOT / candidate / 'roms/mk2ks/mk2ks.mdata').read_bytes()
    source = (ROOT / 'diagnostic_v936_owned_inflation_art/roms/mk2ks/mk2ks.mdata').read_bytes()
    donor = (ROOT / 'mk3/mk3-maincpu.bin').read_bytes()
    report = json.loads((ROOT / encoded / 'report.json').read_text())
    need(assets.sha(payload) == payload_sha and assets.sha(source) == assets.SOURCE_SHA, 'Exact current and immutable base payloads')
    need(assets.sha(donor) == death.DONOR_SHA.upper(), 'Original immutable costume palette source')
    allowed = np.zeros(len(source), dtype=bool)
    allowed[assets.HEADER:assets.END] = True
    for stream in assets.STREAMS:
        at = death.offset(stream)
        for word in set(assets.GROUP_WORDS) | set(assets.RAW_WORDS):
            allowed[at + word * 4:at + word * 4 + 4] = True
    a, b = np.frombuffer(source, dtype=np.uint8), np.frombuffer(payload, dtype=np.uint8)
    need(not np.any((a != b) & ~allowed), 'Only private art and typed main57 pointers change')
    need(source[assets.HEADER:assets.END] == b'\xff' * (assets.END - assets.HEADER), 'Previously empty private payload storage')
    byte_count = struct.unpack_from('<I', payload, assets.HEADER + 8)[0]
    need(struct.unpack_from('<4s11I', payload, assets.HEADER) ==
         (b'KTR1', assets.PIXELS, byte_count, assets.GFX, assets.DESCRIPTORS, assets.ROM_DESCRIPTORS,
          28, 20, assets.GROUPS, assets.ROM_GROUPS, 168, 7) and 0 < byte_count <= assets.END - assets.PIXELS,
         'Exact bounded native section header')
    by_source, palette_colors, descriptor_index, group_at = {}, {}, 0, assets.GROUPS
    for fighter, name in enumerate(('kano', 'sonya')):
        for file in (name + '-upper-torsos.png', 'lower-stumps.png'):
            path = ROOT / 'art_native_torso_v951' / file
            need(digest(path) == assets.ASSETS[file], 'Immutable selected art: ' + file)
            pins[str(path)] = digest(path)
        upper = Image.open(ROOT / 'art_native_torso_v951' / (name + '-upper-torsos.png')).convert('RGBA')
        lower = Image.open(ROOT / 'art_native_torso_v951/lower-stumps.png').convert('RGBA')
        cells = [upper.crop((i % 3 * 512, i // 3 * 512, (i % 3 + 1) * 512, (i // 3 + 1) * 512)) for i in range(6)]
        cells += [lower.crop((fighter * 627, 0, (fighter + 1) * 627, 1254))]
        crops = []
        boxes = []
        for cell in cells:
            box = cell.getchannel('A').point(lambda v: 255 if v >= 128 else 0).getbbox()
            need(box is not None and min(box[:2]) >= 2 and box[2] < cell.width and box[3] < cell.height, 'Unclipped genuine-alpha section')
            crops.append(cell.crop(box))
            boxes.append(box)
        guides = []
        if fighter == 0:
            for filename, expected in assets.GUIDES.items():
                path = ROOT / 'art_native_torso_blood_v976' / filename
                need(digest(path) == expected, 'Immutable image_gen blood guide: ' + filename)
                pins[str(path)] = digest(path)
            upper_guide = Image.open(ROOT / 'art_native_torso_blood_v976/kano-upper-blood-guide.png').convert('RGBA')
            lower_guide = Image.open(ROOT / 'art_native_torso_blood_v976/lower-blood-guide.png').convert('RGBA')
            guide_cells = [upper_guide.crop((i % 3 * 512, i // 3 * 512, (i % 3 + 1) * 512, (i // 3 + 1) * 512)) for i in range(6)]
            guide_cells += [lower_guide.crop((0, 0, 627, 1254))]
            guides = [cell.crop(box) for cell, box in zip(guide_cells, boxes)]
        factor = 76 / crops[0].height
        lower_bottom = 141 if profile == 'current' else 140 + fighter
        normal = colors.palette(donor, (0x92bbc, 0x92cf2)[fighter])
        alternate = colors.palette(donor, (0x92c3e, 0x92d74)[fighter])
        palette_words = struct.unpack_from('<64H', donor, (0x92bbc, 0x92cf2)[fighter] + 4)
        rgb = [0] + [((((v >> 10 & 31) << 3) | (v >> 12 & 7)) << 16) |
                     ((((v >> 5 & 31) << 3) | (v >> 7 & 7)) << 8) |
                     (((v & 31) << 3) | (v >> 2 & 7)) for v in palette_words[:63]]
        groups, descriptors = [], []
        for pose, image in enumerate(crops):
            scale = factor if pose < 6 else (lower_bottom - 47) / image.height
            width, height = round(image.width * scale), round(image.height * scale)
            if pose < 6:
                native = assets.BOUNDS[pose]
                left, bottom = round((native[0] + native[2] - width) / 2), native[3]
                if pose == 5 and profile == 'current':
                    bottom = 59 + fighter
            else:
                left, bottom = round((5 - width) / 2), lower_bottom
            top = bottom - height
            scaled = image.resize((width, height), Image.Resampling.LANCZOS)
            indices = colors.quantize(scaled, normal)
            if fighter == 0:
                # Independent source classification, not the builder's function.
                original = indices.copy()
                coded = np.asarray(guides[pose].resize((width, height), Image.Resampling.LANCZOS)).astype(np.int32)
                rgba = np.asarray(scaled).astype(np.int32)
                marker = ((coded[:, :, 3] >= 128) & (coded[:, :, 1] - coded[:, :, 0] >= 20)
                          & (coded[:, :, 2] - coded[:, :, 0] >= 20)
                          & (coded[:, :, 1] >= coded[:, :, 2] / 2)
                          & (coded[:, :, 2] >= coded[:, :, 1] / 2)
                          & (rgba[:, :, 0] > np.maximum(rgba[:, :, 1], rgba[:, :, 2]) * 1.2 + 8)
                          & (original != 0))
                pens = np.array([48, 46, 63], dtype=np.uint8)
                ramp = normal[pens].astype(np.int32)
                distance = ((rgba[:, :, None, :3] - ramp[None, None, :, :]) ** 2).sum(axis=3)
                indices[marker] = pens[distance.argmin(axis=2)[marker]]
                need(np.array_equal(normal[pens], alternate[pens]) and marker.any(), 'Blood pens red and invariant across native costumes')
                need(np.array_equal(indices == 0, original == 0) and np.array_equal(indices[~marker], original[~marker]),
                     'Original silhouettes and nonblood costume indices untouched')
                need(int(marker.sum()) == report['fighters'][name]['poses'][pose]['blood_pixels'], 'Independent blood-guide coverage')
            pointers = []
            for col in range(assets.COUNTS[pose]):
                x0, x1 = col * width // assets.COUNTS[pose], (col + 1) * width // assets.COUNTS[pose]
                at = assets.DESCRIPTORS + descriptor_index * 20
                dw, dh, xo, yo, graphic, command, pal, pad = struct.unpack_from('<4hIHIH', payload, at)
                need((dw, dh, xo, yo, command, pal, pad) ==
                     (x1 - x0, height, -left - x0, -top, 0x6000, assets.address((0xfda00, 0xfdb00)[fighter]), 0),
                     'Independent owned geometry/palette/component: ' + name + str(pose))
                pixel_at = assets.PIXELS + graphic // 8 - assets.GFX
                length = (dw * dh * 6 + 7) // 8
                need(graphic % 8 == 0 and assets.PIXELS <= pixel_at and pixel_at + length <= assets.PIXELS + byte_count,
                     'Bounded aligned native graphics pointer')
                raw = death.unpack(payload[pixel_at:pixel_at + length], dw * dh)
                need(raw == indices[:, x0:x1].copy().tobytes(), 'Native pixels exactly match selected PNG conversion')
                pointer = assets.address(assets.ROM_DESCRIPTORS + descriptor_index * 20)
                pointers.append(pointer)
                by_source[graphic] = dict(name=name, pose=pose, group=assets.address(assets.ROM_GROUPS + group_at - assets.GROUPS),
                                          size=[dw, dh], descriptor=pointer, bounds=[left + x0, top, left + x1, bottom])
                palette_colors[graphic] = rgb
                descriptor_index += 1
            need(struct.unpack_from('<' + str(len(pointers) + 1) + 'I', payload, group_at) == (*pointers, 0),
                 'Original native component count and zero termination')
            groups.append(assets.address(assets.ROM_GROUPS + group_at - assets.GROUPS))
            if pose < 6:
                descriptors += pointers
            group_at += (len(pointers) + 1) * 4
        original = list(struct.unpack_from('<52I', source, death.offset(assets.STREAMS[fighter])))
        wanted = original.copy()
        for word, pose in assets.GROUP_WORDS.items():
            wanted[word] = groups[pose]
        for word, pointer in zip(assets.RAW_WORDS, descriptors):
            wanted[word] = pointer
        need(struct.unpack_from('<52I', payload, death.offset(assets.STREAMS[fighter])) == tuple(wanted),
             'Entire native main57 control grammar; only typed owned references change')
    need(set(texts) == set(cases), 'Both true-ID victims in both physical slots')
    prior_payload = (ROOT / 'diagnostic_v958_owned_cage_torso_grounding/roms/mk2ks/mk2ks.mdata').read_bytes()
    delta = np.frombuffer(prior_payload, dtype=np.uint8) != np.frombuffer(payload, dtype=np.uint8)
    need(not delta[:assets.PIXELS].any() and not delta[assets.PIXELS + byte_count:].any(),
         'Blood revision changes graphics bytes only; no native code, descriptors, palettes or selectors')
    for case, text in texts.items():
        directory = ROOT / case
        result = json.loads((directory / 'result.json').read_text(encoding='utf-8-sig'))
        name, side = result['player'], result['victim_slot']
        identity = 17 if name == 'kano' else 18
        need(result['executable_sha256'] == executable_sha and result['payload_sha256'] == payload_sha,
             case + ': exact matched candidate')
        need(result['exit_code'] == 0 and result['seconds'] == 95 and result['winner_slot'] == 3 - side and
             result['killer'] == 'cage' and result['command'] == 'ddff_lp' and result['target_gap'] == 64 and
             result['assistance'] == 'none' and result['cheats_enabled'] is False, case + ': genuine physical-input scenario')
        if check_files:
            for file, digest_wanted in result['input_hashes'].items():
                path = Path(file)
                need(path.is_file() and digest(path) == digest_wanted, 'Frozen input changed: ' + file)
                pins[file] = digest_wanted
        need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at', text, re.I), case + ': no runtime error')
        rows = records(text, 'MK2_STOCK_HEAD_V921')
        need(all(r.get('writes') == '0' and r.get('assistance') == 'none' and r.get('header_victim') == name
                 and r.get('side') == str(side) and r.get('killer') == 'cage' for _, r in rows), case + ': consistent physical scenario')
        def items(tag):
            return [r for t, r in rows if t == tag]
        actions, wraps, terminal = items('ACTION'), items('WRAP'), items('RESULT')
        need(len(actions) == len(wraps) == len(terminal) == 1, case + ': one complete native action')
        if len(actions) != 1 or len(wraps) != 1 or len(terminal) != 1:
            continue
        action, wrap, stop = actions[0], wraps[0], terminal[0]
        start = int(action['frame'])
        need(action['damage'] == '322' and action['mode'] == '2' and action['actor'] != action['victim_actor']
             and action['main'] != action['victim_main'], case + ': distinct native owners')
        live = items('FIRST_LIVE')
        need(len(live) == 1 and live[0]['ids'] == f'2,{identity}' and live[0]['own'] == action['actor']
             and live[0]['victim'] == action['victim_actor'], case + ': actual Cage and added victim, no proxy')
        writers = {0xff836700, 0xff825930 if side == 1 else 0xff825960,
                   0xff9dece0 if side == 1 else 0xff9ded10, 0xff9def40 if side == 1 else 0xff9def70}
        collisions = []
        for row in items('HEALTH'):
            need(int(row['pc'], 16) in writers, case + ': original health writer')
            if row['pc'] == 'FF836700' and int(row['frame']) <= start:
                need(0 <= int(row['after']) <= int(row['before']) <= 161, case + ': native collision bounds')
                collisions.append(row)
        need(len(collisions) == 10 and sum(int(r['before']) - int(r['after']) for r in collisions) == 322
             and sum(r['after'] == '0' for r in collisions) == 2 and len(items('WIN')) == 2, case + ': two real KOs')
        need(not items('CACHE_OVERWRITE') and not any(r['mode'] == '0' and int(r['frame']) > 600 for r in items('MODE')),
             case + ': no cache overrun or gameplay reset')
        approach = items('APPROACH')
        need(len(approach) == 1, case + ': physical native distance gate')
        if len(approach) == 1:
            beginning = int(approach[0]['frame'])
            forward = 'Left' if side == 1 else 'Right'
            need(start == beginning + 44 and all(any(int(r['frame']) == beginning + age and
                 r['button'] == button and r['slot'] == str(3 - side) for r in items('INPUT'))
                 for age, button in ((10, 'Down'), (18, 'Down'), (26, forward), (34, forward), (42, 'Low_Punch'))),
                 case + ': real Down Down Forward Forward LP command')
        compared = [r for r in items('COMPARE') if int(r['frame']) == start]
        need(len(compared) == 4 and all(r['wanted'] == r['actual'] for r in compared), case + ': native command parser acceptance')
        need(int(wrap['age']) == 185 and int(wrap['frame']) == start + 185 and wrap['pc'] == 'FF8CDC50'
             and wrap['actor'] == action['actor'], case + ': unchanged original completion')
        need(stop['frame'] == '5198' and stop['damage'] == '322' and stop['wins'] == '2' and
             int(stop['action']) == start and int(stop['wrap']) == start + 185 and
             any(r['mode'] == '3' and int(r['frame']) > start + 185 for r in items('MODE')), case + ': real continue screen')
        need(any(r['index'] == '00000039' and r['actor'] == action['victim_actor'] and
                 r['main'] == action['victim_main'] for r in items('LOOKUP')), case + ': own main57 native selection')
        need([int(r['age']) for r in items('DISPLAY')] == list(range(0, 601, 10)), case + ': full screenshot chronology')
        for age in range(0, 601, 10):
            picture = directory / 'snap' / f'stock_head_{start}_{age:03d}.png'
            need(picture.is_file() and Image.open(picture).size == (400, 254), case + ': actual scene image')
            if picture.is_file():
                pins[str(picture)] = digest(picture)
        need((directory / 'guest_maincpu.bin').read_bytes() == expected_guest(payload), case + ': whole guest only private section additions')
        need((directory / 'native_torso_gfx.bin').read_bytes() == payload[assets.PIXELS:assets.PIXELS + byte_count],
             case + ': actual initialized section graphics exact')
        art = records(text, f'MK2_CAGE_TORSO_V{version}')
        need(all(r['writes'] == '0' and r['assistance'] == 'none' for _, r in art), case + ': read-only observers')
        queues = [r for t, r in art if t == 'QUEUE' and int(r['source'], 16) in by_source]
        dmas = [r for t, r in art if t == 'DMA' and int(r['source'], 16) in by_source]
        fifo = {(r['frame'], r['cursor'], r['source']): r for r in queues}
        seen, first, grounded_upper, grounded_lower = set(), {}, 0, 0
        for dma in dmas:
            component = by_source[int(dma['source'], 16)]
            q = fifo.get((dma['frame'], dma['cursor'], dma['source']))
            need(q is not None and dma['queue_match'] == '1', case + ': actual DMA has exact current-field FIFO')
            if q is None:
                continue
            pose = component['pose']
            need(component['name'] == name and q['id'] == str(identity) and q['physical'] == action['victim_actor']
                 and q['main'] == action['victim_main'] and q['owner'] == action['victim_actor'], case + ': genuine section owner and ID')
            need(q['actor'] != q['physical'] if pose == 6 else q['actor'] == q['physical'], case + ': separate native stump and real upper actor')
            need(int(q['pose'], 16) == component['group'] and dma['fifo_actor'] == q['actor'] and
                 dma['fifo_physical'] == q['physical'] and dma['fifo_main'] == q['main'] and dma['fifo_pose'] == q['pose'],
                 case + ': correct native section object and group')
            need([int(dma['width']), int(dma['height'])] == component['size'] and
                 int(dma['palette'], 16) == (int(q['bank'], 16) & 0x7f00) and
                 int(dma['command'], 16) == int(q['command'], 16) >> 16, case + ': native geometry/command/palette bank')
            ground = int(q['stageY']) + 5 + int(q['displayY']) - int(q['cameraY']) - 1 - (int(q['displayY']) & 256)
            if pose == 6 or (pose == 5 and q['y'] == q['floor']):
                need((int(dma['y']) & 255) + int(dma['height']) - 1 == ground, case + ': every grounded section contacts native raster floor')
                if pose == 6:
                    grounded_lower += 1
                else:
                    grounded_upper += 1
            seen.add(pose)
            first.setdefault(pose, int(dma['frame']) - start)
        need(seen == {0, 1, 2, 3, 5, 6} and first == {0: 70, 1: 74, 2: 130, 3: 134, 5: 138 if side == 1 else 139, 6: 70},
             case + ': unchanged original visible-pose choreography; native pose4 is not dispatched here')
        need(len(queues) == len(dmas) and len(dmas) > 1000 and grounded_upper > 100 and grounded_lower > 100,
             case + ': actual section DMA and sustained floor contact')
        need(not any(t == 'ALL_FIFO' and r['id'] == str(identity) and int(r['frame']) >= start + 70 and
                     int(r['source'], 16) not in by_source for t, r in art), case + ': no leftover whole fighter/stock Liu art after split')
        dumps = [r for t, r in art if t == 'PALETTE_DUMP']
        need(len(dumps) == 12, case + ': every original dispatched component has hardware palette evidence')
        for row in dumps:
            path = directory / row['file']
            need(path.is_file() and path.stat().st_size == 256, case + ': actual hardware palette dump')
            if path.is_file() and path.stat().st_size == 256:
                need(list(struct.unpack('<64I', path.read_bytes()))[1:] == palette_colors[int(row['source'], 16)][1:],
                     case + ': actual native costume/blood RGB pens')
                pins[str(path)] = digest(path)
        need(max(int(r['frame']) for r in dmas) < 4198, case + ': sections retire before terminal continuation')
        snapshots = [r for t, r in art if t == 'POSE_SNAPSHOT' and int(r['source'], 16) in by_source]
        need(len(snapshots) == 6 and all(int(r['frame']) == int(r['queued_frame']) + 1 for r in snapshots),
             case + ': six actual next-field section pictures')
        for row in snapshots:
            picture = directory / 'snap' / f"torso_pose_{row['actor_pose']}_{row['frame']}.png"
            need(picture.is_file() and Image.open(picture).size == (400, 254), case + ': displayed section snapshot')
            if picture.is_file():
                pins[str(picture)] = digest(picture)
        for file in ('run.log', 'result.json', 'guest_maincpu.bin', 'native_torso_gfx.bin'):
            pins[str(directory / file)] = digest(directory / file)
        picture_matches = pictures.check_case(case, version, payload, records) if profile == 'current' else []
        if profile == 'current':
            need(len(picture_matches) == 6 and {r['pose'] for r in picture_matches} == {0, 1, 2, 3, 5, 6}
                 and min((r['score'] for r in picture_matches), default=0) >= 0.5,
                 case + ': presented PNG matches actual encoded native section pixels, not prior page')
        summaries[case] = dict(victim=name, slot=side, nativeDamage=322, nativeWrapAge=185, sectionDMAs=len(dmas),
                               groundedLowerDMAs=grounded_lower, groundedUpperDMAs=grounded_upper, originalVisiblePoses=sorted(seen),
                               firstNativePoseAges=first, hardwarePaletteDumps=len(dumps), periodicPictures=61, sectionPictures=len(snapshots),
                               actualNativePixelMatches=picture_matches)
    for file in ('mk2ks_stock_head_victim_v921.lua', f'mk2ks_cage_torso_display_v{version}.lua'):
        need(not re.search(r'\bp:write_|\.value\s*=(?!=)|load_state|loadstate', (ROOT / file).read_text()), 'Read-only game observers: ' + file)
    return dict(passed=not errors, errors=sorted(set(errors)), cases=summaries, inputHashes=pins,
                normalDeadPoolCageSectionNativeRuntimeAcceptance=not errors, normalCageSectionArtworkAcceptance=False,
                alternateCostumeAcceptance=False, unusedNativePose4RuntimeAcceptance=False, allArenasAcceptance=False,
                fullPortAcceptance=False, cageBloodEncodingCostumeInvariant=not errors, knownAlternateKanoBlueBlood=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--profile', choices=PROFILES, default='current')
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('Preserve verification evidence')
    report = verify(profile=args.profile)
    args.output.mkdir()
    (args.output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'inputHashes'}, indent=2))
    raise SystemExit(0 if report['passed'] else 1)
