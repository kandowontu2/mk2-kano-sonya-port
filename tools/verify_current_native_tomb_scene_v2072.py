"""Current earned P1 Kano Tomb sequence: full native rendering and retirement.

Physical inputs/whole guest/original branch/source art/FIFO/projection/palettes
and native shadow/erase/scanout are independently checked. Native mixed PCM and
sound writes are inventoried, not certified as correct voices or all audio.
This one original-held branch does not accept all finishers/victims/full port.
"""
import json,re,struct,traceback,wave
from pathlib import Path
from collections import defaultdict
import numpy as np
from PIL import Image
import verify_current_interrupt_v1870 as launch
import verify_current_ground_shadow_v1859 as graphics
import native_stage_variant_checks_v1731 as native
import inspect_current_cpu_knife_raster_v1975 as raster
import inspect_ball_register_erase_v1843 as erase
import inspect_native_shadow_rows_v635 as shadow
import verify_human_projectile_display_v1352 as art
from verify_finish_display_v798 import check_owned_body_palette
from verify_native_floor_display_v602 import check_latch

ROOT=launch.ROOT
CASE=ROOT/'audit_v2069_current_kano_p1_tomb_fullscene'
OUT=ROOT/'audit_v2072_current_kano_p1_tomb_scene_checked'
raster.base.STR|={'seconds'}
raster.base.HEX|={'gravity','vx','vy','flags','trail','io0'}
raster.HEX=raster.base.HEX
shadow.data=raster.data

def classic(log):
 return '\n'.join(r for r in log.splitlines()if r.startswith('MK2_STAGE_')and not r.startswith('MK2_STAGE_PROVENANCE_'))

