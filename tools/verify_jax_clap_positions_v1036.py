"""Independent normal Dead Pool Jax head-clap table/identity/floor/pixel proof."""
import hashlib
import json
import re
import struct
from pathlib import Path
import numpy as np
from PIL import Image
import verify_rolling_heads_v1014 as heads

ROOT=heads.ROOT
CANDIDATE='diagnostic_v1028_native_jax_clap_grounding'
CASES=tuple(f'audit_v1029_jax_{name}_p{side}_clap_grounding' for name in ('kano','sonya') for side in (1,2))
OUT=ROOT/'audit_v1036_jax_clap_grounding_checked'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def rows(text,prefix):
    return [(m[1],dict(re.findall(r'(\w+)=([^\s]+)',m[2]))) for m in re.finditer(r'^'+prefix+r'_(\w+) (.*)$',text,re.M)]

def expected_guest():
    guest,assets=heads.verify_payload()
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    wanted=bytearray(guest)
    assert wanted[0xfb600:0xfb64c]==b'\xff'*76
    operand=(0xff8c7b50-0xff800000)//8
    table=(0xff8c7ff0-0xff800000)//8
    assert struct.unpack_from('<I',wanted,operand)[0]==0xff8c7ff0
    wanted[0xfb600:0xfb644]=original[table:table+68]
    struct.pack_into('<2I',wanted,0xfb644,0x0005ffa0,0x0004ffa0)
    struct.pack_into('<I',wanted,operand,0xfffdb000)
    return bytes(wanted),assets

