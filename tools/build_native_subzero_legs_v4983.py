"""Format conversion of the selected semantic legs master, not hand masking/painting.

Keep current whole-body descriptors and all native execution code immutable.
Only true17/18 retained-leg lookup pointers change in the expected guest.
Anchors are staged hypotheses until direct native RGB/grounding inspection.
"""
import hashlib,json,struct,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
import native_subzero_body_context_v4932 as native
import build_native_projectile_impacts as codec
import build_native_death_art_v900 as scalar
import build_native_pit_fall_v2 as colors
import upgrade_ksui_previews as ui

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'asset_v4984_native_subzero_legs'
HEADER,DESC,GROUPS=0x1f6700,0x1f6800,0x1f6880
ROM_DESC,ROM_GROUPS,ROM_LEGS_TABLE=0xac600,0xac680,0xac540
PIXELS,LIMITS=(0x1d2800,0x1e2800),(0x1d4000,0x1e4000)
GFX,GFX_LIMIT,PALETTE=0x1fa4000,0x1fa7000,0xffb06ae0
MASTER_SHA='D9E7CA72B91479803E84E15E6C7CE48F2CAE9906F1ABF548DE3CC7BB86B1E0C3'
SOURCE_SHA='08D87AC46142687CEE2A13A81F4C7B78268C8AA99D3020F3AF21693058F00C08'

def digest(b):return hashlib.sha256(b).hexdigest().upper()
def address(o):return 0xff800000+o*8
def expected_guest(base,payload):
 g=bytearray(base)
 for src,dst,count in((DESC,ROM_DESC,80),(GROUPS,ROM_GROUPS,24)):
  need(base[dst:dst+count]==b'\xff'*count,'Proven unused initialized descriptor/group pool')
  g[dst:dst+count]=payload[src:src+count]
 need(struct.unpack_from('<2I',base,ROM_LEGS_TABLE+17*4)==(0xffd62900,0xffd62960),'Actual existing true17/18 legs rows')
 struct.pack_into('<2I',g,ROM_LEGS_TABLE+17*4,address(ROM_GROUPS),address(ROM_GROUPS+12))
 return bytes(g)

