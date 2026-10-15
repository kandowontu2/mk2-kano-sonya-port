"""Encode existing ice-body masters into native three-piece and two-leg groups.

Format conversion only: alpha isolation, uniform scale, original ice palette,
lossless rectangular component partition, six-bit packing. No image painting.
"""
import hashlib,json,struct,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
import run_native_subzero_offset_regression_v4856 as native
import build_native_projectile_impacts as codec
import build_native_death_art_v900 as scalar
import build_native_pit_fall_v2 as colors
import upgrade_ksui_previews as ui

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'asset_v4921_native_subzero_bodies'
BASE=0xfe800000
HEADER,DESC,GROUPS,TABLE,LEGS_TABLE,LEGS_GROUPS=0x1f6400,0x1f6500,0x1f6580,0x1f65c0,0x1f6680,0x1f66d0
ROM_DESC,ROM_GROUPS,ROM_TABLE,ROM_LEGS,ROM_LEGS_TABLE=0xac400,0xac480,0xac4c0,0xac520,0xac540
PIXELS=(0x1d0800,0x1e0800);LIMITS=(0x1d2800,0x1e2800)
GFX=0x1fa0000;PALETTE=0xffb06ae0
MASTER='13F3938BED3E1337E8847FAAE7A6646DFF227CF02D943AF097C217A63D6F1E2F'

