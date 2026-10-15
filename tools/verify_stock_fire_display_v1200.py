"""Original Scorpion fire: genuine victims, native composites, exact scanout.

All observed copies, palettes, sampled full-scene pixels and original cleanup
are checked, including correct original flame occlusion. No all-fields,
alternate-costume, other-arena, donor-choreography, audio or full-port claim.
"""
import argparse,hashlib,json,re,struct,zlib
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import verify_stock_fire_v1197 as state
import verify_finish_display_v798 as native
ROOT=state.ROOT
def verify(name,side):
 case=f'audit_v1199_fire_{name}_p{side}'
 baseline=f'audit_v1194_fire_{name}_p{side}'
 control=f'audit_v1194_fire_control_{"kitana_p1" if side==1 else "liu_p2"}'
 folder=ROOT/case;pins={}
 def pin(path,wanted=None):
  path=Path(path);actual=state.digest(path);assert wanted is None or actual==wanted,'Changed input '+str(path);pins[str(path)]=actual
 def need(ok,label):
  if not ok:raise ValueError(label)
 build=json.loads((ROOT/state.split.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
 launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
 need(launch['exit_code']==0 and launch['seconds']==95 and launch['candidate']==state.split.CANDIDATE and launch['executable_sha256']==build['executable_sha256'] and launch['payload_sha256']==build['payload_sha256'],'Matched terminal current build')
 need(launch['player']=={'control_kitana':'kitana','control_liu':'liu_kang'}.get(name,name) and launch['victim_slot']==side and launch['winner_slot']==3-side and launch['assistance']=='none' and launch['cheats_enabled'] is False and launch['killer']=='scorpion' and launch['command']=='uu_hp' and launch['target_gap']==160,'Cold physical-only original scenario')
 for file,wanted in launch['input_hashes'].items():pin(file,wanted)
 log=(folder/'run.log').read_text(encoding='utf-8-sig');pin(folder/'run.log');pin(folder/'result.json')
 need(not re.search(r'\[LUA ERROR\]|fatal error|stack traceback|access violation',log,re.I),'No native/observer error')
 guest,_,_,payload=state.split.reconstruct();need((folder/'guest_maincpu.bin').read_bytes()==guest,'Whole guest independently reconstructed')
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();pin(ROOT/'mk2/mk2-maincpu.bin')
 for lo,hi in ((0xff868bd0,0xff868ef0),(0xff876b40,0xff876be0),(0xff876fc0,0xff877420),
  (0xff877580,0xff877fc0),(0xff8c6790,0xff8c6f40),(0xff9e14a0,0xff9e2d00),
  (0xff83b470,0xff83b5f0)):
  need(guest[state.off(lo):state.off(hi)]==original[state.off(lo):state.off(hi)],'Byte-exact original fire/gate/facing code '+hex(lo))
 for file in ('mk2ks_stock_fire_inputs_v1193.lua','mk2ks_stock_fire_display_v1193.lua','mk2ks_stock_fire_full_display_v1198.lua'):
  source=(ROOT/file).read_text();need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state',source),'Read-only input/observer '+file);pin(ROOT/file)
 stock=state.rows(log,'MK2_STOCK_HEAD_V921');art=state.rows(log,'MK2_ROLLING_HEAD_V1003')
 baseline_log=(ROOT/baseline/'run.log').read_text(encoding='utf-8-sig');pin(ROOT/baseline/'run.log')
 need(stock==state.rows(baseline_log,'MK2_STOCK_HEAD_V921') and art==state.rows(baseline_log,'MK2_ROLLING_HEAD_V1003'),'Full observation preserves EVERY earlier physical/native/art event')
 items=lambda tag:[r for t,r in stock if t==tag]
 need(all(r['writes']=='0' and r['assistance']=='none' for _,r in stock+art),'No assisted observations')
 action,wrap,stop,ready=(items(tag) for tag in ('ACTION','WRAP','RESULT','READY'))
 need(len(action)==len(wrap)==len(stop)==len(ready)==1,'One actual action/finish/ready/terminal')
 action,wrap,stop,ready=action[0],wrap[0],stop[0],ready[0]
 start=int(action['frame']);begin=int(ready['frame']);winner=3-side;identity={'kano':17,'sonya':18,'control_kitana':4,'control_liu':1}[name]
 ids=(identity,10) if side==1 else (10,identity)
 need(action['variant']=='1' and action['address']=='FF8C6790' and action['mode']=='2' and action['damage']=='322','Native first fire variant')
 live=items('FIRST_LIVE');need(len(live)==1 and live[0]['ids']==f'10,{identity}' and live[0]['victim']==action['victim_actor'] and live[0]['own']==action['actor'],'True fighters, no proxy')
 need(ready['continuation']=='FFA17E10' and ready['victim_actor']==action['victim_actor'] and ready['victim_main']==action['victim_main'] and 144<=int(ready['gap'])<=176,'Original dizzy state/distance')
 chain=True;hp=161;killed=0;damage=0
 collision=[r for r in items('HEALTH') if r['pc']=='FF836700' and int(r['frame'])<=start]
 for r in collision:
  before,after=int(r['before']),int(r['after']);chain=chain and before==hp and 0<=after<before<=161;hp=after;damage+=before-after
  if after==0:killed+=1;hp=161
 need(chain and len(collision)==10 and killed==2 and damage==322 and len(items('WIN'))==2,'Two genuine collision KOs and wins')
 physical={(int(r['frame'])-begin,r['button']) for r in items('INPUT') if int(r['slot'])==winner and int(r['frame'])>=begin}
 need({age for age,key in physical if key=='Up'}==set(range(10,14))|set(range(20,24)) and {age for age,key in physical if key=='Block'}==set(range(5,30)) and {age for age,key in physical if key=='High_Punch'}=={40,41,42} and start==begin+42,'Exact native recognized physical command phase')
 gates=[r for t,r in art if t=='FIRE_GATE' and int(r['frame'])==start]
 need(any(r['entry']=='FF868DA0' and 144<=int(r['a3'],16)<=176 for r in gates) and any(r['entry']=='FF877160' and r['a0']=='FFA17E10' for r in gates) and any(r['entry']=='FF877350' for r in gates),'Native command/distance/dizzy/common gates')
 need(wrap['age']=='258' and int(wrap['frame'])==start+258 and wrap['actor']==action['actor'] and wrap['main']==action['main'] and wrap['pc']=='FF8CDC50','Original native completion')
 need(stop['frame']=='5198' and stop['damage']=='322' and stop['wins']=='2' and int(stop['action'])==start and int(stop['wrap'])==start+258 and not items('CACHE_OVERWRITE'),'Stable native final continuation')
 calls=[r for t,r in art if t=='FIRE_CALL' and int(r['age'])<=258]
 control_log=(ROOT/control/'run.log').read_text(encoding='utf-8-sig');pin(ROOT/control/'run.log')
 control_art=state.rows(control_log,'MK2_ROLLING_HEAD_V1003')
 control_calls=[r for t,r in control_art if t=='FIRE_CALL' and int(r['age'])<=258]
 def choreography(records):return [(r['entry'],r['age'],r['a0'] if r['entry']=='FFA12530' and int(r['age'])!=84+(side-1) else '') for r in records]
 need(choreography(calls)==choreography(control_calls),'Same-slot original cooperative fire choreography and non-victim sound requests')
 wanted={0xff8c6790:0,0xff8c6c10:56,0xff9e14a0:56,0xff9e1bb0:84+(side-1),0xff9e2300:84+(side-1),0xff9e2440:169+(side-1),0xff9e2160:172+(side-1),0xff9e2c30:174+(side-1),0xff8cdc40:258}
 for address,age in wanted.items():
  found=[r for r in calls if int(r['entry'],16)==address]
  need(len(found)==1 and found[0]['age']==str(age),'Original fire chronology '+hex(address))
  if address in (0xff9e1bb0,0xff9e2300,0xff9e2440,0xff9e2160,0xff9e2c30):need(found[0]['actor']==action['victim_actor'] and found[0]['id']==str(identity),'True victim through original burn coroutine')
 groups,_,_,_,_=native.raster.data(folder)
 need(len(groups['FLOOR_BEGIN'])==len(groups['FLOOR_RESULT'])==1,'One real render window')
 origin=groups['FLOOR_BEGIN'][0];result=groups['FLOOR_RESULT'][0]
 need(origin['origin']==start==result['origin'] and origin['entry']==0xff8c6790 and origin['id']==10 and origin['actor']==int(action['actor'],16),'Actual native Scorpion render origin')
 # Independent source bytes: original MKII parent ZIP plus declared original
 # imported MK3 chips. Custom name glyphs remain runtime-copy-bound only.
 graphics=bytearray(0x2000000);graphics[:0xc00000]=state.original_graphics(pins)
 layout_path=ROOT/'mame-mkp/src/mame/midway/midtunit.cpp';layout=layout_path.read_text().split('ROM_START( mk2ks )',1)[1].split('ROM_END',1)[0]
 pattern=r'ROM_LOAD32_BYTE\(\s*"([^"]+)"\s*,\s*(0x[0-9a-f]+)\s*,\s*(0x[0-9a-f]+)\s*,\s*CRC\(([0-9a-f]+)\)\s*SHA1\(([0-9a-f]+)\)'
 chips=0
 for filename,at,length,crc,sha in re.findall(pattern,layout):
  at,length=int(at,16),int(length,16)
  if at<0xc00000:continue
  path=ROOT/'roms/mk2ks'/filename;raw=path.read_bytes();need(len(raw)==length and zlib.crc32(raw)==int(crc,16) and hashlib.sha1(raw).hexdigest()==sha,'Original imported chip');pin(path)
  graphics[at:at+length*4:4]=raw;chips+=1
 need(chips==20,'Complete original imported graphics')
 source_bound=0
 for capture in groups['FLOOR_GFX']:
  first,last=capture['first'],capture['first']+capture['bytes']
  if last<=0x1e00000:
   need(bytes.fromhex(capture['data'])==graphics[first:last],'Actual captured original/imported graphics differ from independent ROMs');source_bound+=1
 need(source_bound>40,'Positive original/imported source binding')
 queues={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']};parts=defaultdict(list)
 for r in groups['FLOOR_QUEUE_PART']:parts[r['frame'],r['cursor']].append(r)
 dispatch={r['event']:r for r in groups['FLOOR_QUEUE_DISPATCH']};regs={r['event']:r for r in groups['FLOOR_DMA_REGS']}
 need(len(queues)==len(groups['FLOOR_QUEUE']) and len(dispatch)==len(groups['FLOOR_QUEUE_DISPATCH']) and set(regs)=={r['event'] for r in groups['FLOOR_DMA']},'Unambiguous complete native queues/register events')
 publications=defaultdict(list)
 for q in queues.values():publications[q['cursor']].append(q)
 body_draws=0;poses=defaultdict(set);dispatched=defaultdict(list);burn_geometry={}
 for dma in groups['FLOOR_DMA']:
  published=[q for q in publications[regs[dma['event']]['b14']+192] if q['frame']<=dma['frame']];q=max(published,key=lambda q:q['frame']) if published else None
  owned=bool(q and dma['command']&15==2 and q['source']==dma['source'])
  need((dma['event'] in dispatch)==owned and dma['slot']==(q['slot'] if owned else 0),'Every owned or unowned actual DMA correctly classified')
  if not owned:continue
  d=dispatch[dma['event']];need(q==queues[d['queue_frame'],d['cursor']] and d['actor']==q['actor'] and d['main']==q['main'] and d['slot']==q['slot'],'Actual six-word FIFO cursor binds each draw')
  slot=q['slot'];expected_id=ids[slot-1] if slot<=2 else 10
  need(q['id']==q['roster']==expected_id and q['owner']==(q['actor'] if slot<=2 else q['parent']) and q['bank']&0x7f00==dma['palette'],'True original physical/child ownership')
  need(q['multipart']==1,'Actual native multipart Scorpion fire/main/victim')
  expected=state.native.group(q,payload,guest);observed=parts[q['frame'],q['cursor']]
  need(len(observed)==len(expected) and all(all(p[k]==v for k,v in e.items()) for p,e in zip(observed,expected)),'ALL actual cached components match original/owned ROM descriptors and actor F0 facing')
  need(q['row']==q['cache']+q['part']*112 and q['pc']==0xff804420 and q['part'] in range(len(expected)),'Original native component cache iterator')
  part=expected[q['part']]
  need(q['source']==dma['source']==part['source'] and q['size']&65535==dma['width']==part['width'] and q['size']>>16==dma['height']==part['height'] and q['command']>>16==dma['command']==part['command']|0x8002 and q['xy']&1023==dma['x'] and q['xy']>>16&511==dma['y'],'Exact queued size/source/command/facing/XY reaches actual DMA')
  body_draws+=1;poses[slot].add(q['pose']);dispatched[dma['frame']].append(q)
  if slot==side and q['pose'] in state.BURN:burn_geometry[q['pose']]=(q['y'],dma['y']&255,dma['width'],dma['height'])
 need(state.BURN<=poses[side] and body_draws>1000 and bool(poses[3]),'All original victim burn groups and actual Scorpion attached fire draw')
 print(case+' native descriptors/source binding accepted; replaying real full scenes',flush=True)
 drawn=native.raster.inspect(folder)
 need(drawn['frames']>100 and all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in drawn['records']),'Exact event-ordered native VRAM and full-scene scanout, including original fire occlusion')
 visible=defaultdict(set)
 for record in drawn['records']:
  for q in dispatched[record['frame']-1]:
   if record['body'][q['slot']]['pixels']>0:visible[q['slot']].add(q['pose'])
 need(state.BURN<=visible[side],'Every burn group contributes actual visible native pixels in at least one exact replayed scene')
 descriptor=struct.unpack_from('<I',guest,state.off(0xff9e24a0))[0];pointer=struct.unpack_from('<I',guest,state.off(descriptor)+14)[0]
 count=struct.unpack_from('<H',guest,state.off(pointer))[0];need(count==59,'Original native fire palette count')
 words=struct.unpack_from('<59H',guest,state.off(pointer)+2)
 expected=np.asarray([sum(((((v>>shift)&31)<<3)|(((v>>shift)&31)>>2))<<dest for shift,dest in ((10,16),(5,8),(0,0))) for v in words],dtype=np.uint32)
 burn_palettes=0
 for display in groups['FLOOR_DISPLAY']:
  candidates=[q for q in dispatched[display['frame']-1] if q['slot']==side and q['pose'] in state.BURN]
  if not candidates:continue
  actual=np.fromfile(folder/display['palette_file'],dtype='<u4')
  need(len(actual)==32768 and all(np.array_equal(actual[q['bank']&0x7f00:(q['bank']&0x7f00)+59],expected) for q in candidates),'Full original 59-pen burn palette in actual scanout');burn_palettes+=1
 need(burn_palettes>30,'Positive original burn palette coverage')
 teardown=native.retirement(groups,origin,guest,ids,winner)
 need(not any(r['slot']==3 for r in groups['FLOOR_QUEUE_DISPATCH'] if r['frame']>teardown),'No attached fire after original retirement')
 after=[r for r in drawn['records'] if r['frame']>teardown+1];need(len(after)>5 and all(r['body'][3]['pixels']==0 for r in after),'Replayed post-retirement scenes without new attached fire')
 snapshots={r['frame']:r for r in groups['FLOOR_SNAP']};displays={r['frame']:r for r in groups['FLOOR_DISPLAY']};held=[]
 for h in groups['FLOOR_HELD']:
  image=np.asarray(Image.open(folder/'snap'/snapshots[h['frame']]['file']).convert('RGB'));display=displays[h['frame']]
  need(h['frame']==h['snapshot'] and all(h[k]==display[k] for k in ('start','control','tap')),'Actual held scanout metadata')
  checked=native.check_latch(image,(folder/h['file']).read_bytes(),(folder/display['palette_file']).read_bytes(),h['start'],h['control'],h['tap']);held.append({'frame':h['frame'],'pixels':checked['pixels'],'DMAReconstructed':False})
 need(result['snapshots']==drawn['frames']+len(held)==len(snapshots),'All actual presented samples accounted')
 for path in folder.rglob('*'):
  if path.is_file():pin(path)
 for file in ('tools/verify_stock_fire_display_v1200.py','tools/verify_stock_fire_v1197.py','tools/verify_finish_display_v798.py','tools/inspect_finish_display_v680_v1.py'):pin(ROOT/file)
 return dict(passed=True,case=case,trueVictimID=identity,victimSlot=side,nativeAction=start,nativeWrapAge=258,
  originalChoreography=choreography(calls),nativeBodyDraws=body_draws,burnPaletteSamples=burn_palettes,
  independentlySourceBoundGraphicsRecords=source_bound,burnGeometry={f'{p:08X}':v for p,v in burn_geometry.items()},
  visiblePoses={s:[f'{p:08X}' for p in sorted(v)] for s,v in visible.items()},replayed=drawn,heldScanout=held,
  nativeTeardown=teardown,postRetirementReplayedSamples=len(after),inputHashes=pins,
  stockFireNormalDeadPoolSampledRenderAccepted=True,allFatalityArtAccepted=False,alternateCostumesAccepted=False,
  audioAccepted=False,allArenasAccepted=False,allFloorShadowsAccepted=False,fullPortAccepted=False)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya','control_kitana','control_liu'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 out=ROOT/f'audit_v1200_fire_{args.fighter}_p{args.side}_render_checked';assert not out.exists(),'Preserve evidence'
 try:report=verify(args.fighter,args.side)
 except Exception as error:report={'passed':False,'error':str(error),'fullPortAccepted':False}
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('replayed','inputHashes')},indent=2));raise SystemExit(0 if report['passed'] else 1)
