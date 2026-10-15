"""Actual native impact lifecycle, every component, DMA and rendered pose proof."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

import numpy as np
from PIL import Image

import build_native_projectile_impacts as assets
from verify_restart_lifecycle import verify_projectile_join
from verify_projectile_contact import rows as contact_rows

ROOT=Path(__file__).resolve().parents[1]
PAYLOAD_SHA='c846a1a8a58fa8133d514a2ea831448d017b93fcb4d8cdb7b1b6908801c4d10c'
HEX=set('child process pose action vx vy flags pc graphic command palette color scale_x scale_y descriptor colors position size clip_min clip_max buffer'.split())


def rows(log,tag):
    return [{k:v if k=='snapshot' else int(v,16 if k in HEX else 10) for k,v in re.findall(r'(\w+)=([^\s]+)',line)}
            for line in log.splitlines() if line.startswith('MK2_IMPACT_'+tag+' ')]


def unpack_frame(payload,address):
    return struct.unpack_from('<4hIHI',payload,(address-assets.BASE)//8)


def composite(payload,group,leftward=False):
    frames=[];at=(group-assets.BASE)//8
    while True:
        address=struct.unpack_from('<I',payload,at)[0];at+=4
        if not address:break
        w,h,xo,yo,source,command,palette=unpack_frame(payload,address)
        colors=struct.unpack_from('<64H',payload,(palette-assets.BASE)//8+2)
        bit=(assets.PIXELS*8+source-assets.GFX_DEST*8) if source>=assets.GFX_DEST*8 else (0x1c4000*8+source-0x1e04000*8)
        pixels=np.array([((int.from_bytes(payload[(bit+i*6)//8:(bit+i*6)//8+2],'little')>>((bit+i*6)%8))&63)
                         for i in range(w*h)],dtype=np.uint8).reshape(h,w)
        lut=np.array([[((c>>10)&31)*255//31,((c>>5)&31)*255//31,(c&31)*255//31] for c in colors],dtype=np.uint8)
        frames.append((w,h,xo,yo,lut[pixels],pixels!=0))
    xmin=min(-r[2] for r in frames);ymin=min(-r[3] for r in frames)
    xmax=max(-r[2]+r[0] for r in frames);ymax=max(-r[3]+r[1] for r in frames)
    rgb=np.zeros((ymax-ymin,xmax-xmin,3),dtype=np.uint8);mask=np.zeros(rgb.shape[:2],dtype=bool)
    for w,h,xo,yo,part,opaque in frames:
        x=-xo-xmin;y=-yo-ymin
        rgb[y:y+h,x:x+w][opaque]=part[opaque];mask[y:y+h,x:x+w]|=opaque
    if leftward:rgb=rgb[:,::-1].copy();mask=mask[:,::-1].copy()
    return rgb,mask


def match_image(path,rgb,mask):
    image=np.asarray(Image.open(path).convert('RGB'))
    if image.shape!=(254,400,3):raise ValueError('Rendered proof requires unscaled 400x254 native snapshot')
    ys,xs=np.where(mask);expected=rgb[ys,xs].astype(np.int16)
    # Anchor on a saturated effect color. Matching remains a full-pose check,
    # not a cyan/magenta count or a fixed crop; actual pixels must agree.
    saturation=expected.max(1)-expected.min(1)
    candidates=np.flatnonzero(saturation>=40)
    if len(candidates)==0:return dict(score=0,visible=0,x=0,y=0)
    # Multiple spatially separated anchors are necessary: normal foreground
    # chains or a reacting fighter may cover the rarest single color/pixel.
    anchors=candidates[np.linspace(0,len(candidates)-1,min(12,len(candidates)),dtype=int)]
    origins=set();screen=image.astype(np.int16)
    for anchor in anchors:
        anchor_color=expected[anchor]
        ay,ax=np.where(np.all(np.abs(screen-anchor_color)<=2,axis=2))
        origins.update(zip((ax-int(xs[anchor])).tolist(),(ay-int(ys[anchor])).tolist()))
    best=dict(score=0,visible=0,x=0,y=0)
    sample=np.linspace(0,len(xs)-1,min(64,len(xs)),dtype=int)
    for ox,oy in origins:
        sx=xs[sample]+ox;sy=ys[sample]+oy
        sample_inside=(sx>=0)&(sx<400)&(sy>=28)&(sy<254)
        if sample_inside.sum()<min(20,len(sample)):continue
        if np.all(np.abs(screen[sy[sample_inside],sx[sample_inside]]-expected[sample[sample_inside]])<=2,axis=1).mean()<0.60:continue
        px=xs+ox;py=ys+oy
        inside=(px>=0)&(px<400)&(py>=28)&(py<254)
        visible=int(inside.sum())
        if visible<min(40,len(xs)) or visible<len(xs)*0.45:continue
        actual=image[py[inside],px[inside]].astype(np.int16)
        score=float(np.all(np.abs(actual-expected[inside])<=2,axis=1).mean())
        if score>best['score']:best=dict(score=score,visible=visible,x=ox,y=oy)
    return best


def verify(folder,target,side,payload_path,render=True):
    log=(folder/'run.log').read_text(encoding='utf-8-sig');errors=[];visual=[]
    def check(condition,message):
        if not condition and message not in errors:errors.append(message)
    core=verify_projectile_join(log,target,side,False,impact=True)
    errors+=core.get('errors',[])
    payload=payload_path.read_bytes()
    check(hashlib.sha256(payload).hexdigest()==PAYLOAD_SHA,'Exact converted impact/unchanged prior payload')
    report=json.loads((ROOT/'diagnostic_v292_projectile_impact_payload/roms/mk2ks/mk2ks.impact.json').read_text())
    groups=[int(g['native'],16) for g in report[target]['groups']]
    fields=rows(log,'FIELD');components=rows(log,'COMPONENT');dmas=rows(log,'DMA');culls=rows(log,'CULL')
    contact=contact_rows(log,'EVENT');ef=contact_rows(log,'EFFECT');body=contact_rows(log,'FIELD')
    check(len(rows(log,'CHILD'))==len(rows(log,'RETIRE'))==2,'Exactly two complete observed native effect tasks')
    check(len(fields)==len(ef) and len({(f['frame'],f['child']) for f in fields})==len(fields),'Exact full child-field inventory, including reused native allocation')
    for cycle in (1,2):
        events=[e for e in contact if e['cycle']==cycle]
        child=next(e['child'] for e in events if e['kind']=='child')
        lifetime=[f for f in ef if f['cycle']==cycle]
        traced=[f for f in fields if f['child']==child and lifetime[0]['frame']<=f['frame']<=lifetime[-1]['frame']]
        check([f['frame'] for f in traced]==[f['frame'] for f in lifetime],'Every actual child field has full-component render evidence')
        if render:
            check(all((folder/'snap'/f"impact_{f['frame']}.png").exists() for f in traced),'Every live field has an actual native snapshot')
            flight=[f for f in traced if f['action']==0]
            for pose in dict.fromkeys(f['pose'] for f in flight):
                held=[f for f in flight if f['pose']==pose]
                rgb,mask=composite(payload,pose,bool(held[0]['flags']&16))
                matches=[]
                for frame in range(held[0]['frame'],min(held[0]['frame']+8,held[-1]['frame']+4)):
                    path=folder/'snap'/f'impact_{frame}.png'
                    if path.exists():matches.append(dict(frame=frame,**match_image(path,rgb,mask)))
                best=max(matches,key=lambda x:x['score']) if matches else dict(score=0,visible=0)
                travelling=any(f['vx']!=0 for f in held)
                visual.append(dict(cycle=cycle,phase='flight' if travelling else 'startup_diagnostic',pose=f'{pose:08x}',**best))
                if travelling:
                    check(best['score']>=0.85,'Every executed travelling pose actually renders at native palette/scale/facing')
        hits=[e for e in events if e['kind']=='contact']
        if not hits:
            check(all(f['action']!=0x500 and f['pose'] not in groups for f in traced),'Ducked projectile cannot play a false impact')
            continue
        hit=hits[0];start=hit['frame'];before=next(f for f in lifetime if f['frame']==start)
        active=[f for f in traced if start<f['frame']<=start+4*len(groups)]
        check(len(active)==len(groups)*4,'Every held impact field exists')
        direction=-1 if before['flags']&16 else 1
        victim=next(f for f in body if f['frame']==start and f['slot']==3-side)
        for i,f in enumerate(active):
            pose=groups[i//4];group=report[target]['groups'][i//4]
            check(f['pose']==pose and f['action']==0x500 and f['flags']==before['flags'] and f['id']==(17 if target=='kano' else 18) and f['writes']==0,
                  'Own impact pose order, four-field holds, identity and retained travelling facing')
            check(f['x']==victim['x']-direction*(34 if target=='kano' else 106)+direction*(i*2 if target=='sonya' else 0) and
                  f['y']==before['y']+(72 if target=='kano' else 0) and f['vx']==((direction*0x20000)&0xffffffff if target=='sonya' else 0) and f['vy']==0,
                  'Original victim-relative impact origin and native stopped/slow-drift physics')
            actual=[c for c in components if c['frame']==f['frame'] and c['child']==child]
            check(f['components']==len(group['components']) and len(actual)==len(group['components']),'All native composite components present, including tiny raw particles')
            for index,(c,address) in enumerate(zip(actual,group['components'])):
                w,h,xo,yo,source,command,palette=unpack_frame(payload,address)
                check(c['index']==index and c['descriptor']==address and c['pose']==pose and c['graphic']==source and c['command']==command+(16 if direction<0 else 0) and
                      (c['width'],c['height'],c['dx'],c['dy'])==(w,h,w-xo if direction<0 else xo,yo) and c['writes']==0,'Actual component graphics/dimensions/pivots match independently converted original asset')
                draws=[d for d in dmas if d['frame']==f['frame'] and d['graphic']==source]
                clipped=False
                if not draws:
                    # Require the actual stock reject branch and its native
                    # clip rectangle, not an assumption from a missing image.
                    rejected=[r for r in culls if r['frame']==f['frame'] and r['graphic']==source]
                    if len(rejected)==1:
                        r=rejected[0]
                        def xy(v):return tuple(n-65536 if n>=32768 else n for n in (v&65535,v>>16))
                        x,y=xy(r['position']);lo=xy(r['clip_min']);hi=xy(r['clip_max'])
                        clipped=r['pc']==0xff804580 and r['size']==(h<<16|w) and r['writes']==0 and (x+w<=lo[0] or x>=hi[0] or y+h<=lo[1] or y>=hi[1])
                check(clipped or len(draws)==1 and draws[0]['pc']==0xff804640 and draws[0]['width']==w and draws[0]['height']==h and
                      draws[0]['command']==(0xe012 if direction<0 else 0xe002) and draws[0]['scale_x']==draws[0]['scale_y']==0x100 and draws[0]['writes']==0,
                      'Each visible component reaches native DMA once at original scale/facing; absent draws require proved hardware-row culling')
        if render:
            for index,group in enumerate(groups):
                rgb,mask=composite(payload,group,direction<0)
                # Native draw buffering precedes screen capture by up to two
                # fields. A four-field hold provides complete rendered proof
                # without treating a pre-draw snapshot as a missing effect.
                matches=[]
                for frame in range(start+index*4+1,start+index*4+7):
                    path=folder/'snap'/f'impact_{frame}.png'
                    if path.exists():matches.append(dict(frame=frame,**match_image(path,rgb,mask)))
                best=max(matches,key=lambda x:x['score']) if matches else dict(score=0,visible=0)
                visual.append(dict(cycle=cycle,phase='impact',pose=index,**best))
                check(best['score']>=0.75,'Every complete impact pose is actually rendered with its original effect palette/artwork')
    return dict(passed=not errors,errors=errors,target=target,side=side,visual=visual,
                startup_fidelity_proven=False,
                scope='cold_real_join_native_impact_components_DMA_render_travel_art_contact_physics_not_full_startup_flight_choreography_endings_CPU_audio_or_other_moves')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('--target',choices=('kano','sonya'),required=True);p.add_argument('--side',type=int,choices=(1,2),required=True)
    p.add_argument('--payload',type=Path,default=ROOT/'diagnostic_v293_native_projectile_impacts/roms/mk2ks/mk2ks.mdata');p.add_argument('--no-render',action='store_true')
    a=p.parse_args()
    try:r=verify(a.folder,a.target,a.side,a.payload,not a.no_render)
    except (ValueError,KeyError,IndexError,StopIteration,OSError) as e:r=dict(passed=False,errors=['Malformed/missing impact evidence: '+str(e)])
    print(json.dumps(r,indent=2));raise SystemExit(0 if r['passed'] else 1)
