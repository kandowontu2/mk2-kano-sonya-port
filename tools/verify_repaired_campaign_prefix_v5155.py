"""Current4992 actual Sonya ladder prefix, not a tower/ending acceptance.

Verify source-bound native schedule/selection/winner advancement, independent
unchanged per-field Kitana/Jax physical replay and real original Jax callbacks.
The growing gzip log is read only to an actual completed stage-five boundary.
"""
import gzip,hashlib,json,re,struct,sys,traceback
from pathlib import Path
import native_subzero_legs_context_v4993 as native
import run_repaired_sonya_campaign_v5153 as capture
import verify_sonya_p1_kitana_guard_prefix_v4799 as kitana
import verify_sonya_p1_jax_jump_guard_prefix_v4813 as jax

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v5156_repaired_sonya_campaign_prefix_checked'

def read_completed_prefix():
 lines=[];count=0
 with gzip.open(capture.OUT/'run.log.gz','rt',encoding='utf-8',newline='')as reader:
  try:
   for line in reader:
    if not line.endswith('\n'):break
    lines.append(line);count+=len(line.encode())
    need(count<=128*1024*1024,'Finite complete early campaign observation window')
    if line.startswith('MK2_NAT_CAMPAIGN_STAGE ')and ' stage=5 'in line:
     return ''.join(lines)
  except EOFError:pass
 raise ValueError('Await actual completed Jax-to-stage-five event; live run is not a failure')

