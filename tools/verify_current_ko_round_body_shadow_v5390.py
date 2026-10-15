"""Actual Dead Pool KO/rebuild: complete call-phase body and native shadow proof.

Reuses two unchanged, physically identical native runs. No invented POST_FIELD
records and no noncombat exclusions. This is not canonical art or all-KO proof.
"""
import copy,datetime,inspect,json,re,traceback
from collections import Counter,defaultdict
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import verify_special_shadow_v5141 as original
import verify_native_extended_cpu_v2946 as ledgers
ROOT,need,sha=current.ROOT,current.need,current.sha
FOLDER=ROOT/'audit_v5351_current_cpu_sonya_square_human_kano'
SCENE=ROOT/'audit_v5386_current_cpu_ko_round_scene_ram'
PARENT=ROOT/'audit_v5389_current_cpu_ko_round_scene_progress/progress.json'
PROOF=ROOT/'audit_v5387_current_cpu_ko_round_scene_ram_checked/report.json'
OUT=ROOT/'audit_v5391_current_ko_round_body_shadow_checked'
FIRST,LAST=3000,3340

def records(log,prefix):
 rows=defaultdict(list)
 for line in log.splitlines():
  if line.startswith(prefix):
   pairs=re.findall(r'(\w+)=([^\s]+)',line);need(len(pairs)==len(dict(pairs)),'Unique actual observer fields')
   row=dict(pairs)
   if 'frame'in row and FIRST<=int(row['frame'])<=LAST:rows[line.split()[0]].append(row)
 return rows

def build_checker():
 # Preserve every original descriptor, clip, queue, stream and shadow gate;
 # replace only the original two-human/combat-only callback scope binding.
 source=inspect.getsource(original.check_body)
 before="set(compositions)=={(f,s)for f in frames for s in(1,2)}"
 need(source.count(before)==1,'One original body-call coverage predicate')
 source=source.replace(before,"set(compositions)==b['bodyKeys']",1)
 ns=dict(original.check_body.__globals__)
 exec(compile(source,__file__+'::entire_original_body_with_actual_preCPU_call_keys','exec'),ns)
 body_check=ns['check_body']
 source=inspect.getsource(original.check)
 start=source.index(' # The older physical/ownership/health checker')
 end=source.index(' begins=rows[',start)
 source=source[:start]+""" state=b['physicalState']
 entry_frames=set()
 fields=rows['MK2_HPHASE_POST_FIELD']
 frames=set(range(FIRST,LAST+1))
 owners=b['owners'];ids={1:17,2:18};floors=b['floors']
 body_parts,published,clipped=check_body(b,guest,payload,frames,owners,ids)
"""+source[end:]
 before="len(begin_by)==len(begins)==len(by)and set(begin_by)==set(by)"
 need(source.count(before)==1,'One original shadow-call coverage predicate')
 source=source.replace(before,"len(begin_by)==len(begins)==len(b['shadowKeys'])and set(begin_by)==b['shadowKeys']",1)
 ns=dict(original.check.__globals__,check_body=body_check,FIRST=FIRST,LAST=LAST)
 exec(compile(source,__file__+'::entire_original_stream_projection_pen_cadence_with_real_call_phases','exec'),ns)
 return ns['check']

