"""Encode owned split sprites with the original three/zero/seven/zero grammar.

Only connected-alpha extraction, uniform scaling, palette quantization and
native six-bit packing. No source painting, no main0 replacement or proxy IDs.
This experimental encoding is NOT runtime or final visual acceptance.
"""
import hashlib
import json
import struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, find_objects
import build_native_pit_fall_v2 as colors
import build_native_death_art_v900 as death
import build_native_projectile_impacts as codec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'audit_v1107_owned_split_encoding'
SOURCE = ROOT/'diagnostic_v1071_native_detached_arm_costume/roms/mk2ks/mk2ks.mdata'
SOURCE_SHA = '5D78E543EA1E387461BD7EFF0958F9829565469CD51D5B2EE0A6CF1D90F0D322'
HEADER, DESCS, GROUPS, STREAMS, TABLE = 0x1c3800,0x1c3900,0x1c3b00,0x1c3bc0,0x1c3c80
ROM_DESCS,ROM_GROUPS,ROM_STREAMS,ROM_TABLE = 0xfbc80,0xfbe20,0xfbec0,0xfbf40
PIXEL_RANGES = ((0x172000,0x180000),(0x1bc000,0x1c0000))
GFX, GFX_END = 0x1f60000,0x1f80000
HALF_EXTENTS = ((96,90,82,71,80,90,99),(103,95,81,69,90,99,120))


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def address(at):
    return 0xff800000+at*8


def parts(path, count):
    image = Image.open(path).convert('RGBA')
    pixels = np.asarray(image)
    assert image.getextrema()[3] == (0,255)
    labels, _ = label(pixels[:,:,3]>=128, np.ones((3,3)))
    result = []
    for number, box in enumerate(find_objects(labels),1):
        if box is None:
            continue
        yy,xx = box
        mask = labels[box] == number
        if int(mask.sum()) < 1000:
            continue
        # Other poses overlap x projections; connected-alpha extraction keeps
        # their pixels OUT of this sprite without repainting any source color.
        tile = pixels[box].copy()
        tile[:,:,3] = np.where(mask,tile[:,:,3],0)
        bounds = [xx.start,yy.start,xx.stop,yy.stop]
        assert bounds[0]>0 and bounds[1]>0 and bounds[2]<image.width and bounds[3]<image.height
        result.append((bounds,Image.fromarray(tile)))
    result.sort(key=lambda p:p[0][0])
    assert len(result) == count,(path,len(result))
    return result