def main():
 need(not OUT.exists(),'Fresh immutable semantic legs encoding')
 source_path=ROOT/native.NAME/'roms/mk2ks/mk2ks.mdata';source=source_path.read_bytes()
 need(digest(source)==SOURCE_SHA and len(source)==0x200000,'Actual current immutable whole-body payload')
 guest=native.expected();master=ROOT/'art_native_subzero_legs_v4978/kano-sonya-frozen-legs.png'
 need(sha(master)==MASTER_SHA,'Exact selected built-in generated legs-only master')
 free=((HEADER,0x1f6900),*zip(PIXELS,LIMITS))
 for a,b in free:need(source[a:b]==b'\xff'*(b-a),'Actual existing payload pool unused')
 need(guest[0xac600:0xac700]==b'\xff'*0x100,'Actual guest pool unused')
 image=Image.open(master).convert('RGBA');need(image.size==(1774,887),'Exact selected atlas framing')
 po=(PALETTE-0xff800000)//8;need(struct.unpack_from('<H',guest,po)[0]==64,'Native ice palette size')
 palette=np.array([ui.xrgb555(struct.unpack_from('<H',guest,po+2+i*2)[0])for i in range(64)],dtype=np.uint8)
 payload=bytearray(source);records=[];previews=[];total=0;lengths=[]
 for fighter,name,height,floor,center,bbox in((0,'kano',80,139,7,(402,299,814,832)),
                                           (1,'sonya',76,140,3,(215,315,608,830))):
  cell=image.crop((fighter*887,0,(fighter+1)*887,887));rgba=np.asarray(cell)
  yy,xx=np.where(rgba[:,:,3]>=128)
  actual=(int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1))
  need(actual==bbox,'Actual selected semantic alpha bounds')
  crop=cell.crop(bbox);factor=height/crop.height;width=round(crop.width*factor)
  indices=colors.quantize(crop.resize((width,height),Image.Resampling.LANCZOS),palette)
  left=round(center-width/2);top=floor-height;split=width//2
  assembled=np.zeros_like(indices);cursor=PIXELS[fighter];parts=[]
  for part,(x0,x1)in enumerate(((0,split),(split,width))):
   raw=indices[:,x0:x1].tobytes();packed=codec.pack_indices(raw)
   need(scalar.unpack(packed,len(raw))==raw and any(raw)and max(raw)<64,'Independent six-bit round trip')
   need(cursor+len(packed)<=LIMITS[fighter],'Bounded unused per-character pixel pool')
   descriptor=DESC+(fighter*2+part)*20;native_desc=address(ROM_DESC+(fighter*2+part)*20)
   gfx=(GFX+total+cursor-PIXELS[fighter])*8
   struct.pack_into('<4hIHIH',payload,descriptor,x1-x0,height,-(left+x0),-top,gfx,0x6000,PALETTE,0)
   payload[cursor:cursor+len(packed)]=packed
   assembled[:,x0:x1]=np.frombuffer(scalar.unpack(packed,len(raw)),dtype=np.uint8).reshape(height,x1-x0)
   parts.append(dict(order=part,rect=[x0,0,x1,height],descriptor=f'{native_desc:08X}',
                     payloadOffset=descriptor,graphic=f'{gfx:08X}',pixelOffset=cursor,
                     packedBytes=len(packed),indicesSHA256=digest(raw)))
   cursor=(cursor+len(packed)+3)&~3
  need(np.array_equal(assembled,indices),'Two-leg native union equals uniformly scaled semantic master')
  count=cursor-PIXELS[fighter];lengths.append(count);total+=count
  struct.pack_into('<3I',payload,GROUPS+fighter*12,*[int(p['descriptor'],16)for p in parts],0)
  records.append(dict(fighter=name,identity=17+fighter,sourceAlphaBox=list(bbox),size=[width,height],
     bounds=[left,top,left+width,floor],uniformScale=factor,alphaCutoff=128,parts=parts,
     legsGroup=f'{address(ROM_GROUPS+fighter*12):08X}',pixelBytes=count,
     wholeIndicesSHA256=digest(indices.tobytes()),nativeAnchorAccepted=False))
  previews.append(colors.decoded(assembled,palette))
 need(total<=GFX_LIMIT-GFX,'Bounded additional native GFX span')
 header=(PIXELS[0],lengths[0],PIXELS[1],lengths[1],GFX,DESC,ROM_DESC,4,20,
         GROUPS,ROM_GROUPS,ROM_LEGS_TABLE,PALETTE,19)
 struct.pack_into('<4s14I',payload,HEADER,b'KSL1',*header)
 changes=[i for i,(a,b)in enumerate(zip(source,payload))if a!=b]
 need(all(any(a<=i<b for a,b in free)for i in changes),'Only independently unused native payload spans changed')
 repaired=expected_guest(guest,payload)
 allowed_guest=((ROM_DESC,ROM_DESC+80),(ROM_GROUPS,ROM_GROUPS+24),
                (ROM_LEGS_TABLE+17*4,ROM_LEGS_TABLE+19*4))
 need(all(any(a<=i<b for a,b in allowed_guest)for i,(v,w)in enumerate(zip(guest,repaired))if v!=w),
      'Every native execution byte/stock row/whole-body descriptor remains unchanged')
 pins={str(p.resolve()):sha(p)for p in(source_path,master,ROOT/'art_native_subzero_legs_v4978/generation-prompts.json',
       Path(__file__),Path(native.__file__),Path(codec.__file__),Path(scalar.__file__),Path(colors.__file__),Path(ui.__file__))}
 report=dict(passed=True,scope=__doc__,fighters=records,inputHashes=pins,headerExpected=list(header),
    sourcePayloadSHA256=SOURCE_SHA,payloadSHA256=digest(payload),expectedGuestSHA256=digest(repaired),
    initializedGuestByteDelta=sum(a!=b for a,b in zip(guest,repaired)),payloadChangedBytes=len(changes),
    nativeGraphicsBytes=total,nativeGFXSpan=[GFX,GFX+total],allowedPayloadSpans=list(free),
    allowedGuestSpans=list(allowed_guest),stockLegRows0Through16Unchanged=True,
    wholeBodiesTasksAudioAndCleanupUnchanged=True,independentSixBitRoundTrip=True,
    semanticMasterContainsNoHands=True,compiledNativeGFXStorageGuardRequired=True,
    nativeCompiled=False,runtimeAccepted=False,artAccepted=False,fullPortAcceptance=False)
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress generated payload/proof')
 folder=OUT/'roms/mk2ks';folder.mkdir(parents=True);(folder/'mk2ks.mdata').write_bytes(payload)
 for record,preview in zip(records,previews):
  preview.resize((preview.width*3,preview.height*3),Image.Resampling.NEAREST).save(OUT/(record['fighter']+'-decoded-native.png'))
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k]for k in('payloadSHA256','expectedGuestSHA256','initializedGuestByteDelta','nativeGraphicsBytes')},indent=2),flush=True)

if __name__=='__main__':main()
