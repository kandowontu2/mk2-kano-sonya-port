"""Read-only actual Baraka foreground diagnostic; no extra native boots.

Reconstruct actual previously digested GFX, locate all overlapping native
objects in the ordered ledger, and decode their ROM descriptors. This does
not substitute a hash for pixel/VRAM/ownership acceptance.
"""
import json,re,struct
from collections import defaultdict
import numpy as np
import verify_current_baraka_pixels_v5523 as c


def inspect():
    guest=c.model.current.expected();payload=(c.ROOT/c.model.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    reference,_=c.model.source_art(guest,payload,{})
    image=c.transport.source_graphics(payload,{})
    log=(c.BASE/'kano_p1/run.log').read_text();buffers={};meta={}
    for line in log.splitlines():
        if line.startswith('MK2_CURRENT_BARAKA_RAM_GFX_DIGEST '):
            r=dict(re.findall(r'(\w+)=([^\s]+)',line));first=int(r['first']);count=int(r['bytes']);raw=image[first:first+count]
            c.need(c.digest(raw)==r['sha256'],'Whole actual previously captured native source digest exact')
            buffers[r['filename']]=dict(offset=int(r['offset']),data=raw.hex())
        if line.startswith('MK2_CURRENT_BARAKA_RAM_VRAM_DIGEST '):
            r=dict(re.findall(r'(\w+)=([^\s]+)',line));meta[r['filename']]=r
    replay=c.transport.raster.Replay(c.ROOT,defaultdict(list),buffers,{})
    replay.words=np.empty((512,512),np.uint16);replay.body=np.zeros((512,512),np.uint8)
    replay.shadow=np.zeros((512,512),bool);replay.projected=np.zeros((512,512),bool)
    dmas=c.rows(log,'DMA');cutoffs=c.rows(log,'CUTOFF');assets=reference['by_source'];out=[]
    native=c.model.original.records(log,'MK2_ROLLING_HEAD_V1003')
    action=next(r for tag,r in c.model.original.records(log,'MK2_STOCK_HEAD_V921')if tag=='ACTION')
    shots=[r for tag,r in native if tag=='POSE_SNAPSHOT'and int(r['source'],16)in assets]
    owned=[r for tag,r in native if tag=='DMA'and int(r['source'],16)in assets]
    for shot in shots:
        filename=f"head_pose_{shot['actor_pose']}_{shot['frame']}.png"
        cutoff=next(r for r in cutoffs if r['filename']==filename);m=meta[filename]
        start=int(m['start'],16);control=int(m['control'],16);row=((start if control&0x400 else start^0xfffc)>>4)&511
        source=int(shot['source'],16)
        found=[d for d in owned if int(d['frame'])<=cutoff['frame']and int(d['source'],16)==source and int(d['y'])>>8==row>>8]
        latest=max(int(d['frame'])for d in found);found=[d for d in found if int(d['frame'])==latest]
        target=next(d for d in dmas if d['frame']==latest and d['source']==source and d['cursor']==int(found[0]['cursor'],16))
        replay.words.fill(65535);replay.dma(dict(target,slot=1));opaque=replay.words!=65535
        for d in dmas:
            if not target['serial']<d['serial']<=cutoff['serial']:continue
            replay.words.fill(65535);replay.dma(dict(d,slot=1));overlap=(replay.words!=65535)&opaque
            if not overlap.any()or d['source']in assets or d['palette']in(0x1c00,0x400)or d['id']==3:continue
            descriptor={}
            if 0xff800000<=d['cache']<=0xfffffff0:
                at=(d['cache']-0xff800000)//8
                descriptor=dict(compact=list(struct.unpack_from('<HHIH',guest,at)),offset=list(struct.unpack_from('<HHhhIH',guest,at)))
            out.append(dict(kind=assets[source]['kind'],pose=assets[source]['pose'],overlapPixels=int(overlap.sum()),
                            command=d,originalROMDescriptor=descriptor,physicalAction=action))
    return out


if __name__=='__main__':print(json.dumps(inspect(),indent=2))
