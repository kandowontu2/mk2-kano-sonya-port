"""Current real two-human catches at two heights, plus original Jax controls.

Cold two-human matches, not a fresh post-ending/tower proof or whole release.
No game state, positions, RNG, ID, health or velocities are supplied by Lua.
"""
import json
import re
import struct
from pathlib import Path
from verify_cpu_air_runtime import ROOT, NAME, EXE, PAYLOAD, SOURCE, need, h, n, signed, digest, ORIGINAL_SHA, verify_rom
from verify_cpu_air_gate import rows


def records(log, tag):
    return rows(log, 'MK2_HUMAN_AIR_' + tag)


def one(log, tag):
    found = records(log, tag)
    need(len(found) == 1, 'One actual ' + tag)
    return found[0]


def clean(row, prefix):
    return n(row, prefix + 'y') == n(row, prefix + 'floor') and all(h(row, prefix + key) == 0 for key in ('vx', 'vy', 'gravity', 'trail')) and h(row, prefix + 'flags') & 0x1c == 0 and h(row, prefix + 'body') & 0xc == 0


def match_inputs(folder):
    folder = Path(folder)
    meta = json.loads((folder / 'result.json').read_text(encoding='utf-8-sig'))
    need((meta['exit_code'], meta['candidate'], meta['executable_sha256'], meta['payload_sha256'], meta['assistance']) == (0, NAME, EXE, PAYLOAD, 'none'), 'Exact terminal current candidate')
    before = json.loads((folder / 'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need(before == meta['input_hashes'] and len(before) == 7, 'Exact seven frozen launch inputs')
    for filename, wanted in before.items():
        path = Path(filename)
        need(digest(path) == wanted, 'Live launch input changed: ' + filename)
        if path.suffix in ('.lua', '.ps1', '.json'):
            need(digest(folder / 'input_sources' / path.name) == wanted, 'Frozen launch input changed: ' + filename)
    build = json.loads((folder / 'input_sources/build-info.json').read_text(encoding='utf-8-sig'))
    need((build['name'], build['executable_sha256'], build['payload_sha256']) == (NAME, EXE, PAYLOAD), 'Exact matched build metadata')
    for filename, wanted in build['input_hashes'].items():
        need(digest(filename) == wanted, 'Build input changed: ' + filename)
    need(digest(ROOT / 'mame-mkp/src/mame/midway/midtunit_m.cpp') == SOURCE, 'Exact current driver')
    observer_name = 'mk2ks_human_air_control_probe.lua' if (folder / 'input_sources/mk2ks_human_air_control_probe.lua').exists() else 'mk2ks_human_air_height_probe.lua'
    for filename in (observer_name, 'mk2ks_selector_exit_test.lua', 'mk2ks_native_shang_morph.lua'):
        source = (folder / 'input_sources' / filename).read_text()
        need(not re.search(r':write_|write_u\d+|load_?state|\.value\s*=(?!=)', source), 'Guest-writing observer/dependency')
    runners = [Path(filename).name for filename in before if Path(filename).suffix == '.ps1']
    need(len(runners) == 1, 'One actual frozen runner')
    runner_name = runners[0]
    need('-nocheat' in (folder / 'input_sources' / runner_name).read_text(), 'Cheat-disabled launch')
    need(digest(ROOT / 'mk2/mk2-maincpu.bin') == ORIGINAL_SHA, 'Exact original MKII')
    # These exact compiled words were captured from this same executable,
    # not from an older source or inferred from an intended patch.
    cpu = ROOT / 'audit_v401_cpu_air_kano_jump604'
    cpu_meta = json.loads((cpu / 'result.json').read_text(encoding='utf-8-sig'))
    need(cpu_meta['executable_sha256'] == EXE and cpu_meta['payload_sha256'] == PAYLOAD, 'Matched compiled-word provenance')
    original = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
    verify_rom((cpu / 'run.log').read_text(encoding='utf-8-sig'), original)
    return meta, (folder / 'run.log').read_text(encoding='utf-8-sig'), original


def verify_log(log, attacker, victim, side, delay, original):
    need(not re.search(r'\[LUA ERROR\]|fatal error|stack traceback|access violation|MK2_HUMAN_AIR_ERROR', log, re.I), 'No runtime/observer errors')
    aid = {'kano': 17, 'jax': 11}[attacker]
    vid = {'sonya': 18, 'sub_zero': 8}[victim]
    stock = attacker == 'jax'
    need(side in (1, 2) and delay in (8, 20), 'Declared both-height/slot scope')
    result = one(log, 'RESULT')
    match, jump, caught, own, victim_ready, complete, final = [one(log, tag) for tag in ('MATCH', 'JUMP', 'CAUGHT', 'OWN_READY', 'VICTIM_READY', 'COMPLETE', 'FINAL')]
    mf, jf, cf, of, vf, end, ff = [n(row, 'frame') for row in (match, jump, caught, own, victim_ready, complete, final)]
    command, followup = n(result, 'command'), n(result, 'followup')
    need(command == jf + delay and cf == command + 2 and end == max(of, vf) + 1 and followup == end + 16 and ff == followup + 160, 'Actual command/catch/full ready/follow-up chronology')
    need(all(n(result, key) == value for key, value in (('match', mf), ('jump', jf), ('caught', cf), ('own_ready', of), ('victim_ready', vf), ('complete', end), ('final', ff))), 'Summary equals actual observations')
    fields, events, stores, locks, inputs = [records(log, tag) for tag in ('FIELD', 'EVENT', 'HEALTH', 'LOCK', 'INPUT')]
    need([n(r, 'frame') for r in fields] == list(range(mf, ff + 1)), 'Every actual match field exactly once')
    by = {n(r, 'frame'): r for r in fields}
    for r in fields + events + stores + locks + inputs + [match, jump, caught, own, victim_ready, complete, final]:
        need((r['attacker'], r['victim'], n(r, 'side'), n(r, 'delay'), r['writes'], r['assistance']) == (attacker, victim, side, delay, '0', 'none'), 'Actual input-only declared roles')
        for prefix, identity in (('a', aid), ('v', vid)):
            need(n(r, prefix + 'id') == n(r, prefix + 'roster') == identity and r[prefix + 'state'] == '1', 'Independent actual identity/two human controllers')
            for key in ('actor', 'main', 'owner'):
                need(r[prefix + key] == match[prefix + key], 'Stable native owner')
            need(r[prefix + 'actor'] == r[prefix + 'owner'], 'Main actually owns its actor')
    need(all(clean(r, p) for r in (match, jump, complete, final) for p in ('a', 'v')), 'Grounded clean match/input/recovery/final bookends')
    for r in events:
        need(h(r, 'pc') == h(r, 'entry') + 16, 'Typed actual instruction, not an operand fetch')
    for addr, opcode in ((0xff8b6ff0, 0x0d5f), (0xff861500, 0xb5a4), (0xff83d2f0, 0xb9a8),
                         (0xff83ee90, 0xb088), (0xff83efa0, 0xb08d), (0xff876660, 0xa26f), (0xff8366f0, 0x8026)):
        need(struct.unpack_from('<H', original, (addr - 0xff800000) // 8)[0] == opcode, 'Original typed native opcode')
    selected = rows(log, 'MK2KS_SELECTION_RESULT')
    display = rows(log, 'MK2KS_DISPLAY_RESULT')
    ui = rows(log, 'MK2KS_EXIT_RESULT')
    need(len(selected) == len(display) == len(ui) == 1 and selected[0]['errors'] == selected[0]['p2_identity_errors'] == '0' and
         display[0]['pass'] == 'true' and ui[0]['pass'] == 'true' and ui[0]['leaks'] == ui[0]['identity_errors'] == ui[0]['name_errors'] == '0', 'Actual native selection/display/exit passes')
    if not stock:
        shadow = rows(log, 'MK2KS_HUD_SHADOW_RESULT')
        need(len(shadow) == 1 and shadow[0]['pass'] == 'true' and n(shadow[0], 'checks') >= 6, 'Current added name shadow samples')
    else:
        need(not rows(log, 'MK2KS_HUD_SHADOW_RESULT'), 'New-character-only HUD assertion not misapplied to stock pair')

    def ev(address, prefix, first=cf, last=end, single=True):
        found = [r for r in events if h(r, 'entry') == address and first <= n(r, 'frame') < last and r['a8'] == match[prefix + 'actor']]
        need(bool(found) and (len(found) == 1 if single else True), 'Missing/duplicate actual event ' + f'{address:08X}')
        for r in found:
            need(r['a13'] == match[prefix + 'main'], 'True owning Main at actual instruction')
        return found[0] if single else found

    ev(0xff8b6ff0, 'a')
    need(all(n(caught, p + 'y') < n(caught, p + 'floor') for p in ('a', 'v')), 'Both fighters truly airborne at successful catch')
    height = ev(0xfffcac00, 'a', cf, cf + 1)
    need(h(height, 'a1') == 32, 'Original shared 32 argument reaches height router')
    position = [r for r in events if r['entry'] == 'FF83CC20' and n(r, 'frame') == cf and r['a8'] == match['aactor']]
    need(len(position) == 1 and h(position[0], 'a1') == (32 if stock else 0), 'Actual original position helper receives Jax 32 / Kano zero')
    held_y = (h(caught, 'ayraw') + ((32 if stock else 0) << 16)) & 0xffffffff
    if not stock:
        for elapsed in range(1, 27):
            r = by[cf + elapsed]
            pose = 0xfe828e80 if elapsed <= 8 else 0xfe828ec0 if elapsed <= 10 else 0xfe828f00
            need(h(r, 'apose') == pose and n(r, 'aaction') == 0x109 and r['axraw'] == caught['axraw'] and
                 h(r, 'ayraw') == held_y and all(h(r, 'a' + k) == 0 for k in ('vx', 'vy', 'gravity')) and
                 h(r, 'aflags') & 0x10 and h(r, 'abody') & 4, 'Every exact Kano held pose remains at actual catch height')
        direction = 1 if n(caught, 'ax') < n(caught, 'vx') else -1
        for elapsed in range(1, 9):
            r = by[cf + elapsed]
            need(h(r, 'vxraw') == (h(caught, 'axraw') + direction * (41 << 16)) & 0xffffffff and
                 h(r, 'vyraw') == (held_y - (3 << 16)) & 0xffffffff and h(r, 'vpose') == 0xff033d00, 'Every native fixed-point Kano 41,-3 held victim grip')
        release = ev(0xfffff980, 'a')
        flight = ev(0xfffff580, 'v')
        bounce = ev(0xfffc2000, 'v')
        landing = ev(0xfffc1c00, 'a')
        lf, bf = n(flight, 'frame'), n(bounce, 'frame')
        need(n(release, 'frame') == cf + 8 and lf - n(release, 'frame') == (1 if side == 1 else 0) and n(landing, 'frame') + 2 == of, 'Native early release, cooperative slot timing and own landing')
        getup = ev(0xff8ea320, 'v')
        gf = n(getup, 'frame')
        callbacks = ev(0xfffff800, 'v', single=False)
        need([n(r, 'frame') for r in callbacks] == list(range(lf + 1, gf + 1)) and all(h(r, 'a6') == 0xfffff800 for r in callbacks), 'Every actual victim callback through flight/rebound')
        launch = by[lf + 1]
        launch_vx = direction * 0x30000 & 0xffffffff
        need(h(launch, 'vvx') == launch_vx and h(launch, 'vvy') == 0 and h(launch, 'vgravity') == 0xa000 and h(launch, 'vpose') == 0xff033d80, 'Actual early victim launch state')
        for at in range(lf + 2, gf + 1):
            prev, r = by[at - 1], by[at]
            vy = (h(prev, 'vvy') + h(prev, 'vgravity')) & 0xffffffff
            y = (h(prev, 'vyraw') + vy) & 0xffffffff
            if at == bf + 1:
                y = (n(r, 'vfloor') << 16) | (y & 0xffff)
            vx = signed(h(prev, 'vvx'))
            need(h(r, 'vyraw') == y and h(r, 'vxraw') == (h(prev, 'vxraw') + vx + ((vx >> 16) << 16)) & 0xffffffff and h(r, 'vpose') == 0xff02f920, 'Every exact victim X/Y/gravity/pose field')
            if at == bf + 1:
                need(h(r, 'vvx') == (0x1fc00 if side == 1 else 0xfffefc00) and h(r, 'vvy') == 0xfffa8000 and h(r, 'vgravity') == 0x7000, 'Actual victim-slot native rebound arguments')
            else:
                need(h(r, 'vvy') == vy and r['vvx'] == prev['vvx'] and r['vgravity'] == prev['vgravity'], 'Whole original flight/rebound dynamics')
        need(vf == gf + 24, 'Full native shortened Kano victim get-up')
        damage_frame, damage, held = cf + 25, 16, 26
    else:
        seq = struct.unpack_from('<10I', original, (0xff9972c0 - 0xff800000) // 8)
        need(seq == (0xff997400, 0xff997480, 0xff997520, 0xff9975a0, 0xff9975a0, 0xff9975a0, 0, 0xff9975a0, 0xff9975a0, 0), 'Original Jax authored air-throw sequence')
        for elapsed in range(1, 59):
            r = by[cf + elapsed]
            pose = seq[0] if elapsed <= 17 else seq[1] if elapsed <= 19 else seq[2] if elapsed <= 21 else seq[3]
            need(h(r, 'apose') == pose and n(r, 'aaction') == 0x109 and r['axraw'] == caught['axraw'], 'Every original Jax owned throw pose/hold')
            if elapsed <= 7:
                need(h(r, 'ayraw') == held_y, 'Jax original +32 shift preserved')
            if elapsed == 7:
                need(h(r, 'avy') == 0x20000 and h(r, 'agravity') == 0xa000, 'Original Jax downward landing phase starts, not Kano stationary hold')
            elif 8 <= elapsed <= 17:
                prev = by[cf + elapsed - 1]
                vy = (h(prev, 'avy') + 0xa000) & 0xffffffff
                need(h(r, 'avy') == vy and h(r, 'ayraw') == (h(prev, 'ayraw') + vy) & 0xffffffff and h(r, 'agravity') == 0xa000, 'Every original Jax own landing integration step')
            elif elapsed >= 18:
                need(n(r, 'ay') == n(r, 'afloor') and h(r, 'avy') == h(r, 'agravity') == 0, 'Jax retains its native grounded finishing hold')
        need(of == cf + 64, 'Full original Jax own recovery cadence')
        flight = ev(0xff8da830, 'v')
        lf = n(flight, 'frame')
        getup = ev(0xff8ea320, 'v')
        gf = n(getup, 'frame')
        need(lf == cf + (35 if side == 1 else 34) and vf == gf + 28, 'Original late Jax victim flight/full get-up')
        need(not [r for r in events if cf <= n(r, 'frame') < end and h(r, 'entry') in (0xfffff580, 0xfffff800, 0xfffc2000, 0xfffc1c00)], 'Stock Jax does not run Kano flight/bounce/landing')
        first = by[lf + 1]
        need(h(first, 'vvy') == 0xfff80000 and h(first, 'vgravity') == 0xa000, 'Original Jax eight-pixel upward launch')
        for at in range(lf + 2, gf + 1):
            prev, r = by[at - 1], by[at]
            vy = (h(prev, 'vvy') + 0xa000) & 0xffffffff
            need(h(r, 'vvy') == vy and h(r, 'vyraw') == (h(prev, 'vyraw') + vy) & 0xffffffff and h(r, 'vgravity') == 0xa000 and
                 h(r, 'vxraw') == (h(prev, 'vxraw') + signed(h(prev, 'vvx'))) & 0xffffffff, 'Every original Jax victim flight step without Kano callback')
        damage_frame, damage, held = cf + 34, 32, 58

    damage_event = ev(0xff83a7a0, 'a')
    need(n(damage_event, 'frame') == damage_frame and h(damage_event, 'a0') == damage and damage_event['a10'] == match['vactor'], 'Native damage helper argument/real victim')
    pair_stores = [r for r in stores if cf <= n(r, 'frame') <= end and n(r, 'before') != n(r, 'after')]
    need(len(pair_stores) == 1, 'One uninterrupted actual native throw damage store')
    store = pair_stores[0]
    need(n(store, 'frame') == damage_frame and n(store, 'slot') == 3 - side and store['pc'] == 'FF836700' and
         store['a8'] == match['vactor'] and store['a13'] == match['amain'] and (n(store, 'before'), n(store, 'after')) == (161, 161 - damage), 'Actual original health writer and damage')
    for prefix, ready, role in (('a', own, 1), ('v', victim_ready, 2)):
        at = n(ready, 'frame')
        ev(0xff861500, prefix, at, at + 1)
        need(n(ready, prefix + 'action') == 0 and clean(ready, prefix), 'Individual owning native handoff fully clear/grounded/stopped')
        for kind, pc, address, mask in (('body', 'FF83EEB0', h(match, prefix + 'actor') + 0x160, 0xc), ('flags', 'FF83EFC0', h(match, prefix + 'main') + 0x210, 0x14)):
            found = [r for r in locks if n(r, 'frame') == at and n(r, 'role') == role and r['kind'] == kind and r['pc'] == pc and
                     h(r, 'at') == address and r['a8'] == match[prefix + 'actor'] and r['a13'] == match[prefix + 'main'] and
                     h(r, 'after') == h(r, 'before') & (~mask & 0xffff)]
            need(bool(found), 'Actual original body/Main cleanup stores before each native handoff')
    # Entire health timeline: samples precede writes performed later that field.
    health = {side: 161, 3-side: 161}
    writes = sorted(stores, key=lambda r: n(r, 'frame'))
    index = 0
    for r in fields:
        while index < len(writes) and n(writes[index], 'frame') < n(r, 'frame'):
            w = writes[index];slot = n(w, 'slot')
            need(n(w, 'before') == health[slot] and w['pc'] == 'FF836700', 'Native ledger continuity')
            health[slot] = n(w, 'after');index += 1
        need(n(r, 'ahp') == health[side] and n(r, 'vhp') == health[3-side] and n(r, 'ahp') > 0 and n(r, 'vhp') > 0, 'Every living health field exactly follows native ledger')
    # Actual scripted controls are completely bounded. Follow-up contact may
    # hit or miss; native punch/block entries and clean return are mandatory.
    for slot in (1, 2):
        jump_inputs = [n(r, 'frame') for r in inputs if n(r, 'slot') == slot and r['button'] == 'Up' and n(r, 'frame') < end]
        need(jump_inputs == list(range(jf, jf + 3)), 'Both real three-field jump pulses')
    blocks = [n(r, 'frame') for r in inputs if r['button'] == 'Block' and n(r, 'frame') < end]
    need(blocks == list(range(command, command + 6)) and all(n(r, 'slot') == side for r in inputs if r['button'] == 'Block' and n(r, 'frame') < end), 'Only six actual attacker Block catch inputs')
    for r in inputs:
        at, button = n(r, 'frame'), r['button']
        allowed = (mf + 180 <= at < jf and n(r, 'slot') == side and button in ('Left', 'Right') or
                   jf <= at < jf + 3 and button == 'Up' or command <= at < command + 6 and button == 'Block' and n(r, 'slot') == side)
        if at >= followup:
            age = at - followup
            allowed = (0 <= age < 8 and button in ('Left', 'Right') or 40 <= age < 43 and button == 'Up' or
                       112 <= age < 115 and button == 'High_Punch' or 136 <= age < 142 and button == 'Block')
            if age < 8:
                prefix, other = ('a', 'v') if n(r, 'slot') == side else ('v', 'a')
                towards = 'Right' if n(r, prefix + 'x') < n(r, other + 'x') else 'Left'
                wanted = ('Left' if towards == 'Right' else 'Right') if stock else towards
                need(button == wanted, 'Actual inward Kano/outward stock follow-up walk, not a relabelled close clinch')
        need(allowed and n(r, 'slot') in (1, 2), 'No unexpected controls/state forcing')
    for prefix, slot in (('a', side), ('v', 3 - side)):
        following = [r for r in inputs if n(r, 'slot') == slot and n(r, 'frame') >= followup]
        need(len(following) == 20, 'Exact eight walk/three jump/three punch/six block follow-up inputs')
        # Original backward walk is two pixels, forward walk 2.5. The stock
        # control walks outward; do not demand forward-walk distance from it.
        if stock:
            identity = aid if prefix == 'a' else vid
            need(struct.unpack_from('<I', original, (0xff906cd0 - 0xff800000) // 8 + identity * 4)[0] == 0x20000006, 'Original stock backward-walk two-pixel/six-field packed parameter')
        need(abs(h(by[followup + 40], prefix + 'xraw') - h(by[followup], prefix + 'xraw')) >= (16 if stock else 20) << 16, 'Actual ordinary walking displacement')
        physics = ev(0xff876660, prefix, followup + 40, followup + 53)
        need((h(physics, 'a0'), h(physics, 'a1'), h(physics, 'a2'), h(physics, 'a6')) == (0, 0xfff60000, 0x8000, 0), 'Original clean follow-up jump physics callback/arguments')
        airborne = [r for r in fields if followup + 44 <= n(r, 'frame') <= followup + 88 and n(r, prefix + 'y') < n(r, prefix + 'floor')]
        need(len(airborne) == 38 and [n(r, 'frame') for r in airborne] == list(range(n(airborne[0], 'frame'), n(airborne[0], 'frame') + 38)), 'Complete native 38-field vertical follow-up jump')
        base = h(by[followup + 40], prefix + 'yraw')
        for tick, r in enumerate(airborne, 1):
            raw = (base - 10 * 65536 * tick + 32768 * tick * (tick + 1) // 2) & 0xffffffff
            need(h(r, prefix + 'yraw') == raw and h(r, prefix + 'vy') == (-10 * 65536 + tick * 32768) & 0xffffffff and
                 n(r, prefix + 'action') == 0x30b and h(r, prefix + 'vx') == h(r, prefix + 'callback') == 0 and
                 h(r, prefix + 'flags') & 0x1c == 0 and h(r, prefix + 'body') & 0xc == 0, 'Every exact original follow-up jump field with no stale throw callback/locks')
        punch = [r for r in fields if followup + 113 <= n(r, 'frame') <= followup + 135 and n(r, prefix + 'action') in (0x101, 0x106)]
        block = [r for r in fields if followup + 137 <= n(r, 'frame') <= followup + 152 and n(r, prefix + 'action') == 0x700]
        need(len(punch) >= 3 and len(block) >= 3 and all(clean(r, prefix) for r in block), 'Actual native follow-up punch/block and return to control')
    return dict(passed=True, attacker=attacker, victim=victim, side=side, delay=delay, catch=cf,
                catch_y=n(caught, 'ay'), floor=n(caught, 'afloor'), held_height_preserved=not stock,
                Jax_original_shift_preserved=stock, held_fields=held, whole_flight_fields=gf-lf,
                own_ready=of, victim_ready=vf, complete=end, damage=damage,
                original_cleanup_stores=True, followup_fields=161, actual_followup_controls=True,
                native_match_fields=len(fields), whole_character_integration_complete=False,
                scope='declared_current_two_human_catch_height_full_physics_damage_original_cleanup_and_walk_jump_punch_block_not_all_victims_CPU_tower_endings_pixels_audio_or_release')


def verify(folder):
    meta, log, original = match_inputs(folder)
    return verify_log(log, meta['attacker'], meta['victim'], meta['side'], meta['delay'], original)


if __name__ == '__main__':
    import sys
    for folder in sys.argv[1:]:
        try:
            print(json.dumps(verify(folder), indent=2))
        except (ValueError, KeyError, IndexError) as error:
            print(json.dumps({'passed': False, 'error': str(error)}))
            raise SystemExit(1)
