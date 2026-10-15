"""Cold mirror selection -> native alternate flag -> real combat -> own finisher.

This accepts only physical activation, native costume/palette continuity and
continuation in four Dead Pool mirror cases. It does not replace the final
component/DMA/pixel, donor choreography, audio or all-fatalities gates.
"""
import hashlib,json,re,struct
from pathlib import Path
import numpy as np
from PIL import Image
import verify_native_split_blood_v1133 as split
ROOT=split.ROOT
OUT=ROOT/'audit_v1169_natural_mirror_finish_checked'
CASES=tuple(f'audit_v1167_{name}_mirror_finish_winner_p{side}_confirm_p1' for name in ('kano','sonya') for side in (1,2))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def rows(text):
 return [(m[1],dict(re.findall(r'(\w+)=([^\s]+)',m[2]))) for m in re.finditer(r'^MK2_NATURAL_MIRROR_FINISH_V1166_(\w+) (.*)$',text,re.M)]
def off(address):return (address-0xff800000)//8
def colors(guest,at,count=64):
 words=struct.unpack_from('<'+str(count)+'H',guest,at+2)
 return np.asarray([sum(((((w>>shift)&31)<<3)|(((w>>shift)&31)>>2))<<dest for shift,dest in ((10,16),(5,8),(0,0))) for w in words],dtype=np.uint32)
