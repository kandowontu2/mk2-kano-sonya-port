"""Independent staged semantic-leg data/source checks; not native execution acceptance."""
import hashlib,json,struct,subprocess
from pathlib import Path
import native_subzero_body_context_v4932 as native
import build_native_death_art_v900 as scalar

ROOT,need,sha=native.ROOT,native.need,native.sha
SOURCE=ROOT/'source_v4985_native_subzero_legs/midtunit_m.cpp'
BASE=ROOT/'source_v4922_native_subzero_bodies/midtunit_m.cpp'
ASSET=ROOT/'asset_v4984_native_subzero_legs'
OUT=ROOT/'audit_v4988_native_subzero_legs_source_checked'
BLOCK_SHA='D16CF40E502B48036B3A7D15329CBB455B08C547FF9FF5E92DDB912B5EDE1FDA'
GUEST_SHA='5255F3D3870BF9E10999DF79BFD1E15AC892533F38BA1922E981060D2E84ED30'

def digest(b):return hashlib.sha256(b).hexdigest().upper()
def source_gate(text,base):
 anchor='\n\t// Reptile';a=base.index(anchor);b=text.index(anchor)
 need(text[:a]+text[b:]==base,'All original compiled source bytes outside one initializer retained')
 block=text[a:b];need(digest(block.encode())==BLOCK_SHA,'Exact reviewed semantic-legs data-only initializer')
 return block

def data_gate(guest,original,payload,asset):
 need(len(original)==len(payload)==0x200000,'Current exact payload extent')
 header=(0x1d2800,3720,0x1e2800,3312,0x1fa4000,0x1f6800,0xac600,4,20,0x1f6880,0xac680,0xac540,0xffb06ae0,19)
 need(struct.unpack_from('<4s14I',payload,0x1f6700)==(b'KSL1',*header),'Independent exact native metadata')
 allowed=((0x1f6700,0x1f6900),(0x1d2800,0x1d4000),(0x1e2800,0x1e4000))
 need(all(original[a:b]==b'\xff'*(b-a)for a,b in allowed),'Actual unoccupied parent payload pools')
 need(all(any(a<=i<b for a,b in allowed)for i,(v,w)in enumerate(zip(original,payload))if v!=w),
      'Every old whole-body/legs/other payload byte retained')
 for fighter,width,height,left,top,pool,first,padded,total in((0,31,80,-24,59,0x1d2800,0x1fa4000,1860,3720),
                                                          (1,29,76,-26,64,0x1e2800,0x1fa4e88,1656,3312)):
  record=asset['fighters'][fighter]
  need(record['identity']==17+fighter and record['bounds']==[left,top,left+width*2,top+height]
       and record['pixelBytes']==total,'Exact own identity and staged floor coordinates')
  pointers=[];pieces=[]
  for part in range(2):
   at=0x1f6800+(fighter*2+part)*20
   need(struct.unpack_from('<4hIHIH',payload,at)==(width,height,-(left+part*width),-top,
        (first+part*padded)*8,0x6000,0xffb06ae0,0),'Actual original raw six-bit DMA layout, native ice palette, anchor')
   packed_len=(width*height*6+7)//8;pixel=pool+part*padded
   raw=scalar.unpack(payload[pixel:pixel+packed_len],width*height)
   need(digest(raw)==record['parts'][part]['indicesSHA256']and any(raw)and max(raw)<64,
        'Independent actual six-bit component decoded pixel-for-pixel')
   need(payload[pixel+packed_len:pixel+padded]==b'\xff'*(padded-packed_len),'Unwritten alignment padding remains native parent bytes')
   pieces.append(raw);pointers.append(0xff800000+(0xac600+(fighter*2+part)*20)*8)
  joined=b''.join(pieces[0][y*width:(y+1)*width]+pieces[1][y*width:(y+1)*width]for y in range(height))
  need(digest(joined)==record['wholeIndicesSHA256'],'Native two-part union equals entire encoded semantic master')
  need(struct.unpack_from('<3I',payload,0x1f6880+fighter*12)==(*pointers,0),'Actual native two-leg group and zero terminator')
 need(guest[0xac600:0xac700]==b'\xff'*0x100,'Actual full guest allocation unused')
 need(struct.unpack_from('<2I',guest,0xac540+17*4)==(0xffd62900,0xffd62960),'Current actual own-character native rows')
 g=bytearray(guest);g[0xac600:0xac650]=payload[0x1f6800:0x1f6850];g[0xac680:0xac698]=payload[0x1f6880:0x1f6898]
 struct.pack_into('<2I',g,0xac540+17*4,0xffd63400,0xffd63460)
 need(g[0xac540:0xac540+17*4]==guest[0xac540:0xac540+17*4],'All17 native stock leg rows preserved')
 need(digest(g)==GUEST_SHA==asset['expectedGuestSHA256'],'Independent full initialized guest expectation')
 return GUEST_SHA