def check_context(b,check,guest,payload,gfx):
 num=original.num;by=b['roundBy'];rows=b['rows']
 pre={(f,s)for f in range(FIRST,LAST+1)for s in(1,2)if by[f,s]['valid']}
 post={(f,s)for f in range(FIRST,LAST+1)for s in(1,2)if by[f+1,s]['valid']}
 need(b['bodyKeys']==pre and b['shadowKeys']==post,'Coverage derived from actual pre/post physical publications, not trace membership')
 for tag in('MK2_HPHASE_CANDIDATE','MK2_HPHASE_QUEUE','MK2_HPHASE_SHADOW_BEGIN','MK2_HPHASE_PROJECTION'):
  for t in rows[tag]:
   f,s=num(t,'frame'),num(t,'slot');native=by[f if tag in('MK2_HPHASE_CANDIDATE','MK2_HPHASE_QUEUE')else f+1,s]
   need(native['valid']and num(t,'actor')==num(t,'owner')==native['actor']==native['owner']and
    num(t,'main')==native['main']and num(t,'id')==native['id']==(17 if s==1 else 18),
    'Actual call owner/identity bound to independent callback phase, including recycled round actors')
   need(t['writes']=='0'and t['assistance']=='none','Every actual body/shadow observation remains read-only')
   if tag in('MK2_HPHASE_SHADOW_BEGIN','MK2_HPHASE_PROJECTION'):
    need(num(t,'body')==native['body'],'Shadow eligibility bound to genuine post-task native body flags')
   if tag=='MK2_HPHASE_PROJECTION':
    need(num(t,'floor')==native['floor']==b['floors'][s]and original.short(num(t,'world')>>16)==native['y'],
     'Every projected own ground anchor and vertical world coordinate match actual post-task Main/object')
 for t in rows['MK2_HPHASE_POST_FIELD']:
  f,s=num(t,'frame'),num(t,'slot');native=by[f+1,s]
  for k in('mode','actor','main','owner','id','hp','floor','y','body','action','flags','vx','vy','gravity','trail'):
   # Original POST_FIELD writes action decimal; original.num already preserves it.
   need(num(t,k)==native[k],'Every retained actual POST_FIELD agrees with next pre-CPU state: '+k)
 nonlive={num(t,'frame'):num(t,'mode')for t in rows['MK2_HPHASE_NATIVE_NONLIVE']}
 expected_nonlive={f:by[f+1,1]['mode']for f in range(FIRST,LAST+1)if by[f+1,1]['mode']!=2}
 need(nonlive==expected_nonlive,'No noncombat callback fabricated or excluded')
 need({(num(t,'frame'),num(t,'slot'))for t in rows['MK2_HPHASE_POST_FIELD']}==
  {(f,s)for f in range(FIRST,LAST+1)for s in(1,2)if f not in nonlive},'Original POST_FIELD publication predicate retained')
 result=check(b,guest,payload,gfx)
 # Bind actual FIFO geometry and shadow-copy streams to the independent whole
 # scene hardware trace already replayed through native VRAM and displayed RGB.
 scene=b['sceneDMA'];hardware=Counter()
 for t in scene:
  hardware[tuple(num(t,k)for k in('frame','source','command','x','y','width','height','pc'))]+=1
 published=Counter()
 for t in rows['MK2_HPHASE_QUEUE']:
  xy=num(t,'xy');size=num(t,'size')
  published[(num(t,'frame'),num(t,'source'),num(t,'command')>>16,xy&1023,(xy>>16)&511,size&65535,size>>16,0xff804640)]+=1
 need(all(hardware[k]>=v for k,v in published.items()),'Every actual whole native fighter FIFO publication reaches source-qualified scene DMA')
 shadow=Counter(tuple(num(t,k)for k in('frame','source','command','x','y','width','height','pc'))for t in rows['MK2_HPHASE_SHADOW_DMA'])
 scene_shadow=Counter(tuple(num(t,k)for k in('frame','source','command','x','y','width','height','pc'))for t in scene if num(t,'pc')in(0xff8015a0,0xff801610))
 need(shadow==scene_shadow,'Entire actual native shadow hardware stream equals independently accepted scene trace')
 need((3208,1)in pre and (3208,2)in pre and not any(f==3208 for f,s in post)and
  not any(f==3209 for f,s in pre)and (3209,1)in post and (3209,2)in post,'Actual retirement/rebuild phase split preserved')
 corpse=[t for t in rows['MK2_HPHASE_SHADOW_BEGIN']if num(t,'slot')==1 and not num(t,'body')&16]
 need(corpse and all(by[num(t,'frame')+1,1]['hp']==0 for t in corpse),'Native ineligible corpse has genuine zero HP, not missing active fighter shadow')
 result.update(allModeWindow=[FIRST,LAST],actualPhysicalBodyCallKeys=len(pre),actualPhysicalShadowCallKeys=len(post),
  actualNoncombatCallbacks=len(nonlive),actualCorpseIneligibleCalls=len(corpse),
  everyPublishedBodyBoundToWholeSceneDMA=True,entireShadowHardwareStreamBoundToWholeScene=True,
  observedBodyAndShadowSourcesThroughActualKOAndRoundRebuildAccepted=True,
  noInventedPostFields=True,canonicalArtisticGroundingAccepted=False,allKOContextsAccepted=False)
 return result

