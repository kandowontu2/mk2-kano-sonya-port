"""Independent cold physical mirror selection/flags/ownership/palette proof.

Not a general costume button claim, fatality proof, or full UI acceptance.
The native mirror behaviour is compared to the original Liu Kang control.
"""
import hashlib,json,re,struct
from pathlib import Path
import numpy as np
from PIL import Image
import verify_native_split_blood_v1133 as split
ROOT=split.ROOT
OUT=ROOT/'audit_v1144_natural_mirror_selection_checked'
CASES=tuple(f'audit_v1143_{name}_mirror_confirm_p{first}' for name in ('kano','sonya','liu_kang') for first in (1,2))

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def rows(text):
 return [(m[1],dict(re.findall(r'(\w+)=([^\s]+)',m[2]))) for m in re.finditer(r'^MK2_NATURAL_MIRROR_V1142_(\w+) (.*)$',text,re.M)]
def off(address):return (address-0xff800000)//8
def stock_palette(stock,address):
 at=off(address);count=struct.unpack_from('<H',stock,at)[0]
 assert count>=64
 pens=struct.unpack_from('<'+str(count)+'H',stock,at+2)
 return np.asarray([tuple(((pen>>shift)&31)*255//31 for shift in (10,5,0)) for pen in pens],dtype=np.uint8)

def verify():
 errors=[];pins={};summaries={}
 def need(ok,label):
  if not ok:errors.append(label)
 guest,_,_,_=split.reconstruct()
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
 source=ROOT/'mk2ks_natural_mirror_v1142.lua'
 text=source.read_text()
 need(not re.search(r'\b(?:p|cpu|gfx)\s*[:.]\s*(?:write\w*|set\w*)\s*\(',text),'No guest/cpu/graphics mutation in physical driver')
 # The actual flag-setting writer is native original code, not host replacement.
 need(guest[off(0xff8953c0):off(0xff8954d0)]==stock[off(0xff8953c0):off(0xff8954d0)],'Original mirror comparison/flag writer bytes retained')
 for case in CASES:
  directory=ROOT/case
  result=json.loads((directory/'result.json').read_text(encoding='utf-8-sig'))
  name,first=result['player'],result['confirm_first'];identity={'kano':17,'sonya':18,'liu_kang':1}[name]
  info=json.loads((ROOT/split.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
  need(result['candidate']==split.CANDIDATE and result['executable_sha256']==info['executable_sha256'] and result['payload_sha256']==info['payload_sha256'],'Exact build '+case)
  need(result['exit_code']==0 and result['seconds']==60 and result['assistance']=='none' and result['guest_writes']==0 and result['cheats_enabled'] is False,'Unassisted cold physical case '+case)
  for filename,wanted in result['input_hashes'].items():
   need(digest(Path(filename))==wanted,'Unchanged input '+filename);pins[filename]=wanted
  log=(directory/'run.log').read_text(encoding='utf-8-sig')
  need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',log,re.I),'No runtime errors '+case)
  data=rows(log);items=lambda tag:[r for t,r in data if t==tag]
  need(data and all(r['writes']=='0' and r['assistance']=='none' for _,r in data),'Read-only observations/physical input '+case)
  starts,ends,confirm=items('FIRST_LIVE'),items('RESULT'),items('CONFIRM')
  need(len(starts)==len(ends)==1 and len(confirm)==2,'Exactly one genuine match '+case)
  if len(starts)!=1 or len(ends)!=1 or len(confirm)!=2:continue
  start=starts[0];end=ends[0]
  actors=start['actors'].split(',');need(len(set(actors))==2,'Distinct real actor objects '+case)
  need(start['ids']==f'{identity},{identity}' and start['confirm_first']==str(first),'Selected real mirror identities '+case)
  order=sorted(confirm,key=lambda r:int(r['frame']))
  need(order[0]['slot']==str(first) and all(r['roster']==str(identity) for r in confirm),'Actual requested confirmation order '+case)
  need(int(end['frame'])==3283 and int(end['first_live'])==int(start['frame']) and int(end['live_fields'])>=1900 and end['fifo']=='true,true' and end['palettes']=='true,true','Live match through terminal without softlock '+case)
  writes=[r for r in items('FLAG_WRITE') if r['slot']=='2' and r['id']==str(identity) and (int(r['new'],16)^int(r['old'],16))&64]
  need(any(r['pc']=='FF895450' and int(r['new'],16)==int(r['old'],16)|64 and int(r['frame'])<int(start['frame']) for r in writes),'Original native selection sets P2 alternate bit '+case)
  states=items('STATE');need(len(states)>=120,'Sustained two-slot observations '+case)
  fifos,palettes=items('FIFO'),items('PALETTE')
  need(len(fifos)==len(palettes)==2,'Both physical bodies rendered and palettes captured '+case)
  for side in (1,2):
   own=[r for r in states if r['slot']==str(side)]
   need(len(own)>=60 and len({r['pose'] for r in own})>=3,'Native live animation advances P'+str(side)+' '+case)
   for r in own:
    need(r['actor']==r['owner']==actors[side-1] and r['id']==r['roster']==str(identity) and r['hp']=='161' and r['y']==r['floor'],'True identity/ownership/health/floor '+case)
    need(bool(int(r['flags'],16)&64)==(side==2),'Native mirror costume retained P'+str(side)+' '+case)
   fifo=next((r for r in fifos if r['slot']==str(side)),None)
   palette=next((r for r in palettes if r['slot']==str(side)),None)
   need(fifo is not None and palette is not None,'Physical render evidence '+case)
   if fifo is None or palette is None:continue
   need(fifo['actor']==fifo['owner']==actors[side-1] and fifo['id']==str(identity) and palette['actor']==actors[side-1] and palette['id']==str(identity),'Native FIFO and captured palette true owners '+case)
   if name!='liu_kang':
    offset={'kano':(0x92bbc,0x92c3e),'sonya':(0x92cf2,0x92d74)}[name][side-1]
    expected=split.body_palette(donor,offset)
   else:
    pointer=struct.unpack_from('<I',stock,off((0xff907910,0xff907b30)[side-1])+identity*4)[0]
    expected=stock_palette(stock,pointer)
   path=directory/palette['file'];raw=np.asarray(struct.unpack('<64I',path.read_bytes()),dtype=np.uint32)
   actual=np.stack(((raw>>16)&255,(raw>>8)&255,raw&255),axis=1)
   need(np.max(np.abs(actual[1:64].astype(int)-expected[1:64].astype(int)))<=1,'All actual native hardware costume pens P'+str(side)+' '+case)
   pins[str(path)]=digest(path)
  snapshots=items('SNAPSHOT');need(len(snapshots)==5,'Two selection and three actual live captures '+case)
  for r in snapshots:
   path=directory/'snap'/r['file'];need(Image.open(path).size==(400,254),'Actual full-scene capture '+case);pins[str(path)]=digest(path)
  need((directory/'guest_maincpu.bin').read_bytes()==guest,'Exact independently reconstructed whole guest '+case)
  inputs=items('INPUT')
  for side in (1,2):
   need(any(r['slot']==str(side) and r['button']=='Coin' for r in inputs) and any(r['slot']==str(side) and r['button']=='High_Punch' and int(r['frame'])==int(next(r for r in confirm if r['slot']==str(side))['frame']) for r in inputs),'Physical credits and selection confirm P'+str(side)+' '+case)
  for file in ('run.log','result.json','guest_maincpu.bin'):pins[str(directory/file)]=digest(directory/file)
  summaries[case]=dict(fighter=name,confirmFirst=first,physicalActors=actors,firstLive=int(start['frame']),liveFields=int(end['live_fields']),nativeAlternateSlot=2,actualPalettePensPerSlot=63,actualSceneCaptures=len(snapshots))
 need(len(summaries)==6,'Both owned mirror pairs and original control in both confirm orders')
 return dict(passed=not errors,errors=sorted(set(errors)),cases=summaries,inputHashes=pins,
  scope='Cold physical same-character two-human mirror selection, both confirmation orders; native P2 alternate assignment, real IDs/ownership, hardware palettes and sustained animation',
  naturalMirrorAlternateSelectionAccepted=not errors,arbitraryAlternateCostumeButtonAccepted=False,
  naturalAlternateFatalitiesAccepted=False,allSelectionGraphicsAccepted=False,allArenasAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
 if OUT.exists():raise ValueError('Preserve independent mirror evidence')
 report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('cases','inputHashes')},indent=2))
 raise SystemExit(0 if report['passed'] else 1)
