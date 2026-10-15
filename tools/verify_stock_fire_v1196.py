"""Current real-input stock Scorpion fire victims, normal Dead Pool only.

Bind true identities, original gates/choreography, original burn descriptors,
palettes, source ROM pixels and actual sampled presentation. This is not a
whole-screen DMA replay, all-effect/all-field, audio or full-port proof.
"""
import hashlib,json,re,struct,zlib,zipfile
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import verify_native_split_blood_v1133 as split
import verify_cpu_pair_display_v635_v3 as native
from inspect_natural_arena_floor_v602 import decoder
ROOT=split.ROOT;OUT=ROOT/'audit_v1196_stock_fire_victims_checked'
CASES=tuple(f'audit_v1194_fire_{name}_p{side}' for name in ('kano','sonya') for side in (1,2))
CONTROLS=('audit_v1194_fire_control_kitana_p1','audit_v1194_fire_control_liu_p2')
BURN=set(range(0xff9e24a0,0xff9e25e1,64))|{0xff9e2460}
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()
def off(address):return (address-0xff800000)//8
def rows(text,prefix):return split.previous.prior.rows(text,prefix)

def original_graphics(pins):
 source=ROOT/'mame-mkp/src/mame/midway/midtunit.cpp';pins[str(source)]=digest(source)
 declaration=source.read_text().split('ROM_START( mk2ks )',1)[1].split('ROM_END',1)[0]
 region=bytearray(0xc00000);count=0
 pattern=r'ROM_LOAD32_BYTE\(\s*"([^"]+)",\s*(0x[0-9a-f]+),\s*(0x[0-9a-f]+),\s*CRC\(([0-9a-f]+)\) SHA1\(([0-9a-f]+)\)'
 for filename,start,length,crc,sha in re.findall(pattern,declaration):
  start,length=int(start,16),int(length,16)
  if start>=0xc00000:continue
  path=ROOT/'mk2'/filename;raw=path.read_bytes()
  archive=ROOT/'roms/mk2.zip'
  with zipfile.ZipFile(archive) as package:assert package.read(filename)==raw,'Actual MAME parent ROM chip equals independent original source'
  pins[str(archive)]=digest(archive)
  assert len(raw)==length and zlib.crc32(raw)==int(crc,16) and hashlib.sha1(raw).hexdigest()==sha,'Immutable original graphics chip'
  region[start:start+length*4:4]=raw;count+=1;pins[str(path)]=digest(path)
 assert count==12,'Complete twelve-chip original MKII graphics'
 return bytes(region)

