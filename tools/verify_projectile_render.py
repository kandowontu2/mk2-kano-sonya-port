"""Full native component/DMA/palette inventory and original-art bitmap samples.

The optional probe is diagnostic only. Acceptance also requires the independent
real-input lifecycle/field checker; neither claims whole-character completion.
"""
from __future__ import annotations
import argparse
import functools
from collections import defaultdict
import json
import re
import struct
from pathlib import Path

import numpy as np
from PIL import Image

import build_mk2ks_mk3 as animation
import build_native_projectile_choreography as choreography
import build_native_projectile_impacts as impact
import upgrade_ksui_previews as decoder
from verify_projectile_impacts import match_image,rows as render_rows
from verify_projectile_contact import rows as contact_rows
from verify_projectile_choreography import choreography_rows,verify as verify_choreography

ROOT=Path(__file__).resolve().parents[1]
PAYLOAD=ROOT/'diagnostic_v300_native_projectile_choreography/roms/mk2ks/mk2ks.mdata'


@functools.lru_cache(maxsize=1)
def original_source():
    return (ROOT/'mk3/mk3-maincpu.bin').read_bytes(),decoder.load_gfx(ROOT/'mk3')


@functools.lru_cache(maxsize=128)
def parts(payload,group,fighter=None):
    """Decode converted effects or the original body, never screenshot colors."""
    result=[];at=(group-animation.DONOR_TMS_BASE)//8
    while True:
        frame=struct.unpack_from('<I',payload,at)[0];at+=4
        if not frame:break
        if len(result)>=16:raise ValueError('Unterminated native composite')
        if fighter is not None:
            program,gfx=original_source()
            original=frame+0x01000000
            spec=decoder.component_spec(program,original)
            w,h,xo,yo=spec[2:]
            pixels=np.array(impact.decode_indices(gfx,spec),dtype=np.uint8).reshape(h,w)
            colors=np.array([c[:3] for c in decoder.donor_palette(program,fighter)],dtype=np.uint8)
            pal_at=decoder.PALETTE_DESCRIPTORS[fighter]
            words=[0,*struct.unpack_from('<64H',program,pal_at+4)]
            graphic=spec[0]+animation.GFX_REBASE;cmd=spec[1]
        else:
            w,h,xo,yo,source,cmd,palette=struct.unpack_from('<4hIHI',payload,(frame-animation.DONOR_TMS_BASE)//8)
            if cmd!=0x6000:raise ValueError('Effect template is not native full-copy six-bit pixels')
            segments=[(0x1c4000,0x1e04000,struct.unpack_from('<I',payload,0x1c0008)[0]),
                      (0x1e6000,0x1e50000,struct.unpack_from('<I',payload,0x1c1008)[0]),
                      (0x1f4000,0x1e60000,struct.unpack_from('<I',payload,0x1c2008)[0])]
            segment=next((s for s in segments if s[1]*8<=source<(s[1]+s[2])*8),None)
            if segment is None:raise ValueError('Effect graphic outside exact allocated source range')
            bit=segment[0]*8+source-segment[1]*8
            pixels=np.array([((int.from_bytes(payload[(bit+i*6)//8:(bit+i*6)//8+2],'little')>>((bit+i*6)%8))&63)
                             for i in range(w*h)],dtype=np.uint8).reshape(h,w)
            pal=struct.unpack_from('<64H',payload,(palette-animation.DONOR_TMS_BASE)//8+2)
            colors=np.array([decoder.xrgb555(c) for c in pal],dtype=np.uint8)
            words=pal;graphic=source
        result.append(dict(width=w,height=h,xo=xo,yo=yo,rgb=colors[pixels],mask=pixels!=0,frame=frame,
                           indices=pixels,words=words,graphic=graphic,command=cmd))
    if not result:raise ValueError('Empty original composite')
    return result


def composite(payload,group,leftward=False,fighter=None):
    frames=parts(payload,group,fighter)
    xmin=min(-f['xo'] for f in frames);ymin=min(-f['yo'] for f in frames)
    xmax=max(-f['xo']+f['width'] for f in frames);ymax=max(-f['yo']+f['height'] for f in frames)
    rgb=np.zeros((ymax-ymin,xmax-xmin,3),dtype=np.uint8);mask=np.zeros(rgb.shape[:2],dtype=bool)
    for f in frames:
        x=-f['xo']-xmin;y=-f['yo']-ymin;w=f['width'];h=f['height'];opaque=f['mask']
        rgb[y:y+h,x:x+w][opaque]=f['rgb'][opaque];mask[y:y+h,x:x+w]|=opaque
    if leftward:rgb=rgb[:,::-1].copy();mask=mask[:,::-1].copy()
    return rgb,mask


def native_rows(log,tag):
    hexfields={'actor','process','pose','flags','descriptor','graphic','command','pc','palette','color',
               'scale_x','scale_y','lskip','bank'}
    return [{k:v if k=='colors' else int(v,16 if k in hexfields else 10) for k,v in re.findall(r'(\w+)=([^\s]+)',line)}
            for line in log.splitlines() if line.startswith('MK2_RENDER_'+tag+' ')]


@functools.lru_cache(maxsize=1)
def mk2_graphics():
    data=bytearray(0xc00000)
    for base,chips in ((0,(14,14,19,19)),(0x400000,(16,16,20,20)),(0x800000,(17,17,22,22))):
        for lane,chip in enumerate(chips):
            name=f'l1_mortal_kombat_ii_game_rom_{"ug" if lane%2==0 else "uj"}{chip}.{ "ug" if lane%2==0 else "uj"}{chip}'
            source=(ROOT/'mk2'/name).read_bytes()
            if len(source)!=0x100000:raise ValueError('Original MKII graphics chip size changed')
            data[base+lane:base+lane+len(source)*4:4]=source
    return bytes(data)


@functools.lru_cache(maxsize=256)
def native_pixels(source,command,w,h):
    """Ordinary raw/skip T-unit copy pixels, including actual foreground tiles."""
    if source in (0xf000000,0xf002000):
        if command&0xffef!=0xc002 or h!=10:raise ValueError('Unexpected native HUD name draw')
        ui=(ROOT/'roms/mk2ks/mk2ks.ui').read_bytes();colors=struct.unpack_from('<H',ui,6)[0]
        at=8+2*(colors*2+ui[4]*ui[5]);mw,mh=ui[at:at+2]
        fighter=int(source==0xf002000)
        mask=np.frombuffer(ui[at+2+fighter*mw*mh:at+2+(fighter+1)*mw*mh],np.uint8).reshape(mh,mw)[:10]>48
        columns=np.where(mask.any(axis=0))[0];face=mask[:,columns[0]:columns[-1]+1]
        if w!=face.shape[1]+1:raise ValueError('Native HUD name mask width changed')
        program=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
        sw,sh=struct.unpack_from('<HH',program,(0xffa79400-0xff800000)//8)
        source_bit=struct.unpack_from('<I',program,(0xffa79400-0xff800000)//8+8)[0]
        stock=native_pixels(source_bit,0xc002,sw,sh)
        output=np.zeros((10,w),dtype=np.uint8)
        for y in range(10):
            freq=np.bincount(stock[y],minlength=16);freq[[0,1,2,4,12,13,14,15]]=0
            ramp=int(freq.argmax())
            for x in range(w):
                if x<face.shape[1] and face[y,x]:output[y,x]=ramp
                elif x and (face[y,x-1] or (y and face[y-1,x-1])):output[y,x]=2
        return output
    if source>=0x10000000:
        gfx=original_source()[1];cursor=source-animation.GFX_REBASE
    elif source<0x6000000:
        gfx=mk2_graphics();cursor=source
    else:
        payload=PAYLOAD.read_bytes()
        segments=[(0x1c4000,0x1e04000,struct.unpack_from('<I',payload,0x1c0008)[0]),
                  (0x1e6000,0x1e50000,struct.unpack_from('<I',payload,0x1c1008)[0]),
                  (0x1f4000,0x1e60000,struct.unpack_from('<I',payload,0x1c2008)[0])]
        segment=next((s for s in segments if s[1]*8<=source<(s[1]+s[2])*8),None)
        if segment is None:raise ValueError(f'Unsupported foreground graphics source {source:08x}')
        gfx=payload;cursor=segment[0]*8+source-segment[1]*8
    bpp=(command>>12)&7 or 8
    result=np.zeros((h,w),dtype=np.uint8)
    for y in range(h):
        pre=post=0
        if command&0x80:
            skip=decoder.extract_bits(gfx,cursor,255);cursor+=8
            pre=(skip&15)<<((command>>8)&3);post=(skip>>4)<<((command>>10)&3)
        for x in range(pre,max(pre,w-post)):
            value=decoder.extract_bits(gfx,cursor,(1<<bpp)-1);cursor+=bpp
            if x<w:result[y,x]=value
    return result


def palette_at(palettes,draw):
    candidates=[p for p in palettes if p['bank']==(draw['palette']&0x7f00) and
                (p['frame'],p['ordinal'])<=(draw['frame'],draw['ordinal'])]
    if not candidates:raise ValueError('Native DMA has no captured actual palette')
    colors=candidates[-1]['colors'].split(',')
    if len(colors)!=64:raise ValueError('Incomplete actual palette capture')
    return [int(c,16) for c in colors]


def raster_draw(draw,palettes):
    mode=draw['command']&15;w,h=draw['width'],draw['height']
    if draw['scale_x']!=256 or draw['scale_y']!=256 or draw['lskip']!=0:
        raise ValueError('Unsupported scaled/skipped native foreground draw')
    if draw['graphic']>=0x10000000 and mode==8:return None  # Native MK3 shadow-row suppression.
    if mode==12:
        pixels=np.full((h,w),draw['color']&255,dtype=np.uint8);mask=np.ones((h,w),dtype=bool)
    else:
        pixels=native_pixels(draw['graphic'],draw['command'],w,h)
        mask=pixels!=0 if mode in (2,8,10) else np.ones((h,w),dtype=bool)
        if mode in (8,10):pixels=np.where(mask,draw['color']&255,0).astype(np.uint8)
        elif mode not in (2,3):raise ValueError('Unsupported overlapping native draw mode')
    words=palette_at(palettes,draw)
    if pixels.max()>=64:raise ValueError('Overlapping foreground needs an uncaptured palette color')
    lut=np.array([decoder.xrgb555(c) for c in words],dtype=np.uint8);rgb=lut[pixels]
    x=draw['x'];y=draw['y']&511
    if draw['command']&16:rgb=rgb[:,::-1];mask=mask[:,::-1];x-=w-1
    if draw['command']&32:rgb=rgb[::-1];mask=mask[::-1];y-=h-1
    return x,y,rgb,mask


def shadow_layer(draw,source,palettes,all_draws):
    """Project actual native body-bank ownership, not a guessed floor oval."""
    layer=raster_draw(draw,palettes)
    if layer is None:return None
    x,y,rgb,mask=layer;h,w=mask.shape
    ground=y-(source['object_y']-source['part_y'])+source['stage_y']+5
    if not (30<=ground<=510 and 100<=source['stage_y']<=400):return None
    # Transparent pixels can still belong to another component in this same
    # bank. Reconstruct that ownership from every prior actual opaque draw.
    owners=np.zeros((h,w),dtype=bool);bank=draw['palette']&0x7f00
    for prior in all_draws:
        if prior['ordinal']>draw['ordinal']:break
        px=prior['x']-(prior['width']-1 if prior['command']&16 else 0)
        py=(prior['y']&511)-(prior['height']-1 if prior['command']&32 else 0)
        if px+prior['width']<=x or px>=x+w or py+prior['height']<=y or py>=y+h:continue
        raster=raster_draw(prior,palettes)
        if raster is None:continue
        px,py,_,pm=raster;ph,pw=pm.shape
        x0=max(x,px);y0=max(y,py);x1=min(x+w,px+pw);y1=min(y+h,py+ph)
        opaque=pm[y0-py:y1-py,x0-px:x1-px]
        owners[y0-y:y1-y,x0-x:x1-x][opaque]=(prior['palette']&0x7f00)==bank
    height=max(12,min(45,(h+3)//4+1));jump=max(0,min(200,source['floor_y']-source['object_y']))
    bottom=ground-3-jump*3//10;top=bottom-height+1
    projection=owners[np.arange(height)*(h-1)//(height-1)]
    word=palette_at(palettes,dict(draw,palette=0))[15]
    color=np.array(decoder.xrgb555(word),dtype=np.uint8)
    return x,top,np.broadcast_to(color,(height,w,3)),projection


def component_image_check(folder,draw,part,palettes,all_draws,shadow_sources=()):
    """Exact observed position plus independently decoded later native overdraw.

    Expected target pixels come from original assets, not palette RAM or the
    screenshot. Occlusion is accepted only from later actual DMA submissions
    with decoded opaque pixels/colors, never a guessed chain rectangle.
    """
    w,h=part['width'],part['height'];flip=bool(draw['command']&16)
    rgb=part['rgb'][:,::-1].copy() if flip else part['rgb'].copy()
    opaque=part['mask'][:,::-1].copy() if flip else part['mask'].copy()
    x=draw['x']-(w-1 if flip else 0);y=draw['y']&511;page=y//256
    overlay=np.zeros((h,w),dtype=bool)
    banks=np.full((h,w),draw['palette']&0x7f00,dtype=np.uint16)
    source_by={s['ordinal']:s for s in shadow_sources if s['frame']==draw['frame']}
    def apply_layer(layer,bank,is_shadow=False):
        if layer is None:return
        lx,ly,lrgb,lmask=layer;lh,lw=lmask.shape
        x0=max(x,lx);y0=max(y,ly);x1=min(x+w,lx+lw);y1=min(y+h,ly+lh)
        if x0>=x1 or y0>=y1:return
        actual=lmask[y0-ly:y1-ly,x0-lx:x1-lx].copy()
        region_banks=banks[y0-y:y1-y,x0-x:x1-x]
        if is_shadow:actual&=(region_banks!=0x200)&(region_banks!=0x300)
        roi=rgb[y0-y:y1-y,x0-x:x1-x]
        roi[actual]=lrgb[y0-ly:y1-ly,x0-lx:x1-lx][actual]
        region_banks[actual]=bank
        overlay[y0-y:y1-y,x0-x:x1-x]|=actual
    for later in all_draws:
        if later['ordinal']<=draw['ordinal']:continue
        lw,lh=later['width'],later['height']
        lx=later['x']-(lw-1 if later['command']&16 else 0)
        ly=(later['y']&511)-(lh-1 if later['command']&32 else 0)
        # Native VRAM rows wrap at 512, including chains straddling the two
        # pages. A bottom chain segment can therefore overdraw top-page art.
        if lx+lw>x and lx<x+w:
            for offset in (-512,0,512):
                if ly+offset+lh>y and ly+offset<y+h:
                    layer=raster_draw(later,palettes)
                    if layer is not None:
                        ax,ay,ar,am=layer
                        apply_layer((ax,ay+offset,ar,am),later['palette']&0x7f00)
        source=source_by.get(later['ordinal'])
        if source is not None:
            ground=ly-(source['object_y']-source['part_y'])+source['stage_y']+5
            height=max(12,min(45,(lh+3)//4+1));jump=max(0,min(200,source['floor_y']-source['object_y']))
            bottom=ground-3-jump*3//10;top=bottom-height+1
            if lx+lw>x and lx<x+w and bottom+1>y and top<y+h:
                apply_layer(shadow_layer(later,source,palettes,all_draws),0,True)
    py,px=np.where(opaque);sx=px+x-56;sy=py+y-page*256
    inside=(sx>=0)&(sx<400)&(sy>=28)&(sy<254)
    visible=int(inside.sum());unoccluded=int((inside&~overlay[py,px]).sum())
    if not visible:return dict(score=1,visible=0,unoccluded=0,frame=draw['frame'],offscreen=True)
    expected=rgb[py[inside],px[inside]].astype(np.int16);matches=[]
    for frame in range(draw['frame'],draw['frame']+3):
        path=folder/'snap'/f'impact_{frame}.png'
        if not path.exists():path=folder/'snap'/f'choreo_{frame}.png'
        if not path.exists():continue
        bitmap=np.array(Image.open(path).convert('RGB'))
        if bitmap.shape!=(254,400,3):raise ValueError('Native unscaled 400x254 bitmap required')
        actual=bitmap[sy[inside],sx[inside]].astype(np.int16)
        matches.append(dict(frame=frame,score=float(np.all(np.abs(actual-expected)<=2,axis=1).mean())))
    best=max(matches,key=lambda m:m['score']) if matches else dict(score=0,frame=draw['frame'])
    result=dict(**best,visible=visible,unoccluded=unoccluded,overdraw_pixels=visible-unoccluded)
    if best['score']<0.98 and matches:
        path=folder/'snap'/f"impact_{best['frame']}.png"
        if not path.exists():path=folder/'snap'/f"choreo_{best['frame']}.png"
        actual=np.array(Image.open(path).convert('RGB'))[sy[inside],sx[inside]].astype(np.int16)
        wrong=np.flatnonzero(np.any(np.abs(actual-expected)>2,axis=1))
        result['mismatch_sample']=[dict(x=int(sx[inside][i]),y=int(sy[inside][i]),expected=expected[i].tolist(),actual=actual[i].tolist()) for i in wrong[:8]]
    return result


def probe(folder,target,side):
    log=(folder/'run.log').read_text(encoding='utf-8-sig');payload=PAYLOAD.read_bytes()
    report=json.loads((ROOT/'diagnostic_v298_projectile_choreography_payload/roms/mk2ks/mk2ks.choreography.json').read_text())
    impact_report=json.loads((ROOT/'diagnostic_v292_projectile_impact_payload/roms/mk2ks/mk2ks.impact.json').read_text())
    body=choreography_rows(log,'HUMAN');groups=choreography_rows(log,'GROUP');fields=render_rows(log,'FIELD');events=contact_rows(log,'EVENT');visual=[]
    for cycle in (1,2):
        ev=[e for e in events if e['cycle']==cycle]
        first=next(e['frame'] for e in ev if e['kind']=='action')
        end=next(e['frame'] for e in ev if e['kind']=='cleanup')
        actor=next(e['child'] for e in ev if e['kind']=='child')
        for phase,source in [('body',report[target]['body']),('intro',report[target]['intro']),
                             ('flight',report[target]['flight']),('impact',impact_report[target]['groups'])]:
            observations=[h for h in body if h['side']==side and first<h['frame']<first+50] if phase=='body' else [f for f in fields if f['child']==actor and first<f['frame']<=end]
            for index,g in enumerate(source):
                pose=int(g['native'],16);held=[f for f in observations if f['pose']==pose]
                if not held:continue
                # HUMAN.flags is the main task's busy/ready flags, NOT actor
                # facing. The actual native group tap captures actor F0.
                facing=(next(g['flags'] for g in groups if g['body'] and g['group']==pose and first<=g['frame']<first+50)
                        if phase=='body' else held[0]['flags'])
                rgb,mask=composite(payload,pose,bool(facing&16),target if phase=='body' else None)
                # Only a held occurrence and its two-field native buffer lag,
                # not arbitrary future screenshots where the pose might recur.
                occurrence=[held[0]]
                for f in held[1:]:
                    if f['frame']!=occurrence[-1]['frame']+1:break
                    occurrence.append(f)
                matches=[]
                for frame in range(occurrence[0]['frame'],occurrence[-1]['frame']+3):
                    prefix='choreo' if phase=='body' else 'impact';path=folder/'snap'/f'{prefix}_{frame}.png'
                    if path.exists():matches.append(dict(frame=frame,**match_image(path,rgb,mask)))
                best=max(matches,key=lambda m:m['score']) if matches else dict(score=0,visible=0)
                visual.append(dict(cycle=cycle,phase=phase,index=index,pose=f'{pose:08x}',opaque_pixels=int(mask.sum()),**best))
    return dict(scope='diagnostic_template_probe_not_complete_runtime_or_render_acceptance',target=target,side=side,visual=visual)


def verify_render_log(log,folder,target,side,render=True):
    """Full cache/DMA inventory, original palettes and sampled complete poses.

    All native fields/components are checked. Pixel proof samples the first
    occurrence of each held pose in each of the two actual throw lifetimes;
    it is not a claim to compare every bitmap field or unrelated moves.
    """
    errors=[];visual=[];checked=0;culled=0
    def check(ok,label):
        if not ok and label not in errors:errors.append(label)
    payload=PAYLOAD.read_bytes()
    report=json.loads((ROOT/'diagnostic_v298_projectile_choreography_payload/roms/mk2ks/mk2ks.choreography.json').read_text())
    ir=json.loads((ROOT/'diagnostic_v292_projectile_impact_payload/roms/mk2ks/mk2ks.impact.json').read_text())
    phases={int(g['native'],16):phase for phase in ('body','intro','flight') for g in report[target][phase]}
    phases.update({int(g['native'],16):'impact' for g in ir[target]['groups']})
    body=native_rows(log,'BODY');bc=native_rows(log,'BODY_COMPONENT')
    fields=render_rows(log,'FIELD');fc=render_rows(log,'COMPONENT');culls=render_rows(log,'CULL')
    draws=native_rows(log,'DMA');palettes=native_rows(log,'PALETTE')
    shadows=native_rows(log,'SHADOW_SOURCE')
    events=contact_rows(log,'EVENT');effects=contact_rows(log,'EFFECT')
    human=choreography_rows(log,'HUMAN')
    check(bool(draws) and bool(palettes),'Actual complete native DMA and palette capture')
    check(all(row['writes']==0 for row in body+bc+fields+fc+culls+draws+palettes+shadows), 'Read-only body/effect/DMA/palette observation')
    db=defaultdict(list);cb=defaultdict(list);fb=defaultdict(list)
    for d in draws:db[d['frame']].append(d)
    for c in bc:cb[c['frame'],c['actor']].append(c)
    for c in fc:fb[c['frame'],c['child']].append(c)
    for frame,ds in db.items():
        check([d['ordinal'] for d in ds]==list(range(1,len(ds)+1)), 'Every native draw ordinal retained for exact foreground overdraw')
    expected_shadows={(d['frame'],d['ordinal']) for d in draws if 0x10000000<=d['graphic']<0x1a000000 and
                      d['command']&0x008f==0x0082 and 48<=d['height']<=200 and d['width']<=100}
    # Not every copied body source still belongs to a live cache when the
    # write occurs; those copies do not project a floor silhouette. Optional
    # shadow context is usable only for a matching actual native body draw.
    check({(s['frame'],s['ordinal']) for s in shadows}<=expected_shadows and
          len(shadows)==len({(s['frame'],s['ordinal']) for s in shadows}), 'Unique actual body floor-shadow projection inputs')
    draw_by={(d['frame'],d['ordinal']):d for d in draws}
    for s in shadows:
        d=draw_by.get((s['frame'],s['ordinal']))
        check(d is not None and s['graphic']==d['graphic'] and s['id'] in (17,18) and s['side'] in (1,2) and
              0x01000000<=s['actor']<0x01100000 and 0x01000000<=s['process']<0x01100000 and 0<=s['index']<12,
              'Actual own-fighter floor projection source identity and native cache')
    check(len(fields)==len(effects) and len({(f['frame'],f['child']) for f in fields})==len(fields), 'Exact complete child render-field inventory')
    check(len(render_rows(log,'CHILD'))==len(render_rows(log,'RETIRE'))==2,'Two native effect allocations and retirements')
    check(len({(b['frame'],b['actor']) for b in body})==len(body),'Unique actual body render fields')
    used_body=set();used_bc=set();used_fc=set();used_fields=set()
    for cycle in (1,2):
        ev=[e for e in events if e['cycle']==cycle]
        start=next(e['frame'] for e in ev if e['kind']=='action')
        end=next(e['frame'] for e in ev if e['kind']=='cleanup')
        obj=next(e['child'] for e in ev if e['kind']=='child')
        hs=[h for h in human if h['side']==side and start<h['frame']<=start+60 and phases.get(h['pose'])=='body']
        bs=[b for b in body if b['side']==side and start<b['frame']<=start+60]
        check([b['frame'] for b in bs]==[h['frame'] for h in hs], 'All native release/recovery body cache fields observed')
        for b,h in zip(bs,hs):
            check(all(b[k]==h[k] for k in ('frame','actor','process','id','pose','x','y','writes')), 'Body render cache belongs to actual held canonical fighter')
        life=[e for e in effects if e['cycle']==cycle]
        fs=[f for f in fields if f['child']==obj and start<f['frame']<=end]
        check([f['frame'] for f in fs]==[e['frame'] for e in life], 'Every owned child field has full render evidence')
        for f,e in zip(fs,life):
            check(all(f[k]==e[k] for k in ('frame','child','process','id','pose','x','y','vx','vy','flags','writes')), 'Effect render cache matches actual complete child lifecycle')
        hits=[e for e in ev if e['kind']=='contact']
        if hits:
            contact=hits[0]['frame'];before=next(f for f in fs if f['frame']==contact)
            active=[f for f in fs if contact<f['frame']<=end]
            groups=[int(g['native'],16) for g in ir[target]['groups']]
            check(len(active)==4*len(groups) and all(f['pose']==groups[i//4] and f['action']==0x500 and
                  f['flags']==before['flags'] for i,f in enumerate(active)), 'Complete original impact pose order, four-field holds and retained facing')
        else:check(all(f['action']==0 and phases.get(f['pose'])!='impact' for f in fs), 'Duck produces no false native impact artwork')
        sampled=set()
        for phase_body,inventory in ((True,bs),(False,fs)):
            for f in inventory:
                actor=f['actor'] if phase_body else f['child'];frame=f['frame'];pose=f['pose']
                phase=phases.get(pose)
                check(phase is not None and (phase=='body')==phase_body, 'Only original body/startup/travel/impact groups')
                if phase is None:continue
                ps=parts(payload,pose,target if phase_body else None)
                if render:
                    prefix='choreo' if phase_body else 'impact'
                    check((folder/'snap'/f'{prefix}_{frame}.png').exists(), 'Every live body/effect field has an actual native snapshot')
                cs=(cb if phase_body else fb)[frame,actor]
                (used_body if phase_body else used_fields).add((frame,actor))
                check(len(ps)==len(cs)==f['components'], 'Every original native composite component present')
                flip=bool(f['flags']&16);anchors=[];samples=[]
                bootstrap=(target=='sonya' and not phase_body and frame==life[0]['frame'])
                for index,(p,c) in enumerate(zip(ps,cs)):
                    (used_bc if phase_body else used_fc).add((frame,actor,index))
                    check(c['index']==index and c['pose']==pose and c['descriptor']==p['frame'] and
                          c['command']==p['command']+(16 if flip else 0) and
                          (c['width'],c['height'],c['dx'],c['dy'])==(p['width'],p['height'],p['width']-p['xo'] if flip else p['xo'],p['yo']),
                          'Actual complete component descriptor, BPP, facing, dimensions and pivots')
                    # Sonya's allocation buffer is explicitly terminated for
                    # one field; its already-bound bootstrap descriptor is not
                    # a stationary intro and must produce no ring DMA.
                    if bootstrap:
                        check(len(ps)==1 and c['graphic']==0 and not any(d['graphic']==p['graphic'] for d in db[frame]), 'Sonya allocation bootstrap is invisible, not a stationary ring intro')
                        continue
                    check(c['graphic']==p['graphic'], 'Original actual component graphics source')
                    ds=[d for d in db[frame] if d['graphic']==p['graphic'] and (d['command']&15)==2]
                    if not ds:
                        rejected=[r for r in culls if r['frame']==frame and r['graphic']==p['graphic']]
                        valid=False
                        if len(rejected)==1:
                            r=rejected[0]
                            def xy(v):return tuple(n-65536 if n>=32768 else n for n in (v&65535,v>>16))
                            x,y=xy(r['position']);lo=xy(r['clip_min']);hi=xy(r['clip_max'])
                            valid=r['pc']==0xff804580 and r['size']==(p['height']<<16|p['width']) and r['writes']==0 and (x+p['width']<=lo[0] or x>=hi[0] or y+p['height']<=lo[1] or y>=hi[1])
                        check(valid,'Each component reaches native copy DMA once or actual proved culling')
                        culled+=int(valid);continue
                    check(len(ds)==1,'Each component reaches native copy DMA once or actual proved culling')
                    d=ds[0];checked+=1
                    check((d['pc'],d['width'],d['height'],d['command'],d['scale_x'],d['scale_y'],d['lskip'],d['color'])==
                          (0xff804640,p['width'],p['height'],p['command']+(16 if flip else 0)|0x8002,256,256,0,0), 'Exact native component DMA, original scale/copy mode/facing')
                    actual=palette_at(palettes,d)
                    indices=np.unique(p['indices'][p['mask']])
                    check(all((actual[int(i)]&0x7fff)==(p['words'][int(i)]&0x7fff) for i in indices), 'Every used original body/effect palette color reaches actual DMA')
                    # Check complete composite placement, not independent
                    # screenshot searches which could hide displaced parts.
                    anchors.append((d['x']-(p['width']-1 if flip else 0)+c['dx'],(d['y']&511)+c['dy']))
                    samples.append((d,p,index))
                if anchors:check(len(set(anchors))==1,'Every component shares the same actual native composite pivot')
                key=(phase,pose)
                if render and key not in sampled and samples:
                    sampled.add(key);unoccluded=0
                    for d,p,index in samples:
                        image=component_image_check(folder,d,p,palettes,db[frame],shadows)
                        visual.append(dict(cycle=cycle,phase=phase,pose=f'{pose:08x}',component=index,draw_frame=frame,**image))
                        check(image['visible']==0 or image['score']>=0.98, 'Every sampled original component actually renders with decoded native foreground overdraw')
                        unoccluded+=image['unoccluded']
                    check(unoccluded>0, 'Sampled complete pose has visible original artwork, not just occluding foreground')
    check(used_body=={(b['frame'],b['actor']) for b in body}, 'No unexplained body render cache fields')
    check(used_fields=={(f['frame'],f['child']) for f in fields}, 'No unexplained effect render fields')
    check(used_bc=={(c['frame'],c['actor'],c['index']) for c in bc} and len(used_bc)==len(bc), 'Exact body component inventory without extras or duplicates')
    check(used_fc=={(c['frame'],c['child'],c['index']) for c in fc} and len(used_fc)==len(fc), 'Exact effect component inventory without extras or duplicates')
    return dict(passed=not errors,errors=errors,visual=visual,native_component_draws=checked,proved_culls=culled,
                scope='all_cold_release_startup_travel_impact_cache_DMA_palette_fields_and_first_held_pose_component_pixels_each_cycle_not_every_bitmap_or_whole_game')


def verify(folder,target,side,render=True,*,candidate_name='diagnostic_v300_native_projectile_choreography',exe_sha='b67d9fd07b285c5bd186086125b6568bbd2d8fb001e887bb73df353a216d6d20',payload_sha='51bd733de93015db71faa7e5172d68d90832622173d776d1725aeabf27e33e82'):
    core=verify_choreography(folder,target,side,candidate_name=candidate_name,exe_sha=exe_sha,payload_sha=payload_sha)
    try:
        result=verify_render_log((folder/'run.log').read_text(encoding='utf-8-sig'),folder,target,side,render)
    except (ValueError,KeyError,IndexError,StopIteration,OSError) as e:
        result=dict(passed=False,errors=['Malformed/missing native render evidence: '+str(e)],visual=[])
    result['errors']+=core['errors'];result['passed']=not result['errors'];result['choreography']=core
    metadata=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    names={Path(p).name for p in metadata.get('input_hashes',{})}
    required={'mkport_candidate.exe','mk2ks.mdata','mk2ks_projectile_render_probe.lua',
              'mk2ks_projectile_choreography_probe.lua','mk2ks_projectile_impact_probe.lua',
              'mk2ks_join_projectile_probe.lua','mk2ks_projectile_contact.lua','mk2ks_restart_lifecycle.lua',
              'mk2ks_selector_exit_test.lua','run_join_projectile_probe.ps1'}
    if not required<=names or not metadata.get('observer_pass') or metadata.get('scope')!='cold_diagnostic_not_post_ending':
        result['errors'].append('Complete immutable read-only render case launch inventory')
    result['passed']=not result['errors']
    result.update(target=target,side=side,pixel_samples_checked=render,whole_character_integration_complete=False)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path)
    parser.add_argument('--target',choices=('kano','sonya'),required=True);parser.add_argument('--side',choices=(1,2),type=int,required=True)
    parser.add_argument('--diagnostic',action='store_true');parser.add_argument('--no-render',action='store_true')
    args=parser.parse_args()
    result=probe(args.folder,args.target,args.side) if args.diagnostic else verify(args.folder,args.target,args.side,not args.no_render)
    print(json.dumps(result,indent=2));raise SystemExit(0 if args.diagnostic or result['passed'] else 1)