def verify(texts=None,check_files=True):
    errors=[];pins={};cases={}
    def need(ok,label):
        if not ok:errors.append(label)
    guest,assets=expected_guest()
    payload=(ROOT/CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
    need(hashlib.sha256(payload).hexdigest().upper()==heads.PAYLOAD,'Exact independently reconstructed prior artwork payload')
    info=json.loads((ROOT/CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
    need(digest(ROOT/CANDIDATE/'mkport_candidate.exe')==info['executable_sha256'],'Matched compiled candidate')
    if texts is None:texts={case:(ROOT/case/'run.log').read_text(encoding='utf-8-sig') for case in CASES}
    need(set(texts)==set(CASES),'Both true characters and physical slots')
    for case,text in texts.items():
        directory=ROOT/case
        result=json.loads((directory/'result.json').read_text(encoding='utf-8-sig'))
        name,side=result['player'],result['victim_slot'];identity=17 if name=='kano' else 18
        need(result['candidate']==CANDIDATE and result['executable_sha256']==info['executable_sha256'] and result['payload_sha256']==heads.PAYLOAD,case+': exact current build')
        need(result['exit_code']==0 and result['killer']=='jax' and result['command']=='fff_lp_release' and result['target_gap']==64 and result['assistance']=='none' and result['cheats_enabled'] is False,case+': genuine unassisted scenario')
        if check_files:
            for filename,wanted in result['input_hashes'].items():
                path=Path(filename);need(path.is_file() and digest(path)==wanted,'Changed input '+filename);pins[filename]=wanted
        need(not re.search(r'\[LUA ERROR\]|fatal error|access violation',text,re.I),case+': no runtime errors')
        stock=rows(text,'MK2_STOCK_HEAD_V921');art=rows(text,'MK2_ROLLING_HEAD_V1003')
        need(all(r['writes']=='0' and r['assistance']=='none' for _,r in stock+art),case+': read-only observers')
        items=lambda tag:[r for t,r in stock if t==tag]
        actions,wraps,stops=items('ACTION'),items('WRAP'),items('RESULT')
        need(len(actions)==len(wraps)==len(stops)==1,case+': one original action and completion')
        if len(actions)!=1 or len(wraps)!=1 or len(stops)!=1:continue
        action=actions[0];start=int(action['frame'])
        need(action['variant']=='1' and action['address']=='FF8C7820' and action['damage']=='322' and action['mode']=='2',case+': actual original primary Jax action')
        live=items('FIRST_LIVE')
        need(len(live)==1 and live[0]['ids']==f'11,{identity}' and live[0]['own']==action['actor'] and live[0]['victim']==action['victim_actor'],case+': true fighter identity/physical ownership')
        collisions=[r for r in items('HEALTH') if r['pc']=='FF836700' and int(r['frame'])<=start]
        writers={'FF836700','FF825930' if side==1 else 'FF825960','FF9DECE0' if side==1 else 'FF9DED10','FF9DEF40' if side==1 else 'FF9DEF70'}
        # A physically held LP can add genuine punches to the uppercuts. Bind
        # the complete original collision-health chain, not an assumed count.
        next_health=161;closed=0;chain=True
        for collision in collisions:
            before,after=int(collision['before']),int(collision['after'])
            chain=chain and before==next_health and 0<=after<before<=161
            next_health=after
            if after==0:closed+=1;next_health=161
        need(all(r['pc'] in writers for r in items('HEALTH')) and chain and closed==2 and len(collisions)>=10 and sum(int(r['before'])-int(r['after']) for r in collisions)==322 and len(items('WIN'))==2,case+': two native collision KOs')
        approach=items('APPROACH');inputs=items('INPUT')
        need(len(approach)==1,case+': native spacing reached')
        if len(approach)==1:
            begin=int(approach[0]['frame']);forward='Left' if side==1 else 'Right'
            pressed={(int(r['frame']),r['button']) for r in inputs if r['slot']==str(3-side)}
            need(60<=int(approach[0]['gap'])<=68 and start==begin+36 and all((begin+age,forward) in pressed for age in (10,18,26)),case+': physical three Forward inputs')
            # A one-field native actor rebuild between rounds is irrelevant
            # to the required >=64-field final LP hold. Observe the entire
            # hold through the actual last KO and release, not across respawn.
            last_ko=max(int(r['frame']) for r in collisions if r['after']=='0')
            need(begin+34-last_ko>=64 and all((frame,'Low_Punch') in pressed for frame in range(last_ko,begin+34)) and (begin+34,'Low_Punch') not in pressed,case+': real Low Punch hold/release')
        first=0xff878d90 if side==1 else 0xff878d30;token='7' if side==1 else '8'
        comparisons=[r for r in items('COMPARE') if int(r['frame'])==start and first<=int(r['table'],16)<=first+32]
        need([int(r['table'],16) for r in comparisons]==[first+i*16 for i in range(3)] and all(r['wanted']==r['actual']==token for r in comparisons) and any(r['table']=='FF878D10' and int(r['frame'])==start for r in items('PARSER')),case+': actual original directional parser accepted')
        table=[r for r in items('TABLE_RETURN') if r['table']=='FFFDB000']
        need(len(table)==1 and table[0]['age']=='54' and table[0]['value']==('0005FFA0' if name=='kano' else '0004FFA0') and table[0]['id']==str(identity) and table[0]['actor']==action['victim_actor'] and table[0]['main']==action['victim_main'],case+': original consumer reads owned position row')
        need(wraps[0]['age']=='188' and int(wraps[0]['frame'])==start+188 and wraps[0]['actor']==action['actor'] and wraps[0]['pc']=='FF8CDC50',case+': original unchanged completion timing')
        need(stops[0]['damage']=='322' and stops[0]['wins']=='2' and stops[0]['frame']=='5198' and int(stops[0]['wrap'])==start+188 and any(r['mode']=='3' and int(r['frame'])>start+188 for r in items('MODE')) and not items('CACHE_OVERWRITE'),case+': native continue without overrun')
        need((directory/'guest_maincpu.bin').read_bytes()==guest,case+': whole guest changes only table relocation/two rows')
        count=struct.unpack_from('<I',payload,0x160008)[0]
        need((directory/'native_death_gfx.bin').read_bytes()==payload[0x164000:0x164000+count],case+': actual owned graphics unchanged')
        own={source:a for source,a in assets.items() if a['fighter']==name and a['kind']=='body'}
        queues={(r['frame'],r['cursor'],r['source']):r for tag,r in art if tag=='QUEUE'}
        dmas=[r for tag,r in art if tag=='DMA' and int(r['source'],16) in own]
        seen=set()
        for dma in dmas:
            asset=own[int(dma['source'],16)];q=queues.get((dma['frame'],dma['cursor'],dma['source']))
            need(q is not None and dma['queue_match']=='1',case+': exact FIFO/DMA binding')
            if q is None:continue
            need(q['id']==str(identity) and q['actor']==q['physical']==q['owner']==action['victim_actor'] and q['main']==action['victim_main'],case+': true physical owned collapse')
            need(q['y']==q['floor'] and int(q['floor'])==int(q['stageY'])-(134 if name=='kano' else 135),case+': no floating in any owned body pose')
            ground=int(q['stageY'])+5+int(q['displayY'])-int(q['cameraY'])-1-(int(q['displayY'])&256)
            need((int(dma['y'])&255)+int(dma['height'])-1==ground and [int(dma['width']),int(dma['height'])]==asset['size'],case+': exact native raster floor and dimensions')
            seen.add(asset['pose'])
        need(seen==set(range(7)) and len(dmas)>100,case+': all seven actual grounded collapse poses')
        dumps={int(r['source'],16):r for tag,r in art if tag=='PALETTE_DUMP'}
        matches=[]
        for tag,snap in art:
            source=int(snap.get('source','0'),16)
            if tag!='POSE_SNAPSHOT' or source not in own:continue
            asset=own[source];dma=next((r for r in dmas if r['frame']==snap['queued_frame'] and int(r['source'],16)==source),None)
            need(dma is not None and int(snap['frame'])==int(snap['queued_frame'])+1,case+': actual presented native field')
            if dma is None:continue
            palette_path=directory/dumps[source]['file'];palette=np.array(struct.unpack('<64I',palette_path.read_bytes()),dtype=np.uint32)
            w,h=asset['size'];at=0x164000+source//8-0x1ec0000
            indices=heads.decode(payload[at:at+(w*h*6+7)//8],w*h).reshape((h,w))
            picture=directory/'snap'/f"head_pose_{snap['actor_pose']}_{snap['frame']}.png"
            match=heads.pixel_match(picture,indices,palette,bool(int(dma['command'],16)&16))
            x=int(dma['x'])-56-(w-1 if int(dma['command'],16)&16 else 0)
            need(match['score']>=0.5 and (match['x'],match['y'])==(x,int(dma['y'])&255),case+': exact presented owned body pixels/position')
            matches.append({'pose':asset['pose'],'snapshot':str(picture),**match})
            pins[str(picture)]=digest(picture);pins[str(palette_path)]=digest(palette_path)
        need({m['pose'] for m in matches}==set(range(7)),case+': actual visual evidence of every collapse pose')
        cases[case]={'nativeWrapAge':188,'ownedBodyDMAs':len(dmas),'pixelMatches':matches,'victim':name,'side':side}
        for filename in ('run.log','result.json','guest_maincpu.bin','native_death_gfx.bin'):
            pins[str(directory/filename)]=digest(directory/filename)
    return {'passed':not errors,'errors':sorted(set(errors)),'cases':cases,'inputHashes':pins,
            'scope':'normal Dead Pool true victims/both slots; Jax primary positions and grounded owned collapse only',
            'allStockFatalitiesAccepted':False,'allArenasAccepted':False,'alternateCostumesAccepted':False,'fullPortAccepted':False}

if __name__=='__main__':
    if OUT.exists():raise ValueError('Preserve verifier evidence')
    report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('cases','inputHashes')},indent=2))
    raise SystemExit(0 if report['passed'] else 1)
