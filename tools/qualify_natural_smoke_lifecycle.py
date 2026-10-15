"""Original secret gates plus actual native KO/rebuild and physical responses.

Do not relabel the old uninterrupted-round/walking-marker checker. The whole
captured interval is retained; walking is independently reconstructed BEFORE
incoming damage, and post-KO punch input is bound to the actual rebuilt round.
"""
import gzip
import hashlib
import inspect
import json
import math
from pathlib import Path
import check_natural_smoke_route as original

ROOT, need = original.ROOT, original.need


def lifecycle(records, by, first, last, side, own):
    health = records['MK2_SECRET_HEALTH']
    resets = [int(r['frame']) for r in health if first < int(r['frame']) <= last and r['pc'] == 'FF825930']
    unpublished = []
    phases = []
    for f in range(first, last+1):
        mode = by[f, 1]['mode']
        need(mode == by[f, 2]['mode'] and mode in ('2', '5', '7'), 'Whole actual secret battle/round-end/round-init modes')
        if not phases or phases[-1]['mode'] != mode:
            phases.append(dict(frame=f, mode=mode))
        for n, identity, state in ((side, own, 1), (3-side, 14, 0)):
            r = by[f, n]
            need(r['roster'] == str(identity) and r['state'] == str(state) and r['arena'] == '9',
                 'Every secret field retains original human/Smoke roles and secret arena')
            if r['actor'] == '00000000':
                need(mode == '5' and r['main'] == r['owner'] == '00000000' and r['id'] == '-1' and
                     any(f == reset+1 for reset in resets), 'Only original native round-init unpublished actor fields')
                unpublished.append(dict(frame=f, slot=n))
            else:
                need(r['actor'] == r['owner'] and r['id'] == str(identity) and int(r['main'], 16) >= 0x01000000,
                     'Every published secret actor has real character ID and exact Main owner')
                if f > first and by[f-1, n]['actor'] != '00000000':
                    need(r['actor'] == by[f-1, n]['actor'] and r['main'] == by[f-1, n]['main'],
                         'No published actor/Main replacement outside original round-init teardown')
            hp = int(r['hp'])
            need(0 <= hp <= 161 or (mode in ('5', '7') and hp == 65535), 'Native health/fill-sentinel range only')
            if hp == 0:
                lethal = [v for v in health if v['slot'] == str(n) and v['pc'] == 'FF836700' and
                          int(v['before']) > 0 and v['after'] == '0' and first <= int(v['frame']) < f]
                need(lethal and not any(int(lethal[-1]['frame']) < reset < f for reset in resets),
                     'Every zero-health secret field follows actual lethal collision, not forced loss')
    for reset in resets:
        need(any(r['slot'] == '2' and r['pc'] == 'FF825960' and int(r['frame']) == reset for r in health),
             'Both original full-health reset stores occur together')
        need(by[reset, 1]['mode'] == by[reset, 2]['mode'] == '5', 'Original round-end reset, not live-combat health assistance')
    ready = [p['frame'] for p in phases if p['mode'] == '2']
    for f in ready:
        need(by[f, 1]['hp'] == by[f, 2]['hp'] == '161', 'Each actual secret round begins with native full health')
    return dict(passed=True, phases=phases, originalResetFrames=resets, unpublishedFields=unpublished,
                originalNativeRoundStarts=ready, continuousSecretFieldsPerSlot=last-first+1)


