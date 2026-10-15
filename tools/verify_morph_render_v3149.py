"""Every added morph hold and early normal-body handoff against original art.

Actual copy DMA and RGB555 palette writes are checked independently of PNGs.
PNGs must match at the fixed native two-field display-buffer delay, not a
search through arbitrary later screenshots. No full-game/release claim.
"""
import argparse
from collections import defaultdict
import functools
import hashlib
import json
import re
import struct
from pathlib import Path

import numpy as np
from PIL import Image
import build_native_shang_morphs as assets
import build_mk2ks_mk3 as animation
import build_native_projectile_impacts as pixels
import upgrade_ksui_previews as decoder
import verify_projectile_render as raster
import verify_human_shang_v3148 as human

ROOT=Path(__file__).resolve().parents[1]
PAYLOAD=ROOT/human.CANDIDATE/'roms/mk2ks/mk2ks.mdata'
SCOPE='every_added_forward_reverse_morph_component_hold_and_early_body_palette_handoff_both_facings_fixed_native_buffer_delay_not_all_game_art_audio_or_release'
HEX={'actor','main','pose','flags','task_flags','body','descriptor','graphic','command','pc','bank','palette','color','scale_x','scale_y','lskip'}


def rows(log,tag):
    return [{k:v if k in ('colors','phase') else int(v,16 if k in HEX else 10)
             for k,v in re.findall(r'(\w+)=([^\s]+)',line)}
            for line in log.splitlines() if line.startswith('MK2_MORPH_RENDER_'+tag+' ')]


