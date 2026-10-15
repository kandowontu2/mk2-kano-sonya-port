"""Current earned native Pit: actual cinematic victim, complete exit, FIFO and raster.

Each bounded physical-input case checks the whole guest/source, all queued
physical and cinematic bodies, original falling/impact cadence, native effect
and gender command routing, complete saved-pass scanouts and continuous erase.
Not all victims, all stage audio, campaigns, artistic approval or whole port.
"""
import argparse,json,re,struct,traceback,wave
from pathlib import Path
from collections import defaultdict
import numpy as np
from PIL import Image
import verify_current_native_tomb_matrix_v2080 as prior
import verify_pit_initial_cache_v680_v2 as initial
from verify_native_floor_display_v602 import check_latch
ROOT=prior.ROOT
launch=prior.launch;raster=prior.raster;erase=prior.erase;art=prior.art
CASES={'kano_p1':('kano',1,'audit_v2094_current_kano_p1_pit_nextscreen_fullscene'),
       'sonya_p2':('sonya',2,'audit_v2094_current_sonya_p2_pit_nextscreen_fullscene')}
raster.base.HEX|={'group','low','high','table','pointer','original','a2','a4','a5','a6','a8','a11','a13','dst'}
raster.base.STR|={'colors'}
def need(ok,message):
 if not ok:raise ValueError(message)
