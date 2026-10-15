"""Both campaign slots: actual selection, pixels, native ladder and first match.

This is not a full tower/continue/ending, every floor-shadow, move or audio gate.
The independent UI-source raster model verifies complete portraits, not color
counts. Original stock cursor pixels are the live control for border/number.
"""
import json
import re
import struct
from pathlib import Path
import numpy as np
from PIL import Image
from verify_cpu_air_gate import ROOT, rows, digest, ORIGINAL_SHA
from verify_cpu_air_runtime import need, n, h
from verify_native_candidate_v517 import NAME, EXE, PAYLOAD
SOURCE = 'B8542F4777E4F100EC4E86771AD70EC867522FE106DD51E6F164E408489722D3'
from verify_p2_campaign import expected_orders

UI_SHA = 'DBC1881B4696ACD33393D47DCBF626239B91EB6D8DB581003D4774A2F97483EB'
SCOPE = 'current_both_slots_selection_navigation_blink_number_animation_backdrop_clear_native_ladder_icons_and_first_match_identity_name_shadow_not_full_tower_continue_endings_floor_shadows_moves_or_audio'


def records(log, tag):
    if tag == 'INPUT':
        # Native field name contains a space. Validate it before representing
        # it as one token; do not silently ignore a bare word in the trace.
        for line in log.splitlines():
            if line.startswith('MK2_UI_INPUT '):
                need(re.fullmatch(r'MK2_UI_INPUT frame=\d+ side=[12] fighter=(?:kano|sonya) writes=0 assistance=none '
                                  r'button=(?:Coin|Start|High Punch|Left|Right|Up|Down|Block) age=\d+', line),
                     'Unambiguous complete native input field')
        log = log.replace('button=High Punch ', 'button=High_Punch ')
    return rows(log, 'MK2_UI_'+tag)


def unique(values, label):
    need(len(values) == 1, 'One actual '+label)
    return values[0]


