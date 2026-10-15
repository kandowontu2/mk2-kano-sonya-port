"""Independent asset/native-input/FIFO/DMA/presented-pixel evidence, scoped only.

Rebuild the intended payload independently; do not trust the encoder report.
Do not accept an exit0 as activation, unshown frames as rendered artwork, or
normal Dead Pool cases as alternate-costume/all-arena/full-port acceptance.
"""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import label
from scipy.signal import correlate
import build_native_death_art_v900 as death
import build_native_pit_fall_v2 as colors

ROOT=death.ROOT
CANDIDATE='diagnostic_v1002_owned_rolling_head_order'
EXE='885B1A50DB68F6806C8A3B32DA329CAA87CCAC7636ADDB3D0283D83850023D1D'
PAYLOAD='56B3D09C3EF398DE8CEDF11832732D3F2AE517A592CACFFDFB3346BDD497C4B9'
CASES=tuple(f'audit_v1004_baraka_{n}_p{s}_owned_rolling_head' for n in ('kano','sonya') for s in (1,2))


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def records(text,prefix):
    rows=[]
    for match in re.finditer(r'^'+re.escape(prefix)+r'_(\w+) (.*)$',text,re.M):
        row=dict(re.findall(r'(\w+)=([^\s]+)',match[2]))
        if prefix=='MK2_STOCK_HEAD_V921':
            header=re.match(r'frame=\d+ victim=(kano|sonya) side=([12]) killer=baraka writes=0 assistance=none ',match[2])
            row['scenarioVictim']=header[1] if header else 'invalid'
            row['scenarioSide']=header[2] if header else 'invalid'
        rows.append((match[1],row))
    return rows


