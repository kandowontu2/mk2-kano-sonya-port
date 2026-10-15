"""Source-bound lifetime of all seven differing attached-blade addresses.

Fourteen unassisted new/control fixtures preserve the exact original native
combat chronology. Every blade's real original free-head pop, parent Main
attachment, field-by-field descriptor/pose/list membership, original retirement
and detach/reuse are checked without address normalization.
Immediate reuse is accepted only with a later source-bound original pool pop
under a new Main, non-blade descriptor and continuously detached parent. This accepts legitimate
allocator provenance, NOT a universal renderer/audio/CPU/morph or RNG cause.
"""
import json
import re
import struct
import sys
import traceback
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_native_combat_regression_v2854 as combat
import run_blade_allocation_dispatch_v2896 as dispatch

ROOT = assembly.ROOT
OUT = ROOT / 'audit_v2910_blade_allocation_checked'
HEX = set('actor parent parentOwner parentAction main owner object at before data mask merged target targetNext pc a0 a2 a8 a10 a13 sp returnPC op0 op1 op2 entry freeHead trail pose descriptor palette freeStop start stop'.split())
# CODE's start/stop are hex addresses; CONTEXT_RESULT start is a decimal frame.


def rows(log, tag):
    result = []
    for line in log.splitlines():
        if not line.startswith('MK2_BLADE_ALLOC_' + tag + ' '):
            continue
        pairs = re.findall(r'(\w+)=([^\s]+)', line)
        assembly.need(len(pairs) == len(dict(pairs)), 'Unique actual allocation observer fields')
        result.append({k: v if k in ('assistance', 'words') else int(v, 16 if k in HEX and not (tag == 'CONTEXT_RESULT' and k == 'start') else 10)
                       for k, v in pairs})
    return result


def need(ok, label):
    assembly.need(ok, label)


def pool(a):
    return 0x0102d6f0 <= a < 0x0105b950 and (a - 0x0102d6f0) % 0x210 == 0


def one(items, label):
    need(len(items) == 1, label)
    return items[0]


