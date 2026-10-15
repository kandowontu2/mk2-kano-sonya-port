"""Native choke and an early blade follow-up; never relabel INCOMPLETE as COMPLETE.

An uninterrupted grab fixture excludes early follow-up damage by design. This
separate contract checks the actual interleaved attack, both individual native
handoffs, continuous health/flag ledgers, and sampled native display.
"""
import argparse, hashlib, json, re, struct, sys
from pathlib import Path
import numpy as np
import verify_active_launch_cpu_display_v1525 as display
import verify_physical_p1_cpu_pair_v1457 as pair
from verify_restart_pair import CHOKE_OWN, CHOKE_XY, CHOKE_GRIP, CHOKE_GROUPS
from verify_p2_campaign import expected_orders
ROOT=display.ROOT
FOLDER=ROOT/'audit_v1554_cpu_cage_boot604'

def verify(log_override=None, pixels=True):
    pins={};display.matched(FOLDER,pins)
    log=(FOLDER/'run.log').read_text(encoding='utf-8-sig') if log_override is None else log_override
    need=display.require
    need(not re.search(r'\[LUA ERROR\]|fatal error|stack traceback|access violation',log,re.I),'No runtime error')
    get=lambda tag:pair.rows(log,tag)
    entries=get('ENTRY');need(entries and entries[0]['id']==17,'Actual first native Kano entry')
    entry=entries[0];cycle=entry['cycle'];start=entry['frame'];end=start+240
    fields={r['frame']:r for r in get('FIELD') if start<=r['frame']<=end}
    need(set(fields)==set(range(start,end+1)),'Every callback in entire interleaved window')
    cold=pair.rows_prefix(log,'MK2_P1CPU_COLD_LIVE ')
    selected=pair.rows_prefix(log,'MK2_P1CPU_SELECT_RESULT ')
    need(len(cold)==len(selected)==1,'One actual cold selection and fight')
    c,s=cold[0],selected[0]
    need(c['human']==s['human']=='cage' and c['human_id']==s['human_id']==2 and
         s['initial_cpu']==c['cpu_id']==17 and s['checks']>=30 and s['errors']==0 and
         700<s['css']<s['exit']<s['live']==c['frame'] and c['stage']==0 and
         c['schedule']==entry['schedule']==0xfffa3000,'Physical P2 Cage, native stage-zero Kano; no proxy')
    rom=get('ROM');orders=expected_orders()
    need(len(rom)==6 and all(r['order']==n and r['table']==0xfffa2c00 and
         r['list']==0xfffa3000+n*0x180 and tuple(map(int,r['ids'].split(',')))==orders[n]
         for n,r in enumerate(rom)),'All original-derived schedules including official new IDs')
    ids=('actor','main','vactor','vmain')
    need(len({entry[k] for k in ids})==4 and all(0x01000000<=entry[k]<0x01100000 for k in ids),'Distinct actual actors/Main')
    for r in fields.values():
        need(all(r[k]==entry[k] for k in ids) and r['owner']==r['actor'] and r['vowner']==r['vactor'] and
             r['id']==r['roster']==17 and r['vid']==r['vroster']==2 and r['state']==0 and r['vstate']==1 and
             r['mode']==2 and r['stage']==0 and r['schedule']==c['schedule'] and r['hp']==161 and 0<r['vhp']<=161 and
             r['writes']==0 and r['assistance']=='none' and r['cpu_slot']==1 and r['human_slot']==2,'Stable real CPU/human identity and ownership')
    events=[r for r in get('EVENT') if r['cycle']==cycle and start<=r['frame']<=end]
    ev=lambda kind:[r for r in events if r['kind']==kind]
    steps=ev('step');pulses=ev('pulse');damage=ev('damage');release=ev('release');fling=ev('fling')
    need(len(steps)==22 and len(pulses)==len(damage)==4 and len(release)==len(fling)==1,'All native choke phases, four squeezes, release/fling')
    times=[r['frame'] for r in steps];release=release[0]['frame']
    need(all(times[i]-times[i-1]==(5 if i<=3 else 3) for i in range(1,22)) and release in(times[-1],times[-1]+1),'Full original choke cadence')
    need([r['frame'] for r in pulses]==[times[3]+12*i for i in range(1,5)]==[r['frame'] for r in damage] and
         all(r['a10']==8 for r in damage),'Four real eight-point native squeeze calls')
    addresses=dict(action=0xfff91400,intro=0xfff94000,attack=0xfff94800,release=0xfff93800,
                   step=0xfff89400,pulse=0xfff93400,damage=0xff837340,fling=0xff876650,velocity=0xff831bd0,
                   own_ready=0xff861350,victim_ready=0xff861350,own_regain=0xff861500,victim_regain=0xff861500)
    for r in events:
        own=r['kind'] in('action','intro','attack','step','own_ready','own_regain')
        pc={'intro':0xff83bb10,'attack':0xff835480}.get(r['kind'],r['entry']+16)
        need(r['entry']==addresses[r['kind']] and r['pc']==pc and r['actor']==entry['actor'] and
             r['main']==entry['main'] and r['victim']==entry['vactor'] and r['vmain']==entry['vmain'] and
             r['a8']==entry['actor' if own else 'vactor'] and
             r['a13'] in((entry['main'],entry['vmain']) if r['kind'] in('damage','pulse') else (entry['main' if own else 'vmain'],)),
             'Every native choke instruction executes in its actual owning actor/Main')
    origin=fields[times[0]+1];direction=-1 if origin['facing']&16 else 1;held=0
    for i,step in enumerate(steps):
        phase=i if i<3 else (i-3)%4+3
        need(step['group']==CHOKE_OWN[phase] and step['steps']==i+1,'Every original choke composite step')
        dx,dy=CHOKE_XY[18][phase];gx,gy=CHOKE_GRIP[2];dx+=8+gx;dy+=54-gy
        final=times[i+1] if i+1<22 else times[i]+1
        for at in range(times[i]+1,final+1):
            r=fields[at]
            need(r['pose']==CHOKE_OWN[phase] and r['vpose']==CHOKE_GROUPS[2] and
                 r['vx']==r['vy']==0 and r['y']==r['floor'] and r['x']==origin['x'] and
                 r['vxpos']==r['x']+direction*dx and r['vypos']==r['y']+dy and
                 r['action']==0x111 and r['vaction'] in((0x112,0x506) if i==21 and release<=times[i] else(0x112,)),
                 'Every held callback has exact native paired art, grip offset and grounded Kano')
            held+=1
    own=[r for r in get('OWN_REGAIN') if r['cycle']==cycle];victim=[r for r in get('VICTIM_REGAIN') if r['cycle']==cycle]
    need(len(own)==len(victim)==1,'Both real individual native ready handoffs')
    own,victim=own[0],victim[0]
    need(own['frame']-release in(13,14) and own['frame']<victim['frame']<=end,'Original own recovery timing and actual later victim recovery')
    flags=pair.flag_rows(log);guest=display.grab.expected_guest()[0]
    for r,prefix,slot in((own,'',1),(victim,'v',2)):
        need(r[prefix+'action']==0 and r['y' if not prefix else 'vypos']==r[prefix+'floor'] and
             r[prefix+'vx']==r[prefix+'vy']==r[prefix+'gravity']==r[prefix+'trail']==0 and
             r[prefix+'flags']&0x1c==0 and r[prefix+'body']&0x0c==0,'Each owning ready handoff genuinely clears grounded control')
        for kind,pc,offset,mask in(('body',0xff83eeb0,0x160,0x0c),('flags',0xff83efc0,0x210,0x14)):
            need(any(n['frame']==r['frame'] and n['slot']==slot and n['kind']==kind and n['pc']==pc and
                 n['at']==r[prefix+('actor' if kind=='body' else 'main')]+offset and
                 n['a8']==r[prefix+'actor'] and n['a13']==r[prefix+'main'] and n['after']==n['before']&(~mask&0xffff)
                 for n in flags),'Actual original ready body/Main cleanup store')
    # Replay BOTH actual physical actors. Allocated Kano move instructions are
    # checked against the independently reconstructed actual guest, not falsely
    # required to be stock ROM instructions at formerly unused addresses.
    for slot,prefix in((1,''),(2,'v')):
        for kind,offset in(('body',0x160),('flags',0x210),('action',0x1f0)):
            stores=[r for r in flags if r['slot']==slot and r['kind']==kind and start<=r['frame']<end]
            value=fields[start][prefix+kind];cursor=0
            for at in range(start,end):
                need(fields[at][prefix+kind]==value,'Every raw physical callback equals native flag/state stores')
                while cursor<len(stores) and stores[cursor]['frame']==at:
                    r=stores[cursor];actor=entry[prefix+'actor'];main=entry[prefix+'main']
                    off=(r['pc']-32-0xff800000)//8
                    need(r['before']==value and r['actor']==actor and r['main']==main and
                         r['at']==(actor if kind=='body' else main)+offset and
                         0<=off<=len(guest)-4 and struct.unpack_from('<HH',guest,off)==(r['op0'],r['op1']),
                         'Continuous physically owned stores match exact current native instruction bytes')
                    value=r['after'];cursor+=1
            need(cursor==len(stores) and fields[end][prefix+kind]==value,'Both complete native state/flag ledgers')
    health=[r for r in get('HEALTH') if r['slot']==2 and start<=r['frame']<end]
    hp=entry['vhp'];cursor=0
    for at in range(start,end):
        need(fields[at]['vhp']==hp,'Every victim HP callback equals native health stores')
        while cursor<len(health) and health[cursor]['frame']==at:
            r=health[cursor]
            need(r['pc']==0xff836700 and r['before']==hp and 0<r['after']<=hp,'Original collision writer, continuous live health')
            hp=r['after'];cursor+=1
    need(cursor==len(health) and fields[end]['vhp']==hp,'Complete native health ledger')
    hits=[r for r in health if r['before']!=r['after']]
    squeeze=[r for r in hits if r['frame']<release]
    after=[r for r in hits if r['frame']>=release]
    need(len(squeeze)==4 and all(r['before']-r['after']==8 and r['a8']==entry['vactor'] and r['a13']==entry['vmain'] for r in squeeze) and
         [r['frame'] for r in squeeze]==[r['frame'] for r in damage],'Exactly 32 choke damage from victim-owned native squeeze calls')
    follow=[r for r in get('FOLLOW_INSTRUCTION') if r['cycle']==cycle and r['kind']=='action' and start<=r['frame']<=end]
    need(len(follow)==1 and follow[0]['move']=='blade' and follow[0]['entry']==0xfff8cc00 and follow[0]['pc']==0xfff8cc10 and
         follow[0]['actor']==follow[0]['a8']==entry['actor'] and follow[0]['main']==follow[0]['a13']==entry['main'] and
         own['frame']<follow[0]['frame']<victim['frame'],'Actual free CPU chooses its own blade before victim recovery')
    need(len(after)==1 and after[0]['before']-after[0]['after']==26 and after[0]['a8']==entry['actor'] and
         after[0]['a13']==entry['main'] and follow[0]['frame']<after[0]['frame']<victim['frame'],'Separate real 26-point blade contact, not extra grab damage')
    need(any(r['slot']==1 and r['kind']=='action' and r['frame']>after[0]['frame'] and r['pc']==0xff83edd0 and
         r['before']==0x618 and r['after']==0 and r['a8']==entry['actor'] and r['a13']==entry['main'] for r in flags),
         'Blade really clears through original ready before later continuation')
    need(not any(r['cycle']==cycle for r in get('COMPLETE')) and any(r['cycle']==cycle and r['frame']==victim['frame']+1 for r in get('INCOMPLETE')),
         'Preserved fixture remains incomplete for uninterrupted-grab acceptance')
    proof=dict(target='kano',player='cage',cycle=cycle,start=start,release=release,CPU_slot=1,human_slot=2,log=log)
    scans=0;cache=None
    if pixels:
        payload=(ROOT/display.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
        groups,*_=display.raster.data(FOLDER)
        image=bytearray(display.graphics_model.graphics(pins))
        for header,magic,source,dest in((0x1c0000,b'KFX1',0x1c4000,0x1e04000),(0x1c1000,b'KPI1',0x1e6000,0x1e50000),(0x1c2000,b'KPJ1',0x1f4000,0x1e60000),(0x1d0000,b'KBL1',0x1d4000,0x1e08000)):
            need(payload[header:header+4]==magic,'Exact native effect allocation')
            first,count,destination=struct.unpack_from('<III',payload,header+4)
            need(first==source and destination==dest and count>0,'Exact native graphics bounds')
            image[dest:dest+count]=payload[source:source+count]
        for r in groups['FLOOR_GFX']:
            need(bytes.fromhex(r['data'])==image[r['first']:r['first']+r['bytes']],'Whole-scene actual graphics bytes equal independently reconstructed current source')
        cache=display.check_composites(groups,payload,guest,proof)
        drawn=display.raster.inspect(FOLDER)
        need(drawn['frames']>100 and all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in drawn['records']),
             'Every retained original native DMA/CPU pass and full displayed scanout exactly reconstructs')
        need(all(b['pixels']>100 and b['mismatches']==0 for r in drawn['records'] for b in r['body'].values()),'Both exact owned bodies throughout samples')
        need(len(groups['FLOOR_RESULT'])==1 and groups['FLOOR_RESULT'][0]['snapshots']==drawn['frames'] and
             groups['FLOOR_RESULT'][0]['origin']==start,'All exact sampled scanouts accounted from first actual CPU grab')
        displays={r['frame']:r for r in groups['FLOOR_DISPLAY']}
        queues={(r['frame'],r['cursor']):r for r in groups['FLOOR_QUEUE']}
        dmas={r['event']:r for r in groups['FLOOR_DMA']}
        colors_checked=0
        for snap in groups['FLOOR_SNAP']:
            colors=np.fromfile(FOLDER/displays[snap['frame']]['palette_file'],dtype='<u4')
            for r in groups['FLOOR_QUEUE_DISPATCH']:
                if dmas[r['event']]['frame']!=snap['frame']-1 or r['slot']!=1:continue
                q=queues[r['queue_frame'],r['cursor']]
                display.check_owned_body_palette(q,colors,guest,(17,2),1);colors_checked+=1
        need(colors_checked>100,'Real Kano costume across all retained native scanouts')
        scans=drawn['frames']
    return dict(passed=True,candidate=display.NAME,firstGrabStart=start,release=release,heldFields=held,
                chokeDamage=32,earlyBladeDamage=26,ownReady=own['frame'],victimReady=victim['frame'],
                completeBothPhysicalStateLedgers=True,uninterruptedFixtureAccepted=False,
                sampledNativeScanouts=scans,cache=cache,inputHashes=pins,fullPortAcceptance=False,
                scope='Actual native CPU choke plus early blade contact, handoffs and sampled scanout; not all CPU moves, victims, audio, campaign or full port')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--state-only',action='store_true');args=parser.parse_args()
    if args.output.exists():raise ValueError('Never overwrite evidence')
    try:report=verify(pixels=not args.state_only)
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    if report['passed']:
        for path in FOLDER.rglob('*'):
            if path.is_file():report['inputHashes'][str(path.resolve())]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
        for module in tuple(sys.modules.values()):
            value=getattr(module,'__file__',None)
            if value:
                path=Path(value).resolve()
                if path.is_relative_to(ROOT/'tools') and path.suffix=='.py':report['inputHashes'][str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    args.output.parent.mkdir(exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in('inputHashes','cache')},indent=2))
    raise SystemExit(0 if report['passed'] else 1)