def run():
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 parent=json.loads(PARENT.read_text());scene=json.loads(PROOF.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and scene['passed']and
  scene['completeKOToNextRoundNativeSceneEraseAndRGBWindowAccepted'],'Authoritative full native transition scene already accepted')
 pins={str(p.resolve()):sha(p)for p in(PARENT,PROOF,Path(__file__),Path(original.__file__),Path(ledgers.__file__))}
 for table in(parent['newInputHashes'],scene['inputHashes']):
  for p,h in table.items():need(sha(p)==h,'Every authoritative retained dependency unchanged: '+p);pins[p]=h
 observed_path=ROOT/'audit_v5352_current_cpu_sonya_square_observed/report.json'
 observed=json.loads(observed_path.read_text());need(observed['passed']and observed['nativeExit']==0 and observed['originalWholePhysicalTrajectoryUnchanged'],'Existing actual full native body observer reached original terminal')
 for p,h in observed['inputHashes'].items():need(sha(p)==h,'Every actual original body capture input unchanged');pins[p]=h
 pins[str(observed_path)]=sha(observed_path)
 log=(FOLDER/'run.log').read_text();scene_log=(SCENE/'run.log').read_text()
 prefixes=('MK2_CPU_PAIR_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_CPU_CHOICE_','MK2_SQUARE_NATIVE_','MK2_P2CPU_','MK2_SQUARE_BOUNDARY_','MK2_SQUARE_LOCK_')
 select=lambda text:[s for s in text.splitlines()if s.startswith(prefixes)]
 need(select(log)==select(scene_log)and len(select(log))==8848,'Entire original actual input/RNG/state/HP/CPU trajectory exactly equal across two complementary native observations')
 health,by=ledgers.health_ledger(log,guest,'kano');state=ledgers.state_ledgers(log,guest,'kano',by)
 rows=records(log,'MK2_HPHASE_');all_streams=json.loads((FOLDER/'shadow_stream_memory_proofs.json').read_text())
 used={f'{t["graphic"]}_{t["width"]}_{t["height"]}_{t["command"]}'for t in rows['MK2_HPHASE_PROJECTION']}
 streams=[t for t in all_streams if t['stream']in used];need({t['stream']for t in streams}==used,'Every actual transition source stream retained')
 owners={s:(by[FIRST,s]['actor'],by[FIRST,s]['main'])for s in(1,2)}
 floors={s:by[FIRST,s]['floor']for s in(1,2)}
 b=dict(move='square',side=2,rows=rows,streams=streams,roundBy=by,owners=owners,floors=floors,
  bodyKeys={(f,s)for f in range(FIRST,LAST+1)for s in(1,2)if by[f,s]['valid']},
  shadowKeys={(f,s)for f in range(FIRST,LAST+1)for s in(1,2)if by[f+1,s]['valid']},
  physicalState=state,sceneDMA=records(scene_log,'MK2_NAT_CAMPAIGN_FLOOR_')['MK2_NAT_CAMPAIGN_FLOOR_DMA'])
 gfx=original.reconstruct(pins);stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for a,z in((0xff801070,0xff8017b0),(0xff804160,0xff804430)):
  a,z=(a-0xff800000)//8,(z-0xff800000)//8;need(guest[a:z]==stock[a:z],'Whole original native body/shadow instruction kernels unchanged')
 check=build_checker();case=check_context(b,check,guest,payload,gfx);faults=[]
 tests=[('body_source','MK2_HPHASE_CANDIDATE','source','00000000'),
  ('body_y','MK2_HPHASE_QUEUE','xy','00000000'),('shadow_owner','MK2_HPHASE_SHADOW_BEGIN','owner','01000000'),
  ('eligible_flag','MK2_HPHASE_SHADOW_BEGIN','body','0002'),('native_floor','MK2_HPHASE_PROJECTION','floor','999'),
  ('world_y','MK2_HPHASE_PROJECTION','world','00000000'),('descriptor','MK2_HPHASE_PROJECTION','dx','999'),
  ('camera','MK2_HPHASE_PROJECTION','b4','00000000'),('shadow_pen','MK2_HPHASE_SHADOW_DMA','color','0101'),
  ('shadow_row_source','MK2_HPHASE_SHADOW_DMA','source','00000001')]
 for label,tag,k,value in tests:
  changed=copy.deepcopy(b);t=changed['rows'][tag][0];need(t[k]!=value,'Effective actual observation mutation');t[k]=value
  try:check_context(changed,check,guest,payload,gfx)
  except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual mutation accepted: '+label)
 for label in('missing_rebuilt_body','missing_rebuilt_shadow','wrong_ROM_stream','wrong_packed_row','missing_scene_body'):
  changed=copy.deepcopy(b)
  if label=='missing_rebuilt_body':changed['rows']['MK2_HPHASE_CANDIDATE']=[t for t in changed['rows']['MK2_HPHASE_CANDIDATE']if not(t['frame']=='3210'and t['slot']=='1')]
  elif label=='missing_rebuilt_shadow':changed['rows']['MK2_HPHASE_SHADOW_BEGIN']=[t for t in changed['rows']['MK2_HPHASE_SHADOW_BEGIN']if not(t['frame']=='3209'and t['slot']=='1')]
  elif label=='wrong_ROM_stream':changed['streams'][0]['sha256']='0'*64
  elif label=='wrong_packed_row':changed['streams'][0]['actualRowStarts'][1]+=1
  else:
   q=changed['rows']['MK2_HPHASE_QUEUE'][0]
   changed['sceneDMA']=[t for t in changed['sceneDMA']if not(t['frame']==q['frame']and t['source']==q['source']and t['pc']=='FF804640')]
  need(changed!=b,'Effective actual deletion/source fault')
  try:check_context(changed,check,guest,payload,gfx)
  except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual missing/source mutation accepted: '+label)
 for p in FOLDER.rglob('*'):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All final source/evidence/native bytes stable')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=current.NAME,
  case=case,wholeNativeHealth=health,wholeNativeState=state,actualFaultsRejected=faults,inputHashes=pins,
  reusedExistingNativeCaptures=True,newNativeBoots=0,newBuilds=0,rawMediaFilesWritten=0,
  wholeSceneProof=str(PROOF),fullPortAcceptance=False,canonicalArtisticFidelityAccepted=False,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable native transition body/shadow proof')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualFaultsRejected','wholeNativeHealth','wholeNativeState')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
