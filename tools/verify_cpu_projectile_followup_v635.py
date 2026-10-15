"""Current cold P1 CPU knife/ring life, not all moves, victims, slots or pixels.

Models authored release/create programs independently of the captured timeline.
Checks typed native ownership and stores, every child field, both blocked
bursts and the declared ducked ring miss. Bootstrap visibility, collision
rectangles, audio and the reason for miss retirement need separate observers.
"""
import re
import struct
from pathlib import Path
from verify_cpu_air_gate import ROOT, rows, digest
from verify_cpu_launch_v635 import matched_launch, need, n, h
from verify_cpu_recovery import expected_orders

BODY = {
    17: (0xfe82f400, 0xfe82f460, 0xfe82f4c0, 0xfe82f520,
         0xfe82f580, 0xfe82f5e0, 0xfe82f640, 0xfe82f6a0),
    18: (0xfe83dbe0, 0xfe83dc40, 0xfe83dca0, 0xfe83dd00, 0xfe83dec0),
}
INTRO = (0xff614000, 0xff614060, 0xff6140a0, 0xff614100, 0xff614180, 0xff6141e0)
FLIGHT = {17: tuple(range(0xff614800, 0xff614a80, 0x40)),
          18: tuple(range(0xff614a80, 0xff614b80, 0x40))}
IMPACT = {17: (0xff60c000, 0xff60c040, 0xff60c080, 0xff60c0c0, 0xff60c100, 0xff60c160),
          18: (0xff60c1c0, 0xff60c200, 0xff60c240, 0xff60c300,
               0xff60c400, 0xff60c4e0, 0xff60c580)}
SCOPE = 'current_declared_P1_CPU_knife_block_ring_block_and_duck_miss_not_all_CPU_moves_victims_slots_KO_collision_rectangles_pixels_audio_or_goal'


def records(log, tag):
    return rows(log, 'MK2_CPU_SHOT_' + tag)


def one(values, label):
    need(len(values) == 1, 'Exactly one ' + label)
    return values[0]


