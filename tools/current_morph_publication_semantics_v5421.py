"""No stale/orphan morph body publication in four existing native traces.

Stream retained evidence, never recapture or change game/controller state.
Independent physical pre-callback identity/pose, source-defined complete
composites and exact native FIFO dispatch establish semantic ownership.
Finite three-cycle fixtures only; not universal art/audio/port acceptance.
"""
import collections,copy,datetime,json,re,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import verify_morph_adversity_v3235 as physical
import verify_move_phase_shadow_v5089 as descriptors
import build_native_shang_morphs as assets

ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5420_current_morph_scene_progress/progress.json'
OUT=ROOT/'audit_v5422_current_morph_publication_progress'
PREFIX='MK2_NAT_CAMPAIGN_'
HEX=set('actor main owner pose cache body facing bank pc cursor source row size xy command palette parent b14 a0 a1 a3 a7 b10'.split())
TAGS={'FLOOR_ALL_QUEUE','FLOOR_QUEUE','FLOOR_QUEUE_DISPATCH','FLOOR_DMA_REGS','FLOOR_DMA','FLOOR_STATE'}
PAIR_KEYS=('actor','main','owner','id','roster','pose','body','action','y','floor')

def imported(source):return 0x10000000<=source<0x1a000000

def parse(line,ordinal):
 row=dict(re.findall(r'(\w+)=([^\s]+)',line))
 need(len(row)==len(re.findall(r'(\w+)=',line)),'Unambiguous actual native publication schema')
 for k,v in tuple(row.items()):
  if k in HEX:row[k]=int(v,16)
  elif re.fullmatch(r'-?\d+',v):row[k]=int(v)
 row['_line']=ordinal
 need(row['writes']==0 and row['assistance']=='none','Actual read-only native scene provenance')
 return row

def load(path,actors):
 rows=collections.defaultdict(list);counts=collections.Counter()
 # All publications are counted, including scenery outside the fighter family.
 # Retain any imported source irrespective of actor, plus every true body.
 with path.open(encoding='utf-8')as stream:
  for ordinal,line in enumerate(stream):
   if not line.startswith(PREFIX):continue
   tag=line.split(' ',1)[0][len(PREFIX):]
   if tag not in TAGS:continue
   counts[tag]+=1
   if tag=='FLOOR_ALL_QUEUE':
    actor=int(re.search(r' actor=([0-9A-F]+)',line)[1],16)
    source=int(re.search(r' source=([0-9A-F]+)',line)[1],16)
    if actor not in actors and not imported(source):continue
   elif tag in('FLOOR_DMA','FLOOR_DMA_REGS'):
    command=int(re.search(r' command=([0-9A-F]+)',line)[1],16)
    if command&15!=2:continue
    # Retain every body-mode DMA, not only imported sources. It also includes
    # ordinary scenery; native FIFO cursor/actor distinguishes that safely.
   rows[tag].append(parse(line,ordinal))
 return dict(rows),dict(counts)

def unique(rows,fields,label):
 result={tuple(r[k]for k in fields):r for r in rows}
 need(len(result)==len(rows),label)
 return result