def main():
 need(not OUT.exists(),'Fresh immutable staging qualification')
 text,base=SOURCE.read_text(),BASE.read_text();source_gate(text,base)
 native.expected();guest=native.expected()
 original=(ROOT/native.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 asset=json.loads((ASSET/'report.json').read_text());payload=(ASSET/'roms/mk2ks/mk2ks.mdata').read_bytes()
 expected=data_gate(guest,original,payload,asset);source_faults=[];data_faults=[]
 for label,before,after in(
  ('wrong_leg_row','ice_native_legs_table+(17+fighter)*4','ice_native_legs_table+(0+fighter)*4'),
  ('missing_GFX_storage_guard','if (gfx[at]) fatalerror("MK2KS: semantic frozen legs GFX storage occupied");',''),
  ('wrong_descriptor_copy','own_legs_descriptors,80','own_legs_descriptors,60'),
  ('wrong_semantic_palette','donor32(at+14)!=ice_palette','donor32(at+14)!=0xffaf84a0'),
  ('wrong_floor','own_legs_top[2]={59,64}','own_legs_top[2]={60,65}')):
  # These anchors are reviewed inside the new block only; prior initializer untouched.
  start=base.index('\n\t// Reptile');stop=text.index('\n\t// Reptile');block=text[start:stop]
  need(before in block,'Actual staged source fault anchor')
  altered=text[:start]+block.replace(before,after,1)+text[stop:]
  try:source_gate(altered,base)
  except ValueError as e:source_faults.append(dict(fault=label,rejectedBy=str(e)))
  else:raise ValueError('Source fault admitted '+label)
 for label,at,fmt,value in(
  ('wrong_header',0x1f6700+8,'<I',0xffffffff),('wrong_own_group',0x1f6880,'<I',0xffd62900),
  ('missing_terminator',0x1f6880+8,'<I',1),('wrong_ground_anchor',0x1f6800+6,'<h',-60),
  ('opaque_zero_flags',0x1f6800+12,'<H',0x6001),('wrong_palette',0x1f6800+14,'<I',0xffaf84a0),
  ('wrong_graphics',0x1f6800+8,'<I',0x1fa0000*8),
  ('altered_native_pixel',0x1d2800,'<B',payload[0x1d2800]^1),('unrelated_payload_change',0x100,'<B',payload[0x100]^1)):
  altered=bytearray(payload);struct.pack_into(fmt,altered,at,value);need(altered!=payload,'Real counterexample changes bytes')
  try:data_gate(guest,original,altered,asset)
  except ValueError as e:data_faults.append(dict(fault=label,rejectedBy=str(e)))
  else:raise ValueError('Data fault admitted '+label)
 pins={str(p.resolve()):sha(p)for p in(SOURCE,BASE,Path(__file__),Path(native.__file__),Path(scalar.__file__),
       ASSET/'report.json',ASSET/'roms/mk2ks/mk2ks.mdata',ROOT/'tools/build_native_subzero_legs_v4983.py')}
 for p,h in asset['inputHashes'].items():need(sha(p)==h,'Actual immutable encoding inputs');pins[p]=h
 result=dict(passed=True,stagedSource=str(SOURCE),stagedSourceSHA256=sha(SOURCE),
    exactInitializerBlockSHA256=BLOCK_SHA,expectedGuestSHA256=expected,payloadSHA256=digest(payload),
    initializedGuestByteDelta=92,nativeGraphicsBytes=7032,sourceNegativeFaults=source_faults,dataNegativeFaults=data_faults,
    originalNativeCodeWholeBodiesStockLegRowsAudioAndCleanupUnchanged=True,inputHashes=pins,
    actualCompiledGFXAllocationNotYetObserved=True,nativeAnchorAccepted=False,
    compiledFixAccepted=False,runtimeAccepted=False,artAccepted=False,fullPortAcceptance=False)
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress staging proof')
 (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(passed=True,guestSHA256=expected,sourceFaults=len(source_faults),dataFaults=len(data_faults),nativeCompiled=False),indent=2),flush=True)

if __name__=='__main__':main()
