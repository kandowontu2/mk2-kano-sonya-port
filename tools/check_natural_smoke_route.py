"""Finite native Smoke-entry proof, including whole HP history and controls.

Normal physical play only. Source-equivalent secret construction is necessary
but does not substitute for an actual native trigger and live fight.
"""
import collections
import hashlib
import inspect
import json
import re
import struct
from pathlib import Path
from types import SimpleNamespace
import capture_natural_smoke_route as capture_host
import qualify_launch_challenger_transition as prior

ROOT, need = capture_host.ROOT, capture_host.need


def inventory(text):
    records = collections.defaultdict(list)
    for line in text.splitlines():
        if line.startswith('MK2_'):
            records[line.split()[0]].append(dict(re.findall(r'(\w+)=([^\s]+)', line)))
    return records


def physical_ledger(c, first, last, records):
    health, fields = records['MK2_SECRET_HEALTH'], records['MK2_STAGE_SECRET_FIELD']
    # Reuse every original slot/opcode/sentinel/reset/fill/HP chronology check.
    source = inspect.getsource(prior.physical_inventory)
    changes = [
        ("0<=after<before<=161,'Actual native collision damage and saturation'",
         "0<=after<=before<=161,'Native collision never heals; a saturated store may retain HP'"),
        ("elif pc in(0xff825930,0xff825960):", "elif pc==0xff814e90:need(int(r['frame'])<_cold_match and after==0,'Original cold global RAM clear before any match')\n  elif pc in(0xff825930,0xff825960):"),
    ]
    for a, b in changes:
        need(source.count(a) == 1, 'Exact original ledger adaptation '+a)
        source = source.replace(a, b, 1)
    tags = {'MK2_KO_FIELD': fields, 'MK2_INTERRUPT_HEALTH': health}
    boundaries = {'MK2_MAUDIO_BEGIN': {'frame': str(first)}, 'MK2_JR_RESULT': {'frame': str(last)}}
    scope = dict(vars(prior), _cold_match=first, rows=lambda text, tag: tags[tag],
                 prior=SimpleNamespace(one=lambda text, tag: boundaries[tag]))
    exec(compile(source, __file__+'::whole_original_HP_ledger', 'exec'), scope)
    ledger, by = scope['physical_inventory'](c)
    return ledger, by


def rotation_gate(c):
    records = inventory(c['text'])
    matches, windows = records['MK2_STAGE_MATCH'], records['MK2_STAGE_WINDOW']
    own, side = {'kano': 17, 'sonya': 18}[c['fighter']], c['side']
    other = 18 if own == 17 else 17
    need(len(matches) >= 8 and len(matches)-1 <= len(windows) <= len(matches), 'Native earned route includes Portal')
    need([int(r['arena']) for r in matches] == [i%9 for i in range(len(matches))] and
         all(r['ids'] == f'{own},{other}' and r['writes'] == '0' and r['assistance'] == 'none' for r in matches),
         'Native arena rotation and true human IDs, no proxy or arena assistance')
    first = int(matches[0]['frame'])
    last = max(int(r['frame']) for r in records['MK2_STAGE_SECRET_FIELD'])
    need(len(records['MK2_STAGE_RESULT']) == 1 and int(records['MK2_STAGE_RESULT'][0]['frame']) == last,
         'Entire original native callback interval through declared stop, not a shortened ledger')
    ledger, by = physical_ledger(c, first, last, records)
    health = records['MK2_SECRET_HEALTH']
    for index, match in enumerate(matches):
        begin = int(match['frame'])
        need(by[begin, 1]['hp'] == by[begin, 2]['hp'] == '161', 'Full native match admission')
        need(by[begin, 1]['arena'] == by[begin, 2]['arena'] == match['arena'], 'Both actual admitted arena words')
        if index:
            origin = int(windows[index-1]['frame'])+720
            inputs = records['MK2_STAGE_INPUT']
            for button, delay in (('Coin', 0), ('Start', 20)):
                want = [f for f in range(origin+delay, origin+delay+4) if by[f, 1]['mode'] != '4']
                need(want, 'Normal paid challenger must physically receive '+button)
                need([int(r['frame']) for r in inputs if r['slot'] == str(3-side) and r['button'] == button and
                      origin+delay <= int(r['frame']) < origin+delay+4] == want, 'Whole normal paid challenger input '+button)
        end = int(windows[index]['frame']) if index < len(windows) else last
        for f in range(begin, end+1):
            for n, identity in ((side, own), (3-side, other)):
                r = by[f, n]
                if r['mode'] in ('2', '7'):
                    need(r['id'] == r['roster'] == str(identity) and r['state'] == '1' and
                         r['actor'] == r['owner'] != '00000000', 'Every live native two-human field has exact true owners')
        if index < len(windows):
            window = windows[index]
            need(window['arena'] == str(index%9) and window['kos'] == '2' and window['damage'] == '322',
                 'Actual native earned two-win window')
            hits = [r for r in health if begin <= int(r['frame']) <= end and r['slot'] == str(3-side) and r['pc'] == 'FF836700']
            need(sum(int(r['before'])-int(r['after']) for r in hits) == 322 and
                 sum(int(r['before']) > 0 and r['after'] == '0' for r in hits) == 2, 'Whole actual native winning damage')
    return dict(passed=True, scope='earned two-player arena rotation only; NOT secret-fight acceptance',
                fighter=c['fighter'], physicalSlot=side, nativeMatches=len(matches), earnedTwoWinWindows=len(windows),
                nativePortalMatches=sum(r['arena'] == '7' for r in matches), wholePhysicalAndHealthLedger=ledger,
                actualSecretFightAccepted=False, actualNativeTerminal=c['terminal'], fullPortAcceptance=False)