def check(rows,by,side,groups,guest,payload):
 states=rows['FLOOR_STATE'];frames=[r['frame']for r in states]
 need(len(frames)==1974 and frames==list(range(frames[0],frames[-1]+1)),
  'Every intervening native timer field retained, not only dense targets')
 frame_set=set(frames);owners={by[frames[0],s]['actor']:s for s in(1,2)}
 source_groups={}
 for group in groups.values():
  for pose in group:
   for part in descriptors.native_group(dict(pose=f'{pose:08X}',facing='0000'),payload,guest):
    need(imported(part['graphic']),'Actual compressed current morph source belongs to inventoried imported range')
    need(part['graphic']not in source_groups,'Original morph component source unique')
    source_groups[part['graphic']]=pose
 for st in states:
  f=st['frame']
  need(st['mode']==2,'Complete actual fixture remains native combat')
  for s in(1,2):
   p=by[f+1,s]
   need((st[f'p{s}'],st[f'main{s}'],st[f'roster{s}'],st[f'state{s}'],st[f'health{s}'])==
    (p['actor'],p['main'],p['roster'],p['state'],p['hp']),
    'Native post-task state binds independent next physical callback')
 def parts(r):return descriptors.native_group(dict(pose=f"{r['pose']:08X}",facing=f"{r['facing']:04X}"),payload,guest)
 all_by=unique(rows['FLOOR_ALL_QUEUE'],('frame','cursor'),'Unique inventoried fighter/imported FIFO publications')
 queues=unique(rows['FLOOR_QUEUE'],('frame','cursor'),'Unique actual tracked native body packets')
 need(all_by.keys()==queues.keys(),'Every inventoried true-body or imported publication has exactly one genuine tracked native packet; no orphan')
 morph_fields=set();imported_parts=0
 for key,a in all_by.items():
  f=a['frame'];need(f in frame_set and a['actor']in owners,'No imported body publication outside either genuine current actor')
  s=owners[a['actor']];p=by[f,s]
  need(all(a[k]==p[k]for k in('actor','id','pose','body')),
   'Every inventoried body belongs to actual pre-task actor/identity/pose; no stale morph pose')
  ps=parts(a)
  need(a['source']in{v['graphic']for v in ps},
   'Every inventoried source belongs to actual current native pose; no stale morph component')
  q=queues[key]
  need(a['pc']==q['pc']==0xff804420 and a['_line']<q['_line']and
   all(a[k]==q[k]for k in('actor','pose','cache','id','body','facing','bank','source')),
   'Complete unfiltered inventory equals actual later tracked FIFO record')
  need(q['slot']==s and all(q[k]==p[k]for k in PAIR_KEYS)and q['multipart']==1 and
   q['row']==q['cache']+q['part']*112 and q['part']in range(len(ps)),
   'Every genuine FIFO body owner/current pose/cache component bound to independent physical pre-task state')
  part=ps[q['part']]
  need((q['source'],q['size'],q['command'])==
   (part['graphic'],part['width']|(part['height']<<16),(part['command']|0x8002)<<16),
   'Every native packet source/dimensions/pixel command exactly source-derived')
  if imported(a['source']):imported_parts+=1
  if a['source']in source_groups:
   need(s==side and a['id']==6 and a['pose']==source_groups[a['source']]and a['pose']in groups[side],
    'Declared morph component exists only on its actual current own Shang transition pose')
   morph_fields.add(f)
 compositions=collections.defaultdict(list)
 for q in queues.values():compositions[q['frame'],q['slot']].append(q)
 need(compositions.keys()=={(f,s)for f in frames for s in(1,2)},
  'Both genuine body composites actually published through every intervening timer field')
 for key,qs in compositions.items():
  need([q['part']for q in qs]==list(range(len(parts(qs[0])))),
   'Every current native body composite complete and unique, not just selected parts')
 expected_morph={f for f in frames if by[f,side]['pose']in groups[side]}
 need(morph_fields==expected_morph and len(morph_fields)==72,
  'All and only the actual 72 pre-task morph hold fields publish morph components; no post-return remnants')
 dispatches=rows['FLOOR_QUEUE_DISPATCH'];dispatch_by=unique(dispatches,('frame','event'),'Unique genuine FIFO DMA dispatches')
 regs=unique(rows['FLOOR_DMA_REGS'],('frame','event'),'Unique actual body-mode DMA registers')
 dma=unique(rows['FLOOR_DMA'],('frame','event'),'Unique actual body-mode hardware commands')
 need(regs.keys()==dma.keys(),'Each actual body-mode hardware command has its actual CPU/FIFO registers')
 dispatched=set();imported_dma=0
 for key,d in dma.items():
  r=regs[key];f=d['frame'];cursor=r['b14']+192;q=queues.get((f,cursor))
  need(r['_line']<d['_line']and(r['source'],r['command'])==(d['source'],d['command']),
   'Actual register and hardware source/command chronology')
  if q is None:
   need(not imported(d['source'])and d['slot']==0 and key not in dispatch_by,
    'No imported body DMA without actual genuine current queued owner; scenery is not a fighter')
   continue
  need(key in dispatch_by,'Every genuine queued body DMA has its actual native dispatch')
  dispatch=dispatch_by[key]
  need(q['_line']<r['_line']<dispatch['_line']<d['_line']and q['cursor']==cursor and
   (dispatch['queue_frame'],dispatch['cursor'],dispatch['slot'],dispatch['actor'],dispatch['main'],dispatch['source'])==
   (f,cursor,q['slot'],q['actor'],q['main'],q['source']),
   'Exact actual current native FIFO cursor/slot/actor/Main/source dispatch provenance')
  width,height=q['size']&65535,q['size']>>16
  need((d['slot'],d['source'],d['command'],d['width'],d['height'],d['pc'])==
   (q['slot'],q['source'],q['command']>>16,width,height,0xff804640),
   'Actual genuine body DMA consumes exact source-bound current packet')
  need((f,cursor)not in dispatched,'No packet reused as a stale second native draw')
  dispatched.add((f,cursor));imported_dma+=int(imported(d['source']))
 need(dispatched==queues.keys()and len(dispatch_by)==len(queues),
  'Every complete actual body packet drawn exactly once; no missing or fabricated dispatch')
 need(imported_dma==imported_parts,'Every imported body publication reaches exactly one genuine owned native hardware draw')
 return dict(passed=True,fullNativeTimerFields=1974,allActualBodyParts=len(queues),
  importedBodyParts=imported_parts,actualMorphHoldFields=72,
  actualMorphComponents=sum(a['source']in source_groups for a in all_by.values()),
  allActualBodyModeDMA=len(dma),actualGenuineBodyDispatches=len(dispatch_by),
  everyImportedPublicationGenuinelyOwned=True,noPostReturnMorphComponentPublished=True,
  everyCurrentCompleteCompositeSourceBound=True,everyBodyPacketDrawnExactlyOnce=True,
  bodyBindingPhase='pre-task identity/pose; floor state post-task binds next callback',
  nativeHorizontalPhysicsNotMistakenForStalePose=True,fullPortAcceptance=False)