def launch(folder, fighter, side):
    folder = Path(folder)
    result = json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    need((result['exit_code'], result['candidate'], result['executable_sha256'], result['payload_sha256'],
          result['fighter'], result['side'], result['assistance']) == (0, NAME, EXE, PAYLOAD, fighter, side, 'none'),
         'Exact terminal current native UI launch')
    before = json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need(before == result['input_hashes'], 'Launch inputs match before/after')
    for filename, sha in before.items():
        path = Path(filename)
        need(digest(path) == sha, 'Current launch input changed: '+filename)
        if path.suffix in ('.lua', '.ps1', '.json'):
            need(digest(folder/'input_sources'/path.name) == sha, 'Frozen launch input changed')
    build = json.loads((folder/'input_sources/build-info.json').read_text(encoding='utf-8-sig'))
    need((build['name'], build['executable_sha256'], build['payload_sha256']) == (NAME, EXE, PAYLOAD), 'Current build metadata')
    for filename, sha in build['input_hashes'].items():
        need(digest(filename) == sha, 'Current build input changed')
    need(digest(ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp') == SOURCE and
         digest(ROOT/'mk2/mk2-maincpu.bin') == ORIGINAL_SHA and digest(ROOT/'roms/mk2ks/mk2ks.ui') == UI_SHA,
         'Exact current driver, original MKII and UI source')
    observer = (folder/'input_sources/mk2ks_native_ui_flow_v2_probe.lua').read_text()
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(', observer), 'Standalone observer cannot supply guest state')
    need('-nocheat' in (folder/'input_sources/run_native_ui_flow_v2_probe.ps1').read_text(), 'Cheat-disabled native launch')
    return (folder/'run.log').read_text(encoding='utf-8-sig')


def compiled(log):
    windows = records(log, 'CODE')
    need(len(windows) == 2 and {h(r, 'start'): h(r, 'stop') for r in windows} ==
         {0xfffe1800: 0xfffe2400, 0xffff0800: 0xffff3880}, 'Complete native table readout windows')
    memory = {}
    for r in windows:
        words = [int(w, 16) for w in r['words'].split(',')]
        need(len(words) == (h(r, 'stop')-h(r, 'start'))//16, 'Untruncated table dump')
        memory.update((h(r, 'start')+i*16, w) for i, w in enumerate(words))
    def word(address):return memory[address]
    def long(address):return word(address) | word(address+16)<<16
    ids = (1, 0, 2, 9, 8, 6, 4, 11, 5, 3, 10, 7, 17, 18)
    need(tuple(word(0xffff0c00+i*16) for i in range(14)) == ids, 'Fourteen actual selection IDs, no proxies')
    original = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    original_portraits = struct.unpack_from('<48H', original, (0xff894c00-0xff800000)//8)
    need(tuple(word(0xffff2400+i*16) for i in range(48)) == original_portraits, 'All twelve original portraits unchanged')
    original_ladder = struct.unpack_from('<17I', original, (0xff8a0e70-0xff800000)//8)
    need(tuple(long(0xffff3000+i*32) for i in range(17)) == original_ladder, 'All original ladder entries unchanged')
    for identity, x, css, ladder in ((17, 23, 0xffff2800, 0xffff2a00), (18, 323, 0xffff2900, 0xffff2b00)):
        need((word(0xffff2000+identity*32), word(0xffff2010+identity*32)) == (x, 24), 'Dedicated top-row cell coordinates')
        need((word(0xffff1600+identity*16), word(0xffff1400+identity*16),
              word(0xffff1200+identity*16)) == ((1, 17, 8) if identity == 17 else (18, 9, 11)),
             'Correct right/left/down native neighbor IDs')
        index = 12+identity-17
        need((long(0xffff2400+index*64), word(0xffff2420+index*64), word(0xffff2430+index*64)) == (css, x, 24),
             'Actual added portrait list entry, not an overlay')
        need((word(css), word(css+16), word(ladder), word(ladder+16), long(0xffff3000+identity*32)) ==
             (55, 70, 35, 45, ladder), 'Native CSS/ladder descriptor dimensions and true ID lookup')
    return dict(original_portraits_preserved=12, original_ladder_entries_preserved=17)


def verify_log(log, fighter, side):
    need(fighter in ('kano', 'sonya') and side in (1, 2), 'Declared actual UI character/slot')
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|stack traceback', log, re.I), 'No emulator/observer error')
    groups = {tag: records(log, tag) for tag in ('CODE', 'CSS', 'SELECT', 'INPUT', 'EXIT', 'OUTSIDE', 'LADDER', 'LIVE', 'FIELD', 'SNAP', 'RESULT')}
    for values in groups.values():
        for r in values:
            need((r['fighter'], n(r, 'side'), r['writes'], r['assistance']) == (fighter, side, '0', 'none'),
                 'All observations are actual declared slot and input-only')
    tables = compiled(log)
    css, exit_row, live, result = (unique(groups[tag], tag) for tag in ('CSS', 'EXIT', 'LIVE', 'RESULT'))
    c, e, f, final = (n(r, 'frame') for r in (css, exit_row, live, result))
    need(700 < c < e < f and final == f+180 and (n(result, 'css'), n(result, 'exit'), n(result, 'live'), n(result, 'schema')) ==
         (c, e, f, 1), 'Full native selection, ladder transition and 180 first-match fields')
    selection = groups['SELECT']
    need([n(r, 'frame') for r in selection] == list(range(c, e+1)) and
         all(n(r, 'age') == n(r, 'frame')-c for r in selection), 'Every real selection field through actual exit')
    selected = {n(r, 'age'): n(r, 'roster') for r in selection}
    identity, stock, down = (17, 1, 8) if fighter == 'kano' else (18, 9, 11)
    for age, expected in ((60, identity), (84, stock), (108, identity), (132, stock),
                          (156, identity), (180, down), (204, stock), (228, identity)):
        need(selected.get(age) == expected, 'Actual adjacent and vertical navigation visit '+str(age))
    # A sampled visit alone misses a one-field wrong neighbor between samples.
    # After each real direction pulse settles, require every held selection
    # field until the next pulse, including Sonya -> Jax -> Reptile -> Sonya.
    for first, stop, expected in ((54, 72, identity), (78, 96, stock),
                                 (102, 120, identity), (126, 144, stock),
                                 (150, 168, identity), (174, 192, down),
                                 (198, 216, stock), (222, e-c+1, identity)):
        need(all(selected.get(age) == expected for age in range(first, stop)),
             'Every settled navigation field from age '+str(first))
    need(all(selected.get(age) == identity for age in range(54, 71)) and
         all(selected.get(age) == stock for age in range(78, 95)) and
         all(selected.get(age) == identity for age in range(228, e-c+1)), 'Highlighted native/stock controls and committed true ID')
    outside = groups['OUTSIDE']
    need([n(r, 'frame') for r in outside] == list(range(e, final+1)) and
         all(n(r, 'age') == n(r, 'frame')-e and n(r, 'css') == 0 and n(r, 'refs') == 192 and
             max(n(r, 'kano_matches'), n(r, 'sonya_matches')) < 19 for r in outside),
         'No full-size old portrait signature on any post-selection field')
    ladder = groups['LADDER']
    need({n(r, 'id') for r in ladder} == {17, 18} and bool(ladder), 'Both native character ladder lookups actually executed')
    for r in ladder:
        pid = n(r, 'id')
        need(h(r, 'pc') == 0xff8a0c00 and h(r, 'at') == h(r, 'a0') == 0xffff3000+pid*32 and
             h(r, 'mask') == 0xffff and h(r, 'descriptor') == (0x2a00 if pid == 17 else 0x2b00) and
             c < n(r, 'frame') < f, 'Actual original native ladder table consumer, not Lua read or hint')
    order = (h(live, 'schedule')-0xfffa3000)//0x180
    need(order in range(6) and h(live, 'schedule') == 0xfffa3000+order*0x180 and n(live, 'stage') == 0,
         'First match follows original-derived stage-zero native schedule')
    fields = groups['FIELD']
    need([(n(r, 'frame'), n(r, 'slot')) for r in fields] == [(time, slot) for time in range(f, final+1) for slot in (1, 2)],
         'Every actual participant field for the entire initial match interval')
    base = {slot: next(r for r in fields if n(r, 'slot') == slot) for slot in (1, 2)}
    for r in fields:
        slot = n(r, 'slot');pid = identity if slot == side else expected_orders()[order][0]
        need(n(r, 'age') == n(r, 'frame')-f and n(r, 'id') == n(r, 'roster') == pid and
             n(r, 'state') == (1 if slot == side else 0) and r['actor'] == r['owner'] == base[slot]['actor'] and
             r['main'] == base[slot]['main'] and r['list'] == base[slot]['list'] and
             0x01000000 <= h(r, 'actor') < 0x01100000 and 0x01000000 <= h(r, 'main') < 0x01100000,
             'No Liu proxy or identity replacement from ladder into real owned fighters')
    snaps = groups['SNAP']
    for r in snaps:
        time = n(r, 'frame');scene = r['scene']
        need(r['file'] == f'ui_{time:04d}.png' and time % 2 == 0 and scene in ('select', 'transition', 'fight') and
             n(r, 'age') == time-{'select': c, 'transition': e, 'fight': f}[scene] and
             n(r, 'roster') == (selected[time-c] if scene == 'select' else identity), 'Exact native-size screenshot field and roster label')
    inputs = groups['INPUT']
    need(sum(r['button'] == 'High_Punch' and 264 <= n(r, 'age') < 272 for r in inputs) == 8 and
         {n(r, 'frame') for r in inputs if r['button'] == 'Block'} == set(range(f, final+1)),
         'Real eight-field HP selection and held human Block in first match')
    return dict(passed=True, fighter=fighter, side=side, css=c, exit=e, live=f, terminal=final,
                true_id=identity, cpu_id=expected_orders()[order][0], selection_fields=len(selection),
                outside_fields=len(outside), first_match_participant_fields=len(fields),
                native_ladder_lookups=len(ladder), scope=SCOPE, whole_character_integration_complete=False, **tables)


def portrait(ui, fighter, width, height):
    sw, sh, colors = ui[4], ui[5], int.from_bytes(ui[6:8], 'little')
    offset = 8+fighter*(colors*2+sw*sh)
    palette = np.frombuffer(ui[offset:offset+colors*2], dtype='<u2')
    source = np.frombuffer(ui[offset+colors*2:offset+colors*2+sw*sh], dtype=np.uint8).reshape(sh, sw)
    indices = source[np.arange(height)*sh//height][:, np.arange(width)*sw//width]
    channels = np.stack([(palette>>10)&31, (palette>>5)&31, palette&31], axis=1).astype(int)
    count = 64 if width == 35 else 128
    order = np.argsort(-np.bincount(indices.ravel(), minlength=colors), kind='stable')[:min(count-1, colors)]
    mapping = ((channels[:, None]-channels[order][None])**2).sum(2).argmin(1)
    rgb = channels[order][mapping[indices]]
    return ((rgb<<3)|(rgb>>2)).astype(np.uint8)


def find_portrait(image, template):
    height, width = template.shape[:2]
    yy, xx = np.where(np.all(image == template[0, 0], axis=2))
    for y, x in zip(yy, xx):
        if x+width <= 400 and y+height <= 254 and np.array_equal(image[y:y+height, x:x+width], template):
            return int(x), int(y)
    return None


def shadow(ui, identity, side):
    sw, sh, colors = ui[4], ui[5], int.from_bytes(ui[6:8], 'little')
    names = 8+2*(colors*2+sw*sh);w, height = ui[names:names+2]
    offset = names+2+(identity-17)*w*height
    face = np.frombuffer(ui[offset:offset+w*height], dtype=np.uint8).reshape(height, w)[:10] > 48
    occupied = np.where(face)[1];first, last = int(occupied.min()), int(occupied.max())
    face = face[:, first:last+1];width = face.shape[1]+1
    visible = np.pad(face, ((0, 0), (0, 1)))
    edge = np.zeros(visible.shape, dtype=bool)
    edge[:, 1:] |= visible[:, :-1];edge[1:, 1:] |= visible[:-1, :-1];edge &= ~visible
    return visible, edge, 29 if side == 1 else 367-width


def render(folder, log, fighter, side, load=None):
    ui = (ROOT/'roms/mk2ks/mk2ks.ui').read_bytes()
    snapshots = records(log, 'SNAP');exit_at = n(unique(records(log, 'EXIT'), 'render exit'), 'frame')
    live_at = n(unique(records(log, 'LIVE'), 'render live'), 'frame')
    images = {}
    def image(row):
        filename = row['file']
        if filename not in images:
            value = load(filename) if load else np.asarray(Image.open(folder/'snap'/filename).convert('RGB'))
            need(value.shape == (254, 400, 3) and value.dtype == np.uint8, 'Unscaled 400x254 native screenshot')
            images[filename] = value
        return images[filename]
    selection = {n(r, 'age'): image(r) for r in snapshots if r['scene'] == 'select'}
    left, stock = (19, 79) if fighter == 'kano' else (319, 259)
    ages = sorted(age for age in selection if 54 <= age <= 70)
    need(len(ages) >= 8 and all(age+24 in selection for age in ages), 'Full native and phase-matched stock blink controls')
    border = np.zeros((78, 63), dtype=bool)
    border[:4] = True;border[-4:] = True;border[:, :4] = True;border[:, -4:] = True
    colors = set()
    for age in ages:
        a, b = selection[age], selection[age+24]
        need(np.array_equal(a[20:98, left:left+63][border], b[20:98, stock:stock+63][border]),
             'Four complete native border segments: same thickness, placement and blink as stock')
        color = a[25, left];colors.add(tuple(map(int, color)))
        y1, y2 = (30, 56) if side == 1 else (62, 87)
        native = np.all(a[y1:y2, left+24:left+40] == color, axis=2)
        original = np.all(b[y1:y2, stock+24:stock+40] == color, axis=2)
        need(np.array_equal(native, original) and int(native.sum()) == (66 if side == 1 else 84),
             'Complete player-number glyph mask and original placement, not just colored pixels')
    need(len(colors) >= 2, 'Cursor continues blinking on imported character')
    inactive = selection[ages[0]+24]
    for index, x in enumerate((23, 323)):
        need(np.array_equal(inactive[24:94, x:x+55], portrait(ui, index, 55, 70)),
             'Every unselected native portrait pixel equals source-authored raster: no player number/hint')
    xx = np.arange(5, 74, 2) if side == 1 else np.arange(325, 394, 2)
    yy = np.arange(110, 241, 2)
    native, original = selection[ages[0]], inactive
    scores = {(dx, dy): int(np.all(native[yy[:, None], xx] == original[(yy+dy)[:, None], xx+dx], axis=2).sum())
              for dy in range(-2, 3) for dx in range(-2, 3)}
    runner_up = max(value for key, value in scores.items() if key != (0, 0))
    need(max(scores, key=scores.get) == (0, 0) and scores[0, 0] > 500 and scores[0, 0] > runner_up*2,
         'Selected stance backdrop has no one/two-pixel shift relative to stock')
    changed = int(np.any(native[110:241, xx[0]:xx[-1]+1] != selection[ages[-1]][110:241, xx[0]:xx[-1]+1], axis=2).sum())
    need(changed > 10, 'Native selected stance actually animates while cursor blinks')
    # Native idle AND confirmed/locked poses must disappear, not just icons.
    # Use foreground pixels differing from the unchanged stock backdrop;
    # retain all distinct observed CSS poses, including the last locked pose.
    # Correlation also catches a dimmed copy instead of only exact RGB reuse.
    preview_x = 5 if side == 1 else 325
    stock_preview = inactive[106:242, preview_x:preview_x+70]
    previews = {}
    target_id = 17 if fighter == 'kano' else 18
    for row in snapshots:
        if row['scene'] != 'select' or n(row, 'roster') != target_id or n(row, 'frame') >= exit_at:continue
        value = image(row)[106:242, preview_x:preview_x+70]
        key = value.tobytes()
        if key in previews:continue
        mask = ((np.max(np.abs(value.astype(int)-stock_preview.astype(int)), 2) > 40) &
                (value.max(2).astype(int)-value.min(2).astype(int) > 30) & (value.max(2) > 75))
        if int(mask.sum()) <= 100:continue
        expected = value[mask].ravel().astype(float)
        expected -= expected.mean()
        previews[key] = (mask, expected/np.linalg.norm(expected))
    need(len(previews) >= 3, 'Distinct actual idle and locked-selection foreground pose templates')
    matches = {17: [], 18: []};outside_files = set();max_pose_correlation = 0.0
    for r in snapshots:
        if n(r, 'frame') < exit_at:continue
        actual = image(r);outside_files.add(r['file'])
        for index, x in enumerate((23, 323)):
            expected = portrait(ui, index, 55, 70).ravel().astype(float)
            area = actual[24:94, x:x+55].ravel().astype(float)
            correlation = float(np.corrcoef(expected, area)[0, 1]) if area.std() else 0.0
            need(correlation < 0.70, 'No retained normal or dimmed full-size CSS portrait after exit')
        if r['scene'] == 'transition':
            if n(r, 'frame') < live_at:
                preview = actual[106:242, preview_x:preview_x+70]
                for mask, expected in previews.values():
                    observed = preview[mask].ravel().astype(float)
                    observed -= observed.mean();length = np.linalg.norm(observed)
                    correlation = float(np.dot(observed/length, expected)) if length else 0.0
                    max_pose_correlation = max(max_pose_correlation, correlation)
                    need(correlation < 0.80, 'No retained idle/locked CSS character pose during ladder, including dimmed copies')
            for index in (0, 1):
                position = find_portrait(actual, portrait(ui, index, 35, 45))
                if position is not None:matches[17+index].append(dict(frame=n(r, 'frame'), position=position))
    need(len(outside_files) > 60 and all(len(values) >= 3 for values in matches.values()),
         'Both complete source-authored ladder icons actually rendered during native reveal')
    participants = {n(r, 'slot'): n(r, 'id') for r in records(log, 'FIELD') if n(r, 'age') == 0}
    name_checks = 0
    for r in snapshots:
        if r['scene'] != 'fight' or n(r, 'age') < 60:continue
        actual = image(r)
        for slot, identity in participants.items():
            if identity not in (17, 18):continue
            face, edge, x = shadow(ui, identity, slot)
            area = actual[30:40, x:x+face.shape[1]]
            need(np.all(area[edge] == np.array([66, 0, 0], dtype=np.uint8)) and
                 np.all((area[face, 0] > 150) & (area[face, 1] > 100) & (area[face, 2] < 100)),
                 'Every native name face and original black-shadow pen, at correct lifebar slot')
            name_checks += 1
    need(name_checks >= 4, 'Repeated actual native lifebar-name shadow captures')
    return dict(complete_css_portraits=2, phase_matched_cursor_samples=len(ages), player_number_pixels=66 if side == 1 else 84,
                blink_colors=len(colors), backdrop_unshifted_pixels=scores[0, 0], backdrop_runner_up=runner_up,
                native_stance_changed_pixels=changed, selection_pose_templates=len(previews),
                maximum_ladder_selection_pose_correlation=max_pose_correlation, unique_post_exit_images=len(outside_files),
                full_ladder_icon_matches={str(k): len(values) for k, values in matches.items()},
                first_ladder_icon_matches={str(k): values[0] for k, values in matches.items()}, native_name_shadow_checks=name_checks)


def verify(folder, fighter, side):
    folder = Path(folder);log = launch(folder, fighter, side)
    return {**verify_log(log, fighter, side), 'rendered': render(folder, log, fighter, side)}
