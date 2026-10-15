"""Native joined Kano air throw after a separately verified full ending/restart.

This verifies the real two-human join path, not naturally jumping CPU coverage.
The parent verifier owns source tower, ending pages and fresh CPU bookends.
"""
import argparse
import json
import math
import re
from pathlib import Path

ENTRIES = dict(gate=0xff8643e0, action=0xff8b6ff0, align=0xfffc0680,
               release=0xfffff980, flight=0xfffff580, callback=0xfffff800,
               bounce=0xfffc2000, damage=0xff83a7a0, own_landing=0xfffc1c00,
               victim_getup=0xff8ea320, own_recovery=0xff861410,
               victim_recovery=0xff861410)
POSES = 'FE828E80,FE828EC0,FE828F00,FE828F00,FE828F00,FE828F00,00000000,FE828F00,FE828F00,00000000'


def verify(log, target='kano', side=1, require_followup=False, require_restart=True):
    if side not in (1, 2):
        raise ValueError('Invalid player side')
    errors = []

    def rows(tag):
        return [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in log.splitlines()
                if line.startswith('MK2_AIR_JOIN_' + tag + ' ')]

    def one(tag):
        found = rows(tag)
        if len(found) != 1:
            errors.append('Missing/duplicate ' + tag)
            return {}
        return found[0]

    def n(row, key, base=10):
        try:
            return int(row[key], base)
        except (KeyError, ValueError, TypeError):
            errors.append('Missing/invalid ' + key)
            return -1

    def h(row, key):
        return n(row, key, 16)

    def require(ok, why):
        if not ok:
            errors.append(why)

    begin, rom, match, jump, command, ready, final, result = [one(t) for t in
        ('BEGIN', 'ROM', 'MATCH', 'JUMP', 'COMMAND', 'READY', 'FINAL', 'RESULT')]
    follow_plans=rows('FOLLOW_PLAN')
    followup=bool(follow_plans) or require_followup
    follow=one('FOLLOW_PLAN') if followup else {}
    vid = {'sonya':18, 'sub_zero':8}.get(begin.get('victim'), -1)
    bf, mf, jf, cf, rf, ff = [n(row, 'frame') for row in (begin, match, jump, command, ready, final)]
    require(target == 'kano' and vid in (8, 18), 'Only intended Kano air throw and supported native victim')
    require(n(begin, 'side') == side and n(begin, 'joining') == 3-side and n(begin, 'mode') == 2,
            'Actual opposite-slot challenger join required')
    require(begin.get('p'+str(side)) == '1,17' and begin.get('p'+str(3-side), '').startswith('0,'),
            'Join must begin from fresh single-human Kano/CPU match')
    restart = re.findall(r'MK2_RESTART_COMPLETE frame=(\d+) source=\w+ target=kano live=601 errors=0 restart_writes=0', log)
    if require_restart:
        require(restart == [str(bf)], 'Join must follow exact actual 601-field post-ending completion')
    else:
        cold=re.findall(r'MK2_AIR_COLD_MATCH frame=(\d+) scope=cold_diagnosis_not_post_ending',log)
        require(side==1 and len(cold)==1 and int(cold[0])+600==bf if cold else False,
                'Actual cold P1 start and 600-field wait required, not an ending claim')
    fresh = re.findall(r'MK2_RESTART_MATCH frame=(\d+) target=kano id=17 actor=[0-9A-F]+ stage=0', log)
    if require_restart:
        require(len(fresh) == 1 and int(fresh[0])+600 == bf if fresh else False,
                'Fresh target epoch missing (cold probes are not acceptance)')
    require(n(rom, 'side') == side and n(rom, 'vid') == vid and h(rom, 'block_gate') == ENTRIES['gate'] and
            h(rom, 'root') == 0xff014900 and rom.get('poses') == POSES and h(rom, 'alignment') == 0xfffd0029 and
            h(rom, 'flight_pose') == (0xff02f920 if vid == 18 else 0xff97ba70), 'Exact native ROM/own donor pose guards')
    inputs = rows('INPUT')
    require([(n(r, 'frame'), n(r, 'age'), n(r, 'slot'), r.get('button'), n(r, 'hold')) for r in inputs] ==
            [(bf+a,a,3-side,b,5) for a,b in ((10,'coin'),(30,'coin'),(60,'start'))], 'Real coin/start join input sequence')
    css, highlights = rows('CSS'), rows('HIGHLIGHT')
    require(len(css) == 2 and len(highlights) == 2, 'Both actual native select cursors/highlights required')
    coords = {17:(0,0),1:(1,0),0:(2,0),2:(3,0),9:(4,0),18:(5,0),8:(1,1),6:(2,1),4:(3,1),11:(4,1),5:(1,2),3:(2,2),10:(3,2),7:(4,2)}
    for row in css:
        slot, initial = n(row,'slot'), n(row,'initial')
        desired = 17 if slot == side else vid
        require(slot in (1,2) and n(row,'target') == desired and n(row,'state') == 3, 'Native selectable cursor ownership')
        route=[]
        if initial in coords and desired in coords:
            x,y=coords[initial];tx,ty=coords[desired]
            route=['up']*y+(['right'] if tx>x else ['left'])*abs(tx-x)+['down']*ty
        else:
            errors.append('Unknown actual native initial cursor')
        require(row.get('route','').split(',') == route if route else row.get('route') == '', 'Selection route must follow actual 14-slot topology')
        hl=[r for r in highlights if n(r,'slot') == slot]
        require(len(hl)==1 and n(hl[0],'target')==desired and n(hl[0],'roster')==desired and n(hl[0],'state')==3 and
                n(hl[0],'age')==156 and n(hl[0],'frame')==n(row,'frame')+156, 'Actual joined highlight/identity')
        require(bf+60<n(row,'frame')<n(row,'frame')+176<mf, 'Native challenger/CSS/confirm/fight chronology')
    require(bf<mf<jf<cf<rf<ff and cf==jf+20 and ff==mf+600, 'Joined match/air-input/recovery/601-field chronology')
    if not (0<=mf<=jf<=cf<=rf<=ff<=mf+1800):
        return dict(passed=False,errors=sorted(set(errors+['Unbounded/missing joined chronology'])),
                    side=side,full_goal_complete=False)
    require(n(command,'side')==side and command.get('button')=='block' and n(command,'hold')==6 and
            n(command,'jump')==jf and 20<=n(command,'gap')<=63 and n(command,'victim_hp')==161, 'Actual airborne Block command')
    controls=rows('CONTROL')
    for slot in (1,2):
        ups=[n(r,'frame') for r in controls if n(r,'slot')==slot and r.get('button')=='up' and n(r,'value')==1]
        require(ups==list(range(jf,jf+3)), 'Both real human Up pulses, not CPU/memory jump')
    blocks=[n(r,'frame') for r in controls if n(r,'slot')==side and r.get('button')=='block' and n(r,'value')==1]
    require(blocks==list(range(cf,cf+6)), 'Six actual attacker Block fields')
    require(all(n(r,'slot')==side and r.get('button') in ('left','right') and mf+180<=n(r,'frame')<jf or
                r.get('button')=='up' and n(r,'slot') in (1,2) and jf<=n(r,'frame')<jf+3 or
                r.get('button')=='block' and n(r,'slot')==side and cf<=n(r,'frame')<cf+6 for r in controls),
            'Unexpected joined controls or CPU forcing')
    fields=rows('FIELD')
    require([n(r,'frame') for r in fields]==list(range(mf,ff+1)), 'Every joined combat field must be observed')
    states={n(r,'frame'):r for r in fields}
    actor,main,vactor,vmain=[h(match,k) for k in ('actor','main','victim','vmain')]
    require(all(0x01000000<=a<0x01100000 for a in (actor,main,vactor,vmain)) and actor!=vactor and main!=vmain,
            'Distinct actual native actor/main owners')
    follow_start=n(follow,'begin') if followup else ff+1
    follow_health=rows('FOLLOW_HEALTH')
    # Native health is allowed to change only through observed original stores.
    ledger={side:[(mf-1,161)],3-side:[(mf-1,161)]}
    for row in rows('HEALTH'):
        ledger[3-side].append((n(row,'frame'),n(row,'after')))
    for row in follow_health:
        slot=n(row,'slot')
        if slot in ledger:ledger[slot].append((n(row,'frame'),n(row,'after')))
    for values in ledger.values():values.sort()
    def expected_health(slot,field):
        return next((value for when,value in reversed(ledger[slot]) if when<field),161)
    for row in fields+[match,jump,ready,final]:
        require((h(row,'actor'),h(row,'main'),h(row,'victim'),h(row,'vmain'))==(actor,main,vactor,vmain), 'Joined owners changed')
        require((n(row,'id'),n(row,'roster'),n(row,'state'),n(row,'vid'),n(row,'vroster'),n(row,'vstate'))==(17,17,1,vid,vid,1),
                'Joined canonical/live/participation identity changed')
        require(n(row,'hp')==expected_health(side,n(row,'frame')) and n(row,'vhp')==expected_health(3-side,n(row,'frame')) and n(row,'side')==side,
                'Native health-store field continuity/slot')
        require(row.get('writes')=='0' and n(row,'age')==n(row,'frame')-mf, 'Field epoch/memory-free evidence')
    def clean(row):
        return all(h(row,prefix+'action') in (0,0x303) and n(row,prefix+'y' if not prefix else 'vypos')==n(row,prefix+'floor') and
                   h(row,prefix+'vx')==0 and h(row,prefix+'vy')==0 and h(row,prefix+'flags')&0x1c==0 and
                   h(row,prefix+'body')&0x0c==0 and h(row,prefix+'trail')==0 for prefix in ('','v'))
    require(clean(jump) and clean(ready) and clean(final) and n(ready,'suppression')==0 and n(final,'suppression')==0,
            'Grounded clean inputs/returned controllers, not stale throw flags/trails/velocity')
    require(n(match,'hp')==161 and n(match,'vhp')==161 and n(ready,'vhp')==145 and n(final,'vhp')==expected_health(3-side,ff), 'Native health continuity bookends')
    events=rows('EVENT'); groups={kind:[r for r in events if r.get('kind')==kind] for kind in ENTRIES}
    for kind,group in groups.items():
        require(len(group)>=20 if kind=='callback' else len(group)==1, 'Missing/duplicate actual '+kind)
        for index,row in enumerate(group,1):
            require(h(row,'entry')==ENTRIES[kind] and h(row,'pc')==ENTRIES[kind]+16 and n(row,'count')==index,
                    'Actual typed native entry/count '+kind)
            require((h(row,'actor'),h(row,'main'),h(row,'victim'),h(row,'vmain'))==(actor,main,vactor,vmain), 'Event owner binding')
            victim_kind=kind in ('flight','callback','bounce','victim_getup','victim_recovery')
            require(h(row,'a8')==(vactor if victim_kind else actor), 'Executing actor '+kind)
            require(0x01000000<=h(row,'a13')<0x01100000 if kind=='gate' else h(row,'a13')==(vmain if victim_kind else main),
                    'Actual native process '+kind)
            require(cf<=n(row,'frame')<rf and n(row,'age')==n(row,'frame')-mf, 'Native event chronology '+kind)
    def ef(kind):
        return n(groups[kind][0],'frame') if len(groups[kind]) else -1
    af=ef('action');release=ef('release');flight=ef('flight');bounce=ef('bounce');getup=ef('victim_getup')
    # FF842710 schedules the real victim process. Depending on which slot
    # remains to run in this cooperative field, its first instruction is in
    # this field or the next. Neither a late flight nor reversed handoff is valid.
    ordered=[r.get('kind') for r in events if r.get('kind') in ('release','flight')]
    require(ordered==['release','flight'], 'Victim handoff must precede actual flight execution')
    require(cf<=af<=cf+6 and ef('gate')==af and ef('align')==af and release==af+8 and 0<=flight-release<=1 and
            flight<bounce<getup<=ef('victim_recovery')<rf and af<ef('damage')<ef('own_landing')<ef('own_recovery')<rf,
            'Native catch/8-field hold/early flight/bounce/landing/cleanup sequence')
    if groups['damage']:
        require(h(groups['damage'][0],'a0')==16 and h(groups['damage'][0],'a10')==vactor, 'Original sixteen-point damage argument/victim')
    callbacks=[n(r,'frame') for r in groups['callback']]
    require(callbacks==list(range(flight+1,getup+1)), 'Native callback each field across flight and rebound')
    for row in groups['callback']:
        require(h(row,'a6')==0xfffff800, 'Native callback attachment')
    # The authored catch alignment is 41,-3; the three imported Kano poses
    # must be drawn by his actual main process, not a Jax/Liu proxy.
    for field in range(af+1,release+1):
        row=states.get(field,{})
        direction=1 if n(jump,'x')<n(jump,'vxpos') else -1
        require(h(row,'action')==0x109 and h(row,'pose')==0xfe828e80 and
                n(row,'vxpos')-n(row,'x')==41*direction and n(row,'vypos')-n(row,'y')==-3,
                'Eight-field own pose/native victim catch alignment')
    ownposes={h(r,'pose') for r in fields if af<n(r,'frame')<ef('own_recovery')}
    require({0xfe828e80,0xfe828ec0,0xfe828f00}<=ownposes, 'Complete imported catch/throw pose progression')
    direction=1 if n(jump,'x')<n(jump,'vxpos') else -1
    for elapsed in range(1,27):
        row=states.get(af+elapsed,{})
        expected=0xfe828e80 if elapsed<=8 else 0xfe828ec0 if elapsed<=10 else 0xfe828f00
        require(h(row,'pose')==expected and h(row,'action')==0x109 and
                n(row,'x')==n(jump,'x') and n(row,'y')==n(row,'floor')-63 and
                h(row,'vx')==0 and h(row,'vy')==0 and h(row,'flags')&0x10 and h(row,'body')&4,
                'Exact three-pose catch/throw holds with native frozen ownership')
    for field in range(flight+2,getup+1):
        row=states.get(field,{})
        require(h(row,'vpose')==(0xff02f920 if vid==18 else 0xff97ba70), 'Victim-specific native horizontal flight pose')
    first_arc=[r for r in fields if flight+2<=n(r,'frame')<=bounce]
    rebound=[r for r in fields if bounce+1<=n(r,'frame')<=getup]
    require(len(first_arc)>=8 and all(n(b,'vypos')>=n(a,'vypos') for a,b in zip(first_arc,first_arc[1:])), 'Descending early release arc')
    for row in first_arc:
        f=n(row,'frame');previous=states.get(f-1,{})
        require(h(row,'vvx')==(0x30000 if direction==1 else 0xfffd0000) and
                n(row,'vxpos')-n(previous,'vxpos')==6*direction and
                h(row,'vvy')==(f-flight-1)*0xa000,
                'Native three-pixel velocity plus callback travel and .625 gravity')
    for row in rebound:
        f=n(row,'frame')
        require(h(row,'vvx')==(0x1fc00 if side==1 else 0xfffefc00) and
                h(row,'vvy')==(-0x58000+(f-bounce-1)*0x7000)&0xffffffff,
                'Native signed mirror rebound velocity and .4375 gravity')
    require(any(h(r,'vvy')>=0x80000000 for r in rebound) and any(0<h(r,'vvy')<0x80000000 for r in rebound),
            'Real upward/downward native impact rebound')
    stores=rows('HEALTH')
    require(len(stores)==1, 'Exactly one native health write')
    if len(stores)==1:
        row=stores[0]
        require(h(row,'pc')==0xff836700 and h(row,'a8')==vactor and h(row,'a13')==main and
                h(row,'actor')==actor and h(row,'victim')==vactor and n(row,'frame')==ef('damage') and
                (n(row,'before'),n(row,'after'),n(row,'delta'),n(row,'stores'))==(161,145,16,1), 'Actual original health writer/context/damage')
        sf=n(row,'frame')
        require(all(n(r,'vhp')==(161 if n(r,'frame')<=sf else 145) for r in fields if n(r,'frame')<follow_start+112), 'Native health-store/field continuity')
    for field in range(rf,ff+1):
        if not followup or not follow_start<=field<follow_start+160:
            require(clean(states.get(field,{})), 'Sustained clean recovered control')
    if followup:
        walk_count=24 if follow.get('walk')=='0,24' and vid==8 else 8
        require(n(follow,'frame')==rf and follow_start==rf+16 and n(follow,'side')==side and n(follow,'vid')==vid and
                (follow.get('walk'),follow.get('jump'),follow.get('hp'),follow.get('block'),follow.get('settle'),follow.get('writes'))==
                ('0,'+str(walk_count),'40,3','112,3','136,6','160','0'), 'Exact post-recovery normal control plan')
        require(follow_start+160<ff, 'Follow-up must finish before final clean coverage')
        following=rows('FOLLOW_CONTROL')
        direction=1 if n(ready,'x')<n(ready,'vxpos') else -1
        for slot in (1,2):
            towards='right' if (slot==side and direction==1 or slot!=side and direction==-1) else 'left'
            actual=[(n(r,'frame'),n(r,'age'),r.get('button'),n(r,'value')) for r in following if n(r,'slot')==slot]
            expected=[(follow_start+a,a,b,1) for b,first,count in ((towards,0,walk_count),('up',40,3),('hp',112,3),('block',136,6)) for a in range(first,first+count)]
            require(actual==expected, 'Actual normal walk/jump/punch/block controls slot '+str(slot))
        require(len(following)==2*(walk_count+12) and all(n(r,'slot') in (1,2) and r.get('writes')=='0' for r in following), 'No extra/missing follow-up inputs')
        physics=rows('FOLLOW_EVENT')
        require(len(physics)==2 and sorted(n(r,'slot') for r in physics)==[1,2], 'Both native jump physics entries required')
        for row in physics:
            slot=n(row,'slot');a,m=(actor,main) if slot==side else (vactor,vmain)
            require(row.get('kind')=='jump_physics' and h(row,'entry')==0xff876660 and h(row,'pc')==0xff876670 and
                    (h(row,'a8'),h(row,'a13'),h(row,'actor'),h(row,'main'))==(a,m,a,m) and
                    40<=n(row,'age')<=52 and n(row,'frame')==follow_start+n(row,'age') and
                    h(row,'a0')==0 and h(row,'a1')==0xfff60000 and h(row,'a2')==0x8000 and h(row,'a6')==0,
                    'Original grounded jump integrator arguments/controller')
        for prefix,slot in (('',side),('v',3-side)):
            xkey,ykey=('x','y') if not prefix else ('vxpos','vypos')
            start=states.get(follow_start,{})
            walking=[r for r in fields if follow_start+1<=n(r,'frame')<=follow_start+32 and h(r,prefix+'vx')!=0]
            require(walking and all(h(r,prefix+'action')==0 and h(r,prefix+'vx') in (0x28000,0xfffd8000) and
                                   n(r,ykey)==n(r,prefix+'floor') and h(r,prefix+'vy')==0 for r in walking),
                    'Native walking velocity/ground state slot '+str(slot))
            walking_end=states.get(follow_start+40,{})
            require(abs(n(walking_end,xkey)-n(start,xkey))>=20, 'Actual walking displacement, not frozen pose slot '+str(slot))
            airborne=[r for r in fields if follow_start+44<=n(r,'frame')<=follow_start+88 and n(r,ykey)<n(r,prefix+'floor')]
            require(len(airborne)==38 and all(h(r,prefix+'action')==0x30b and h(r,prefix+'callback')==0 and h(r,prefix+'vx')==0 and
                                            h(r,prefix+'flags')&0x1c==0 and h(r,prefix+'body')&0x0c==0 for r in airborne),
                    'Real follow-up jump with cleared throw callback/ownership slot '+str(slot))
            if len(airborne)==38:
                middle,tucked=(0xfe828320,0xfe828380) if slot==side else ((0xfe835c20,0xfe835c80) if vid==18 else (None,None))
                first_air=n(airborne[0],'frame')
                require([n(r,'frame') for r in airborne]==list(range(first_air,first_air+38)), 'Complete contiguous ordinary jump')
                native=[r for r in physics if n(r,'slot')==slot]
                require(len(native)==1 and first_air-n(native[0],'frame') in (1,2), 'Native jump entry before actual motion')
                base=h(walking_end,prefix+'yraw')
                require(base>>16==n(walking_end,prefix+'floor'), 'Actual full fixed-point grounded jump origin')
                for tick,row in enumerate(airborne,1):
                    raw=base-10*65536*tick+32768*tick*(tick+1)//2
                    require(n(row,ykey)==math.floor(raw/65536) and h(row,prefix+'yraw')==raw&0xffffffff and
                            h(row,prefix+'vy')==(-10*65536+tick*32768)&0xffffffff,
                            'Exact original 38-field vertical jump trajectory')
                    if middle is not None:
                        require(h(row,prefix+'pose')==(middle if tick<=4 else tucked), 'Own imported native jump cadence/art')
            require(any(h(r,prefix+'vy')>=0x80000000 for r in airborne) and any(0<h(r,prefix+'vy')<0x80000000 for r in airborne),
                    'Both ascent and descent of follow-up jump slot '+str(slot))
            hpfields=[r for r in fields if follow_start+113<=n(r,'frame')<=follow_start+135 and h(r,prefix+'action')==0x101]
            require(len(hpfields)>=3 and any(h(r,prefix+'pose')!=h(walking_end,prefix+'pose') for r in hpfields), 'Actual native high punch slot '+str(slot))
            blocked=[r for r in fields if follow_start+137<=n(r,'frame')<=follow_start+152 and h(r,prefix+'action')==0x700]
            require(len(blocked)>=3 and all(n(r,ykey)==n(r,prefix+'floor') and h(r,prefix+'vx')==0 and h(r,prefix+'vy')==0 and
                                          h(r,prefix+'flags')&0x1c==0 for r in blocked), 'Original grounded block action slot '+str(slot))
        require(1<=len(follow_health)<=2, 'Actual unassisted follow-up punch contact required')
        before={side:161,3-side:145}
        for row in follow_health:
            slot=n(row,'slot');a,m=(actor,main) if slot==side else (vactor,vmain)
            attacker_main=vmain if slot==side else main
            attacker_actor=vactor if slot==side else actor
            require(slot in (1,2) and h(row,'actor')==a and h(row,'main')==m and h(row,'a8')==attacker_actor and
                    h(row,'a13')==attacker_main and h(row,'pc')==0xff836700 and
                    follow_start+113<=n(row,'frame')<=follow_start+135 and n(row,'age')==n(row,'frame')-follow_start and
                    n(row,'before')==before.get(slot) and n(row,'delta')==11 and n(row,'after')==n(row,'before')-11,
                    'Native high-punch health writer/eleven-point contact context')
            before[slot]=n(row,'after')
        samples=rows('FOLLOW_SAMPLE')
        require([n(r,'frame') for r in samples]==[follow_start+a for a in (walk_count,64,120,144,160)], 'Actual walk/air/punch/block/recovered snapshots')
        for row in samples:
            require(row==dict(states.get(n(row,'frame'),{})), 'Follow-up sample must match actual per-field observation')
        finished=one('FOLLOW_RESULT')
        require(n(finished,'frame')==follow_start+160 and n(finished,'begin')==follow_start and n(finished,'fields')==161 and
                finished.get('pass')=='true' and finished.get('writes')=='0', 'Complete normal-input recovery checkpoint')
    else:
        require(not rows('FOLLOW_CONTROL') and not rows('FOLLOW_EVENT') and not follow_health and not rows('FOLLOW_RESULT'), 'Undeclared follow-up evidence')
    require(result.get('pass')=='true' and n(result,'side')==side and result.get('victim')==begin.get('victim') and
            all(n(result,k)==v for k,v in (('begin',bf),('match',mf),('jump',jf),('command',cf),('caught',af),
            ('own_recovery',ef('own_recovery')),('victim_recovery',ef('victim_recovery')),('damage',16),('stores',1),('errors',0),('writes',0))),
            'Observer summary must match independent native evidence')
    require(not re.search(r'MK2_AIR_JOIN_ERROR|\[LUA ERROR\]|fatal error|access violation',log,re.I), 'Actual join/throw runtime errors')
    return dict(passed=not errors, errors=sorted(set(errors)), side=side, victim=begin.get('victim'),
                native_events={k:len(v) for k,v in groups.items()}, joined_fields=len(fields),
                followup_verified=followup and not errors,
                scope=('post_ending_' if require_restart else 'cold_diagnostic_')+'native_two_human_join_airthrow_not_naturally_jumping_cpu_or_all_moves',
                full_goal_complete=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('log',type=Path);parser.add_argument('--side',type=int,choices=(1,2),default=1)
    parser.add_argument('--followup',action='store_true')
    parser.add_argument('--cold',action='store_true')
    args=parser.parse_args();out=verify(args.log.read_text(encoding='utf-8-sig'),side=args.side,require_followup=args.followup,require_restart=not args.cold)
    print(json.dumps(out,indent=2));raise SystemExit(0 if out['passed'] else 1)