def compiled(log, original):
    windows = records(log, 'CODE')
    ranges = {0xffffb000: 0xffffb450, 0xfffc3800: 0xfffc6000, 0xfffbc000: 0xfffbc400}
    need(len(windows) == 3 and {h(r, 'start'): h(r, 'stop') for r in windows} == ranges,
         'Exact complete compiled observer windows')
    memory = {}
    for r in windows:
        start, stop = h(r, 'start'), h(r, 'stop')
        words = [int(w, 16) for w in r['words'].split(',')]
        need(len(words) == (stop-start)//16, 'No truncated compiled window')
        memory.update((start+i*16, w) for i, w in enumerate(words))

    def check(address, words):
        need([memory.get(address+i*16) for i in range(len(words))] == words,
             f'Exact independently authored program {address:08X}')

    def movi(reg, value):
        return [0x09e0+reg, value & 0xffff, (value >> 16) & 0xffff]

    def call(address):
        return [0x0d5f, address & 0xffff, address >> 16]

    def sleep(count):
        return movi(0, count) + call(0xff80dcc0)

    recovery_pc = {}
    for identity in (17, 18):
        sonya = identity == 18
        release = 0xfffc4800 if sonya else 0xfffc3800
        create = 0xfffc5c00 if sonya else 0xfffc5800
        action = 0xffffb400 if sonya else 0xffffb000
        check(action, [0x574a, 0xc080, release & 0xffff, release >> 16])
        words = [0x574a] + call(0xff8a5c20) + movi(1, 4) + [0xb02d, 0x1f0]
        words += movi(0, 5) + call(0xffa12530)
        for i, pose in enumerate(BODY[identity]):
            if not sonya and i == 1:
                words += call(create)
            words += movi(0, pose) + call(0xff838790) + sleep(4 if not sonya and i == 7 else 3)
        if sonya:
            words += call(create)
        words += movi(1, 0x604) + [0xb02d, 0x1f0]
        recovery_pc[identity] = release + len(words)*16
        words += sleep(35 if sonya else 24) + [0xc080, 0x1350, 0xff86]
        check(release, words)
        words = movi(9, 39) + call(0xff906090) + call(0xff8b6450)
        words += movi(0, 0 if sonya else -100) + movi(1, 0 if sonya else -72)
        words += [0x4d45] + call(0xff83cbb0) + [0x4d40] + call(0xff8093e0)
        words += movi(1, 0x700) + movi(7, 0xfffc7000 if sonya else 0xfffc6000)
        words += call(0xff8b5d20) + movi(1, 0x80000) + [0xb220, 0x250, 0x0960]
        check(create, words)
        router = [0x09c0, 250] + call(0xff80ec20) + [0xc80c, 0x09c0, 400]
        router += call(0xff80ec20) + [0xc803, 0xc080, action & 0xffff, action >> 16]
        alternate, third = ((0xffffde00, 0xfff8cc00) if not sonya else (0xffffca00, 0xfff9a400))
        router += [0xc080, alternate & 0xffff, alternate >> 16, 0xc080, third & 0xffff, third >> 16]
        check(0xfffbc200 if sonya else 0xfffbc000, router + [0xffff]*(32-len(router)))
    pins = {0xff838cd0: (0xb1c8, 0x160), 0xff877d30: (0xb08d, 0x210),
            0xff83edb0: (0xb00d, 0x1f0), 0xff83ee90: (0xb088, 0x160),
            0xff83efa0: (0xb08d, 0x210), 0xff9065b0: (0xb00d, 0x1f0),
            0xff8b6820: (0xb700, 0x20), 0xff8366f0: (0x8026, 0xc133),
            0xff861500: (0xb5a4, 0x210), 0xff837d40: (0xb7a0, 0x170)}
    for address, words in pins.items():
        need(struct.unpack_from('<2H', original, (address-0xff800000)//8) == words,
             f'Original typed native store/entry {address:08X}')
    need(struct.unpack_from('<8H', original, (0xff837d40-0xff800000)//8) ==
         (0xb7a0, 0x170, 0xb404, 0x210, 0x1fe4, 0xcb02, 0x0320, 0x0960),
         'Original guard tests victim Main flag bit zero, not only action 700 or drawn block pose')
    return recovery_pc


def verify_log(log, identity, scenario, original):
    need((identity, scenario) in ((17, 'block'), (18, 'block'), (18, 'duck_miss')),
         'Only declared current CPU/victim/scenario evidence')
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|stack traceback', log, re.I),
         'No runtime or observer error')
    tags = ('CODE', 'ENTRY', 'FLOW', 'FIELD', 'STORE', 'CHILD', 'GROUP', 'EFFECT',
            'RETIRE', 'HANDOFF', 'HEALTH', 'COMPLETE', 'INPUT', 'RESULT')
    groups = {tag: records(log, tag) for tag in tags}
    for values in groups.values():
        for r in values:
            need((r['cpu_slot'], r['human_slot'], r['writes'], r['assistance']) ==
                 ('1', '2', '0', 'none'), 'Every record is read-only P1 CPU/P2 human')
    recovery_pc = compiled(log, original)
    entry, child, handoff, retire, done, result = (one(groups[tag], tag) for tag in
                ('ENTRY', 'CHILD', 'HANDOFF', 'RETIRE', 'COMPLETE', 'RESULT'))
    start, ready, retired, end = (n(r, 'frame') for r in (entry, handoff, retire, done))
    release_total, recovery, birth_age, flight_age, flight_hold = ((25, 24, 3, 22, 1)
                                          if identity == 17 else (15, 35, 15, 16, 3))
    need(ready == start+release_total+recovery and end == max(ready, retired)+1 and
         (n(done, 'start'), n(done, 'ready'), n(done, 'retired'), n(done, 'completed_serial')) ==
         (start, ready, retired, 1), 'Complete only after actual body handoff and child retirement')
    need((n(result, 'schema'), n(result, 'entries'), n(result, 'complete'),
          n(result, 'live_children'), n(result, 'frame'), n(result, 'serial')) ==
         (1, 1, end, 0, end+30, 1), 'Unique complete shot and bounded terminal with no child')
    selection = one(rows(log, 'MK2_P1CPU_SELECT_RESULT'), 'cold selection')
    cold = one(rows(log, 'MK2_P1CPU_COLD_LIVE'), 'cold first fight')
    css = one(rows(log, 'MK2_P1CPU_SELECT_CSS'), 'cold CSS')
    human, victim_id = ('kano', 17) if identity == 17 else ('cage', 2)
    for r in (selection, cold, css):
        need(r['writes'] == '0' and r['assistance'] == 'none' and r['human'] == human,
             'Actual cold selection has no assistance')
    order = (h(cold, 'schedule')-0xfffa3000)//0x180
    need(order in range(6) and h(cold, 'schedule') == 0xfffa3000+order*0x180 and
         expected_orders()[order][0] == identity and n(cold, 'stage') == 0 and
         n(cold, 'cpu_id') == n(selection, 'initial_cpu') == identity and
         n(selection, 'human_id') == n(cold, 'human_id') == victim_id and
         n(selection, 'checks') == 39 and n(selection, 'errors') == 0 and
         700 < n(selection, 'css') == n(css, 'frame') < n(selection, 'exit') <
         n(selection, 'live') == n(cold, 'frame') < start, 'Original-derived stage-zero campaign and true P2 identity')
    fields = [r for r in groups['FIELD'] if start < n(r, 'frame') <= end+30]
    need([n(r, 'frame') for r in fields] == list(range(start+1, end+31)),
         'Every paired field through full completion and terminal')
    by = {n(r, 'frame'): r for r in fields}
    pointers = ('actor', 'main', 'vactor', 'vmain')
    need(len({h(entry, k) for k in pointers}) == 4 and
         all(0x01000000 <= h(entry, k) < 0x01100000 for k in pointers), 'Distinct real native actors and Main processes')
    for r in [entry, handoff, done, *fields, *[r for r in groups['FLOW'] if start <= n(r, 'frame') <= end]]:
        for prefix, pid, state in (('', identity, 0), ('v', victim_id, 1)):
            need(n(r, prefix+'id') == n(r, prefix+'roster') == pid and n(r, prefix+'state') == state and
                 r[prefix+'actor'] == r[prefix+'owner'] == entry[prefix+'actor'] and
                 r[prefix+'main'] == entry[prefix+'main'] and r[prefix+'list'] == entry[prefix+'list'],
                 'Stable published actual character/actor/Main/draw-list identity')
        need(n(r, 'mode') == 2 and n(r, 'stage') == 0 and r['schedule'] == cold['schedule'],
             'Native campaign ownership remains unchanged')
    need(all(n(r, 'serial') == 1 for r in [entry, child, handoff, retire, done, *fields]),
         'No spliced child/body cycle')
    action_entry = 0xffffb000 if identity == 17 else 0xffffb400
    release_entry = 0xfffc3800 if identity == 17 else 0xfffc4800
    need(h(entry, 'entry') == action_entry and h(entry, 'pc') == action_entry+16,
         'Actual canonical knife/ring entry, not proxy or overlay')
    flow = [r for r in groups['FLOW'] if start <= n(r, 'frame') <= ready]
    sequence = [0xff8a5900, 0xfffbc000 if identity == 17 else 0xfffbc200,
                action_entry, release_entry, 0xff8a5c20, 0xff861350, 0xff83ed80, 0xff861500, 0xff83ed80]
    need([h(r, 'entry') for r in flow] == sequence, 'Ordered original AI/variety/actual release/native ready chain')
    for r in flow:
        need(h(r, 'pc') == h(r, 'entry')+16 and r['a8'] == entry['actor'] and
             r['a13'] == entry['main'], 'Typed flow instruction executes in actual CPU Main')
    need(h(flow[0], 'a0') == (22 if identity == 17 else 23) and n(flow[0], 'frame') == start,
         'Original AI dispatch requests real new special index')
    for age in range(1, release_total+recovery+1):
        r = by[start+age]
        pose_index = min((age-1)//3, len(BODY[identity])-1)
        need(h(r, 'pose') == BODY[identity][pose_index] and n(r, 'action') ==
             (4 if age <= release_total else 0x604) and h(r, 'flags') == 0x10 and h(r, 'body') == 0x16 and
             all(h(r, k) == 0 for k in ('vx', 'vy', 'gravity', 'trail')) and
             r['xraw'] == entry['xraw'] and r['yraw'] == entry['yraw'] and n(r, 'y') == n(r, 'floor'),
             'Every authored body hold/recovery state, exact stationary ground origin and locks')
    # An ordinary walk redraw occurs earlier on the same scheduler field,
    # before the actual shot ENTRY increments serial. It is not a release pose.
    body_groups = [r for r in groups['GROUP'] if r['child'] == '0' and r['serial'] == '1' and
                   start <= n(r, 'frame') < ready]
    need([h(r, 'group') for r in body_groups] == list(BODY[identity]) and
         [n(r, 'frame')-start for r in body_groups] == list(range(0, len(BODY[identity])*3, 3)),
         'Every body pose is installed by its actual native renderer')
    for r in body_groups:
        need(r['actor'] == entry['actor'] and r['main'] == entry['main'] and
             n(r, 'id') == identity and h(r, 'pc') == 0xff8387a0 and h(r, 'vx') == h(r, 'vy') == 0 and
             r['xraw'] == entry['xraw'] and r['yraw'] == entry['yraw'],
             'Native body render owner and stopped motion')
    stores = [r for r in groups['STORE'] if r['slot'] == '1' and start <= n(r, 'frame') <= ready]
    for r in stores:
        need(r['actor'] == r['owner'] == r['a8'] == entry['actor'] and
             r['main'] == r['a13'] == entry['main'] and n(r, 'id') == n(r, 'roster') == identity and
             n(r, 'state') == 0 and h(r, 'at') == h(entry, 'actor' if r['kind'] == 'body' else 'main')+
             {'body': 0x160, 'flags': 0x210, 'action': 0x1f0}[r['kind']], 'Actual native store target and CPU owner')
    store_order = []
    def store(kind, time, before, after, pc):
        found = one([r for r in stores if r['kind'] == kind and n(r, 'frame') == time and
                     h(r, 'before') == before and h(r, 'after') == after and h(r, 'pc') == pc],
                    f'{kind} native store {pc:08X}')
        need(n(found, 'action') == (before if kind == 'action' else 0x303 if time == start else 0),
             'Pre-store state is genuine, not fabricated after cleanup')
        store_order.append(stores.index(found))
        return found
    store('body', start, 0x12, 0x16, 0xff838cf0)
    store('flags', start, 0, 0x10, 0xff877d50)
    store('action', start, 0x303, 4, release_entry+0x90)
    store('action', start+release_total, 4, 0x604, recovery_pc[identity])
    store('action', ready, 0x604, 0, 0xff83edd0)
    store('body', ready, 0x16, 0x12, 0xff83eeb0)
    store('flags', ready, 0x10, 0, 0xff83efc0)
    store('action', ready, 0, 0x303, 0xff9065d0)
    need(store_order == sorted(set(store_order)), 'Original setup/recovery/individual cleanup/walk stores ordered within fields')
    need(n(handoff, 'action') == 0 and h(handoff, 'flags') == 0 and h(handoff, 'body') == 0x12 and
         all(h(handoff, k) == 0 for k in ('vx', 'vy', 'gravity', 'trail')) and
         h(handoff, 'entry') == 0xff861500 and h(handoff, 'pc') == 0xff861510,
         'First original ready handoff after individual native cleanup')
    for time in range(ready+1, ready+11):
        r = by[time]
        need(n(r, 'action') == 0x303 and h(r, 'flags') == 0 and h(r, 'body') == 0x12 and
             h(r, 'vx') == 0x28000 and all(h(r, k) == 0 for k in ('vy', 'gravity', 'trail')) and
             h(r, 'xraw') == h(entry, 'xraw')+(time-ready-1)*0x28000 and r['yraw'] == entry['yraw'],
             'Ten clean native forward-walk fields after shot with actual 2.5-pixel physics')
    need(n(child, 'frame') == start+birth_age and n(child, 'serial') == 1 and
         h(child, 'entry') == (0xfffc6000 if identity == 17 else 0xfffc7000) and
         h(child, 'pc') == h(child, 'entry')+16 and n(child, 'id') == identity and
         child['owner'] == entry['actor'] and
         len({h(entry, k) for k in pointers} | {h(child, 'actor'), h(child, 'main')}) == 6,
         'Distinct real owned projectile child born at authored field')
    need(retire['actor'] == child['actor'] and retire['main'] == child['main'] and
         retire['owner'] == child['owner'] and n(retire, 'child_serial') == 1 and
         h(retire, 'pc') == 0xff8b6830, 'Actual original retirement of that child, not body or another projectile')
    effects = groups['EFFECT']
    need([n(r, 'frame') for r in effects] == list(range(start+birth_age+1, retired+1)),
         'Every child lifetime field once, none after retirement')
    for r in effects:
        need(r['actor'] == child['actor'] and r['main'] == child['main'] and r['owner'] == entry['actor'] and
             n(r, 'id') == identity and n(r, 'child_serial') == n(r, 'serial') == 1 and n(r, 'type') == 81 and
             h(r, 'vy') == 0 and h(r, 'velocity_parameter') == 0x80000 and
             0x01000000 <= h(r, 'list') < 0x01100000 and r['list'] == effects[0]['list'],
             'Every child field retains actual owner, type, draw-list and native velocity parameter')
    child_groups = [r for r in groups['GROUP'] if r['child'] == '1']
    for r in child_groups:
        need(r['actor'] == child['actor'] and r['main'] == child['main'] and n(r, 'id') == identity and
             n(r, 'serial') == 1 and h(r, 'pc') == 0xff8387a0 and h(r, 'vy') == 0,
             'Every real child group uses actual executing child Main and native renderer')
    hits = [r for r in groups['HEALTH'] if start <= n(r, 'frame') <= end]
    contact = None
    if scenario == 'block':
        hit = one(hits, 'declared projectile chip health store')
        contact = n(hit, 'frame')
        need(hit['slot'] == '2' and n(hit, 'before')-n(hit, 'after') == 6 and
             h(hit, 'pc') == 0xff836700 and hit['a8'] == child['actor'] and hit['a13'] == child['main'],
             'One actual native six-chip health write from projectile, not actor or observer')
        need(retired == contact+len(IMPACT[identity])*4, 'Complete four-field impact holds then retirement')
    else:
        need(not hits and identity == 18, 'Ducked miss has no native damage store')
    last = contact if contact is not None else retired
    flight_x = h(entry, 'xraw') + (-12 if identity == 17 else 8)*0x10000
    flight_y = h(entry, 'yraw') + (-40 if identity == 17 else 0)*0x10000
    travelling = [r for r in child_groups if h(r, 'group') in FLIGHT[identity] and h(r, 'vx') == 0x80000]
    expected_times = list(range(start+flight_age, last+1, flight_hold))
    need([n(r, 'frame') for r in travelling] == expected_times and bool(travelling),
         'Every travelling group with exact one/three-field authored cadence')
    for i, r in enumerate(travelling):
        need(h(r, 'group') == FLIGHT[identity][i % len(FLIGHT[identity])] and
             h(r, 'xraw') == flight_x+i*flight_hold*0x80000 and h(r, 'yraw') == flight_y,
             'Full native travelling pose order and eight-pixel group physics')
    intro = [r for r in child_groups if h(r, 'group') in INTRO]
    if identity == 17:
        need([h(r, 'group') for r in intro] == list(INTRO) and
             [n(r, 'frame')-start for r in intro] == list(range(3, 21, 3)) and
             all(h(r, 'vx') == 0 and h(r, 'xraw') == h(entry, 'xraw')-100*0x10000 and
                 h(r, 'yraw') == h(entry, 'yraw')-72*0x10000 for r in intro), 'Full stopped knife intro and body-relative origin')
    else:
        need(not intro, 'Ring has no held knife intro')
    bursts = [r for r in child_groups if h(r, 'group') in IMPACT[identity]]
    redraws = [r for r in child_groups if h(r, 'group') in FLIGHT[identity] and h(r, 'vx') == 0]
    need(len(child_groups) == len(intro)+len(travelling)+len(bursts)+len(redraws), 'No unexplained child group')
    if contact is None:
        need(not bursts and not redraws and len(travelling) >= len(FLIGHT[identity]),
             'Ducked miss completes full flight cycle with no impact or alignment')
    else:
        need([h(r, 'group') for r in bursts] == list(IMPACT[identity]) and
             [n(r, 'frame') for r in bursts] == list(range(contact, retired, 4)) and
             len(redraws) == 2 and all(n(r, 'frame') == contact and h(r, 'group') == h(travelling[-1], 'group')
                                     for r in redraws), 'Exact native alignment redraws and complete burst order')
        offset = -34 if identity == 17 else -106
        impact_x = h(redraws[-1], 'xraw')+offset*0x10000
        # Declared grounded blocked fixtures only. This is not a general hit
        # height/collision proof; original impact physics adjusts the Y origin.
        impact_y = h(entry, 'yraw')+(32*0x10000 if identity == 17 else 0)
        impact_vx = 0 if identity == 17 else 0x20000
        for i, r in enumerate(bursts):
            need(h(r, 'xraw') == impact_x+i*4*impact_vx and h(r, 'yraw') == impact_y and
                 h(r, 'vx') == impact_vx, 'Exact native aligned blocked impact group origin and motion')
    for r in effects:
        time, age = n(r, 'frame'), n(r, 'frame')-start
        if identity == 17 and age <= flight_age:
            index = min((age-4)//3, 5)
            wanted = (INTRO[index], h(entry, 'xraw')-100*0x10000, h(entry, 'yraw')-72*0x10000,
                      0x80000 if age == flight_age else 0, 0)
        elif identity == 18 and age == flight_age:
            wanted = (FLIGHT[18][0], h(entry, 'xraw'), h(entry, 'yraw'), 0x80000, 0)
        elif contact is None or time <= contact:
            elapsed = time-(start+flight_age+1)
            wanted = (FLIGHT[identity][(elapsed//flight_hold) % len(FLIGHT[identity])],
                      flight_x+elapsed*0x80000, flight_y, 0x80000, 0)
        else:
            elapsed = time-contact-1
            wanted = (IMPACT[identity][elapsed//4], impact_x+elapsed*impact_vx, impact_y, impact_vx, 0x500)
        need((h(r, 'pose'), h(r, 'xraw'), h(r, 'yraw'), h(r, 'vx'), n(r, 'action')) == wanted,
             'Every child intro/handoff/travel/impact pose, state and exact raw physics field')
    for r in [entry, *fields]:
        time = n(r, 'frame')
        need(n(r, 'hp') == n(entry, 'hp') and n(r, 'vhp') == n(entry, 'vhp')-
             (6 if contact is not None and time > contact else 0), 'Whole paired health ledger agrees with actual native store')
    # Inputs are chosen at the beginning of the callback field. Actual CPU
    # ENTRY executes later that field; reacted duck input starts next field.
    inputs = [r for r in groups['INPUT'] if start < n(r, 'frame') <= end]
    need([n(r, 'frame') for r in inputs] == list(range(start+1, end+1)), 'Every post-entry human-only input field recorded')
    if scenario == 'duck_miss':
        need(all(r['buttons'] == 'Down' and r.get('phase') == 'duck_projectile' for r in inputs),
             'Ducked miss uses genuine held P2 Down')
    else:
        guarding = [r for r in inputs if contact-3 <= n(r, 'frame') <= contact]
        # Original FF837D40 tests Main flag bit 0. Cage can block while
        # finishing get-up (action 0), before the standing block graphic.
        need(len(guarding) == 4 and all(r['buttons'] == 'Block' for r in guarding) and
             h(by[contact], 'vflags') & 1 and n(by[contact], 'vypos') == n(by[contact], 'vfloor') and
             h(by[contact], 'vvy') == 0, 'Actual P2 Block before contact and native grounded victim guard flag')
    return dict(passed=True, identity=identity, human=human, scenario=scenario, start=start, ready=ready,
                child_birth=n(child, 'frame'), retired=retired, complete=end, terminal=end+30,
                release_fields=release_total, recovery_fields=recovery, child_fields=len(effects),
                travelling_groups=len(travelling), full_flight_cycle=len(travelling) >= len(FLIGHT[identity]),
                impact_groups=len(bursts), chip_damage=6 if contact is not None else 0,
                native_clean_walk_fields=10, source_or_gameplay_changed=False,
                scope=SCOPE, whole_character_integration_complete=False)


def verify(folder, identity, scenario, version):
    observer = f'mk2ks_cpu_projectile_followup_{version}_probe.lua'
    runner = 'run_cpu_projectile_followup_v5_probe.ps1'
    launch, log, original = matched_launch(folder, observer, runner)
    nested = folder/'input_sources/mk2ks_cold_p2_selection.lua'
    source = nested.read_text()
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)', source), 'Nested cold selector cannot write guest state')
    need("dofile('mk2ks_cold_p2_selection.lua')" in (folder/'input_sources'/observer).read_text() and
         any(Path(p).name == nested.name and digest(nested) == sha
             for p, sha in launch['input_hashes'].items()), 'Nested selector is exact matched frozen launch input')
    return verify_log(log, identity, scenario, original)
