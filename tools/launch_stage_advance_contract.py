"""Whole native HP ledger, earned ladder advance and actual next-fight controls."""
import inspect
import struct
from pathlib import Path
import qualify_launch_challenger_transition as physical
import single_continue_controls_v6580 as controls
import kano_ball_launch_context_v6642 as current

ROOT, need, sha, rows = current.ROOT, current.need, current.sha, physical.rows


def inventory(text):
    result = {}
    for line in text.splitlines():
        if not line.startswith('MK2_'): continue
        tag = line.split()[0]
        result.setdefault(tag, []).append(dict(physical.re.findall(r'(\w+)=([^\s]+)', line)))
    return result


def gate(text, guest):
    records = inventory(text)
    actual = lambda tag: records.get(tag, [])
    begin, final = actual('MK2_MAUDIO_BEGIN'), actual('MK2_NAT_CAMPAIGN_STAGE_RESULT')
    need(len(begin) == len(final) == 1 and not actual('MK2_STAGE_DEADLINE'), 'One natural stage/control terminal, never a deadline')
    first, last = int(begin[0]['frame']), int(final[0]['frame'])
    need(last > first and final[0]['fighter'] == 'kano' and final[0]['human_slot'] == '2', 'Actual declared human slot and fighter')
    # Retain every original collision/reset/sentinel/animated-fill check.
    source = inspect.getsource(physical.physical_inventory)
    for before, after in [("'MK2_JR_RESULT'", "'MK2_NAT_CAMPAIGN_STAGE_RESULT'"),
                          ("0<=after<before<=161,'Actual native collision damage and saturation'",
                           "0<=after<=before<=161,'Native collision stores may retain HP, never heal'")]:
        need(source.count(before) == 1, 'Only native terminal tag/no-damage-store distinction changes')
        source = source.replace(before, after, 1)
    scope = dict(vars(physical), rows=lambda text, tag: actual(tag))
    exec(compile(source, __file__+'::whole_original_HP_and_physical_ledger', 'exec'), scope)
    ledger, by = scope['physical_inventory'](dict(text=text, guest=guest))
    stock = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo, hi in ((0xff836650, 0xff836750), (0xff8258b0, 0xff8259a0), (0xff9decb0, 0xff9defa0)):
        a, b = (lo-0xff800000)//8, (hi-0xff800000)//8
        need(guest[a:b] == stock[a:b], 'Whole independent native HP instruction interval')
    # KO_FIELD.stage is the arena word at 01061AC0, NOT the ladder index at 01061B30.
    wins = actual('MK2_NAT_CAMPAIGN_WIN')
    need(len(wins) == 4 and [r['slot'] for r in wins] == ['1', '1', '2', '2'], 'Actual CPU-earned loss then two own wins, not supplied victory')
    health = actual('MK2_INTERRUPT_HEALTH')
    for win in wins:
        side = int(win['slot']); identity = 18 if side == 1 else 17
        hp = list(map(int, win['health'].split(',')))
        need(win['pc'] == 'FF8296B0' and win['stage'] == '0' and int(win['id']) == identity and
             int(win['entry'], 16) == 0xfffef800 + identity*32 and hp[side-1] > 0 and hp[2-side] == 0,
             'Every original true-ID winner-table read and winning health')
        lethal = [r for r in health if r['slot'] == str(3-side) and r['pc'] == 'FF836700' and
                  int(r['before']) > 0 and r['after'] == '0' and int(r['frame']) < int(win['frame'])]
        need(lethal and int(win['frame'])-int(lethal[-1]['frame']) < 100, 'Each winning round follows real native lethal collision')
    losses = actual('MK2_NAT_CAMPAIGN_LOSS')
    selections = actual('MK2_NAT_CAMPAIGN_SELECT')
    need(len(losses) == 1 and len(selections) == 2 and selections[1]['continue'] == losses[0]['frame'], 'Actual paid continue and genuine native reselect')
    controls_rows = actual('MK2_NAT_CAMPAIGN_INPUT')
    origin = int(losses[0]['frame'])
    for button, age, count in [('Coin', 20, 5), ('Coin', 270, 5), ('Start', 310, 5)]:
        want = list(range(origin+age, origin+age+count))
        need([int(r['frame']) for r in controls_rows if r['button'] == button and origin+age <= int(r['frame']) < origin+age+count] == want,
             'Whole normal physical continue payment '+button)
    advance = actual('MK2_NAT_CAMPAIGN_ADVANCE')
    need(len(advance) == 1 and advance[0]['frame'] == final[0]['advance'] and advance[0]['stage'] == '1', 'One earned next ladder stage')
    at = int(advance[0]['frame'])
    need(int(wins[-1]['frame']) < at < last and by[at, 1]['hp'] == by[at, 2]['hp'] == '161', 'Real match retirement/refill then full-health next fight')
    declared = actual('MK2_NAT_CAMPAIGN_ROM')
    need(len(declared) == 6, 'All original initialized native ladder schedules')
    schedules = {}
    for row in declared:
        address = int(row['list'], 16)
        wanted = [struct.unpack_from('<H', guest, (address-0xff800000)//8+i*2)[0] for i in range(17)]
        need(list(map(int, row['ids'].split(','))) == wanted, 'Entire actual schedule equals independent whole guest')
        schedules[row['list']] = wanted
    need(advance[0]['schedule'] in schedules and schedules[advance[0]['schedule']][1] == int(advance[0]['cpu']) == 7,
         'Next opponent from actual untouched native schedule, not a forced CPU')
    oldfight = actual('MK2_NAT_CAMPAIGN_FIGHT')[-2]
    need(oldfight['stage'] == '0' and oldfight['cpu'] == '18:18', 'Continued original native CPU Sonya fight')
    oldactors = set(oldfight['actors'].split(','))
    for frame in range(at, last+1):
        for slot, identity, state in [(1, 7, 0), (2, 17, 1)]:
            row = by[frame, slot]
            need(row['mode'] == '2' and row['state'] == str(state) and row['id'] == row['roster'] == str(identity) and
                 row['actor'] == row['owner'] != '00000000' and row['actor'] not in oldactors and
                 row['main'] == by[at, slot]['main'] and row['actor'] == by[at, slot]['actor'] and 0 < int(row['hp']) <= 161,
                 'Every stable real next-fight actor/Main/human/CPU identity and native health')
    # This logger runs in register_frame, not the older delayed frame-done logger.
    source = inspect.getsource(controls.actual_controls)
    before = "events[tag.lower()]-1"
    need(source.count(before) == 1, 'Only independently observed same-callback logger alignment changes')
    source = source.replace(before, "events[tag.lower()]", 1)
    def control_records(text, tag):
        mapped = {'RESULT': 'MK2_NAT_CAMPAIGN_STAGE_RESULT', 'FIELD': 'MK2_KO_FIELD', 'HEALTH': 'MK2_INTERRUPT_HEALTH'}
        values = actual(mapped.get(tag, 'MK2_NAT_CAMPAIGN_'+tag))
        if tag == 'RESULT': return [dict(r, target=r['fighter']) for r in values]
        if tag == 'INPUT': return [dict(r, slot=r['human_slot']) for r in values]
        return values
    scope = dict(vars(controls), rows=control_records)
    exec(compile(source, __file__+'::whole_actual_controls_same_register_frame_alignment', 'exec'), scope)
    events = dict(reReady=at)
    scope['actual_controls'](text, events, actual('MK2_KO_FIELD'), 2, last)
    return dict(passed=True, continuousPhysicalAndHealth=ledger, events=events,
                nativeWinnerReads=len(wins), collisionEarnedLosses=1, nativePaidReselections=1,
                ownWinsAfterPaidContinue=2, nextLadderIndex=1, nextNativeOpponent=7,
                nextFightFieldsPerSlot=last-at+1, nextArenaId=int(by[at, 2]['stage']),
                actualWalkJumpPunchRecoveryAndSurvivalAccepted=True, terminal=last), by