def gate(c):
    records = inventory(c['text'])
    actual = lambda tag: records[tag]
    need(not actual('MK2_SECRET_DEADLINE'), 'No deadline substitutes for a secret fight')
    matches, windows = actual('MK2_STAGE_MATCH'), actual('MK2_STAGE_WINDOW')
    accepted, fight, result = (actual('MK2_STAGE_SECRET_'+tag) for tag in ('ACCEPT', 'FIGHT', 'RESULT'))
    need(len(matches) >= 8 and len(matches)%9 == 8 and len(windows) == len(matches)-1 and
         len(accepted) == len(fight) == len(result) == 1,
         'Earned native arena rotation reaches Portal and one complete secret fight')
    own, side = {'kano': 17, 'sonya': 18}[c['fighter']], c['side']
    other = 18 if own == 17 else 17
    need([int(r['arena']) for r in matches] == [i%9 for i in range(len(matches))] and
         all(r['ids'] == f'{own},{other}' and r['writes'] == '0' and r['assistance'] == 'none' for r in matches),
         'Native arena rotation and true human IDs, no proxy or arena assistance')
    first, last = int(matches[0]['frame']), int(result[0]['frame'])
    health = actual('MK2_SECRET_HEALTH')
    ledger, by = physical_ledger(c, first, last, records)
    stock = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo, hi in ((0xffa19fd0, 0xffa1a610), (0xffa1bda0, 0xffa1c5f0), (0xffa0ba10, 0xffa0baf0),
                   (0xff836650, 0xff836750), (0xff8258b0, 0xff8259a0), (0xff9decb0, 0xff9defa0)):
        a, b = (lo-0xff800000)//8, (hi-0xff800000)//8
        need(c['guest'][a:b] == stock[a:b], 'Entire original native secret/HP instruction interval')
    for index, window in enumerate(windows):
        begin, end = int(matches[index]['frame']), int(window['frame'])
        need(begin < end < int(matches[index+1]['frame']) and window['arena'] == str(index%9) and
             window['kos'] == '2' and window['damage'] == '322', 'Each earned native two-win window')
        hits = [r for r in health if begin <= int(r['frame']) <= end and r['slot'] == str(3-side)
                and r['pc'] == 'FF836700']
        need(sum(int(r['before'])-int(r['after']) for r in hits) == 322 and
             sum(int(r['before']) > 0 and r['after'] == '0' for r in hits) == 2,
             'All winning damage and both lethal collisions independently observed')
    at, secret = int(accepted[0]['frame']), int(fight[0]['frame'])
    accept = accepted[0]
    need(int(matches[-1]['frame']) < at < secret < last and accept['arena'] == '7' and
         accept['pc'] == 'FFA1A470' and accept['secretID'] == '14' and accept['taskSide'] == str(side-1) and
         accept['states'] == '1,1' and accept['rosters'] == (f'{own},{other}' if side == 1 else f'{other},{own}') and
         0 <= (int(accept['tick'])-int(accept['toastTick'])) % 65536 <= 64 and
         not int(accept['in0'], 16) & (2 << (8*(side-1))),
         'Original native Down/Toasty/Start acceptance, genuine human side and unchanged roster')
    toasts = [r for r in actual('MK2_STAGE_TOASTY') if int(r['frame']) <= at and r['arena'] == '7']
    need(toasts and all(r['pc'] == 'FFA0BAF0' for r in toasts) and toasts[-1]['tick'] == accept['toastTick'],
         'Real native Toasty popup, never a timestamp reset mistaken for one')
    controls = actual('MK2_STAGE_INPUT')
    for button in ('Down', 'Start'):
        need(any(r['slot'] == str(side) and r['button'] == button and at-1 <= int(r['frame']) <= at
                 for r in controls), 'Normal physical secret input '+button)
    entries = actual('MK2_STAGE_SECRET_ENTRY')
    need(any(r['entry'] == 'FFA1A310' and int(r['frame']) == at for r in entries) and
         any(r['entry'] == 'FFA1BFC0' and at < int(r['frame']) <= secret for r in entries),
         'Actual native trigger decision and secret opponent construction')
    for f in range(secret, last+1):
        for n, identity, state in ((side, own, 1), (3-side, 14, 0)):
            r, start = by[f, n], by[secret, n]
            need(r['mode'] == '2' and r['id'] == r['roster'] == str(identity) and r['state'] == str(state) and
                 r['actor'] == r['owner'] == start['actor'] != '00000000' and r['main'] == start['main'] and
                 0 < int(r['hp']) <= 161, 'Every actual secret fight human/CPU actor/Main/health field')
    need(by[secret, side]['hp'] == by[secret, 3-side]['hp'] == '161', 'Normal full-health secret match admission')
    events = {tag.lower(): int(result[0][tag.lower()]) for tag in ('WALK', 'JUMP', 'PUNCH', 'RECOVER')}
    need(secret < events['walk'] < events['jump'] < events['punch'] < events['recover'] and
         last == events['recover']+180, 'Actual ordered responses and complete survival interval')
    for tag in ('WALK', 'JUMP', 'PUNCH', 'RECOVER'):
        event = actual('MK2_STAGE_SECRET_'+tag)
        need(len(event) == 1 and int(event[0]['frame']) == events[tag.lower()], 'One actual response '+tag)
        r = by[events[tag.lower()], side]
        grounded = r['y'] == r['floor'] and r['vx'] == r['vy'] == r['gravity'] == '00000000' and not int(r['flags'], 16)&0x1c
        if tag == 'RECOVER':
            need(grounded and r['action'] in ('0', '771'), 'Native grounded recovery')
            continue
        begin, end = int(event[0]['start']), int(event[0]['frame'])
        need(secret <= begin < end, 'Physical input precedes response '+tag)
        pulses = [v for v in controls if v['slot'] == str(side) and begin <= int(v['frame']) < end]
        if tag == 'WALK':
            need(grounded and r['action'] == '0' and int(r['x']) == int(event[0]['toX']) and
                 abs(int(r['x'])-int(event[0]['fromX'])) >= 4 and
                 any(v['button'] in ('Left', 'Right') for v in pulses), 'Real grounded walk response')
        elif tag == 'JUMP':
            need(int(r['y']) < int(r['floor']) and r['action'] != '1283' and any(v['button'] == 'Up' for v in pulses) and
                 not any(v['slot'] == str(side) and begin <= int(v['frame']) < end and
                         int(v['before']) > int(v['after']) for v in health), 'Physical jump, not CPU-hit airborne reaction')
        else:
            need(r['action'] == '257' and any(v['button'] == 'High_Punch' for v in pulses), 'Actual native ordinary punch')
    blocks = [int(r['frame']) for r in controls if r['slot'] == str(side) and r['button'] == 'Block'
              and int(r['frame']) > events['recover']]
    need(blocks == list(range(events['recover']+1, last)), 'Every ordinary Block survival input')
    return dict(passed=True, fighter=c['fighter'], physicalSlot=side, earnedMatches=len(windows),
                actualPortalMatch=matches[-1], actualNativeSecretAcceptance=accept,
                actualSecretFight=fight[0], events=events, terminal=last,
                wholePhysicalAndHealthLedger=ledger, secretFightFieldsPerSlot=last-secret+1,
                completeSecretAudioAccepted=False, fullPortAcceptance=False)


