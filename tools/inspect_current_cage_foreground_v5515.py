"""Read-only diagnostic of actual Cage capture foreground-owner counterexample.

Rebuild only already-digested actual GFX streams to locate each overlapped
object in the actual ordered ledger. No runtime/raster acceptance from hashes,
no replay boot, raw dumps, tolerance, ownership bypass or public changes.
"""
from collections import defaultdict
import json,re
import numpy as np
import verify_current_cage_sections_v5509 as c


def inspect():
    guest=c.model.current.expected();payload=(c.ROOT/c.model.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    reference,_=c.model.source_art(guest,payload,{})
    image=c.source_graphics(payload,{})
    log=(c.ROOT/'audit_v5513_current_cage_sections_ram/kano_p1/run.log').read_text()
    buffers={};meta={}
    for line in log.splitlines():
        if line.startswith('MK2_CURRENT_CAGE_RAM_GFX_DIGEST '):
            r=dict(re.findall(r'(\w+)=([^\s]+)',line));first=int(r['first']);count=int(r['bytes'])
            raw=image[first:first+count]
            c.need(c.digest(raw)==r['sha256'],'Every reconstructed stream equals complete actual previously captured native GFX digest')
            buffers[r['filename']]=dict(offset=int(r['offset']),data=raw.hex())
        if line.startswith('MK2_CURRENT_CAGE_RAM_VRAM_DIGEST '):
            r=dict(re.findall(r'(\w+)=([^\s]+)',line));meta[r['filename']]=r
    replay=c.raster.Replay(c.ROOT,defaultdict(list),buffers,{})
    replay.words=np.empty((512,512),np.uint16);replay.body=np.zeros((512,512),np.uint8)
    replay.shadow=np.zeros((512,512),bool);replay.projected=np.zeros((512,512),bool)
    dmas=c.rows(log,'DMA');cutoffs=c.rows(log,'CUTOFF');assets=reference['by_source'];out=[]
    native=c.model.original.records(log,'MK2_CAGE_TORSO_V979')
    action=next(r for tag,r in c.model.original.records(log,'MK2_STOCK_HEAD_V921')if tag=='ACTION')
    shots=[r for tag,r in native if tag=='POSE_SNAPSHOT'and int(r['source'],16)in assets]
    owned=[r for tag,r in native if tag=='DMA'and int(r['source'],16)in assets]
    for shot in shots:
        filename=f"torso_pose_{shot['actor_pose']}_{shot['frame']}.png"
        cutoff=next(r for r in cutoffs if r['filename']==filename)
        m=meta[filename];start=int(m['start'],16);control=int(m['control'],16)
        row=((start if control&0x400 else start^0xfffc)>>4)&511
        pose=assets[int(shot['source'],16)]['group']
        found=[d for d in owned if int(d['frame'])<=cutoff['frame']and int(d['fifo_pose'],16)==pose and int(d['y'])>>8==row>>8]
        latest=max(int(d['frame'])for d in found);found=[d for d in found if int(d['frame'])==latest]
        targets=[d for d in dmas if d['frame']==latest and any(d['source']==int(o['source'],16)and d['cursor']==int(o['cursor'],16)for o in found)]
        serials={d['serial']for d in targets};opaque=np.zeros((512,512),bool)
        for d in targets:
            replay.words.fill(65535);replay.dma(dict(d,slot=1));opaque|=replay.words!=65535
        for d in dmas:
            if not min(serials)<=d['serial']<=cutoff['serial']or d['serial']in serials:continue
            replay.words.fill(65535);replay.dma(dict(d,slot=1));overlap=(replay.words!=65535)&opaque
            if not overlap.any()or d['source']in assets or d['palette']==0x1c00:continue
            parts=c.graphics.native_group(dict(pose=f"{d['pose']:08X}",facing=f"{d['command']&0x30:08X}"),b'',guest)if d['pose']>=0xff800000 else []
            out.append(dict(sectionPose=assets[int(shot['source'],16)]['pose'],opaqueOverlapPixels=int(overlap.sum()),
                            command=d,physicalAction=action,nativeParts=parts))
    return out


if __name__=='__main__':print(json.dumps(inspect(),indent=2))