@functools.lru_cache(maxsize=1)
def references():
    payload=PAYLOAD.read_bytes();program,gfx=raster.original_source();parts={}
    if hashlib.sha256(payload).hexdigest().upper()!=human.PAYLOAD:raise ValueError('Exact native morph asset payload required')
    for fi,target in enumerate(('kano','sonya')):
        first=animation.frame_group(program,assets.SOURCE_GROUPS[target][0],0xff800000,0xffffffff)[0]
        palette_at=animation.stock_file(animation.u32(program,animation.stock_file(first)+14))
        count=animation.u16(program,palette_at);words=struct.unpack_from(f'<{count}H',program,palette_at+2)
        for gi,group in enumerate(assets.SOURCE_GROUPS[target]):
            native=assets.address(assets.GROUPS+(fi*3+gi)*12);items=[]
            for ci,descriptor in enumerate(animation.frame_group(program,group,0xff800000,0xffffffff)):
                spec=decoder.component_spec(program,descriptor);w,h,xo,yo=spec[2:]
                indices=np.frombuffer(pixels.decode_indices(gfx,spec),np.uint8).reshape(h,w)
                ndesc=assets.address(assets.FRAMES+(fi*6+gi*2+ci)*20)
                nw,nh,nx,ny,source,cmd,pal=struct.unpack_from('<4hIHI',payload,(ndesc-assets.BASE)//8)
                if (nw,nh,nx,ny,cmd)!=(w,h,xo,yo,0x6000):raise ValueError('Exact converted native morph descriptor required')
                items.append(dict(frame=ndesc,width=w,height=h,xo=xo,yo=yo,indices=indices,
                    mask=indices!=0,rgb=np.array([decoder.xrgb555(c) for c in words],np.uint8)[indices],
                    words=words,graphic=source,command=cmd))
            parts[native]=items
    return parts


def stance_parts(group,target,alternate):
    parts=raster.parts(PAYLOAD.read_bytes(),group,target)
    if not alternate:return parts
    descriptor={'kano':0x092c3e,'sonya':0x092d74}[target]
    program,_=raster.original_source();words=[0,*struct.unpack_from('<64H',program,descriptor+4)]
    lut=np.array([decoder.xrgb555(c) for c in words],np.uint8)
    return [dict(p,words=words,rgb=lut[p['indices']]) for p in parts]


@functools.lru_cache(maxsize=32)
def stock_parts(group):
    program=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();items=[]
    at=(group-0xff800000)//8
    first=struct.unpack_from('<I',program,at)[0]
    palette=struct.unpack_from('<I',program,(first-0xff800000)//8+14)[0]
    pal=(palette-0xff800000)//8;count=struct.unpack_from('<H',program,pal)[0]
    words=struct.unpack_from(f'<{count}H',program,pal+2)
    lut=np.array([decoder.xrgb555(c) for c in words],np.uint8)
    for i in range(16):
        descriptor=struct.unpack_from('<I',program,at+i*4)[0]
        if not descriptor:break
        w,h,xo,yo,source,cmd=struct.unpack_from('<4hIH',program,(descriptor-0xff800000)//8)
        indices=raster.native_pixels(source,cmd,w,h)
        items.append(dict(frame=descriptor,width=w,height=h,xo=xo,yo=yo,indices=indices,
            mask=indices!=0,rgb=lut[indices],words=words,graphic=source,command=cmd))
    return items


def bitmap_check(folder,draw,part,palettes,all_draws):
    """No screenshot-derived expected colors and no unconstrained alignment."""
    flip=bool(draw['command']&16);w,h=part['width'],part['height']
    rgb=part['rgb'][:,::-1].copy() if flip else part['rgb'].copy()
    mask=part['mask'][:,::-1].copy() if flip else part['mask'].copy()
    x=draw['x']-(w-1 if flip else 0);y=draw['y']&511;page=y//256
    overlay=np.zeros((h,w),bool)
    by_source={p['graphic']:p for ps in references().values() for p in ps}
    for later in all_draws:
        if later['ordinal']<=draw['ordinal']:continue
        lx=later['x']-(later['width']-1 if later['command']&16 else 0)
        ly=(later['y']&511)-(later['height']-1 if later['command']&32 else 0)
        if lx+later['width']<=x or lx>=x+w:continue
        for wrap in (-512,0,512):
            if ly+wrap+later['height']<=y or ly+wrap>=y+h:continue
            source=by_source.get(later['graphic'])
            if source:
                ind=source['indices'];m=ind!=0
                words=raster.palette_at(palettes,later)
                lr=np.array([decoder.xrgb555(v) for v in words],np.uint8)[ind]
                if later['command']&16:lr=lr[:,::-1];m=m[:,::-1]
                layer=(lx,ly,lr,m)
            else:layer=raster.raster_draw(later,palettes)
            if layer is None:continue
            ax,ay,lr,lm=layer;ay+=wrap;lh,lw=lm.shape
            x0=max(x,ax);y0=max(y,ay);x1=min(x+w,ax+lw);y1=min(y+h,ay+lh)
            if x0>=x1 or y0>=y1:continue
            opaque=lm[y0-ay:y1-ay,x0-ax:x1-ax]
            rgb[y0-y:y1-y,x0-x:x1-x][opaque]=lr[y0-ay:y1-ay,x0-ax:x1-ax][opaque]
            overlay[y0-y:y1-y,x0-x:x1-x]|=opaque
    py,px=np.where(mask);sx=px+x-56;sy=py+y-page*256
    inside=(sx>=0)&(sx<400)&(sy>=28)&(sy<254)
    path=folder/'snap'/f"choreo_{draw['frame']+2}.png"
    if not path.is_file():return dict(score=0,visible=0,unoccluded=0,error='Missing exact buffer-delayed native bitmap')
    bitmap=np.array(Image.open(path).convert('RGB'))
    if bitmap.shape!=(254,400,3):raise ValueError('Native unscaled 400x254 bitmap required')
    actual=bitmap[sy[inside],sx[inside]].astype(np.int16)
    expected=rgb[py[inside],px[inside]].astype(np.int16)
    score=float(np.all(np.abs(actual-expected)<=2,axis=1).mean()) if len(actual) else 0
    wrong=np.flatnonzero(np.any(np.abs(actual-expected)>2,axis=1))
    return dict(score=score,visible=int(inside.sum()),unoccluded=int((inside&~overlay[py,px]).sum()),
        bitmap_frame=draw['frame']+2,mismatches=[dict(x=int(sx[inside][i]),y=int(sy[inside][i]),expected=expected[i].tolist(),actual=actual[i].tolist()) for i in wrong[:4]])


def verify_log(log,folder,target,side,render=True):
    errors=[];visual=[];checked=0
    def need(ok,label):
        if not ok and label not in errors:errors.append(label)
    base=human.verify_log(log,target,side,'native');errors.extend(base['errors'])
    body=rows(log,'BODY');components=rows(log,'COMPONENT');draws=rows(log,'DMA');palettes=rows(log,'PALETTE');windows=rows(log,'WINDOW')
    need([w['phase'] for w in windows]==['forward','reverse'],'Actual forward/reverse capture windows')
    need(all(r.get('writes')==0 for r in body+components+draws+palettes+windows),'Read-only full drawing observation')
    need(bool(draws) and bool(palettes),'Actual native DMA/palette evidence')
    db=defaultdict(list);cb=defaultdict(list)
    for d in draws:db[d['frame']].append(d)
    for c in components:cb[c['frame'],c['actor']].append(c)
    for ds in db.values():need([d['ordinal'] for d in ds]==list(range(1,len(ds)+1)),'No omitted native draw ordinals')
    refs=references();groups=sorted(g for g in refs if (g<0xff0c4120)==(target=='kano'))
    # Three composites * four holds in each direction. All are checked, not
    # merely the clearest first occurrence of each pose.
    morph=[b for b in body if b['pose'] in groups]
    need(len(morph)==24,'Every original transition hold in both directions')
    for phase,order in [('forward',groups),('reverse',groups[::-1])]:
        held=[b for b in morph if b['phase']==phase]
        need([b['pose'] for b in held]==[g for g in order for _ in range(4)],'Original group order and four-field holds')
    identity=17 if target=='kano' else 18
    handoffs=[b for b in body if b['phase']=='forward' and b['id']==identity]
    need(len(handoffs)>=8,'Early actual own-body palette/floor handoff fields')
    restored=[b for b in body if b['phase']=='reverse' and b['id']==6]
    need(len(restored)>=8,'Early actual restored-Shang palette/floor handoff fields')
    inventory=morph+handoffs[:8]+restored[:8]
    for b in inventory:
        ps=refs[b['pose']] if b['pose'] in refs else stock_parts(b['pose']) if b['id']==6 else stance_parts(b['pose'],target,bool(b['body']&0x40))
        cs=cb[b['frame'],b['actor']];flip=bool(b['flags']&16);anchors=[]
        need(len(ps)==len(cs)==b['components'],'Full original composite inventory')
        need(all(c['main']==b['main'] and c['pose']==b['pose'] for c in cs),'Component cache belongs to actual morph actor/process')
        for index,(p,c) in enumerate(zip(ps,cs)):
            need(c['index']==index and c['descriptor']==p['frame'] and c['graphic']==p['graphic'] and c['command']==p['command']+(16 if flip else 0) and (c['width'],c['height'],c['dx'],c['dy'])==(p['width'],p['height'],p['width']-p['xo'] if flip else p['xo'],p['yo']),'Exact native original pixels/descriptor/dimensions/pivots/facing')
            ds=[d for d in db[b['frame']] if d['graphic']==p['graphic'] and d['command']&15==2]
            need(len(ds)==1,'Exactly one native copy for every original component field')
            if len(ds)!=1:continue
            d=ds[0];checked+=1
            need((d['pc'],d['command'],d['width'],d['height'],d['scale_x'],d['scale_y'],d['lskip'],d['color'])==(0xff804640,p['command']+(16 if flip else 0)|0x8002,p['width'],p['height'],256,256,0,0),'Native full-scale component copy DMA')
            actual=raster.palette_at(palettes,d);used=np.unique(p['indices'][p['mask']])
            need(all((actual[int(i)]&0x7fff)==(p['words'][int(i)]&0x7fff) for i in used),'All used original morph/body colors reach actual DMA palette')
            anchors.append((d['x']-(p['width']-1 if flip else 0)+c['dx'],(d['y']&511)+c['dy']))
            if render:
                image=bitmap_check(folder,d,p,palettes,db[b['frame']])
                visual.append(dict(phase=b['phase'],kind='transition' if b['pose'] in refs else 'body_handoff',pose=f"{b['pose']:08X}",component=index,draw_frame=b['frame'],**image))
                need(image['visible']>0 and image['unoccluded']>0 and image['score']==1.0,'Every original opaque component pixel matches at exact two-field native buffer delay')
        need(len(set(anchors))==1,'Actual components share one native composite pivot')
    return dict(passed=not errors,errors=errors,target=target,side=side,transition_fields=len(morph),handoff_fields=min(8,len(handoffs)),restored_handoff_fields=min(8,len(restored)),native_component_fields=checked,visual=visual,scope=SCOPE,whole_character_integration_complete=False)


def verify(folder,target,side,render=True,*,candidate=human.CANDIDATE,exe_sha=human.EXE):
    proof=verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),folder,target,side,render)
    provenance=human.verify(folder,target,side,'native',candidate=candidate,exe_sha=exe_sha);proof['errors'].extend(provenance['errors'])
    frozen=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    if not any(Path(p).name=='mk2ks_morph_render_probe.lua' for p in frozen):proof['errors'].append('Exact render observer launch input')
    probe=(folder/'input_sources/mk2ks_morph_render_probe.lua').read_text()
    if re.search(r':write_|\.value\s*=(?!=)|loadstate|load_state',probe):proof['errors'].append('Render observer cannot force guest state')
    proof['passed']=not proof['errors'];return proof


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('case',type=Path);parser.add_argument('target',choices=['kano','sonya']);parser.add_argument('side',type=int,choices=[1,2]);parser.add_argument('--output',type=Path)
    parser.add_argument('--candidate',default=human.CANDIDATE);parser.add_argument('--exe-sha',default=human.EXE)
    args=parser.parse_args();proof=verify(args.case,args.target,args.side,candidate=args.candidate,exe_sha=args.exe_sha)
    if args.output:
        if args.output.exists():raise SystemExit('Refusing to overwrite proof')
        args.output.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps({k:v for k,v in proof.items() if k!='visual'},indent=2));raise SystemExit(not proof['passed'])

