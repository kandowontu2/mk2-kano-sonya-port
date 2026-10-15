"""Bind a fresh mirror-match display transition to real actor caches and DMA.

This bounded fixture proves who is blocking and who finishes the bicycle miss.
It does not claim general animation, tower, sound or complete-port acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

import numpy as np
from PIL import Image

import upgrade_ksui_previews as graphics
import build_mk2ks_mk3 as builder
import verify_cpu_followup_v545 as paired

ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'audit_v571_sonya_native_display_transition'
HEX={'actor','main','pose','list','facing','palette','body','source','command','pc','a8','a13'}

def parse(log,kind):
    rows=[]
    for line in log.splitlines():
        if not line.startswith('MK2_VISUAL_'+kind+' '):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        if len({k for k,v in pairs})!=len(pairs):raise ValueError('Duplicate visual field')
        rows.append({k:v if k in ('colors','phase') else int(v,16 if k in HEX else 10)for k,v in pairs})
    return rows

def pal_rgb(word):
    # MAME's palette expands five bits by bit replication, not floor(255*x/31).
    return tuple(((word>>shift)&31)*8+(((word>>shift)&31)>>2) for shift in (10,5,0))

def frame_template(dmas,actors,gfx):
    colors={a['palette']: [(0,0,0,0)]+[(*pal_rgb(int(v,16)),255)for v in a['colors'].split(',')[1:]] for a in actors}
    canvas=Image.new('RGBA',(512,256))
    for d in dmas:
        part=graphics.decode_component(gfx,colors[d['palette']],d['source']-0x10000000,d['command'],d['width'],d['height'])
        if d['command']&0x10:part=part.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if d['command']&0x20:part=part.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        x=d['x']-d['width']+1 if d['command']&0x10 else d['x']
        y=d['y']&255
        canvas.alpha_composite(part,(x,y))
    return np.asarray(canvas)

def pixel_fit(template,png):
    """Exact native scanout translation; no searching/scaling/pose substitution."""
    target=np.asarray(png.convert('RGB'),dtype=np.int16)
    if png.size!=(400,254):return dict(ratio=0.0,dx=-56,dy=0,pixels=0)
    yy,xx=np.nonzero(template[:,:,3])
    expected=template[yy,xx,:3].astype(np.int16)
    sx,sy=xx-56,yy
    keep=(sx>=0)&(sx<400)&(sy>=0)&(sy<254)
    good=np.all(target[sy[keep],sx[keep]]==expected[keep],axis=1)
    return dict(ratio=float(good.mean())if len(good)else 0.0,dx=-56,dy=0,pixels=int(keep.sum()))

def ordinary_groups(payload,indices=(0,1,2,3,4,9)):
    """Read only the actual native stance/walk/turn dispatch scripts."""
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    spans=builder.sequence_spans(original,builder.LIU_MAIN,builder.LIU_BLOCK,(builder.LIU_MAIN,builder.LIU_SPECIAL))
    groups=set()
    for index in indices:
        script=struct.unpack_from('<I',payload,0x104000+index*4)[0]
        off=(script-0xfe800000)//8
        length=(spans[index][1]-spans[index][0])//8
        for at in range(off,off+length-3,2):
            ptr=struct.unpack_from('<I',payload,at)[0]
            if 0xff02d000<=ptr<0xff040000 and ptr&15==0:
                group_off=(ptr-0xfe800000)//8
                first=struct.unpack_from('<I',payload,group_off)[0]
                if 0xfeb00000<=first<0xfec00000 and first&15==0:groups.add(ptr)
    return groups

def check(log,payload,donor,gfx,images):
    errors=[]
    def need(ok,label):
        if not ok and label not in errors:errors.append(label)
    actors,parts,dmas,screens=(parse(log,t)for t in ('ACTOR','PART','DMA','SCREEN'))
    need(len(actors)==128 and len({(a['frame'],a['side'])for a in actors})==128,'All 64 consecutive paired actor samples')
    need([s['frame']for s in screens]==list(range(1960,1976)) and all(s['phase']=='done'for s in screens),'All 16 consecutive frame-done snapshots')
    need(all(r['writes']==0 for rows in (actors,parts,dmas,screens)for r in rows),'Read-only visual provenance')
    for a in actors:
        side=a['side'];frame=a['frame']
        need((a['actor'],a['main'],a['list'],a['palette'],a['body']&0x40)==
             ((0x01034e90,0x0106a370,0x0105ed30,0x0202,0) if side==1 else (0x010350a0,0x0106bf30,0x0105f230,0x0303,0x40)),
             'Actual independent CPU/human display-list and palette ownership')
        offset=0x92cf2 if side==1 else 0x92d74
        expected=[0]+list(struct.unpack_from('<63H',donor,offset+4))
        need([int(v,16)for v in a['colors'].split(',')]==expected,'Exact independent normal/alternate donor palette in native RAM')
        at=(a['pose']-0xfe800000)//8
        group=[]
        for ix in range(8):
            ptr=struct.unpack_from('<I',payload,at+ix*4)[0]
            if not ptr:break
            off=(ptr-0xfe800000)//8
            w,h,dx,dy,source,cmd=struct.unpack_from('<HHhhIH',payload,off)
            if a['facing']&0x10:dx=w-dx
            if a['facing']&0x20:dy=h-dy
            group.append(dict(source=source,width=w,height=h,dx=dx,dy=dy,command=(cmd&~0x30)|(a['facing']&0x30)))
        observed=[p for p in parts if p['frame']==frame and p['side']==side]
        need(len(observed)==len(group) and [p['part']for p in observed]==list(range(len(group))),'Every native cached component is sampled')
        need(all(all(p[k]==v for k,v in g.items())for p,g in zip(observed,group)),'Exact ROM composite-to-owned-cache descriptors, offsets and flip bits')
        draw=[d for d in dmas if d['frame']==frame and d['palette']==a['palette']]
        if frame<1991: # The terminal callback requests exit before another draw.
            need(len(draw)==len(observed) and all(d['source']==p['source'] and d['width']==p['width'] and d['height']==p['height'] and d['command']==(p['command']|0x8002) for d,p in zip(draw,observed)),
                 'Every owned cached component reaches native DMA without added Y flip')
        if side==2 and 1960<=frame<=1975:
            need(a['action']==0x700 and a['y']==81 and a['facing']&0x20==0 and a['pose']in(0xff02f180,0xff02f1e0,0xff02f240),'Human remains grounded in actual upright standing-block poses')
    cpu={a['frame']:a for a in actors if a['side']==1}
    need(cpu[1961]['action']==0x611 and cpu[1961]['pose']==0xfe83ec40 and cpu[1962]['y']==81 and cpu[1962]['pose']==0xfe83ec40,'Actual final cycling pose and native first landed field')
    allowed=ordinary_groups(payload)
    need(bool(allowed) and all(cpu[f]['action']==0x303 and cpu[f]['y']==81 and cpu[f]['facing']&0x20==0 and cpu[f]['pose']in allowed for f in range(1963,1971)),
         'CPU publishes ordinary upright movement on next scheduled animation tick')
    setups=paired.flag_rows(log)
    for kind,pc,at,after in (('body',0xff838cf0,0x01034ff0,0x16),('flags',0xff877d50,0x0106a580,0x10)):
        need(any(r['frame']==1970 and r['slot']==1 and r['kind']==kind and r['pc']==pc and r['at']==at and r['after']==after and r['a8']==0x01034e90 and r['a13']==0x0106a370 for r in setups),
             'New original owned high-punch setup after ordinary recovery')
    punch=ordinary_groups(payload,(19,))
    need(bool(punch)and all(cpu[f]['pose']in punch and cpu[f]['action']==0x303 and cpu[f]['body']&4 and cpu[f]['y']==81 for f in range(1971,1976)),
         'Later CPU high-punch poses belong to the real ordinary dispatch and new native lock')
    if errors:
        return dict(passed=False,errors=errors,fullPortAcceptance=False,
                    scope='Invalid display provenance; do not infer rendered acceptance')
    fits=[]
    for f in range(1960,1976):
        # Double-buffered scanout displays the previous native draw field.
        df=f-1
        template=frame_template([d for d in dmas if d['frame']==df],[a for a in actors if a['frame']==df],gfx)
        fit=pixel_fit(template,images[f]);fits.append(dict(frame=f,draw_field=df,**fit))
        need(fit['ratio']==1.0 and fit['pixels']>=3000,'Whole visible composite pixels match previous-field native DMA and own palette')
    need(all((p['dx'],p['dy'])==(-56,0)for p in fits),'One unchanged native scanout translation across all 16 frames')
    return dict(passed=not errors,errors=errors,actor_fields=len(actors),frame_done_images=len(screens),pixel_matches=fits,
                exact_visible_body_pixels=sum(f['pixels']for f in fits),cpu_first_upright_cache_field=1963,cpu_first_upright_rendered_field=1964,
                finding='Green normal-palette P1 CPU finishes bicycle; white alternate-palette P2 human blocks upright. No persistent inverted human block in this capture.',
                scope='one_natural_Sonya_mirror_grab_bicycle_miss_transition_not_all_animations_or_full_port',fullPortAcceptance=False)

def verify(folder=CASE):
    proof=paired.verify(folder,'sonya','bicycle')
    if not proof['passed']:return dict(passed=False,errors=proof['errors'])
    payload=(ROOT/paired.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    if hashlib.sha256(donor).hexdigest().upper()!='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651':raise ValueError('Original donor changed')
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    observer=(folder/'input_sources/mk2ks_cpu_recovery_visual_probe_v2.lua').read_text()
    if re.search(r':write_|\.value\s*=(?!=)|load_state|loadstate',observer):raise ValueError('Display observer may not mutate guest state')
    images={f:Image.open(folder/'snap'/f'done_{f}.png')for f in range(1960,1976)}
    result=check(log,payload,donor,graphics.load_gfx(ROOT/'roms/mk2ks'),images)
    result['paired_followup']=proof
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args();proof=verify()
    if args.output:
        if args.output.exists():raise SystemExit('Refusing to overwrite evidence')
        args.output.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(proof,indent=2));raise SystemExit(0 if proof['passed']else 1)
