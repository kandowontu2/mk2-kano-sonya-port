"""Real-input native hat head-hit, own death art and continuation; Dead Pool.

No proxy, flag assistance, simulated scene, or activation-only acceptance.
Use independently reconstructed current guest/payload and frozen owned art.
"""
import hashlib,json,re,struct
from pathlib import Path
import numpy as np
from PIL import Image
import verify_native_split_blood_v1133 as split
ROOT=split.ROOT;OUT=ROOT/'audit_v1157_native_hat_kill_checked'
CASES=tuple(f'audit_v1156_kung_lao_{name}_p{side}_early_hat_up_two' for name in ('kano','sonya') for side in (1,2))
CONTROLS=('audit_v1156_kung_lao_kitana_p1_early_hat_up_two','audit_v1156_kung_lao_liu_kang_p2_early_hat_up_two')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def rows(text,prefix):return split.previous.prior.rows(text,prefix)
def off(address):return (address-0xff800000)//8
def unpack(packed,count):
 return np.asarray([(int.from_bytes(packed[(n*6)//8:(n*6)//8+2],'little')>>((n*6)%8))&63 for n in range(count)],dtype=np.uint8)

def verify(texts=None,check_files=True):
 guest,_,_,payload=split.reconstruct();errors=[];pins={};summaries={}
 def need(ok,label):
  if not ok:errors.append(label)
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in ((0xff8bd040,0xff8bd2f0),(0xff8ae840,0xff8af1f0),(0xff8e0b80,0xff8e0da0),(0xffa16cb0,0xffa17280)):
  need(guest[off(lo):off(hi)]==original[off(lo):off(hi)],'Original hat/head-height/native victim code preserved '+hex(lo))
 info=json.loads((ROOT/split.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
 encoding_path=ROOT/'audit_v900_native_death_grounding_encoding/report.json'
 historical=json.loads((ROOT/'audit_v1146_split_blood_and_mirror_checkpoint/checkpoint.json').read_text())
 need(digest(encoding_path)==historical['inputHashes'][str(encoding_path)],'Exact previously source-verified owned death assets')
 encoding=json.loads(encoding_path.read_text());pins[str(encoding_path)]=digest(encoding_path)
 assets={}
 for name in ('kano','sonya'):
  for frame in encoding['fighters'][name]['frames']:
   at,size=frame['pixel_offset'],frame['size'];width,height=size
   indices=unpack(payload[at:at+frame['packed_bytes']],width*height).reshape((height,width))
   need(hashlib.sha256(indices.tobytes()).hexdigest()==frame['indices_sha256'],'Frozen source encoded indices '+name+' '+str(frame['pose']))
   assets[int(frame['graphics'],16)]=dict(**frame,fighter=name,indices=indices)
 for file in ('mk2ks_stock_hat_inputs_v1153.lua','mk2ks_stock_hat_display_v1154.lua','mk2ks_stock_hat_trace_v1155.lua'):
  text=(ROOT/file).read_text()
  need(not re.search(r'\b(?:p|cpu|gfx)\s*[:.]\s*(?:write\w*|set\w*)\s*\(',text),'No guest/CPU/graphics writes '+file)
  pins[str(ROOT/file)]=digest(ROOT/file)
 for case in CASES+CONTROLS:
  directory=ROOT/case;result=json.loads((directory/'result.json').read_text(encoding='utf-8-sig'))
  name,side=result['player'],result['victim_slot'];identity={'kano':17,'sonya':18,'kitana':4,'liu_kang':1}[name]
  label=' '+case
  need(result['exit_code']==0 and result['candidate']==split.CANDIDATE and result['executable_sha256']==info['executable_sha256'] and result['payload_sha256']==info['payload_sha256'],'Exact terminal build'+label)
  need(result['seconds']==95 and result['assistance']=='none' and result['cheats_enabled'] is False and result['killer']=='kung_lao' and result['winner_slot']==3-side and result['command']=='bf_lp_release' and result['target_gap']==272 and result['steer']=='Up' and result['steer_start']==20 and result['steer_end']==22 and result['approach_delay']==20,'Explicit real-input-only scenario'+label)
  for filename,wanted in result['input_hashes'].items():
   if check_files:need(digest(Path(filename))==wanted,'Unchanged input '+filename)
   pins[filename]=wanted
  text=texts[case] if texts is not None else (directory/'run.log').read_text(encoding='utf-8-sig')
  need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',text,re.I),'No runtime errors'+label)
  stock=rows(text,'MK2_STOCK_HEAD_V921');hat=rows(text,'MK2_HAT_V1155');art=rows(text,'MK2_ROLLING_HEAD_V1003')
  need(all(r['writes']=='0' and r['assistance']=='none' for _,r in stock+hat+art),'Read-only native observation'+label)
  items=lambda tag:[r for t,r in stock if t==tag]
  actions,wraps,stops=items('ACTION'),items('WRAP'),items('RESULT')
  need(len(actions)==len(wraps)==len(stops)==1,'One actual native hat kill and terminal'+label)
  if len(actions)!=1 or len(wraps)!=1 or len(stops)!=1:continue
  action,wrap,stop=actions[0],wraps[0],stops[0];start=int(action['frame']);hit=int(wrap['frame'])
  need(action['variant']=='2' and action['address']=='FF8BD040' and action['mode']=='2' and action['damage']=='322','Original real hat action'+label)
  live=items('FIRST_LIVE');need(len(live)==1 and live[0]['ids']==f'0,{identity}' and live[0]['own']==action['actor'] and live[0]['victim']==action['victim_actor'],'True Kung Lao/selected victim, no proxy'+label)
  health=[r for r in items('HEALTH') if int(r['frame'])<=start and r['pc']=='FF836700']
  need(len(health)==10 and sum(int(r['before'])-int(r['after']) for r in health)==322 and sum(r['after']=='0' for r in health)==2 and len(items('WIN'))==2,'Actual two rounds/322 collision damage/two KOs'+label)
  inputs=items('INPUT');up=[r for r in inputs if r['button']=='Up' and int(r['slot'])==3-side]
  need([int(r['frame'])-start for r in up]==[20,21],'Actual two-field upward flight steering'+label)
  need(any(r['button']=='Low_Punch' and int(r['slot'])==3-side and int(r['frame'])==start-1 for r in inputs) and not any(r['button']=='Low_Punch' and int(r['slot'])==3-side and int(r['frame'])==start for r in inputs),'Actual LP release into original action'+label)
  states=[r for tag,r in hat if tag=='STATE'];hit_rows=[r for r in states if r['at']=='FF835E30']
  gates=[r for r in states if r['at']=='FFA16CB0'];branches=[r for r in states if r['at']=='FF8E0D20']
  need(len(hit_rows)==len(gates)==len(branches)==1,'One actual collision and original head-height kill branch'+label)
  if gates:
   gate=gates[0]
   need(gate['actor']==action['victim_actor'] and gate['main']==action['victim_main'] and gate['id']==str(identity) and int(gate['frame'])==hit and 104<=int(gate['a1'],16)<=118,'True victim passes original 104..118 head-height window'+label)
  writes=[r for tag,r in hat if tag=='SUCCESS_WRITE']
  need(any(r['pc']=='FF8CDCC0' and r['new']=='65535' and r['actor']==action['victim_actor'] and int(r['frame'])==hit for r in writes) and not any(r['pc']=='FF8E0D90' for r in writes),'Native success, not ordinary hit fallback'+label)
  need(wrap['pc']=='FF8CDC50' and wrap['actor']==action['victim_actor'] and wrap['main']==action['victim_main'] and 30<=int(wrap['age'])<=45 and int(wrap['age'])==hit-start,'Native collision-triggered completion, not synthetic fixed timer'+label)
  need(stop['frame']=='5198' and stop['damage']=='322' and stop['wins']=='2' and int(stop['action'])==start and int(stop['wrap'])==hit and any(r['mode']=='3' and int(r['frame'])>hit+100 for r in items('MODE')) and not items('CACHE_OVERWRITE'),'Long continuation without cache overrun/softlock'+label)
  need((directory/'guest_maincpu.bin').read_bytes()==guest,'Entire initialized guest independently matches'+label)
  matches=[];seen_body=set();seen_head=set();body_count=head_count=0
  if name in ('kano','sonya'):
   own={s:a for s,a in assets.items() if a['fighter']==name}
   queues={(r['frame'],r['cursor'],r['source']):r for tag,r in art if tag=='QUEUE'}
   dmas=[r for tag,r in art if tag=='DMA' and int(r['source'],16) in own]
   palettes={int(r['source'],16):r for tag,r in art if tag=='PALETTE_DUMP'}
   for dma in dmas:
    asset=own[int(dma['source'],16)];q=queues.get((dma['frame'],dma['cursor'],dma['source']))
    need(q is not None and dma['queue_match']=='1','Native FIFO/DMA binding'+label)
    if q is None:continue
    need(q['physical']==q['owner']==action['victim_actor'] and q['main']==action['victim_main'] and q['id']==str(identity),'Own real native body/head ID and physical owner'+label)
    need([int(dma['width']),int(dma['height'])]==asset['size'],'Actual owned sprite dimensions'+label)
    if asset['kind']=='body':
     body_count+=1;seen_body.add(asset['pose'])
     need(q['actor']==action['victim_actor'] and q['y']==q['floor'] and int(q['floor'])==int(q['stageY'])-(134 if name=='kano' else 135),'Physical own headless body floor'+label)
     ground=int(q['stageY'])+5+int(q['displayY'])-int(q['cameraY'])-1-(int(q['displayY'])&256)
     need((int(dma['y'])&255)+int(dma['height'])-1==ground,'Measured native raster floor'+label)
    else:
     head_count+=1;seen_head.add(asset['pose'])
     need(q['actor']!=action['victim_actor'] and q['cache']==asset['descriptor'],'Own native separate head descriptor'+label)
   for tag,snap in art:
    source=int(snap.get('source','0'),16)
    if tag!='POSE_SNAPSHOT' or source not in own:continue
    asset=own[source]
    dma=next((r for r in dmas if r['frame']==snap['queued_frame'] and r['source']==snap['source'] and r['fifo_actor']==snap['actor_pose'].split('_')[0]),None)
    need(dma is not None and int(snap['frame'])==int(snap['queued_frame'])+1,'Actual presented snapshot chronology'+label)
    if dma is None:continue
    palette_path=directory/palettes[source]['file']
    raw=np.asarray(struct.unpack('<64I',palette_path.read_bytes()),dtype=np.uint32)
    palette=np.stack(((raw>>16)&255,(raw>>8)&255,raw&255),axis=1)
    pointer={'kano':0xfffed000,'sonya':0xfffed800}[name];at=off(pointer)
    words=struct.unpack_from('<64H',guest,at+2)
    expected=np.asarray([tuple(((word>>shift)&31)*255//31 for shift in (10,5,0)) for word in words],dtype=np.uint8)
    need(np.max(np.abs(palette[1:64].astype(int)-expected[1:64].astype(int)))<=1,'Actual native headless hardware palette'+label)
    picture=directory/'snap'/f"head_pose_{snap['actor_pose']}_{snap['frame']}.png"
    score,count=split.previous.pixel_score(picture,asset['indices'],palette,dma)
    matches.append(dict(kind=asset['kind'],pose=asset['pose'],actor=dma['fifo_actor'],score=score,visibleChromaticPixels=count,picture=str(picture)))
    pins[str(picture)],pins[str(palette_path)]=digest(picture),digest(palette_path)
   need(seen_body==set(range(7)) and body_count>100 and head_count>0,'Native seven-pose own body collapse and own separate head'+label)
   strong={(m['kind'],m['pose']) for m in matches if m['score']>=0.5 and m['visibleChromaticPixels']>=8}
   need({('body',n) for n in range(7)}.issubset(strong) and any(k=='head' for k,n in strong),'Actual source-bound presented own body/head pixels'+label)
  captures=items('DISPLAY');need([int(r['age']) for r in captures]==list(range(0,601,10)),'Complete actual native finish timeline captures'+label)
  for r in captures:
   path=directory/'snap'/f"stock_head_{start}_{int(r['age']):03d}.png"
   need(Image.open(path).size==(400,254),'Actual scene size'+label);pins[str(path)]=digest(path)
  for file in ('run.log','result.json','guest_maincpu.bin','native_death_gfx.bin'):pins[str(directory/file)]=digest(directory/file)
  summaries[case]=dict(victim=name,slot=side,nativeDamage=322,nativeWrapAge=hit-start,headHeight=int(gates[0]['a1'],16) if gates else None,
    bodyDMAs=body_count,headDMAs=head_count,ownBodyPoses=sorted(seen_body),ownHeadPoses=sorted(seen_head),pixelMatches=matches,actualTimelineCaptures=len(captures))
 need(len(summaries)==6,'Both owned victims in both real slots plus original same-slot controls')
 return dict(passed=not errors,errors=sorted(set(errors)),cases=summaries,inputHashes=pins,
  scope='Real BF LP release, upward hat steering, original head-height hit/kill and own seven-pose headless body/separate head; normal Dead Pool both real victims/slots plus Kitana and Liu controls',
  genuineNativeHatKillAccepted=not errors,alternateCostumesAccepted=False,allStockFatalitiesAccepted=False,allArenasAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
 if OUT.exists():raise ValueError('Never replace native hat verification')
 report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('cases','inputHashes')},indent=2))
 raise SystemExit(0 if report['passed'] else 1)
