"""Read-only native snapshot/DMA comparison; reports findings, not acceptance."""
import argparse
import json
import re
import struct
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
HEX = {'actor','main','owner','pose','cache','vx','vy','gravity','body','flags','bank','facing',
       'source','command','palette','pc','cameraXY','worldXY','world2'}

def rows(log, tag):
    output = []
    for line in log.splitlines():
        if not line.startswith('MK2_GROUND_'+tag+' '): continue
        row = dict(re.findall(r'(\w+)=([^\s]+)', line))
        for k,v in list(row.items()):
            if k in {'data','key','file','fighter','colors','scope','assistance','button'}: continue
            if k in HEX: row[k] = int(v,16)
            elif re.fullmatch(r'-?\d+',v): row[k] = int(v)
        output.append(row)
    return output

def decode(dma, buffers):
    key = f"{dma['source']:08X}_{dma['command']:04X}_{dma['width']}_{dma['height']}"
    record = buffers[key]
    raw = bytes.fromhex(record['data'])
    bit = record['offset'] % 8
    w,h,c = dma['width'],dma['height'],dma['command']
    bpp = (c>>12)&7
    def extract(n):
        nonlocal bit
        value = (int.from_bytes(raw[bit//8:bit//8+3], 'little')>>(bit%8))&((1<<n)-1)
        bit += n
        return value
    indices = np.zeros((h,w), dtype=np.uint8)
    for y in range(h):
        pre=post=0
        if c&0x80:
            skip=extract(8);pre=(skip&15)<<((c>>8)&3);post=(skip>>4)<<((c>>10)&3)
        for x in range(pre,max(pre,w-post)):
            value=extract(bpp)
            if x<w: indices[y,x]=value
    return indices

def descriptor_geometry(payload):
    base=0xfe800000;result={}
    for at in range((0xfe823ca0-base)//8,(0xfe8408c0-base)//8-3,2):
        pointer=struct.unpack_from('<I',payload,at)[0]
        if pointer<base or pointer%16 or (pointer-base)//8+14>len(payload):continue
        w,h,xo,yo,source,command=struct.unpack_from('<4hIH',payload,(pointer-base)//8)
        if not (0<w<=100 and 0<h<=200 and -1024<=xo<=1024 and -1024<=yo<=1024 and
                0x10000000<=source<0x1a000000 and command&127==0 and ((command>>12)&7)>=3):continue
        key=(source,w,h)
        if key in result and result[key]!=yo:result[key]=None
        else:result[key]=yo
    return result

def render(dmas, buffers, palettes, fields, parts, cache_rows=(), geometry=None):
    body=np.zeros((512,512,3),dtype=np.uint8)
    bodymask=np.zeros((512,512),dtype=bool)
    masks={1:np.zeros((512,512),dtype=bool),2:np.zeros((512,512),dtype=bool)}
    shadows=np.zeros((512,512),dtype=bool)
    for d in dmas:
        if d['command']&15 != 2: continue
        indices=decode(d,buffers)
        rgb=palettes[d['palette']][indices]
        ys,xs=np.where(indices!=0)
        xs=d['x']+((-xs) if d['command']&16 else xs)
        ys=(d['y']+((-ys) if d['command']&32 else ys))&511
        inside=(xs>=0)&(xs<512)&(ys>=0)&(ys<254)
        source_y,source_x=np.where(indices!=0)
        body[ys[inside],xs[inside]]=rgb[source_y[inside],source_x[inside]]
        bodymask[ys[inside],xs[inside]]=True
        masks[1 if d['palette']==0x200 else 2][ys[inside],xs[inside]]=True
    # Original shadow row DMAs. Imported tagged rows are suppressed by v400.
    for d in dmas:
        if d['command']&15 != 8 or 0x10000000<=d['source']<0x1a000000: continue
        indices=decode(d,buffers)
        ys,xs=np.where(indices!=0)
        xs=d['x']+((-xs) if d['command']&16 else xs)
        ys=(d['y']+((-ys) if d['command']&32 else ys))&511
        inside=(xs>=0)&(xs<512)&(ys>=0)&(ys<254)
        shadows[ys[inside],xs[inside]]=True
    native=np.zeros((512,512),dtype=bool)
    for d in dmas:
        if d['command']&15 != 2 or not 0x10000000<=d['source']<0x1a000000:continue
        slot=1 if d['palette']==0x200 else 2
        matches=[r for r in parts if r['slot']==slot and r['source']==d['source'] and d['frame']<=r['frame']<=d['frame']+2]
        component=min(matches,key=lambda r:abs(r['frame']-(d['frame']+1))) if matches else None
        current=[r for r in cache_rows if r['slot']==slot and r['source']==d['source'] and r['frame']==d['frame']]
        if current:actor=current[0]
        elif component:actor=next(r for r in fields if r['slot']==slot and r['frame']==component['frame'])
        else:continue
        yoff=geometry.get((d['source'],d['width'],d['height'])) if geometry is not None else None
        if yoff is None:
            if component is None:continue
            yoff=component['yoff']
        indices=decode(d,buffers)
        h,w=indices.shape;sh=min(45,max(12,(h+3)//4+1))
        jump=max(0,min(200,actor['floor']-actor['y']))
        if 'cameraXY' in actor:
            signed=lambda value:value-65536 if value>=32768 else value
            ground=actor['stageY']+5+signed(actor['cameraXY']>>16)-signed(actor['worldXY']>>16)
        else:ground=d['y']-(actor['y']-yoff)+actor['stageY']+5
        bottom=ground-3-jump*3//10;top=bottom-sh+1
        for row in range(sh):
            sy=row*(h-1)//(sh-1)
            xs=np.flatnonzero(indices[sy]!=0)
            xs=d['x']+(-xs if d['command']&16 else xs)
            y=top+row
            if 0<=y<512:native[y,xs[(xs>=0)&(xs<512)]]=True
    return body,bodymask,masks,shadows,native

def inspect(folder, shift=None, image_load=None, comparison_folder=None):
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    fields=rows(log,'FIELD');parts=rows(log,'PART');dmas=rows(log,'DMA');snaps=rows(log,'SNAP')
    buffers={r['key']:r for r in rows(log,'GFX')}
    cache_rows=rows(log,'DMA_CACHE')
    geometry=descriptor_geometry((ROOT/'diagnostic_v323_native_shang_morph_payload/roms/mk2ks/mk2ks.mdata').read_bytes())
    palettes={int(r['bank'],16) if isinstance(r['bank'],str) else r['bank']:
              np.array([[int(c[i:i+2],16) for i in (0,2,4)] for c in r['colors'].split(',')],dtype=np.uint8)
              for r in rows(log,'PALETTE')}
    byframe=defaultdict(list)
    for r in dmas:byframe[r['frame']].append(r)
    records=[]
    for snap in snaps:
        path=folder/'snap'/snap['file']
        image=np.asarray(image_load(path) if image_load else Image.open(path).convert('RGB'))
        if image.shape!=(254,400,3):raise ValueError('Native 400x254 image required')
        best=None
        # Whole-body pixel evidence determines the observed display field/offset.
        for frame in range(snap['frame']-4,snap['frame']+1):
            draw=byframe.get(frame,[])
            if not any(d['command']&15==2 for d in draw):continue
            body,mask,slotmasks,shadow,native=render(draw,buffers,palettes,fields,parts,cache_rows,geometry)
            for offset in (range(0,113) if shift is None else [shift]):
                crop=body[:254,offset:offset+400];opaque=mask[:254,offset:offset+400].copy();opaque[:44]=False
                if opaque.sum()<100:continue
                score=float(np.all(image[opaque]==crop[opaque],axis=1).mean())
                if best is None or score>best['score']:
                    best={'score':score,'frame':frame,'shift':offset,'body':crop,'mask':opaque,
                          'slotmasks':{n:m[:254,offset:offset+400] for n,m in slotmasks.items()},
                          'shadow':shadow[:254,offset:offset+400], 'native':native[:254,offset:offset+400], 'draw':draw}
        if best is None:raise ValueError('No body provenance for snapshot '+snap['file'])
        contacts={n:int(np.where(m)[0].max()) if m.any() else None for n,m in best['slotmasks'].items()}
        rec={k:snap[k] for k in ('frame','age','file')}
        rec.update(dmaFrame=best['frame'],xShift=best['shift'],bodyScore=best['score'],opaqueFootRows=contacts)
        if comparison_folder:
            previous=np.asarray(Image.open(comparison_folder/'snap'/snap['file']).convert('RGB'))
            rec['bodyPixelsBitExactBeforeAfter']=bool(np.array_equal(image[best['mask']],previous[best['mask']]))
        # Stock expected full silhouette, excluding the independently decoded bodies.
        stock=best['shadow']&~best['mask'];stock[:44]=False
        rec['stockShadowPixels']=int(stock.sum())
        rec['stockShadowScore']=float(np.all(image[stock]==palettes[0][15],axis=1).mean()) if stock.any() else None
        projected=best['native']&~best['mask'];projected[:44]=False
        rec['nativeShadowPixels']=int(projected.sum())
        rec['nativeShadowScore']=float(np.all(image[projected]==palettes[0][15],axis=1).mean()) if projected.any() else None
        rec['blackRows']={}
        for n in (1,2):
            xs=np.where(best['slotmasks'][n])[1]
            if len(xs)==0:continue
            x0,x1=max(0,int(xs.min())-4),min(400,int(xs.max())+5)
            black=np.all(image==palettes[0][15],axis=2)&~best['mask']
            counts=black[140:240,x0:x1].sum(axis=1)
            ys=np.where(counts>8)[0]+140
            rec['blackRows'][n]={'top':int(ys.min()) if len(ys) else None,'bottom':int(ys.max()) if len(ys) else None,'pixels':int(counts.sum())}
        records.append(rec)
    return {'case':folder.name,'snapshots':len(records),'minimumBodyScore':min(r['bodyScore'] for r in records),
            'xShifts':sorted({r['xShift'] for r in records}), 'minimumStockShadowScore':min(r['stockShadowScore'] for r in records if r['stockShadowScore'] is not None),
            'fields':len(fields),'parts':len(parts),'records':records,'terminal':rows(log,'RESULT')}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('cases',nargs='+');parser.add_argument('--output');parser.add_argument('--shift',type=int)
    args=parser.parse_args();reports=[inspect(ROOT/case,args.shift) for case in args.cases]
    if args.output:
        dest=ROOT/args.output
        if dest.exists():raise ValueError('Refusing overwrite')
        dest.write_text(json.dumps(reports,indent=2)+'\n')
    for report in reports:
        print(json.dumps({k:v for k,v in report.items() if k not in ('records','terminal')}))
        for r in report['records']:
            if r['age'] in (32,140,240,260,380,480):print(json.dumps(r))