def verify_log(log, guest, kind, side, victim):
    need(not re.search(r'LUA ERROR|fatal error|access violation|stack traceback', log, re.I), 'No runtime/observer failure')
    if kind == 'interrupt':
        original = combat.interrupt.verify_interrupt(log, 'blade', side, victim)
        native_fields = combat.interrupt.rows(log, 'FIELD')
    else:
        original = combat.lifecycle.verify(log, 'blade', side, victim)
        need(original['passed'], 'Original complete native KO contract ' + str(original['errors']))
        native_fields = combat.lifecycle.rows(log, 'FIELD')
    for tag in ('CREATE', 'TRAIL_STORE', 'HEAD_STORE', 'CLEANUP', 'RETIRE', 'FIELD', 'CONTEXT_RESULT', 'CODE', 'RESULT'):
        need(all(r['writes'] == 0 and r['assistance'] == 'none' for r in rows(log, tag)), 'Read-only actual allocation scope')
    code = rows(log, 'CODE')
    wanted_ranges = {(0xff8090c0, 0xff809280), (0xff8096c0, 0xff809800), (0xff83efd0, 0xff83f060), (0xfff8d800, 0xfff8d980)}
    need(len(code) == 4 and {(r['start'], r['stop']) for r in code} == wanted_ranges, 'Entire four actual allocator/retirement/attachment code windows')
    original_rom = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
    for r in code:
        lo, hi = ((r[k] - 0xff800000) // 8 for k in ('start', 'stop'))
        words = [int(w, 16) for w in r['words'].split(',')]
        need(len(words) == (hi - lo) // 2 and struct.pack('<' + 'H' * len(words), *words) == guest[lo:hi],
             'Whole actually executed code window independently reconstructed')
        if r['start'] < 0xfff80000:
            need(guest[lo:hi] == original_rom[lo:hi], 'Original allocator, pool push and trail cleanup program unchanged')
    def opcode(pc, words):
        need(struct.unpack_from('<' + 'H' * len(words), guest, (pc - 0xff800000) // 8) == words, 'Independent original native store instruction')
    opcode(0xff809120, (0x0782, 0x0130, 0x0106))
    opcode(0xff8097a0, (0x0780, 0x0130, 0x0106))
    opcode(0xfff8d950, (0xb34d, 0x0190))
    opcode(0xff83f030, (0xb20d, 0x0190))
    heads = rows(log, 'HEAD_STORE')
    terminal = one(rows(log, 'RESULT'), 'One actual allocation terminal')
    need(heads and [r['sequence'] for r in heads] == list(range(1, len(heads) + 1)) and terminal['headStores'] == len(heads),
         'Complete native free-head store history')
    current = heads[0]['before']
    for r in heads:
        shift = r['at'] - 0x01060130
        need(shift in (0, 16) and r['mask'] == 0xffff and r['before'] == current, 'Continuous original 32-bit free-head word history')
        current = ((current & ~(r['mask'] << shift)) | ((r['data'] & r['mask']) << shift)) & 0xffffffff
        need(r['merged'] == current, 'Every actual native head half-store independently merged')
        offset = (r['pc'] - 48 - 0xff800000) // 8
        need(0 <= offset <= len(guest) - 6 and struct.unpack_from('<HHH', guest, offset) == (r['op0'], r['op1'], r['op2']),
             'Every actual free-head writer matches the independent guest instruction words')
        if r['pc'] in (0xff809150, 0xff8097d0):
            popped = r['pc'] == 0xff809150
            want = r['a2'] if popped else r['a0']
            need(pool(r['target']) and r['target'] == r['a0'] and r['data'] == ((want >> shift) & 0xffff) and
                 (r['op0'], r['op1'], r['op2']) == ((0x0782 if popped else 0x0780), 0x0130, 0x0106),
                 'Actual original sprite pop/push target and exact live register data')
    head_by_sequence = {r['sequence']:r for r in heads}
    def complete_head_store(low, value):
        high = head_by_sequence.get(low['sequence'] + 1)
        need(high is not None and low['at'] == 0x01060130 and high['at'] == 0x01060140 and
             high['frame'] == low['frame'] and high['before'] == low['merged'] and
             high['merged'] == value and high['data'] == value >> 16 and
             all(high[k] == low[k] for k in ('context','pc','target','targetNext','a0','a2','a8','a10','a13')),
             'Full original 32-bit native head transaction, including cross-high-word pointer changes')
        return high
    contexts = rows(log, 'CONTEXT_RESULT')
    need(len(contexts) == terminal['contexts'] == (2 if kind == 'interrupt' else 8) and
         [r['context'] for r in contexts] == list(range(1, len(contexts) + 1)), 'Every original active blade creation through retirement')
    creates, stores, fields = rows(log, 'CREATE'), rows(log, 'TRAIL_STORE'), rows(log, 'FIELD')
    cleanups, retires = rows(log, 'CLEANUP'), rows(log, 'RETIRE')
    by = {(r['frame'], r['slot']): r for r in native_fields}
    need(len(by) == len(native_fields), 'Unique actual unchanged participant callbacks')
    expected = [(0xfe82fc40 + i * 0x60, 0xfff8f800 + i * 160)
                for i, hold in enumerate(combat.lifecycle.BLADE_HOLDS) for _ in range(hold)]
    proofs = []
    for ctx in contexts:
        n, start, end = ctx['context'], ctx['start'], ctx['detached']
        obj, actor, main = ctx['object'], ctx['parent'], ctx['main']
        need(ctx['side'] == side and pool(obj) and start == ctx['attached'] < end < terminal['frame'],
             'Actual distinct owned sprite allocation, attachment and later detach')
        creation = one([r for r in creates if r['context'] == n], 'One actual blade constructor')
        need((creation['frame'], creation['actor'], creation['owner'], creation['main'], creation['id'], creation['side'],
              creation['entry'], creation['pc'], creation['freeHead']) ==
             (start, actor, actor, main, 17, side, 0xfff8d800, 0xfff8d810, obj), 'Native constructor owns the exact observed free-head object')
        pop = one([r for r in heads if r['frame'] == start and r['context'] == n and r['pc'] == 0xff809150 and
                   r['at'] == 0x01060130 and r['target'] == obj], 'One actual original sprite head pop')
        pop_high = complete_head_store(pop, pop['a2'])
        need(pop['before'] == pop['a0'] == obj and pop['targetNext'] == pop['a2'] and
             pop['a8'] == actor and pop['a13'] == main, 'Exact native next-link pop under original parent registers')
        all_stores = [r for r in stores if r['context'] == n]
        ledger = [r for r in all_stores if start <= r['frame'] <= end]
        later_zero_stores = [r for r in all_stores if r['frame'] > end]
        need(len(all_stores) == len(ledger) + len(later_zero_stores), 'No pre-construction trail store spliced into context')
        for r in later_zero_stores:
            # The mode/round transition's ORIGINAL native MOVB zero-fill can
            # revisit a reclaimed Main slot. Retain every such raw store,
            # require before/data/merged all zero, the exact stock byte-clear
            # PC/instruction and its actual pointer. Never silently drop it.
            offset = (r['pc'] - 32 - 0xff800000) // 8
            need(r['before'] == r['data'] == r['merged'] == 0 and
                 r['pc'] == 0xff83a100 and (r['op0'],r['op1']) == (0x0388,0x8c20) and
                 r['a0'] in (r['at'],r['at']+8) and r['at'] in (main+0x190,main+0x1a0) and
                 guest[offset:offset+4] == original_rom[offset:offset+4] == struct.pack('<HH',r['op0'],r['op1']),
                 'Every later Main-slot zero-fill is an actual unchanged original MOVB, never a stale attachment')
        need(len(ledger) == 4 and [r['at'] for r in ledger] == [main + 0x190, main + 0x1a0] * 2 and
             [r['frame'] for r in ledger] == [start, start, end, end], 'Complete original attach/detach half-store history')
        trail = 0
        for i, r in enumerate(ledger):
            need(r['before'] == trail and r['actor'] == r['a8'] == actor and r['main'] == r['a13'] == main and r['mask'] == 0xffff,
                 'Actual physically owned Main trail store, not pointer substitution')
            shift = r['at'] - (main + 0x190)
            trail = ((trail & ~(0xffff << shift)) | (r['data'] << shift)) & 0xffffffff
            need(r['merged'] == trail and r['pc'] == (0xfff8d970 if i < 2 else 0xff83f050) and
                 (r['op0'], r['op1']) == ((0xb34d if i < 2 else 0xb20d), 0x0190) and
                 r['a10'] == obj and (r['a0'] == 0x51 if i < 2 else r['a0'] == 0), 'Independent attachment/clear source and live original operands')
        need(trail == 0 and ledger[1]['merged'] == obj, 'Exact full-width native attach followed by zero detach')
        cleanup = one([r for r in cleanups if r['context'] == n], 'One actual original owning cleanup')
        retire = one([r for r in retires if r['context'] == n], 'One actual original blade retirement')
        for r, pc, entry in ((cleanup, 0xff83efe0, 0xff83efd0), (retire, 0xff840460, 0xff840450)):
            need((r['frame'], r['actor'], r['main'], r['object'], r['trail'], r['a8'], r['a13'], r['pc'], r['entry']) ==
                 (end, actor, main, obj, obj, actor, main, pc, entry), 'Actual owned original cleanup/retirement execution')
        need(retire['a0'] == obj, 'Original retirement receives the exact attached sprite')
        push = one([r for r in heads if r['frame'] == end and r['context'] == n and r['pc'] == 0xff8097d0 and
                    r['at'] == 0x01060130 and r['target'] == obj], 'One actual original free-list push')
        push_high = complete_head_store(push, obj)
        need(push['a0'] == obj and push['targetNext'] == push['before'] == push['a2'] and
             push['a8'] == actor and push['a13'] == main, 'Retired original sprite linked to the actual previous free head')
        timeline = [r for r in fields if r['context'] == n]
        need([r['frame'] for r in timeline] == list(range(start + 1, end + 3)) and
             end - start == (10 if kind == 'interrupt' and n == 1 else 38), 'Every original attached phase and two post-retirement fields')
        reuse_fields = []
        for r in timeline:
            need((r['side'], r['parent'], r['parentOwner'], r['parentID'], r['main'], r['object'], r['mode']) ==
                 (side, actor, actor, 17, main, obj, 2) and r['activeValid'] == r['freeValid'] == 1 and
                 r['freeStop'] in (0x00fe0190, 0x0105b950), 'Valid original native render/free lists and stable actual parent ownership')
            native = by.get((r['frame'], side))
            need(native is not None and (native['actor'], native['main'], native['trail'], native['pose'], native['action']) ==
                 (actor, main, r['trail'], r['pose'], r['parentAction']), 'Independent participant callback equals exact raw observer ownership and trail')
            if r['frame'] <= end:
                pose, descriptor = expected[r['frame'] - start - 1]
                need((r['trail'], r['active'], r['free'], r['attached'], r['detached'], r['pose'], r['descriptor']) ==
                     (obj, 1, 0, start, -1, pose, descriptor), 'Every source-derived body/blade phase owns its actual allocated active sprite')
            else:
                need(r['trail'] == 0 and r['detached'] == end, 'Immediate post-retirement parent remains natively detached')
                if (r['active'], r['free']) == (0, 1):
                    pass
                else:
                    # The interrupted blade slot is returned and immediately
                    # reused for stock counter-hit blood in the SAME field.
                    # Never treat a later occupant as the old attached blade.
                    reuse = [h for h in heads if h['sequence'] > push_high['sequence'] and
                             h['frame'] < r['frame'] and h['pc'] == 0xff809150 and
                             h['at'] == 0x01060130 and h['target'] == obj]
                    latest = reuse[-1] if reuse else None
                    need(latest is not None, 'Actual new original pop required before address reuse')
                    complete_head_store(latest, latest['a2'])
                    need(latest['before'] == obj and latest['targetNext'] == latest['a2'] and
                         latest['a13'] != main and (r['active'], r['free']) == (1, 0) and
                         not 0xfff8f800 <= r['descriptor'] <= 0xfff8fda0,
                         'Reoccupied address has a NEW actual original free-head pop, new Main, non-blade descriptor and no parent attachment')
                    reuse_fields.append(dict(frame=r['frame'], nativeReuseSequence=latest['sequence'],
                                             nativeReuseFrame=latest['frame'], newMain=latest['a13'],
                                             actualNewDescriptor=r['descriptor']))
        proofs.append(dict(context=n, object=obj, parent=actor, main=main, start=start, nativePopSequence=pop['sequence'], nativePopFinalSequence=pop_high['sequence'],
                           attached=start, nativeRetirement=end, nativePushSequence=push['sequence'], nativePushFinalSequence=push_high['sequence'], detached=end,
                           attachedFields=end-start, detachedFields=2, laterOriginalZeroFillStores=len(later_zero_stores), postRetirementNativeReuse=reuse_fields, addressUnnormalized=True))
    return dict(passed=True, originalContract=original, contexts=proofs, completeHeadStoreRows=len(heads),
                allActualAllocationAttachmentRetirementSourceBound=True, rawStackTopNotAcceptedAsReturnAddress=True,
                allocationAddressProvenanceAccepted=True, exactHardwareRNGCauseAccepted=False, fullPortAcceptance=False)


def verify():
    pins = assembly.source_check()
    new, old, payload, _, _ = assembly.expected()
    def pin(path, wanted=None):
        path = Path(path)
        path = path if path.is_absolute() else ROOT/path
        key = str(path.absolute())
        actual = assembly.sha(path)
        need(wanted is None or actual == wanted, 'Immutable actual allocation dependency ' + key)
        need(key not in pins or pins[key] == actual, 'Consistent actual dependency ' + key)
        pins[key] = actual
    previous_path = combat.OUT/'report.json'
    previous = json.loads(previous_path.read_text())
    pin(previous_path)
    need(previous['passed'] and len(previous['cases']) == 20, 'Earlier original accepted combat contracts')
    difference_path = ROOT/'audit_v2861_native_combat_differences/report.json'
    differences = json.loads(difference_path.read_text())
    pin(difference_path)
    changed = [r for r in differences['cases'] if r['changedParticipantFields']]
    need(len(changed) == 7 and {r['case'] for r in changed} ==
         {f'audit_v2853_{kind}_blade_p{side}_{victim}' for kind, side, victim in dispatch.FIXTURES}, 'All and only seven recorded raw blade differences covered')
    ran_path = dispatch.OUT/'report.json'
    ran = json.loads(ran_path.read_text())
    pin(ran_path)
    need(ran['allRunnersTerminal'] and ran['allRunnerExitsZero'] and len(ran['cases']) == 14 and
         ran['bothActualBuilds'] == dispatch.BUILDS, 'All actual new/control runners terminal')
    pin(dispatch.__file__, ran['sourceSHA256'])
    pin(dispatch.OUT/Path(dispatch.__file__).name, ran['sourceSHA256'])
    cases = {}
    for kind, side, victim in dispatch.FIXTURES:
        pair = {}
        for build_name, candidate in dispatch.BUILDS.items():
            folder = ROOT/dispatch.leaf(build_name, kind, side, victim)
            meta = json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
            before = json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
            info_path = ROOT/candidate/'build-info.json'
            info = json.loads(info_path.read_text(encoding='utf-8-sig'))
            pin(info_path)
            need(meta['exit_code'] == 0 and meta['observer_passed'] and meta['candidate'] == candidate and
                 (meta['kind'], meta['move'], meta['side'], meta['victim']) == (kind, 'blade', side, victim) and
                 not meta['cheats'] and not meta['cheats_enabled'] and meta['guest_writes'] == meta['emulator_resets'] == 0 and
                 not meta['saved_states_used'] and meta['assistance'] == meta['memory_assistance'] == 'none' and before == meta['input_hashes'],
                 'Actual terminal unchanged physical input fixture, no guest state assistance')
            need(meta['executable_sha256'] == info['executable_sha256'] and meta['payload_sha256'] == info['payload_sha256'] and
                 all(before.get(file) == wanted for file, wanted in info['input_hashes'].items()), 'Entire actually compiled and launched build matched')
            pin(ROOT/candidate/'mkport_candidate.exe', info['executable_sha256'])
            pin(ROOT/candidate/'roms/mk2ks/mk2ks.mdata', info['payload_sha256'])
            need((ROOT/candidate/'roms/mk2ks/mk2ks.mdata').read_bytes() == payload, 'Independent unchanged complete donor payload')
            for file, wanted in before.items():
                pin(file, wanted)
                path = Path(file)
                if path.suffix in ('.lua', '.ps1', '.json'):
                    pin(folder/'input_sources'/path.name, wanted)
                if path.suffix == '.lua':
                    need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(', path.read_text()), 'Read-only emulated observations and original physical inputs only')
            guest = new if build_name == 'new' else old
            need((folder/'guest_maincpu.bin').read_bytes() == guest, 'Every actually executed guest byte independently assembled')
            log = (folder/'run.log').read_text(encoding='utf-8-sig')
            baseline = ROOT/(f'audit_v2853_{kind}_blade_p{side}_{victim}' if build_name == 'new' else
                             f'audit_v{1869 if kind == "interrupt" else 1871}_{kind}_blade_p{side}_{victim}')/'run.log'
            pin(baseline, previous['inputHashes'][str(baseline)])
            prefix = 'MK2_INTERRUPT_' if kind == 'interrupt' else 'MK2_LIFE_TRACE_'
            chronology = lambda text: [line for line in text.splitlines() if line.startswith(prefix)]
            need(chronology(log) == chronology(baseline.read_text(encoding='utf-8-sig')), 'Entire original native combat chronology exact under added allocation observer')
            result = verify_log(log, guest, kind, side, victim)
            result.update(case=folder.name, build=build_name, wholeActualGuestReconstructed=True, originalNativeChronologyExact=True)
            pair[build_name] = result
            for file in folder.rglob('*'):
                if file.is_file():
                    pin(file)
            print(folder.name + ': all actual native blade allocations attached/retired/reclaimed', flush=True)
        need(len(pair['new']['contexts']) == len(pair['old']['contexts']), 'Both actual builds retain every same blade lifetime')
        pair['actualAddressDifferences'] = [dict(context=a['context'], actual=a['object'], previous=b['object'])
                                          for a, b in zip(pair['new']['contexts'], pair['old']['contexts']) if a['object'] != b['object']]
        need(pair['actualAddressDifferences'], 'Actual address differences reproduced, not masked or normalized away')
        cases[f'{kind}_p{side}_{victim}'] = pair
    for module in tuple(sys.modules.values()):
        file = getattr(module, '__file__', None)
        if file:
            path = Path(file).absolute()
            if path.is_relative_to(ROOT/'tools') and path.suffix == '.py':
                pin(path)
    return dict(passed=True, candidate=assembly.NAME, control=assembly.prior.NAME, cases=cases, actualFixtures=14,
                actualBladeLifetimes=sum(len(r[b]['contexts']) for r in cases.values() for b in ('new', 'old')),
                allSevenChangedBladeAddressesSourceBound=True, noAddressNormalization=True, originalPhysicalInputStrategiesUnchanged=True,
                wholeActualGuestReconstructedForBothBuilds=True, originalNativeChronologyExactForEveryFixture=True,
                exactHardwareRNGCauseAccepted=False, fullRendererOrAudioAccepted=False, allCPUOrMorphsAccepted=False,
                fullPortAcceptance=False, scope=__doc__, inputHashes=pins)


if __name__ == '__main__':
    need(not OUT.exists(), 'Immutable source-bound allocation proof')
    try:
        report = verify()
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), fullPortAcceptance=False)
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes', 'cases')}, indent=2), flush=True)
    raise SystemExit(0 if report['passed'] else 1)
