"""Read-only whole-DMA floor diagnostic; no game/asset edits or acceptance claim.

Reconstructs the actual command ordering, including native foreground copies
after imported shadows. A caller must independently bind the displayed field
and validate the native-style projection/ground contact before acceptance.
"""
import argparse
import json
import re
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image

HEX={'source','command','palette','pc','actor','main','owner','cache','pose','bank','body','facing','start','control','tap','address','at','value','mask'}
STR={'fighter','assistance','colors','file','phase','scope','key','data','human','cpu','time','palette_file'}


def data(folder):
    groups=defaultdict(list)
    serial=0
    with (Path(folder)/'run.log').open(encoding='utf-8-sig')as stream:
        for line in stream:
            match=re.match(r'MK2_NAT_CAMPAIGN_(FLOOR_\w+) ',line)
            if not match:continue
            row=dict(re.findall(r'(\w+)=([^\s]+)',line))
            for k,v in row.items():
                if k not in STR:row[k]=int(v,16 if k in HEX else 10)
            if match[1]=='FLOOR_DMA':serial+=1;row['serial']=serial
            if match[1]=='FLOOR_SNAP':row['serial']=serial
            groups[match[1]].append(row)
    buffers={r['key']:r for r in groups['FLOOR_GFX']}
    palettes={r['ref']:np.array([[int(c[i:i+2],16)for i in (0,2,4)]for c in r['colors'].split(',')],dtype=np.uint8)
              for r in groups['FLOOR_PALETTE']}
    draws=defaultdict(list)
    for r in groups['FLOOR_DMA']:draws[r['frame']].append(r)
    owners=defaultdict(list)
    for r in groups['FLOOR_OWNER']:owners[(r['frame'],r['source'],r['slot'])].append(r)
    return groups,buffers,palettes,draws,owners


