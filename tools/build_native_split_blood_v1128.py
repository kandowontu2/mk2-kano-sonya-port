"""Kano split blood indices only; immutable source art, no painting or code."""
import hashlib,json,struct
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,find_objects
import build_native_pit_fall_v2 as colors
import build_native_torso_art_v977 as blood
import verify_rolling_heads_v1014 as decoder
import build_native_projectile_impacts as packer

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_v1128_owned_split_blood_encoding'
SOURCE=ROOT/'diagnostic_v1110_owned_native_split/roms/mk2ks/mk2ks.mdata'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def sections(image,count):
    rgba=np.asarray(image)
    components,_=label(rgba[:,:,3]>=128,np.ones((3,3)))
    result=[]
    for number,box in enumerate(find_objects(components),1):
        if box is None:continue
        mask=components[box]==number
        if int(mask.sum())<1000:continue
        yy,xx=box
        tile=rgba[box].copy();tile[:,:,3]=np.where(mask,tile[:,:,3],0)
        result.append(([xx.start,yy.start,xx.stop,yy.stop],Image.fromarray(tile),mask))
    result.sort(key=lambda row:row[0][0])
    assert len(result)==count
    return result

if OUT.exists():raise ValueError('Preserve encoding evidence')
assert digest(SOURCE)=='C19F8C6F6860FC68EBD6E50635E4906F89729D2B20356F361FE5A0DC0A519734'
source=SOURCE.read_bytes();payload=bytearray(source)
metadata_path=ROOT/'audit_v1107_owned_split_encoding/report.json'
metadata=json.loads(metadata_path.read_text())
donor_path=ROOT/'mk3/mk3-maincpu.bin';donor=donor_path.read_bytes()
assert digest(donor_path)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
normal,alternate=(colors.palette(donor,at) for at in (0x92bbc,0x92c3e))
provenance_path=ROOT/'art_native_split_blood_v1127/provenance.json'
provenance=json.loads(provenance_path.read_text())
pins={str(path):digest(path) for path in (SOURCE,metadata_path,donor_path,provenance_path)}
preview=Image.new('RGBA',(1400,360),(35,35,40,255));draw=ImageDraw.Draw(preview)
records,spans=[],[]
OUT.mkdir()
for kind,count,start in (('initial',3,0),('half',7,3)):
    info=provenance[kind]
    art_path=ROOT/info['sourceTarget'];guide_path=ROOT/'art_native_split_blood_v1127'/info['file']
    assert digest(guide_path)==info['sha256'] and guide_path.read_bytes()==Path(info['builtinSource']).read_bytes()
    sheet,guide=(Image.open(path).convert('RGBA') for path in (art_path,guide_path))
    assert sheet.size==guide.size==(2172,724)
    assert sheet.getextrema()[3]==guide.getextrema()[3]==(0,255)
    pins[str(art_path)],pins[str(guide_path)]=digest(art_path),digest(guide_path)
    for part,(box,image,component_mask) in enumerate(sections(sheet,count)):
        pose=start+part
        record=metadata['fighters']['kano']['poses'][pose]
        assert record['sourceCrop']==box
        # Use SOURCE alpha membership, never the guide's redrawn alpha/anatomy.
        coded=np.asarray(guide.crop(tuple(box))).copy()
        coded[:,:,3]=np.where(component_mask,coded[:,:,3],0)
        size=tuple(record['size'])
        scaled=image.resize(size,Image.Resampling.LANCZOS)
        coded=Image.fromarray(coded).resize(size,Image.Resampling.LANCZOS)
        indices,mask,base=blood.quantize_blood(scaled,coded,normal,alternate)
        assert int(mask.sum())>=8,'Every actual split wound must be classified'
        assert np.array_equal(indices[~mask],base[~mask]) and np.array_equal(indices==0,base==0)
        assert set(np.unique(indices[mask])).issubset(blood.BLOOD_PENS)
        at,length=record['pixelOffset'],record['packedBytes']
        previous=decoder.decode(source[at:at+length],indices.size).reshape(indices.shape)
        assert np.array_equal(previous,base),'Immutable original native source raster'
        packed=packer.pack_indices(indices.tobytes())
        assert len(packed)==length and np.array_equal(decoder.decode(packed,indices.size).reshape(indices.shape),indices)
        payload[at:at+length]=packed;spans.append((at,at+length))
        changed=int(np.count_nonzero(indices!=base));assert changed>0
        records.append(dict(pose=pose,kind=kind,bloodPixels=int(mask.sum()),changedIndices=changed,
            sourceCrop=box,size=list(size),pixelOffset=at,packedBytes=length,
            alphaUnchanged=True,nonbloodIndicesUnchanged=True,
            changedMaskSHA256=hashlib.sha256(mask.tobytes()).hexdigest().upper()))
        for costume,palette in enumerate((normal,alternate)):
            picture=colors.decoded(indices,palette)
            picture.save(OUT/f'kano-{pose}-{("normal","alternate")[costume]}.png')
            x,y=pose*140,costume*180
            draw.text((x+3,y+3),f'Kano{pose} c{costume} blood{int(mask.sum())}',fill='white')
            preview.alpha_composite(picture,(x+(140-picture.width)//2,y+175-picture.height))
changed_bytes=[i for i,(a,b) in enumerate(zip(source,payload)) if a!=b]
assert changed_bytes and all(any(lo<=i<hi for lo,hi in spans) for i in changed_bytes)
assert payload[0x1c3800:0x1c4000]==source[0x1c3800:0x1c4000]
path=OUT/'roms/mk2ks/mk2ks.mdata';path.parent.mkdir(parents=True);path.write_bytes(payload)
preview.save(OUT/'kano-normal-alternate-blood-preview.png')
report=dict(scope='Kano split blood indices only; native runtime/alternate selection unverified',
    sourcePayloadSHA256=digest(SOURCE),payloadSHA256=digest(path),inputHashes=pins,
    bloodPens=list(blood.BLOOD_PENS),poses=records,changedPackedBytes=len(changed_bytes),
    classifiedBloodPixels=sum(r['bloodPixels']for r in records),
    changedIndices=sum(r['changedIndices']for r in records),
    everyNonbloodIndexAndAlphaUnchanged=True,sonyaAndEveryOtherMoveAssetUnchanged=True,
    nativeDescriptorsStreamsTablesAndPalettesUnchanged=True,guestCodeChanged=False,
    guidePixelsDisplayedInGame=False,runtimeAccepted=False,naturalAlternateSelectionAccepted=False,
    fullPortAccepted=False)
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','poses')},indent=2))
