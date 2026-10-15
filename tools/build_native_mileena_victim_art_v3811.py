"""Encode owned swallowing artwork; no pose painting and no runtime acceptance.

Uniform downsampling per fighter, alpha isolation, existing costume palette,
six-bit packing. Native clipping-plane X and phase-center Y are source-bound.
The original seven/eight-pose streams and native cadence remain unchanged.
"""
import hashlib,json,struct,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import build_native_pit_fall_v2 as colors
import build_native_projectile_impacts as codec
import build_native_death_art_v900 as unpacker
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'asset_v3812_native_mileena_victims'
BASE=ROOT/'diagnostic_v3680_native_sound_packet_guard/roms/mk2ks/mk2ks.mdata'
HEADER,DESC,GROUPS,STREAMS,TABLE,END=0x1f6000,0x1f6100,0x1f6280,0x1f6300,0x1f6380,0x1f6400
R_DESC,R_GROUPS,R_STREAMS,R_TABLE=0xac000,0xac200,(0xac280,0xac2a0),0xac300
POOLS=((0x122000,0x130000),(0x154000,0x160000))
GFX,GFX_END=0x1f80000,0x1fa0000
ART_HASHES=('C9D25CDAB198EE3ED400A18EA401AE53F1F3F32193B9F56C3E860CF9D13C0924','37ED3F47FF31112D5AA0194F6F84FBB55E16B632330037F30CE521E711E5704B')
def sha(b):return hashlib.sha256(b).hexdigest().upper()
def addr(b):return 0xff800000+b*8
def off(b):return (b-0xff800000)//8
def require(c,s):
    if not c:raise ValueError(s)
