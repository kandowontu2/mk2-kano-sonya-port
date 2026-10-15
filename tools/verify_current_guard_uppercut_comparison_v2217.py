"""Current-build human command/contact/recovery smoke matrix, not full acceptance."""
import json
import re
from pathlib import Path
import verify_continue_palette_floor as build
from verify_ko_round_floor_shadows import need, digest, rgb

ROOT=build.p.ROOT
SPECS={'uppercut_kano':(17,0xff870dc0,40),'uppercut_sonya':(18,0xff870dc0,40),'uppercut_liu':(1,0xff870dc0,40),'uppercut_subzero':(8,0xff870dc0,40)}
HEX={'actor','main','owner','pose','vx','vy','gravity','flags','body','trail','bank',
     'entry','expectedEntry','pc','a8','a13','mask','hardware0','a0','a1'}

def rows(log,tag):
    out=[]
    for line in log.splitlines():
        if not line.startswith('MK2_HSPECIAL_'+tag+' '):continue
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        for key,value in row.items():
            if key in HEX and not(tag=='RESULT' and key=='entry'):row[key]=int(value,16)
            elif re.fullmatch(r'-?\d+',value):row[key]=int(value)
        out.append(row)
    return out

def clean(field):
    return (field['y']==field['floor'] and field['vx']==field['vy']==field['gravity']==field['trail']==0
            and field['flags']&0x1c==0 and field['body']&0x0c==0 and field['action']==0x303)