def faults(rows,by,side,groups,guest,payload):
 tests=[]
 def change(label,tag,index,key,value):
  old=rows[tag][index];need(old[key]!=value,'Effective actual-record mutation '+label)
  altered=dict(rows);altered[tag]=list(rows[tag]);altered[tag][index]=dict(old,**{key:value});tests.append((label,altered))
 own=next((i,a)for i,a in enumerate(rows['FLOOR_ALL_QUEUE'])if a['actor']==by[a['frame'],side]['actor'])
 i,a=own
 change('orphan_imported_publication_actor','FLOOR_ALL_QUEUE',i,'actor',0x01000000)
 change('wrong_current_identity','FLOOR_ALL_QUEUE',i,'id',1)
 change('wrong_source_component','FLOOR_ALL_QUEUE',i,'source',a['source']+1)
 late=next((i,a)for i,a in enumerate(rows['FLOOR_ALL_QUEUE'])if a['actor']==by[a['frame'],side]['actor']and a['id']==6 and a['frame']>max(f for f,s in by if s==side and by[f,s]['pose']in groups[side]))
 i,a=late;old_pose=groups[side][0];old_source=descriptors.native_group(dict(pose=f'{old_pose:08X}',facing='0000'),payload,guest)[0]['graphic']
 change('old_morph_component_after_final_return','FLOOR_ALL_QUEUE',i,'source',old_source)
 change('old_morph_pose_after_final_return','FLOOR_ALL_QUEUE',i,'pose',old_pose)
 for label,k,v in(('dispatch_wrong_slot','slot',3-rows['FLOOR_QUEUE_DISPATCH'][0]['slot']),
   ('dispatch_wrong_cursor','cursor',rows['FLOOR_QUEUE_DISPATCH'][0]['cursor']+192),
   ('dispatch_old_queue_frame','queue_frame',rows['FLOOR_QUEUE_DISPATCH'][0]['queue_frame']-1),
   ('dispatch_wrong_source','source',rows['FLOOR_QUEUE_DISPATCH'][0]['source']+1)):
  change(label,'FLOOR_QUEUE_DISPATCH',0,k,v)
 altered=dict(rows);altered['FLOOR_QUEUE_DISPATCH']=rows['FLOOR_QUEUE_DISPATCH'][1:];tests.append(('missing_actual_native_dispatch',altered))
 # Actual imported DMA loses its cursor without changing any pixel/source;
 # this reaches ownership semantic gates, not a generic malformed-record error.
 i,r=next((i,r)for i,r in enumerate(rows['FLOOR_DMA_REGS'])if imported(r['source']))
 change('imported_DMA_orphan_cursor','FLOOR_DMA_REGS',i,'b14',0x01000000)
 rejected=[]
 for label,altered in tests:
  try:check(altered,by,side,groups,guest,payload)
  except ValueError as error:rejected.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual stale/orphan publication fault accepted: '+label)
 return rejected

