"""Bounded native true-ID palette proof; does not accept missing death art."""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BEFORE=ROOT/'audit_v864_sonya_p2_reptile_replay/guest_maincpu.bin'
AFTER=ROOT/'audit_v876_sonya_p2_native_headless_palette/guest_maincpu.bin'
CANDIDATE=ROOT/'diagnostic_v873_native_headless_palettes'
CASES=('audit_v876_sonya_p2_native_headless_palette',
       'audit_v878_kano_p2_native_headless_palette','audit_v878_sonya_p2_head_bite_scout')
EXE='CFF2453AA529CB3B06744CFED5F4E52F235A20A4E0C2EFA1C89F60D3445D0F23'
PAYLOAD='7896C93822473376AD724BB5E747EDE88C198203786F3F9B928CD1D860BAE019'
GUEST='91B5629C930AEA0BDA07833B3C40E1CD8667E71A3043379CFAE86BBB99E7F071'
def sha(data):return hashlib.sha256(data).hexdigest().upper()
def digest(path):return sha(path.read_bytes())
def at(address):return(address-0xff800000)//8
def records(text):
 return [(m[1],dict(re.findall(r'(\w+)=([^\s]+)',m[2])))
         for m in re.finditer(r'^MK2_NAT_CAMPAIGN_(\w+) (.*)$',text,re.M)]