def decode(packed,count):
    # Deliberately independent from the asset encoder and its codec module.
    return np.array([(int.from_bytes(packed[(i*6)//8:(i*6)//8+2],'little')>>(i*6%8))&63
                     for i in range(count)],dtype=np.uint8)


def pack(raw):
    value=bits=0;result=bytearray()
    for index in raw:
        value|=int(index)<<bits;bits+=6
        while bits>=8:
            result.append(value&255);value>>=8;bits-=8
    if bits:result.append(value&255)
    return bytes(result)


def verify_payload(payload=None):
    source=(ROOT/'diagnostic_v978_owned_torso_invariant_blood/roms/mk2ks/mk2ks.mdata').read_bytes()
    if payload is None:payload=(ROOT/CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
    assert hashlib.sha256(source).hexdigest().upper()=='2679C041539C99F917CE1A9AAADAE455859A20DA5F5CC8AF9FB6013DB6A79F79'
    artwork=ROOT/'art_native_rolling_heads_v998/sonya-diagonals-135-225-315.png'
    assert digest(artwork)=='3ABABEDEA62905D75B161DC2D26A8424EEC19280B2A6FB9560D10C57B226E17E'
    donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    assert hashlib.sha256(donor).hexdigest()==death.DONOR_SHA
    wanted=bytearray(source)
    native0=struct.unpack_from('<4hIHIH',source,0x160400+21*20)
    w,h,_,_,graphic,*_=native0
    at=0x164000+graphic//8-0x1ec0000
    target=int(np.count_nonzero(decode(source[at:at+(w*h*6+7)//8],w*h)))
    # Checked visually against actual original MKII seven-pose references.
    for fighter,mapping in ((0,{0:0,1:6,2:3,3:4,4:5,5:2,6:1}),(1,{0:0,1:2,3:4,5:6})):
        for pose,old in mapping.items():
            dest=0x160400+(fighter*14+7+pose)*20
            src=0x160400+(fighter*14+7+old)*20
            wanted[dest:dest+20]=source[src:src+20]
    image=Image.open(artwork).convert('RGBA')
    assert image.size==(2172,724)
    palette=colors.palette(donor,0x92cf2).astype(np.int32)
    append=0x164000+49228
    for cell,pose in enumerate((2,4,6)):
        pixels=np.array(image.crop((cell*724,0,(cell+1)*724,724)))
        labels,count=label(pixels[:,:,3]>=128,np.ones((3,3)))
        areas=np.bincount(labels.ravel());areas[0]=0
        selected=int(areas.argmax());area=int(areas[selected])
        yy,xx=np.where(labels==selected)
        x0,y0,x1,y1=int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1
        crop=pixels[y0:y1,x0:x1].copy()
        crop[:,:,3]=np.where(labels[y0:y1,x0:x1]==selected,255,0)
        factor=(target/area)**0.5
        size=(round((x1-x0)*factor),round((y1-y0)*factor))
        scaled=np.array(Image.fromarray(crop).resize(size,Image.Resampling.LANCZOS))
        distance=((scaled[:,:,:3,None].transpose(0,1,3,2).astype(np.int32)-palette[None,None,1:64,:])**2).sum(axis=3)
        indices=(distance.argmin(axis=2)+1).astype(np.uint8)
        indices[scaled[:,:,3]<128]=0
        packed=pack(indices.ravel())
        assert np.array_equal(decode(packed,indices.size).reshape(indices.shape),indices)
        graphic=(0x1ec0000+append-0x164000)*8
        dest=0x160400+(21+pose)*20
        struct.pack_into('<4hIHIH',wanted,dest,*size,size[0]//2,size[1]//2,graphic,0x6000,0xfffed800,0)
        end=(append+len(packed)+3)&~3
        assert source[append:end]==b'\xff'*(end-append)
        wanted[append:append+len(packed)]=packed
        wanted[append+len(packed):end]=b'\0'*(end-append-len(packed))
        append=end
    struct.pack_into('<I',wanted,0x160008,append-0x164000)
    assert bytes(wanted)==payload,'Whole payload differs from independently reconstructed intention'
    # Whole original guest from the hash-pinned accepted current build. Only
    # the twelve rotating-head descriptors are allowed to change in this ROM.
    baseline=ROOT/'audit_v979_cage_kano_p1_owned_torso/guest_maincpu.bin'
    checkpoint=json.loads((ROOT/'audit_v995_owned_torso_blood_checkpoint/checkpoint.json').read_text())
    assert digest(baseline)==checkpoint['inputHashes'][str(baseline)]
    guest=bytearray(baseline.read_bytes())
    guest[0xfaa00:0xfaa00+560]=payload[0x160400:0x160400+560]
    by_source={}
    for fighter,name in enumerate(('kano','sonya')):
        for index in range(14):
            at=0x160400+(fighter*14+index)*20
            w,h,xo,yo,graphic,command,palette,pad=struct.unpack_from('<4hIHIH',payload,at)
            kind='body' if index<7 else 'head';pose=index%7
            by_source[graphic]=dict(fighter=name,kind=kind,pose=pose,size=[w,h],offset=[xo,yo],
                                   descriptor=f'{0xff800000+(0xfaa00+(fighter*14+index)*20)*8:08X}')
    return bytes(guest),by_source


def pixel_match(path,indices,palette,flip):
    if flip:indices=indices[:,::-1]
    template=palette[indices]
    r,g,b=template>>16,template>>8&255,template&255
    maximum=np.maximum.reduce([r,g,b]);minimum=np.minimum.reduce([r,g,b])
    meaningful=(indices>0)&(maximum>40)&(maximum-minimum>10)
    picture=np.asarray(Image.open(path).convert('RGB'),dtype=np.uint32)
    actual=picture[:,:,0]<<16|picture[:,:,1]<<8|picture[:,:,2]
    matches=np.zeros((actual.shape[0]-template.shape[0]+1,actual.shape[1]-template.shape[1]+1))
    for rgb in np.unique(template[meaningful]):
        matches+=correlate((actual==rgb).astype(float),(meaningful&(template==rgb)).astype(float),mode='valid',method='fft')
    y,x=np.unravel_index(matches.argmax(),matches.shape)
    return dict(score=float(matches[y,x])/int(meaningful.sum()),x=int(x),y=int(y),pixels=int(meaningful.sum()))


def verify(texts=None,check_files=True):
    errors=[];pins={};summaries={}
    def need(ok,label):
        if not ok:errors.append(label)
    payload=(ROOT/CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
    try:guest,by_source=verify_payload(payload)
    except (AssertionError,ValueError) as error:
        return dict(passed=False,errors=['Independent payload reconstruction: '+str(error)],fullPortAccepted=False)
    need(hashlib.sha256(payload).hexdigest().upper()==PAYLOAD,'Matched intended payload')
    need(digest(ROOT/CANDIDATE/'mkport_candidate.exe')==EXE,'Unchanged matched native binary')
    if texts is None:texts={case:(ROOT/case/'run.log').read_text(encoding='utf-8-sig') for case in CASES}
    need(set(texts)==set(CASES),'Both real added victims in both physical slots')
    for case,text in texts.items():
        directory=ROOT/case;result=json.loads((directory/'result.json').read_text(encoding='utf-8-sig'))
        name=result['player'];side=result['victim_slot'];identity=17 if name=='kano' else 18
        need(result['candidate']==CANDIDATE and result['executable_sha256']==EXE and result['payload_sha256']==PAYLOAD,
             case+': exact matched current candidate')
        need(result['exit_code']==0 and result['killer']=='baraka' and result['command']=='bbbb_hp' and
             result['target_gap']==64 and result['winner_slot']==3-side and result['seconds']==95 and
             result['assistance']=='none' and result['cheats_enabled'] is False,case+': cold physical-only scenario')
        if check_files:
            for filename,wanted in result['input_hashes'].items():
                path=Path(filename);need(path.is_file() and digest(path)==wanted,'Frozen input changed: '+filename);pins[filename]=wanted
        need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',text,re.I),case+': no runtime errors')
        rows=records(text,'MK2_STOCK_HEAD_V921')
        need(all(r['writes']=='0' and r['assistance']=='none' and r['scenarioVictim']==name and r['scenarioSide']==str(side)
                 for tag,r in rows),case+': read-only observations of exact scenario')
        def items(tag):return [r for t,r in rows if t==tag]
        actions=items('ACTION');wraps=items('WRAP');stops=items('RESULT')
        need(len(actions)==len(wraps)==len(stops)==1,case+': one genuinely activated and completed original action')
        if len(actions)!=1 or len(wraps)!=1 or len(stops)!=1:continue
        action,wrap,stop=actions[0],wraps[0],stops[0];start=int(action['frame'])
        need(action['damage']=='322' and action['mode']=='2' and action['actor']!=action['victim_actor'] and
             action['main']!=action['victim_main'],case+': distinct native actor/main owners')
        live=items('FIRST_LIVE')
        need(len(live)==1 and live[0]['ids']==f'3,{identity}' and live[0]['own']==action['actor'] and
             live[0]['victim']==action['victim_actor'],case+': Baraka against true Kano/Sonya, no proxy')
        writers={0xff836700,0xff825930 if side==1 else 0xff825960,
                 0xff9dece0 if side==1 else 0xff9ded10,0xff9def40 if side==1 else 0xff9def70}
        collisions=[]
        for row in items('HEALTH'):
            need(int(row['pc'],16) in writers,case+': only original health writers')
            if row['pc']=='FF836700' and int(row['frame'])<=start:
                need(0<=int(row['after'])<=int(row['before'])<=161,case+': original collision damage bounds')
                collisions.append(row)
        need(len(collisions)==10 and sum(int(r['before'])-int(r['after']) for r in collisions)==322 and
             sum(r['after']=='0' for r in collisions)==2 and len(items('WIN'))==2,case+': two real KOs')
        approach=items('APPROACH');inputs=items('INPUT')
        need(len(approach)==1,case+': reached real native spacing')
        if len(approach)==1:
            beginning=int(approach[0]['frame']);back='Right' if side==1 else 'Left'
            need(60<=int(approach[0]['gap'])<=68 and start==beginning+44,case+': native spacing and input latency')
            need(all(any(int(r['frame'])==beginning+age and r['slot']==str(3-side) and r['button']==button
                         for r in inputs) for age,button in ((10,back),(18,back),(26,back),(34,back),(42,'High_Punch'))),
                 case+': actual four Back taps followed by HP')
            need(all(any(int(r['frame'])==beginning+age and r['slot']==str(3-side) and r['button']=='Block' for r in inputs)
                     for age in range(10,42)) and not any(int(r['frame'])==beginning+42 and r['button']=='Block' for r in inputs),
                 case+': real Block-held directions and release for HP')
        # The native parser first rejects a different High-Punch command.
        # Bind the four accepted comparisons to the original BBBB table,
        # not every comparison of every attempted command in this field.
        comparisons=[r for r in items('COMPARE') if int(r['frame'])==start and
                     0xff87aa00<=int(r['table'],16)<=0xff87aa30]
        need([int(r['table'],16) for r in comparisons]==[0xff87aa00+i*16 for i in range(4)] and
             all(r['wanted']==r['actual']=='8' and r['pc']=='FF8777A0' for r in comparisons) and
             [int(r['tick']) for r in comparisons]==[int(comparisons[0]['tick'])-i*8 for i in range(4)] and
             any(r['table']=='FF87A980' and int(r['frame'])==start for r in items('PARSER')),
             case+': exact original BBBB command parser accepted')
        need(int(wrap['age'])==174 and int(wrap['frame'])==start+174 and wrap['pc']=='FF8CDC50' and wrap['actor']==action['actor'],
             case+': unchanged original Baraka completion')
        need(stop['frame']=='5198' and stop['damage']=='322' and stop['wins']=='2' and int(stop['action'])==start and
             int(stop['wrap'])==start+174 and any(r['mode']=='3' and int(r['frame'])>start+174 for r in items('MODE')),
             case+': terminal real continue screen')
        need(not items('CACHE_OVERWRITE') and not any(r['mode']=='0' and int(r['frame'])>600 for r in items('MODE')),
             case+': no overrun/reset after native action')
        need([int(r['age']) for r in items('DISPLAY')]==list(range(0,601,10)),case+': complete real display chronology')
        need((directory/'guest_maincpu.bin').read_bytes()==guest,case+': entire guest only intended head descriptors changed')
        count=struct.unpack_from('<I',payload,0x160008)[0]
        need((directory/'native_death_gfx.bin').read_bytes()==payload[0x164000:0x164000+count],case+': actual initialized graphics equal intended assets')
        art=records(text,'MK2_ROLLING_HEAD_V1003')
        need(all(r['writes']=='0' and r['assistance']=='none' for tag,r in art),case+': read-only native art observer')
        own={source:a for source,a in by_source.items() if a['fighter']==name}
        queues=[r for t,r in art if t=='QUEUE' and int(r['source'],16) in own]
        dmas=[r for t,r in art if t=='DMA' and int(r['source'],16) in own]
        fifo={(r['frame'],r['cursor'],r['source']):r for r in queues}
        seen={'head':set(),'body':set()};first={'head':{},'body':{}}
        body_ground=0
        for row in dmas:
            source=int(row['source'],16);asset=own[source]
            q=fifo.get((row['frame'],row['cursor'],row['source']))
            need(q is not None and row['queue_match']=='1',case+': exact current-field FIFO/DMA binding')
            if q is None:continue
            need(q['id']==str(identity) and q['physical']==action['victim_actor'] and q['main']==action['victim_main'] and
                 q['owner']==q['physical'] and row['fifo_actor']==q['actor'] and row['fifo_physical']==q['physical'] and
                 row['fifo_main']==q['main'] and row['fifo_pose']==q['pose'],case+': physical true-ID native art ownership')
            need([int(row['width']),int(row['height'])]==asset['size'] and
                 int(row['palette'],16)==int(q['bank'],16)&0x7f00 and
                 int(row['command'],16)==int(q['command'],16)>>16,case+': native dimensions/command/palette bank')
            if asset['kind']=='head':
                need(q['actor']!=q['physical'] and q['cache']==asset['descriptor'],case+': native detached head and exact own descriptor')
            else:
                need(q['actor']==q['physical'] and int(q['pose'],16)==death.GROUPS[name][asset['pose']] and q['y']==q['floor'],
                     case+': physical headless body uses original collapse group/floor')
                ground=int(q['stageY'])+5+int(q['displayY'])-int(q['cameraY'])-1-(int(q['displayY'])&256)
                need((int(row['y'])&255)+int(row['height'])-1==ground,case+': all collapse poses on native raster floor')
                body_ground+=1
            seen[asset['kind']].add(asset['pose']);first[asset['kind']].setdefault(asset['pose'],int(row['frame'])-start)
        need(seen=={'head':set(range(7)),'body':set(range(7))} and len(queues)==len(dmas) and body_ground>100,
             case+': all seven actual head rotations and body poses rendered')
        snapshots=[r for t,r in art if t=='POSE_SNAPSHOT' and int(r['source'],16) in own]
        dumps={int(r['source'],16):r for t,r in art if t=='PALETTE_DUMP' and int(r['source'],16) in own}
        need(len(snapshots)==14 and len(dumps)==14,case+': every body/head pose has actual picture and hardware palette')
        donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
        words=struct.unpack_from('<64H',donor,(0x92bbc if name=='kano' else 0x92cf2)+4)
        rgb=[0]+[((((v>>10&31)<<3)|(v>>12&7))<<16)|((((v>>5&31)<<3)|(v>>7&7))<<8)|(((v&31)<<3)|(v>>2&7)) for v in words[:63]]
        matches=[]
        for snap in snapshots:
            source=int(snap['source'],16);asset=own[source];dump=dumps.get(source)
            need(dump is not None,case+': actual source hardware palette binding')
            if dump is None:continue
            palette_path=directory/dump['file']
            need(palette_path.is_file() and palette_path.stat().st_size==256,case+': actual64-pen palette bytes')
            if not palette_path.is_file():continue
            palette=np.array(struct.unpack('<64I',palette_path.read_bytes()),dtype=np.uint32)
            need(palette[1:].tolist()==rgb[1:],case+': exact original owned normal costume RGB pens')
            need(int(snap['frame'])==int(snap['queued_frame'])+1,case+': snapshot after actual native presentation')
            path=directory/'snap'/f"head_pose_{snap['actor_pose']}_{snap['frame']}.png"
            need(path.is_file() and Image.open(path).size==(400,254),case+': actual presented pose picture')
            if not path.is_file():continue
            w,h=asset['size'];at=0x164000+source//8-0x1ec0000
            indices=decode(payload[at:at+(w*h*6+7)//8],w*h).reshape((h,w))
            dma=next((r for r in dmas if r['frame']==snap['queued_frame'] and r['source']==snap['source']),None)
            need(dma is not None,case+': exact snapshot DMA field')
            if dma is None:continue
            match=pixel_match(path,indices,palette,bool(int(dma['command'],16)&16))
            need(match['score']>=0.5,case+': actual presented encoded '+asset['kind']+' pose'+str(asset['pose']))
            matches.append(dict(kind=asset['kind'],pose=asset['pose'],snapshot=str(path),**match))
            if check_files:pins[str(path)]=digest(path);pins[str(palette_path)]=digest(palette_path)
        for age in range(0,601,10):
            path=directory/'snap'/f'stock_head_{start}_{age:03d}.png'
            need(path.is_file() and Image.open(path).size==(400,254),case+': periodic actual scene '+str(age))
            if check_files and path.is_file():pins[str(path)]=digest(path)
        need(dmas and max(int(r['frame']) for r in dmas)<4198,case+': custom native art retires before long continuation')
        summaries[case]=dict(victim=name,slot=side,damage=322,nativeWrapAge=174,
                             headPoses=sorted(seen['head']),bodyPoses=sorted(seen['body']),firstPoseAges=first,
                             ownedDMAs=len(dmas),groundedBodyDMAs=body_ground,
                             hardwarePaletteDumps=len(dumps),posePictures=len(snapshots),periodicPictures=61,pixelMatches=matches)
        if check_files:
            for filename in ('run.log','result.json','guest_maincpu.bin','native_death_gfx.bin'):
                path=directory/filename;pins[str(path)]=digest(path)
    for filename in ('mk2ks_stock_head_victim_v921.lua','mk2ks_rolling_head_display_v1003.lua'):
        need(not re.search(r'\bp:write_|\.value\s*=(?!=)|load_state|loadstate',(ROOT/filename).read_text()),'Read-only physical observer: '+filename)
    return dict(passed=not errors,errors=sorted(set(errors)),cases=summaries,inputHashes=pins,
                normalDeadPoolBarakaNativeRollingHeadRuntimeAccepted=not errors,
                sourceRotationsManuallyReviewed=True,actualPresentationManuallyReviewed=False,
                alternateCostumesAccepted=False,allStockFatalitiesAccepted=False,allArenasAccepted=False,fullPortAccepted=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    if args.output.exists():raise ValueError('Preserve verification evidence')
    report=verify();args.output.mkdir();(args.output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    compact={k:v for k,v in report.items() if k not in ('cases','inputHashes')}
    compact['cases']={k:{a:b for a,b in v.items() if a!='pixelMatches'} for k,v in report.get('cases',{}).items()}
    print(json.dumps(compact,indent=2));raise SystemExit(0 if report['passed'] else 1)