def decoder(buffers):
    @lru_cache(maxsize=8192)
    def decode(source,command,w,h):
        key=f'{source:08X}_{command:04X}_{w}_{h}'
        record=buffers[key];raw=bytes.fromhex(record['data']);bit=record['offset']%8
        bpp=(command>>12)&7 or 8
        pixels=np.zeros((h,w),dtype=np.uint8)
        def extract(count):
            nonlocal bit
            if bit+count>len(raw)*8:raise ValueError('Graphics observation exhausted')
            value=(int.from_bytes(raw[bit//8:bit//8+2],'little')>>(bit%8))&((1<<count)-1)
            bit+=count
            return value
        for y in range(h):
            pre=post=0
            if command&0x80:
                skip=extract(8);pre=(skip&15)<<((command>>8)&3);post=(skip>>4)<<((command>>10)&3)
            for x in range(pre,max(pre,w-post)):
                value=extract(bpp)
                if x<w:pixels[y,x]=value
        return pixels
    return decode


def renderer(buffers,palettes,draws,owners,legacy_labels=False):
    decode=decoder(buffers)
    def render(frame,cutoff=None,carry=0,page=0):
        color=np.zeros((512,512,3),dtype=np.uint8)
        banks=np.full((512,512),-1,dtype=np.int32)
        known=np.zeros((512,512),dtype=bool)
        body=np.zeros((512,512),dtype=np.uint8)
        projected=np.zeros((512,512),dtype=bool)
        shadow=np.zeros((512,512),dtype=bool)
        body_owners={}
        relevant=[d for f in range(frame-carry,frame+1)for d in draws[f]if cutoff is None or d['serial']<=cutoff]
        for d in relevant:
            if d['slot']:
                found=owners[(d['frame'],d['source'],d['slot'])]
                if found:body_owners[d['slot']]=found[-1]
        protected={a['bank']&0x7f00 for a in body_owners.values()}
        for d in relevant:
            source,c,w,h=d['source'],d['command'],d['width'],d['height']
            port=0x10000000<=source<0x1a000000
            mode=c&15
            if not w or not h or (port and mode==8):continue
            if d['scaleX']not in (0,256)or d['scaleY']not in (0,256):raise ValueError('Unmodeled DMA scaling')
            if mode not in (2,8,12):raise ValueError('Unmodeled native DMA pixel mode')
            indices=np.zeros((h,w),dtype=np.uint8)if mode==12 else decode(source,c,w,h)
            sy,sx=np.where(np.ones((h,w),dtype=bool)if mode==12 else indices!=0)
            x=d['x']+(-sx if c&16 else sx);y=(d['y']+(-sy if c&32 else sy))&511
            left,right,top,bottom=(d[k]for k in ('left','right','top','bottom'))
            if legacy_labels:left,right,top,bottom=top,bottom,left,right
            inside=(x>=left)&(x<=right)&(y>=top)&(y<=bottom)&(x>=0)&(x<512)
            x,y,sy,sx=(a[inside]for a in (x,y,sy,sx))
            pens=np.full(len(x),d['color'],dtype=np.uint8)if mode in (8,12)else indices[sy,sx]
            color[y,x]=palettes[d['palref']][pens];banks[y,x]=d['palette'];known[y,x]=True
            body[y,x]=d['slot']if mode==2 else 0
            shadow[y,x]=False
            if port and mode==2:
                found=owners[(d['frame'],source,d['slot'])]
                if not found:raise ValueError('Imported body missing actual owner')
                a=found[-1]
                if a['owner']!=a['actor']or a['id']not in (17,18):raise ValueError('Imported nonfighter projected')
                ground=a['stageY']+5+a['displayY']-a['cameraY']
                if d['mode']not in (2,3,5,7)or not 30<=ground<=510 or not 100<=a['stageY']<=400:continue
                jump=max(0,min(200,a['floor']-a['y']))
                sh=max(12,min(45,(h+3)//4+1));bottom=ground-3-jump*3//10;top=bottom-sh+1
                silhouette=indices[::-1]if c&32 else indices
                for row in range(sh):
                    sy=row*(h-1)//(sh-1);sx=np.flatnonzero(silhouette[sy]!=0)
                    x=d['x']+(-sx if c&16 else sx);y=top+row
                    x=x[(x>=0)&(x<512)]
                    if not 0<=y<512:continue
                    projected[y,x]=True
                    allowed=~np.isin(banks[y,x],list(protected));x=x[allowed]
                    color[y,x]=0;banks[y,x]=0;known[y,x]=True;body[y,x]=0;shadow[y,x]=True
        crop=lambda value:value[page:page+254,56:456]
        return dict(color=crop(color),known=crop(known),body=crop(body),shadow=crop(shadow),projected=crop(projected),owners=body_owners)
    return render


def inspect(folder,lag=1,limit=None,legacy_labels=False,page=256):
    groups,buffers,palettes,draws,owners=data(folder)
    model=renderer(buffers,palettes,draws,owners,legacy_labels)
    output=[]
    snaps=groups['FLOOR_SNAP'][:limit]if limit else groups['FLOOR_SNAP']
    for snap in snaps:
        r=model(snap['frame']-lag,snap['serial'],carry=2,page=page)
        image=np.asarray(Image.open(Path(folder)/'snap'/snap['file']).convert('RGB'))
        equal=np.all(image==r['color'],axis=2)
        masks={n:r['body']==n for n in (1,2)}
        count=int(np.count_nonzero(r['shadow']))
        output.append(dict(file=snap['file'],frame=snap['frame'],dma_frame=snap['frame']-lag,
                           epoch=snap['epoch'],arena=snap['arena'],known=int(r['known'].sum()),
                           known_matches=int((equal&r['known']).sum()),shadow=count,
                           missing_shadow=int((r['shadow']&np.any(image!=0,axis=2)).sum()),
                           body={n:dict(pixels=int(m.sum()),matches=int((m&equal).sum()),
                                        sole=int(np.where(m)[0].max())if m.any()else None,
                                        id=r['owners'].get(n,{}).get('id'),
                                        grounded=r['owners'].get(n,{}).get('y')==r['owners'].get(n,{}).get('floor'))
                                 for n,m in masks.items()}))
    return dict(scope='Diagnostic actual DMA shadow/ground pixels, not acceptance',lag=lag,page=page,
                arenas=sorted({r['arena']for r in output}),snapshots=len(output),records=output)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path);parser.add_argument('--lag',type=int,default=1)
    parser.add_argument('--page',type=int,choices=(0,256),default=256)
    parser.add_argument('--limit',type=int);parser.add_argument('--legacy-labels',action='store_true');args=parser.parse_args()
    print(json.dumps(inspect(args.folder,args.lag,args.limit,args.legacy_labels,args.page),indent=2))
