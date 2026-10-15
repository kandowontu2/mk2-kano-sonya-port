"""Repair native head ordering; encode missing diagonals without changing game code.

Kano uses only existing descriptor/pixel bytes, reordered in-place. Sonya's
three cardinal rotations use existing bytes; only three missing diagonal
sprites are alpha-cropped, uniformly scaled, palette-quantized and packed.
Both upright descriptors/pixels, all body art and all native streams remain
byte-identical. Encoding is not runtime acceptance.
"""
import hashlib
import json
import struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import build_native_death_art_v900 as death
import build_native_pit_fall_v2 as colors
import build_native_projectile_impacts as codec

ROOT=death.ROOT
SOURCE=ROOT/'diagnostic_v978_owned_torso_invariant_blood/roms/mk2ks/mk2ks.mdata'
SOURCE_SHA='2679C041539C99F917CE1A9AAADAE455859A20DA5F5CC8AF9FB6013DB6A79F79'
ART=ROOT/'art_native_rolling_heads_v998/sonya-diagonals-135-225-315.png'
ART_SHA='3ABABEDEA62905D75B161DC2D26A8424EEC19280B2A6FB9560D10C57B226E17E'
OUT=ROOT/'audit_v1000_owned_rolling_head_encoding'
ANGLES=(0,90,135,180,225,270,315)
KANO=(0,6,5,4,3,2,1)
SONYA={0:0,1:2,3:4,5:6}


def digest(data):return hashlib.sha256(data).hexdigest().upper()