def signed(v):return(v&65535)-65536 if v&32768 else v&65535
def verify(case):
 fighter,side,leaf=CASES[case];folder=ROOT/leaf
 identity=17 if fighter=='kano'else 18;victim=35-identity
 ids=tuple(identity if s==side else victim for s in(1,2))
 pins=launch.source_pins();guest,_,payload=launch.current.expected()
 meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
 before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
 build=json.loads((ROOT/launch.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 need(meta['exit_code']==0 and meta['candidate']==launch.NAME and meta['cheats_enabled']is False,'Matched terminal unassisted current capture')
 need((meta['winner'],meta['side'],meta['arena'],meta['command_case'],meta['seconds'])==(fighter,side,6,'positive',900),'Requested physical earned Pit case')
 need(meta['guest_writes']==0 and meta['assistance']=='none'and meta['input_hashes']==before,'Input-only before/after pins')
 need(meta['executable_sha256']==build['executable_sha256']and meta['payload_sha256']==build['payload_sha256'],'Exact current executable/payload')
 need(all(before.get(f)==h for f,h in build['input_hashes'].items()),'All compiled inputs pinned')
 for file,wanted in before.items():
  need(launch.sha(file)==wanted,'Changed executed input '+file);pins[file]=wanted
  if Path(file).suffix in('.lua','.ps1','.json'):need(launch.sha(folder/'input_sources'/Path(file).name)==wanted,'Frozen source differs')
  if Path(file).suffix=='.lua':need(not re.search(r':write_|write_u\d+|load_?state|\.value\s*=(?!=)',Path(file).read_text()),'Guest state assistance')
 observer=(folder/'input_sources/mk2ks_native_pit_display_v2092.lua').read_text()
 need("dofile('mk2ks_native_stage_performer_v806.lua')"in observer and 'm+0x140'in observer and 'cine and p:read_u16(0x010601d0)==3'in observer,'Actual movie owner and exit capture')
 need(not re.search(r':write_|write_u\d+|set_value|clear_value|load_?state|\.value\s*=(?!=)',observer),'Observer must only read')
 runner=(folder/'input_sources/run_current_native_pit_display_v2093.ps1').read_text()
 need('-nocheat'in runner and '-noautoframeskip -frameskip 0'in runner and '-wavwrite'in runner,'Actual cheat-disabled full capture options')
 need((folder/'guest_maincpu.bin').read_bytes()==guest,'Entire actual guest independently reconstructed')
 log=(folder/'run.log').read_text(encoding='utf-8-sig')
 need(not re.search(r'WRONG CHECKSUMS|might not run correctly|LUA ERROR|Lua error|fatal error|stack traceback|access violation',log,re.I),'No runtime errors')
 baseline=ROOT/f'audit_v1714_{fighter}_pit_p{side}/run.log'
 old=baseline.read_text(encoding='utf-8-sig');pins[str(baseline)]=launch.sha(baseline)
 need(prior.classic(log)==prior.classic(old),'Entire original input/damage/motion/mode trajectory unchanged')
 state=prior.native.check_log(prior.classic(log),fighter,side,6,'positive')
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for start,stop in((0xff804040,0xff804470),(0xff85c300,0xff85c330),(0xff85c350,0xff85c4a0),
                   (0xff85c4c0,0xff85c700),(0xff8387c0,0xff838840),(0xff9e1290,0xff9e1480),(0xff82b800,0xff82bca0),(0xff80dcc0,0xff80de00)):
  lo,hi=(start-0xff800000)//8,(stop-0xff800000)//8
  need(guest[lo:hi]==original[lo:hi],'Original native Pit phase/copy/effect code changed')
 initial.stub(guest[(0xfffc9c00-0xff800000)//8:(0xfffca000-0xff800000)//8],
              guest[(0xff85bd30-0xff800000)//8:(0xff85bd60-0xff800000)//8])
 branches=[initial.execute(i)for i in range(19)]
 image=bytearray(prior.graphics.graphics(pins))
 for header,magic,source,dest in((0x1c0000,b'KFX1',0x1c4000,0x1e04000),(0x1c1000,b'KPI1',0x1e6000,0x1e50000),
  (0x1c2000,b'KPJ1',0x1f4000,0x1e60000),(0x1d0000,b'KBL1',0x1d4000,0x1e08000),(0x130000,b'KPT2',0x134000,0x1e80000)):
  need(payload[header:header+4]==magic,'Own declared graphics payload header')
  start,count,destination=struct.unpack_from('<III',payload,header+4)
  need(start==source and destination==dest and 0<count<=len(payload)-source and dest+count<=len(image),'Own graphics range')
  image[dest:dest+count]=payload[source:source+count]
 raster.source(pins);groups,buffers,_,_,owners=raster.data(folder)
 for g in groups['FLOOR_GFX']:
  need(0<=g['first']<g['first']+g['bytes']<=len(image)and bytes.fromhex(g['data'])==image[g['first']:g['first']+g['bytes']],'All native body/scenery/foreground/Pit graphics source-bound')
 begins,results,ends,physical=(groups[k]for k in('FLOOR_BEGIN','FLOOR_RESULT','FLOOR_RETIRED','FLOOR_PHYSICAL_RETIRED'))
 need(len(begins)==len(results)==len(ends)==len(physical)==1,'Actual action, movie retirement and separate physical retirement')
 origin=begins[0]['origin'];end=ends[0]['frame'];normal_end=physical[0]['frame']
 need(origin==state['action_frame']==results[0]['origin']and end==results[0]['retired'],'Actual action/exit binding')
 need(begins[0]['entry']==0xff8bdde0 and begins[0]['id']==identity,'Own native stage performer')
 expected=list(range(origin+1,end+31))
 need([s['frame']for s in groups['FLOOR_SNAP']]==expected and results[0]['snapshots']==len(expected),'Every movie and thirty later fields retained')
 need(end>normal_end+60 and physical[0]['mode']==9 and ends[0]['mode']==3,'Not premature normal-pointer retirement')
 phases=groups['FLOOR_PHASE'];states=groups['FLOOR_STATE']
 need([p['frame']for p in phases]==[s['frame']for s in states]==list(range(origin,end+31)),'Consecutive actual movie state/phase fields')
 need(all(float(a['seconds'])<float(b['seconds'])for a,b in zip(phases,phases[1:])),'Monotonic completed-field time')
 first=states[0];actors={s:first[f'p{s}']for s in(1,2)};mains={s:first[f'main{s}']for s in(1,2)}
 need(all(s['p1']==s['p2']==0 for s in states if s['frame']>=normal_end),'Physical actors retired independently of movie')
 need(all(tuple(s[f'roster{n}']for n in(1,2))==ids for s in states),'Native IDs persist')
 # Queue publication can precede native pointer clear within the same field.
 for slot in(1,2):
  at=0x01060220 if slot==1 else 0x01060df0
  lines=log.splitlines()
  positions=[i for i,line in enumerate(lines)if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_POINTER_STORE ')and f'frame={normal_end} 'in line and f'field={at:08X} 'in line]
  need(positions,'Actual physical pointer stores retained')
  pubs=[i for i,line in enumerate(lines)if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_QUEUE ')and f'frame={normal_end} 'in line and f'slot={slot} 'in line]
  need(not pubs or max(pubs)<min(positions),'Same-field body publication precedes actual native pointer store')
 constructors=groups['FLOOR_PIT_CONSTRUCTED'];need(len(constructors)==1,'One true constructed cinematic victim')
 cine=constructors[0];a,m=cine['actor'],cine['main']
 need(cine['id']==victim and cine['owner']==a and a not in actors.values(),'Actual Main+140 cinematic victim, no proxy')
 constructor_calls=[q for q in groups['FLOOR_PIT_NATIVE']if q['entry']in(0xff906ef0,0xff85bc10)]
 need(len(constructor_calls)==2 and all(q['a0']==victim and q['a2']==0 and q['a11']==actors[3-side]and q['a13']==m for q in constructor_calls),'Original native constructor carries actual defeated actor in A11 and true victim ID in A0')
 need(struct.unpack_from('<HI',guest,(0xff838790-0xff800000)//8)==(0xc080,0xfffe0800),'Source-bound current native composite entry hook')
 lookups=groups['FLOOR_PIT_LOOKUP'];need(len(lookups)==2,'Native fall and impact lookups')
 seq=0xff181000+(victim-17)*0x200;firstgroup=0xff182000+(victim-17)*384;firstdescriptor=0xff184000+(victim-17)*768
 enter,impact=(q['frame']for q in lookups)
 for q in lookups:
  need((q['at'],q['low'],q['high'],q['mask'],q['pc'],q['table'],q['actor'],q['main'],q['owner'],q['id'],q['mode'])==
    (0xff180800+victim*32,seq&65535,seq>>16,65535,0xff83b850,0xff180800,a,m,a,victim,9),'Actual own stream fetch and owner')
 mode=[q for q in groups['FLOOR_PIT_MODE_STORE']if q['before']==9 and q['value']==5]
 need(len(mode)==1 and mode[0]['frame']<end and mode[0]['pc']==0xff820390 and mode[0]['mask']==65535,'Original native movie exit, not observer stop')
 movie_exit=mode[0]['frame']
 need(end==min(s['frame']for s in states if s['mode']==3),'Original native next-screen transition, not invented retirement')
 initial_rows=groups['FLOOR_PIT_INITIAL'];need(len(initial_rows)==2,'One actual synchronous preload/return pair')
 begin,leave=initial_rows
 need((begin['entry'],leave['entry'],begin['frame'],leave['frame'])==(0xfffc9c00,0xfffc9df0,enter,enter),'Original preload same-field before own stream')
 need(begin['pose']==0 and leave['pose']==firstgroup and leave['a0']==0xff180c00,'Own cache before original registration')
 need(all(begin[k]==leave[k]for k in('actor','main','owner','id','cache','a1','a2','a3','a4','a5','a6','a7')),'Actual observed preserved preload registers')
 draws=[d for d in groups['FLOOR_PIT_DRAW']if d['actor']==a]
 need(len(draws)==22,'Own initial preload plus twenty falling groups and impact')
 need(draws[0]['frame']==enter and draws[0]['group']==firstgroup,'Synchronous native first body')
 for index,d in enumerate(draws[1:]):
  phase=index%5 if index<20 else 5;frame=enter+1+index*3 if index<20 else impact
  need((d['frame'],d['group'],d['actor'],d['main'],d['owner'],d['id'],d['x'],d['y'],d['cache'])==
    (frame,firstgroup+phase*64,a,m,a,victim,192,64,0x0105ed30 if 3-side==1 else 0x0105f230),'Original fall cadence, all own phases and centered origin')
  components=[c for c in groups['FLOOR_PIT_COMPONENT']if c['frame']==frame and c['actor']==a]
  need(len(components)==2 and [(c['source'],c['value'],c['dst'],c['main'])for c in components]==
    [(firstgroup+phase*64,firstdescriptor+phase*128,d['cache'],m),(firstgroup+phase*64+32,0,d['cache']+112,m)],'Exact native component/terminator, no overrun')
 palettes=groups['FLOOR_PIT_PALETTE'];need(len(palettes)==1,'Actual original movie palette constructor')
 pal=palettes[0];ptr=0xff800000+(0xfda00 if victim==17 else 0xfdb00)*8
 need((pal['variant'],pal['id'],pal['pointer'],pal['count'])==(0,victim,ptr,65),'Original normal true-ID movie palette')
 need(tuple(int(c,16)for c in pal['colors'].split(','))==struct.unpack_from('<65H',guest,(ptr-0xff800000)//8+2),'Every movie constructor palette source color')
 lifetime=groups['FLOOR_PIT_LIFETIME']
 firstgroup_set={firstgroup+i*64 for i in range(6)}
 cleared=min(q['frame']for q in lifetime if q['id']!=victim or q['pose']not in firstgroup_set)
 need(cleared==end+8,'Original four scheduler tick/eight display-field transition, no delayed private body')
 need(struct.unpack_from('<HHHI',guest,(0xff82bac0-0xff800000)//8)==(0x09c0,4,0x0d5f,0xff80dcc0),'Original native four-tick yield before scene object-list clear')
 need(all(q['owner']==a and q['id']==victim and q['pose']in firstgroup_set for q in lifetime if q['frame']<cleared),'Owned native cinematic object through normal held-impact interval')
 need(all(q['id']==0 and q['pose']==0 for q in lifetime if q['frame']>=cleared),'Native cinematic address repurposed to scenery, not persistent victim')
 queues={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']}
 inventory={(q['frame'],q['cursor']):q for q in groups['FLOOR_ALL_QUEUE']}
 need(len(queues)==len(groups['FLOOR_QUEUE'])and len(inventory)==len(groups['FLOOR_ALL_QUEUE'])>len(queues),'Complete unique FIFO inventory')
 parts=defaultdict(list);published=defaultdict(list);drawn=defaultdict(list);poses=defaultdict(set)
 for q in groups['FLOOR_QUEUE_PART']:parts[q['frame'],q['cursor']].append(q)
 transforms={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE_TRANSFORM']}
 need(set(transforms)==set(queues),'Every actual queue transform')
 for key,q in inventory.items():
  if q['actor']in actors.values()and q['frame']<=normal_end:need(key in queues,'Tracked live physical body omitted from FIFO')
  if q['actor']==a and enter<=q['frame']<cleared:need(key in queues,'Actual cinematic body omitted, including held native impact after mode9 exit')
  if q['actor']==a and q['frame']>=cleared:need(q['id']!=victim or q['pose']not in {firstgroup+i*64 for i in range(6)},'Own Pit body still published after next-screen transition')
  if q['actor']==a and q['frame']<enter:need(q['id']==0 and q['pose']==0,'Only original pre-construction scenery at subsequently reused movie address')
 for key,q in queues.items():
  s=q['slot'];need(s in(1,2,4)and q['owner']==q['actor'],'Actual physical/cinematic ownership')
  if s==4:
   need((q['actor'],q['main'],q['id'],q['roster'],q['kind'],q['parent'])==(a,m,victim,victim,2,cine['original'])and enter<=q['frame']<cleared,'Own live movie actor, no post-clear publication')
   need(q['pose']in {firstgroup+i*64 for i in range(6)}and(q['x'],q['y'])==(192,64),'Every own movie cache/center')
  else:
   need((q['actor'],q['main'],q['id'],q['roster'],q['kind'],q['parent'])==(actors[s],mains[s],ids[s-1],ids[s-1],0,actors[s])and q['frame']<=normal_end,'Actual native physical fighter')
  need(q['multipart']==1 and key in inventory and all(q[k]==inventory[key][k]for k in('actor','source','pose','cache','id','body','facing','bank','pc')),'All native publications bound, no untracked true-ID body')
  composition=art.group(q,payload,guest);observed=parts[key]
  need(len(composition)==len(observed)and all(all(p[k]==v for k,v in e.items())for p,e in zip(observed,composition)),'Source descriptors equal every actual native cache part')
  need(q['row']==q['cache']+112*q['part']and q['pc']==0xff804420,'Exact native FIFO iterator')
  t=transforms[key];p=composition[q['part']]
  need(t['world']==((q['y']&65535)<<16)|(q['x']&65535),'Actual actor world transform')
  x,y=signed(t['world']),signed(t['world']>>16)
  if not t['a7']&1:x-=signed(t['camera']);y-=signed(t['camera']>>16)
  x-=p['dx'];y-=p['dy'];command=q['command']>>16
  if command&16:x+=p['width']-1
  if command&32:y+=p['height']-1
  x+=signed(t['display']);y+=signed(t['display']>>16)
  need((q['xy']&1023,q['xy']>>16&511)==(x&1023,y&511),'Native actual queued camera/flip/cache projection')
  published[q['cursor']].append(q)
 regs={q['event']:q for q in groups['FLOOR_DMA_REGS']};dmas={q['event']:q for q in groups['FLOOR_DMA']};dispatch={q['event']:q for q in groups['FLOOR_QUEUE_DISPATCH']}
 need(len(dmas)==len(groups['FLOOR_DMA'])and set(regs)==set(dmas)and len(dispatch)==len(groups['FLOOR_QUEUE_DISPATCH']),'Complete native command register inventory')
 for event,d in dmas.items():
  candidates=[q for q in published[regs[event]['b14']+192]if q['frame']<=d['frame']]
  q=max(candidates,key=lambda q:q['frame'])if candidates else None
  owned=bool(q and d['command']&15==2 and q['source']==d['source'])
  need((event in dispatch)==owned and d['slot']==(q['slot']if owned else 0),'Actual FIFO dispatch including cinematic victim, not palette')
  if not owned:continue
  p=art.group(q,payload,guest)[q['part']];pub=dispatch[event]
  need(queues[pub['queue_frame'],pub['cursor']]==q and all(pub[k]==q[k]for k in('actor','main','slot')),'Exact published actor/consumer')
  need((d['source'],d['width'],d['height'],d['command'],d['x'],d['y'],d['palette'])==
    (p['source'],p['width'],p['height'],p['command']|0x8002,q['xy']&1023,q['xy']>>16&511,q['bank']&0x7f00),'Exact native DMA/cache/palette')
  poses[q['slot']].add(q['pose']);drawn[d['frame']].append(q)
 need(poses[4]=={firstgroup+i*64 for i in range(6)},'Every own fall and impact pose actually dispatched')
 arguments=groups['FLOOR_PIT_NATIVE']
 shake=[q for q in arguments if q['entry']==0xff9e1290 and q['frame']==impact]
 sounds=[q for q in arguments if q['entry']==0xffa12530 and q['frame']==impact and q['a0']in(0xcf,0xcc,0xce)]
 sex=[q for q in arguments if q['entry']==0xffa12210 and q['frame']==impact]
 voice=0xcc if victim==17 else 0xce
 need(len(shake)==1 and shake[0]['a11']==0x50005,'Original five-step/five-pixel shake')
 need([q['a0']for q in sounds]==[0xcf,voice]and all(q['a8']==a and q['a13']==m for q in sounds),'Actual native impact and male/female voice groups')
 need(len(sex)==1 and sex[0]['a1']==0xccccccce and sex[0]['a8']==a and sex[0]['a13']==m,'True native gender selector')
 ports=[q for q in groups['FLOOR_SOUND']if q['frame']==impact and q['a8']==a]
 need(len(ports)==4 and all(q['at']==0x01d01030 and q['mask']==65535 and q['value']>>8==255 and q['a13']==m for q in ports),'Complete actual owned impact/victim port commands')
 need([q['pc']for q in ports]==[0xffa13c90,0xffa13d60]*2,'Native high/low port writers')
 commands=[((ports[i]['value']&255)<<8)|(ports[i+1]['value']&255)for i in(0,2)]
 wanted=[struct.unpack_from('<HH',original,(0xffa0ef20+g*32-0xff800000)//8)[1]for g in(0xcf,voice)];wanted[1]+=1
 need(commands==wanted,'Actual native serialized impact and gender-correct commands')
 cameras=[(q['frame'],q['cameraY'])for q in phases if impact-1<=q['frame']<=impact+20]
 changes=[p for i,p in enumerate(cameras)if i and p[1]!=cameras[i-1][1]]
 need(len(changes)==5 and [p[1]for p in changes]==[-5,0,-5,0,-5]and all(b[0]-a[0]==3 for a,b in zip(changes,changes[1:])),'Original alternating three-field shake cadence')
 print('Current native Pit full movie state/source/FIFO/phase/impact checks pass; replaying complete scene',flush=True)
 video=raster.inspect(folder)
 need(all(q['vram_mismatches']==q['displayed_mismatches']==q['shadow_mismatches']==0 for q in video['records']),'Every saved native drawing pass exact')
 displays={q['frame']:q for q in groups['FLOOR_DISPLAY']};snaps={q['frame']:q for q in groups['FLOOR_SNAP']}
 held=[]
 for h in groups['FLOOR_HELD']:
  rgb=np.asarray(Image.open(folder/'snap'/snaps[h['frame']]['file']).convert('RGB'))
  bound=check_latch(rgb,(folder/h['file']).read_bytes(),(folder/displays[h['frame']]['palette_file']).read_bytes(),h['start'],h['control'],h['tap'])
  held.append(dict(frame=h['frame'],pixels=bound['pixels'],DMAReconstructed=False))
 need(video['frames']+len(held)==len(expected),'Every completed movie scanout accounted, native no-DMA flashes retained')
 visible=set();palette_checks=0
 for q in video['records']:
  colors=np.fromfile(folder/displays[q['frame']]['palette_file'],dtype='<u4')
  for body in drawn[q['frame']-1]:
   if body['slot']==4:
    raw=struct.unpack_from('<65H',guest,(ptr-0xff800000)//8+2)
    expected_colors=np.array([sum(((((color>>shift)&31)<<3)|(((color>>shift)&31)>>2))<<dest for shift,dest in((10,16),(5,8),(0,0)))for color in raw],dtype=np.uint32)
    need(np.array_equal(colors[body['bank']&0x7f00:(body['bank']&0x7f00)+65],expected_colors),'All actual movie body palette entries reach scanout unchanged')
    palette_checks+=1
   else:
    prior.check_owned_body_palette(body,colors,guest,ids,body['slot']);palette_checks+=1
  if q['body'][4]['pixels']>100:visible.update(p['pose']for p in drawn[q['frame']-1]if p['slot']==4)
 need(visible==poses[4],'All six own movie poses visibly rendered')
 continuous=erase.inspect(folder);need(continuous['passed'],str(continuous));pins.update(continuous['inputHashes'])
 mix=folder/'native_mix.wav';need(launch.sha(mix)==meta['mix_sha256'],'Actual retained mix hash')
 with wave.open(str(mix),'rb')as wav:
  need((wav.getnchannels(),wav.getsampwidth(),wav.getframerate())==(2,2,48000),'Actual stereo PCM format')
  firstsample=int(float(phases[0]['seconds'])*48000);lastsample=int(float(phases[-1]['seconds'])*48000)
  need(0<=firstsample<lastsample<wav.getnframes(),'Complete scene mixed PCM retained')
  wav.setpos(firstsample);pcm=np.frombuffer(wav.readframes(lastsample-firstsample),dtype='<i2')
  need(np.count_nonzero(pcm)>48000,'Non-silent scene inventory')
 audio=dict(nativeCommands=commands,originalVictimVoiceGroup=voice,stereoFrames=lastsample-firstsample,
  peak=int(np.max(np.abs(pcm.astype(np.int32)))),waveformFidelityAcceptance=False)
 launch.module_pins(pins)
 return dict(passed=True,case=case,candidate=launch.NAME,nativeState=state,movie=dict(enter=enter,impact=impact,nextScreen=end,
  physicalPointerRetirement=normal_end,actualActor=a,actualMain=m,actualID=victim,originalNativeMode9Exit=movie_exit,actualMovieAddressRepurposed=cleared,fallingGroups=20,impactGroups=1,initialPreloads=1,
  staticInitializerBranches=branches,observedPreservedRegisters=7),sampledFrames=len(expected),exactReplayedFrames=video['frames'],
  exactHeldScanouts=len(held),exactScreenPixels=sum(q['display_pixels']for q in video['records'])+sum(q['pixels']for q in held),
  sourceBoundProjections=len(queues),fullOwnPaletteChecks=palette_checks,actualMoviePoses=sorted(visible),originalShakeChanges=changes,
  continuousErase={k:continuous[k]for k in('continuousExactPreBuffers','continuousExactFlips','shiftLoads','shiftFills','nativeShiftTransfers','oneInitialBaseOnly')},
  audioInventory=audio,records=video['records'],heldScanouts=held,inputHashes=pins,artisticApproval=False,
  allStageAudioAcceptance=False,allVictimsAccepted=False,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('case',choices=tuple(CASES));p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 need(not args.output.exists(),'Do not overwrite executed evidence')
 try:report=verify(args.case)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k]for k in('passed','error','sampledFrames','exactReplayedFrames','exactHeldScanouts','exactScreenPixels','movie','audioInventory')if k in report}),flush=True)
 raise SystemExit(0 if report['passed']else 1)
