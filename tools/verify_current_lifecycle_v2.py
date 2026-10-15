"""Check actual per-field unassisted blade/bicycle KO and next-round evidence.

This deliberately does not claim CPU, ending/restart or all-victim coverage.
"""
import argparse
import json
import re
from pathlib import Path

IDS={'kano':17,'sonya':18,'kitana':4,'sub_zero':8}
BLADE_HOLDS=(2,2,2,2,2,4,4,12,4,4)
BIKE_CYCLE=(0xFE83EB40,0xFE83EB80,0xFE83EBC0,0xFE83EC00,0xFE83EC40,
            0xFE83EC80,0xFE83EC40,0xFE83EC00,0xFE83EBC0,0xFE83EB80)
KANO_STUMBLE=(0xFE8294A0,0xFE829500,0xFE829560,0xFE8295A0,0xFE829620,0xFE829680)
HEX={'actor','main','action','pose','xraw','yraw','vx','vy','gravity','flags','body','trail','descriptor',
    'entry','pc',*(f'a{i}' for i in (0,1,2,3,6,8,9,10,11,13))}
TEXT={'move','names','kind'}


def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith('MK2_LIFE_TRACE_'+tag+' '):continue
        record={}
        for key,value in re.findall(r'(\w+)=([^\s]+)',line):
            record[key]=value if key in TEXT else int(value,16 if key in HEX or tag=='VELOCITY' and key in ('before','after') else 10)
        result.append(record)
    return result


def bike_poses(own,events,first):
    """Use actual native cursor reads, NEVER pick a phase from observed poses.

    The action initializes the authored loop before its seeking flight, and
    deliberately retains that cursor when contact occurs. An earlier contact
    can therefore begin the pair one pose earlier than a later contact.
    FF83BB00's original MOVE reads the list pointer; each periodic tick advances
    exactly one authored cell, with the original loop-token recursion.
    """
    root=0xFFF9EB00
    calls=[e for e in events if e['kind']=='animation' and
           e['a8']==own[0]['actor'] and e['a13']==own[0]['main'] and
           root<=e['a9']<=root+10*32 and e['age']<=first+47]
    if not calls or calls[0]['a9']!=root:
        raise ValueError('Missing original loop initialization cursor')
    draws=[];next_index=0
    for event in calls:
        if event['pc']!=0xFF83BB10 or event['entry']!=0xFF83BB00:
            raise ValueError('Original native loop reader instruction')
        index=(event['a9']-root)//32
        if event['a9']!=root+index*32:
            raise ValueError('Authored loop cursor alignment')
        if next_index==10:
            if index!=10:raise ValueError('Missing actual loop-token read')
            next_index=0
            continue
        if index!=next_index:raise ValueError('Skipped/reordered authored bicycle loop cell')
        draws.append((event['age'],BIKE_CYCLE[index]))
        next_index=index+1
    periodic=[age for age,pose in draws if first<=age<=first+47]
    if periodic!=list(range(first,first+48,4)):
        raise ValueError('Every actual paired loop draw at its original four-field cadence')
    output=[]
    for age in range(first,first+48):
        preceding=[pose for draw_age,pose in draws if draw_age<age]
        if not preceding:raise ValueError('Independent pre-callback loop provenance absent')
        output.append(preceding[-1])
    return output