def verify(texts=None,check_files=True):
 guest,_,_,_=split.reconstruct();errors=[];pins={};summaries={}
 def need(ok,label):
  if not ok:errors.append(label)
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in ((0xff8953c0,0xff8954d0),(0xff8366c0,0xff836710),(0xff82bbb0,0xff82bc30)):
  need(guest[off(lo):off(hi)]==stock[off(lo):off(hi)],'Original native mirror/damage/retirement code '+hex(lo))
 source=ROOT/'mk2ks_natural_mirror_finish_v1166.lua';text=source.read_text()
 need(not re.search(r'\b(?:p|cpu|gfx)\s*[:.]\s*(?:write\w*|set\w*)\s*\(|\.value\s*=(?!=)|load_?state',text),'No guest/CPU/gfx/loaded-state writes')
 need("local target_gap=68" in text and "10+(i-1)*10" in text and "age<begin+4" in text,'Exact physical command scenario')
 pins[str(source)]=digest(source)
 build=json.loads((ROOT/split.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
 for case in CASES:
  folder=ROOT/case;launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
  name,side=launch['player'],launch['winner'];victim=3-side;identity={'kano':17,'sonya':18}[name];label=' '+case
  need(launch['exit_code']==0 and launch['candidate']==split.CANDIDATE and launch['executable_sha256']==build['executable_sha256'] and launch['payload_sha256']==build['payload_sha256'],'Exact terminal candidate'+label)
  need(launch['confirm_first']==1 and launch['seconds']==95 and launch['assistance']=='none' and launch['guest_writes']==0 and launch['cheats_enabled'] is False,'Unassisted cold physical scenario'+label)
  for filename,wanted in launch['input_hashes'].items():
   if check_files:need(digest(Path(filename))==wanted,'Unchanged input '+filename)
   pins[filename]=wanted
  log=texts[case] if texts is not None else (folder/'run.log').read_text(encoding='utf-8-sig')
  need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',log,re.I),'No runtime error'+label)
  data=rows(log);items=lambda tag:[r for t,r in data if t==tag]
  need(bool(data) and all(r['writes']=='0' and r['assistance']=='none' for _,r in data),'Read-only observations'+label)
  starts,actions,wraps,stops=map(items,('FIRST_LIVE','ACTION','WRAP','RESULT'))
  need(len(starts)==len(actions)==len(wraps)==len(stops)==1,'One real match/finisher/completion/terminal'+label)
  if not all(len(x)==1 for x in (starts,actions,wraps,stops)):continue
  live,action,wrap,stop=starts[0],actions[0],wraps[0],stops[0];start=int(action['frame']);actors=live['actors'].split(',')
  need(live['ids']==f'{identity},{identity}' and len(set(actors))==2,'Two real mirror actors/IDs'+label)
  need(action['actor']==actors[side-1] and action['victim_actor']==actors[victim-1] and action['address']==('FFFAAE00' if name=='kano' else 'FFFAB200') and action['damage']=='322','Selected true own finisher/victim'+label)
  confirms=items('CONFIRM');need(len(confirms)==2 and [r['slot'] for r in confirms]==['1','2'] and all(r['roster']==str(identity) for r in confirms),'Physical mirror confirms'+label)
  # The CSS actor is naturally retired and a new combat actor is constructed.
  # Bind the original assignment to actual CSS confirmation, and separately
  # prove the bit and full hardware palette on the new physical combat actor.
  writes=[r for r in items('FLAG_WRITE') if r['slot']=='2' and r['id']==str(identity) and r['pc']=='FF895450']
  need(any(int(r['new'],16)==int(r['old'],16)|64 and int(r['old'],16)&64==0 and 0x01000000<=int(r['actor'],16)<0x01100000 and int(r['frame'])<min(int(c['frame']) for c in confirms) for r in writes),'Original game sets CSS alternate bit before confirmation'+label)
  need([bool(int(v,16)&64) for v in live['flags'].split(',')]==[False,True],'Native new physical combat actors inherit primary/alternate assignment'+label)
  inputs=items('INPUT')
  for n in (1,2):
   need(any(r['slot']==str(n) and r['button']=='Coin' for r in inputs) and any(r['slot']==str(n) and r['button']=='High_Punch' and r['frame']==next((c['frame'] for c in confirms if c['slot']==str(n)),'') for r in inputs),'Actual credits/confirm P'+str(n)+label)
  health=[r for r in items('HEALTH') if int(r['frame'])<start]
  expected=161;chains=0;total=0
  for r in health:
   before,after=int(r['before']),int(r['after'])
   need(r['pc']=='FF836700' and before==expected and 0<=after<before<=161,'Unbroken original native damage chain'+label)
   total+=before-after;expected=after
   if after==0:chains+=1;expected=161
  need(len(health)==10 and chains==2 and total==322 and len(items('WIN'))==2,'Two naturally earned KOs and wins'+label)
  approach=items('APPROACH');need(len(approach)==1 and 64<=int(approach[0]['gap'])<=72,'Physical reachable fatality spacing'+label)
  if approach:
   begin=int(approach[0]['frame']);own_inputs={(int(r['frame']),r['button']) for r in inputs if int(r['slot'])==side}
   direction='Right' if side==1 else 'Left';back='Left' if side==1 else 'Right'
   keys=[back,'Down',direction,'High_Kick'] if name=='kano' else [back,direction,'Down','Down','Low_Punch']
   # The driver stops assigning inputs after native activation. Last pulse
   # reaches the action on its third input field; no fourth post-action field
   # is required or injected. All preceding direction pulses are four fields.
   need(all((begin+10+i*10+k,key) in own_inputs for i,key in enumerate(keys) for k in range(4 if i<len(keys)-1 else 3)),'Exact genuine physical finisher command through native activation'+label)
   need(begin+10+(len(keys)-1)*10<=start<=begin+10+(len(keys)-1)*10+5,'Physical button reaches native action in normal phase'+label)
  need(wrap['actor']==action['actor'] and wrap['main']==action['main'] and int(wrap['age'])==int(wrap['frame'])-start and int(wrap['age'])==(233 if name=='kano' else 231),'Own native choreography completion'+label)
  need(stop['frame']=='5198' and stop['damage']=='322' and stop['damage_events']=='10' and stop['kos']=='2' and stop['wins']=='2' and stop['cache_errors']=='0' and int(stop['action'])==start and int(stop['wrap'])==int(wrap['frame']) and not items('CACHE_OVERWRITE'),'Long terminal run and no native cache overrun'+label)
  need(any(r['mode']=='3' and int(r['frame'])>int(wrap['frame'])+100 for r in items('MODE')),'Actual post-fatality native continue'+label)
  need((folder/'guest_maincpu.bin').read_bytes()==guest,'Exact entire independently reconstructed initialized guest'+label)
  palettes=items('PALETTE');need(len(palettes)==2,'Both initial physical palettes'+label)
  palette_samples=0
  def check_palette(r,expected,label2):
   nonlocal palette_samples
   path=folder/r['file'];raw=np.frombuffer(path.read_bytes(),dtype='<u4')
   need(raw.shape==(64,) and np.array_equal(raw[1:64],expected[1:64]),label2+label)
   pins[str(path)]=digest(path);palette_samples+=1
  for n in (1,2):
   at=(0xf1500 if name=='kano' else 0xf1600) if n==2 else (0xfda00 if name=='kano' else 0xfdb00)
   need(struct.unpack_from('<H',guest,at)[0]==65,'Native own palette dimensions'+label)
   record=next((r for r in palettes if r['slot']==str(n)),None)
   need(record is not None,'Initial actual palette P'+str(n)+label)
   if record:check_palette(record,colors(guest,at),'All 63 original hardware costume pens before combat')
  states=items('FINISH_STATE');need(len(states)>=60,'Positive two-body finisher state coverage'+label)
  for r in states:
   n=int(r['slot'])
   need(r['id']==r['roster']==str(identity) and r['actor']==r['owner']==actors[n-1] and r['main']==(action['main'] if n==side else action['victim_main']) and bool(int(r['flags'],16)&64)==(n==2),'True IDs/owners and native costume bit throughout finish'+label)
   need(r['hp']==('161' if n==side else '0'),'No assisted health during finish'+label)
   if n==side and int(r['age'])<=int(wrap['age'])+250:
    at=(0xf1500 if name=='kano' else 0xf1600) if n==2 else (0xfda00 if name=='kano' else 0xfdb00)
    check_palette(r,colors(guest,at),'Own full-bright normal/alternate palette through choreography/win')
   else:pins[str(folder/r['file'])]=digest(folder/r['file'])
  physical_fifo=[r for r in items('FINISH_FIFO') if r['actor'] in actors]
  need(len(physical_fifo)>100 and all(r['id']==str(identity) for r in physical_fifo),'Actual native FIFO retains true own bodies, no proxy'+label)
  # Ten-field state samples intentionally do not cover every short pose. The
  # actual native FIFO publications do; require every imported own finisher
  # group, not a guessed number of sampled state poses.
  poses={int(r['pose'],16) for r in physical_fifo if r['actor']==action['actor'] and int(r['age'])<=int(wrap['age'])}
  table=0xf56c0 if name=='kano' else 0xf5740
  required=set(struct.unpack_from('<'+str(9 if name=='kano' else 11)+'I',guest,table))
  need(required<=poses,'Every current own finisher group actually reaches native FIFO'+label)
  captures=[r for r in items('SNAPSHOT') if r['file'].startswith('mirror_finish_')]
  need([r['file'] for r in captures]==[f'mirror_finish_{start}_{age:03d}.png' for age in range(0,701,10)],'Complete actual selected-field timeline through continue'+label)
  for r in items('SNAPSHOT'):
   path=folder/'snap'/r['file'];need(Image.open(path).size==(400,254),'Actual full-scene size'+label);pins[str(path)]=digest(path)
  for file in ('run.log','result.json','guest_maincpu.bin'):pins[str(folder/file)]=digest(folder/file)
  summaries[case]=dict(fighter=name,winner=side,nativeAlternateSlot=2,nativeDamage=total,nativeKOs=chains,
   action=start,nativeWrapAge=int(wrap['age']),actualHardwarePaletteSamples=palette_samples,
   ownFinisherPoses=[f'{pose:08X}' for pose in sorted(poses)],actualTimelineCaptures=len(captures))
 need(len(summaries)==4,'Both real mirror finishers from both physical sides')
 return dict(passed=not errors,errors=sorted(set(errors)),cases=summaries,inputHashes=pins,
  scope='Four cold physical Dead Pool mirror games: natural P2 alternate assignment, two KOs, own individual finisher activation, costume/palette continuity and native continue',
  naturalMirrorFinisherStatePaletteAccepted=not errors,naturalAlternateAllFatalityArtAccepted=False,
  exactComponentDMAAndPixelAcceptance=False,donorChoreographyAccepted=False,audioAccepted=False,
  allStockFatalitiesAccepted=False,allArenasAccepted=False,fullPortAccepted=False)
if __name__=='__main__':
 assert not OUT.exists(),'Preserve verification evidence'
 report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('cases','inputHashes')},indent=2))
 raise SystemExit(0 if report['passed'] else 1)
