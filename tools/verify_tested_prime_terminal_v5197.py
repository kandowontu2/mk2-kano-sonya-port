"""Whole actual5187 bounded progression/guard replay, including native Shang morphs. No clear."""
import gzip,hashlib,inspect,json,re,traceback
from pathlib import Path
import native_subzero_legs_context_v4993 as native
import run_tested_prime_sonya_campaign_v5186 as capture
import verify_tested_prime_prefix_v5188 as prefix
import verify_repaired_campaign_prefix_v5155 as early

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v5198_tested_prime_terminal_checked'

def make_campaign():
 code=inspect.getsource(early.campaign_prefix)
 changes=[
  ("selection=None;schedule=None;last_stage=None;wins={};stages=[];own=0;specials=0",
   """selection=None;schedule=None;last_stage=None;wins={};stages=[];own=0;specials=0
 morph_ids=tuple(early.struct.unpack_from('<14H',guest,0xf9040))
 need(morph_ids==(0,1,2,3,4,5,5,7,8,9,10,11,17,18),'Actual source-bound fourteen native morph choices')
 last_morph={};morphs=0;last_loss={};stage_start={}
 def scheduled_cpu(r):
  expected=u16(schedule+int(r['stage'])*16)
  cpu=tuple(map(int,r['cpu'].split(':')))
  if cpu==(expected,expected):return True
  previous=last_morph.get(r['cpu_actor'])
  return bool(expected==6 and int(r['stage'])==14 and cpu[0]==6 and previous and
   int(previous['after'])==cpu[1]and previous['a13']==r['cpu_main'])"""),
  ("elif tag=='FIGHT':",
   """elif tag=='CPU_ID':
   pc=int(r['pc'],16);new=int(r['after'])
   need(int(r['mask'],16)==0xffff and r['a8']==r['actor'] and
    ((pc==0xff86e670 and new in morph_ids and new==int(r['a9'],16)&0xffff)or
     (pc==0xffa16700 and new==6 and new==int(r['a0'],16)&0xffff)),
    'Actual original CPU morph/restore instruction and actor/register provenance')
   last_morph[r['actor']]=r;morphs+=1
  elif tag=='LOSS':
   last_loss[int(r['stage'])]=r['frame']
  elif tag=='FIGHT':"""),
  ("need(r['cpu']==str(u16(schedule+int(r['stage'])*16))+':'+str(u16(schedule+int(r['stage'])*16)),\n    'Actual owned scheduled CPU identity in early campaign')",
   "need(scheduled_cpu(r),'Actual source-bound scheduled CPU or original proven Shang morph')"),
  ("need(r['cpu']==str(u16(schedule+int(r['stage'])*16))+':'+str(u16(schedule+int(r['stage'])*16)),\n    'True live scheduled CPU identity')",
   "need(scheduled_cpu(r),'True live scheduled CPU or original proven Shang morph')"),
  ("own+=1;key=(selection,stage);wins[key]=wins.get(key,0)+1",
   "own+=1;key=(selection,stage);wins.setdefault(key,[]).append(r['frame'])"),
  ("stage=int(r['stage']);need(stage==(0 if last_stage is None else last_stage+1),'Natural sequential early ladder stages')",
   """stage=int(r['stage'])
   need(stage==0 if last_stage is None else
    (stage==last_stage+1 or(last_stage==12 and stage==14 and u16(schedule+13*16)==14)),
    'Only actual source-bound endurance sentinel13 may be skipped')"""),
  ("need(wins.get((selection,last_stage),0)>=2,'Native own round wins required before next opponent')",
   """boundary=max(last_loss.get(last_stage,-1),stage_start[last_stage])
    earned=[at for at in wins.get((selection,last_stage),[])if boundary<at<r['frame']]
    need(len(earned)>=2,'Two actual own round wins in successful attempt required before next opponent')"""),
  ("stages.append(stage);last_stage=stage",
   "stages.append(stage);last_stage=stage;stage_start[stage]=r['frame']"),
  ("stages==list(range(6))and own>=10 and specials>0",
   "stages==list(range(13))+[14,15]and own>=28 and specials>0"),
  ("sourceBoundScheduleRows=6,actualNativeCacheOverrunObserved=False",
   "sourceBoundScheduleRows=6,actualOriginalMorphRestoreRows=morphs,actualNativeCacheOverrunObserved=False")]
 for before,after in changes:
  need(code.count(before)==1,'Unique source-bound native progression extension '+before)
  code=code.replace(before,after,1)
 scope=dict(vars(early),early=early)
 exec(compile(code,__file__+'::actual_source_bound_endurance_and_Sh ang'.replace(' ',''),'exec'),scope)
 return scope['campaign_prefix']


