"""Read-only original secondary fatality: full sampled native rendering.

Bind genuine input runs, original detached allocation, ROM components, all
CPU/DMA copies, loaded palettes, exact displayed scenes and native retirement.
Normal Dead Pool samples only; other moves/arenas/audio remain unaccepted.
"""
import argparse, hashlib, json, re, struct, zlib
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import verify_stock_scorpion_secondary_v1257 as physical
import verify_stock_fire_v1197 as util
import verify_finish_display_v798 as native
import inspect_secondary_display_v1231 as raster
ROOT=physical.ROOT

def verify(key):
 folder=ROOT/f'audit_v1253_secondary_{key}';pins={}
 def need(ok,label):
  if not ok:raise ValueError(label)
 def pin(path,wanted=None):
  path=Path(path);actual=util.digest(path)
  need(wanted is None or actual==wanted,'Changed evidence '+str(path));pins[str(path)]=actual
 launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
 build=json.loads((ROOT/physical.headed.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
 need(launch['exit_code']==0 and launch['candidate']==physical.headed.CANDIDATE and
      launch['executable_sha256']==build['executable_sha256'] and launch['payload_sha256']==build['payload_sha256'], 'Matched terminal build')
 need(launch['seconds']==95 and launch['assistance']=='none' and launch['cheats_enabled'] is False and
      launch['command']=='dfff_hp_release' and launch['killer']=='scorpion' and launch['target_gap']==64,'Genuine unassisted original command')
 for file,wanted in launch['input_hashes'].items():pin(file,wanted)
 metadata_path=physical.headed.OUT/'report.json';metadata=json.loads(metadata_path.read_text());pin(metadata_path)
 need(metadata['passed'] and metadata['nativeROMAuditAccepted'] and metadata['candidate']==launch['candidate'],'Actual rebuilt source metadata/native instruction/ROM audit proof')
 for file,wanted in metadata['inputHashes'].items():pin(file,wanted)
 pin(ROOT/physical.headed.CANDIDATE/'build-info.json')
 guest,_,_,payload=physical.headed.reconstruct()
 need((folder/'guest_maincpu.bin').read_bytes()==guest,'Entire actual guest independently reconstructed')
 log=(folder/'run.log').read_text(encoding='utf-8-sig')
 need(not re.search(r'WRONG CHECKSUMS|might not run correctly|\[LUA ERROR\]|fatal error|stack traceback|access violation',log,re.I),'No ROM checksum/runtime/observer error')
 baseline=ROOT/f'audit_v1230_secondary_{key}'
 baseline_log=(baseline/'run.log').read_text(encoding='utf-8-sig');pin(baseline/'run.log')
 for prefix in ('MK2_STOCK_HEAD_V921','MK2_ROLLING_HEAD_V1003'):
  need(util.rows(log,prefix)==util.rows(baseline_log,prefix),'Every physical/native/art event unchanged '+prefix)
 state_path=physical.OUT/'report.json';state=json.loads(state_path.read_text());pin(state_path)
 need(state['passed'] and state['candidate']==launch['candidate'],'Current six-case native physical proof')
 for file,wanted in state['inputHashes'].items():pin(file,wanted)
 for age in range(0,601,10):
  filename=f"stock_head_{state['cases'][key]['actionFrame']}_{age:03d}.png"
  need((folder/'snap'/filename).read_bytes()==(baseline/'snap'/filename).read_bytes(),'Observer preserves actual complete timeline image '+filename)
 need((folder/'snap/continue_4080.png').read_bytes()==(baseline/'snap/continue_4080.png').read_bytes(),'Observer preserves actual continue image')
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in ((0xff868700,0xff868930),(0xff8bbfe0,0xff8bd040),(0xff8ca980,0xff8caa10),
               (0xff83ae20,0xff83b250),(0xff83ce60,0xff83cf00),(0xff80dcc0,0xff80dde0)):
  need(guest[util.off(lo):util.off(hi)]==original[util.off(lo):util.off(hi)],'Unmodified native choreography/allocator/mirror/owner '+hex(lo))
 for file in ('mk2ks_stock_scorpion_secondary_inputs_v1210.lua','mk2ks_stock_scorpion_secondary_display_v1210.lua','mk2ks_stock_secondary_full_display_v1229.lua'):
  code=(ROOT/file).read_text();pin(ROOT/file)
  need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state',code),'No observer game/state writes '+file)
 groups,_,_,_,_=raster.data(folder)
 need(len(groups['FLOOR_BEGIN'])==len(groups['FLOOR_RESULT'])==1,'One bounded native render window')
 origin=groups['FLOOR_BEGIN'][0];start=origin['origin'];side=launch['victim_slot'];winner=3-side
 identity={'kano':17,'sonya':18,'kitana':4,'liu_kang':1}[launch['player']]
 ids=(identity,10) if side==1 else (10,identity)
 need(start==state['cases'][key]['actionFrame'] and origin['entry']==0xff8bbfe0 and origin['id']==10,'Original actual secondary action starts capture')
 first=groups['FLOOR_STATE'][0];actors={s:first[f'p{s}'] for s in (1,2)};mains={s:first[f'main{s}'] for s in (1,2)}
 allocation=groups['FLOOR_DETACHED_ALLOC'];linked=groups['FLOOR_DETACHED_LINK']
 need(len(allocation)==len(linked)==1,'Exactly one original independent torso allocation/link')
 allocation,linked=allocation[0],linked[0]
 need(allocation['entry']==0xff8bcbd0 and linked['entry']==0xff8bcd70 and
      allocation['frame']==linked['frame']==start+71+side and
      allocation['actor']==linked['actor']!=actors[side] and
      allocation['parent']==linked['parent']==actors[side] and allocation['main']==linked['main']==mains[side] and
      linked['id']==linked['roster']==identity,'Original true victim allocation, copy and publication, not attached proxy')
 graphics=bytearray(0x2000000);graphics[:0xc00000]=util.original_graphics(pins)
 source=ROOT/'mame-mkp/src/mame/midway/midtunit.cpp';declaration=source.read_text().split('ROM_START( mk2ks )',1)[1].split('ROM_END',1)[0];pin(source)
 pattern=r'ROM_LOAD32_BYTE\(\s*"([^"]+)"\s*,\s*(0x[0-9a-f]+)\s*,\s*(0x[0-9a-f]+)\s*,\s*CRC\(([0-9a-f]+)\)\s*SHA1\(([0-9a-f]+)\)'
 chips=0
 for filename,at,length,crc,sha in re.findall(pattern,declaration):
  at,length=int(at,16),int(length,16)
  if at<0xc00000:continue
  path=ROOT/'roms/mk2ks'/filename;raw=path.read_bytes();pin(path)
  need(len(raw)==length and zlib.crc32(raw)==int(crc,16) and hashlib.sha1(raw).hexdigest()==sha,'Original declared imported graphics chip')
  graphics[at:at+length*4:4]=raw;chips+=1
 need(chips==20,'All twenty imported graphics chips')
 torso_bytes=struct.unpack_from('<I',payload,0x1b0008)[0]
 need(payload[0x1b0000:0x1b0004]==b'KTR1' and 0<torso_bytes<=0x20000,'Independent owned torso artwork header')
 graphics[0x1f20000:0x1f20000+torso_bytes]=payload[0x1b1000:0x1b1000+torso_bytes]
 # Independently reconstruct both actual HUD name masks, including stock
 # dark pen 2 at the native one-pixel offset. Not a new art modification.
 ui_path=ROOT/'roms/mk2ks/mk2ks.ui';ui=ui_path.read_bytes();pin(ui_path)
 colors=struct.unpack_from('<H',ui,6)[0];names=8+2*(colors*2+ui[4]*ui[5]);mw,mh=ui[names:names+2]
 ow=struct.unpack_from('<H',original,util.off(0xffa79400))[0];os=struct.unpack_from('<I',original,util.off(0xffa79400)+8)[0]
 ramp=[]
 for y in range(10):
  counts=[0]*16;best=0
  for x in range(ow):
   bit=os+(y*ow+x)*4;pen=(int.from_bytes(graphics[bit//8:bit//8+2],'little')>>(bit%8))&15
   if pen==3 or 5<=pen<=11:
    counts[pen]+=1
    if counts[pen]>counts[best]:best=pen
  ramp.append(best)
 for fighter in range(2):
  mask=ui[names+2+fighter*mw*mh:names+2+(fighter+1)*mw*mh]
  xs=[x for y in range(10) for x in range(mw) if mask[y*mw+x]>48];need(bool(xs),'Actual nonempty HUD mask')
  left,right=min(xs),max(xs);fw=right-left+1;w=fw+1
  face=lambda x,y:0<=x<fw and 0<=y<10 and mask[y*mw+left+x]>48
  for y in range(10):
   for x in range(w):
    pen=ramp[y] if face(x,y) else 2 if x and (face(x-1,y) or (y and face(x-1,y-1))) else 0
    pixel=y*w+x;graphics[0x1e00000+fighter*0x400+pixel//2]|=pen<<((pixel&1)*4)
 counts=defaultdict(int)
 for r in groups['FLOOR_GFX']:
  first_byte,last=r['first'],r['first']+r['bytes']
  # The read-only capture retains eight extra decoder lookahead bytes.
  # ROMREGION_ERASE00 and the exact bounded native copy leave these bytes
  # zero. Compare them as well; do not drop the tail from source binding.
  region='original_imported' if last<=0x1e00000 else 'hud_names' if 0x1e00000<=first_byte and last<=0x1e00800 else 'owned_torso' if 0x1f20000<=first_byte<0x1f20000+torso_bytes and last<=0x1f20000+torso_bytes+8 else None
  need(region is not None,'Unbound captured graphics region '+hex(first_byte))
  need(bytes.fromhex(r['data'])==graphics[first_byte:last],'Actual source bytes differ from independently reconstructed '+region)
  counts[region]+=1
 queues={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']};parts=defaultdict(list)
 for p in groups['FLOOR_QUEUE_PART']:parts[p['frame'],p['cursor']].append(p)
 dispatch={r['event']:r for r in groups['FLOOR_QUEUE_DISPATCH']};regs={r['event']:r for r in groups['FLOOR_DMA_REGS']}
 need(len(queues)==len(groups['FLOOR_QUEUE']) and len(dispatch)==len(groups['FLOOR_QUEUE_DISPATCH']) and len(regs)==len(groups['FLOOR_DMA_REGS'])==len(groups['FLOOR_DMA']) and set(regs)=={r['event'] for r in groups['FLOOR_DMA']},'Unique complete FIFO/register observations')
 publications=defaultdict(list)
 for q in queues.values():publications[q['cursor']].append(q)
 draws=defaultdict(int);poses=defaultdict(set);dispatched=defaultdict(list)
 for d in groups['FLOOR_DMA']:
  candidates=[q for q in publications[regs[d['event']]['b14']+192] if q['frame']<=d['frame']];q=max(candidates,key=lambda q:q['frame']) if candidates else None
  owned=bool(q and d['command']&15==2 and q['source']==d['source'])
  need((d['event'] in dispatch)==owned and d['slot']==(q['slot'] if owned else 0),'Recomputed classification of every actual DMA')
  if not owned:continue
  publication=dispatch[d['event']]
  need(q==queues[publication['queue_frame'],publication['cursor']] and all(publication[k]==q[k] for k in ('actor','main','slot')),'Original six-word FIFO consumer reaches published actor')
  slot=q['slot'];ps=slot if slot<=2 else winner if slot==3 else side
  need(slot in (1,2,3,4) and q['parent']==actors[ps] and q['owner']==q['parent'] and q['main']==mains[ps] and q['id']==q['roster']==ids[ps-1] and q['bank']&0x7f00==d['palette'],'Every true physical/weapon/torso identity, native owner, ancestry and palette')
  need(q['actor']==(actors[slot] if slot<=2 else linked['actor'] if slot==4 else q['actor']) and q['kind']==(0 if slot<=2 else 1 if slot==3 else 2),'Actual independent actor kind')
  if slot>=3:need(q['actor']!=q['parent'],'Child/static torso cannot replace physical fighter')
  need(q['multipart']==1,'Original multipart native body/weapon/torso branch')
  expected=util.native.group(q,payload,guest);observed=parts[q['frame'],q['cursor']]
  need(len(expected)==len(observed) and all(all(p[k]==v for k,v in e.items()) for p,e in zip(observed,expected)),'Every source-bound composite component and actual F0 facing')
  need(q['pc']==0xff804420 and q['row']==q['cache']+q['part']*112 and q['part'] in range(len(expected)),'Original cache iterator')
  p=expected[q['part']]
  need(q['source']==d['source']==p['source'] and q['size']&65535==d['width']==p['width'] and q['size']>>16==d['height']==p['height'] and q['command']>>16==d['command']==p['command']|0x8002 and q['xy']&1023==d['x'] and q['xy']>>16&511==d['y'],'Exact source/size/command/facing/XY reaches native DMA')
  draws[slot]+=1;poses[slot].add(q['pose']);dispatched[d['frame']].append(q)
 need(draws[side]>100 and draws[winner]>100 and draws[3]>0 and draws[4]>0,'Positive physical, actual weapon and detached torso drawing coverage')
 print(key+' all native descriptors/source bytes accepted; replaying complete scenes',flush=True)
 drawn=raster.inspect(folder)
 need(drawn['frames']>100 and all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in drawn['records']),'Every complete sampled VRAM/scanout exactly reconstructed')
 visible=defaultdict(set)
 for r in drawn['records']:
  for q in dispatched[r['frame']-1]:
   if r['body'][q['slot']]['pixels']>0:visible[q['slot']].add(q['pose'])
 need(bool(visible[4]),'Detached torso contributes actual displayed native pixels')
 palette_samples=0;headed=set()
 if identity in (17,18):
  base=0x100000 if identity==17 else 0x104000;script=(struct.unpack_from('<I',payload,base+55*4)[0]-0xfe800000)//8
  headed=set(struct.unpack_from('<5I',payload,script))
  need(headed<=visible[side],'All five corrected headed groups are visibly drawn in exact replay')
  need(counts['owned_torso']>0,'Positive independently bound dedicated severed torso graphics')
  for display in groups['FLOOR_DISPLAY']:
   applicable=[q for q in dispatched[display['frame']-1] if q['slot']==4 or q['slot']==side and q['pose'] in headed]
   if not applicable:continue
   actual=np.fromfile(folder/display['palette_file'],dtype='<u4')
   for q in applicable:
    native.check_owned_body_palette(dict(q,slot=side),actual,guest,ids,side)
   palette_samples+=1
  need(palette_samples>20,'Positive complete 65-pen native victim/torso palette coverage')
 teardown=native.retirement(groups,origin,guest,ids,winner)
 need(not any(d['slot'] in (3,4) for d in groups['FLOOR_QUEUE_DISPATCH'] if d['frame']>teardown),'No weapon/torso dispatch after original retirement')
 after=[r for r in drawn['records'] if r['frame']>teardown+1]
 need(len(after)>5 and all(r['body'][3]['pixels']==r['body'][4]['pixels']==0 for r in after),'Actual post-retirement scenes free of both original child objects')
 snaps={r['frame']:r for r in groups['FLOOR_SNAP']};displays={r['frame']:r for r in groups['FLOOR_DISPLAY']};held=[]
 for h in groups['FLOOR_HELD']:
  display=displays[h['frame']];image=np.asarray(Image.open(folder/'snap'/snaps[h['frame']]['file']).convert('RGB'))
  need(h['frame']==h['snapshot'] and all(h[k]==display[k] for k in ('start','control','tap')),'Actual held-field scanout metadata')
  result=native.check_latch(image,(folder/h['file']).read_bytes(),(folder/display['palette_file']).read_bytes(),h['start'],h['control'],h['tap'])
  held.append(dict(frame=h['frame'],pixels=result['pixels'],DMAReconstructed=False))
 need(groups['FLOOR_RESULT'][0]['snapshots']==drawn['frames']+len(held)==len(snaps),'All actual presented samples accounted')
 for path in folder.rglob('*'):
  if path.is_file():pin(path)
 for file in ('verify_stock_secondary_display_v1258.py','inspect_secondary_display_v1231.py','verify_stock_scorpion_secondary_v1257.py','verify_native_metadata_build_v1254.py','verify_stock_fire_v1197.py','verify_finish_display_v798.py','verify_cpu_pair_display_v635_v3.py','verify_native_floor_display_v602.py','inspect_natural_arena_floor_v602.py'):
  pin(ROOT/'tools'/file)
 return dict(passed=True,case=key,candidate=launch['candidate'],trueVictimID=identity,victimSlot=side,
  originalDetachedAllocation=allocation,originalDetachedLink=linked,sourceBoundGraphics=dict(counts),nativeDraws=dict(draws),
  visiblePoses={s:[f'{p:08X}' for p in sorted(v)] for s,v in visible.items()},paletteSamples=palette_samples,
  replayed=drawn,heldScanout=held,nativeTeardown=teardown,postRetirementSamples=len(after),inputHashes=pins,
  currentSecondarySampledFullNativeRenderAccepted=True,allFatalityArtAccepted=False,audioAccepted=False,
  alternateCostumesAccepted=False,allArenasAccepted=False,allFloorShadowsAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('case',choices=physical.CASES);args=parser.parse_args()
 out=ROOT/f'audit_v1258_secondary_{args.case}_render_checked';assert not out.exists(),'Preserve all previous evidence'
 try:report=verify(args.case)
 except Exception as error:report=dict(passed=False,case=args.case,error=repr(error),fullPortAccepted=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(args.case+' passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
 raise SystemExit(0 if report['passed'] else 1)
