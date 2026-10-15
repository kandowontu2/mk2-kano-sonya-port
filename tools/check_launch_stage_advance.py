"""Whole retained native stage contract, actual mutations and source clocks."""
import copy
import json
import struct
import types
from decimal import Decimal
from pathlib import Path
import launch_stage_advance_contract_v3 as stage
import launch_stage_advance_audio_v2 as audio

ROOT, need, sha = stage.ROOT, stage.need, stage.sha


def cached_gate(records, text, guest):
    globals_copy = dict(stage.gate.__globals__, inventory=lambda ignored: records)
    return types.FunctionType(stage.gate.__code__, globals_copy)(text, guest)


def semantics(c, game):
    text, guest = c['text'], c['guest']
    records = stage.inventory(text)
    need(cached_gate(records, text, guest)[0] == game, 'Whole unchanged native gate with complete parsed records')
    faults = []
    def reject(label, tag, predicate, key=None, value=None, omit=False):
        changed = dict(records)
        changed[tag] = list(records[tag])
        n = next(i for i, r in enumerate(changed[tag]) if predicate(r))
        if omit:
            changed[tag].pop(n)
        else:
            need(changed[tag][n].get(key) != value, 'Effective actual state mutation '+label)
            changed[tag][n] = dict(changed[tag][n], **{key: value})
        try:
            cached_gate(changed, text, guest)
        except (ValueError, KeyError, IndexError) as error:
            faults.append(dict(kind=label, rejectedBy=str(error)))
        else:
            raise ValueError('Actual native contract fault admitted '+label)
    for tag in ('WALK', 'JUMP', 'PUNCH', 'RECOVER'):
        reject('actual '+tag+' response omitted', 'MK2_NAT_CAMPAIGN_'+tag, lambda r: True, omit=True)
    by = {(int(r['frame']), int(r['slot'])): r for r in records['MK2_KO_FIELD']}
    for event, key, value in [('walk', 'x', records['MK2_NAT_CAMPAIGN_WALK'][0]['fromX']),
                              ('jump', 'y', by[game['events']['jump'], 2]['floor']),
                              ('jump', 'action', '1283'), ('punch', 'action', '771'),
                              ('recover', 'flags', '00000005')]:
        at = str(game['events'][event])
        reject('actual '+event+' '+key+' changed', 'MK2_KO_FIELD', lambda r, at=at: r['frame'] == at and r['slot'] == '2', key, value)
    first_win = records['MK2_NAT_CAMPAIGN_WIN'][0]
    for key, wrong in [('id', '0'), ('pc', 'FF8296B1'), ('health', '11,1')]:
        reject('native winner '+key+' corrupted', 'MK2_NAT_CAMPAIGN_WIN', lambda r: r is first_win, key, wrong)
    reject('normal paid Start omitted', 'MK2_NAT_CAMPAIGN_INPUT', lambda r: r['button'] == 'Start' and int(r['frame']) > 4781, omit=True)
    for key, wrong in [('stage', '0'), ('cpu', '0'), ('schedule', 'FFFA3781')]:
        reject('earned advance '+key+' corrupted', 'MK2_NAT_CAMPAIGN_ADVANCE', lambda r: True, key, wrong)
    at = str(game['events']['reReady'])
    for slot, key, wrong in [('2', 'id', '0'), ('2', 'roster', '0'), ('2', 'state', '0'),
                              ('1', 'id', '18'), ('1', 'state', '1'), ('2', 'owner', '00000000')]:
        reject('next true slot'+slot+' '+key+' corrupted', 'MK2_KO_FIELD', lambda r, slot=slot: r['frame'] == at and r['slot'] == slot, key, wrong)
    reject('native collision opcode corrupted', 'MK2_INTERRUPT_HEALTH', lambda r: r['pc'] == 'FF836700', 'op0', '0000')
    reject('first physical callback omitted', 'MK2_KO_FIELD', lambda r: True, omit=True)
    reject('last physical callback omitted', 'MK2_KO_FIELD', lambda r: r['frame'] == str(game['terminal']) and r['slot'] == '2', omit=True)
    # A complete native zero-health finish interval, not an arbitrary delay.
    lethal = next(r for r in reversed(records['MK2_INTERRUPT_HEALTH']) if r['slot'] == '2' and r['pc'] == 'FF836700' and r['after'] == '0' and int(r['before']) > 0 and int(r['frame']) < int(first_win['frame']))
    reject('post-lethal loser health revived', 'MK2_KO_FIELD', lambda r: r['frame'] == str(int(lethal['frame'])+1) and r['slot'] == '2', 'hp', '1')
    need(cached_gate(records, text, guest)[0] == game, 'Entire original positive remains unchanged after actual faults')
    return dict(passed=True, actualFaultsRejected=faults)


