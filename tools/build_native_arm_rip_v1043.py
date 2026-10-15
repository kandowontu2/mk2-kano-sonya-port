"""Encode imagegen-owned Jax victim art; no repainting or native state writes.

Uniform scaling, alpha crops, palette quantization, native multipart tiling and
six-bit packing only. Encoding success is NOT actual fatality acceptance.
"""
import hashlib
import json
import struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import build_native_pit_fall_v2 as colors
import build_native_death_art_v900 as death
import build_native_projectile_impacts as codec

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_v1043_owned_arm_rip_encoding'
ART=ROOT/'art_native_arm_rip_v1041'
SOURCE=ROOT/'diagnostic_v1028_native_jax_clap_grounding/roms/mk2ks/mk2ks.mdata'
SOURCE_SHA='56B3D09C3EF398DE8CEDF11832732D3F2AE517A592CACFFDFB3346BDD497C4B9'
HEADER,DESCS,GROUPS,STREAMS=0x1c3000,0x1c3100,0x1c3500,0x1c3600
ROM_DESCS,ROM_GROUPS,ROM_STREAMS=0xfb680,0xfb900,0xfb980
PIXEL_RANGES=((0x1c7000,0x1d0000),(0x1d6000,0x1e0000))
GFX,GFX_END=0x1f40000,0x1f60000
COUNTS=((3,2,2,2,2),(3,1,1,2,2))
ARM_BOUNDS=((31,90,88,116),(-6,113,58,128),(-44,57,2,105),(-83,91,-24,114),(-97,135,-40,145))
GENERATED={
 'kano-body-five.png':'exec-700cc78f-1a0a-417d-afd8-6854b64a9e28.png',
 'sonya-body-rejected-costume.png':'exec-f1622c80-6837-41fb-9cb3-709fcea69842.png',
 'sonya-body-five.png':'exec-7c85c100-c6a9-4487-acb6-a5088c75abd2.png',
 'kano-arms-five.png':'exec-0cc6d7b4-92d7-42fa-9f97-56eb0456f7dc.png',
 'sonya-arms-five.png':'exec-ad2109a4-e948-498e-ad6b-c4508aa26988.png'}

def sha(data):return hashlib.sha256(data).hexdigest().upper()
def address(at):return 0xff800000+at*8

def crop(sheet,pose):
    # Generated sprites are isolated but not exactly equal-cell centered.
    # Find original alpha gaps; crop the existing pixels without moving any.
    present=np.flatnonzero((np.asarray(sheet)[:,:,3]>=128).any(axis=0))
    runs=np.split(present,np.flatnonzero(np.diff(present)>25)+1)
    assert len(runs)==5,'Exactly five horizontally isolated source sprites required'
    x0=int(runs[pose][0])-3;x1=int(runs[pose][-1])+4
    assert x0>=0 and x1<=sheet.width
    cell=sheet.crop((x0,0,x1,sheet.height))
    bounds=cell.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox()
    if not bounds or bounds[0]<2 or bounds[2]>cell.width-2 or bounds[1]<2 or bounds[3]>cell.height-2:
        raise ValueError('Missing/clipped five-column alpha sprite')
    return cell.crop(bounds),list(bounds)