def verify(texts=None,check_files=True):
 guest,_,_,payload=split.reconstruct();pins={};errors=[];summaries={}
 def need(ok,label):
  if not ok:errors.append(label)
 original_path=ROOT/'mk2/mk2-maincpu.bin';original=original_path.read_bytes();pins[str(original_path)]=digest(original_path)
 for lo,hi in ((0xff868bd0,0xff868ef0),(0xff876b40,0xff876be0),
  (0xff876fc0,0xff877420),(0xff877580,0xff877fc0),
  (0xff8c6790,0xff8c6f40),(0xff9e14a0,0xff9e2d00)):
  need(guest[off(lo):off(hi)]==original[off(lo):off(hi)],'Byte-exact original fire code/data '+hex(lo))
 graphics=original_graphics(pins)
 build=json.loads((ROOT/split.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
 for filename,wanted in build['input_hashes'].items():
  if check_files:need(digest(filename)==wanted,'Compiled input '+filename)
  pins[filename]=wanted
 for file in ('mk2ks_stock_fire_inputs_v1193.lua','mk2ks_stock_fire_display_v1193.lua'):
  path=ROOT/file;code=path.read_text()
  need(not re.search(r'\b(?:p|cpu|gfx)\s*[:.]\s*(?:write\w*|set\w*)\s*\(',code),'No guest/CPU/graphics writes '+file)
  need('load_state' not in code and 'loadstate' not in code,'No loaded state '+file);pins[str(path)]=digest(path)
 # Both stock controls must establish the same native fire choreography and
 # completion, before comparing true new victims with their same-slot control.
 control_signatures={};control_geometry={}
 for case in CONTROLS+CASES:
  directory=ROOT/case;result=json.loads((directory/'result.json').read_text(encoding='utf-8-sig'))
  name,side=result['player'],result['victim_slot'];identity={'kano':17,'sonya':18,'kitana':4,'liu_kang':1}[name];label=' '+case
  need(result['exit_code']==0 and result['seconds']==95 and result['candidate']==split.CANDIDATE and result['executable_sha256']==build['executable_sha256'] and result['payload_sha256']==build['payload_sha256'],'Matched terminal current build'+label)
  need(result['assistance']=='none' and result['cheats_enabled'] is False and result['killer']=='scorpion' and result['winner_slot']==3-side and result['command']=='uu_hp' and result['target_gap']==160,'Cold physical scenario'+label)
  for filename,wanted in result['input_hashes'].items():
   if check_files:need(digest(filename)==wanted,'Unchanged run input '+filename)
   pins[filename]=wanted
  text=texts[case] if texts is not None else (directory/'run.log').read_text(encoding='utf-8-sig')
  need(not re.search(r'\[LUA ERROR\]|fatal error|stack traceback|access violation',text,re.I),'No runtime error'+label)
  stock=rows(text,'MK2_STOCK_HEAD_V921');art=rows(text,'MK2_ROLLING_HEAD_V1003')
  need(all(r['writes']=='0' and r['assistance']=='none' for _,r in stock+art),'Read-only observations'+label)
  items=lambda tag:[r for t,r in stock if t==tag]
  actions,wraps,stops,ready=items('ACTION'),items('WRAP'),items('RESULT'),items('READY')
  need(len(actions)==len(wraps)==len(stops)==len(ready)==1,'One real native activation/completion/ready/terminal'+label)
  if not(len(actions)==len(wraps)==len(stops)==len(ready)==1):continue
  action,wrap,stop=actions[0],wraps[0],stops[0];start=int(action['frame']);begin=int(ready[0]['frame'])
  need(action['variant']=='1' and action['address']=='FF8C6790' and action['mode']=='2' and action['damage']=='322','Original fire variant'+label)
  need(ready[0]['continuation']=='FFA17E10' and ready[0]['victim_actor']==action['victim_actor'] and ready[0]['victim_main']==action['victim_main'] and 144<=int(ready[0]['gap'])<=176,'Native original dizzy state, owner and distance'+label)
  live=items('FIRST_LIVE');need(len(live)==1 and live[0]['ids']==f'10,{identity}' and live[0]['victim']==action['victim_actor'] and live[0]['own']==action['actor'],'True selected victim and Scorpion'+label)
  chain=True;hp=161;killed=0;damage=0
  collision=[r for r in items('HEALTH') if r['pc']=='FF836700' and int(r['frame'])<=start]
  for r in collision:
   before,after=int(r['before']),int(r['after']);chain=chain and before==hp and 0<=after<before<=161;hp=after;damage+=before-after
   if after==0:killed+=1;hp=161
  need(chain and len(collision)==10 and killed==2 and damage==322 and len(items('WIN'))==2,'Two native collision KOs and wins'+label)
  physical={(int(r['frame'])-begin,r['button']) for r in items('INPUT') if int(r['slot'])==3-side and int(r['frame'])>=begin}
  need({age for age,key in physical if key=='Up'}==set(range(10,14))|set(range(20,24)) and {age for age,key in physical if key=='Block'}==set(range(5,30)) and {age for age,key in physical if key=='High_Punch'}=={40,41,42} and start==begin+42,'Exact recognized physical Up Up, Block release, HP phase'+label)
  gates=[r for t,r in art if t=='FIRE_GATE' and int(r['frame'])==start]
  need(any(r['entry']=='FF868DA0' and 144<=int(r['a3'],16)<=176 for r in gates) and any(r['entry']=='FF877160' and r['a0']=='FFA17E10' for r in gates) and any(r['entry']=='FF877350' for r in gates),'Original command/distance/dizzy/common gates pass'+label)
  need(wrap['age']=='258' and int(wrap['frame'])==start+258 and wrap['actor']==action['actor'] and wrap['main']==action['main'] and wrap['pc']=='FF8CDC50','Native control-bound completion'+label)
  need(stop['frame']=='5198' and stop['damage']=='322' and stop['wins']=='2' and int(stop['action'])==start and int(stop['wrap'])==start+258 and any(r['mode']=='3' and int(r['frame'])>start+258 for r in items('MODE')) and not items('CACHE_OVERWRITE'),'Safe native continuation'+label)
  calls=[r for t,r in art if t=='FIRE_CALL' and int(r['age'])<=258]
  wanted={0xff8c6790:0,0xff8c6c10:56,0xff9e14a0:56,0xff9e1bb0:84,0xff9e2300:84,0xff9e2440:169,0xff9e2160:172,0xff9e2c30:174,0xff8cdc40:258}
  for address,age in wanted.items():
   found=[r for r in calls if int(r['entry'],16)==address]
   need(len(found)==1 and found[0]['age']==str(age),'Original fire chronology '+hex(address)+label)
   if found and address in (0xff9e1bb0,0xff9e2300,0xff9e2440,0xff9e2160,0xff9e2c30):
    need(found[0]['actor']==action['victim_actor'] and found[0]['id']==str(identity),'True-ID original victim routine '+hex(address)+label)
  # The original packed voice helper chooses a victim-class scream at age84.
  # Preserve that native request separately; don't demand Kitana/Liu's voice
  # from Kano/Sonya or call an unaudited sound request audible fidelity.
  signature=[(r['entry'],r['age'],r['a0'] if r['entry']=='FFA12530' and r['age']!='84' else '') for r in calls]
  if case in CONTROLS:control_signatures[side]=signature
  else:need(signature==control_signatures[side],'Exact same-slot original fire/sound-request chronology'+label)
  need((directory/'guest_maincpu.bin').read_bytes()==guest,'Entire current guest independently reconstructed'+label)
  queues={(r['frame'],r['cursor'],r['source']):r for t,r in art if t=='QUEUE'}
  dmas=[r for t,r in art if t=='DMA' and int(r['fifo_pose'],16) in BURN]
  palettes={r['source']:r for t,r in art if t=='PALETTE_DUMP'}
  seen=set();per_source={};geometry={}
  for dma in dmas:
   q=queues.get((dma['frame'],dma['cursor'],dma['source']));need(q is not None and dma['queue_match']=='1','Actual FIFO/DMA binding'+label)
   if q is None:continue
   pose=int(q['pose'],16);seen.add(pose)
   need(q['actor']==q['physical']==q['owner']==action['victim_actor'] and q['id']==str(identity) and q['main']==action['victim_main'],'Real physical burned-victim owner/ID'+label)
   expected=native.group({'pose':pose,'facing':int(q['body'],16)},payload,guest)
   need(len(expected)==1,'Original single-component burn group'+label)
   part=expected[0];w,h=int(dma['width']),int(dma['height']);command=int(dma['command'],16);source=int(dma['source'],16)
   need(part['source']==source and (part['width'],part['height'])==(w,h) and command==part['command']|0x8002,'Exact original burn descriptors to DMA'+label)
   need(int(q['size'],16)==w|(h<<16) and int(q['xy'],16)&1023==int(dma['x']) and (int(q['xy'],16)>>16)&511==int(dma['y']) and int(q['bank'],16)&0x7f00==int(dma['palette'],16),'Native actual geometry/palette publication'+label)
   geometry[pose]=(int(q['y']),int(q['stageY']),int(q['cameraY']),int(dma['y'])&255,w,h)
   per_source[dma['source']]=(pose,part)
  need(seen==BURN and len(dmas)>80,'All seven original generic burn groups actually draw'+label)
  if case in CONTROLS:control_geometry[side]=geometry
  else:need(geometry==control_geometry[side],'Original same-slot burn vertical geometry; no added-character height shift'+label)
  matches=[];visible=set()
  snaps=[r for t,r in art if t=='POSE_SNAPSHOT' and r['source'] in per_source]
  for snap in snaps:
   pose,part=per_source[snap['source']]
   dma=next((r for r in dmas if r['frame']==snap['queued_frame'] and r['source']==snap['source'] and r['fifo_actor']==snap['actor_pose'].split('_')[0]),None)
   need(dma is not None and int(snap['frame'])==int(snap['queued_frame'])+1,'Actual presented pose chronology'+label)
   if dma is None:continue
   source,command,w,h=int(dma['source'],16),int(dma['command'],16),int(dma['width']),int(dma['height'])
   raw=graphics[source//8:source//8+(w+128)*h+2];key=f'{source:08X}_{command:04X}_{w}_{h}'
   indices=decoder({key:{'data':raw.hex(),'offset':source}})(source,command,w,h)
   palette_path=directory/palettes[snap['source']]['file'];colors=np.asarray(struct.unpack('<64I',palette_path.read_bytes()),dtype=np.uint32)
   palette=np.stack(((colors>>16)&255,(colors>>8)&255,colors&255),axis=1)
   descriptor=struct.unpack_from('<I',guest,off(pose))[0]
   palette_pointer=struct.unpack_from('<I',guest,off(descriptor)+14)[0]
   count=struct.unpack_from('<H',guest,off(palette_pointer))[0];need(1<=count<=64,'Original burn palette count'+label)
   words=struct.unpack_from('<'+str(count)+'H',guest,off(palette_pointer)+2)
   expected=np.asarray([tuple(((v>>shift)&31)*8+(((v>>shift)&31)>>2) for shift in (10,5,0)) for v in words],dtype=np.uint8)
   need(np.array_equal(palette[:count],expected),'Actual complete original burn hardware palette'+label)
   picture=directory/'snap'/f"head_pose_{snap['actor_pose']}_{snap['frame']}.png"
   # Include visible light skeleton pixels as well as chromatic flames.
   pixels=np.asarray(Image.open(picture).convert('RGB'));tile=indices[:,::-1] if command&16 else indices
   x=int(dma['x'])-56-(w-1 if command&16 else 0);y=int(dma['y'])&255
   x0,y0,x1,y1=max(0,x),max(0,y),min(400,x+w),min(254,y+h)
   tile=tile[y0-y:y1-y,x0-x:x1-x];expected=palette[tile];mask=(tile!=0)&(np.max(expected,axis=2)>32)
   count_pixels=int(mask.sum());score=float((np.max(np.abs(pixels[y0:y1,x0:x1].astype(int)-expected.astype(int)),axis=2)<=3)[mask].mean()) if count_pixels else 0
   matches.append({'pose':f'{pose:08X}','source':snap['source'],'score':score,'visiblePixels':count_pixels,'picture':str(picture)})
   if score>=0.8 and count_pixels>=64:visible.add(pose)
   pins[str(picture)]=digest(picture);pins[str(palette_path)]=digest(palette_path)
  need(visible==BURN,'Positive source-ROM-bound presented pixels for every burn pose'+label)
  captures=items('DISPLAY');need([int(r['age']) for r in captures]==list(range(0,601,10)),'Complete sampled native fatality timeline'+label)
  for r in captures:
   path=directory/'snap'/f"stock_head_{start}_{int(r['age']):03d}.png";need(Image.open(path).size==(400,254),'Actual timeline capture'+label);pins[str(path)]=digest(path)
  for path in directory.rglob('*'):
   if path.is_file():pins[str(path)]=digest(path)
  summaries[case]={'trueVictimID':identity,'victimSlot':side,'nativeActionFrame':start,'nativeWrapAge':258,'nativeFireSignature':signature,'burnDMA':len(dmas),'burnGroups':len(seen),'burnGeometry':{f'{p:08X}':v for p,v in geometry.items()},'actualPosePixelMatches':matches,'sameSlotStockControl':CONTROLS[side-1]}
 need(len(summaries)==6 and len(control_signatures)==2,'Four true victim cases and both stock controls')
 return dict(passed=not errors,errors=sorted(set(errors)),cases=summaries,inputHashes=pins,
  stockFireVictimStateAndSampledBurnArtAccepted=not errors,allEffectsRenderAccepted=False,
  fullScreenDMAReplayAccepted=False,allFatalityArtAccepted=False,alternateCostumesAccepted=False,
  audioAccepted=False,allArenasAccepted=False,allFloorShadowsAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
 assert not OUT.exists(),'Do not overwrite evidence'
 report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('cases','inputHashes')},indent=2))
 raise SystemExit(0 if report['passed'] else 1)
