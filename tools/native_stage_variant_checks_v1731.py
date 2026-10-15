"""Current earned human stage commands, both slots/arenas and native rejection.

State/input/action/cleanup acceptance only. Not complete scene raster/art/audio
certification, full tower clears, or whole-port/release acceptance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import wave
from PIL import Image
import verify_native_candidate_v798 as candidate

need = candidate.need

def rows(log, tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in log.splitlines()
            if line.startswith('MK2_STAGE_' + tag + ' ')]

def number(r, key):
    return int(r[key])

def check_log(log, fighter, side, arena, case='positive', certified_drop_log=None):
    own = 17 if fighter == 'kano' else 18
    victim = 18 if own == 17 else 17
    boots, results = rows(log, 'BOOT'), rows(log, 'RESULT')
    need(len(boots) == len(results) == 1, 'Cold boot and terminal result required')
    boot, result = boots[0], results[0]
    need(number(boot, 'frame') == 1 and number(boot, 'own_id') == own
         and number(boot, 'victim_id') == victim, 'True native IDs from cold boot')
    if 'target_arena' in boot:
        need(number(boot, 'target_arena') == arena and boot['command_case'] == case,
             'Requested arena/case actually executed')
    for line in log.splitlines():
        if line.startswith('MK2_STAGE_'):
            r = dict(re.findall(r'(\w+)=([^\s]+)', line))
            need(r['writes'] == '0' and r['assistance'] == 'none' and r['winner'] == fighter
                 and number(r, 'side') == side, 'Wrong slot/assistance/identity')
    need('Lua error' not in log and 'Error in' not in log, 'Runtime Lua error')
    matches, windows = rows(log, 'MATCH'), rows(log, 'WINDOW')
    need(len(matches) == len(windows) == arena + 1 == number(result, 'matches'),
         'Every normal arena earned through rematches')
    need([number(r, 'arena') for r in matches] == list(range(arena + 1)), 'Forced/skipped arena')
    need([number(r, 'match') for r in matches] == list(range(1, arena + 2))
         and all(r['ids'] == f'{own},{victim}' for r in matches), 'Proxy/rematch identity')
    need(all(number(r, 'actual') == number(r, 'target') == (own if number(r, 'slot') == side else victim)
             for r in rows(log, 'SELECT_ID')), 'Wrong selected native ID')
    inputs = rows(log, 'INPUT')
    for index, window in enumerate(windows, 1):
        need(number(window, 'match') == index and number(window, 'arena') == index - 1
             and number(window, 'kos') == 2 and number(window, 'damage') == 322, 'Unearned finish window')
        hits = [r for r in rows(log, 'DAMAGE') if number(r, 'match') == index]
        need(hits and sum(number(r, 'before') - number(r, 'after') for r in hits) == 322
             and sum(number(r, 'after') == 0 for r in hits) == 2
             and all(r['pc'] == 'FF836700' and 0 <= number(r, 'after') < number(r, 'before') <= 161 for r in hits),
             'Native two full-health KO damage chains')
        for n, chain in enumerate((hits[:next(i for i, r in enumerate(hits) if number(r, 'after') == 0)+1],
                                   hits[next(i for i, r in enumerate(hits) if number(r, 'after') == 0)+1:])):
            need(chain[0]['before'] == '161' and chain[-1]['after'] == '0', 'Full native round health')
            need(all(a['after'] == b['before'] for a, b in zip(chain, chain[1:])), 'Assisted/discontinuous damage')
        if index < len(matches):
            later = [r for r in inputs if number(window, 'frame') + 720 <= number(r, 'frame') < number(matches[index], 'frame')
                     and number(r, 'slot') == 3 - side]
            need(any(r['button'] == 'Coin' for r in later) and any(r['button'] == 'Start' for r in later),
                 'Missing physical paid challenger')
    commands = rows(log, 'COMMAND')
    need(len(commands) == 1 and number(commands[0], 'arena') == arena, 'Exactly one requested stage input')
    command = commands[0]; begin = number(command, 'frame')
    need(number(result, 'command') == begin and number(result, 'window') == number(windows[-1], 'frame')
         and begin >= number(windows[-1], 'frame') + 65, 'Round recoil/command chronology')
    gap = number(command, 'gap')
    need(gap >= 130 if case == 'far' else 60 <= gap <= 65, 'Physical input-only stage distance')
    button = 'Low_Kick' if own == 17 else 'High_Punch'
    stage_inputs = [r for r in inputs if begin <= number(r, 'frame') < begin + 44]
    need(all(number(r, 'slot') == side for r in stage_inputs), 'Opponent automation during command')
    def keys(age):
        return {r['button'] for r in stage_inputs if number(r, 'frame') == begin + age}
    back, forward = ('Left', 'Right') if side == 1 else ('Right', 'Left')
    wanted = {10: {'Block', 'Up'}, 20: {'Block', 'Up'}, 30: {'Block', forward if case == 'wrong_command' else back}, 40: {button}} if own == 17 else {
        10: {forward}, 20: {forward}, 30: {back if case == 'wrong_command' else 'Down'}, 40: {button}}
    need(all(keys(age) == expected for age, expected in wanted.items()), 'Wrong actual facing-specific button sequence')
    entries = [r for r in rows(log, 'ENTRY') if number(r, 'frame') >= begin + 40]
    parser = 'FFFAA200' if own == 17 else 'FFFAA400'
    parser_rows = [r for r in entries if r['entry'] == parser]
    need(parser_rows and all(number(r, 'id') == own and number(r, 'arena') == arena for r in parser_rows),
         'Missing character-owned native event parser')
    event_frame = number(parser_rows[0], 'frame')
    event = [r for r in entries if number(r, 'frame') == event_frame and r['a8'] == parser_rows[0]['a8']]
    gate = [r['entry'] for r in event if r['entry'] in {
        'FF876D20','FF876E50','FF876E80','FF876F40','FF877000','FF877120','FF8771F0',
        'FF877270','FF877280','FF877300','FF877350','FF8773A0','FF877420'}]
    action_rows = [r for r in rows(log, 'ENTRY') if r['entry'] in ('FF8BDDE0','FF8BDFE0')]
    fields = rows(log, 'FIELD')
    if arena == 0 or case != 'positive':
        need(not action_rows and not fields and result['action'] == '-1' and result['action_arena'] == '-1',
             'Rejected command entered native stage action')
        expected = ['FF876D20','FF877420'] if arena == 0 else (
            ['FF876D20','FF876E50','FF877420'] if case == 'wrong_command' else
            ['FF876D20','FF876E50','FF876E80','FF876F40','FF877420'])
        need(gate == expected, 'Wrong native rejection boundary')
        if case == 'far':
            rejected = next(r for r in event if r['entry'] == 'FF877420')
            need(int(rejected['a3'], 16) > 0x48, 'Original 72-unit range gate did not reject distance')
        ends = rows(log, 'REJECT_END')
        need(len(ends) == 1 and number(ends[0], 'mode') == 3 and number(ends[0], 'arena') == arena + 1,
             'Rejected action did not cleanly return to next screen')
        return {'arena': arena, 'case': case, 'native_rejection_gate': gate, 'earned_matches': len(matches), 'passed': True}
    expected = ['FF876D20','FF876E50','FF876E80','FF876F40','FF877000','FF877120','FF8771F0',
                'FF877270','FF877280','FF877300','FF877350','FF8773A0','FF877420']
    need(gate == expected, 'Native history/range/finish/opponent/action gates not all reached')
    action_pc = 'FF8BDFE0' if arena == 1 else 'FF8BDDE0'
    need(len(action_rows) == 1 and action_rows[0]['entry'] == action_pc
         and number(action_rows[0], 'id') == own and number(action_rows[0], 'arena') == arena
         and action_rows[0]['a8'] == parser_rows[0]['a8']
         and number(result, 'action') == number(action_rows[0], 'frame') == event_frame
         and number(result, 'action_arena') == arena, 'Wrong owner/native arena action')
    need(len(fields) >= 801 and [number(r, 'age') for r in fields[:801]] == list(range(801))
         and [number(r, 'frame') for r in fields[:801]] == list(range(event_frame, event_frame + 801)),
         'Missing consecutive action/cleanup fields')
    actor, main = fields[0]['own'], fields[0]['main']
    victim_actor, victim_main = fields[0]['victim'], fields[0]['victim_main']
    need(actor == action_rows[0]['a8'] and main == action_rows[0]['a13']
         and number(fields[0], 'id') == own and number(fields[0], 'victim_id') == victim, 'Physical action ownership')
    for r in fields:
        need((r['own'] == '00000000' and r['main'] == '00000000' and r['id'] == '-1') or
             (r['own'] == actor and r['main'] == main and number(r, 'id') == own), 'Own proxy/pointer substitution')
        need((r['victim'] == '00000000' and r['victim_main'] == '00000000' and r['victim_id'] == '-1') or
             (r['victim'] == victim_actor and r['victim_main'] == victim_main and number(r, 'victim_id') == victim),
             'Victim proxy/pointer substitution')
    live_victims = [r for r in fields if r['victim'] != '00000000']
    need(min(number(r, 'victim_y') for r in live_victims) < -100, 'Native uppercut/falling trajectory absent')
    if arena == 6:
        need(any(number(r, 'mode') == 9 for r in fields) and any(number(r, 'victim_y') > 150 for r in live_victims),
             'Native Pit falling scene absent')
    else:
        need(not any(number(r, 'mode') == 9 for r in fields), 'Original Tomb must not enter Pit mode')
        held = max(number(r, 'victim_y') for r in live_victims[60:300]) < -100
        if not held:
            need((fighter,side,arena,case)==('sonya',2,1,'positive') and
                 certified_drop_log is not None and log==certified_drop_log,
                 'Non-held Tomb requires exact source-bound original random-drop chronology')
        else:
            need(max(number(r, 'victim_y') for r in live_victims[60:300]) < -100,
                 'Tomb ceiling victim not held natively')
    need(any(number(r, 'mode') == 5 for r in fields) and number(fields[800], 'mode') == 3
         and number(fields[800], 'arena') == arena + 1 and fields[800]['id'] == fields[800]['victim_id'] == '-1'
         and number(result, 'frame') >= event_frame + 1100, 'Native retirement/next screen missing or softlock')
    return {'arena': arena, 'arena_name': 'Kombat Tomb' if arena == 1 else 'Pit II', 'case': case,
            'earned_matches': len(matches), 'native_action': action_pc, 'action_frame': event_frame,
            'consecutive_fields': 801, 'passed': True}
