"""Independent true-ID/table/native-timing/DMA/pixel proof, normal Dead Pool only."""
import hashlib,json,re,struct
from pathlib import Path
import numpy as np
from PIL import Image
import verify_jax_clap_positions_v1036 as prior
import build_native_pit_fall_v2 as colors
import verify_rolling_heads_v1014 as heads

ROOT=prior.ROOT
CANDIDATE='diagnostic_v1048_owned_jax_arm_tables'
OUT=ROOT/'audit_v1051_native_arm_rip_checked'
CASES=tuple(f'audit_v1050_jax_{n}_p{s}_owned_arms' for n in ('kano','sonya') for s in (1,2))
TABLES=(0xff9f57b0,0xff8bef70,0xff8bf790,0xff9a66a0,0xff9a6c10,0xff9a6d90)
OPERANDS=(0xff8bf180,0xff8bf2b0,0xff8be5b0,0xff9a6530,0xff9a6980,0xff9a6a20)
ADDED=((0xfffdcc00,0xfffdcd80),(0x0005ff70,0x0004ff70),
       (0xfffdccc0,0xfffdce40),(0x002d0010,0x0023000c),
       (0x001effee,0x001fffeb),(0x001e0016,0x001f0016))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def off(pointer):return (pointer-0xff800000)//8