def verify(before=None,after=None,texts=None,check_files=True):
 before=BEFORE.read_bytes()if before is None else before
 after=AFTER.read_bytes()if after is None else after
 texts={name:(ROOT/name/'run.log').read_text(encoding='utf-8-sig')for name in CASES}if texts is None else texts
 errors=[];pins={};summaries={}
 def need(ok,label):
  if not ok:errors.append(label)
 need(len(before)==len(after)==0x100000,'Complete guest snapshots')
 if len(before)!=0x100000 or len(after)!=0x100000:return {'passed':False,'errors':errors}
 need(sha(before)=='C52742158221D0221397D0D1709BE47012F3024AE21738BA1C8A178ECCF648EB','Exact preceding repaired guest')
 original=at(0xff90c900);storage=0xfa900;operand=at(0xff90c840)
 expected=bytearray(before)
 need(before[storage:storage+152]==b'\xff'*152,'Previously empty allocation')
 need(struct.unpack_from('<I',before,operand)[0]==0xff90c900,'Original palette operand')
 expected[storage:storage+136]=before[original:original+136]
 palettes={17:(0xfffed000,0xfff8a800),18:(0xfffed800,0xfff8b000)}
 for identity,values in palettes.items():
  struct.pack_into('<2I',expected,storage+identity*8,*values)
  for pointer in values:
   offset=at(pointer)
   need(struct.unpack_from('<H',after,offset)[0]==65 and
        after[offset:offset+130]==before[offset:offset+130],
        'Owned normal/alternate costume palettes preserved')
 struct.pack_into('<I',expected,operand,0xfffd4800)
 need(after==expected,'Only full native palette table and its one operand change')
 need(sha(after)==GUEST,'Exact current guest snapshot')
 for name,text in texts.items():
  capture=ROOT/name;result=json.loads((capture/'result.json').read_text(encoding='utf-8-sig'))
  need(result['exit_code']==0 and result['seconds']==1800 and result['human_slot']==2 and
       result['assistance']=='none'and result['cheats_enabled']is False,
       name+': cold unassisted terminal campaign')
  need(result['executable_sha256']==EXE and result['payload_sha256']==PAYLOAD,
       name+': matched executable/payload')
  if check_files:
   need(digest(capture/'guest_maincpu.bin')==GUEST,name+': actual matching guest dump')
   for filename,wanted in result['input_hashes'].items():
    path=Path(filename);need(path.is_file()and digest(path)==wanted,'Frozen input changed: '+filename)
    pins[filename]=wanted
   for filename in ('run.log','result.json','guest_maincpu.bin'):
    pins[str(capture/filename)]=digest(capture/filename)
  rows=records(text);identity=17 if result['player']=='kano'else 18
  need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',text,re.I),name+': no native/observer error')
  need(not any(tag in('REENTRY','CACHE_OVERWRITE')for tag,r in rows),name+': no reset/cache overrun')
  selected=[];physical=[];live=None;pending={};native_reads=0
  writers={1:{0xff836700,0xff825930,0xff9dece0,0xff9def40},
           2:{0xff836700,0xff825960,0xff9ded10,0xff9def70}}
  for tag,row in rows:
   if tag=='LIVE':
    live=row
    need(row['human']==f'{identity}:{identity}',name+': actual true character in combat')
   elif tag=='HEALTH':
    slot=int(row['slot']);pc=int(row['pc'],16)
    need(pc in writers[slot]and int(row['at'],16)==(0x010602f0 if slot==1 else 0x01060ec0),name+': exact physical-slot health writer')
    if pc==0xff836700:need(0<=int(row['after'])<=int(row['before'])<=161,name+': original collision damage bounds')
   elif tag=='HEADLESS_PALETTE':
    flags=int(row['flags'],16);alternate=bool(flags&0x40);part=int(row['part'])
    pointer=palettes[identity][int(alternate)]
    address=0xfffd4800+identity*64+int(alternate)*32
    need(row['row']==str(identity)and row['id']==str(identity)and
         int(row['at'],16)==address+(part%2)*16 and part==int(alternate)*2+part%2 and
         int(row['mask'],16)==0xffff and row['pc']=='FF90C8D0'and
         int(row['selected'],16)==address and
         int(row['data'],16)==((pointer>>(part%2*16))&0xffff),name+': exact native palette halfword')
    key=(row['frame'],row['actor'],row['main']);pending.setdefault(key,[]).append(row);native_reads+=1
   elif tag=='HEADLESS_PALETTE_SELECTED':
    key=(row['frame'],row['actor'],row['main']);fetched=pending.pop(key,[])
    flags=int(row['flags'],16);alternate=bool(flags&0x40)
    need(row['id']==str(identity)and row['pc']=='FF90C8E0'and
         int(row['pointer'],16)==palettes[identity][int(alternate)]and len(fetched)==2 and
         [int(r['part'])for r in fetched]==[int(alternate)*2,int(alternate)*2+1]and
         all(r['flags']==row['flags']for r in fetched),name+': actual pointer after both native reads')
    selected.append(row)
    if (live and row['actor']==live['human_actor']and row['main']==live['human_main']and
        0<=int(row['frame'])-int(live['frame'])<=30):
     physical.append(row)
  need(not pending,name+': complete native fetch pairs')
  terminal=[r for tag,r in rows if tag=='RESULT']
  need(len(terminal)==1 and terminal[0]['frame']=='98473'and int(terminal[0]['live_fields'])>40000,
       name+': full campaign chronology')
  if identity==18:need(len(physical)>=2,name+': actual physical Sonya palette uses, not just effects')
  summaries[name]={'selectedPointers':len(selected),'physicalVictimSelections':len(physical),
                   'nativeHalfwordReads':native_reads,'normalRuntime':any(not(int(r['flags'],16)&0x40)for r in physical),
                   'alternateRuntime':any(int(r['flags'],16)&0x40 for r in physical),
                   'headBiteObserved':any(t=='REPTILE_ROW'for t,r in rows),
                   'towerClear':False}
 # Same physical input/state chronology until the first repaired table use.
 tags={'BOOT','MORPH_ROM','ROM','STATE','LOSS','SELECT','SELECT_ID','SELECT_EXIT','FIGHT','STAGE','LIVE','DECISION','INPUT','SPECIAL','HEALTH','WIN','CPU_ID'}
 def prefix(text):
  return [line for line in text.splitlines()if(m:=re.match(r'MK2_NAT_CAMPAIGN_(\w+) frame=(\d+) ',line))and m[1]in tags and int(m[2])<27622]
 old_text=(ROOT/'audit_v864_sonya_p2_reptile_replay/run.log').read_text(encoding='utf-8-sig')
 a,b=prefix(old_text),prefix(texts[CASES[0]])
 need(len(a)>10000 and a==b,'Exact prior input/state chronology before first palette repair executes')
 if check_files:
  need(digest(CANDIDATE/'mkport_candidate.exe')==EXE,'Current exact executable')
  need(digest(CANDIDATE/'roms/mk2ks/mk2ks.mdata')==PAYLOAD,'Current unchanged graphics payload')
  for path in(BEFORE,AFTER,Path(__file__),ROOT/'audit_v864_sonya_p2_reptile_replay/run.log'):
   pins[str(path)]=digest(path)
 return {'passed':not errors,'errors':sorted(set(errors)),'native_palette_table_repair_proven':not errors,
         'guestChangedBytes':sum(a!=b for a,b in zip(before,after)),'preservedPrefixRecords':len(a),
         'cases':summaries,'kanoPaletteRuntimeProven':False,'alternatePaletteRuntimeProven':False,
         'completeHeadBiteRuntimeProven':False,'nativeDeathArtAccepted':False,'fullPortAcceptance':False,
         'inputHashes':pins}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 if args.output.exists():raise ValueError('Preserve existing proof')
 report=verify();args.output.mkdir();(args.output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2))
 raise SystemExit(0 if report['passed']else 1)
if __name__=='__main__':main()
