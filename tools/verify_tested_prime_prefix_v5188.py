"""Independent actual Sub-Zero physical guard/leg replay; never a forced clear."""
import collections,gzip,hashlib,inspect,json,re,sys,traceback
from pathlib import Path
import native_subzero_legs_context_v4993 as native
import run_tested_prime_sonya_campaign_v5186 as capture
import verify_sonya_p1_kitana_guard_prefix_v4799 as kitana

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v5189_tested_prime_prefix_checked'

def make_replay():
 code=inspect.getsource(kitana.original.replay)
 changes=[("'GUARD_DECISION'","'SUBZERO_DECISION'"),("'GUARD_FIELD'","'SUBZERO_FIELD'"),
  ("'GUARD_ACTION'","'SUBZERO_ACTION'"),("f['human_slot'] == '2'","f['human_slot'] == '1'"),
  ("r['slot'] == '2'","r['slot'] == '1'"),('Actual true Sonya P2 identity','Actual true Sonya P1 identity'),
  ("f['cpu_id'] == f['cpu_roster'] == '18'","f['cpu_id'] == f['cpu_roster'] == '8'"),
  ("r['tag'] == 'SPECIAL' and r['move'] == 'leg'","r['tag'] == 'SPECIAL' and r['move'] == 'leg' and r['frame'] in decisions"),
  ('if ca in (4, 0xa, 0x10):','if ca in (4, 0xa, 0x10, 0x604):'),
  ("reason, upper = 'anti_air_attempt', frame\n                expected.append('High_Punch')",
   "reason, upper, move, leg = 'anti_air_attempt', frame, 'uppercut', frame"),
  ('if leg is not None and frame - leg < 12:','if leg is not None and frame - leg < (26 if move == \'uppercut\' else 12):'),
  ('if age < 9:','if age < 24:'),
  ('if 6 <= age < 9:','if 10 <= age < 13:')]
 for before,after in changes:
  need(code.count(before)==1,'Unique unchanged physical replay context boundary '+before)
  code=code.replace(before,after,1)
 need(code.count("f['cpu_roster'] == '18'")==4,'Exactly four opponent readiness/move predicates')
 code=code.replace("f['cpu_roster'] == '18'","f['cpu_roster'] == '8'")
 scope=dict(vars(kitana.original));exec(compile(code,__file__+'::original_complete_guard_plus_actual_freeze604','exec'),scope)
 return scope['replay']

def completed_prefix():
 lines=[];count=0;seen=False
 with gzip.open(capture.OUT/'run.log.gz','rt',encoding='utf-8',newline='')as reader:
  try:
   for line in reader:
    if not line.endswith('\n'):break
    lines.append(line);count+=len(line.encode())
    need(count<=160*1024*1024,'Bounded actual complete Sub-Zero encounter window')
    if line.startswith('MK2_NAT_CAMPAIGN_SUBZERO_FIELD '):seen=True
    if seen and ((line.startswith('MK2_NAT_CAMPAIGN_LOSS ')and ' stage=7'in line)or
     (line.startswith('MK2_NAT_CAMPAIGN_STAGE ')and ' stage=8 'in line)):
     return ''.join(lines)
  except EOFError:pass
 raise ValueError('Await actual complete first Sub-Zero loss or genuine next-stage boundary; do not rerun a live game')