def main():
    require(not OUT.exists(),'Fresh immutable encoded art')
    source=BASE.read_bytes();donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    guest_path=ROOT/'audit_v3788_mileena_kano_p1_earned_cache/guest_maincpu.bin';guest=guest_path.read_bytes()
    require(sha(source)=='ED9023949F73BD719F8BC688C69230C68239D7CC140F814C1A4E54A5BF561BC3','Current complete payload')
    require(sha(guest)=='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7','Actual unchanged initialized guest')
    require(sha(stock)==unpacker.STOCK_SHA.upper() and sha(donor)==unpacker.DONOR_SHA.upper(),'Original programs')
    require(guest[R_DESC:R_TABLE+76]==b'\xff'*(R_TABLE+76-R_DESC),'Entire initialized native allocation unoccupied')
    require(struct.unpack_from('<I',guest,off(0xff9e7ea0))[0]==0xff9e9140,'Original native victim consumer')
    for a,b in ((HEADER,END),*POOLS):require(source[a:b]==b'\xff'*(b-a),'Payload allocation unoccupied')
    reference_path=ROOT/'art_reference_mileena_v3801/reference.json';refs=json.loads(reference_path.read_text())
    payload=bytearray(source);allowed=set(range(HEADER,END));pins={str(p):sha(p.read_bytes())for p in (BASE,guest_path,reference_path,ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin',Path(__file__))}
    preview=Image.new('RGBA',(1200,340),(32,32,38,255));draw=ImageDraw.Draw(preview)
    records=[];sizes=[];graphic_cursor=GFX;index=0
    for fighter,(name,sex,count)in enumerate((('kano','male',7),('sonya','female',8))):
        path=ROOT/'art_native_mileena_v3810'/f'{name}-swallowing.png';raw=path.read_bytes();require(sha(raw)==ART_HASHES[fighter],'Selected own art unchanged');pins[str(path)]=sha(raw)
        sheet=Image.open(path);require(sheet.mode=='RGBA' and sheet.size==(1536,1024),'Eight-cell source alpha atlas')
        parts=[]
        for phase in range(8):
            cell=sheet.crop((phase%4*384,phase//4*512,(phase%4+1)*384,(phase//4+1)*512))
            box=cell.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
            if phase>=count:require(box is None,'Empty unused Kano cell');continue
            require(box is not None and min(box[:2])>=2 and box[2]<=382 and box[3]<=510,'No clipped source cell')
            parts.append((box,cell.crop(box)))
        original=refs['stock'][sex]['poses'];require(len(original)==count,'Original phase grammar')
        factor=original[0]['size'][1]/parts[0][1].height
        palette=colors.palette(donor,(0x92bbc,0x92cf2)[fighter]);pixel_at=POOLS[fighter][0];group_pointers=[]
        for phase,(box,cell)in enumerate(parts):
            width,height=round(cell.width*factor),round(cell.height*factor)
            require(1<=width<=160 and 1<=height<=160,'Native sprite bounds')
            image=cell.resize((width,height),Image.Resampling.LANCZOS)
            indices=colors.quantize(image,palette);raw=indices.tobytes();packed=codec.pack_indices(raw)
            require(unpacker.unpack(packed,width*height)==raw and any(raw),'Independent six-bit roundtrip')
            require(pixel_at+len(packed)<=POOLS[fighter][1] and graphic_cursor+len(packed)<=GFX_END,'Owned pixel ranges')
            bounds=original[phase]['bounds'];right=bounds[2];left=right-width
            top=round((bounds[1]+bounds[3]-height)/2)
            descriptor=addr(R_DESC+index*20);group=addr(R_GROUPS+index*8)
            palette_address=addr((0xfda00,0xfdb00)[fighter]);graphic=graphic_cursor*8
            struct.pack_into('<4hIHIH',payload,DESC+index*20,width,height,-left,-top,graphic,0x6000,palette_address,0)
            struct.pack_into('<2I',payload,GROUPS+index*8,descriptor,0)
            payload[pixel_at:pixel_at+len(packed)]=packed;allowed.update(range(pixel_at,pixel_at+len(packed)))
            records.append(dict(fighter=name,id=17+fighter,phase=phase,sourceCrop=box,uniformScale=factor,size=[width,height],bounds=[left,top,right,top+height],stockBounds=bounds,descriptor=f'{descriptor:08X}',group=f'{group:08X}',palette=f'{palette_address:08X}',graphics=f'{graphic:08X}',payloadPixelOffset=pixel_at,packedBytes=len(packed),indicesSHA256=sha(raw),visiblePixels=int(np.count_nonzero(indices))))
            image=colors.decoded(indices,palette);preview.alpha_composite(image,(phase*150+(150-width)//2,fighter*170+27+(137-height)//2));draw.text((phase*150+3,fighter*170+4),f'{name} phase {phase}',fill='white')
            group_pointers.append(group);index+=1
            padded=(len(packed)+3)&~3;pixel_at+=padded;graphic_cursor+=padded
        sizes.append(pixel_at-POOLS[fighter][0]);struct.pack_into('<'+str(count+1)+'I',payload,STREAMS+fighter*32,*group_pointers,0)
    require(index==15,'All character-owned phase groups')
    table=list(struct.unpack_from('<17I',stock,off(0xff9e9140)))+[addr(s)for s in R_STREAMS]
    struct.pack_into('<19I',payload,TABLE,*table)
    fields=[POOLS[0][0],sizes[0],POOLS[1][0],sizes[1],GFX,DESC,R_DESC,15,20,GROUPS,R_GROUPS,STREAMS,R_STREAMS[0],R_STREAMS[1],TABLE,R_TABLE,7,8]
    struct.pack_into('<4s18I',payload,HEADER,b'KME1',*fields)
    changed={i for i,(a,b)in enumerate(zip(source,payload))if a!=b};require(changed and changed<=allowed and len(payload)==len(source),'Only new owned allocations changed')
    expected=bytearray(guest)
    for a,b,n in ((DESC,R_DESC,300),(GROUPS,R_GROUPS,120),(STREAMS,R_STREAMS[0],32),(STREAMS+32,R_STREAMS[1],36),(TABLE,R_TABLE,76)):expected[b:b+n]=payload[a:a+n]
    struct.pack_into('<I',expected,off(0xff9e7ea0),addr(R_TABLE))
    OUT.mkdir();require(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Inherited compression before output')
    (OUT/'roms/mk2ks').mkdir(parents=True);(OUT/'roms/mk2ks/mk2ks.mdata').write_bytes(payload)
    preview.save(OUT/'encoded-poses-review.png')
    report=dict(scope=__doc__,encoded=True,inputHashes=pins,headerFields=fields,frames=records,pixelBytes=sizes,outputPayloadSHA256=sha(payload),expectedGuestSHA256=sha(expected),newProgramStorage=[R_DESC,R_TABLE+76],oldTableRowsPreserved=17,stockPlayableRows=12,uniformScalePerFighter=True,nativeConsumerOnlyOperandChanged=True,actualNativeRuntimeAccepted=False,artAcceptance=False,fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k]for k in ('encoded','outputPayloadSHA256','expectedGuestSHA256','pixelBytes','artAcceptance','actualNativeRuntimeAccepted')}))
if __name__=='__main__':main()
