"""Original CPU kick deliberately animates through C340, not C320's state store.

Declared blocked rounds followed by a miss, full native authored animation,
counter cadence, chip ledger and individual cleanup. Not every CPU move/KO.
"""
import struct
from verify_cpu_action_flow import records, need
from verify_cpu_recovery import rows
from verify_cpu_air_gate import rows as text_rows

KANO_SEQUENCE = (0xff00fcc0, 0xff00fd20, 0xff00fd80, 0, 0xff00fde0, 0xff00fe40,
                 0xff00fea0, 0, 0xff00fe40, 0xff00fde0, 1, 0xff001880, 0,
                 0xff00fd20, 0xff00fcc0, 0, 0xff00fe40, 0, 0xff00fde0, 0xff00ff00)


def instructions(original):
    pins = {
        0xff9b9470: (0x098c, 0x3840, 0xb00d, 0x02a0, 0xb02d, 0x01d0,
                     0x0d5f, 0x7bc0, 0xff87),
        0xff9b9500: (0x8789, 0x0d5f, 0x6090, 0xff90, 0x1860),
        0xff9b9590: (0xc080, 0xc340, 0xff83),
        0xff9b9650: (0x0d5f, 0x5440, 0xff83, 0xc93a),
        0xff9b9690: (0xb5a0, 0x02a0, 0x1420, 0xca36, 0xb00d, 0x02a0,
                     0xb5a0, 0x01d0, 0x0d5f, 0xdcc0, 0xff80),
        0xff9b9790: (0xc080, 0xc340, 0xff83),
        0xff9b9850: (0x0d5f, 0x5440, 0xff83, 0xc90c),
        0xff9b9880: (0xc90c, 0xb5a0, 0x02a0, 0x1420, 0xca08, 0xb00d,
                     0x02a0, 0xb5a0, 0x01d0, 0x0d5f, 0xdcc0, 0xff80),
        0xff9b9940: (0xc0bf,),
        0xff9b9950: (0x8789, 0x0d5f, 0x8650, 0xff83, 0x0d5f, 0x8680,
                     0xff83, 0x0d5f, 0x8680, 0xff83, 0x0d5f, 0x8680, 0xff83),
        0xff9b9a30: (0x8789, 0x0d5f, 0x8650, 0xff83, 0x0d5f, 0x8680,
                     0xff83, 0x0d5f, 0x8680, 0xff83),
        0xff9b9b20: (0xc080, 0xc340, 0xff83, 0x09ac, 0x021c, 0x09ac, 0x0080, 0x0127),
        0xff83c320: (0xb02d, 0x01f0, 0xa20c),
    }
    for address, words in pins.items():
        need(struct.unpack_from('<' + 'H' * len(words), original, (address-0xff800000)//8) == words,
             f'Original native CPU kick instructions {address:08X}')
    return len(pins)


def verify(log, start, original, identity=17, field_tag='FIELD', late_miss=False):
    need(identity in (17, 3), 'Declared actual Kano/stock control')
    instructions(original)
    fields = rows(log, field_tag)
    duration = 45 if late_miss else 37
    clear = start + duration
    timeline = [r for r in fields if start < r['frame'] <= clear + 1]
    need([r['frame'] for r in timeline] == list(range(start+1, clear+2)),
         'Every native CPU kick and first clear field')
    origin = timeline[0]
    actor, main, cycle = origin['actor'], origin['main'], origin['cycle']
    native = [r for r in records(log) if r['slot'] == 1 and start <= r['frame'] <= clear]
    for r in native:
        need((r['actor'], r['main'], r['a8'], r['a13'], r['id'], r['state'],
              r['cpu_slot'], r['human_slot'], r['writes'], r['assistance'], r['cycle']) ==
             (actor, main, actor, main, identity, 0, 1, 2, 0, 'none', cycle),
             'Actual published CPU owner of every kick instruction/store')
        if r['tag'] == 'FLOW':
            need(r['pc'] == r['entry'] + 16, 'Native typed first-word instruction fetch')
        else:
            need(r['at'] == (actor+0x160 if r['kind']=='body' else main+0x210 if r['kind']=='flags' else main+0x1f0),
                 'Native body/Main store target')

    def one(tag, pc, time, **wanted):
        found = [r for r in native if r['tag']==tag and r['pc']==pc and r['frame']==time and
                 all(r.get(k)==v for k,v in wanted.items())]
        need(len(found)==1, f'Unique kick {tag} {pc:08X} at {time}')
        return found[0]

    begin = one('FLOW', 0xff9b9480, start, action=0x303, a0=7, a1=2, a9=19)
    need(begin['flags']&0x1c==0 and begin['body']&0x0c==0, 'Kick begins genuinely clear')
    setup = one('FLOW', 0xff877bd0, start, action=0x303, attack_count=7, attack_delay=2)
    body = one('FLAG', 0xff838cf0, start, kind='body', action=0x303,before=begin['body'], after=begin['body']|4)
    flags = one('FLAG', 0xff877d50, start, kind='flags', action=0x303,before=begin['flags'], after=begin['flags']|0x10)
    root = 0xff001840 if identity==17 else 0xff93e8f0
    if identity==17:
        sequence = KANO_SEQUENCE
    else:
        sequence = struct.unpack_from('<20I', original, (root-0xff800000)//8)
    dumps = text_rows(log, 'MK2_CPU_PAIR_SEQUENCE')
    for time, address, expected in ((start, root, sequence), (start+22, root+0x100, sequence[8:])):
        found=[r for r in dumps if int(r['frame'])==time and r['slot']=='1' and int(r['at'],16)==address]
        need(len(found)==1, 'Unique actual native authored CPU sequence window')
        r=found[0]; words=tuple(int(w,16)for w in r['words'].split(','))
        need(len(words)==20 and words[:len(expected)]==tuple(expected) and
             (int(r['actor'],16),int(r['main'],16),int(r['id']),int(r['state']),int(r['cycle']))==
             (actor,main,identity,0,cycle) and r['cpu_slot']=='1' and r['human_slot']=='2' and
             r['writes']=='0' and r['assistance']=='none', 'Exact character-owned native sequence/loop/terminators')
    animation = one('FLOW',0xff9b9550,start,action=0x303,a9=root,attack_count=7,attack_delay=2)
    first = one('FLOW',0xff83c350,start,action=0x303,a0=3,a9=root)
    check1 = one('FLOW',0xff9b95d0,start+9,action=0x303,attack_count=7)
    second = one('FLOW',0xff83c350,start+11,action=0x303,a0=3,a9=root+0x80,attack_count=6)
    check2 = one('FLOW',0xff9b97d0,start+20,action=0x303,attack_count=6)
    returning = one('FLOW',0xff9b9550,start+22,action=0x303,a9=root+0x100,attack_count=5)
    check3 = one('FLOW',0xff9b95d0,start+31,action=0x303,attack_count=5)
    chain = [begin,setup,body,flags,animation,first,check1,second,check2,returning,check3]
    if late_miss:
        extra=one('FLOW',0xff83c350,start+33,action=0x303,a0=3,a9=root+0x80,attack_count=4)
        check4=one('FLOW',0xff9b97d0,start+42,action=0x303,attack_count=4)
        branch=one('FLOW',0xff9b9960,start+42,action=0x303)
        chain += [extra,check4,branch]
        recovery_at,recovery_pointer=start+42,root+0x200
    else:
        branch=one('FLOW',0xff9b9a40,start+31,action=0x303)
        chain.append(branch)
        recovery_at,recovery_pointer=start+31,root+0x1a0
    recovery=one('FLOW',0xff9b9ae0,recovery_at,action=0x303,a9=recovery_pointer)
    resumed=one('FLOW',0xff9b9b60,clear,action=0x303)
    ready=one('FLOW',0xff861360,clear,action=0x303,a9=19)
    cleanup=one('FLOW',0xff83ed90,clear,action=0x303)
    cleared=one('ACTION',0xff83edd0,clear,kind='action',before=0x303,after=0)
    clear_body=one('FLAG',0xff83eeb0,clear,kind='body',action=0,before=begin['body']|4,after=begin['body']&0xfff3)
    clear_flags=one('FLAG',0xff83efc0,clear,kind='flags',action=0,before=begin['flags']|0x10,after=begin['flags']&0xffeb)
    handoff=one('FLOW',0xff861510,clear,action=0)
    walk=one('ACTION',0xff9065d0,clear,kind='action',before=0,after=0x303)
    chain += [recovery,resumed,ready,cleanup,cleared,clear_body,clear_flags,handoff,walk]
    need(all(a['index']<b['index']for a,b in zip(chain,chain[1:])), 'Actual within-field native kick/recovery/cleanup ordering')
    need(not any(r['tag']=='ACTION' or r['tag']=='FLOW' and r['entry']==0xff83c320
                 for r in native if r['frame']<clear), 'Original C340 animation skips action-word writer, not a delayed fake state')
    pattern=[(0,3),(1,3),(2,5),(4,3),(5,3),(6,5),(8,3),(9,3)]
    pattern += [(2,5),(4,3),(5,3),(6,3),(16,3)] if late_miss else [(2,3),(13,3),(14,3)]
    poses=[sequence[index] for index,count in pattern for _ in range(count)]
    need(len(poses)==duration, 'Complete declared native kick duration')
    health=[r for r in rows(log,'HEALTH')if start<=r['frame']<=clear and r['before']!=r['after']]
    hit_times=[start+9,start+20]+([start+31] if late_miss else [])
    need([r['frame']for r in health]==hit_times and all(r['slot']==2 and r['pc']==0xff836700 and
         r['a8']==actor and r['a13']==main and r['before']-r['after']==3 and
         r['writes']==0 and r['assistance']=='none' and r['cycle']==cycle and r['cpu_slot']==1 and r['human_slot']==2
         for r in health), 'Every blocked roundhouse native three-point chip store')
    expected_health=origin['vhp']
    for i,r in enumerate(timeline):
        for store in health:
            if store['frame']==r['frame']-1:
                need(store['before']==expected_health, 'Continuous chip ledger')
                expected_health=store['after']
        need((r['actor'],r['main'],r['owner'],r['id'],r['roster'],r['state'],r['mode'],r['cycle'],r['writes'],r['assistance'])==
             (actor,main,actor,identity,identity,0,2,cycle,0,'none') and r['cpu_slot']==1 and r['human_slot']==2 and r['vowner']==r['vactor'] and
             r['vid']==r['vroster'] and r['vstate']==1 and 0<r['hp']<=161 and 0<r['vhp']<=161,
             'Living published native CPU/human identities throughout kick recovery')
        need(all(r[k]==origin[k]for k in ('vactor','vmain','vid','schedule','stage','hp','xraw','yraw')) and
             r['y']==r['floor'] and r['vy']==r['gravity']==r['trail']==0 and r['vhp']==expected_health,
             'Every kick field is grounded/stopped/detached with actual health continuity')
        need(r['action']==0x303, 'Original generic kick keeps its old action word')
        if i<duration:
            count=7 if i<9 else 6 if i<20 else 5 if not late_miss or i<31 else 4
            need(r['pose']==poses[i] and r['attack_count']==count and r['attack_delay']==2 and r['vx']==0 and
                 r['flags']&0x1c==0x10 and r['body']&0x0c==4, 'Every authored kick/loop/recovery pose, counter and lock')
        else:
            packed=0x28000005 if identity==17 else struct.unpack_from('<I',original,(0xff906ab0-0xff800000)//8+identity*4)[0]
            speed=(packed>>16)<<4
            wanted=speed if r['x']<r['vxpos'] else (-speed)&0xffffffff
            need(r['flags']&0x1c==0 and r['body']&0x0c==0 and r['vx']==wanted and r['attack_delay']==packed&0xffff,
                 'First subsequent CPU walk is clear with original actual-ID forward speed')
    return dict(start=start,clear=clear,first_clean=clear+1,actual_CPU_id=identity,
                native_pose_fields=duration,chip_damage=len(health)*3,
                ordered_events=len(chain),action_write_intentionally_skipped=True,
                scope='declared_original_blocked_CPU_roundhouse_and_miss_recovery_not_all_actions_hits_or_KO')
