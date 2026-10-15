"""Narrow current-build, input-only P1 CPU air-throw proof.

Checks observed native instructions, actual ownership, every held/flight field,
native damage and each Main's post-cleanup ready entry. This observer does NOT
prove individual cleanup stores, all artwork/audio, human catches, Jax catches,
other victims/slots, interruptions or the complete integration goal.
"""
import json
import re
import struct
from pathlib import Path
from verify_cpu_air_gate import ROOT, digest, rows, route, ORIGINAL_SHA
from verify_cpu_air_counter import verify_compiled, words_from_log

NAME = 'diagnostic_v400_native_kano_air_height'
EXE = '822CD6BC358854162A4769A9D6C09923D737ADA025201B64B6521988DF9837F6'
PAYLOAD = '82FE153FB56B46A6F9D42F493451AC3D59AD61713433714ACA7704E2881F8951'
SOURCE = '1F9E368A0763D63DF928D04E8A0CAE3B78A79DEC911FDB85308A92A99D0B1C97'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def n(row, field):
    return int(row[field])


def h(row, field):
    return int(row[field], 16)


def signed(value):
    return value - 0x100000000 if value & 0x80000000 else value


def verify_rom(log, original):
    dumps = rows(log, 'MK2_CPU_AIR_ROM')
    need(len(dumps) == 3, 'One continuous observer: exactly three ROM windows')
    windows = {h(r, 'start'): r for r in dumps}
    need(set(windows) == {0xff9beef0, 0xfffc8700, 0xfffca000}, 'Exact ROM windows')
    for start, stop in ((0xff9beef0, 0xff9bf2c0), (0xfffc8700, 0xfffc8800), (0xfffca000, 0xfffcb000)):
        r = windows[start]
        need(h(r, 'stop') == stop and r['writes'] == '0' and r['assistance'] == 'none', 'Unassisted complete ROM window')
        need(len(r['words'].split(',')) == (stop - start) // 16, 'Complete compiled words')
    gate = [int(w, 16) for w in windows[0xff9beef0]['words'].split(',')]
    stock = list(struct.unpack_from('<' + 'H' * len(gate), original, (0xff9beef0 - 0xff800000) // 8))
    need(gate[:5] == [0xc080, 0x8700, 0xfffc, 0x0300, 0x0300] and gate[5:] == stock[5:], 'Original eligibility and stack unwind retained')
    router = [int(w, 16) for w in windows[0xfffc8700]['words'].split(',')]
    for identity in range(19):
        need(route(router, identity) == (0xfffca400 if identity in (11, 17) else 0xff9bf050, identity), 'Real identity routing without proxies')
    proof = verify_compiled(log)
    # Exact small instruction program: preserve A2, load actual ID into A2,
    # compare 17, skip CLR A1 for all others, restore A2 and tail-call original.
    height = words_from_log(log)[192:208]
    need(height == [0x098f, 0x2000, 0xb502, 0x1f0, 0x0b42, 0xffee, 0xcb01,
                    0x5621, 0x09af, 0x0004, 0xc080, 0xcc20, 0xff83, 0xffff, 0xffff, 0xffff], 'Exact Kano-only height instructions/register preservation')
    height_matrix = []
    for identity in range(19):
        original_a2, a1 = 0x12345678, 32
        stack = [original_a2]
        a2 = identity
        zero = a2 == (~height[5] & 0xffff)
        pc = 7 if zero else 8  # CB01 skips exactly the one-word CLR.
        if pc == 7:
            a1 = a1 ^ a1
        a2 = stack.pop()
        need(a2 == original_a2 and a1 == (0 if identity == 17 else 32), 'Height helper aliases stock identity')
        height_matrix.append({'id': identity, 'a1': a1, 'a2_preserved': True})
    return {**proof, 'identity_routes': 19, 'height_routes': height_matrix}


def matched_launch(folder, observer='mk2ks_cpu_air_height_probe.lua', runner='run_cpu_air_height_probe.ps1'):
    folder = Path(folder)
    launch = json.loads((folder / 'result.json').read_text(encoding='utf-8-sig'))
    need((launch['exit_code'], launch['candidate'], launch['executable_sha256'], launch['payload_sha256'],
          launch['cpu_slot'], launch['human_slot'], launch['assistance']) == (0, NAME, EXE, PAYLOAD, 1, 2, 'none'), 'Exact terminal current input-only candidate')
    before = json.loads((folder / 'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need(before == launch['input_hashes'], 'Before/after input identity')
    for filename, expected in before.items():
        path = Path(filename)
        need(digest(path) == expected, 'Changed live launch input: ' + filename)
        if path.suffix in ('.lua', '.ps1', '.json'):
            need(digest(folder / 'input_sources' / path.name) == expected, 'Changed frozen launch input: ' + filename)
    build = json.loads((folder / 'input_sources/build-info.json').read_text(encoding='utf-8-sig'))
    need(build['name'] == NAME and build['executable_sha256'] == EXE and build['payload_sha256'] == PAYLOAD, 'Matched build metadata')
    for filename, expected in build['input_hashes'].items():
        need(digest(filename) == expected, 'Changed build input: ' + filename)
    need(digest(ROOT / 'mame-mkp/src/mame/midway/midtunit_m.cpp') == SOURCE, 'Current driver source')
    source = (folder / 'input_sources' / observer).read_text()
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)', source), 'Observer writes guest state')
    need('-nocheat' in (folder / 'input_sources' / runner).read_text(), 'Cheat-disabled launch')
    original_path = ROOT / 'mk2/mk2-maincpu.bin'
    need(digest(original_path) == ORIGINAL_SHA, 'Original MKII binary')
    return launch, (folder / 'run.log').read_text(encoding='utf-8-sig'), original_path.read_bytes()


def verify_log(log, player, original):
    need(player in ('kano', 'sonya'), 'Declared accepted victim')
    need(not re.search(r'\[LUA ERROR\]|fatal error|stack traceback|access violation', log, re.I), 'No runtime/observer errors')
    compiled = verify_rom(log, original)
    selection = rows(log, 'MK2_P1CPU_SELECT_RESULT')
    results = rows(log, 'MK2_CPU_AIR_RESULT')
    need(len(selection) == len(results) == 1, 'One native selection/terminal result')
    selected, result = selection[0], results[0]
    vid = 17 if player == 'kano' else 18
    need(selected['human'] == player and n(selected, 'human_id') == vid and n(selected, 'checks') == 39 and
         selected['errors'] == '0' and n(selected, 'live') > 0 and selected['initial_cpu'] == '17', 'Actual independent cold P2 selection')
    need(result['schema'] == '3' and result['actions'] == '1', 'Exactly one actual observed CPU catch')
    groups = {tag: rows(log, 'MK2_CPU_AIR_' + tag) for tag in ('CAUGHT', 'OWN_READY', 'VICTIM_READY', 'COMPLETE', 'FIELD', 'EVENT', 'HEALTH', 'INPUT')}
    for tag in ('CAUGHT', 'OWN_READY', 'VICTIM_READY', 'COMPLETE'):
        need(len(groups[tag]) == 1, 'One actual ' + tag)
    caught, own, victim, done = (groups[tag][0] for tag in ('CAUGHT', 'OWN_READY', 'VICTIM_READY', 'COMPLETE'))
    start, end = n(caught, 'frame'), n(done, 'frame')
    need(end == max(n(own, 'frame'), n(victim, 'frame')) + 1 and
         all(n(result, name) == n(row, 'frame') for name, row in (('caught', caught), ('own_ready', own), ('victim_ready', victim), ('complete', done))), 'Completion after both first individual native handoffs')
    need(n(groups['FIELD'][-1], 'frame') == end + 30, 'Bounded terminal follow-up')
    timeline = [r for r in groups['FIELD'] if start < n(r, 'frame') <= end]
    need([n(r, 'frame') for r in timeline] == list(range(start + 1, end + 1)), 'Every paired field exactly once')
    by = {n(r, 'frame'): r for r in timeline}
    events = [r for r in groups['EVENT'] if start - 1 <= n(r, 'frame') <= end]
    for r in [caught, own, victim, done] + timeline + events + [r for r in groups['HEALTH'] if start <= n(r, 'frame') <= end]:
        need((r['writes'], r['assistance'], r['cpu_slot'], r['human_slot'], r['cstate'], r['hstate']) == ('0', 'none', '1', '2', '0', '1'), 'Input-only actual controller states')
        for prefix, identity in (('c', 17), ('h', vid)):
            need(n(r, prefix + 'id') == n(r, prefix + 'roster') == identity, 'Independent actual character identity')
            for key in ('actor', 'main', 'owner'):
                need(r[prefix + key] == caught[prefix + key], 'Stable owning actor/Main throughout selected pair')
            need(r[prefix + 'actor'] == r[prefix + 'owner'], 'Actual native Main owns its actor')
    for r in events:
        need(h(r, 'pc') == h(r, 'entry') + 16, 'Typed actual first-word instruction fetch')
    for address, opcode in ((0xff9c8180, 0xa2cf), (0xff9bef40, 0x0d5f), (0xff9bf1c0, 0x09af),
                            (0xff8b6ff0, 0x0d5f), (0xff861500, 0xb5a4), (0xff837bf0, 0xb7a0),
                            (0xff80ec20, 0x098f), (0xff83a7a0, 0x098f), (0xff8ea320, 0x0d3f), (0xff8366f0, 0x8026),
                            (0xff83d2f0, 0xb9a8), (0xff876ae0, 0x0d5f)):
        need(struct.unpack_from('<H', original, (address - 0xff800000) // 8)[0] == opcode, 'Original typed native opcode')

    def event(address, slot, frame=None, unique=True):
        prefix = 'c' if slot == 1 else 'h'
        found = [r for r in events if h(r, 'entry') == address and (frame is None or n(r, 'frame') == frame)]
        need(bool(found) and (len(found) == 1 if unique else True), 'Missing/duplicate native event ' + f'{address:08X}')
        for r in found:
            need(r['a8'] == caught[prefix + 'actor'] and r['a13'] == caught[prefix + 'main'], 'Actual event owner ' + f'{address:08X}')
        return found[0] if unique else found

    # Native uppercut response selects the new chance branch; RNG result and
    # native jump are observed, never supplied by the test controller.
    counter = [r for r in events if h(r, 'entry') in (0xfffca000, 0xfffca800) and n(r, 'frame') == start - 1]
    need(len(counter) == 1, 'Native CPU counter chooses actual air-catch jump')
    helper = h(counter[0], 'entry')
    wrapper = 0xff9b8100 if helper == 0xfffca000 else 0xff9b8080
    sequence = [wrapper, helper, 0xff837bf0, 0xff80ec20, 0xff9c8180, 0xff9beef0,
                0xfffc8700, 0xfffca400, 0xff837bf0, 0xff9bef40, 0xff9bf1c0, 0xff8b6ff0, 0xfffcac00, 0xfffc0680]
    cursor = 0
    for r in events:
        if cursor < len(sequence) and h(r, 'entry') == sequence[cursor]:
            need(r['a8'] == caught['cactor'] and r['a13'] == caught['cmain'], 'Counter/jump/catch chain has actual CPU ownership')
            cursor += 1
    need(cursor == len(sequence), 'Ordered native counter/chance/jump/catch/height/alignment chain')
    need(h(event(0xff80ec20, 1, start - 1), 'a0') == 250 and
         h(event(0xff9c8180, 1, start - 1), 'a6') == 0xff9beef0, 'Native probability threshold and jump callback')
    need(all(n(caught, p + 'y') < n(caught, p + 'floor') for p in ('c', 'h')), 'Both actors genuinely airborne at catch')
    need(h(event(0xfffcac00, 1, start), 'a1') == 32, 'Original shared height input reaches Kano-only helper')
    event(0xfffff980, 1, start + 8)
    event(0xfffff580, 2, start + 9)
    bounce = event(0xfffc2000, 2)
    getup = event(0xff8ea320, 2)
    landing = event(0xfffc1c00, 1)
    bf, gf = n(bounce, 'frame'), n(getup, 'frame')
    need(start + 10 < bf < gf and n(landing, 'frame') + 2 == n(own, 'frame') and gf + 24 == n(victim, 'frame'), 'Native bounce/landing/full get-up cadence')
    callbacks = event(0xfffff800, 2, unique=False)
    need([n(r, 'frame') for r in callbacks] == list(range(start + 10, gf + 1)) and
         all(h(r, 'a6') == 0xfffff800 for r in callbacks), 'Every original victim flight callback across both arcs')
    catch_pose, launch_pose, flight_pose = ((0xff013b40, 0xff013bc0, 0xff00f8c0) if vid == 17 else (0xff033d00, 0xff033d80, 0xff02f920))
    for elapsed in range(1, 27):
        r = by[start + elapsed]
        pose = 0xfe828e80 if elapsed <= 8 else 0xfe828ec0 if elapsed <= 10 else 0xfe828f00
        need(h(r, 'cpose') == pose and n(r, 'caction') == 0x109 and r['cxraw'] == caught['cxraw'] and
             r['cyraw'] == caught['cyraw'] and all(h(r, 'c' + k) == 0 for k in ('vx', 'vy', 'gravity')) and
             h(r, 'cflags') & 0x10 and h(r, 'cbody') & 4, 'All 26 native owned held poses at actual catch height, not Jax +32')
        if elapsed <= 9:
            need(h(r, 'hpose') == catch_pose and h(r, 'hxraw') == h(caught, 'cxraw') + (41 << 16) and
                 h(r, 'hyraw') == h(caught, 'cyraw') - (3 << 16) and
                 all(h(r, 'h' + k) == 0 for k in ('vx', 'vy', 'gravity')), 'Original held victim pose and full fixed-point 41,-3 grip')
    launch = by[start + 10]
    need(h(launch, 'hpose') == launch_pose and h(launch, 'hvx') == 0x30000 and h(launch, 'hvy') == 0 and
         h(launch, 'hgravity') == 0xa000, 'Actual first victim flight continuation')
    for at in range(start + 11, gf + 1):
        previous, r = by[at - 1], by[at]
        need(h(r, 'hpose') == flight_pose, 'Victim-specific horizontal flight artwork address')
        vy = (h(previous, 'hvy') + h(previous, 'hgravity')) & 0xffffffff
        y = (h(previous, 'hyraw') + vy) & 0xffffffff
        if at == bf + 1:
            # Original FF876AE0 calls FF83D2F0 after impact. Its word move
            # copies Main.floor to actor.Y.integer; the fraction is retained.
            # Kano's overshoot already has the floor's integer. Sonya's is
            # two pixels lower and is corrected by that same original store.
            y = (n(r, 'hfloor') << 16) | (y & 0xffff)
        need(h(r, 'hyraw') == y, 'Every fixed-point native Y integration including original impact floor-word clamp')
        # Native callback adds the integer velocity, then original physics adds
        # the full fixed-point velocity. Do not clamp the first impact to floor.
        vx = signed(h(previous, 'hvx'))
        need(h(r, 'hxraw') == (h(previous, 'hxraw') + vx + ((vx >> 16) << 16)) & 0xffffffff, 'Every native X velocity plus callback step')
        if at == bf + 1:
            need(h(r, 'hvy') == 0xfffa8000 and h(r, 'hvx') == 0x1fc00 and h(r, 'hgravity') == 0x7000, 'Actual native P2 rebound parameters')
        else:
            need(h(r, 'hvy') == vy and h(r, 'hvx') == h(previous, 'hvx') and h(r, 'hgravity') == h(previous, 'hgravity'), 'Unmodified complete victim gravity/velocity sequence')
    damage = event(0xff83a7a0, 1, start + 25)
    need(h(damage, 'a0') == 16 and damage['a10'] == caught['hactor'], 'Original native sixteen-point damage argument and actual victim')
    stores = [r for r in groups['HEALTH'] if start <= n(r, 'frame') <= end]
    need(len(stores) == 1, 'No extra hit/refill hidden in uninterrupted selected pair')
    store = stores[0]
    need(n(store, 'frame') == start + 25 and store['slot'] == '2' and h(store, 'pc') == 0xff836700 and
         store['a8'] == caught['hactor'] and store['a13'] == caught['cmain'] and
         n(store, 'before') == n(caught, 'hhp') and n(store, 'after') == n(caught, 'hhp') - 16, 'Actual original damage store ownership/value')
    for r in timeline:
        need(n(r, 'chp') == n(caught, 'chp') and n(r, 'hhp') == n(caught, 'hhp') - (16 if n(r, 'frame') > start + 25 else 0), 'Every observed health field follows exactly its native store')
    for r, prefix in ((own, 'c'), (victim, 'h')):
        event(0xff861500, 1 if prefix == 'c' else 2, n(r, 'frame'))
        need(r['entry'] == 'FF861500' and r['pc'] == 'FF861510' and n(r, prefix + 'action') == 0 and
             n(r, prefix + 'y') == n(r, prefix + 'floor') and
             all(h(r, prefix + key) == 0 for key in ('vx', 'vy', 'gravity', 'trail')) and
             h(r, prefix + 'flags') & 0x1c == 0 and h(r, prefix + 'body') & 0x0c == 0, 'Actual individual post-cleanup native ready handoff fully clear/grounded/stopped')
    # Frame callbacks issue the last jump input before the CPU executes later
    # in that same field. Use actual log order, not a >= frame shortcut.
    need('MK2_CPU_AIR_INPUT ' not in log.split('MK2_CPU_AIR_CAUGHT ', 1)[1], 'No scripted player input after the catch')
    return dict(passed=True, player=player, CPU_slot=1, human_slot=2, catch=start,
                complete=end, own_ready=n(own, 'frame'), victim_ready=n(victim, 'frame'),
                paired_fields=len(timeline), held_fields=26, flight_fields=gf-start-10,
                native_callback_fields=len(callbacks), damage=16, compiled_branches=compiled['compiled_branches'],
                compiled_height_routes=19, actual_catch_height_retained=True,
                cleanup_store_provenance=False, all_bitmap_audio_acceptance=False,
                whole_character_integration_complete=False,
                scope='only_two_declared_uninterrupted_P1_CPU_catches_real_Kano_and_Sonya_victims_not_all_slots_victims_human_Jax_KO_art_audio_or_goal')


def verify(folder):
    launch, log, original = matched_launch(folder)
    return verify_log(log, launch['player'], original)


def verify_y_provenance(folder):
    launch, log, original = matched_launch(folder, 'mk2ks_cpu_air_y_provenance_probe.lua', 'run_cpu_air_y_provenance_probe.ps1')
    proof = verify_log(log, launch['player'], original)
    need(launch['player'] == 'sonya', 'Declared Sonya floor-word control')
    caught = rows(log, 'MK2_CPU_AIR_CAUGHT')[0]
    bounce = [r for r in rows(log, 'MK2_CPU_AIR_EVENT') if r['entry'] == 'FFFC2000'][0]
    frame = n(bounce, 'frame')
    field = {n(r, 'frame'): r for r in rows(log, 'MK2_CPU_AIR_FIELD')}[frame]
    expected = (h(field, 'hyraw') + h(field, 'hvy') + h(field, 'hgravity')) & 0xffffffff
    writes = [r for r in rows(log, 'MK2_CPU_AIR_Y_WRITE') if n(r, 'frame') == frame and r['slot'] == '2' and r['pc'] == 'FF83D320']
    need(len(writes) == 1, 'One original floor-word store at actual bounce')
    store = writes[0]
    need(store['writes'] == '0' and store['assistance'] == 'none' and store['a8'] == caught['hactor'] and
         store['a13'] == caught['hmain'] and h(store, 'at') == h(caught, 'hactor') + 0xb0 and
         h(store, 'before') == expected and h(store, 'data') == n(field, 'hfloor') and h(store, 'mask') == 0xffff,
         'Actual original integer floor clamp value, address, mask and owner')
    need(struct.unpack_from('<3H', original, (0xff83d2f0 - 0xff800000) // 8) == (0xb9a8, 0x200, 0xb0), 'Original floor-to-Y word MOVE opcode')
    return {**proof, 'original_impact_floor_word_store': True, 'bounce_frame': frame,
            'pre_clamp_yraw': f'{expected:08X}', 'floor': n(field, 'hfloor')}


if __name__ == '__main__':
    import sys
    for folder in sys.argv[1:]:
        try:
            print(json.dumps(verify(folder), indent=2))
        except (ValueError, KeyError, IndexError) as error:
            print(json.dumps({'passed': False, 'error': str(error)}))
            raise SystemExit(1)