def main():
    if OUT.exists():raise ValueError('Never overwrite an encoded asset')
    source=SOURCE.read_bytes(); donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    assert digest(source)==SOURCE_SHA and digest(donor)==death.DONOR_SHA.upper()
    assert digest(ART.read_bytes())==ART_SHA
    header=struct.unpack_from('<4s9I',source,death.HEADER)
    assert header==(b'KDH1',death.PIXELS,49228,death.GFX,death.DESCRIPTORS,death.ROM_DESCRIPTORS,28,20,7,2)
    parts=death.components(ART)
    assert len(parts)==3
    native0=death.DESCRIPTORS+21*20
    w,h,xo,yo,gfx,cmd,pal,pad=struct.unpack_from('<4hIHIH',source,native0)
    at=death.PIXELS+gfx//8-death.GFX
    raw=death.unpack(source[at:at+(w*h*6+7)//8],w*h)
    target_area=sum(v!=0 for v in raw)
    payload=bytearray(source);append=death.PIXELS+header[2]
    records=[];allowed=[(death.HEADER+8,death.HEADER+12)]
    for fighter,name in enumerate(('kano','sonya')):
        normal=colors.palette(donor,(0x92bbc,0x92cf2)[fighter])
        for pose,angle in enumerate(ANGLES):
            dest=death.DESCRIPTORS+(fighter*14+7+pose)*20
            before=source[dest:dest+20]
            record=dict(fighter=name,pose=pose,angleClockwise=angle,descriptorOffset=dest,
                        descriptor=f'{death.ROM_BASE+(death.ROM_DESCRIPTORS+dest-death.DESCRIPTORS)*8:08X}')
            if name=='kano' or pose in SONYA:
                origin=KANO[pose] if name=='kano' else SONYA[pose]
                old=death.DESCRIPTORS+(fighter*14+7+origin)*20
                payload[dest:dest+20]=source[old:old+20]
                record.update(sourceKind='unchanged_original_descriptor_and_pixels',oldPose=origin)
            else:
                index={2:0,4:1,6:2}[pose]
                box,image,area=parts[index]
                factor=(target_area/area)**0.5
                size=(round(image.width*factor),round(image.height*factor))
                scaled=image.resize(size,Image.Resampling.LANCZOS)
                indices=colors.quantize(scaled,normal)
                packed=codec.pack_indices(indices.tobytes())
                assert death.unpack(packed,indices.size)==indices.tobytes()
                end=(append+len(packed)+3)&~3
                assert source[append:end]==b'\xff'*(end-append)
                assert end<=death.END and death.GFX+end-death.PIXELS<=0x1ee0000
                graphic=(death.GFX+append-death.PIXELS)*8
                struct.pack_into('<4hIHIH',payload,dest,*size,size[0]//2,size[1]//2,
                                 graphic,0x6000,0xfffed800,0)
                payload[append:append+len(packed)]=packed
                payload[append+len(packed):end]=b'\0'*(end-append-len(packed))
                allowed.append((append,end))
                record.update(sourceKind='generated_missing_diagonal',sourceCrop=box,
                              sourceAlphaArea=area,scale=factor,targetNativeAlphaArea=target_area,
                              nativeAlphaArea=int(np.count_nonzero(indices)),pixelOffset=append,
                              packedBytes=len(packed),indicesSHA256=digest(indices.tobytes()))
                append=end
            if pose:allowed.append((dest,dest+20))
            else:assert payload[dest:dest+20]==before
            spec=struct.unpack_from('<4hIHIH',payload,dest)
            record.update(size=list(spec[:2]),offset=list(spec[2:4]),graphics=f'{spec[4]:08X}',
                          descriptorSHA256=digest(payload[dest:dest+20]))
            records.append(record)
    struct.pack_into('<I',payload,death.HEADER+8,append-death.PIXELS)
    mask=np.zeros(len(source),dtype=bool)
    for lo,hi in allowed:mask[lo:hi]=True
    changed=np.frombuffer(source,dtype=np.uint8)!=np.frombuffer(payload,dtype=np.uint8)
    assert not np.any(changed&~mask)
    assert payload[death.PIXELS:death.PIXELS+49228]==source[death.PIXELS:death.PIXELS+49228]
    OUT.mkdir();(OUT/'roms/mk2ks').mkdir(parents=True)
    (OUT/'roms/mk2ks/mk2ks.mdata').write_bytes(payload)
    sheet=Image.new('RGBA',(1120,360),(35,35,40,255));draw=ImageDraw.Draw(sheet)
    for record in records:
        fighter=0 if record['fighter']=='kano' else 1
        offset=record['descriptorOffset'];w,h,xo,yo,graphic,cmd,pal,pad=struct.unpack_from('<4hIHIH',payload,offset)
        pixel=death.PIXELS+graphic//8-death.GFX
        data=death.unpack(payload[pixel:pixel+(w*h*6+7)//8],w*h)
        image=colors.decoded(np.frombuffer(data,dtype=np.uint8).reshape((h,w)),
                             colors.palette(donor,(0x92bbc,0x92cf2)[fighter]))
        image=image.resize((w*4,h*4),Image.Resampling.NEAREST)
        x,y=record['pose']*160,fighter*180
        sheet.alpha_composite(image,(x+(160-image.width)//2,y+175-image.height))
        draw.text((x+3,y+3),f'{record["fighter"]} {record["pose"]}/{record["angleClockwise"]}',fill='white')
    sheet.save(OUT/'native-heads-order-4x.png')
    report=dict(scope='encoding only; native runtime/presentation acceptance pending',
                sourceSHA256=SOURCE_SHA,outputSHA256=digest(payload),sourceArtworkSHA256=ART_SHA,
                nativeAngles=list(ANGLES),frames=records,allowedChanges=allowed,
                changedBytes=int(changed.sum()),oldDeathPackedBytes=49228,newDeathPackedBytes=append-death.PIXELS,
                preservedPriorGraphics=True,preservedBodyAndUprightHeads=True,preservedAllNativeStreams=True,
                scalePolicy='uniform per new sprite; alpha area normalized to exact tested upright Sonya head; no stretching',
                runtimeAccepted=False,fullPortAccepted=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('frames','allowedChanges')},indent=2))


if __name__=='__main__':main()
