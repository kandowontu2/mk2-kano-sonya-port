"""Independent native P2 tower proof, with health assistance explicitly scoped."""
import argparse
import json
import re
import struct
from pathlib import Path

from verify_p2_campaign import expected_orders, IDENTITIES, ROM


def rows(log, label, pattern, names, hexadecimal=()):
    return [dict(zip(names, (int(v, 16 if name in hexadecimal else 10)
                            for name, v in zip(names, m.groups()))),event_offset=m.start())
            for m in re.finditer(label + ' ' + pattern, log)]


def verify(log, fighter):
    errors = []
    identity = IDENTITIES[fighter]
    orders = expected_orders()
    original=ROM.read_bytes()
    for address,word in ((0xff86e650,0xb128),(0xff86e660,0x01f0),(0xffa166e0,0xb008),(0xffa166f0,0x01f0)):
        if struct.unpack_from('<H',original,(address-0xff800000)//8)[0]!=word:
            errors.append('Original native Shang ID-store instruction changed')
    morph_writers=(0xff86e670,0xffa16700)
    if 'MK2_NATIVE_SHANG_ROM morph_store=FF86E650:B128,01F0 restore_store=FFA166E0:B008,01F0' not in log:
        errors.append('Actual native morph-store instruction guard not captured')
    boots = re.findall(r'MK2_P2_TOWER_BOOT fighter=(\w+) assistance=(\w+) identity_writes=(\d+) position_writes=(\d+) stage_writes=(\d+) schedule_writes=(\d+)', log)
    assistance = boots[0][1] if boots else None
    if len(boots) != 1 or boots[0][0] != fighter or boots[0][2:] != ('0',)*4 or assistance not in ('none', 'health_only'):
        errors.append('Missing, duplicate or invalid tower boot scope')
    schedules = {}
    for table, order, pointer, ids in re.findall(r'MK2_P2_TOWER_ROM table=([0-9A-F]+) order=(\d+) list=([0-9A-F]+) ids=([0-9,]+)', log):
        order = int(order)
        if order not in range(6) or order in schedules:
            errors.append('Duplicate/invalid ROM schedule'); continue
        schedules[order] = tuple(map(int, ids.split(',')))
        if int(table, 16) != 0xfffa2c00 or int(pointer, 16) != 0xfffa3000 + order*0x180 or schedules[order] != orders[order]:
            errors.append('ROM schedule does not preserve stock order and both actual new IDs')
    if set(schedules) != set(range(6)): errors.append('Six original-derived schedules not captured')
    states = rows(log, 'MK2_P2_TOWER_STATE',
        r'frame=(\d+) mode=(\d+) states=(\d+),(\d+) stage=(\d+) order=(-?\d+) schedule=([0-9A-F]+) expected=(\d+) roster=(\d+),(\d+) actors=([0-9A-F]+):(\d+),([0-9A-F]+):(\d+) health=(\d+),(\d+) winner=(\d+) hud_read=(-?\d+)',
        ('frame','mode','s1','s2','stage','order','schedule','expected','r1','r2','a1','id1','a2','id2','h1','h2','winner','hud'), ('schedule','a1','a2'))
    live = rows(log, 'MK2_P2_TOWER_LIVE',
        r'frame=(\d+) stage=(\d+) order=(\d+) schedule=([0-9A-F]+) cpu=(\d+):(\d+) human=(\d+):(\d+) actors=([0-9A-F]+),([0-9A-F]+) health=(\d+),(\d+) flags=([0-9A-F]+),([0-9A-F]+)',
        ('frame','stage','order','schedule','r1','id1','r2','id2','a1','a2','h1','h2','flags1','flags2'), ('schedule','a1','a2','flags1','flags2'))
    writes = rows(log, 'MK2_NATIVE_SHANG_ID',
        r'frame=(\d+) actor=([0-9A-F]+) old=(\d+) new=(\d+) pc=([0-9A-F]+) a9=([0-9A-F]+) a0=([0-9A-F]+) a8=([0-9A-F]+) process=([0-9A-F]+) mask=([0-9A-F]+)',
        ('frame','actor','old','new','pc','a9','a0','a8','process','mask'), ('actor','pc','a9','a0','a8','process','mask'))
    for write in writes:
        morph=write['pc']==0xff86e670 and write['new'] in range(12) and write['new']==write['a9']&0xffff
        restore=write['pc']==0xffa16700 and write['new']==6 and write['new']==write['a0']&0xffff
        if not (morph or restore) or write['a8']!=write['actor'] or write['mask']!=0xffff or not 0x01000000<=write['process']<0x01100000:
            errors.append('Invalid native morph/restore store provenance')
    def native_cpu(row):
        order, stage = row['order'], row['stage']
        if order not in range(6) or stage not in range(17): return False
        expected = orders[order][stage]
        if row['schedule'] != 0xfffa3000+order*0x180 or row['r1'] != expected: return False
        if row['id1'] == expected: return True
        if stage != 14 or expected != 6 or row['id1'] not in range(12): return False
        # Never accept an arbitrary stock ID merely because Shang is scheduled.
        # Native morph/restore and frame callbacks can share a frame number.
        # A restore printed AFTER this sample must not retroactively replace
        # the ID which was actually live when the sample was captured.
        previous = [w for w in writes if w['frame'] <= row['frame'] and w['event_offset']<row['event_offset'] and w['actor'] == row['a1']]
        return bool(previous and previous[-1]['pc'] in morph_writers and previous[-1]['new'] == row['id1'] and
                    previous[-1]['a8'] == row['a1'] and previous[-1]['mask'] == 0xffff)
    for row in live:
        if not native_cpu(row) or row['r2'] != identity or row['id2'] != identity or min(row['h1'],row['h2']) <= 0 or not all(0x01000000 <= row[a] < 0x01100000 for a in ('a1','a2')):
            errors.append(f"Live ownership/provenance failed at {row['frame']}")
    if len(live) < 500: errors.append('Insufficient independently captured live samples')
    wins = rows(log, 'MK2_P2_TOWER_WIN',
        r'frame=(\d+) stage=(\d+) order=(\d+) schedule=([0-9A-F]+) states=(\d+),1 cpu=(\d+):(\d+) human=(\d+):(\d+) actors=([0-9A-F]+),([0-9A-F]+) health=(\d+),(\d+) wins=(\d+) stage_wins=(\d+)',
        ('frame','stage','order','schedule','s1','r1','id1','r2','id2','a1','a2','h1','h2','wins','stage_wins'), ('schedule','a1','a2'))
    initial = [w for w in wins if w['s1'] == 1]
    if len(initial) != 2 or any(w['h1'] != 0 or w['r2'] != identity or w['id2'] != identity for w in initial):
        errors.append('Normal initial two-human P2 victories not established')
    campaign = [w for w in wins if w['s1'] == 0]
    counts = {}
    for number, win in enumerate(wins, 1):
        if win['wins'] != number: errors.append('Missing/duplicated native winner-table event')
    for win in campaign:
        if not native_cpu(win) or win['r2'] != identity or win['id2'] != identity or win['h2'] <= win['h1']:
            errors.append(f"Owned native P2 win invalid at {win['frame']}")
        # A timer victory retains positive CPU health. Require the actual
        # matching next-field native winner scene, rather than inventing a KO.
        scene = [s for s in states if s['frame'] == win['frame']+1]
        if not scene or scene[0]['mode'] not in (5,11) or scene[0]['winner'] != 2 or scene[0]['h1'] != win['h1'] or scene[0]['h2'] != win['h2']:
            errors.append(f"Native winner scene missing at {win['frame']}")
        counts[win['stage']] = counts.get(win['stage'],0)+1
        if win['stage_wins'] != counts[win['stage']]: errors.append('Stage-win accounting differs from actual native events')
    mandatory = list(range(13))+[14,15,16]
    for stage in mandatory:
        if counts.get(stage,0) < (1 if stage == 16 else 2): errors.append(f'Missing native wins at mandatory stage {stage}')
    stages = rows(log, 'MK2_P2_TOWER_STAGE', r'frame=(\d+) stage=(\d+) order=(\d+) cpu=(\d+) human=(\d+) previous=(?:nil|\d+)',
                  ('frame','stage','order','r1','r2'))
    if [s['stage'] for s in stages] not in (mandatory, list(range(17))): errors.append('Incomplete/duplicated/nonsequential native tower')
    for before, after in zip(stages, stages[1:]):
        earned = sum(w['stage'] == before['stage'] and w['frame'] < after['frame'] for w in campaign)
        if earned < 2: errors.append('Native advance precedes two owned wins')
    if len({s['order'] for s in stages}) != 1: errors.append('Native schedule changed during campaign')
    health = rows(log, 'MK2_P2_TOWER_HEALTH', r'frame=(\d+) side=(\d+) stage=(\d+) old=(\d+) new=(\d+)', ('frame','side','stage','old','new'))
    for row in health:
        if assistance != 'health_only' or row['stage'] not in range(17) or not ((row['side']==1 and row['old']==161 and row['new']==1) or (row['side']==2 and 0<row['old']<161 and row['new']==161)):
            errors.append('Undeclared/invalid health mutation')
    starts = re.findall(r'MK2_P2_TOWER_ENDING_START frame=(\d+) fighter=(\w+) roster=(\d+) health=(\d+),(\d+) winner=(\d+)',log)
    endings = re.findall(r'MK2_P2_TOWER_COMPLETED frame=(\d+) ending_age=(\d+) mode=(\d+) roster=(\d+),(\d+) pictures=(\d+),(\d+) texts=(\d+),(\d+)',log)
    if len(starts)!=1 or len(endings)!=1: errors.append('Actual ending start/completion not captured')
    else:
        start, ending = starts[0], list(map(int,endings[0]))
        if start[1]!=fighter or int(start[2])!=identity or int(start[3])!=0 or int(start[5])!=2 or not any(w['stage']==16 and w['frame']<int(start[0]) for w in campaign):
            errors.append('Ending does not follow owned P2 Shao Kahn victory')
        if not any(s['frame']==int(start[0]) and s['mode']==11 and s['winner']==2 and s['h1']==0 and s['h2']>0 and s['r2']==identity and s['a1']==s['a2']==0 for s in states):
            errors.append('Ending start lacks actual retained native boss-win teardown')
        if ending[0]-int(start[0])!=ending[1] or ending[1]<=1200 or ending[2]!=11 or ending[4]==identity or min(ending[5:])<=0:
            errors.append('Ending has not completed both own pages and returned to stock attract')
        if not any(s['frame']==ending[0] and s['mode']==11 and s['r2']==ending[4] for s in states): errors.append('Completion marker lacks actual matching attract state')
    page_counts = {'PICTURE':[0,0], 'TEXT':[0,0]}
    for kind in page_counts:
        for frame,page,roster,entry,value,pc in re.findall('MK2_P2_TOWER_'+kind+r' frame=(\d+) page=(\d+) roster=(\d+) entry=([0-9A-F]+) value=([0-9A-F]+) pc=([0-9A-F]+)',log):
            page=int(page);entry=int(entry,16)
            if page not in (1,2) or int(roster)!=identity:
                errors.append('Wrong ending-page ownership');continue
            if kind=='PICTURE': permitted=[0xff800000+0xf4900*8+(50+(identity-17)*2+page-1)*32]
            else: permitted=[0xff800000+(0xf4a00 if page==1 else 0xf4b00)*8+(identity*3+i)*32 for i in range(3)]
            if entry not in permitted: errors.append('Ending lookup uses another fighter or page')
            page_counts[kind][page-1]+=1
    if any(min(counts)==0 for counts in page_counts.values()): errors.append('Both own native ending pictures/texts not observed')
    result=re.search(r'MK2_P2_TOWER_RESULT pass=(\w+) fighter=(\w+) checks=(\d+) errors=(\d+) wins=(\d+) initial_action=(\w+) complete=(\w+) mandatory=(\w+) health_writes=(\d+) regen_writes=(\d+) assistance=(\w+)',log)
    groups=result.groups() if result else ()
    if not result or groups[:2]!=('true',fighter) or int(result[3])<500 or result[4]!='0' or groups[5:8]!=('true','true','true') or result[11]!=assistance:
        errors.append('Final tower result is missing/incomplete/dirty')
    elif (int(result[9]),int(result[10])) != (sum(h['side']==1 for h in health),sum(h['side']==2 for h in health)):
        errors.append('Health-assistance accounting mismatch')
    for marker in ('MK2KS_EXIT_RESULT pass=true ','MK2KS_DISPLAY_RESULT pass=true ','MK2KS_HUD_SHADOW_RESULT pass=true ', 'MK2KS_STABILITY stalled_frames=0 trap_frames=0','MK2_RANGE_RESULT pass=true '):
        if marker not in log: errors.append('Missing acceptance evidence: '+marker)
    if re.search(r'MK2_FINISH_POSITION_ASSIST|\[LUA ERROR\]|fatal error|access violation|MK2_P2_TOWER_ERROR',log,re.I): errors.append('Runtime, ownership, transition or forbidden mutation error')
    return {'passed':not errors,'errors':errors,'fighter':fighter,'assistance':assistance,
            'live_samples':len(live),'native_campaign_wins':len(campaign),'stage_wins':counts,
            'health_writes':len(health),'own_ending_pages':page_counts,'morph_writers':[f'{pc:08X}' for pc in morph_writers],
            'scope':'full_p2_native_tower_structure_not_unassisted_clear','unassisted_clear_proven':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('log',type=Path)
    parser.add_argument('--fighter',required=True,choices=IDENTITIES)
    args=parser.parse_args()
    result=verify(args.log.read_text(encoding='utf-8-sig'),args.fighter)
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['passed'] else 1)