def _verify(log,move,side,victim,require_base=True):
    errors=[]
    def check(ok,label):
        if not ok and label not in errors:errors.append(label)
    boot=rows(log,'BOOT')
    names=[victim,victim];names[side-1]='kano' if move=='blade' else 'sonya'
    check(boot==[{'move':move,'side':side,'names':','.join(names),'writes':0}], 'Actual move/player-order boot')
    expected_cycles,end_age,damage=(8,150,26) if move=='blade' else (9,200,22)
    fields,events,health=rows(log,'FIELD'),rows(log,'EVENT'),rows(log,'HEALTH')
    velocity=rows(log,'VELOCITY')
    check(len(fields)==expected_cycles*(end_age+1)*2,'Complete both-slot field trace')
    check({r['cycle'] for r in fields}==set(range(1,expected_cycles+1)),'All actual cycles traced')
    check(all(r.get('writes')==0 for r in fields+events+health),'No observer writes')
    check(len(health)==expected_cycles,'One native damage store per cycle')
    previous_end=0
    for cycle in range(1,expected_cycles+1):
        by_age={(r['age'],r['slot']):r for r in fields if r['cycle']==cycle}
        complete=set(by_age)=={(a,n) for a in range(end_age+1) for n in (1,2)}
        check(complete,f'Cycle {cycle}: consecutive unique fields')
        if not complete:continue
        own=[by_age[a,side] for a in range(end_age+1)]
        other=[by_age[a,3-side] for a in range(end_age+1)]
        epoch=own[0]['frame'];check(epoch>previous_end,f'Cycle {cycle}: ordered commands');previous_end=own[-1]['frame']
        initial=161 if cycle==expected_cycles else max(0,161-damage*(cycle-1))
        after=max(0,initial-damage)
        for slot,fld in ((side,own),(3-side,other)):
            actor,main=fld[0]['actor'],fld[0]['main']
            check(0x01000000<=actor<0x01100000 and 0x01000000<=main<0x01100000,f'Cycle {cycle}: native RAM owners')
            check(all(r['frame']==epoch+r['age'] and r['actor']==actor and r['main']==main and
                      r['id']==r['roster']==IDS[names[slot-1]] and r['state']==1 for r in fld),f'Cycle {cycle}: live independent human identities/owners')
        check(all(r['hp']==161 for r in own),f'Cycle {cycle}: no attacker damage/assistance')
        ev=[r for r in events if r['cycle']==cycle]
        native_entries={'action':0xFFF8CC00,'strike':0xFFF8E400,'create':0xFFF8D800,'step':0xFFF8E000,
                        'hurt':0xFFF90000,'blood_request':0xFF9A5B00,'blood_start':0xFF9A7F70,
                        'blood_allocate':0xFF9AFF00,'blood_insert':0xFF83F610,'blood_cleanup':0xFF9B0E50,
                        'recovery':0xFF861350} if move=='blade' else {
                        'action':0xFFF9A400,'strike':0xFFF9EE00,'tick':0xFFF9D000,'release':0xFFF9E000,
                        'animation':0xFF83BB00,'fling':0xFF876650,'recovery':0xFF861350}
        check(all(r['kind'] in native_entries and r['entry']==native_entries[r['kind']] and
                  (r['kind']=='strike' or r['pc']==r['entry']+16) for r in ev),f'Cycle {cycle}: actual typed native event entries/PCs')
        def kind(name):return [r for r in ev if r['kind']==name]
        def context(r,fld):return r['a8']==fld[0]['actor'] and r['a13']==fld[0]['main']
        action=kind('action');check(len(action)==1,f'Cycle {cycle}: one native action')
        if len(action)!=1:continue
        act=action[0];start=act['age']
        entry=0xFFF8CC00 if move=='blade' else 0xFFF9A400
        check(act['entry']==entry and act['pc']==entry+16 and context(act,own) and start==(8 if move=='blade' else 15),f'Cycle {cycle}: actual command/action ownership')
        check(all(r['frame']==epoch+r['age'] and 0<=r['age']<=end_age for r in ev),f'Cycle {cycle}: event chronology')
        hp=[r for r in health if r['cycle']==cycle]
        if len(hp)==1:
            h=hp[0]
            check(h['slot']==3-side and h['before']==initial and h['after']==after and
                  h['pc']==0xFF836700 and context(h,own) and h['frame']==epoch+h['age'],f'Cycle {cycle}: original damage writer/context')
            check(all(r['hp']==(initial if r['frame']<=h['frame'] else after) for r in other),f'Cycle {cycle}: full native health ledger')
        else:check(False,f'Cycle {cycle}: exact health event')
        if move=='blade':
            expected=[]
            for index,hold in enumerate(BLADE_HOLDS):expected += [(0xFE82FC40+index*0x60,0xFFF8F800+index*160)]*hold
            for elapsed,(pose,descriptor) in enumerate(expected,1):
                r=own[start+elapsed]
                check(r['pose']==pose and r['descriptor']==descriptor and 0x01000000<=r['trail']<0x01100000 and
                      r['action']==(0x117 if elapsed<=10 else 0x618),f'Cycle {cycle}: exact 38-field body/trail choreography')
            check(len(kind('create'))==1 and context(kind('create')[0],own) and kind('create')[0]['age']==start,f'Cycle {cycle}: one owned effect allocation')
            check([r['age']-start for r in kind('step')]==[2,4,6,8,10,14,18,30,34] and all(context(r,own) for r in kind('step')),f'Cycle {cycle}: nine original effect steps')
            strike=kind('strike')
            check(len(strike)==1 and strike[0]['entry']==0xFFF8E400 and strike[0]['age']==start+10 and context(strike[0],own),f'Cycle {cycle}: ten-field startup/collision')
            for name in ('hurt','blood_request','blood_start'):
                check(len(kind(name))==1,f'Cycle {cycle}: own cut reaction/native blood recipe')
            if len(kind('hurt'))==1:check(context(kind('hurt')[0],other),f'Cycle {cycle}: victim-owned cut reaction')
            if len(kind('blood_request'))==1:check(context(kind('blood_request')[0],other) and kind('blood_request')[0]['a0']==1,f'Cycle {cycle}: native blood type one')
            allocations=kind('blood_allocate')
            allocated={r['a8'] for r in allocations}
            # The generic display insertion also inserts the danger indicator.
            # Bind blood evidence to the actual allocated victim-owned objects.
            insertions=[r for r in kind('blood_insert') if r['a8'] in allocated]
            cleanups=[r for r in kind('blood_cleanup') if r['a8'] in allocated]
            check(len(allocations)==len(insertions)==len(cleanups)==len(allocated)==8 and
                  allocated=={r['a8'] for r in insertions}=={r['a8'] for r in cleanups} and
                  all(r['a11']==other[0]['actor'] for r in allocations),f'Cycle {cycle}: eight actual victim blood objects allocated/inserted/cleaned')
            for obj in allocated:
                a=[r['frame'] for r in allocations if r['a8']==obj];i=[r['frame'] for r in insertions if r['a8']==obj];c=[r['frame'] for r in cleanups if r['a8']==obj]
                check(len(a)==len(i)==len(c)==1 and a[0]<=i[0]<c[0],f'Cycle {cycle}: blood object lifetime')
        else:
            ticks=kind('tick');check(len(ticks)==48,f'Cycle {cycle}: full 32-rise/16-float paired update sequence')
            if len(ticks)==48:
                first=ticks[0]['age']
                check([r['age'] for r in ticks]==list(range(first,first+48)) and all(r['entry']==0xFFF9D000 and context(r,own) for r in ticks),f'Cycle {cycle}: consecutive native paired ticks')
                direction=1 if own[0]['x']<other[0]['x'] else -1
                expected_poses=bike_poses(own,ev,first)
                for i in range(48):
                    a,b=own[first+i],other[first+i]
                    check(a['action']==0x214 and b['action']==0x215,f'Cycle {cycle}: native paired states')
                    requested=(direction*(0x30000 if i<32 else 0x10000))&0xFFFFFFFF
                    clamped=False
                    if a['vx']==0 and 'left' in a and 'right' in a:
                        clears=[r for r in velocity if r['cycle']==cycle and r['slot']==side and r['actor']==a['actor'] and
                                r['frame']<a['frame'] and r['after']==0 and r['before']==requested and r['a2']==a['actor'] and
                                r['pc']==(0xFF805610 if direction==1 else 0xFF805580) and r['a13']==0xFFFFF010 and
                                (r['a0']&0xFFFF)==(r['left']&0xFFFF) and (r['a1']&0xFFFF)==(r['right']&0xFFFF)]
                        clamped=bool(clears) and a['x']==a['right' if direction==1 else 'left']
                    check(a['vy']==(0xFFFD0000 if i<32 else 0x8000) and (a['vx']==requested or clamped) and a['gravity']==0,f'Cycle {cycle}: original rise/float velocities or actual native corner clamp')
                    check(a['pose']==expected_poses[i],f'Cycle {cycle}: exact own ten-pose loop from independent native cursor reads')
                    if i:
                        check(b['x']-a['x']==direction*48 and b['y']-a['y']==-32 and b['vx']==a['vx'] and b['vy']==a['vy'] and b['gravity']==0,f'Cycle {cycle}: actual paired offset/physics')
                        check(a['yraw']==(own[first+i-1]['yraw']+own[first+i-1]['vy'])&0xFFFFFFFF,f'Cycle {cycle}: exact fixed-point paired Y trajectory')
                    if victim=='kano':check(b['pose']==(KANO_STUMBLE[0] if i==0 else KANO_STUMBLE[((i-1)//4+1)%6]),f'Cycle {cycle}: independent six-pose victim loop')
                release=kind('release')
                check(len(release)==1 and release[0]['age'] in (first+47,first+48) and context(release[0],other),f'Cycle {cycle}: actual victim release after all ticks')
            flings=kind('fling')
            check(any(context(r,other) and (r['a0'],r['a1'],r['a2'],r['a3'])==(0x40000,0xFFFA0000,0xA000,5) for r in flings),f'Cycle {cycle}: native victim fling parameters')
            check(any(context(r,own) and (r['a0'],r['a1'],r['a2'],r['a3'])==(0,0x20000,0x8000,0xFFF) for r in flings),f'Cycle {cycle}: native attacker landing parameters')
        for fld in (own,other):
            r=fld[-1]
            flag_mask=0x18 if r['hp']==0 and r['action']==0x506 else 0x1C
            check(r['y']==r['floor'] and r['vx']==r['vy']==r['gravity']==r['trail']==0 and r['flags']&flag_mask==0 and r['body']&0x0C==0,f'Cycle {cycle}: floor/physics/flags/effect cleanup')
            if r['hp']>0:check(any(context(e,fld) for e in kind('recovery')),f'Cycle {cycle}: original recovery for surviving owner')
    marker='MK2KS_'+move.upper()+'_LIFECYCLE_RESULT pass=true '
    check(marker in log and f'cycles={expected_cycles} ' in log,'Actual completed KO/next-round observer')
    next_tag='MK2KS_BLADE_LIFECYCLE_NEXT_ROUND' if move=='blade' else 'MK2KS_BICYCLE_LIFECYCLE_NEXT'
    next_frames=re.findall(r'^'+next_tag+r' frame=(\d+)',log,re.M)
    check(len(next_frames)==1 and any(r['cycle']==expected_cycles and r['hp']==161 and r['frame']>int(next_frames[0]) for r in fields),'Actual native new full-health round')
    markers=['MK2KS_DISPLAY_RESULT pass=true ','MK2KS_HUD_SHADOW_RESULT pass=true ','MK2KS_STABILITY stalled_frames=0 trap_frames=0']
    if require_base:markers.append('MK2KS_EXIT_RESULT pass=true ')
    for marker in markers:
        check(marker in log,'Native selection/presentation/stability acceptance')
    check(not re.search(r'(?i)\[LUA ERROR\]|access violation|fatal error|LIFECYCLE_ERROR',log),'No runtime/observer errors')
    return {'passed':not errors,'errors':errors,'move':move,'side':side,'victim':victim,'cycles':expected_cycles,
            'actual_fields':len(fields),'health_stores':len(health),'scope':'unassisted_cold_two_human_full_move_KO_next_round_not_CPU_or_post_ending'}


def verify(log,move,side,victim,require_base=True):
    try:return _verify(log,move,side,victim,require_base)
    except (KeyError,ValueError,TypeError,IndexError) as error:
        return {'passed':False,'errors':['Malformed or incomplete actual trace: '+str(error)],'move':move,'side':side,'victim':victim}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('log',type=Path)
    parser.add_argument('--move',choices=('blade','bicycle'),required=True)
    parser.add_argument('--side',type=int,choices=(1,2),required=True)
    parser.add_argument('--victim',choices=IDS,required=True)
    args=parser.parse_args();result=verify(args.log.read_text(encoding='utf-8-sig'),args.move,args.side,args.victim)
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)