def reconstruct():
    payload=(ROOT/CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
    old=(ROOT/prior.CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
    assert digest(ROOT/prior.CANDIDATE/'roms/mk2ks/mk2ks.mdata')==heads.PAYLOAD
    allowed=((0x1c3000,0x1c3800),(0x1c7000,0x1d0000),(0x1d6000,0x1e0000))
    assert len(payload)==len(old)==0x200000
    assert all(a==b or any(lo<=i<hi for lo,hi in allowed) for i,(a,b) in enumerate(zip(payload,old)))
    header=struct.unpack_from('<4s15I',payload,0x1c3000)
    assert header[0]==b'KAR1' and header[1]==0x1c7000 and header[3]==0x1d6000
    assert list(header[5:])==[0x1f40000,0x1c3100,0xfb680,30,20,0x1c3500,0xfb900,120,0x1c3600,0xfb980,96]
    graphics=payload[header[1]:header[1]+header[2]]+payload[header[3]:header[3]+header[4]]
    guest,_=prior.expected_guest();guest=bytearray(guest)
    assert guest[0xfb680:0xfbbe0]==b'\xff'*(0xfbbe0-0xfb680)
    guest[0xfb680:0xfb680+600]=payload[0x1c3100:0x1c3100+600]
    guest[0xfb900:0xfb978]=payload[0x1c3500:0x1c3578]
    guest[0xfb980:0xfb9e0]=payload[0x1c3600:0x1c3660]
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for index,(table,operand) in enumerate(zip(TABLES,OPERANDS)):
        assert struct.unpack_from('<I',guest,off(operand))[0]==table
        at=0xfba00+index*0x50
        guest[at:at+68]=stock[off(table):off(table)+68]
        struct.pack_into('<2I',guest,at+68,*ADDED[index])
        struct.pack_into('<I',guest,off(operand),0xff800000+at*8)
    donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    assets={};descriptor_index=0;group_cursor=0
    counts=((3,2,2,2,2),(3,1,1,2,2))
    arms=((31,90,88,116),(-6,113,58,128),(-44,57,2,105),(-83,91,-24,114),(-97,135,-40,145))
    for fighter,name in enumerate(('kano','sonya')):
        palette=colors.palette(donor,(0x92bbc,0x92cf2)[fighter])
        for kind in ('body','arms'):
            sheet=Image.open(ROOT/f'art_native_arm_rip_v1041/{name}-{kind}-five.png').convert('RGBA')
            alpha=np.asarray(sheet)[:,:,3]>=128
            xs=np.flatnonzero(alpha.any(axis=0));parts=np.split(xs,np.flatnonzero(np.diff(xs)>25)+1)
            assert len(parts)==5
            crops=[]
            for part in parts:
                sub=sheet.crop((int(part[0]),0,int(part[-1])+1,sheet.height))
                box=sub.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
                crops.append(sub.crop(box))
            scale=(134+fighter)/crops[4].height if kind=='body' else 60/crops[1].width
            pointers=[]
            for pose,crop in enumerate(crops):
                width,height=round(crop.width*scale),round(crop.height*scale)
                indices=colors.quantize(crop.resize((width,height),Image.Resampling.LANCZOS),palette)
                if kind=='body':left=-14 if pose==0 else -width//2+3;bottom=139+fighter
                else:left=round((arms[pose][0]+arms[pose][2]-width)/2);bottom=arms[pose][3]
                top=bottom-height;components=counts[fighter][pose] if kind=='body' else 1
                descriptors=[]
                for column in range(components):
                    at=0x1c3100+descriptor_index*20
                    spec=struct.unpack_from('<4hIHIH',payload,at)
                    x0,x1=column*width//components,(column+1)*width//components
                    assert spec[:4]==(x1-x0,height,-left-x0,-top) and spec[5:]==(0x6000,0xff800000+(0xfda00 if fighter==0 else 0xfdb00)*8,0)
                    graphic=spec[4];g=graphic//8-0x1f40000
                    assert 0<=g<len(graphics) and graphic%8==0
                    expected=indices[:,x0:x1]
                    decoded=heads.decode(graphics[g:g+(expected.size*6+7)//8],expected.size).reshape(expected.shape)
                    assert np.array_equal(decoded,expected),'Independently encoded own source raster'
                    pointer=0xff800000+(0xfb680+descriptor_index*20)*8
                    descriptors.append(pointer);descriptor_index+=1
                    assets[graphic]={'fighter':name,'kind':kind,'pose':pose,'size':[x1-x0,height],
                      'indices':decoded,'colors':palette,'descriptor':pointer}
                if kind=='body':
                    pointer=0xff800000+(0xfb900+group_cursor)*8
                    assert struct.unpack_from('<'+str(components+1)+'I',payload,0x1c3500+group_cursor)==tuple(descriptors+[0])
                    group_cursor+=(components+1)*4
                else:pointer=descriptors[0]
                pointers.append(pointer)
            stream=0x1c3600+fighter*48+(0 if kind=='body' else 24)
            assert struct.unpack_from('<6I',payload,stream)==tuple(pointers+[0])
    assert descriptor_index==30 and group_cursor==120
    return bytes(guest),graphics,assets

def pixel_score(picture,indices,palette,dma):
    # Compare at the measured hardware DMA position, clipping only the real
    # viewport. Native actors/blood may occlude pixels; no composited proof.
    pixels=np.asarray(Image.open(picture).convert('RGB'))
    if int(dma['command'],16)&16:indices=indices[:,::-1]
    height,width=indices.shape
    x=int(dma['x'])-56-(width-1 if int(dma['command'],16)&16 else 0);y=int(dma['y'])&255
    x0,y0,x1,y1=max(0,x),max(0,y),min(pixels.shape[1],x+width),min(pixels.shape[0],y+height)
    if x1<=x0 or y1<=y0:return 0.0,0
    tile=indices[y0-y:y1-y,x0-x:x1-x]
    expected=palette[tile]
    mask=(tile!=0)&(np.max(expected,axis=2)-np.min(expected,axis=2)>20)
    count=int(mask.sum())
    if not count:return 0.0,0
    actual=pixels[y0:y1,x0:x1]
    match=np.max(np.abs(actual.astype(int)-expected.astype(int)),axis=2)<=3
    return float(match[mask].mean()),count

def verify(texts=None,check_files=True):
    guest,graphics,assets=reconstruct();errors=[];pins={};cases={}
    def need(ok,label):
        if not ok:errors.append(label)
    build=json.loads((ROOT/CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
    for filename,wanted in build['input_hashes'].items():
        if check_files:need(digest(Path(filename))==wanted,'Build input changed '+filename)
        pins[filename]=wanted
    need(digest(ROOT/CANDIDATE/'mkport_candidate.exe')==build['executable_sha256'],'Matched executable')
    need(digest(ROOT/CANDIDATE/'roms/mk2ks/mk2ks.mdata')==build['payload_sha256'],'Matched payload')
    for case in CASES:
        directory=ROOT/case;result=json.loads((directory/'result.json').read_text(encoding='utf-8-sig'))
        text=texts[case] if texts is not None else (directory/'run.log').read_text(encoding='utf-8-sig')
        name=result['player'];side=result['victim_slot'];fighter=0 if name=='kano' else 1;identity=17+fighter
        need(result['exit_code']==0 and result['candidate']==CANDIDATE and result['executable_sha256']==build['executable_sha256'] and result['payload_sha256']==build['payload_sha256'],'Exact terminal build '+case)
        need(result['assistance']=='none' and not result['cheats_enabled'] and result['killer']=='jax' and result['command']=='bbbb_lp' and result['target_gap']==96,'Physical scenario '+case)
        for filename,wanted in result['input_hashes'].items():
            if check_files:need(digest(Path(filename))==wanted,'Changed evidence input '+filename)
            pins[filename]=wanted
        need(not re.search(r'\[LUA ERROR\]|fatal error|access violation',text,re.I),'Runtime errors '+case)
        stock=prior.rows(text,'MK2_STOCK_HEAD_V921');art=prior.rows(text,'MK2_ROLLING_HEAD_V1003')
        need(all(r['writes']=='0' and r['assistance']=='none' for _,r in stock+art),'Read-only observers '+case)
        items=lambda tag:[r for t,r in stock if t==tag]
        actions,wraps,stops=items('ACTION'),items('WRAP'),items('RESULT')
        need(len(actions)==len(wraps)==len(stops)==1,'One action and completion '+case)
        if len(actions)!=1 or len(wraps)!=1 or len(stops)!=1:continue
        action=actions[0];start=int(action['frame'])
        need(action['variant']=='2' and action['address']=='FF8BE240' and action['damage']=='322','Original secondary action '+case)
        live=items('FIRST_LIVE');need(len(live)==1 and live[0]['ids']==f'11,{identity}' and live[0]['victim']==action['victim_actor'],'True selected fighter '+case)
        collision=[r for r in items('HEALTH') if r['pc']=='FF836700' and int(r['frame'])<=start]
        next_health=161;killed=0;chain=True
        for r in collision:
            before,after=int(r['before']),int(r['after']);chain=chain and before==next_health and 0<=after<before<=161;next_health=after
            if after==0:killed+=1;next_health=161
        need(chain and killed==2 and sum(int(r['before'])-int(r['after']) for r in collision)==322,'Two real collision KOs '+case)
        approach=items('APPROACH');inputs={(int(r['frame']),r['button']) for r in items('INPUT') if r['slot']==str(3-side)}
        need(len(approach)==1,'Reached native spacing '+case)
        if approach:
            begin=int(approach[0]['frame'])
            need(92<=int(approach[0]['gap'])<=100 and start==begin+44 and all((begin+a,'Block') in inputs for a in (10,18,26,34)) and (begin+42,'Low_Punch') in inputs,'Physical BBBB LP '+case)
        comparisons=[r for r in items('COMPARE') if int(r['frame'])==start and 0xff879bd0<=int(r['table'],16)<=0xff879c10]
        need([r['actual'] for r in comparisons]==['1','2','2','2','2'] and all(r['actual']==r['wanted'] for r in comparisons) and any(r['table']=='FF879BB0' for r in items('BUTTON_PARSER')),'Original button parser '+case)
        need(wraps[0]['age']=='147' and int(wraps[0]['frame'])==start+147 and wraps[0]['pc']=='FF8CDC50','Native completion timing '+case)
        need(stops[0]['frame']=='5198' and stops[0]['wins']=='2' and stops[0]['damage']=='322' and int(stops[0]['wrap'])==start+147 and any(r['mode']=='3' and int(r['frame'])>start+147 for r in items('MODE')) and not items('CACHE_OVERWRITE'),'Safe native continue '+case)
        for index in range(6):
            table=f'{0xff800000+(0xfba00+index*0x50)*8:08X}'
            returns=[r for r in items('TABLE_RETURN') if r['table']==table]
            need(bool(returns) and all(r['value']==f'{ADDED[index][fighter]:08X}' and r['id']==str(identity) and r['actor']==action['victim_actor'] for r in returns),'True-ID native table '+str(index)+' '+case)
        need((directory/'guest_maincpu.bin').read_bytes()==guest,'Whole guest ROM changes only owned art/tables '+case)
        need((directory/'native_arm_rip_gfx.bin').read_bytes()==graphics,'Actual initialized packed graphics '+case)
        own={source:a for source,a in assets.items() if a['fighter']==name}
        queues={(r['frame'],r['cursor'],r['source']):r for t,r in art if t=='QUEUE'}
        dmas=[r for t,r in art if t=='DMA' and int(r['source'],16) in own]
        seen=set();arm_actors=set()
        for dma in dmas:
            asset=own[int(dma['source'],16)];q=queues.get((dma['frame'],dma['cursor'],dma['source']))
            need(q is not None and dma['queue_match']=='1','Bound FIFO/DMA '+case)
            if q is None:continue
            need([int(dma['width']),int(dma['height'])]==asset['size'],'Actual dimensions '+case)
            if asset['kind']=='body':
                need(q['id']==str(identity) and q['actor']==q['physical']==q['owner']==action['victim_actor'] and q['main']==action['victim_main'],'True victim body '+case)
                need(q['y']==q['floor'] and int(q['floor'])==int(q['stageY'])-(134+fighter),'Own actor floor '+case)
                ground=int(q['stageY'])+5+int(q['displayY'])-int(q['cameraY'])-1-(int(q['displayY'])&256)
                need((int(dma['y'])&255)+int(dma['height'])-1==ground,'Actual body raster grounding '+case)
            else:arm_actors.add(q['actor'])
            seen.add((asset['kind'],asset['pose']))
        need(seen=={(k,p) for k in ('body','arms') for p in range(5)} and len(arm_actors)==2,'Every body pose and two native detached arms '+case)
        dumps={int(r['source'],16):r for t,r in art if t=='PALETTE_DUMP'};matches=[]
        for tag,snap in art:
            source=int(snap.get('source','0'),16)
            if tag!='POSE_SNAPSHOT' or source not in own:continue
            dma=next((r for r in dmas if r['frame']==snap['queued_frame'] and int(r['source'],16)==source and r['fifo_actor']==snap['actor_pose'].split('_')[0]),None)
            need(dma is not None and int(snap['frame'])==int(snap['queued_frame'])+1,'Presented native field '+case)
            if dma is None:continue
            asset=own[source];palette_path=directory/dumps[source]['file'];raw=np.array(struct.unpack('<64I',palette_path.read_bytes()),dtype=np.uint32)
            palette=np.stack(((raw>>16)&255,(raw>>8)&255,raw&255),axis=1)
            used=np.unique(asset['indices']);used=used[used!=0]
            need(np.max(np.abs(palette[used].astype(int)-asset['colors'][used].astype(int)))<=1,'Actual owned normal palette '+case)
            picture=directory/'snap'/f"head_pose_{snap['actor_pose']}_{snap['frame']}.png"
            score,count=pixel_score(picture,asset['indices'],palette,dma)
            matches.append({'kind':asset['kind'],'pose':asset['pose'],'score':score,'visibleChromaticPixels':count,'picture':str(picture)})
            pins[str(picture)]=digest(picture);pins[str(palette_path)]=digest(palette_path)
        strong={(m['kind'],m['pose']) for m in matches if m['score']>=0.5 and m['visibleChromaticPixels']>=8}
        need(strong=={(k,p) for k in ('body','arms') for p in range(5)},'Actual presented pixels for all ten poses '+case)
        cases[case]={'victim':name,'slot':side,'nativeWrapAge':147,'ownedDMAs':len(dmas),'nativeArmActors':sorted(arm_actors),'pixelMatches':matches}
        for filename in ('run.log','result.json','guest_maincpu.bin','native_arm_rip_gfx.bin'):pins[str(directory/filename)]=digest(directory/filename)
    return {'passed':not errors,'errors':sorted(set(errors)),'cases':cases,'inputHashes':pins,
      'scope':'four real-input normal Dead Pool Jax arm-rip cases, native tables/ten owned poses/true body grounding/continue',
      'regressionsOnThisCandidateAccepted':False,'alternateCostumesAccepted':False,'allArenasAccepted':False,'allStockFatalitiesAccepted':False,'fullPortAccepted':False}

if __name__=='__main__':
    if OUT.exists():raise ValueError('Preserve evidence')
    report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('cases','inputHashes')},indent=2))
    raise SystemExit(0 if report['passed'] else 1)