def verify_log(log,move,side,air=False):
    identity,entry_address,damage=SPECS[move]
    if air:
        need(move=='square','Only square has this airborne victim fixture')
        damage=27
    need(not re.search(r'Lua error|LUA ERROR|Fatal error|access violation',log,re.I),'Runtime error')
    need(not rows(log,'FAILED'),'Actual failed phase')
    results=rows(log,'RESULT');need(len(results)==1,'One complete terminal record')
    result=results[0]
    need(result['move']==move and result['side']==side and result.get('air')==int(air) and result['writes']==0 and
         result['assistance']=='none' and result['fullPortAcceptance']=='false','Unassisted bounded result')
    for tag,key in [('CSS','css'),('LIVE','live'),('READY','ready'),('COMMAND','command'),
                    ('RECOVERED','recovered'),('FINAL','frame')]:
        events=rows(log,tag);need(len(events)==1 and events[0]['frame']==result[key], 'Actual '+tag+' event')
    need(700<=result['css']<result['live']<result['ready']<=result['command']<result['entry']<
         result['recovered']<result['followup']<result['frame'], 'Actual phase chronology')
    need(result['followup']==result['recovered']+16 and result['frame']==result['followup']+160,
         'Full ordinary follow-up interval')
    fields=rows(log,'FIELD');by={(f['frame'],f['slot']):f for f in fields}
    expected={(f,s)for f in range(result['ready'],result['frame']+1)for s in (1,2)}
    need(len(fields)==len(by)==len(expected) and set(by)==expected,'Every paired actual field')
    owners={n:(by[result['ready'],n]['actor'],by[result['ready'],n]['main'])for n in (1,2)}
    for field in fields:
        n=field['slot'];ident=identity if n==side else 8
        need(field['move']==move and field['side']==side and field['writes']==0 and
             field['assistance']=='none' and field['mode']==2 and field['state']==1 and
             field['id']==field['roster']==ident and field['owner']==field['actor'] and
             (field['actor'],field['main'])==owners[n] and
             0x01000000<=field['actor']<0x01100000 and 0x01000000<=field['main']<0x01100000 and
             0<=field['hp']<=161, 'Actual native character identity, human ownership and health')
    need(all(by[result['ready'],n]['hp']==161 and clean(by[result['ready'],n])for n in (1,2)),
         'Original full-health grounded match ready')
    events=rows(log,'EVENT');entries=[e for e in events if e['entry']==entry_address]
    need(len(entries)==1 and entries[0]['frame']==result['entry'],'Exactly one own native special entry')
    for event in events:
        need((event['actor'],event['main'])==owners[side] and event['a8']==event['actor'] and
             event['a13']==event['main'] and event['id']==identity and event['pc']==event['entry']+16 and
             event['entry'] in (entry_address,0xff861350,0xff861500) and event['writes']==0,
             'Native instruction and actual actor/Main provenance')
    returns=[e for e in events if e['entry']==0xff861350 and
             result['entry']<e['frame']<=result['recovered']]
    need(bool(returns),'Original individual ready handoff after own special')
    need(all(clean(by[result['recovered'],n])for n in (1,2)),'Both actual fighters recover on their own floors')
    health=rows(log,'HEALTH')
    for event in health:
        need(event['slot']==3-side and event['writes']==0 and event['pc']==0xff836700 and
             event['mask']==0xffff and 0<=event['after']<=event['before']<=161,
             'Original collision damage, no health assistance')
    for n in (1,2):
        for frame in range(result['ready'],result['frame']):
            stores=[h for h in health if h['frame']==frame and h['slot']==n]
            before,after=by[frame,n]['hp'],by[frame+1,n]['hp']
            if stores:
                need(stores[0]['before']==before and stores[-1]['after']==after,
                     'Actual collision stores explain adjacent callback health')
                need(all(a['after']==b['before']for a,b in zip(stores,stores[1:])), 'Ordered damage ledger')
            else:need(before==after,'Unexplained health change')
    contacts=[h for h in health if result['entry']<=h['frame']<=result['recovered']]
    actual_damage=sum(h['before']-h['after']for h in contacts)
    need(actual_damage==damage,'Own special contact damage (excludes initial ordinary charged kick)')
    own_poses={by[f,side]['pose']for f in range(result['entry']+1,result['recovered']+1)}
    need(len(own_poses)>=3,'Actual special body animation advances')
    if air:
        need(contacts and all(by[h['frame'],3-side]['y']<by[h['frame'],3-side]['floor']
                             for h in contacts if h['before']!=h['after']),
             'Square-wave hit actually occurs against airborne victim')
    need(all(by[f,side]['hp']==161 for f in range(result['ready'],result['frame']+1)),
         'Passive opponent cannot injure attacker')
    inputs=rows(log,'INPUT');keys={(i['frame'],i['slot'],i['button'])for i in inputs}
    need(len(inputs)==len(keys) and all(i['writes']==0 and i['assistance']=='none'for i in inputs),
         'Actual input inventory without duplicates/assistance')
    command=rows(log,'COMMAND')[0];forward=command['forward'];back='Left'if forward=='Right'else'Right'
    need(command['expectedEntry']==entry_address and forward in ('Left','Right'),'Own command spec')
    plan=[]
    if move in ('knife','ring','blade','choke'):
        plan=[('Down',0,3),(back if move=='knife'else forward,5,3),
              ('High_Punch'if move in ('knife','blade')else'Low_Punch',6,3)]
    elif move=='square':plan=[(forward,0,3),(back,5,3),('High_Punch',6,3)]
    elif move=='ball':plan=[('Low_Kick',0,84)]
    elif move=='bicycle':plan=[(back,0,3),(back,6,3),('Down',12,3),('High_Kick',13,3)]
    elif move in SPECS:
        release=120 if result['profile']=='guard_release'else 0
        plan=[('Down',0,release+result['lead']+36),('High_Punch',release+result['lead'],6)]
        if release:plan.append(('Block',0,release))
    else:raise ValueError('Unknown actual clean uppercut command')
    expected_command={(result['command']+at,side,button)for button,start,hold in plan
                      for at in range(start,start+hold)}
    if air:expected_command|={(result['command']+at,3-side,'Up')for at in range(3)}
    actual_command={key for key in keys if result['command']<=key[0]<result['followup']}
    need(actual_command==expected_command,'Exact real native command inputs, including LK release')
    follow=result['followup']
    expected_follow={(follow+at,side,button)for button,start,hold in
                     [(forward,0,8),('Up',40,3),('High_Punch',112,3)]for at in range(start,start+hold)}
    need({key for key in keys if key[0]>=follow}==expected_follow,'Actual ordinary follow-up inputs')
    walking=[by[f,side]for f in range(follow+1,follow+10)]
    # Square-wave crossings and the leg flip can leave the old command
    # direction pointing AWAY from the opponent. MKII walks backward at
    # two pixels, forward at 2.5; do not mistake a real backwalk for a stall.
    sign=1 if forward=='Right'else -1
    opponent=by[follow,3-side];walker=by[follow,side]
    toward=(opponent['x']-walker['x'])*sign>0
    speed=0x28000 if toward else 0x20000
    velocity=(speed*sign)&0xffffffff
    need(all(by[f,side]['vx']==velocity and by[f,side]['y']==by[f,side]['floor']
             for f in range(follow+3,follow+9)), 'Native forward/back walking responds after special')
    need(all((by[f,side]['x']-by[f-1,side]['x'])*sign in ((2,3)if toward else(2,))
             for f in range(follow+3,follow+9)), 'Actual walk coordinates agree with native velocity')
    need(any(by[f,side]['y']<by[f,side]['floor'] and by[f,side]['vy']!=0
             for f in range(follow+42,follow+65)),'Actual jump responds after special')
    need(any(by[f,side]['action']==0x101 for f in range(follow+114,follow+140)),
         'Original high-punch action responds after landing')
    need(all(clean(by[result['frame'],n])for n in (1,2)),'Both fighters finish follow-up cleanly')
    need(not any(result['command']-120<=row['frame']<result['command']for row in inputs),
         'At least120actual fields of neutral physical input before Down/HP')
    active=[by[f,side]for f in range(result['entry']+1,result['recovered'])if by[f,side]['action']==0x107]
    need(bool(active),'Actual HUMAN uppercut107 action; CPU106 is not its substitute')
    need(any(by[f,3-side]['action']==0x503 and by[f,3-side]['gravity']==0x6000
             for f in range(result['entry']+1,result['recovered'])),'Original uppercut victim trajectory')
    return dict(move=move,side=side,air=air,fields=len(fields),entry=result['entry'],
                recovered=result['recovered'],nativeContactDamage=actual_damage,
                fullPortAcceptance=False)