def digest(b):return hashlib.sha256(b).hexdigest().upper()
def off(a):return (a-0xff800000)//8
def address(o):return 0xff800000+o*8
def read(source,guest,a,fmt):
 b,o=(guest,off(a))if a>=0xff800000 else(source,(a-BASE)//8)
 return struct.unpack_from(fmt,b,o)

def expected_guest(base,payload):
 g=bytearray(base)
 for src,dst,count in ((DESC,ROM_DESC,120),(GROUPS,ROM_GROUPS,32),(TABLE,ROM_TABLE,76),
                       (LEGS_GROUPS,ROM_LEGS,24),(LEGS_TABLE,ROM_LEGS_TABLE,76)):
  need(g[dst:dst+count]==b'\xff'*count,'Exact unused initialized program span')
  g[dst:dst+count]=payload[src:src+count]
 need(struct.unpack_from('<H',base,off(0xff8c2660))[0]==0xfff4 and
      struct.unpack_from('<I',base,off(0xff8c26c0))[0]==0xff8c2890 and
      struct.unpack_from('<I',base,off(0xff8c3090))[0]==0xff8c3110,'Original native consumers unchanged')
 struct.pack_into('<H',g,off(0xff8c2660),(~18)&0xffff)
 struct.pack_into('<I',g,off(0xff8c26c0),address(ROM_TABLE))
 struct.pack_into('<I',g,off(0xff8c3090),address(ROM_LEGS_TABLE))
 return bytes(g)

def main():
 need(not OUT.exists(),'Fresh immutable native art payload')
 source_path=ROOT/native.NAME/'roms/mk2ks/mk2ks.mdata';source=source_path.read_bytes()
 need(digest(source)=='91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24','Exact current payload')
 guest=native.expected();master=ROOT/'art_native_subzero_v4888/kano-sonya-frozen-bodies.png'
 need(sha(master)==MASTER,'Exact selected existing art')
 need(source[HEADER:0x1f6700]==b'\xff'*(0x1f6700-HEADER),'Unused owned metadata span')
 for start,end in zip(PIXELS,LIMITS):need(source[start:end]==b'\xff'*(end-start),'Unused bounded pixel pool')
 need(guest[0xac400:0xac600]==b'\xff'*0x200,'Unused actual initialized program span')
 image=Image.open(master).convert('RGBA');need(image.size==(1774,887),'Exact master framing')
 count=struct.unpack_from('<H',guest,off(PALETTE))[0];need(count==64,'Original native ice palette')
 palette=np.array([ui.xrgb555(struct.unpack_from('<H',guest,off(PALETTE)+2+i*2)[0])for i in range(64)],dtype=np.uint8)
 payload=bytearray(source);records=[];previews=[];total=0;pixel_bytes=[]
 for fighter,name,identity,group in ((0,'kano',17,0xff011f60),(1,'sonya',18,0xff0320c0)):
  pointers=read(source,guest,group,'<3I');need(pointers[-1]==0,'Existing own dizzy topology')
  specs=[read(source,guest,p,'<4hIH')for p in pointers[:-1]]
  left=min(-s[2]for s in specs);right=max(-s[2]+s[0]for s in specs)
  top=min(-s[3]for s in specs);bottom=max(-s[3]+s[1]for s in specs)
  need((left,top,right,bottom)==((-23,9,37,139)if fighter==0 else(-25,14,32,140)),
       'Exact existing character-owned height and floor anchor')
  cell=image.crop((fighter*887,0,(fighter+1)*887,887));rgba=np.asarray(cell)
  yy,xx=np.where(rgba[:,:,3]>=128)
  bbox=(int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1))
  need(bbox==((443,182,786,821)if fighter==0 else(242,192,515,824)),'Exact selected alpha crop')
  crop=cell.crop(bbox);factor=(bottom-top)/crop.height
  width,height=round(crop.width*factor),bottom-top
  scaled=crop.resize((width,height),Image.Resampling.LANCZOS)
  indices=colors.quantize(scaled,palette);newleft=round((left+right-width)/2)
  split_y=round(height*0.48);split_x=width//2
  # Original group order: screen-left leg, screen-right leg, upper body.
  partitions=((0,split_y,split_x,height),(split_x,split_y,width,height),(0,0,width,split_y))
  assembled=np.zeros_like(indices);cursor=PIXELS[fighter];parts=[]
  for part,(x0,y0,x1,y1)in enumerate(partitions):
   raw=indices[y0:y1,x0:x1].tobytes();packed=codec.pack_indices(raw)
   need(scalar.unpack(packed,len(raw))==raw and any(raw)and max(raw)<64,'Independent6-bit round trip')
   need(cursor+len(packed)<=LIMITS[fighter],'Pixels inside proven free pool')
   desc=DESC+(fighter*3+part)*20;native_desc=address(ROM_DESC+(fighter*3+part)*20)
   graphic=(GFX+total+(cursor-PIXELS[fighter]))*8
   struct.pack_into('<4hIHIH',payload,desc,x1-x0,y1-y0,-(newleft+x0),-(top+y0),graphic,0x6000,PALETTE,0)
   payload[cursor:cursor+len(packed)]=packed
   assembled[y0:y1,x0:x1]=np.frombuffer(scalar.unpack(packed,len(raw)),dtype=np.uint8).reshape(y1-y0,x1-x0)
   parts.append(dict(order=part,rect=[x0,y0,x1,y1],descriptor=f'{native_desc:08X}',payloadOffset=desc,
                     graphic=f'{graphic:08X}',pixelOffset=cursor,packedBytes=len(packed),indicesSHA256=digest(raw)))
   cursor=(cursor+len(packed)+3)&~3
  need(np.array_equal(assembled,indices),'Three-part union identical to uniformly scaled/quantized whole art')
  byte_count=cursor-PIXELS[fighter];pixel_bytes.append(byte_count);total+=byte_count
  ptr=[int(p['descriptor'],16)for p in parts]
  struct.pack_into('<4I',payload,GROUPS+fighter*16,*ptr,0)
  struct.pack_into('<3I',payload,LEGS_GROUPS+fighter*12,*ptr[:2],0)
  previews.append(colors.decoded(assembled,palette))
  records.append(dict(fighter=name,identity=identity,sourceAlphaBox=bbox,uniformScale=factor,size=[width,height],
                      originalOwnDizzyBounds=[left,top,right,bottom],bounds=[newleft,top,newleft+width,bottom],
                      wholeGroup=f'{address(ROM_GROUPS+fighter*16):08X}',legsGroup=f'{address(ROM_LEGS+fighter*12):08X}',
                      alphaCutoff=128,parts=parts,wholeIndicesSHA256=digest(indices.tobytes()),pixelBytes=byte_count))
 stock=list(struct.unpack_from('<12I',guest,off(0xff8c2890)))
 whole=stock+[stock[11]]*5+[address(ROM_GROUPS),address(ROM_GROUPS+16)]
 legs=list(struct.unpack_from('<17I',guest,off(0xff8c3110)))+[address(ROM_LEGS),address(ROM_LEGS+12)]
 struct.pack_into('<19I',payload,TABLE,*whole);struct.pack_into('<19I',payload,LEGS_TABLE,*legs)
 expected=(PIXELS[0],pixel_bytes[0],PIXELS[1],pixel_bytes[1],GFX,DESC,ROM_DESC,6,20,GROUPS,ROM_GROUPS,TABLE,ROM_TABLE,
           LEGS_GROUPS,ROM_LEGS,LEGS_TABLE,ROM_LEGS_TABLE,PALETTE)
 struct.pack_into('<4s18I',payload,HEADER,b'KSF1',*expected)
 allowed=[(HEADER,0x1f6700),*[tuple(p)for p in zip(PIXELS,LIMITS)]]
 need(all(any(a<=i<b for a,b in allowed)for i,(v,w)in enumerate(zip(source,payload))if v!=w),'Only proven free payload spans changed')
 repaired=expected_guest(guest,payload)
 for identity in range(65536):
  if identity not in (17,18):
   old=stock[min(identity,11)];new=whole[identity if identity<=18 else11]
   need(old==new,'Every other unsigned victim whole-body semantic unchanged')
 need(legs[:17]==list(struct.unpack_from('<17I',guest,off(0xff8c3110))),'All existing legs-only ID-indexed cells unchanged')
 pins={str(p.resolve()):sha(p)for p in (source_path,master,ROOT/'art_native_subzero_v4888/generation-prompts_v4917.json',
       Path(__file__).resolve(),Path(codec.__file__),Path(scalar.__file__),Path(colors.__file__))}
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress before output')
 folder=OUT/'roms/mk2ks';folder.mkdir(parents=True);(folder/'mk2ks.mdata').write_bytes(payload)
 for record,preview in zip(records,previews):preview.resize((preview.width*3,preview.height*3),Image.Resampling.NEAREST).save(OUT/(record['fighter']+'-decoded-native.png'))
 report=dict(passed=True,scope=__doc__,inputHashes=pins,fighters=records,headerExpected=list(expected),
             sourcePayloadSHA256=digest(source),payloadSHA256=digest(payload),expectedGuestSHA256=digest(repaired),
             initializedGuestByteDelta=sum(a!=b for a,b in zip(guest,repaired)),nativeGraphicsBytes=total,
             originalWholeBodyRowsPreserved=12,originalLegsRowsPreserved=17,allOtherUnsignedWholeBodySemanticsPreserved=True,
             allowedPayloadSpans=allowed,payloadChangedBytes=sum(a!=b for a,b in zip(source,payload)),
             rectangularPartsUnionVerified=True,independentSixBitRoundTrip=True,originalNativeIcePalette=hex(PALETTE),
             originalTaskAudioAndCleanupCodeUnchanged=True,nativeCompiled=False,runtimeAccepted=False,artAccepted=False,fullPortAcceptance=False)
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k]for k in ('payloadSHA256','expectedGuestSHA256','initializedGuestByteDelta','nativeGraphicsBytes','payloadChangedBytes')},indent=2),flush=True)

if __name__=='__main__':main()