def channels(c, launches, announcements, records=None):
    clock = audio.previous.clock
    records = stage.inventory(c['text']) if records is None else records
    callback = records['MK2_TOMB_MIX_CHANNEL']
    headers = c['pcmHeaders']
    need(len(callback) == 14*len(headers) and
         {(int(r['index']), int(r['channel'])) for r in callback} == {(i, n) for i in range(1, len(headers)+1) for n in range(14)},
         'All fourteen actual sources at every initial/interior/final callback')
    by = {(int(r['index']), int(r['channel'])): r for r in callback}
    events = launches+announcements
    initial = next(e for e in announcements if e['sample_id'] == 0)
    for i, h in enumerate(headers):
        tick = int(Decimal(h['seconds'])*50)
        sec, fraction = divmod(tick*960*(clock.ATTO//48000), clock.ATTO)
        output_end = sec*48000+(fraction+clock.PERIOD-1)//clock.PERIOD
        time = int(Decimal(h['seconds'])*clock.ATTO)
        for n in range(14):
            row = by[i+1, n]
            need(row['frame'] == h['frame'] and row['seconds'] == h['seconds'] and
                 row['writes'] == row['loop'] == row['paused'] == '0' and row['assistance'] == 'none',
                 'Exact passive finite nonlooping unpaused source callback')
            previous = [e for e in events if e['channel'] == n and e['start'] <= output_end]
            if previous:
                event = previous[-1]
                processed = min(len(event['positions']), max(0, output_end-event['start']))
                if 'stopAttoseconds' in event and time >= event['stopAttoseconds']:
                    processed = min(processed, event['generatedBeforeStop'])
                active = 0 < processed < len(event['positions']) and ('stopAttoseconds' not in event or time < event['stopAttoseconds'])
                saved = event['sample_id'] if active and (n == 0 or len(previous) > 1) else 4294967295
                wanted = event['positions'][processed-1] if processed else 0.0
                length = event['length']
            elif n == 0:
                # The initial physical Kano selection finished before capture.
                # The exact source already reconstructed for the paid reselect.
                saved, length, wanted = 4294967295, initial['length'], initial['positions'][-1]
            else:
                saved, length, wanted = 4294967295, 0, 0.0
            need(int(row['sample']) == saved and int(row['length']) == length and float(row['position']) == wanted and
                 row['bits'] == struct.pack('<d', wanted).hex().upper(),
                 'Every exact source saved ID/length/repeated-double position/EOF or hit retirement')
    battle = records['MK2_INTERRUPT_CHANNEL']
    begin, end = records['MK2_MAUDIO_BEGIN'][0], records['MK2_NAT_CAMPAIGN_STAGE_RESULT'][0]
    first, last = int(begin['frame']), int(end['frame'])
    need(len(battle) == 4*(last-first+1) and
         {(int(r['frame']), int(r['channel'])) for r in battle} == {(f, n) for f in range(first, last+1) for n in range(10,14)},
         'All four battle source states across every real physical callback')
    for r in battle:
        need(r['loop'] == r['paused'] == r['writes'] == '0' and r['assistance'] == 'none', 'Entire passive finite battle-state inventory')
        if r['channel'] in ('12', '13'):
            need(r['sample'] == '4294967295' and r['length'] == r['position'] == '0', 'Human Kano slot stays actually silent, never an invented launch')
    return dict(passed=True, completeCallbackChannelFields=len(callback), completeBattleChannelFields=len(battle),
                initialSelectionCarryInRetired=True, allSourceClockPositionsAccepted=True)


def channel_faults(c, launches, announcements, positive):
    records = stage.inventory(c['text'])
    faults = []
    def reject(label, tag, predicate, key=None, value=None, omit=False):
        changed = dict(records)
        changed[tag] = list(records[tag])
        at = next(i for i, r in enumerate(changed[tag]) if predicate(r))
        if omit:
            changed[tag].pop(at)
        else:
            need(changed[tag][at].get(key) != value, 'Effective source fault '+label)
            changed[tag][at] = dict(changed[tag][at], **{key: value})
        try:
            channels(c, launches, announcements, changed)
        except (ValueError, KeyError, IndexError) as error:
            faults.append(dict(kind=label, rejectedBy=str(error)))
        else:
            raise ValueError('Actual channel fault admitted '+label)
    for key, value in [('sample', '13'), ('length', '40719'), ('position', '1'), ('bits', '0000000000000000'), ('loop', '1'), ('paused', '1')]:
        reject('active Bicycle '+key+' corrupted', 'MK2_TOMB_MIX_CHANNEL', lambda r: r['channel'] == '10' and r['sample'] == '14', key, value)
    reject('retired cry position advances', 'MK2_TOMB_MIX_CHANNEL', lambda r: r['channel'] == '11' and r['length'] == '66523' and float(r['seconds']) > 126.1, 'position', '15200')
    reject('unused human source activated', 'MK2_TOMB_MIX_CHANNEL', lambda r: r['channel'] == '12', 'sample', '16')
    reject('first source callback omitted', 'MK2_TOMB_MIX_CHANNEL', lambda r: True, omit=True)
    reject('last source callback omitted', 'MK2_TOMB_MIX_CHANNEL', lambda r: r['index'] == str(len(c['pcmHeaders'])) and r['channel'] == '13', omit=True)
    need(channels(c, launches, announcements, records) == positive, 'Whole original source clock positive unchanged')
    return dict(passed=True, actualFaultsRejected=faults)


def ownership_faults(c, physical):
    records = stage.inventory(c['text'])
    def gate(actual):
        scope = dict(audio.source_events.__globals__, stage=types.SimpleNamespace(inventory=lambda ignored: actual))
        return types.FunctionType(audio.source_events.__code__, scope)(c, physical, {})
    positive, _ = gate(records)
    faults = []
    def reject(label, tag, predicate, key=None, value=None, omit=False):
        changed = dict(records)
        changed[tag] = list(records[tag])
        at = next(i for i, r in enumerate(changed[tag]) if predicate(r))
        if omit:
            changed[tag].pop(at)
        else:
            need(changed[tag][at].get(key) != value, 'Effective actual ownership fault '+label)
            changed[tag][at] = dict(changed[tag][at], **{key: value})
        try:
            gate(changed)
        except (ValueError, KeyError, IndexError) as error:
            faults.append(dict(kind=label, rejectedBy=str(error)))
        else:
            raise ValueError('Actual source ownership fault admitted '+label)
    for key, value in [('a8', '01000000'), ('a13', '01000000'), ('pc', 'FFFFCAC1'), ('mask', '00FF')]:
        reject('CPU source marker '+key+' corrupted', 'MK2_MAUDIO_SOUND', lambda r: r['word'] == '6B00', key, value)
    for key, value in [('actor', '01000000'), ('main', '01000000'), ('id', '17'), ('health', '161')]:
        reject('active CPU source '+key+' corrupted', 'MK2_INTERRUPT_OWNER', lambda r: r['slot'] == '1' and r['id'] == '18', key, value)
    reject('retired source revived at next arena', 'MK2_INTERRUPT_OWNER', lambda r: r['frame'] == '7937' and r['slot'] == '1', 'actor', '01036960')
    reject('first owner callback omitted', 'MK2_INTERRUPT_OWNER', lambda r: True, omit=True)
    reject('last owner callback omitted', 'MK2_INTERRUPT_OWNER', lambda r: r['frame'] == '8215' and r['slot'] == '2', omit=True)
    restored, _ = gate(records)
    keys = ('start', 'generatedBeforeStop', 'stopAttoseconds', 'lastStreamUpdateAttoseconds')
    need([[e[k] for k in keys] for e in restored] == [[e[k] for k in keys] for e in positive], 'Whole original source ownership positive unchanged')
    return dict(passed=True, actualFaultsRejected=faults)