def qualify(c):
    need(c['report']['passed'] and c['terminal']['nativeExit'] == 0, 'Actual transport terminal passed')
    need(not capture_host.native.census(), 'No live game; qualify the same terminal capture')
    need(all(capture_host.sha(p) == h for p, h in c['pins'].items()), 'Executed input pins remain intact')
    result = gate(c)
    path = c['folder']/'secret_contract.json'
    need(not path.exists(), 'Preserve any already executed contract result')
    result.update(inputHashes=dict(c['pins']), checkerSHA256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest().upper())
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('passed', 'fighter', 'physicalSlot', 'earnedMatches', 'secretFightFieldsPerSlot')}))
    return result


def rotation_faults(c):
    original = c['text'].splitlines()
    records = inventory(c['text'])
    first = int(records['MK2_STAGE_MATCH'][0]['frame'])
    last = int(records['MK2_STAGE_RESULT'][0]['frame'])
    own = str(c['side'])
    faults = []
    selectors = [
        ('first combat owner ID', 'MK2_STAGE_SECRET_FIELD', lambda r: r['slot'] == own and int(r['frame']) == first, 'id', '0'),
        ('first combat owner pointer', 'MK2_STAGE_SECRET_FIELD', lambda r: r['slot'] == own and int(r['frame']) == first, 'owner', '00000000'),
        ('actual collision opcode', 'MK2_SECRET_HEALTH', lambda r: r['pc'] == 'FF836700' and int(r['frame']) > first, 'op0', '0000'),
        ('actual collision omitted', 'MK2_SECRET_HEALTH', lambda r: r['pc'] == 'FF836700' and int(r['before']) > int(r['after']) and int(r['frame']) > first, None, None),
        ('earned second KO omitted', 'MK2_STAGE_WINDOW', lambda r: True, 'kos', '1'),
        ('normal paid Start omitted', 'MK2_STAGE_INPUT', lambda r: r['button'] == 'Start' and int(r['frame']) > first, None, None),
        ('last complete callback omitted', 'MK2_STAGE_SECRET_FIELD', lambda r: int(r['frame']) == last, None, None),
    ]
    for label, tag, select, key, value in selectors:
        candidate = list(original)
        index = next(i for i, line in enumerate(candidate) if line.startswith(tag+' ') and select(dict(re.findall(r'(\w+)=([^\s]+)', line))))
        if key:
            candidate[index], count = re.subn(r'\b'+key+r'=[^\s]+', key+'='+value, candidate[index])
            need(count == 1 and candidate[index] != original[index], 'Actual non-vacuous fault '+label)
        else:
            candidate.pop(index)
        altered = dict(c, text='\n'.join(candidate)+'\n')
        try:
            rotation_gate(altered)
        except ValueError as error:
            faults.append(dict(fault=label, rejected=str(error)))
            print(json.dumps(faults[-1]), flush=True)
        else:
            raise ValueError('Actual record fault accepted: '+label)
    return faults
