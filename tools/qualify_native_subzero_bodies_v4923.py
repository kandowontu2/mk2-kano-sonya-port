"""Exact reviewed initializer plus independently decoded owned native body data."""
import copy,hashlib,json,re,struct,subprocess
from pathlib import Path
import run_native_subzero_offset_regression_v4856 as native
import build_native_death_art_v900 as scalar

ROOT,need,sha=native.ROOT,native.need,native.sha
SOURCE=ROOT/'source_v4922_native_subzero_bodies/midtunit_m.cpp'
BASE=ROOT/'source_v4844_native_subzero_victim_offset/midtunit_m.cpp'
ASSET=ROOT/'asset_v4928_native_subzero_bodies'
OUT=ROOT/'audit_v4924_native_subzero_bodies_source_checked'
BLOCK_SHA='D1AED12DD115D34BEAE20909BE954E1CA77327D02AB8BF785D49D50BB663277C'

def source_gate(text,base):
 a=text.index('\t// Dedicated true17/18 frozen bodies');b=text.index('\n\t// Reptile',a)
 block=text[a:b]
 need(text[:a]+text[b+1:]==base,'Every pre-existing source byte outside one initializer block retained')
 need(hashlib.sha256(block.encode()).hexdigest().upper()==BLOCK_SHA,'Exact reviewed data-only native initializer')
 return block