def run():
 need(not OUT.exists(),'Fresh actual physical prefix qualifier')
 text=completed_prefix();guest=native.expected()
 proofpath=capture.OUT/'guest_memory_proof.json';proof=json.loads(proofpath.read_text())
 pins=json.loads((capture.OUT/'input_hashes_before.json').read_text())
 need(all(sha(p)==h for p,h in pins.items()),'All actually executed immutable current sources')
 need(proof['everyActualByteComparedInRAM']and proof['bytes']==1048576 and proof['guestDumpFilesWritten']==0 and
  proof['sha256']==native.GUEST_SHA==hashlib.sha256(guest).hexdigest().upper()and
  proof['captureSourceSHA256']==sha(capture.__file__)and proof['transportSourceSHA256']==sha(ROOT/capture.LUA),
  'Actual complete current initialized guest and exact physical controller')
 rows=kitana.original.parse(text);fields=[r for r in rows if r['tag']=='SUBZERO_FIELD']
 decisions=[r for r in rows if r['tag']=='SUBZERO_DECISION']
 need(fields and [r['frame']for r in fields]==[r['frame']for r in decisions],
  'Exactly one complete native state and physical decision for every actual Sub-Zero field')
 replay=make_replay();positive=replay(text)
 need(positive['actualNativeLegActivations']>0,'Actual owned native leg entry, never a planned command credited')
 need(positive['actualNativeHumanUppercut107Stores']>0,'Actual original HUMAN107 uppercut store must execute; planned prime is not success')
 faults=[];f=fields[0]
 for tag,key,value in(('SUBZERO_FIELD','human_id',1),('SUBZERO_FIELD','cpu_id',1),
  ('SUBZERO_FIELD','human_owner','01000000'),('SUBZERO_FIELD','health','0,161'),
  ('SUBZERO_FIELD','reset',1-int(f['reset'])),('SUBZERO_DECISION','reason','fabricated')):
  damaged=kitana.original.change(text,tag,f['frame'],key,value)
  try:replay(damaged)
  except ValueError as error:faults.append(dict(tag=tag,key=key,rejectedBy=str(error)))
  else:raise ValueError('Actual physical record fault admitted '+key)
 attack=next(r for r in rows if r['tag']=='INPUT'and r['frame']in {f['frame']for f in fields}and r['button']=='Low_Punch')
 damaged=kitana.original.change(text,'INPUT',attack['frame'],'button','High_Kick')
 try:replay(damaged)
 except ValueError as error:faults.append(dict(tag='INPUT',key='button',rejectedBy=str(error)))
 else:raise ValueError('Missing real physical LP edge admitted')
 need(replay(text)==positive,'Complete actual physical positive restored')
 cache=any(line.startswith('MK2_MILEENA_CAMPAIGN_OVERRUN ')for line in text.splitlines())
 need(not cache,'No observed original cache global overwrite in completed encounter prefix')
 actions=collections.Counter(int(f['cpu_action'])for f in fields)
 subwins=[r for r in rows if r['tag']=='WIN'and r.get('stage')=='7'and r['slot']=='1']
 for r in subwins:
  need(r['id']=='18'and r['entry']=='FFFEFA40'and r['pc']=='FF8296B0'and
   int(r['health'].split(',')[0])>int(r['health'].split(',')[1]),'Actual own Sub-Zero round win instruction and health')
 for p in[Path(__file__),proofpath,capture.OUT/'input_hashes_before.json',capture.OUT/'process.json']:
  pins[str(p.resolve())]=sha(p)
 for module in tuple(sys.modules.values()):
  path=getattr(module,'__file__',None)
  if path and Path(path).suffix=='.py'and Path(path).resolve().is_relative_to(ROOT/'tools'):
   pins[str(Path(path).resolve())]=sha(path)
 raw=text.encode()
 return dict(passed=True,actualPhysicalReplay=positive,actualCPUActionHistogram=dict(actions),
  actualOwnNativeSubZeroRoundWins=len(subwins),actualOwnNativeSubZeroWins=subwins,
  completedEncounterBoundary=text.splitlines()[-1],actualRecordFaultsRejected=faults,inputHashes=pins,
  nativeLogPrefixBytes=len(raw),nativeLogPrefixSHA256=hashlib.sha256(raw).hexdigest().upper(),
  prefixProofOnly=True,growingLogNotPinnedAsTerminal=True,actualNaturalTowerClearAccepted=False,
  fullEndingPixelsAccepted=False,completeAudioAccepted=False,fullPortAcceptance=False)

if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable proof');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualOwnNativeSubZeroWins')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)