def run():
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active','Actual current whole three-cycle scene checkpoint')
 pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
 for p,h in pins.items():need(sha(p)==h,'All original current source/physical/native/public dependencies unchanged')
 declared={t:[assets.address(assets.GROUPS+(i*3+j)*12)for j in range(3)]for i,t in enumerate(('kano','sonya'))}
 cases={};all_faults=[]
 for target in('kano','sonya'):
  for side in(1,2):
   key=f'{target}_p{side}';proof=ROOT/'audit_v5418_current_morph_scene_checked'/key/'report.json';report=json.loads(proof.read_text())
   need(report['passed']and report['candidate']==current.NAME and report['nativeExit']==0 and report['actualPhysicalTrajectoryUnchanged'],
    'Actual same current terminal unassisted whole-scene fixture '+key)
   path=ROOT/'audit_v5417_current_morph_scene_ram'/key/'run.log'
   need(sha(path)==report['inputHashes'][str(path)],'Actual previously source-qualified whole native scene trace unchanged')
   physical_path=ROOT/'audit_v5404_current_morph_adversity_ram'/f'{key}_repeat_morph_added'/'run.log'
   need(str(physical_path)in pins and sha(physical_path)==pins[str(physical_path)],'Independent actual physical trajectory unchanged')
   log=physical_path.read_text();by={(r['frame'],r['slot']):r for r in physical.rows(log,'PAIR')}
   actors={r['actor']for r in by.values()};need(len(actors)==2,'Two actual stable independent physical actors')
   rows,counts=load(path,actors);groups={side:declared[target],3-side:[]}
   case=check(rows,by,side,groups,guest,payload);rejected=faults(rows,by,side,groups,guest,payload)
   case.update(actualUnfilteredPublicationCount=counts['FLOOR_ALL_QUEUE'],
    actualAllHardwareDMA=counts['FLOOR_DMA'],actualRecordFaultsRejected=len(rejected),nativePID=report['nativePID'],
    sourceTrace=str(path),acceptedSceneProof=str(proof));cases[key]=case
   all_faults.extend(dict(case=key,**r)for r in rejected)
   pins[str(proof)]=sha(proof);pins[str(path)]=sha(path)
   print(key+' all 1974 native fields: complete source-bound body, no orphan/stale imported component, exact current FIFO dispatch',flush=True)
 ps="Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',ps],capture_output=True,text=True)
 need(census.returncode==0,'Actual native process census');live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 need(not any(r['ProcessId']in{c['nativePID']for c in cases.values()}for r in live),'All reused native captures actually terminal')
 for p in(Path(__file__).resolve(),Path(current.__file__),Path(physical.__file__),Path(descriptors.__file__),Path(assets.__file__)):
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All final current/public/source/evidence hashes unchanged')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  remaining=parent['remaining'],parentAdditiveJournal=str(PARENT),cases=cases,
  previousGoalTurnClassification='no progress: acknowledgement-only reply; authoritative current checkpoint and terminal-process census revalidated before next safe action',
  thisGoalTurnClassification='progress: semantic no-orphan/no-stale current repeated morph publication and exact FIFO dispatch proved across every intervening native field in both slots; effective actual-record faults rejected',
  actualNativeTimerFields=7896,actualBodyParts=sum(c['allActualBodyParts']for c in cases.values()),
  actualImportedBodyParts=sum(c['importedBodyParts']for c in cases.values()),
  actualMorphComponents=sum(c['actualMorphComponents']for c in cases.values()),
  actualUnfilteredNativePublicationsInventoried=sum(c['actualUnfilteredPublicationCount']for c in cases.values()),
  actualRecordFaultsRejected=all_faults,semanticOwnershipAbsenceCheckComplementsExactPixelReplay=True,
  noStaleMorphComponentAfterActualReturnInObservedFixtures=True,noImportedOrphanBodyPublicationOrDMAInObservedFixtures=True,
  nativeProcessCensus=live,newNativeBoots=0,newBuilds=0,newDeletedFiles=0,newLargeCaptureFiles=0,
  rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,publicPlayableChanged=False,refreshedReleaseZIP=False,
  allArenasCPUInterruptKOAudioMorphsAccepted=False,canonicalArtisticFidelityAccepted=False,fullPortAcceptance=False,
  newInputHashes=pins,nextAction='Continue remaining actual finisher/victim/arena/audio and CPU/interrupt/KO art contexts, then combined native selection/ladder/names/audio regression, dependency-aware obsolete-folder cleanup and refreshed ZIP. All original scope groups remain unchanged.')

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable semantic native morph checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','newInputHashes','remaining','actualRecordFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