def campaign_prefix(text,guest):
 rows=kitana.original.parse(text)
 def u16(at):return struct.unpack_from('<H',guest,(at-0xff800000)//8)[0]
 def u32(at):return struct.unpack_from('<I',guest,(at-0xff800000)//8)[0]
 table=u32(0xff8a11f0)
 roms=[r for r in rows if r['tag']=='ROM']
 need(len(roms)==6 and [int(r['order'])for r in roms]==list(range(6)),'Six actual native schedule rows')
 for r in roms:
  order=int(r['order']);address=u32(table+order*32)
  need(int(r['table'],16)==table and int(r['list'],16)==address and
   [int(i)for i in r['ids'].split(',')]==[u16(address+i*16)for i in range(17)],
   'Actual native schedule source bytes, not synthetic opponents')
 need(not re.search(r'^MK2_MILEENA_CAMPAIGN_OVERRUN ',text,re.M),'No observed original cache global overrun in completed prefix')
 selection=None;schedule=None;last_stage=None;wins={};stages=[];own=0;specials=0
 entries={'ring':(0xffffb400,0xffffb420),'square':(0xffffca00,0xffffca20),
  'bicycle':(0xfff9a400,0xfff9a430),'leg':(0xfff80800,0xfff80830)}
 for r in rows:
  need(r['human_slot']=='1'and r['fighter']=='sonya'and r['writes']=='0'and r['assistance']=='none',
   'Actual P1 physical-only true Sonya scope')
  tag=r['tag']
  if tag=='SELECT_ID':need(r['roster']=='18'and r['state']=='3','Actual native Sonya confirm roster')
  elif tag=='FIGHT':
   selection=int(r['selection']);schedule=int(r['schedule'],16)
   need(r['human']=='18:18','True Sonya match, never proxy state')
   need(r['cpu']==str(u16(schedule+int(r['stage'])*16))+':'+str(u16(schedule+int(r['stage'])*16)),
    'Actual owned scheduled CPU identity in early campaign')
  elif tag=='LIVE':
   need(r['human']=='18:18'and int(r['selection'])==selection and int(r['schedule'],16)==schedule,
    'True live Sonya and continued native schedule')
   need(r['cpu']==str(u16(schedule+int(r['stage'])*16))+':'+str(u16(schedule+int(r['stage'])*16)),
    'True live scheduled CPU identity')
  elif tag=='SPECIAL':
   address,pc=entries[r['move']]
   need(r['id']==r['roster']=='18'and r['actor']==r['a8']and r['main']==r['a13']and
    int(r['entry'],16)==address and int(r['at'],16)==address+16 and int(r['pc'],16)==pc,
    'Actual owned native Sonya special entry and registers')
   specials+=1
  elif tag=='WIN':
   slot=int(r['slot']);identifier=int(r['id']);stage=int(r['stage']);health=list(map(int,r['health'].split(',')))
   need(slot in(1,2)and int(r['pc'],16)==0xff8296b0 and int(r['entry'],16)==0xfffef800+identifier*32,
    'Actual original winner-table instruction and own row')
   need(identifier==(18 if slot==1 else u16(schedule+stage*16))and
    all(0<=h<=161 for h in health)and health[slot-1]>health[2-slot],
    'Native winning identity and actual winning health, including real timeouts')
   if slot==1:
    own+=1;key=(selection,stage);wins[key]=wins.get(key,0)+1
  elif tag=='STAGE':
   stage=int(r['stage']);need(stage==(0 if last_stage is None else last_stage+1),'Natural sequential early ladder stages')
   if last_stage is not None:
    need(wins.get((selection,last_stage),0)>=2,'Native own round wins required before next opponent')
   stages.append(stage);last_stage=stage
 need(stages==list(range(6))and own>=10 and specials>0,'Actual stage0..5 progression and genuine owned native specials')
 return dict(actualStages=stages,actualOwnNativeRoundWins=own,actualOwnedNativeSpecials=specials,
  actualPaidLosses=sum(r['tag']=='LOSS'for r in rows),actualSelectionConfirmRows=sum(r['tag']=='SELECT_ID'for r in rows),
  sourceBoundScheduleRows=6,actualNativeCacheOverrunObserved=False)

def run():
 need(not OUT.exists(),'Fresh immutable current prefix proof')
 guest=native.expected();text=read_completed_prefix();raw=text.encode()
 pins=json.loads((capture.OUT/'input_hashes_before.json').read_text())
 need(all(sha(p)==h for p,h in pins.items()),'All actual current compiled and physical policy inputs unchanged')
 proofpath=capture.OUT/'guest_memory_proof.json';proof=json.loads(proofpath.read_text())
 need(proof['sha256']==native.GUEST_SHA==hashlib.sha256(guest).hexdigest().upper()and
  proof['bytes']==1048576 and proof['everyActualByteComparedInRAM']and proof['guestDumpFilesWritten']==0 and
  proof['captureSourceSHA256']==sha(capture.__file__)and proof['transportSourceSHA256']==sha(ROOT/capture.LUA),
  'Actual initialized full guest and exact currently executed host/Lua')
 actual=campaign_prefix(text,guest)
 replay_k=kitana.make_replay();replay_j=jax.make_replay()
 physical_k=replay_k(text);physical_j=replay_j(text);callbacks=jax.callbacks(text,guest)
 faults=[]
 def reject(label,check,damaged):
  need(damaged!=text,'Actual nonvacuous captured record mutation')
  try:check(damaged)
  except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Captured record fault admitted '+label)
 rows=kitana.original.parse(text);change=kitana.original.change
 first=lambda tag:next(r for r in rows if r['tag']==tag)
 f=first('SELECT_ID');reject('wrong_selection',lambda t:campaign_prefix(t,guest),change(text,'SELECT_ID',f['frame'],'roster',1))
 f=first('LIVE');reject('proxy_match',lambda t:campaign_prefix(t,guest),change(text,'LIVE',f['frame'],'human','1:1'))
 f=first('WIN');reject('foreign_winner_PC',lambda t:campaign_prefix(t,guest),change(text,'WIN',f['frame'],'pc','FFF00000'))
 f=first('ROM');reject('false_schedule',lambda t:campaign_prefix(t,guest),change(text,'ROM',f['frame'],'ids','1,'*16+'1'))
 for label,replay,tag in(('kitana',replay_k,'KITANA_FIELD'),('jax',replay_j,'JAX_FIELD')):
  f=first(tag)
  reject(label+'_proxy_actor',replay,change(text,tag,f['frame'],'human_id',1))
  reject(label+'_fabricated_input',replay,change(text,tag.replace('FIELD','DECISION'),f['frame'],'reason','fabricated'))
 line=next(l for l in text.splitlines()if l.startswith('MK2_JAX_GROUND_NATIVE ')and ' kind=ground_result 'in l)
 for key,value in(('pc','FFF00000'),('opcode','0000')):
  changed=re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
  reject('Jax_native_'+key,lambda t:jax.callbacks(t,guest),text.replace(line,changed,1))
 need(campaign_prefix(text,guest)==actual and replay_k(text)==physical_k and replay_j(text)==physical_j and
  jax.callbacks(text,guest)==callbacks,'All entire current positive checks restored')
 for p in[Path(__file__),proofpath,capture.OUT/'input_hashes_before.json',capture.OUT/'process.json']:
  pins[str(p.resolve())]=sha(p)
 for module in tuple(sys.modules.values()):
  path=getattr(module,'__file__',None)
  if path and Path(path).suffix=='.py'and Path(path).resolve().is_relative_to(ROOT/'tools'):
   pins[str(Path(path).resolve())]=sha(path)
 return dict(passed=True,candidate=native.NAME,executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,
  actualCampaignPrefix=actual,actualKitanaPhysicalReplay=physical_k,actualJaxPhysicalReplay=physical_j,
  actualJaxNativeCallbacks=callbacks,actualFaultsRejected=faults,inputHashes=pins,
  nativeLogUncompressedPrefixBytes=len(raw),nativeLogUncompressedPrefixSHA256=hashlib.sha256(raw).hexdigest().upper(),
  terminalPrefixBoundary=text.splitlines()[-1],logStillGrowingIsNotPinnedAsTerminal=True,prefixProofOnly=True,
  actualNaturalTowerClearAccepted=False,fullEndingPixelsAccepted=False,completeAudioAccepted=False,
  fullPortAcceptance=False,rawGuestMediaFilesWritten=0)

if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable evidence leaf');OUT.mkdir()
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualJaxNativeCallbacks')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