def data_gate(base,original,payload,asset):
 need(len(payload)==len(original)==0x200000,'Exact current native payload region size')
 header=struct.unpack_from('<4s18I',payload,0x1f6400)
 need(header[0]==b'KSF1'and list(header[1:])==asset['headerExpected'],'Exact native body header')
 allowed=((0x1f6400,0x1f6700),(0x1d0800,0x1d2800),(0x1e0800,0x1e2800))
 need(all(any(a<=i<b for a,b in allowed)for i,(v,w)in enumerate(zip(original,payload))if v!=w),
      'No unrelated native payload changes')
 need(all(original[a:b]==b'\xff'*(b-a)for a,b in allowed),'Every owned storage span originally unused')
 for index,fighter in enumerate(asset['fighters']):
  need(fighter['identity']==17+index and fighter['bounds'][3]==139+index,'Actual own identity/floor anchor')
  pointers=[]
  for part,record in enumerate(fighter['parts']):
   at=0x1f6500+(index*3+part)*20
   width,height,xo,yo,graphic,command,palette,pad=struct.unpack_from('<4hIHIH',payload,at)
   rect=record['rect'];left,top=fighter['bounds'][:2]
   need((width,height,xo,yo)==(rect[2]-rect[0],rect[3]-rect[1],-(left+rect[0]),-(top+rect[1]))
        and command==0x6000 and palette==0xffb06ae0 and pad==0,'Actual native rectangle, anchor, ice palette and stride')
   pixel=record['pixelOffset'];packed=payload[pixel:pixel+record['packedBytes']]
   raw=scalar.unpack(packed,width*height)
   need(hashlib.sha256(raw).hexdigest().upper()==record['indicesSHA256']and max(raw)<64 and any(raw),
        'Every actual native packed component independently decoded')
   first=0x1fa0000+(asset['fighters'][0]['pixelBytes']if index else 0)
   pool=(0x1d0800,0x1e0800)[index]
   need(graphic==(first+pixel-pool)*8,'Exact non-overlapping native graphics addressing')
   pointers.append(0xff800000+(0xac400+(index*3+part)*20)*8)
  need(struct.unpack_from('<4I',payload,0x1f6580+index*16)==(*pointers,0)
       and struct.unpack_from('<3I',payload,0x1f66d0+index*12)==(*pointers[:2],0),
       'Three whole-body pieces and original-order two retained legs; native zero terminators')
 whole=struct.unpack_from('<19I',payload,0x1f65c0);legs=struct.unpack_from('<19I',payload,0x1f6680)
 old=struct.unpack_from('<12I',base,(0xff8c2890-0xff800000)//8)
 need(whole[:12]==old and whole[12:17]==(old[11],)*5,'Native original whole-body/clamped rows retained')
 for identity in range(65536):
  if identity not in (17,18):need(whole[identity if identity<=18 else 11]==old[min(identity,11)],'Every other unsigned whole-body identity preserved')
 need(whole[17:]==(0xffd62400,0xffd62480)and legs[17:]==(0xffd62900,0xffd62960),
      'Dedicated true17/18 whole-body and retained-leg groups')
 need(legs[:17]==struct.unpack_from('<17I',base,(0xff8c3110-0xff800000)//8),'All17 existing native leg lookup cells preserved')
 guest=bytearray(base)
 for src,dst,count in ((0x1f6500,0xac400,120),(0x1f6580,0xac480,32),(0x1f65c0,0xac4c0,76),
                       (0x1f66d0,0xac520,24),(0x1f6680,0xac540,76)):
  need(base[dst:dst+count]==b'\xff'*count,'Unused initialized guest program storage')
  guest[dst:dst+count]=payload[src:src+count]
 need(struct.unpack_from('<4H',base,(0xff8c2650-0xff800000)//8)==(0x0b49,0xfff4,0xc202,0x09c9),
      'Original CMPI11/JRLS/MOVI11 flow intact')
 struct.pack_into('<H',guest,(0xff8c2660-0xff800000)//8,0xffed)
 struct.pack_into('<I',guest,(0xff8c26c0-0xff800000)//8,0xffd62600)
 struct.pack_into('<I',guest,(0xff8c3090-0xff800000)//8,0xffd62a00)
 need(struct.unpack_from('<H',guest,(0xff8c2690-0xff800000)//8)[0]==11,'Out-of-range native MOVI11 clamp retained')
 result=hashlib.sha256(guest).hexdigest().upper()
 need(result==asset['expectedGuestSHA256'],'Independent whole initialized guest agrees with encoder')
 return result

def main():
 need(not OUT.exists(),'Fresh source/data qualification')
 need(sha(BASE)=='BAF102148E740A1CC96A44320E51051938E3AE4EADE5B716CD6B6D2534B252A6','Actual compiled4850 base source')
 text=SOURCE.read_text();base_text=BASE.read_text();block=source_gate(text,base_text)
 asset=json.loads((ASSET/'report.json').read_text());payload=(ASSET/'roms/mk2ks/mk2ks.mdata').read_bytes()
 original=(ROOT/native.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes();guest=native.expected()
 expected=data_gate(guest,original,payload,asset);source_faults=[];data_faults=[]
 for label,before,after in (('missing_legs_redirect','write32(rom_offset(0xff8c3090),native_address(ice_native_legs_table));',''),
  ('wrong_bound','uint16_t(~18)','uint16_t(~11)'),('wrong_part_count','ice_descriptors,120','ice_descriptors,100'),
  ('wrong_palette','ice_palette=0xffb06ae0','ice_palette=0xffaf84a0'),('invalid_pixel_limit','ice_gfx_limit=0x1fa4000','ice_gfx_limit=0x1fe4000'),
  ('lost_stock_semantics','std::min(row,11U)','std::min(row,18U)')):
  need(text.count(before)==1,'Unique actual source fault anchor')
  try:source_gate(text.replace(before,after,1),base_text)
  except ValueError as e:source_faults.append(dict(fault=label,rejectedBy=str(e)))
  else:raise ValueError('Source fault accepted '+label)
 for label,at,fmt,value in (('wrong_whole_identity',0x1f65c0+17*4,'<I',0xff8c2e10),
  ('wrong_legs_identity',0x1f6680+18*4,'<I',0xff8c3590),('missing_terminator',0x1f6580+12,'<I',0xffffffff),
  ('wrong_native_palette',0x1f6500+14,'<I',0xffaf84a0),('wrong_ground_anchor',0x1f6500+6,'<h',0),
  ('wrong_native_pixel',asset['fighters'][0]['parts'][0]['pixelOffset'],'<B',0),('unrelated_payload_change',0x100,'<B',0)):
  altered=bytearray(payload);struct.pack_into(fmt,altered,at,value)
  need(altered!=payload,'Actual data fault changes a byte')
  try:data_gate(guest,original,altered,asset)
  except ValueError as e:data_faults.append(dict(fault=label,rejectedBy=str(e)))
  else:raise ValueError('Native data fault accepted '+label)
 pins={str(p.resolve()):sha(p)for p in (SOURCE,BASE,Path(__file__).resolve(),ASSET/'report.json',ASSET/'roms/mk2ks/mk2ks.mdata',
  ROOT/'audit_v4914_earned_subzero_offset_matrix_checked/report.json',ROOT/native.NAME/'build-info.json')}
 for p,h in asset['inputHashes'].items():need(sha(p)==h,'Exact encoder inputs');pins[p]=h
 result=dict(passed=True,stagedSource=str(SOURCE),stagedSourceSHA256=sha(SOURCE),baseCompiledSource=str(BASE),
  baseCompiledSourceSHA256=sha(BASE),expectedGuestSHA256=expected,initializedGuestByteDelta=273,
  actualSourceFaultsRejected=source_faults,actualNativeDataFaultsRejected=data_faults,inputHashes=pins,
  originalNativeSourceOutsideOneBlockUnchanged=True,originalNativeTaskAudioCleanupUnchanged=True,
  wholeBodyUnsignedIdentitiesChecked=65536,originalLegRowsPreserved=17,compiledFixAccepted=False,fullPortAcceptance=False)
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress before proof')
 (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(passed=True,expectedGuestSHA256=expected,sourceFaults=len(source_faults),dataFaults=len(data_faults)),indent=2),flush=True)

if __name__=='__main__':main()
