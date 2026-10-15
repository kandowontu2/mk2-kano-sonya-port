"""Current native blade/knife source art, owned FIFO and continuous scene.

Retain full641-field one-base CPU/DMA/shift/VRAM/RGB replay and every original
physical/AI/state/health/pool observation. Independently bind donor indices,
all effect/body compositions, actual native FIFO dispatch and visible phase
coverage through original KO/reset and both effect retirement tails.
No audio, every-arena or whole-port acceptance claim.
"""
import copy,datetime,gzip,json,re,struct,subprocess,traceback
from collections import defaultdict
from pathlib import Path
import numpy as np
import capture_current_cpu_effect_render_v6348 as capture
import verify_human_projectile_display_v1352 as art
import build_native_blade as blade
import current_cpu_effect_render_model_v6347 as model
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
CASE=capture.FOLDER
OUT=ROOT/'audit_v6351_current_cpu_effect_render_checked'
PARENT=ROOT/'audit_v6344_current_cpu_blade_allocation_checked/report.json'


def blade_art(guest,payload,image,pins):
 donor_path=ROOT/'mk3/mk3-maincpu.bin';donor=donor_path.read_bytes();pins[str(donor_path)]=sha(donor_path)
 need(pins[str(donor_path)]=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651','Exact original donor program')
 need(guest[0xf1f00:0xf1f00+200]==payload[0x1d0400:0x1d0400+200],
      'Every native single-frame blade descriptor equals actual payload records')
 colors=art.read(payload,0xfe800000+0x1d0100*8,'<H64H',0xfe800000)
 native=art.read(donor,0xffc96600,'<H24H',0xff800000)
 need(colors==(64,0,*native[2:],*([0]*40))and native[0]==24,'Original dedicated blade palette, transparent0and exact padding')
 def pixels(source,command,w,h,data):
  first=source//8;count=(source%8+w*h*((command>>12)&7 or 8)+(h*8 if command&128 else 0)+7)//8+8
  need(first>=0 and first+count<=len(data),'Independent original scanner range')
  key=f'{source:08X}_{command:04X}_{w}_{h}'
  return art.decoder({key:dict(offset=source,first=first,bytes=count,data=data[first:first+count].hex())})(source,command,w,h)
 sources=set();indices=0
 for i,(group,source_frame)in enumerate(zip(blade.GROUPS,blade.SOURCE_FRAMES)):
  need(art.read(donor,group,'<II',0xff800000)==(source_frame,0),'Exact original single-piece trail group')
  w,h,dx,dy,source,command,pal=struct.unpack_from('<4hIHI',payload,0x1d0400+i*20)
  ew,eh,ex,ey,es,ec=art.read(donor,source_frame,'<4hIH',0xff800000)
  need((w,h,dx,dy)==(ew,eh,ex,ey)and command==0x6000 and pal==0xfe800000+0x1d0100*8,
       'Original trail dimensions/origin, no knife pivot or body-palette proxy')
  a=pixels(source,command|0x8002,w,h,image);b=pixels(es,ec|0x8002,w,h,image[0xc00000:0x1e00000])
  need(np.array_equal(a,b),'Every converted blade index equals independent original donor scanner')
  sources.add(source);indices+=w*h
 return dict(frames=10,originalPixelIndices=indices,originalPaletteColors=24,sources=sources)


def groups(text):
 result=defaultdict(list)
 wanted={'FLOOR_ALL_QUEUE','FLOOR_QUEUE','FLOOR_QUEUE_PART','FLOOR_QUEUE_TRANSFORM','FLOOR_DMA','FLOOR_DMA_REGS',
         'FLOOR_QUEUE_DISPATCH','FLOOR_SINGLE_DESCRIPTOR','FLOOR_ACTION','FLOOR_CHILD_ALLOC','FLOOR_CHILD_SPAWN','FLOOR_CHILD_RETIRE',
         'FLOOR_SNAP','FLOOR_RESULT','FLOOR_STATE','FLOOR_POINTER_STORE','FLOOR_RETIRED'}
 for line in text.splitlines():
  match=re.match(r'MK2_NAT_CAMPAIGN_(\w+) ',line)
  if not match or match[1]not in wanted:continue
  digest=re.search(r'\bdata_sha256=([^\s]+)',line)
  parsed=model.parse(re.sub(r'\bdata_sha256=[^\s]+','',line))
  need(parsed and parsed[0]==match[1],'Original exact numeric observation parser')
  if digest:parsed[1]['actualDataSHA256']=digest[1]
  result[parsed[0]].append(parsed[1])
 return result


def gate(g,records,guest,payload,seq,blade_sources):
 queues={(q['frame'],q['cursor']):q for q in g['FLOOR_QUEUE']}
 inventory={(q['frame'],q['cursor']):q for q in g['FLOOR_ALL_QUEUE']}
 need(len(queues)==len(g['FLOOR_QUEUE'])and len(inventory)==len(g['FLOOR_ALL_QUEUE']), 'Complete unique actual publication inventories')
 parts=defaultdict(list);by_cursor=defaultdict(list)
 for r in g['FLOOR_QUEUE_PART']:parts[r['frame'],r['cursor']].append(r)
 for q in queues.values():by_cursor[q['cursor']].append(q)
 single={(r['frame'],r['cursor']):r for r in g['FLOOR_SINGLE_DESCRIPTOR']}
 transforms={(r['frame'],r['cursor']):r for r in g['FLOOR_QUEUE_TRANSFORM']}
 need(set(transforms)==set(queues),'Every body/child/trail publication has actual native projection registers')
 need([r['frame']for r in records]==[r['frame']for r in g['FLOOR_SNAP']]==list(range(1870,2511)),
      'Entire continuous scene, including actual transition and effect tails')
 need([(r['frame'],r['entry'])for r in g['FLOOR_ACTION']]==[(1871,0xfff8cc00),(2442,0xffffb000)],'Actual naturally chosen native actions')
 alloc=g['FLOOR_CHILD_ALLOC'];born=g['FLOOR_CHILD_SPAWN'];dead=g['FLOOR_CHILD_RETIRE']
 need(len(alloc)==len(born)==len(dead)==1 and alloc[0]['frame']==born[0]['frame']==2445 and dead[0]['frame']==2495 and
      alloc[0]['actor']==born[0]['actor']==dead[0]['actor']and born[0]['main']==dead[0]['main'],
      'Entire actual knife child allocation/scheduler/removal, distinct from blade')
 # Bind exact actual addresses to original state inventory, never normalize.
 first=g['FLOOR_STATE'][0];actors={n:first[f'p{n}']for n in(1,2)};mains={n:first[f'main{n}']for n in(1,2)}
 blade_actor=0x01031b00;knife_actor=born[0]['actor']
 common=('actor','source','pose','cache','id','body','facing','bank','pc')
 for key,q in inventory.items():
  if q['actor']in actors.values():need(key in queues and queues[key]['slot']in(1,2),'No physical body publication hidden')
  if q['actor']==knife_actor and 2445<=q['frame']<=2495:need(key in queues and queues[key]['slot']==3,'No live knife publication hidden')
  if q['actor']==blade_actor and 1871<=q['frame']<1909:need(key in queues and queues[key]['slot']==4,'No attached blade publication hidden')
  if q['frame']>=1909:need(q['source']not in blade_sources,'No blade art still published after native retirement')
  if q['frame']>2495:need(q['pose']not in set(seq['intro']+seq['flight']+seq['impact']),'No knife art after child removal')
 for key,q in queues.items():
  need(key in inventory and all(q[k]==inventory[key][k]for k in common),'Tracked publication equals whole native inventory')
  slot=q['slot'];need(slot in(1,2,3,4),'Only independently defined physical/effect roles')
  if slot<=2:
   need(q['actor']==q['owner']==q['parent']==actors[slot]and q['main']==mains[slot]and q['id']==q['roster']==17 and q['kind']==0,
        'True native Kano body/Main/roster, no proxy')
  elif slot==3:
   need(q['actor']==q['owner']==knife_actor and q['main']==born[0]['main']and q['parent']==actors[2]and q['kind']==1 and
        q['id']==q['roster']==17 and 2445<=q['frame']<=2495,'Actual distinct live owned knife child')
  else:
   need(q['actor']==blade_actor and q['main']==mains[2]and q['owner']==q['parent']==actors[2]and q['kind']==2 and
        q['roster']==17 and q['multipart']==q['pose']==0 and 1871<=q['frame']<1909,'Actual live single-frame attached blade, not a fighter')
  if q['multipart']:
   composition=art.group(q,payload,guest);actual=parts[key]
   need(len(actual)==len(composition)and all(all(p[k]==v for k,v in e.items())for p,e in zip(actual,composition)),
        'Complete source-derived multipart composition reaches actual cache')
   e=composition[q['part']];need(q['row']==q['cache']+q['part']*112,'Original full cache iterator')
  else:
   need(slot==4 and key in single,'Only source-owned single-frame trail')
   s=single[key];offset=(q['cache']-0xff800000)//8;raw=guest[offset:offset+32]
   need(s['slot']==4 and s['actor']==q['actor']and s['descriptor']==q['cache']and s['bytes']==32 and
        s['actualDataSHA256']==model.digest(raw),'Complete actual32byte descriptor compared with compiled source')
   w,h,dx,dy,source,command=struct.unpack_from('<4hIH',raw)
   e=dict(source=source,width=w,height=h,dx=dx,dy=dy,command=(command&~0x30)|(q['facing']&0x30))
  need(q['source']==e['source']and q['size']==e['width']|(e['height']<<16)and q['command']>>16==e['command']|0x8002,
       'Native FIFO source/dimensions/command equal original piece')
  t=transforms[key];need(t['world']==((q['y']&65535)<<16)|(q['x']&65535),'Actual published whole-body world position')
  xy=lambda n:(n&65535,n>>16&65535)
  x,y=xy(t['world']);cx,cy=xy(t['camera']);bx,by=xy(t['display'])
  if not t['a7']&1:x-=cx;y-=cy
  x-=e['dx'];y-=e['dy'];cmd=q['command']>>16
  if cmd&16:x+=e['width']-1
  if cmd&32:y+=e['height']-1
  need((q['xy']&1023,q['xy']>>16&511)==((x+bx)&1023,(y+by)&511),'Native camera/origin/flip/descriptor projection, no offset substitute')
 dmas={r['event']:r for r in g['FLOOR_DMA']};regs={r['event']:r for r in g['FLOOR_DMA_REGS']};dispatch={r['event']:r for r in g['FLOOR_QUEUE_DISPATCH']}
 need(len(dmas)==len(g['FLOOR_DMA'])and set(regs)==set(dmas)and len(dispatch)==len(g['FLOOR_QUEUE_DISPATCH']), 'Every DMA has unique native register context')
 draws=defaultdict(int);visible=defaultdict(set);record_by={r['frame']:r for r in records}
 for event,d in dmas.items():
  candidates=[q for q in by_cursor[regs[event]['b14']+192]if q['frame']<=d['frame']]
  q=max(candidates,key=lambda r:r['frame'])if candidates else None
  owned=bool(q and d['command']&15==2 and q['source']==d['source'])
  need((event in dispatch)==owned and d['slot']==(q['slot']if owned else 0),'Exact native FIFO dispatch, never palette-only attribution')
  if not owned:continue
  pub=dispatch[event];need(all(pub[k]==q[k]for k in('actor','main','slot','cursor'))and pub['queue_frame']==q['frame'], 'Original queue reaches native DMA unchanged')
  need(d['source']==q['source']and(d['width'],d['height'])==(q['size']&65535,q['size']>>16)and
       d['command']==q['command']>>16 and(d['x'],d['y'])==(q['xy']&1023,q['xy']>>16&511)and d['palette']==q['bank']&0x7f00,
       'Every source/size/command/position/palette reaches actual DMA unchanged')
  slot=q['slot'];draws[slot]+=1
  r=record_by.get(d['frame']+1)
  if r and r['body'][str(slot)]['pixels']>0:visible[slot].add(q['cache']if slot==4 else q['pose'])
 need(draws[1]>100 and draws[2]>100 and draws[3]>30 and draws[4]>=38,'Both fighters and all actual effects draw')
 need({0xfff8f800+i*160 for i in range(10)}<=visible[4],'All ten native blade trail phases actually visible')
 need(set(seq['body'])<=visible[2]and set(seq['intro']+seq['impact'])<=visible[3],'Every knife body/release/impact phase visible')
 actual_flight={q['pose']for q in queues.values()if q['slot']==3 and q['pose']in seq['flight']}
 need(actual_flight and actual_flight<=visible[3],'Complete actually executed flight/contact prefix visible')
 need(all(r['body']['4']['pixels']==0 for r in records if r['frame']>=1911)and
      all(r['body']['3']['pixels']==0 for r in records if r['frame']>=2497),
      'No old effect pixels through original continuous erase after either retirement')
 return dict(nativeDraws=dict(draws),bladeVisibleFrames=len(visible[4]),knifeActualFlightGroups=len(actual_flight),
             completeKnifeIntroImpactVisible=True,bodyCacheParts=len(g['FLOOR_QUEUE_PART']),publications=len(inventory),
             bladeCleanupTailFields=sum(r['frame']>=1911 for r in records),knifeCleanupTailFields=sum(r['frame']>=2497 for r in records))


def main():
 need(not OUT.exists(),'Immutable independent qualification')
 meta=json.loads((CASE/'result.json').read_text());terminal=json.loads((CASE/'native_terminal.json').read_text())
 need(meta['passed']and terminal['naturalTerminal']and terminal['exitCode']==meta['nativeExit']==0 and
      not terminal['observationErrors']and meta['originalWholePhysicalTrajectoryUnchanged'], 'Actual same process naturally terminal before full qualification')
 need(not capture.terminal.process_tools.census(),'No live native process, no further replay')
 pins=dict(meta['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Every actual executed source still unchanged')
 guest,build,scene,transport,graphics_pins=capture.init_model();payload=scene.payload
 pins.update(graphics_pins);sequences,pieces=art.independent_art(payload,scene.graphics,pins)
 donor_blade=blade_art(guest,payload,scene.graphics,pins)
 with gzip.open(CASE/'run.log.gz','rt',encoding='utf-8')as file:text=file.read()
 g=groups(text);records=json.loads((CASE/'continuous_scene_records.json').read_text());positive=gate(g,records,guest,payload,sequences['knife'],donor_blade['sources'])
 rejected=[]
 trials=[('native_dispatch_owner','FLOOR_QUEUE_DISPATCH','actor',0),('native_dispatch_source','FLOOR_QUEUE','source',0),
         ('native_part_origin','FLOOR_QUEUE_PART','dx',999),('native_palette_bank','FLOOR_DMA','palette',0),
         ('blade_descriptor_digest','FLOOR_SINGLE_DESCRIPTOR','actualDataSHA256','0'*64),
         ('native_projection_camera','FLOOR_QUEUE_TRANSFORM','camera',0),
         ('knife_parent','FLOOR_QUEUE','parent',0),('effect_pose','FLOOR_QUEUE','pose',0)]
 for label,tag,key,value in trials:
  bad=copy.deepcopy(g)
  if label=='native_palette_bank':index=next(i for i,r in enumerate(bad[tag])if r['slot']==4)
  elif label=='knife_parent' or label=='effect_pose':index=next(i for i,r in enumerate(bad[tag])if r['slot']==3)
  elif label=='native_projection_camera':
   index=next(i for i,r in enumerate(bad[tag])if r['slot']==4);value=bad[tag][index][key]^1
  else:index=0
  need(bad[tag][index][key]!=value,'Actual non-noop observed fault '+label);bad[tag][index][key]=value
  try:gate(bad,records,guest,payload,sequences['knife'],donor_blade['sources'])
  except(ValueError,AssertionError,KeyError,IndexError)as error:rejected.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Accepted real effect-render fault '+label)
 need(gate(g,records,guest,payload,sequences['knife'],donor_blade['sources'])==positive,'Untouched positive restored after actual faults')
 parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active','Full original objective remains active')
 for path in(PARENT,Path(__file__),Path(capture.__file__),Path(model.__file__),Path(art.__file__),Path(blade.__file__),
             *(p for p in CASE.rglob('*')if p.is_file())):pins[str(path.resolve())]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'All actual source/proof hashes retained')
 donor_blade['sources']=sorted(donor_blade['sources'])
 result=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=capture.terminal.current.NAME,
             goalStatus='active',parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],case=positive,
             nativeContinuousRender=meta['continuousRender'],originalKnifeRingDonorPieces=pieces,originalBladeDonorArt=donor_blade,
             actualFaultsRejected=rejected,inputHashes=pins,scope=__doc__,newNativeBoots=1,newBuilds=0,newZIPs=0,newRawMedia=0,
             currentCPUBladeKnifeEffectRasterPaletteEraseAccepted=True,allCPUOrArenaEffectAudioAccepted=False,
             fullPortAcceptance=False,fullGoalComplete=False,
             previousGoalTurnClassification='progress: complete current CPU blade pool/attach/retire lifetime',
             thisGoalTurnClassification='progress: full current CPU blade/knife original effect artwork/owned palettes/projection/FIFO/continuous screen/erase evidence',
             nextAction='Remaining effect audio and broader native CPU/arena integration; no repeat solely for accepted current screen sequence')
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,'Lossless exactfile terminal report compression')
 print(json.dumps(dict(passed=True,case=positive,continuousRender=meta['continuousRender'],actualFaultsRejected=len(rejected),newBuilds=0)),flush=True)


if __name__=='__main__':
 try:main()
 except Exception as error:
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