def main():
    if OUT.exists():raise ValueError('Never overwrite build/evidence')
    source=SOURCE.read_bytes();assert sha(source)==SOURCE_SHA
    donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();assert sha(donor)==death.DONOR_SHA.upper()
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();assert sha(stock)==death.STOCK_SHA.upper()
    payload=bytearray(source)
    allocations=((HEADER,0x1c3800),)+PIXEL_RANGES
    for lo,hi in allocations:assert source[lo:hi]==b'\xff'*(hi-lo),(hex(lo),hex(hi))
    pins={str(SOURCE):sha(source),str(ROOT/'mk3/mk3-maincpu.bin'):sha(donor),str(ROOT/'mk2/mk2-maincpu.bin'):sha(stock)}
    for path in ART.iterdir():
        if path.is_file():pins[str(path)]=sha(path.read_bytes())
    generated=Path('C:/Users/kando/.codex/generated_images/01a054e7-3dff-78b2-ba5c-269642375adb')
    for asset,original in GENERATED.items():assert (ART/asset).read_bytes()==(generated/original).read_bytes()
    OUT.mkdir()
    preview=Image.new('RGBA',(1500,800),(35,35,40,255));draw=ImageDraw.Draw(preview)
    descriptor_index=0;group_cursor=0;pixel_bank=0;pixel_cursor=PIXEL_RANGES[0][0];gfx_cursor=GFX
    used=[0,0];report={'scope':'owned native Jax arm-rip asset encoding only','inputHashes':pins,
      'header':HEADER,'romDescriptors':ROM_DESCS,'romGroups':ROM_GROUPS,'romStreams':ROM_STREAMS,
      'gfxStart':GFX,'componentCounts':COUNTS,'fighters':{},'generatedImages':GENERATED,
      'tool':'built-in image_gen','sourceArtReviewed':True,'encodedArtReviewed':False,
      'runtimeAccepted':False,'alternateCostumeAccepted':False,'fullPortAccepted':False}
    for fighter,name in enumerate(('kano','sonya')):
        normal=colors.palette(donor,(0x92bbc,0x92cf2)[fighter])
        alternate=colors.palette(donor,(0x92c3e,0x92d74)[fighter])
        record={'id':17+fighter,'poses':[],'bodyStream':f'{address(ROM_STREAMS+fighter*48):08X}',
                'armStream':f'{address(ROM_STREAMS+fighter*48+24):08X}'}
        for kind in ('body','arms'):
            sheet=Image.open(ART/f'{name}-{kind}-five.png').convert('RGBA')
            assert sheet.size==(1774,887) and sheet.getextrema()[3]==(0,255)
            parts=[crop(sheet,i) for i in range(5)]
            # One scale for all body poses, another for the rotated arm atlas.
            # Own standing floor anchors are 134/135 with the MKII +5 contact.
            scale=(134+fighter)/parts[4][0].height if kind=='body' else 60/parts[1][0].width
            pointers=[]
            for pose,(image,bounds) in enumerate(parts):
                size=(round(image.width*scale),round(image.height*scale))
                assert 1<=size[0]<=128 and 1<=size[1]<=160
                scaled=image.resize(size,Image.Resampling.LANCZOS)
                indices=colors.quantize(scaled,normal)
                if kind=='body':
                    left=-14 if pose==0 else -size[0]//2+3
                    bottom=139+fighter
                    components=COUNTS[fighter][pose]
                else:
                    original=ARM_BOUNDS[pose]
                    left=round((original[0]+original[2]-size[0])/2)
                    bottom=original[3];components=1
                top=bottom-size[1];descriptors=[]
                component_records=[]
                for column in range(components):
                    x0,x1=column*size[0]//components,(column+1)*size[0]//components
                    tile=indices[:,x0:x1].copy();packed=codec.pack_indices(tile.tobytes())
                    assert death.unpack(packed,tile.size)==tile.tobytes() and tile.any()
                    required=(len(packed)+3)&~3
                    if pixel_cursor+required>PIXEL_RANGES[pixel_bank][1]:
                        used[pixel_bank]=pixel_cursor-PIXEL_RANGES[pixel_bank][0]
                        pixel_bank+=1;assert pixel_bank<len(PIXEL_RANGES)
                        pixel_cursor=PIXEL_RANGES[pixel_bank][0]
                    assert gfx_cursor+required<=GFX_END
                    pointer=address(ROM_DESCS+descriptor_index*20)
                    graphic=gfx_cursor*8
                    palette=address((0xfda00,0xfdb00)[fighter])
                    struct.pack_into('<4hIHIH',payload,DESCS+descriptor_index*20,
                        x1-x0,size[1],-left-x0,-top,graphic,0x6000,palette,0)
                    payload[pixel_cursor:pixel_cursor+len(packed)]=packed
                    component_records.append({'descriptor':f'{pointer:08X}','gfx':f'{graphic:08X}',
                        'pixelOffset':pixel_cursor,'packedBytes':len(packed),'size':[x1-x0,size[1]],
                        'bounds':[left+x0,top,left+x1,bottom],'indicesSHA256':sha(tile.tobytes())})
                    descriptors.append(pointer);descriptor_index+=1;pixel_cursor+=required;gfx_cursor+=required
                if kind=='body':
                    pointer=address(ROM_GROUPS+group_cursor)
                    struct.pack_into('<'+str(components+1)+'I',payload,GROUPS+group_cursor,*descriptors,0)
                    group_cursor+=(components+1)*4
                else:pointer=descriptors[0]
                pointers.append(pointer)
                record['poses'].append({'kind':kind,'pose':pose,'pointer':f'{pointer:08X}',
                  'sourceCrop':bounds,'scale':scale,'bounds':[left,top,left+size[0],bottom],
                  'size':list(size),'indicesSHA256':sha(indices.tobytes()),'components':component_records})
                for costume,palette in enumerate((normal,alternate)):
                    y=fighter*400+(0 if kind=='body' else 170)+costume*85 if kind=='arms' else fighter*400+costume*150
                    x=pose*300
                    draw.text((x+2,y+2),f'{name} {kind}{pose} costume{costume}: {size}',fill='white')
                    preview.alpha_composite(colors.decoded(indices,palette),(x+120-size[0]//2,y+145-size[1] if kind=='body' else y+70-size[1]))
                colors.decoded(indices,normal).save(OUT/f'{name}-{kind}-{pose}-normal.png')
                colors.decoded(indices,alternate).save(OUT/f'{name}-{kind}-{pose}-alternate.png')
            offset=STREAMS+fighter*48+(0 if kind=='body' else 24)
            struct.pack_into('<6I',payload,offset,*pointers,0)
        report['fighters'][name]=record
    used[pixel_bank]=pixel_cursor-PIXEL_RANGES[pixel_bank][0]
    assert descriptor_index==30 and group_cursor==120
    fields=[PIXEL_RANGES[0][0],used[0],PIXEL_RANGES[1][0],used[1],GFX,DESCS,ROM_DESCS,30,20,GROUPS,ROM_GROUPS,120,STREAMS,ROM_STREAMS,96]
    struct.pack_into('<4s15I',payload,HEADER,b'KAR1',*fields)
    changed=[i for i,(a,b) in enumerate(zip(source,payload)) if a!=b]
    assert all(any(lo<=i<hi for lo,hi in allocations) for i in changed)
    output=OUT/'roms/mk2ks/mk2ks.mdata';output.parent.mkdir(parents=True);output.write_bytes(payload)
    preview.save(OUT/'arm-rip-normal-alternate-preview.png')
    report.update(headerFields=fields,payloadSHA256=sha(payload),changedPayloadBytes=len(changed),
      packedPixelBytes=sum(used),gfxEnd=gfx_cursor,descriptorCount=30,groupBytes=120,
      priorPayloadOutsideDedicatedAllocationsUnchanged=True)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'output':str(OUT),'payloadSHA256':sha(payload),'packedPixelBytes':sum(used),
                      'descriptorCount':30,'runtimeAccepted':False}))

if __name__=='__main__':main()