import argparse
import struct
import verify_ball_register_source_v1837 as current_source
import verify_current_interrupt_v1870 as current_launch

def restore_driver(text):
    old=(ROOT/'mk2ks_human_special_matrix_v3.lua').read_text().rstrip()+'\n'
    text=text.replace("leg={18,0xfff80800},uppercut_kano={17,0xff870dc0},uppercut_sonya={18,0xff870dc0}}","leg={18,0xfff80800}}",1)
    text=text.replace("assert(move=='uppercut_kano'or move=='uppercut_sonya','Dedicated clean ordinary uppercut probe')\n",'',1)
    dump=" if frame==1 then\n  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)\n  local file=assert(io.open(assert(os.getenv('MK2KS_HUMAN_ORDINARY_OUT'))..'/guest_maincpu.bin','wb'));file:write(raw);file:close()\n end\n"
    need(text.count(dump)==1,'One read-only initialized guest dump')
    text=text.replace(dump,'',1).replace('if frame-settle>=120 then','if frame-settle>=30 then',1)
    command="   elseif move=='uppercut_kano'or move=='uppercut_sonya'then\n    pulse(side,'Down',age,0,9);pulse(side,'High Punch',age,6,3)\n"
    need(text.count(command)==1,'One physical ordinary Down/HP command branch')
    text=text.replace(command,'',1)
    need(text.rstrip()+'\n'==old,'All original two-human selection, physical approach and native observers exact except declared ordinary command/neutral interval/read-only dump; EOF whitespace normalized')
    return old

def restore_guard_driver(text):
    original=ROOT/'mk2ks_human_uppercut_clean_v2151.lua'
    need(current_launch.sha(original)=='D73672581E89B0F9070503998C4D28763B0B358E4BDCC7FA0634621FAED178A8','Pinned original clean uppercut driver')
    text=text.replace("uppercut_sonya={18,0xff870dc0},uppercut_liu={1,0xff870dc0},uppercut_subzero={8,0xff870dc0}}","uppercut_sonya={18,0xff870dc0}}",1)
    text=text.replace("assert(move=='uppercut_kano'or move=='uppercut_sonya'or move=='uppercut_liu'or move=='uppercut_subzero','Native guard-transition comparison')","assert(move=='uppercut_kano'or move=='uppercut_sonya','Dedicated clean ordinary uppercut probe')",1)
    for name in ('declared physical guard comparison','read-only native guard/HP dispatch observation'):
        pattern=r'-- BEGIN '+re.escape(name)+r' v2212\.\n[\s\S]*?-- END '+re.escape(name)+r' v2212\.\n'
        need(len(re.findall(pattern,text))==1,'One declared comparison '+name)
        text=re.sub(pattern,'',text,count=1)
    text=text.replace("victim=%s profile=%s lead=%d writes=0 assistance=none %s',tag,frame,move,side,air and 1 or 0,victim_name,profile,lead,text or''","victim=%s writes=0 assistance=none %s',tag,frame,move,side,air and 1 or 0,victim_name,text or''",1)
    text=text.replace("   elseif move=='uppercut_kano'or move=='uppercut_sonya'or move=='uppercut_liu'or move=='uppercut_subzero'then","   elseif move=='uppercut_kano'or move=='uppercut_sonya'then",1)
    pattern=r'    -- BEGIN physical guard-to-uppercut command v2212\.\n[\s\S]*?    -- END physical guard-to-uppercut command v2212\.\n'
    need(len(re.findall(pattern,text))==1,'One physical native guard command')
    text=re.sub(pattern,"    pulse(side,'Down',age,0,9);pulse(side,'High Punch',age,6,3)\n",text,count=1)
    need(text.rstrip()+'\n'==original.read_text().rstrip()+'\n','Only physical guard command, declared native stock comparison IDs and read-only handler observations differ; entire remaining driver exact')
    return restore_driver(original.read_text())