def run():
 need(not OUT.exists(),'Fresh immutable whole current terminal qualifier')
 result=json.loads((capture.OUT/'result.json').read_text())
 need(result['passed']and result['nativeExit']==0 and result['actualStages']==list(range(13))+[14,15]and
  not result['nativeCacheOverrunObserved']and not result['actualNaturalTowerClearAccepted'],
  'Actual native terminal and incomplete natural campaign, not inferred from elapsed time')
 pins=dict(result['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'All executed compiled/native/control inputs unchanged')
 with gzip.open(capture.OUT/'run.log.gz','rb')as reader:raw=reader.read()
 text=raw.decode();guest=native.expected()
 proof=json.loads((capture.OUT/'guest_memory_proof.json').read_text())
 need(proof['everyActualByteComparedInRAM']and proof['bytes']==1048576 and proof['guestDumpFilesWritten']==0 and
  proof['sha256']==native.GUEST_SHA==hashlib.sha256(guest).hexdigest().upper()and
  proof['captureSourceSHA256']==sha(capture.__file__)and proof['transportSourceSHA256']==sha(ROOT/capture.LUA),
  'Complete actual current RAM guest/source provenance')
 metadata=capture.qualify_payload_metadata_warning((capture.OUT/'stderr.log').read_text(),proof)
 need(metadata==result['qualifiedTestCandidateMetadataWarning']and
  not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',text,re.I),
  'Only exact compiled metadata discrepancy, no hidden native/callback errors')
 campaign=make_campaign()(text,guest)
 physical=prefix.make_replay()(text)
 need(physical['actualNativeHumanUppercut107Stores']>0,'Actual original HUMAN107 executed in whole trace')
 faults=[]
 check=make_campaign();rows_for_fault=early.kitana.original.parse(text)
 for tag,key,value in [('LIVE','human','1:1'),('CPU_ID','pc','FFF00000'),('CPU_ID','a13','01000000'),('STAGE','stage',13)]:
  f=next(r for r in rows_for_fault if r['tag']==tag and(tag!='STAGE'or r['stage']=='14'))
  damaged=early.kitana.original.change(text,tag,f['frame'],key,value)
  try:check(damaged,guest)
  except ValueError as error:faults.append(dict(tag=tag,key=key,rejectedBy=str(error)))
  else:raise ValueError('Actual native progression fault admitted '+key)
 need(check(text,guest)==campaign,'Whole actual native positive restored')
 need(physical['actualCompleteGuardFields']>2277 and physical['actualNativeLegActivations']>6,
  'Complete repeated real Sub-Zero encounters beyond independently qualified first prefix')
 prefixpath=prefix.OUT/'report.json';first=json.loads(prefixpath.read_text())
 need(first['passed']and first['actualPhysicalReplay']['actualNativeHumanUppercut107Stores']>0,
  'Actual independently qualified first encounter original human uppercut, not planned buttons')
 firsttext=prefix.completed_prefix();firstphysical=prefix.make_replay()(firsttext)
 need(firstphysical['actualNativeHumanUppercut107Stores']>0 and raw.startswith(firsttext.encode())and
  first['nativeLogPrefixSHA256']==hashlib.sha256(firsttext.encode()).hexdigest().upper(),
  'Actual complete first independently verified encounter remains byte-identical in whole terminal')
 kitana=early.kitana.make_replay()(text);jax=early.jax.make_replay()(text);callbacks=early.jax.callbacks(text,guest)
 rows=early.kitana.original.parse(text)
 finals=[r for r in rows if r['tag']=='RESULT'];need(len(finals)==1,'One actual native terminal')
 final=finals[0]
 need(final['frame']==322771 and final['selections']=='72'and final['losses']=='71'and
  final['ending']==final['ending_completed']=='-1'and final['pictures']==final['texts']=='0,0',
  'Actual71paid losses/72selections, no ending or victory supplied')
 deadline=re.findall(r'^MK2_CAMPAIGN_HOST_DEADLINE seconds=([\d.]+) limit=(\d+) assistance=none writes=0\r?$',text,re.M)
 need(len(deadline)==1 and deadline[0][1]=='5900'and 5900<=float(deadline[0][0])<5900.03,'Exact real host deadline')
 cache=[line for line in text.splitlines()if line.startswith('MK2_MILEENA_CAMPAIGN_RESULT ')]
 need(len(cache)==1 and 'global_cache_stores=0'in cache[0],'Actual original cache monitor zero stores through stop')
 subwins=[r for r in rows if r['tag']=='WIN'and r.get('stage')=='7'and r['slot']=='1']
 for p in[Path(__file__),Path(prefix.__file__),Path(early.__file__),prefixpath,*capture.OUT.rglob('*')]:
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every actual terminal/input/prefix byte retained')
 return dict(passed=True,nativeExit=0,actualWholeBoundedNativeCampaign=campaign,
  actualWholeSubZeroPhysicalReplay=physical,actualNativeProgressionFaultsRejected=faults,actualKitanaReplay=kitana,actualJaxReplay=jax,actualJaxNativeCallbacks=callbacks,
  actualFinalNativeResult=final,actualOwnSubZeroRoundWins=len(subwins),actualNativeCacheGlobalStores=0,
  actualFirstPrefixOriginalUppercut107Verified=True,actualFirstEncounterPhysicalReplay=firstphysical,exactCompiledMetadataWarning=metadata,
  completeUncompressedNativeLogBytes=len(raw),completeUncompressedNativeLogSHA256=hashlib.sha256(raw).hexdigest().upper(),
  inputHashes=pins,actualNaturalTowerClearAccepted=False,deadlineIsNotClear=True,
  fullEndingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullArtAcceptance=False,fullPortAcceptance=False,
  nextAction='Native own wins reached Kintaro after original Shang morphs; no boss or ending clear accepted. Continue actual boss input evidence; all five scope groups remain.')

if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable actual result');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualJaxNativeCallbacks')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)