def main():
    if OUT.exists():
        raise ValueError('Never overwrite assets or evidence')
    source = SOURCE.read_bytes()
    assert len(source)==0x200000 and sha(source)==SOURCE_SHA
    stock = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    donor = (ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    assert sha(stock)==death.STOCK_SHA.upper() and sha(donor)==death.DONOR_SHA.upper()
    allocations = ((HEADER,0x1c4000),)+PIXEL_RANGES
    assert all(source[lo:hi]==b'\xff'*(hi-lo) for lo,hi in allocations)
    guest = (ROOT/'audit_v1091_jax_kano_p1_palette_regression/guest_maincpu.bin').read_bytes()
    assert guest[ROM_DESCS:0xfc000]==b'\xff'*(0xfc000-ROM_DESCS)
    pins = {str(SOURCE):sha(source),str(ROOT/'mk2/mk2-maincpu.bin'):sha(stock),str(ROOT/'mk3/mk3-maincpu.bin'):sha(donor)}
    art_review = json.loads((ROOT/'art_native_split_v1106/prompts-and-review.json').read_text())
    assert art_review['draft'] and not art_review['installed']
    for record in art_review['assets'].values():
        path=ROOT/'art_native_split_v1106'/record['file']
        assert sha(path.read_bytes())==record['sha256']
        assert path.read_bytes()==Path(record['source']).read_bytes()
    prior_review = json.loads((ROOT/'art_native_split_v1104/prompts-and-review.json').read_text())
    for record in prior_review['assets'].values():
        assert sha((ROOT/'art_native_split_v1104'/record['file']).read_bytes())==record['sha256']
    for folder in ('art_native_split_v1104','art_native_split_v1106'):
        for path in (ROOT/folder).iterdir():
            if path.is_file():pins[str(path)]=sha(path.read_bytes())
    payload = bytearray(source)
    OUT.mkdir()
    preview=Image.new('RGBA',(1400,680),(35,35,40,255))
    draw=ImageDraw.Draw(preview)
    pixel_bank,pixel_cursor,gfx_cursor=0,PIXEL_RANGES[0][0],GFX
    descriptor_index=0
    used=[0,0]
    report={'scope':'experimental owned vertical split encoding, not actual fatality acceptance',
        'sourcePayloadSHA256':SOURCE_SHA,'inputHashes':pins,'header':HEADER,
        'romDescriptors':ROM_DESCS,'romGroups':ROM_GROUPS,'romStreams':ROM_STREAMS,
        'romVictimTable':ROM_TABLE,'gfxStart':GFX,'fighters':{},
        'sourceArtPainted':False,'nonuniformStretchUsed':False,'main0Modified':False,
        'encodedVisualReviewed':False,'runtimeAccepted':False,'alternateCostumeAccepted':False,
        'bloodCostumeInvarianceAccepted':False,'fullPortAccepted':False}
    for fighter,name in enumerate(('kano','sonya')):
        normal=colors.palette(donor,(0x92bbc,0x92cf2)[fighter])
        alternate=colors.palette(donor,(0x92c3e,0x92d74)[fighter])
        initial=parts(ROOT/f'art_native_split_v1106/{name}-initial-three.png',3)
        halves=parts(ROOT/f'art_native_split_v1104/{name}-half-seven.png',7)
        full_scale=(134+fighter)/initial[0][1].height
        sequences=[]
        poses=[]
        for index,(bounds,image) in enumerate(initial+halves):
            # Full bodies retain ONE shared physical scale. Half-body source
            # rotation atlas changes raw size: normalize each with one uniform
            # factor to the corresponding ORIGINAL native pose's major extent.
            scale=full_scale if index<3 else HALF_EXTENTS[fighter][index-3]/max(image.size)
            width,height=round(image.width*scale),round(image.height*scale)
            assert 1<=width<=128 and 1<=height<=160,(name,index,width,height)
            scaled=image.resize((width,height),Image.Resampling.LANCZOS)
            indices=colors.quantize(scaled,normal)
            packed=codec.pack_indices(indices.tobytes())
            assert death.unpack(packed,indices.size)==indices.tobytes() and indices.any()
            required=(len(packed)+3)&~3
            if pixel_cursor+required>PIXEL_RANGES[pixel_bank][1]:
                used[pixel_bank]=pixel_cursor-PIXEL_RANGES[pixel_bank][0]
                pixel_bank+=1
                assert pixel_bank<len(PIXEL_RANGES),'Dedicated split pixels overflow'
                pixel_cursor=PIXEL_RANGES[pixel_bank][0]
            assert gfx_cursor+required<=GFX_END
            left=-width//2 if index<3 else -width
            bottom=139+fighter
            top=bottom-height
            descriptor=address(ROM_DESCS+descriptor_index*20)
            group=address(ROM_GROUPS+descriptor_index*8)
            graphic=gfx_cursor*8
            palette=address((0xfda00,0xfdb00)[fighter])
            struct.pack_into('<4hIHIH',payload,DESCS+descriptor_index*20,
                width,height,-left,-top,graphic,0x6000,palette,0)
            struct.pack_into('<2I',payload,GROUPS+descriptor_index*8,descriptor,0)
            payload[pixel_cursor:pixel_cursor+len(packed)]=packed
            sequences.append(group)
            poses.append({'pose':index,'kind':'initial' if index<3 else 'half',
                'sourceCrop':bounds,'uniformScale':scale,'size':[width,height],
                'bounds':[left,top,left+width,bottom],'descriptor':f'{descriptor:08X}',
                'group':f'{group:08X}','gfx':f'{graphic:08X}',
                'pixelOffset':pixel_cursor,'packedBytes':len(packed),'indicesSHA256':sha(indices.tobytes())})
            for costume,palette_colors in enumerate((normal,alternate)):
                pic=colors.decoded(indices,palette_colors)
                pic.save(OUT/f'{name}-{index}-{("normal","alternate")[costume]}.png')
                x=index*140;y=(fighter*2+costume)*170
                draw.text((x+3,y+3),f'{name}{index} c{costume} {width}x{height}',fill='white')
                preview.alpha_composite(pic,(x+(140-width)//2,y+160-height))
            descriptor_index+=1
            pixel_cursor+=required;gfx_cursor+=required
        words=sequences[:3]+[0]+sequences[3:]+[0]
        struct.pack_into('<12I',payload,STREAMS+fighter*48,*words)
        report['fighters'][name]={'actualID':17+fighter,'stream':f'{address(ROM_STREAMS+fighter*48):08X}',
            'nativeWords':[f'{word:08X}'for word in words],'poses':poses,
            'fullBodySharedScale':full_scale,'ownFloor':134+fighter,'exclusiveBottom':139+fighter}
    used[pixel_bank]=pixel_cursor-PIXEL_RANGES[pixel_bank][0]
    assert descriptor_index==20
    table=list(struct.unpack_from('<17I',stock,(0xff8cf110-0xff800000)//8))
    table += [address(ROM_STREAMS),address(ROM_STREAMS+48)]
    struct.pack_into('<19I',payload,TABLE,*table)
    fields=[PIXEL_RANGES[0][0],used[0],PIXEL_RANGES[1][0],used[1],GFX,
        DESCS,ROM_DESCS,20,20,GROUPS,ROM_GROUPS,160,STREAMS,ROM_STREAMS,96,TABLE,ROM_TABLE,76]
    struct.pack_into('<4s18I',payload,HEADER,b'KSP1',*fields)
    changed=[n for n,(a,b)in enumerate(zip(source,payload))if a!=b]
    assert all(any(lo<=n<hi for lo,hi in allocations)for n in changed)
    path=OUT/'roms/mk2ks/mk2ks.mdata'
    path.parent.mkdir(parents=True)
    path.write_bytes(payload)
    preview.save(OUT/'split-normal-alternate-preview.png')
    report.update(headerFields=fields,packedPixelBytes=sum(used),gfxEnd=gfx_cursor,
        payloadSHA256=sha(payload),changedPayloadBytes=len(changed),
        priorPayloadOutsideDedicatedAllocationsUnchanged=True,
        preservedOriginalVictimRows=[f'{word:08X}'for word in table[:17]])
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k]for k in ('payloadSHA256','packedPixelBytes','gfxEnd','runtimeAccepted')}))


if __name__=='__main__':
    main()
