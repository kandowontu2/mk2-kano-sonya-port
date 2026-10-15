"""Ordered native walk -> CPU uppercut -> recovery -> cleanup provenance.

This is a declared uninterrupted uppercut continuation, not all CPU actions,
stock moves, KO, artwork or whole-character acceptance. Stores are pre-write
observations: the native setup still sees 0303 until the action word is written.
"""
import re
import struct
from verify_cpu_recovery import HEX, TEXT, rows

POSES = {
    18: (0xff0303a0, 0xff030400, 0xff030460, 0xff0304a0, 0xff0304e0,
         0xff030540, 0xff030580),
    3: (0xff93f570, 0xff93f5d0, 0xff93f630, 0xff93f690, 0xff93f6f0,
        0xff93f770, 0xff93f7d0),
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def records(log):
    result = []
    for index, line in enumerate(log.splitlines()):
        match = re.match(r'MK2_CPU_PAIR_(FLOW|FLAG|ACTION) ', line)
        if not match:
            continue
        pairs = re.findall(r'(\w+)=([^\s]+)', line)
        need(len({k for k, v in pairs}) == len(pairs), 'Duplicate provenance key')
        row = {k: v if k in TEXT else int(v, 16 if k in HEX or k in
               ('at', 'before', 'after') else 10) for k, v in pairs}
        row.update(tag=match[1], index=index)
        result.append(row)
    return result


def original_instructions(original):
    # Instruction plus operands, including word stores, masks, original
    # recovery call and real normal-walk action setter. No state aliases.
    pins = {
        0xff870880: (0x0d3f, 0x0732),
        0xff870920: (0x09c1, 0x0106),
        0xff870940: (0x09c9, 0x0015),
        0xff870a60: (0x18c0,),
        0xff870a70: (0x09c1, 0x0600),
        0xff870a90: (0xc000, 0x058a),
        0xff838ca0: (0x0bae, 0x0004, 0x0000),
        0xff838cd0: (0xb1c8, 0x0160),
        0xff877d00: (0x0ba4, 0x0010, 0x0000),
        0xff877d30: (0xb08d, 0x0210),
        0xff83c320: (0xb02d, 0x01f0),
        0xff8763c0: (0x0d5f, 0xed80, 0xff83),
        0xff83ed80: (0x5600,),
        0xff83edb0: (0xb00d, 0x01f0),
        0xff83ee90: (0xb088, 0x0160),
        0xff83efa0: (0xb08d, 0x0210),
        0xff9065b0: (0xb00d, 0x01f0),
    }
    for address, words in pins.items():
        need(struct.unpack_from('<' + 'H' * len(words), original,
                                (address - 0xff800000) // 8) == words,
             f'Exact original action instruction {address:08X}')
    return len(pins)


def verify_followup(log, actor, main, identity, after, before, field_tag='FIELD',
                    terminal_clean=False):
    need(identity in POSES, 'Declared authored uppercut identity')
    events = records(log)
    begins = [r for r in events if r['tag'] == 'FLOW' and r['entry'] == 0xff870880
              and r['slot'] == 1 and after < r['frame'] <= before]
    need(len(begins) == 1, 'One actual native CPU uppercut after original pair cleanup')
    begin = begins[0]
    start, clear = begin['frame'], begin['frame'] + 33
    selected = [r for r in events if r['slot'] == 1 and start <= r['frame'] <= clear]
    for r in selected:
        need((r['actor'], r['main'], r['a8'], r['a13'], r['id'], r['state'],
              r['cpu_slot'], r['human_slot'], r['writes'], r['assistance']) ==
             (actor, main, actor, main, identity, 0, 1, 2, 0, 'none') and r['cycle']==begin['cycle'],
             'Every native continuation instruction/store has actual CPU ownership')
        if r['tag'] == 'FLOW':
            need(r['pc'] == r['entry'] + 16, 'Actual first-word instruction fetch')
        else:
            need(r['at'] == (actor + 0x160 if r['kind'] == 'body' else
                            main + 0x210 if r['kind'] == 'flags' else main + 0x1f0),
                 'Store targets actual owning body/Main word')
            need(r['kind'] in ('body', 'flags', 'action'), 'Typed native store')
            need(r['y'] == r['floor'] and r['vx'] == r['vy'] == r['gravity'] == 0,
                 'Native uppercut stores remain stopped and grounded')
    need(begin['action'] == 0x303 and begin['flags'] & 0x1c == 0 and
         begin['body'] & 0x0c == 0, 'New attack begins with cleared walk, not stale pair locks')

    def one(tag, pc, frame, **wanted):
        found = [r for r in selected if r['tag'] == tag and r['pc'] == pc and
                 r['frame'] == frame and all(r.get(k) == v for k, v in wanted.items())]
        need(len(found) == 1, f'Unique native {tag} {pc:08X} at {frame}')
        return found[0]

    setup = one('FLOW', 0xff877bd0, start, action=0x303, flags=begin['flags'], body=begin['body'])
    body = one('FLAG', 0xff838cf0, start, kind='body', action=0x303,
               before=begin['body'], after=begin['body'] | 4)
    flags = one('FLAG', 0xff877d50, start, kind='flags', action=0x303,
                before=begin['flags'], after=begin['flags'] | 0x10)
    attack = one('FLOW', 0xff837460, start, action=0x303, a1=0x106, a9=0x15)
    writer = one('FLOW', 0xff83c330, start, action=0x303, a1=0x106)
    assigned = one('ACTION', 0xff83c340, start, kind='action', action=0x303,
                   before=0x303, after=0x106)
    recover = one('FLOW', 0xff876360, start + 21, action=0x106, a0=6, a1=0x600)
    recovery_writer = one('FLOW', 0xff83c330, start + 21, action=0x106, a1=0x600)
    recovery = one('ACTION', 0xff83c340, start + 21, kind='action', action=0x106,
                   before=0x106, after=0x600)
    cleanup = one('FLOW', 0xff8763d0, clear, action=0x600)
    native_clear = one('FLOW', 0xff83ed90, clear, action=0x600)
    cleared = one('ACTION', 0xff83edd0, clear, kind='action', action=0x600,
                  before=0x600, after=0)
    body_clear = one('FLAG', 0xff83eeb0, clear, kind='body', action=0,
                     before=begin['body'] | 4, after=begin['body'] & 0xfff3)
    flags_clear = one('FLAG', 0xff83efc0, clear, kind='flags', action=0,
                      before=begin['flags'] | 0x10, after=begin['flags'] & 0xffeb)
    walk = one('ACTION', 0xff9065d0, clear, kind='action', action=0, before=0, after=0x303)
    chain = [begin, setup, body, flags, attack, writer, assigned, recover,
             recovery_writer, recovery, cleanup, native_clear, cleared,
             body_clear, flags_clear, walk]
    need(all(a['index'] < b['index'] for a, b in zip(chain, chain[1:])),
         'Exact within-field setup/action/recovery/clear/walk ordering')
    need([r for r in selected if r['tag'] == 'ACTION'] ==
         [assigned, recovery, cleared, walk], 'No hidden intervening CPU action stores')
    for r in selected:
        if r['tag'] == 'FLAG' and start <= r['frame'] < clear:
            need(r['frame'] == start and r['pc'] in (0xff838cf0, 0xff877d50) and
                 r['action'] == 0x303 and r['after'] == r['before'] |
                 (4 if r['kind'] == 'body' else 0x10), 'Only native new-attack setup locks')

    timeline = [r for r in rows(log, field_tag) if start < r['frame'] <= clear + 1]
    need([r['frame'] for r in timeline] == list(range(start + 1, clear + 2)),
         'Every uppercut/recovery/first-clean field exactly once')
    poses = [p for p, count in zip(POSES[identity], (3, 3, 3, 3, 9, 6, 6))
             for _ in range(count)]
    origin = timeline[0]
    for index, r in enumerate(timeline):
        need((r['actor'], r['main'], r['owner'], r['id'], r['roster'], r['state'], r['mode'],
              r['cpu_slot'], r['human_slot'], r['writes'], r['assistance']) ==
             (actor, main, actor, identity, identity, 0, 2, 1, 2, 0, 'none') and r['cycle']==begin['cycle'] and
             r['vowner'] == r['vactor'] and r['vid'] == r['vroster'] and r['vstate'] == 1 and
             0 < r['hp'] <= 161 and 0 < r['vhp'] <= 161,
             'Live actual CPU/human match throughout uninterrupted follow-up')
        need(all(r[k] == origin[k] for k in ('vactor', 'vmain', 'vid', 'schedule', 'stage', 'hp', 'xraw', 'yraw')),
             'Stable ownership, campaign, own health and uppercut position')
        need(r['y'] == r['floor'] and r['vx'] == r['vy'] == r['gravity'] == r['trail'] == 0,
             'Every follow-up field is stopped, grounded and detached')
        if index < 33:
            need(r['pose'] == poses[index] and r['action'] == (0x106 if index < 21 else 0x600) and
                 r['flags'] & 0x1c == 0x10 and r['body'] & 0x0c == 4,
                 'Every authored uppercut/recovery pose, cadence and native lock')
        else:
            need(r['action'] == 0x303 and r['flags'] & 0x1c == 0 and r['body'] & 0x0c == 0,
                 'First subsequent walk field is genuinely clear')
    if terminal_clean:
        prior = [r for r in rows(log, field_tag) if after < r['frame'] <= start]
        need([r['frame'] for r in prior] == list(range(after + 1, start + 1)) and
             all(r['actor'] == actor and r['main'] == main and r['owner'] == actor and
                 r['id'] == r['roster'] == identity and r['state'] == 0 and r['mode'] == 2 and
                 r['action'] == 0x303 and r['flags'] & 0x1c == 0 and r['body'] & 0x0c == 0 and
                 r['y'] == r['floor'] and r['vy'] == r['gravity'] == r['trail'] == 0 and
                 abs(r['vx'] - (0x100000000 if r['vx'] & 0x80000000 else 0)) <= 0x30000
                 for r in prior), 'Every intervening walk field is clear after actual pair handoff')
        late = [r for r in rows(log, field_tag) if r['frame'] > clear]
        need(late and [r['frame'] for r in late] == list(range(clear + 1, late[-1]['frame'] + 1)),
             'Continuous terminal follow-up fields')
        need(all(r['actor'] == actor and r['main'] == main and r['owner'] == actor and
                 r['id'] == r['roster'] == identity and r['state'] == 0 and r['mode'] == 2 and
                 r['action'] == 0x303 and r['flags'] & 0x1c == 0 and r['body'] & 0x0c == 0 and
                 r['y'] == r['floor'] and r['vx'] == r['vy'] == r['gravity'] == r['trail'] == 0
                 for r in late), 'No residual paired/uppercut locks through terminal CPU walk')
    return dict(start=start, recovery=start + 21, clear=clear, authored_fields=33,
                first_clean=clear + 1, ordered_native_events=len(chain),
                actual_CPU_id=identity, state_store_before_completion=True,
                scope='one_original_CPU_uppercut_full_action_recovery_and_first_clean_walk_not_all_actions_or_KO')
