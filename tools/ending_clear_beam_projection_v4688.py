"""Source-bound single clear-field raster diagnosis; no whole-ending acceptance.

One actual preceding VRAM field initializes this diagnostic. Native CPU clear
stores are reconstructed from strictly sequential actual beam buckets. Each
visible row is sampled before stores made after its original partial update.
No image/address search, tolerance, skipped pixels or guest mutation.
"""
import hashlib,json,re
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent.parent

def need(ok,message):
    if not ok:raise ValueError(message)

def digest(raw):return hashlib.sha256(raw).hexdigest().upper()

def validate(native,buckets):
    need(native['frame']=='58183'and native['age']=='1887'and native['identity']=='17'and native['side']=='2'and
         native['writes']=='0'and native['assistance']=='none'and native['origin']=='56296'and
         native['start']=='FFFC'and native['dpyadr']=='F01C'and native['control']=='F010'and native['tap']=='001C'and
         native['vcount']=='273'and native['veblnk']=='20'and native['vsblnk']=='274',
         'Actual precise earned-Kano clear field and source-bound hardware scope')
    need(buckets and len(buckets)==260,'All260 actual clear-field CPU beam buckets')
    counts={};seen=set()
    for b in buckets:
        need(all(b[k]==native[k]for k in('frame','age','identity','side','writes','assistance')),
             'Every actual beam bucket belongs to the same true physical no-write context')
        beam=int(b['beam']);first,last=int(b['first'],16),int(b['last'],16)
        pc=b['pc'];count=int(b['count']);address=int(b['dpyadr'],16)
        need(b['mask']=='FFFF'and first%16==last%16==0 and first<=last<0x200000 and
             last-first==(count-1)*16 and count>0,'Every exact consecutive original CPU store, no holes or fabricated range')
        key=(beam,address,pc,b['value'],b['mask']);need(key not in seen,'No duplicate actual beam bucket');seen.add(key)
        if pc=='FF808680':
            need(b['value']=='3F3F'and 276<=beam<=280 and address==0xfffc and 0x1fe000<=first<=last<=0x1ffff0,
                 'Original pre-visible shift-template preparation, exact address/data/beam')
        else:
            need(pc=='FF80F550'and b['value']=='0000'and 19<=beam<=273 and first<=last<=0x106490,
                 'Only original zero-clear instruction with actual contiguous addresses and visible phase')
            wanted=0xfffc if beam<20 else(0xfffc-(beam-20+1)*16)&0xffff
            need(address==wanted,'Every actual post-partial-update DPYADR bound to original DUDATE, never image-derived')
        counts[pc]=counts.get(pc,0)+count
    need(counts=={'FF808680':512,'FF80F550':67146},'Entire actual source-exact template/clear store inventory')
    for pc,start,stop in(('FF808680',0x1fe000,0x200000),('FF80F550',0,0x1064a0)):
        rows=sorted((b for b in buckets if b['pc']==pc),key=lambda b:int(b['first'],16))
        cursor=start
        for b in rows:
            need(int(b['first'],16)==cursor,'Every original store represented once in continuous source-address order')
            cursor=int(b['last'],16)+16
        need(cursor==stop,'Complete original store range, not a sparse reconstruction')
    return True

def project(prior,end,palettes,rgb,native,buckets):
    validate(native,buckets)
    need(len(prior)==len(end)==524288 and len(palettes)==131072 and rgb.shape==(254,400,3),
         'Whole actual preceding/end VRAM, palette and visible RGB remain in RAM')
    words=np.frombuffer(prior,dtype='<u2').copy().reshape(512,512)
    surface=np.zeros((254,400),dtype=np.uint16);completed=0
    # Original frame begins in the preceding blank (274..), then wraps to
    # the20..273 visible rows. All template stores are before the clear.
    phase=lambda beam:beam if beam>=274 else beam+289
    ordered=sorted(buckets,key=lambda b:(phase(int(b['beam'])),int(b['first'],16)))
    for b in ordered:
        beam=int(b['beam'])
        if 20<=beam<274:
            upto=beam-20+1
            for row in range(completed,upto):
                address=(int(b['dpyadr'],16)+(beam-(20+row)+1)*16)&0xffff
                inverted=address^0xfffc
                source_row=(inverted>>4)&511
                column=((((inverted&0x7c)<<4)|0x1c)*2)&511
                surface[row]=words[source_row,(column+np.arange(400))&511]&0x7fff
            completed=upto
        first,last=int(b['first'],16)//8,int(b['last'],16)//8+2
        need(first<=last<=512*512,'Native bit-addressed CPU stores map to both T-unit pixels')
        value=int(b['value'],16)
        words.ravel()[first:last:2]=value&255
        words.ravel()[first+1:last:2]=(value>>8)&255
    need(completed==254,'Every original visible row sampled at real beam, none omitted')
    actual=np.frombuffer(end,dtype='<u2').reshape(512,512)
    mismatch=words!=actual
    need(not mismatch.any(),'Every reconstructed end VRAM word exact after all actual original stores')
    colors=np.frombuffer(palettes,dtype='<u4')
    expected=np.stack([(colors[surface]>>shift)&255 for shift in(16,8,0)],axis=2).astype(np.uint8)
    different=np.any(expected!=rgb,axis=2);where=np.argwhere(different)
    record=dict(frame=58183,sourceNativeCPUWrites=sum(int(b['count'])for b in buckets),exactEndVRAMWords=262144,
                actualVisibleRows=completed,projectedRGBSHA256=digest(expected.tobytes()),actualRGBSHA256=digest(rgb.tobytes()),
                mismatchedPixels=int(different.sum()),firstMismatch=where[0].tolist()if len(where)else None,
                fullEndingRendererVideoAccepted=False,diagnosticOnePrecedingVRAMBaseOnly=True)
    need(not different.any(),'Source-derived beam projection still differs: '+json.dumps(record))
    return record