def responses(records, by, first, last, side, own, life):
    result = records['MK2_STAGE_SECRET_RESULT'][0]
    inputs, health = records['MK2_STAGE_INPUT'], records['MK2_SECRET_HEALTH']
    reported = {k: int(result[k]) for k in ('walk', 'jump', 'punch', 'recover')}
    need(last == reported['recover']+180, 'Complete original recovery-to-terminal survival interval')
    jump = records['MK2_STAGE_SECRET_JUMP']
    punch = records['MK2_STAGE_SECRET_PUNCH']
    recover = records['MK2_STAGE_SECRET_RECOVER']
    need(len(jump) == len(punch) == len(recover) == 1, 'One reported actual jump/punch/recovery in this capture')
    flat = lambda r: r['y'] == r['floor'] and r['vy'] == r['gravity'] == '00000000' and not int(r['flags'], 16)&0x1c
    # Walking has nonzero horizontal velocity. Stationary recovery is not a walk.
    witness = None
    for start in range(first+1, int(jump[0]['start'])-1):
        values = [by[f, side] for f in range(start, start+3)]
        velocity = int(values[0]['vx'], 16)
        if velocity >= 2**31:
            velocity -= 2**32
        if not velocity or not all(r['mode'] == '2' and r['id'] == r['roster'] == str(own) and
                                   r['actor'] == r['owner'] and r['hp'] == values[0]['hp'] and r['action'] == '0' and
                                   r['vx'] == values[0]['vx'] and flat(r) for r in values):
            continue
        steps = [int(b['x'])-int(a['x']) for a,b in zip(values, values[1:])]
        if not all(step in (math.floor(velocity/65536), math.ceil(velocity/65536)) for step in steps):
            continue
        if abs(int(values[-1]['x'])-int(values[0]['x'])) < 4:
            continue
        direction = 'Right' if velocity > 0 else 'Left'
        if not all(any(int(v['frame']) == f and v['slot'] == str(side) and v['button'] == direction for v in inputs)
                   for f in range(start-1, start+2)):
            continue
        if any(v['slot'] == str(side) and start-1 <= int(v['frame']) <= start+2 and int(v['before']) > int(v['after']) for v in health):
            continue
        witness = dict(start=start, frame=start+2, fromX=int(values[0]['x']), toX=int(values[-1]['x']),
                       horizontalVelocity=velocity, physicalDirection=direction, actualSteps=steps)
        break
    need(witness is not None, 'Actual source-velocity grounded walking before damage, never knockback/recovery displacement')
    at, start = int(jump[0]['frame']), int(jump[0]['start'])
    r = by[at, side]
    need(witness['frame'] < start < at and at == reported['jump'] and int(r['y']) < int(r['floor']) and r['action'] != '1283' and
         any(v['slot'] == str(side) and v['button'] == 'Up' and start <= int(v['frame']) < at for v in inputs) and
         not any(v['slot'] == str(side) and start <= int(v['frame']) < at and int(v['before']) > int(v['after']) for v in health),
         'Actual physical jump, no incoming-hit airborne substitution')
    pat = int(punch[0]['frame'])
    pstart = max(int(punch[0]['start']), max(f for f in life['originalNativeRoundStarts'] if f <= pat))
    need(at < pstart < pat == reported['punch'] and by[pat, side]['action'] == '257' and
         any(v['slot'] == str(side) and v['button'] == 'High_Punch' and pstart <= int(v['frame']) < pat for v in inputs),
         'Actual ordinary punch uses input in its real current round, not pre-KO input carried over')
    rec = int(recover[0]['frame'])
    r = by[rec, side]
    need(pat < rec == reported['recover'] and flat(r) and r['vx'] == '00000000' and r['action'] in ('0', '771'),
         'Actual native grounded stationary recovery')
    for f in range(rec, last+1):
        for n in (1,2):
            r = by[f,n]
            need(r['mode'] == '2' and 0 < int(r['hp']) <= 161 and r['actor'] == by[rec,n]['actor'] and r['main'] == by[rec,n]['main'],
                 'Whole actual final survival remains alive in one stable native round')
    blocks = [int(r['frame']) for r in inputs if r['slot'] == str(side) and r['button'] == 'Block' and int(r['frame']) > rec]
    need(blocks == list(range(rec+1,last)), 'Every original finite Block survival input')
    return dict(walk=witness, jump=dict(start=start, frame=at), punch=dict(start=pstart, frame=pat), recover=rec,
                originalWalkMarkerAccepted=False, originalWalkMarker=reported['walk'],
                singleUninterruptedRoundControlSequenceAccepted=False,
                actualControlsAcrossOriginalNativeRoundLifecycleAccepted=True)


source = inspect.getsource(original.gate)
begin = source.index('    for f in range(secret, last+1):')
end = source.index("    need(by[secret, side]['hp']", begin)
source = source[:begin]+'    life = lifecycle(records, by, secret, last, side, own)\n'+source[end:]
begin = source.index('    events = {tag.lower():')
end = source.index('    return dict(passed=True', begin)
source = source[:begin]+'    events = responses(records, by, secret, last, side, own, life)\n'+source[end:]
source = source.replace('wholePhysicalAndHealthLedger=ledger, secretFightFieldsPerSlot=last-secret+1,',
                        'wholePhysicalAndHealthLedger=ledger, secretFightFieldsPerSlot=last-secret+1, nativeRoundLifecycle=life,')
scope = dict(vars(original), lifecycle=lifecycle, responses=responses)
exec(compile(source, __file__+'::whole_original_secret_gate_native_round_lifecycle', 'exec'), scope)
gate = scope['gate']


def qualify(c):
    need(c['report']['passed'] and c['terminal']['nativeExit'] == 0 and not original.capture_host.native.census(), 'Original actual native terminal passed')
    result = gate(c)
    path = c['folder']/'native_secret_lifecycle_contract.json'
    need(not path.exists(), 'Fresh additive proof, never rewrite old rejected contract')
    with gzip.open(c['folder']/'executed_sources.json.gz', 'wt', encoding='utf-8') as f:
        sources = {}
        for name, wanted in c['pins'].items():
            p = Path(name)
            raw = p.read_bytes()
            need(hashlib.sha256(raw).hexdigest().upper() == wanted, 'Every executed source/artifact unchanged before preservation')
            if p.suffix in ('.py','.lua'):
                sources[name] = dict(sha256=wanted, text=raw.decode())
        json.dump(sources, f)
    try:
        original.gate(c)
    except ValueError as e:
        need(str(e) == 'Every actual secret fight human/CPU actor/Main/health field', 'Exact original rejected stationary/no-KO contract preserved')
        result['originalRejectedContract'] = dict(passed=False, error=str(e), nativeGameFailure=False,
                                                sourceSHA256=hashlib.sha256(Path(original.__file__).read_bytes()).hexdigest().upper())
    else:
        raise ValueError('The originally rejected contract unexpectedly passed')
    result.update(candidate=original.capture_host.current.NAME, nativeTerminal=c['terminal'],
                  inputHashes=dict(c['pins']), sourceHashes={str(Path(p).resolve()):hashlib.sha256(Path(p).read_bytes()).hexdigest().upper() for p in (__file__,original.__file__)},
                  independentlyObservedWalkBeforeIncomingHit=True,
                  oldWalkMarkerNotUsedAsResponseEvidence=True, allSecretBranchesAccepted=False,
                  fullSecretAudioAccepted=False, fullPortAcceptance=False,
                  newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('passed','fighter','physicalSlot','earnedMatches','secretFightFieldsPerSlot')}),flush=True)
    return result