def verify_context(log,meta):
    result=rows(log,'RESULT');need(len(result)==1,'Unique native comparison terminal result');r=result[0]
    move=meta['move'];side=meta['side'];identity=SPECS[move][0]
    for line in log.splitlines():
        if not line.startswith('MK2_HSPECIAL_'):continue
        scope=dict(re.findall(r'(\w+)=([^\s]+)',line))
        need(scope.get('move')==move and scope.get('side')==str(side)and scope.get('profile')==meta['profile']and scope.get('lead')==str(meta['lead'])and scope.get('writes')=='0'and scope.get('assistance')=='none','Every actual native comparison row has exact unassisted scope')
    need(not re.search(r'Lua error|LUA ERROR|Fatal error|access violation',log,re.I),'No observer/runtime errors')
    for tag,key in (('CSS','css'),('LIVE','live'),('READY','ready'),('COMMAND','command')):
        events=rows(log,tag);need(len(events)==1 and events[0]['frame']==r[key],'Actual native '+tag)
    need(700<=r['css']<r['live']<r['ready']<=r['command']<r['frame'],'Native cold selection/live/command chronology')
    fields=rows(log,'FIELD');by={(f['frame'],f['slot']):f for f in fields}
    expected={(frame,n)for frame in range(r['ready'],r['frame']+1)for n in (1,2)}
    need(len(fields)==len(by)==len(expected)and set(by)==expected,'All consecutive physical paired fields')
    owners={n:(by[r['ready'],n]['actor'],by[r['ready'],n]['main'])for n in(1,2)}
    for f in fields:
        identity_n=identity if f['slot']==side else 8
        need(f['id']==f['roster']==identity_n and f['state']==1 and f['mode']==2 and f['owner']==f['actor']and(f['actor'],f['main'])==owners[f['slot']],'True actual human IDs and stable native actor/Main, never proxies')
    need(all(clean(by[r['ready'],n])and by[r['ready'],n]['hp']==161 for n in (1,2)),'Full-health genuine ordinary match ready')
    for event in rows(log,'EVENT')+rows(log,'HANDLER'):
        need(event['id']==identity and(event['actor'],event['main'])==owners[side]and event['a8']==event['actor']and event['a13']==event['main']and event['pc']==event['entry']+16,'Own actual native instruction handler provenance')
    inputs=rows(log,'INPUT');keys={(i['frame'],i['slot'],i['button'])for i in inputs}
    need(len(keys)==len(inputs),'Unique physical inputs')
    need(not any(r['command']-120<=i['frame']<r['command']for i in inputs),'120actual neutral fields before command')
    release=120 if meta['profile']=='guard_release'else 0
    planned={(r['command']+age,side,'Down')for age in range(release+meta['lead']+36)}
    planned|={(r['command']+age,side,'High_Punch')for age in range(release+meta['lead'],release+meta['lead']+6)}
    if release:planned|={(r['command']+age,side,'Block')for age in range(120)}
    stop=r['followup']if r['followup']>0 else r['frame']+1
    need({k for k in keys if r['command']<=k[0]<stop}==planned,'Every exact physical guard/release/HP command field')
    return r,fields,by

def verify_no_activation(log,meta,r,fields,by):
    failed=rows(log,'FAILED')
    need(len(failed)==1 and failed[0]['reason']=='no_activation_or_full_recovery'and r['frame']==r['command']+400,'Exact bounded unactivated native diagnostic')
    need(r['entry']==r['recovered']==r['followup']==-1,'No native entry/recovery promoted from intended inputs')
    need(not rows(log,'HEALTH')and all(f['hp']==161 for f in fields),'Actual unchanged native health, not a claimed hit')
    need(not any(e['entry']==SPECS[meta['move']][1]for e in rows(log,'EVENT'))and not any(f['action']==0x107 for f in fields),'Neither actual uppercut entry nor human107 action occurred')
    need(all(clean(by[r['frame'],n])for n in (1,2)),'Both real humans return naturally to clean stance after the failed input')
    return dict(nativeUppercutAccepted=False,activationObserved=False,entry=-1,nativeContactDamage=0,fullOwnedRecoveryAndFollowupAccepted=False,fields=len(fields))

