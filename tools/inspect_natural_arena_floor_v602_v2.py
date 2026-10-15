"""Read-only event-ordered native VRAM reconstruction, not floor acceptance.

Starts from the actual pre-window VRAM, then independently decodes all queued
DMA copies, native CPU writes and imported silhouettes up to the actual flip.
It does not initialize from the tested flip or choose a matching field/buffer.
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
    hex_fields=HEX|{'op','before0','before1','before','after'}
    str_fields=STR|{'register'}
    with(Path(folder)/'run.log').open(encoding='utf-8-sig')as stream:
        for line in stream:
            match=re.match(r'MK2_NAT_CAMPAIGN_(FLOOR_\w+) ',line)
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
        if not w or not h or(port and mode==8):return
        assert d['scaleX']in(0,256)and d['scaleY']in(0,256),'Unmodeled scaling'
        assert mode in(2,8,12)and d['skip']==0,'Unmodeled DMA mode or start/end skip'
        indices=np.zeros((h,w),dtype=np.uint8)if mode==12 else self.decode(source,c,w,h)
        sy,sx=np.where(np.ones((h,w),dtype=bool)if mode==12 else indices!=0)
        x=(d['x']+(-sx if c&16 else sx))&1023
        y=(d['y']+(-sy if c&32 else sy))&511
        inside=(x>=d['left'])&(x<=d['right'])&(y>=d['top'])&(y<=d['bottom'])&(x<512)
        x,y,sy,sx=(a[inside]for a in(x,y,sy,sx))
        pens=np.full(len(x),d['color'],dtype=np.uint16)if mode in(8,12)else indices[sy,sx].astype(np.uint16)
        self.words[y,x]=pens|d['palette']
        self.body[y,x]=d['slot']if mode==2 else 0
        self.shadow[y,x]=False
        if not(port and mode==2):return
        assert(c&0x8f)==0x82 and w<=200 and h<=200,'Imported body projection gate'
        candidates=self.owners[(d['frame'],source,d['slot'])]
        assert candidates,'Missing actual imported body owner'
        a=candidates[-1]
        assert a['owner']==a['actor']and a['id']in(17,18)
        ground=a['stageY']+5+a['displayY']-a['cameraY']
        if d['mode']not in(2,3,5,7)or not 30<=ground<=510 or not 100<=a['stageY']<=400:return
        protected=set()
        for key,records in self.owners.items():
            if key[0]==d['frame']:
                own=records[-1]
                if own['owner']==own['actor']and own['id']<=18 and own['bank']&0x7f00:
                    protected.add(own['bank']&0x7f00)
        jump=max(0,min(200,a['floor']-a['y']))
        sh=max(12,min(45,(h+3)//4+1))
        bottom=ground-3-jump*3//10
        silhouette=indices[::-1]if c&32 else indices
        for row in range(sh):
            yy=bottom-sh+1+row
            if not 0<=yy<512:continue
            sx=np.flatnonzero(silhouette[row*(h-1)//(sh-1)]!=0)
            xx=d['x']+(-sx if c&16 else sx)
            xx=xx[(xx>=0)&(xx<512)]
            self.projected[yy,xx]=True
            xx=xx[~np.isin(self.words[yy,xx]&0x7f00,list(protected))]
            self.words[yy,xx]=15
            self.body[yy,xx]=0
            self.shadow[yy,xx]=True

    def apply(self, kind, d):
        if self.epoch!=d['epoch']:self.begin(d['epoch'])
        assert d['event']>self.last_event,'Strict original event ordering'
        self.last_event=d['event']
        if kind=='FLOOR_DMA':self.dma(d)
        elif kind=='FLOOR_CPU':self.cpu(d)


def inspect(folder):
    folder=Path(folder)
    groups,buffers,palettes,draws,owners=data(folder)
    replay=Replay(folder,groups,buffers,owners)
    events=sorted([(kind,r)for kind in('FLOOR_DMA','FLOOR_CPU','FLOOR_FLIP')for r in groups[kind]],key=lambda e:e[1]['event'])
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
