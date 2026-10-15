"""Actual missed CPU Knife: ungated constructor, pool lifetime and native return.

Qualify retained27520 without replay. Preserve the entire previously proven
49-field fighter/53-field projectile mechanics. Independently bind all639
ungated records, every captured source word, active/free membership, both
masked allocation/return stores and later original reuse of the same record.
No complete projectile FIFO/DMA/pixel or all-context acceptance is inferred.
"""
import json
import struct
import traceback
from pathlib import Path
import capture_native_selector_sonya_walkin_kano_cpu as capture
import qualify_native_selector_sonya_walkin_pairs as paired

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
OUT = ROOT/'audit_native_selector_sonya_walkin_knife_pool_checked'
PARENT = paired.OUT/'report.json'
TAG = 'MK2_STARTUP_PROJECTILE_'
rows = paired.rows


def one(records, label):
    need(len(records) == 1, label)
    return records[0]


def h(record, key):
    return int(record[key], 16)


def pool_stores(records, guest, frame, pc, actor, main, child, pop):
    selected = [r for r in records if int(r['frame']) == frame and h(r, 'pc') == pc]
    need(len(selected) == 2 and [h(r, 'at') for r in selected] == [0x01060130, 0x01060140]
         and int(selected[1]['sequence']) == int(selected[0]['sequence'])+1,
         'Both consecutive original native low/high free-head stores')
    for r in selected:
        shift = h(r, 'at')-0x01060130
        before, data, mask, merged = (h(r, k) for k in ('before', 'data', 'mask', 'merged'))
        need(mask == 65535 and
             merged == ((before & ~(mask << shift)) | ((data & mask) << shift)) & 0xffffffff and
             h(r, 'target') == h(r, 'a0') == child and
             (h(r, 'a8'), h(r, 'a13')) == (actor, main) and
             r['writes'] == '0' and r['assistance'] == 'none',
             'Full masked store arithmetic, actual operand, owner and executing Main')
        words = struct.unpack_from('<HHH', guest, (pc-48-0xff800000)//8)
        need(words == tuple(h(r, 'op'+str(n)) for n in range(3)) and
             words == ((0x0782 if pop else 0x0780), 0x0130, 0x0106),
             'Actual complete original native allocation/return instruction operands')
    low, high = selected
    need(h(high, 'before') == h(low, 'merged'), 'Independent low/high store continuity')
    if pop:
        need(h(low, 'before') == child and
             h(high, 'merged') == h(low, 'targetNext') == h(high, 'targetNext') == h(low, 'a2'),
             'Native creator removes the exact child from the original free-list head')
    else:
        need(h(low, 'targetNext') == h(high, 'targetNext') == h(low, 'before') == h(low, 'a2') and
             h(high, 'merged') == child,
             'Native child returns itself ahead of the prior free-list head')
    return selected


def gate(text, guest):
    _, mechanics = paired.followup(text, guest, 2)
    need(mechanics['typedKnifeFollowup'] and mechanics['actuallyMissed'] and
         (mechanics['start'], mechanics['bodyFields'], mechanics['childFields'], mechanics['nativeRetirement']) ==
         (2256, 49, 53, 2312), 'Whole unmodified actual missed Knife physical contract')
    ordered = []
    for line in text.splitlines():
        if line.startswith(TAG):
            ordered.extend(rows(line, line.split()[0]))
    need(len(ordered) == 639 and [int(r['sequence']) for r in ordered] == list(range(1, 640)) and
         all(r['writes'] == '0' and r['assistance'] == 'none' for r in ordered),
         'Entire actual ungated sequence, no dropped callbacks or assistance')
    source_words = 0
    for tag, ranges in ((TAG+'CODE', {(0xfffc3800, 0xfffc8000), (0xff8b6820, 0xff8b69a0)}),
                        ('MK2_BLADE_ALLOC_CODE', {(0xff8090c0, 0xff809280), (0xff8096c0, 0xff809800),
                                                (0xff83efd0, 0xff83f060), (0xfff8d800, 0xfff8d980)})):
        codes = rows(text, tag)
        need(len(codes) == len(ranges) and {(h(r, 'start'), h(r, 'stop')) for r in codes} == ranges,
             'Whole captured constructor, release, retirement and native pool code windows')
        for r in codes:
            lo, hi = ((h(r, k)-0xff800000)//8 for k in ('start', 'stop'))
            words = [int(v, 16) for v in r['words'].split(',')]
            need(struct.pack('<'+'H'*len(words), *words) == guest[lo:hi],
                 'Every captured native program word equals independent current guest')
            source_words += len(words)
    events = rows(text, TAG+'EVENT')
    for r in events:
        address = h(r, 'entry')
        need(h(r, 'pc') == address+16 and h(r, 'mask') == 65535 and
             h(r, 'opcode') == struct.unpack_from('<H', guest, (address-0xff800000)//8)[0],
             'Every ungated executed opcode, native PC and full read mask')
    child, main, parent, parent_main = 0x01031d10, 0x0106bf30, 0x010350a0, 0x0106a370
    victim, victim_main = 0x01034e90, 0x0106b840
    constructor = {}
    for kind, frame in (('knife', 2256), ('knife_release', 2256), ('knife_create', 2259)):
        r = one([r for r in events if r['kind'] == kind], 'One actual ungated '+kind)
        need(int(r['frame']) == frame and
             (h(r, 'a8'), h(r, 'a13'), h(r, 'owner'), h(r, 'p2'), h(r, 'p2main')) ==
             (parent, parent_main, parent, parent, parent_main) and
             (h(r, 'p1'), h(r, 'p1main')) == (victim, victim_main) and
             r['id'] == '17' and r['type'] == '80' and r['roster'] == '18,17' and
             r['states'] == '1,0' and r['mode'] == '2',
             'True CPU Kano parent/Main and native Sonya victim, never projectile/global alias')
        constructor[kind] = r
    birth = one([r for r in events if r['kind'] == 'knife_child'], 'One native child allocation')
    need(int(birth['frame']) == 2259 and
         (h(birth, 'a8'), h(birth, 'a13'), h(birth, 'owner'), h(birth, 'parent'), h(birth, 'victim')) ==
         (child, main, child, parent, victim_main) and
         birth['parent_id'] == birth['id'] == '17' and birth['type'] == '81' and
         birth['process_slot'] == '2048' and h(birth, 'parameter') == 0x80000 and
         birth['roster'] == '18,17' and birth['states'] == '1,0' and birth['mode'] == '2' and
         0x0102d6f0 <= child < 0x0105b950 and (child-0x0102d6f0) % 0x210 == 0,
         'Distinct source-defined projectile process, true native pool record and original parent')
    fields = rows(text, TAG+'FIELD')
    native = paired.knife.overlap.rows(text, 'CHILD_FIELD')
    need([int(r['frame']) for r in fields] == list(range(2260, 2313)) and len(native) == 53,
         'Every independently observed child field through native retirement')
    native_by = {r['frame']: r for r in native}
    for r in fields:
        n = native_by[int(r['frame'])]
        need(r['kind'] == 'knife_child' and r['birth'] == '2259' and
             (h(r, 'actor'), h(r, 'main'), h(r, 'owner'), h(r, 'parent'), h(r, 'original_parent')) ==
             (child, main, child, parent, parent) and r['id'] == '17' and r['type'] == '81' and
             r['mode'] == '2' and (r['active'], r['free'], r['active_valid'], r['free_valid']) == ('1', '0', '1', '1') and
             all(h(r, k) == n[k] for k in
                 ('actor', 'main', 'owner', 'pose', 'xraw', 'yraw', 'vx', 'vy', 'flags', 'body', 'parameter')) and
             h(r, 'parent') == n['shot_owner'],
             'Each child pose/physical word and independent native active/free pool membership')
    groups = [r for r in events if r['kind'] == 'group']
    old_groups = [r for r in paired.knife.overlap.rows(text, 'EVENT') if r['kind'] == 'group' and r['a8'] == child]
    need(len(groups) == len(old_groups) == 40, 'All forty native child group invocations')
    for r, n in zip(groups, old_groups):
        need(int(r['frame']) == n['frame'] and
             all(h(r, k) == n[k] for k in ('a8', 'a13', 'pc', 'a0', 'a4', 'a5', 'xraw', 'yraw', 'vx', 'body', 'pose', 'action')) and
             (h(r, 'owner'), h(r, 'parent'), h(r, 'victim')) == (child, parent, victim_main),
             'Independent executing group ABI and physical state agree for the whole child')
    retire = one(rows(text, TAG+'RETIRE'), 'One actual ungated retirement')
    event = one([r for r in events if r['kind'] == 'retire'], 'One actual retirement opcode')
    need(retire['frame'] == event['frame'] == '2312' and retire['birth'] == '2259' and
         h(retire, 'original_parent') == parent and
         all(retire[k] == event[k] for k in event if k not in ('kind', 'sequence')) and
         (h(retire, 'a8'), h(retire, 'a13'), h(retire, 'owner'), h(retire, 'parent')) == (child, main, child, parent),
         'Retirement belongs to the original exact child/Main and parent, not a reused address')
    need(not rows(text, TAG+'HEALTH'), 'Actual miss: no manufactured child hit or guard damage')
    terminal = one(rows(text, TAG+'RESULT'), 'One original terminal observer receipt')
    need(terminal['frame'] == '3615' and terminal['live_children'] == '0', 'No outstanding original child at native terminal')
    heads = rows(text, 'MK2_BLADE_ALLOC_HEAD_STORE')
    pop = pool_stores(heads, guest, 2259, 0xff809150, parent, parent_main, child, True)
    push = pool_stores(heads, guest, 2312, 0xff8097d0, child, main, child, False)
    later = [r for r in heads if int(r['frame']) > 2312 and h(r, 'target') == child]
    need(later and int(later[0]['frame']) == 2365 and h(later[0], 'pc') == 0xff809150,
         'Later actual native allocation reuses the returned record, not persistent projectile ownership')
    reuse = pool_stores(heads, guest, 2365, 0xff809150, 0x0106467a, 0x01069c80, child, True)
    need(not [r for r in fields if int(r['frame']) > 2312] and not
         [r for r in groups if int(r['frame']) > 2312], 'No ungated child lifetime is incorrectly extended through later reuse')
    return dict(passed=True, actualMissedKnifeMechanics=mechanics, ungatedRecords=len(ordered),
        sourceProgramWords=source_words, independentlyAllocatedChildFields=len(fields),
        independentNativeGroupInvocations=len(groups), actualNativePoolPop=pop,
        actualNativePoolPush=push, actualLaterNativeRecordReuse= reuse,
        laterReuseFrame=2365, nativeTerminalFrame=3615, fullProjectilePixelsAccepted=False)


def execute(state):
    need(not OUT.exists(), 'New immutable missed Knife pool qualification')
    parent = json.loads(PARENT.read_text())
    folder, text, _ = capture.RAM_CASES[capture.KEY]
    held = capture.NATIVE_HANDLES[capture.KEY]
    meta = json.loads((folder/'result.json').read_text())
    pins = dict(parent['inputHashes'])
    need(parent['passed'] and meta['passed'] and held['process'].poll() == meta['nativeExit'] == 0 and
         held['identity'] == parent['actualNativeIdentity'] == meta['nativeTerminal']['actualWindowsIdentity'] and
         (held['identity']['ProcessId'], held['identity']['ParentProcessId'], held['identity']['createdUnix']) ==
         (27520, 38752, 1791760361.8604069) and not capture.original.previous.choices.current.prior.identity.census() and
         all(sha(p) == d for p, d in pins.items()), 'Same retained native terminal, exact identity and complete frozen inputs')
    positive = gate(text, state['guest'])
    trials = [
        ('ungated_sequence', TAG+'FIELD', 'sequence', '1', dict(frame='2260')),
        ('active_pool_missing', TAG+'FIELD', 'active', '0', dict(frame='2280')),
        ('early_free', TAG+'FIELD', 'free', '1', dict(frame='2280')),
        ('invalid_active_chain', TAG+'FIELD', 'active_valid', '0', dict(frame='2280')),
        ('invalid_free_chain', TAG+'FIELD', 'free_valid', '0', dict(frame='2280')),
        ('independent_child_parent', TAG+'FIELD', 'parent', '01034E90', dict(frame='2280')),
        ('independent_child_pose', TAG+'FIELD', 'pose', 'FF614800', dict(frame='2280')),
        ('constructor_owner', TAG+'EVENT', 'owner', '01031D10', dict(kind='knife_create')),
        ('constructor_type', TAG+'EVENT', 'type', '81', dict(kind='knife_create')),
        ('child_process', TAG+'EVENT', 'process_slot', '1', dict(kind='knife_child')),
        ('child_opcode', TAG+'EVENT', 'opcode', '09E1', dict(kind='knife_child')),
        ('independent_group_parent', TAG+'EVENT', 'parent', '01034E90', dict(kind='group',frame='2278')),
        ('retire_original_parent', TAG+'RETIRE', 'original_parent', '01034E90', dict(frame='2312')),
        ('live_child_at_terminal', TAG+'RESULT', 'live_children', '1', dict(frame='3615')),
        ('pool_pop_operand', 'MK2_BLADE_ALLOC_HEAD_STORE', 'a0', '01031F20', dict(sequence='2485')),
        ('pool_pop_high_word', 'MK2_BLADE_ALLOC_HEAD_STORE', 'merged', '01000000', dict(sequence='2486')),
        ('pool_push_next', 'MK2_BLADE_ALLOC_HEAD_STORE', 'targetNext', '01031F20', dict(sequence='2577')),
        ('pool_push_opcode', 'MK2_BLADE_ALLOC_HEAD_STORE', 'op0', 'FFFF', dict(sequence='2578')),
        ('later_reuse_owner', 'MK2_BLADE_ALLOC_HEAD_STORE', 'a8', '01031D10', dict(sequence='2603')),
        ('later_reuse_high_word', 'MK2_BLADE_ALLOC_HEAD_STORE', 'merged', '01000000', dict(sequence='2604')),
    ]
    faults = []
    for label, tag, key, value, where in trials:
        matching = [line for line in text.splitlines() if line.startswith(tag+' ') and
                    all(rows(line,tag)[0].get(k) == v for k,v in where.items())]
        line = one(matching, 'One effective actual fault target '+label)
        old = rows(line,tag)[0][key]
        need(old != value, 'Effective corruption '+label)
        import re
        changed = re.sub(r'\b'+key+r'=\S+', key+'='+value, line, count=1)
        try:
            gate(text.replace(line,changed,1),state['guest'])
        except (ValueError, AssertionError, KeyError, IndexError) as error:
            faults.append(dict(fault=label,rejectedBy=str(error)))
        else:
            raise ValueError('Native missed Knife pool corruption admitted '+label)
    for label, address in (('child_constructor_source', 0xfffc6000), ('native_pool_pop_source', 0xff809120),
                           ('native_pool_push_source', 0xff8097a0)):
        bad = bytearray(state['guest']); bad[(address-0xff800000)//8] ^= 1
        try:
            gate(text,bytes(bad))
        except (ValueError, AssertionError, KeyError, IndexError) as error:
            faults.append(dict(fault=label,rejectedBy=str(error)))
        else:
            raise ValueError('Native program corruption admitted '+label)
    need(len(faults) == 23 and gate(text,state['guest']) == positive, 'Twenty-three effective faults reject, whole positive restored')
    for path in (Path(__file__).resolve(), PARENT.resolve(), ROOT/'mk2ks_native_selector_cpu_startup_guard.lua',
                 ROOT/'mk2ks_blade_allocation_v2892.lua'):
        key=str(path); digest=sha(path)
        need(key not in pins or pins[key] == digest, 'No old executed source/evidence replaced')
        pins[key]=digest
    need(all(sha(p) == d for p,d in pins.items()), 'Whole immutable source/evidence inventory after actual faults')
    result = dict(passed=True, goalStatus='active', actualNativeIdentity=held['identity'],
        actualMissedKnifePoolLifetime=positive, actualFaultsRejected=faults, inputHashes=pins,
        requirements=parent['requirements'], remainingGroups=parent['remainingGroups'],
        fullProjectilePixelsAccepted=False, allArenaCPUContextsAccepted=False, fullPortAcceptance=False,
        publicPlayableChanged=False, newNativeGames=0, newBuilds=0, newROMCopies=0, newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS missed Knife native constructor,53 pool fields,40 groups,pop/push/reuse,23 faults',flush=True)
    return result


def safe_execute(state):
    try:
        return execute(state)
    except Exception as error:
        need(not OUT.exists(), 'Preserve original qualification rejection')
        OUT.mkdir(); (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
