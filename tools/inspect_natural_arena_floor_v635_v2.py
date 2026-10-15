"""Read-only event-ordered native VRAM reconstruction, not floor acceptance.

Starts from each actual pre-draw-pass VRAM, then independently decodes all queued
DMA copies, native CPU writes and imported silhouettes up to the actual flip.
It does not initialize from the tested flip or choose a matching field/buffer.
Pre-pass erasure itself is outside this bounded runtime copy contract.
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
from inspect_natural_arena_floor_v602 import decoder, HEX, STR
from verify_native_floor_display_v602 import check_latch


def data(folder):
    groups=defaultdict(list)
    hex_fields=HEX|{'op','before0','before1','before','after','first_source','row'}
    str_fields=STR|{'register'}
    with(Path(folder)/'run.log').open(encoding='utf-8-sig')as stream:
        for line in stream:
            match=re.match(r'MK2_NAT_CAMPAIGN_(FLOOR_\w+|SHADOW_\w+) ',line)
            if not match:continue
            row=dict(re.findall(r'(\w+)=([^\s]+)',line))
            for k,v in row.items():
                if k not in str_fields:row[k]=int(v,16 if k in hex_fields else 10)
            groups[match[1]].append(row)
    buffers={r['key']:r for r in groups['FLOOR_GFX']}
    owners=defaultdict(list)
    for r in groups['FLOOR_OWNER']:owners[(r['frame'],r['source'],r['slot'])].append(r)
    return groups,buffers,None,None,owners


class Replay:
    def __init__(self, folder, groups, buffers, owners):
        self.folder=Path(folder)
        self.groups=groups
        self.decode=decoder(buffers)
        self.owners=owners
        self.bases={r['epoch']:r for r in groups['FLOOR_BASE']}
        self.epoch=None
        self.words=None
        self.body=None
        self.shadow=None
        self.projected=None
        self.last_event=0

    def begin(self, epoch):
        base=self.bases[epoch]
        raw=(self.folder/base['file']).read_bytes()
        assert len(raw)==512*512*2 and base['phase']=='before_first_observed_write'
        self.words=np.frombuffer(raw,dtype='<u2').copy().reshape(512,512)
        self.body=np.zeros((512,512),dtype=np.uint8)
        self.shadow=np.zeros((512,512),dtype=bool)
        self.projected=np.zeros((512,512),dtype=bool)
        self.epoch=epoch
        self.last_event=base['event']

    def cpu(self, d):
        for part,mask in enumerate((0xff,0xff00)):
            if not d['mask']&mask:continue
            y,x=divmod(d['index']+part,512)
            old=int(self.words[y,x])
            assert old==d[f'before{part}'], 'CPU pre-write VRAM differs from independent replay'
            byte=(d['value']>>(8*part))&255
            if d['video_bank']:
                bank=((d['palette']&255)<<8)if part==0 else d['palette']&0xff00
                self.words[y,x]=byte|bank
            else:self.words[y,x]=(old&255)|(byte<<8)
            self.body[y,x]=0
            self.shadow[y,x]=False

    def dma(self, d):
        source,c,w,h=d['source'],d['command'],d['width'],d['height']
        port=0x10000000<=source<0x1a000000
        mode=c&15
        if not w or not h:return
        assert d['scaleX']in(0,256)and d['scaleY']in(0,256),'Unmodeled scaling'
        assert mode in(2,8,12),'Unmodeled DMA pixel mode'
        indices=np.zeros((h,w),dtype=np.uint8)if mode==12 else self.decode(source,c,w,h)
        sy,sx=np.where(np.ones((h,w),dtype=bool)if mode==12 else indices!=0)
        x=(d['x']+(-sx if c&16 else sx))&1023
        y=(d['y']+(-sy if c&32 else sy))&511
        # Actual native LRSKIP semantics: bit 40 splits low-byte start and
        # high-byte end; otherwise the entire word is the end skip.
        # This limits emitted columns without changing row-stream decoding.
        startskip=(d['skip']&255)if c&64 else 0
        endskip=(d['skip']>>8)if c&64 else d['skip']
        inside=(sx>=startskip)&(sx<w-endskip)&(x>=d['left'])&(x<=d['right'])&(y>=d['top'])&(y<=d['bottom'])&(x<512)
        x,y,sy,sx=(a[inside]for a in(x,y,sy,sx))
        pens=np.full(len(x),d['color'],dtype=np.uint16)if mode in(8,12)else indices[sy,sx].astype(np.uint16)
        self.words[y,x]=pens|d['palette']
        self.body[y,x]=d['slot']if mode==2 else 0
        self.shadow[y,x]=port and mode==8
    def apply(self, kind, d):
        if self.epoch!=d['epoch']:self.begin(d['epoch'])
        assert d['event']>self.last_event,'Strict original event ordering'
        self.last_event=d['event']
        if kind=='FLOOR_PRE_FRAME':
            assert d['phase']=='before_first_frame_dma'
            raw=(self.folder/d['file']).read_bytes()
            assert len(raw)==512*512*2,'Exact pre-pass VRAM size'
            self.words=np.frombuffer(raw,dtype='<u2').copy().reshape(512,512)
            self.body[:]=0
            self.shadow[:]=False
            self.projected[:]=False
        elif kind=='FLOOR_DMA':self.dma(d)
        elif kind=='FLOOR_CPU':self.cpu(d)


def inspect(folder):
    folder=Path(folder)
    groups,buffers,palettes,draws,owners=data(folder)
    replay=Replay(folder,groups,buffers,owners)
    events=sorted([(kind,r)for kind in('FLOOR_PRE_FRAME','FLOOR_DMA','FLOOR_CPU','FLOOR_FLIP')for r in groups[kind]],key=lambda e:e[1]['event'])
    latches={r['event']:r for r in groups['FLOOR_LATCH']if r['flip_frame']==r['snapshot']}
    displays={r['frame']:r for r in groups['FLOOR_DISPLAY']}
    snaps={r['frame']:r for r in groups['FLOOR_SNAP']}
    records=[]
    for kind,d in events:
        if kind!='FLOOR_FLIP':replay.apply(kind,d);continue
        if d['event']not in latches:continue
        latch=latches[d['event']]
        frame=d['frame']
        actual=np.fromfile(folder/latch['file'],dtype='<u2').reshape(512,512)
        mismatch=replay.words!=actual
        display=displays[frame]
        image=np.asarray(Image.open(folder/'snap'/snaps[frame]['file']).convert('RGB'))
        bound=check_latch(image,actual.tobytes(),(folder/display['palette_file']).read_bytes(),d['value'],d['control'],d['tap'])
        row,col=bound['row'],bound['column']
        crop=lambda a:a[row:row+254,col:col+400]
        difference=crop(mismatch)
        y,x=np.where(difference)
        masks={n:crop(replay.body)==n for n in(1,2)}
        body={n:dict(pixels=int(m.sum()),mismatches=int((m&difference).sum()),
                     sole=int(np.where(m)[0].max())if m.any()else None)for n,m in masks.items()}
        for n in body:
            found=[a for a in groups['FLOOR_OWNER']if a['frame']==frame-1 and a['slot']==n]
            if found:
                a=found[-1]
                body[n].update(id=a['id'],object_y=a['y'],floor=a['floor'],action=a['action'],
                    grounded=a['y']==a['floor'],native_ground=a['stageY']+5+a['displayY']-a['cameraY']-row)
        sm=crop(replay.shadow)
        records.append(dict(frame=frame,event=d['event'],arena=snaps[frame]['arena'],
            file=snaps[frame]['file'],display_pixels=bound['pixels'],vram_mismatches=int(mismatch.sum()),
            displayed_mismatches=int(difference.sum()),shadow_pixels=int(sm.sum()),shadow_mismatches=int((sm&difference).sum()),
            body=body,first_differences=[dict(x=int(xx),y=int(yy),model=int(crop(replay.words)[yy,xx]),actual=int(crop(actual)[yy,xx]))for yy,xx in zip(y[:20],x[:20])]))
    return dict(scope='Diagnostic event-ordered native VRAM reconstruction, not desired floor/shadow geometry acceptance',
        cpu_writes=len(groups['FLOOR_CPU']),frames=len(records),records=records,
        fullPortAcceptance=False,floorAcceptance=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path)
    args=parser.parse_args()
    print(json.dumps(inspect(args.folder),indent=2))