def verify():
 pins=launch.source_pins()
 guest,_,payload=launch.current.expected()
 meta=json.loads((CASE/'result.json').read_text(encoding='utf-8-sig'))
 before=json.loads((CASE/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
 build=json.loads((ROOT/launch.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 assert meta['exit_code']==0 and meta['candidate']==launch.NAME and meta['cheats_enabled']is False
 assert(meta['winner'],meta['side'],meta['arena'],meta['command_case'],meta['seconds'])==('kano',1,1,'positive',900)
 assert meta['guest_writes']==0 and meta['assistance']=='none'and meta['input_hashes']==before
 assert meta['executable_sha256']==build['executable_sha256']and meta['payload_sha256']==build['payload_sha256']
 assert all(before.get(file)==wanted for file,wanted in build['input_hashes'].items())
 for file,wanted in before.items():
  assert launch.sha(file)==wanted,'Changed executed input '+file
  pins[file]=wanted
  if Path(file).suffix in('.lua','.ps1','.json'):
   assert launch.sha(CASE/'input_sources'/Path(file).name)==wanted
  if Path(file).suffix=='.lua':
   assert not re.search(r':write_|write_u\d+|load_?state|\.value\s*=(?!=)',Path(file).read_text())
 required={'mk2ks_native_stage_performer_v806.lua','mk2ks_stage_branch_provenance_v1722.lua',
  'mk2ks_native_tomb_display_v2062.lua','run_current_native_tomb_display_v2063.ps1','34010ops.hxx','34010gfx.hxx'}
 assert required<={Path(f).name for f in before}
 observer=(CASE/'input_sources/mk2ks_native_tomb_display_v2062.lua').read_text()
 assert "dofile('mk2ks_stage_branch_provenance_v1722.lua')"in observer
 assert not re.search(r':write_|write_u\d+|set_value|clear_value|load_?state|\.value\s*=(?!=)',observer)
 assert 'retired.frame+30'in observer and 'f<=window_end()'in observer
 assert(CASE/'guest_maincpu.bin').read_bytes()==guest,'Entire actual guest reconstructed independently'
 log=(CASE/'run.log').read_text(encoding='utf-8-sig')
 assert not re.search(r'WRONG CHECKSUMS|might not run correctly|LUA ERROR|Lua error|fatal error|stack traceback|access violation',log,re.I)
 baseline=ROOT/'audit_v1714_kano_tomb_p1/run.log'
 old=baseline.read_text(encoding='utf-8-sig')
 assert classic(log)==classic(old),'All original physical input, damage, motion, mode and teardown records unchanged'
 pins[str(baseline)]=launch.sha(baseline)
 state=native.check_log(classic(log),'kano',1,1,'positive',certified_drop_log=classic(old))
 # Preserve the original native held branch; the unchanged input prefix
 # reproduces the earlier natural held case, not the random-drop fixture.
 provenance_rows=[dict(re.findall(r'(\w+)=([^\s]+)',r))for r in log.splitlines()if r.startswith('MK2_STAGE_PROVENANCE_BRANCH ')]
 tomb=[r for r in provenance_rows if int(r['frame'])>=state['action_frame']and r['entry']in('FF8EB0D0','FF8EB150','FF80EC20','FF8EB1A0','FF8EB1B0','FF8EB200','FF8EB290','FF8EB3C0','FF8EB400')]
 assert [r['entry']for r in tomb]==['FF8EB0D0','FF8EB150','FF80EC20','FF8EB1A0','FF8EB400']
 assert len({r['frame']for r in tomb})==1 and all(r['io0']=='FFFFFFFF'and r['a8']==r['actor']and r['a13']==r['main']for r in tomb)
 assert tomb[2]['a0']=='00000032'and int(tomb[3]['a0'],16)>=50 and tomb[4]['a0']==tomb[3]['a0']
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for first,last in((0xff804040,0xff804470),(0xff8eaf00,0xff8eb490),(0xff876650,0xff876b40),(0xff80e980,0xff80ecf0),(0xff82b800,0xff82bca0)):
  lo,hi=(first-0xff800000)//8,(last-0xff800000)//8
  assert guest[lo:hi]==original[lo:hi],'Original projection/Tomb branch/RNG/fall code unchanged'
 image=bytearray(graphics.graphics(pins))
 for header,magic,source,dest in((0x1c0000,b'KFX1',0x1c4000,0x1e04000),(0x1c1000,b'KPI1',0x1e6000,0x1e50000),
  (0x1c2000,b'KPJ1',0x1f4000,0x1e60000),(0x1d0000,b'KBL1',0x1d4000,0x1e08000)):
  assert payload[header:header+4]==magic
  start,count,destination=struct.unpack_from('<III',payload,header+4)
  assert start==source and destination==dest and count>0 and source+count<=len(payload)and dest+count<=len(image)
  image[dest:dest+count]=payload[source:source+count]
 raster.source(pins)
 groups,buffers,_,_,owners=raster.data(CASE)
 for r in groups['FLOOR_GFX']:
  assert 0<=r['first']<r['first']+r['bytes']<=len(image)
  assert bytes.fromhex(r['data'])==image[r['first']:r['first']+r['bytes']],'All body/blood/scenery/shadow/foreground graphics source-bound'
 begin,result,retired=groups['FLOOR_BEGIN'],groups['FLOOR_RESULT'],groups['FLOOR_RETIRED']
 assert len(begin)==len(result)==len(retired)==1
 origin=begin[0]['origin'];end=retired[0]['frame']
 assert origin==state['action_frame']==result[0]['origin'] and end==result[0]['retired']
 assert begin[0]['id']==17 and begin[0]['entry']==0xff8bdfe0
 expected=list(range(origin+1,end+31))
 assert len(expected)>500 and [r['frame']for r in groups['FLOOR_SNAP']]==expected and result[0]['snapshots']==len(expected)
 assert retired[0]['mode']==3 and retired[0]['p1']==retired[0]['p2']==0 and retired[0]['victim_health']==0
 first=groups['FLOOR_STATE'][0]
 actors={s:first[f'p{s}']for s in(1,2)};mains={s:first[f'main{s}']for s in(1,2)}
 ids=(17,18);anchors={17:134,18:135}
 # Native post-fight mode retires the loser state before clearing only actor
 # globals. Main globals retain their scheduler addresses; v806's sample()
 # reports nil for them after actor=0, so do not confuse nil with guest stores.
 transition=[r for r in groups['FLOOR_STATE']if r['mode']==3][0]['frame']
 oldfields=native.rows(classic(old),'FIELD')
 assert transition==min(int(r['frame'])for r in oldfields if r['mode']=='3')
 assert end==min(int(r['frame'])for r in oldfields if r['own']=='00000000'and r['victim']=='00000000')
 stores=groups['FLOOR_POINTER_STORE']
 assert len(stores)==4
 for n,r in enumerate(stores):
  field=(0x01060220 if n<2 else 0x01060df0)
  assert r['frame']==end and r['field']==field and r['at']==field+(16 if n%2 else 0)
  assert r['value']==0 and r['mask']==65535 and r['pc']==(0xff82bbf0 if n<2 else 0xff82bc20)
 for r in groups['FLOOR_STATE']:
  assert all(r[f'main{s}']==mains[s]and r[f'roster{s}']==ids[s-1]for s in(1,2))
  assert (r['state1'],r['state2'])==((1,1)if r['frame']<transition else(1,2))
  if r['frame']<end:
   assert all(r[f'p{s}']==actors[s]for s in(1,2))
  else:
   assert r['p1']==r['p2']==0 and r['mode']==3
 assert len(groups['FLOOR_STATE'])==len(expected)+1
 phase=groups['FLOOR_PHASE'];assert[r['frame']for r in phase]==list(range(origin,end+31))
 assert all(float(a['seconds'])<float(b['seconds'])for a,b in zip(phase,phase[1:]))
 assert not groups['FLOOR_CHILD_ALLOC']and not groups['FLOOR_CHILD_SPAWN']and not groups['FLOOR_CHILD_RETIRE']
 bodies=groups['FLOOR_BODY']
 for r in bodies:
  s=r['slot'];assert r['actor']==r['owner']==actors[s]and r['main']==mains[s]and r['id']==r['roster']==ids[s-1]
  assert r['floor']==220-anchors[r['id']]
  assert r['frame']<end,'No physical body survives actual slot pointer teardown'
 # Every independent pre-execution victim callback must equal the previous
 # completed native body, including the actual ceiling-held no-drop horizon.
 # Compare native motion/action/actor data, not the legacy IN0 mirror field.
 body_at={(r['frame'],r['slot']):r for r in bodies}
 victim_fields=[dict(re.findall(r'(\w+)=([^\s]+)',r))for r in log.splitlines()if r.startswith('MK2_STAGE_PROVENANCE_FIELD ')]
 held_fields=[r for r in victim_fields if origin<int(r['frame'])<=end]
 assert [int(r['frame'])for r in held_fields]==list(range(origin+1,end+1))
 for r in held_fields:
  prior=body_at[int(r['frame'])-1,2]
  assert tuple(int(r[k],16)for k in('actor','main','vy','gravity','action'))==tuple(prior[k]for k in('actor','main','vy','gravity','action'))
  assert int(r['id'])==prior['id']==18 and int(r['y'])==prior['y']
 branch_frame=int(tomb[0]['frame'])
 ceiling=[r for r in held_fields if int(r['frame'])>branch_frame]
 assert ceiling and all((int(r['y']),int(r['vy'],16),int(r['gravity'],16),int(r['action'],16))==(-174,0,0,0x503)for r in ceiling)
 queues={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']}
 inventory={(q['frame'],q['cursor']):q for q in groups['FLOOR_ALL_QUEUE']}
 assert len(queues)==len(groups['FLOOR_QUEUE'])and len(inventory)==len(groups['FLOOR_ALL_QUEUE'])>len(queues)
 parts=defaultdict(list);published=defaultdict(list);drawn=defaultdict(list);poses=defaultdict(set)
 for r in groups['FLOOR_QUEUE_PART']:parts[r['frame'],r['cursor']].append(r)
 for q in queues.values():published[q['cursor']].append(q)
 for key,q in inventory.items():
  if q['actor']in actors.values():assert key in queues,'Native physical actor publication omitted'
 transforms={(t['frame'],t['cursor']):t for t in groups['FLOOR_QUEUE_TRANSFORM']}
 assert set(transforms)==set(queues)
 signed=lambda v:(v&65535)-65536 if v&32768 else v&65535
 for key,q in queues.items():
  s=q['slot'];assert s in(1,2)and q['actor']==q['owner']==q['parent']==actors[s]and q['main']==mains[s]
  assert q['id']==q['roster']==ids[s-1]and q['kind']==0 and q['multipart']==1 and q['frame']<end
  assert key in inventory and all(q[k]==inventory[key][k]for k in('actor','source','pose','cache','id','body','facing','bank','pc'))
  composition=art.group(q,payload,guest);observed=parts[key]
  assert len(composition)==len(observed)and all(all(p[k]==v for k,v in e.items())for p,e in zip(observed,composition))
  assert q['row']==q['cache']+112*q['part']and q['pc']==0xff804420
  t=transforms[key];p=composition[q['part']]
  assert all(t[k]==q[k]for k in('slot','actor','main'))and t['world']==((q['y']&65535)<<16)|(q['x']&65535)
  assert t['floor']==q['floor']==t['stageY']-anchors[q['id']]
  x,y=signed(t['world']),signed(t['world']>>16)
  if not t['a7']&1:x-=signed(t['camera']);y-=signed(t['camera']>>16)
  x-=p['dx'];y-=p['dy'];command=q['command']>>16
  if command&16:x+=p['width']-1
  if command&32:y+=p['height']-1
  x+=signed(t['display']);y+=signed(t['display']>>16)
  assert(q['xy']&1023,q['xy']>>16&511)==(x&1023,y&511),'Actual native queued camera/cache/flip projection'
 dmas={d['event']:d for d in groups['FLOOR_DMA']};regs={r['event']:r for r in groups['FLOOR_DMA_REGS']}
 dispatch={r['event']:r for r in groups['FLOOR_QUEUE_DISPATCH']}
 assert set(regs)==set(dmas)and len(dispatch)==len(groups['FLOOR_QUEUE_DISPATCH'])
 for event,d in dmas.items():
  candidates=[q for q in published[regs[event]['b14']+192]if q['frame']<=d['frame']]
  q=max(candidates,key=lambda r:r['frame'])if candidates else None
  owned=bool(q and d['command']&15==2 and q['source']==d['source'])
  assert(event in dispatch)==owned and d['slot']==(q['slot']if owned else 0),'Complete FIFO dispatch not palette-based'
  if not owned:continue
  pub=dispatch[event]
  assert queues[pub['queue_frame'],pub['cursor']]==q and all(pub[k]==q[k]for k in('actor','main','slot'))
  p=art.group(q,payload,guest)[q['part']]
  assert d['source']==p['source']and(d['width'],d['height'])==(p['width'],p['height'])and d['command']==p['command']|0x8002
  assert(q['xy']&1023,q['xy']>>16&511,q['bank']&0x7f00)==(d['x'],d['y'],d['palette'])
  drawn[d['frame']].append(q);poses[q['slot']].add(q['pose'])
 shadows=shadow.inspect(CASE)
 assert shadows['rowStreamVerified']and not shadows['failures']and not shadows['oversized_rows']and set(map(tuple,shadows['identities']))=={(1,17),(2,18)}
 print('Current native Tomb input/branch/source/FIFO/projection and shadow rows pass; replaying every scene',flush=True)
 video=raster.inspect(CASE)
 assert all(r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in video['records'])
 displays={r['frame']:r for r in groups['FLOOR_DISPLAY']};snaps={r['frame']:r for r in groups['FLOOR_SNAP']}
 palette_checks=0;visible=defaultdict(set)
 for r in video['records']:
  colors=np.fromfile(CASE/displays[r['frame']]['palette_file'],dtype='<u4');assert colors[15]==0
  for q in drawn[r['frame']-1]:
   check_owned_body_palette(q,colors,guest,ids,q['slot']);palette_checks+=1
   if r['body'][q['slot']]['pixels']>100:visible[q['slot']].add(q['pose'])
 held=[]
 for h in groups['FLOOR_HELD']:
  rgb=np.asarray(Image.open(CASE/'snap'/snaps[h['frame']]['file']).convert('RGB'))
  bound=check_latch(rgb,(CASE/h['file']).read_bytes(),(CASE/displays[h['frame']]['palette_file']).read_bytes(),h['start'],h['control'],h['tap'])
  held.append(dict(frame=h['frame'],pixels=bound['pixels'],DMAReconstructed=False))
 assert video['frames']+len(held)==len(expected)and len(held)==30
 assert palette_checks>len(expected)and all(visible[s]for s in(1,2))
 # Continuous original CPU/shift-register/DMA operations, one initial base only.
 continuous=erase.inspect(CASE);assert continuous['passed'],continuous
 pins.update(continuous['inputHashes'])
 sound=groups['FLOOR_SOUND'];assert sound and all(r['at']==0x01d01030 and r['mask']==65535 for r in sound)
 assert all(float(a['seconds'])<float(b['seconds'])for a,b in zip(sound,sound[1:]))
 mix=CASE/'native_mix.wav';assert launch.sha(mix)==meta['mix_sha256']
 with wave.open(str(mix),'rb')as wav:
  assert(wav.getnchannels(),wav.getsampwidth(),wav.getframerate())==(2,2,48000)
  duration=wav.getnframes()/48000
  first=int(float(phase[0]['seconds'])*48000);last=int(float(phase[-1]['seconds'])*48000)
  assert 0<=first<last<wav.getnframes()
  wav.setpos(first);pcm=np.frombuffer(wav.readframes(last-first),dtype='<i2')
  assert np.count_nonzero(pcm)>48000
 audio=dict(duration=duration,firstSample=first,lastSample=last,peak=int(np.max(np.abs(pcm.astype(np.int32)))),nonzeroSamples=int(np.count_nonzero(pcm)),
  nativeSoundWrites=len(sound),audioAcceptance=False)
 launch.module_pins(pins)
 return dict(passed=True,candidate=launch.NAME,nativeState=state,unchangedOriginalPhysicalAndTombBranchTrajectory=True,
  sampledFrames=len(expected),exactReplayedFrames=video['frames'],exactHeldScanouts=len(held),
  exactScreenPixels=sum(r['display_pixels']for r in video['records'])+sum(r['pixels']for r in held),
  exactOwnedPixels=sum(b['pixels']for r in video['records']for b in r['body'].values()),
  sourceBoundProjections=len(queues),fullPhysicalPaletteChecks=palette_checks,nativeShadowCopies=shadows['checked_copies'],
  continuousErase={k:continuous[k]for k in('continuousExactPreBuffers','continuousExactFlips','shiftLoads','shiftFills','nativeShiftTransfers','oneInitialBaseOnly')},
  visiblePoses={s:sorted(v)for s,v in visible.items()},heldScanouts=held,records=video['records'],audioInventory=audio,inputHashes=pins,
  fullTombArtAudioAcceptance=False,allFinishersAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 assert not OUT.exists(),'Never overwrite executed evidence'
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k]for k in('passed','error','sampledFrames','exactReplayedFrames','exactScreenPixels','nativeShadowCopies','audioInventory')if k in report}),flush=True)
 raise SystemExit(0 if report['passed']else 1)