def verify_case(folder):
    meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/current_source.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    need(meta['candidate']==current_source.NAME and meta['exit_code']==0 and meta['assistance']=='none'and not meta['cheats_enabled'],'Current terminal unassisted ordinary capture')
    need(meta['move']in SPECS and meta['side']in(1,2)and meta['profile']in('neutral','guard_release')and meta['lead']in(6,12,24)and not meta['air']and meta['victim']=='sub_zero','Requested real two-human ordinary match')
    need(meta['executable_sha256']==build['executable_sha256']and meta['payload_sha256']==build['payload_sha256'],'Exact current playable executable/payload')
    need(before==meta['input_hashes']and all(before.get(path)==sha for path,sha in build['input_hashes'].items()),'All actual compiled inputs frozen before/after')
    pins={}
    for path,wanted in before.items():
        need(current_launch.sha(path)==wanted,'Changed actual input '+path);pins[path]=wanted
        if Path(path).suffix in('.lua','.ps1','.json'):
            frozen=folder/'input_sources'/Path(path).name
            need(current_launch.sha(frozen)==wanted,'Changed frozen input '+str(frozen));pins[str(frozen)]=wanted
    source=(folder/'input_sources/mk2ks_guard_uppercut_comparison_v2212.lua').read_text()
    need(not re.search(r':write_|write_u\d+|load_?state|\.value\s*=(?!=)|\bdofile\s*\(|\bload\s*\(',source),'No forced native state or dynamic delegated gameplay')
    restore_guard_driver(source)
    runner=(folder/'input_sources/run_current_guard_uppercut_comparison_v2213.ps1').read_text()
    need('-nocheat'in runner and '-noautoframeskip -frameskip 0'in runner,'Original difficulty/no cheats/full fields')
    guest=(folder/'guest_maincpu.bin').read_bytes()
    need(guest==current_source.expected()[0],'Whole actual initialized current guest independently reconstructed')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(current_launch.sha(ROOT/'mk2/mk2-maincpu.bin')=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23','Exact original native program')
    first=(0xff870dc0-0xff800000)//8;last=(0xff871030-0xff800000)//8
    need(guest[first:last]==original[first:last],'Entire original HUMAN uppercut routine unchanged')
    for address,words in((0xff870e30,(0x1b89,)),(0xff870f50,(0x09c1,0x0107)),(0xff871000,(0xc080,0x73f0,0xff83))):
        at=(address-0xff800000)//8
        need(struct.unpack_from('<'+'H'*len(words),original,at)==words,'Original human animation28/action107/native attack signature')
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    terminal,fields,by=verify_context(log,meta)
    if terminal['entry']>0:
        result=verify_log(log,meta['move'],meta['side']);result.update(nativeUppercutAccepted=True,activationObserved=True,fullOwnedRecoveryAndFollowupAccepted=True)
    else:result=verify_no_activation(log,meta,terminal,fields,by)
    pins.update(current_launch.source_pins())
    for path in folder.rglob('*'):
        if path.is_file():pins[str(path.resolve())]=current_launch.sha(path)
    for path in(Path(__file__),ROOT/'tools/verify_human_special_matrix.py',ROOT/'mk2ks_human_special_matrix_v3.lua'):
        pins[str(path.resolve())]=current_launch.sha(path)
    current_launch.module_pins(pins)
    result.update(passed=True,boundedGuardTransitionContextAccepted=True,move=meta['move'],side=meta['side'],profile=meta['profile'],lead=meta['lead'],humanUppercutAction='0107',
     physicalNeutralFieldsBeforeCommand=120,wholeCurrentGuestAccepted=True,inputHashes=pins,
     fullMoveArtGroundShadowAudioAccepted=False,fullPortAcceptance=False,
     scope='Source-exact real two-human native guard/HP comparison. A bounded no-activation diagnostic is not an accepted move; nativeUppercutAccepted requires full original40damage/trajectory/recovery/ordinary follow-up. Not universal native gameplay/art/audio/arena/CPU/KO or complete port.')
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    need(not args.output.exists(),'Immutable ordinary evidence')
    try:report=verify_case(args.folder)
    except Exception as error:
        import traceback
        report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items()if key!='inputHashes'},indent=2))
    raise SystemExit(0 if report['passed']else 1)
