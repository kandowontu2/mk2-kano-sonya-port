"""Complete native Kitana Ring-spacing encounter, all original replay guards.

Positive or lost encounter is measured honestly; neither is a tower clear.
Current full guest, exact physical provenance and actual instruction/health
and winner rows are required. Faults mutate the actual capture, not fixtures.
"""
import gzip,hashlib,inspect,json,re,struct,traceback
from pathlib import Path
import run_sonya_p2_kitana_ring_probe_v5637 as capture
import verify_shang_jump_retry_prefix_v4306 as original
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v5640_sonya_p2_kitana_ring_probe_checked'

def make_replay():
 source=inspect.getsource(original.replay)
 changes=[
  ("((f['stage']=='9' and f['cpu_id']==f['cpu_roster']=='5') or",
   "((f['stage']=='2' and f['cpu_id']==f['cpu_roster']=='4') or\n              (f['stage']=='9' and f['cpu_id']==f['cpu_roster']=='5') or"),
  ("(r['stage']=='9' and r['id']==r['roster']=='5') or",
   "(r['stage']=='2' and r['id']==r['roster']=='4') or\n          (r['stage']=='9' and r['id']==r['roster']=='5') or"),
  ("int(r['stage']) in (9,12)","int(r['stage']) in (2,9,12)")]
 for before,after in changes:
  need(source.count(before)==1,'Entire original Ring input replay context extension '+before)
  source=source.replace(before,after,1)
 scope=dict(vars(original),__file__=__file__)
 exec(compile(source,__file__+'::entire_Ring_spacing_plus_true_Kitana4','exec'),scope)
 return scope['replay']

def native_gate(text,guest):
 rows=original.parse(text);losses=[r for r in rows if r['tag']=='LOSS'and r['stage']=='2']
 stages=[r for r in rows if r['tag']=='STAGE'];select=[r for r in rows if r['tag']=='SELECT_ID']
 need(select and all(r['roster']=='18'and r['state']=='3'for r in select),'True Sonya18 before every actual selection confirm')
 wins=[];damage=[]
 for r in rows:
  need(r['human_slot']=='2'and r['fighter']=='sonya'and r['writes']=='0'and r['assistance']=='none',
   'Every actual native row is true physical P2 Sonya, without guest writes or assistance')
  if r['tag']=='FIGHT':need(r['human']=='18:18','True actual Sonya fight, never proxy')
  if r['tag']=='LIVE':need(r['human']=='18:18','True actual live Sonya, never proxy')
  if r['tag']=='WIN'and r['stage']=='2':
   side=int(r['slot']);identifier=int(r['id']);hp=list(map(int,r['health'].split(',')))
   need(side in(1,2)and identifier==(18 if side==2 else 4)and r['pc']=='FF8296B0'and
    int(r['entry'],16)==0xfffef800+identifier*32 and all(0<=h<=161 for h in hp)and hp[side-1]>hp[2-side],
    'Actual native Kitana/Sonya winner-table instruction/identity and winning health')
   wins.append(r)
  if r['tag']=='HEALTH'and r['pc']=='FF836700'and int(r['after'])<int(r['before']):
   need(0<=int(r['after'])<int(r['before'])<=161,'Native collision damage never heals or underflows')
   damage.append(r)
 need(wins and damage,'Genuine original native winner and collision damage stores required')
 boundary=[s for s in text.splitlines()if s.startswith('MK2_KITANA_RING_PROBE_BOUNDARY ')]
 need(len(boundary)==1,'Exactly one real completed encounter boundary, not timed fallback')
 end=dict(re.findall(r'(\w+)=([^\s]+)',boundary[0]))
 won=end['stage']=='3'
 need((won and len([r for r in wins if r['slot']=='2'])>=2 and not losses and
  [int(r['stage'])for r in stages]==[0,1,2,3])or
  (not won and end['stage']=='2'and len(losses)==1 and [int(r['stage'])for r in stages]==[0,1,2]),
  'Actual two own Kitana round wins before advancement, or actual first loss; never invented victory')
 return dict(actualKitanaEncounterWon=won,actualOwnKitanaRoundWins=sum(r['slot']=='2'for r in wins),
  actualKitanaRoundWins=sum(r['slot']=='1'for r in wins),actualNativeDamageStores=len(damage),
  actualStages=[int(r['stage'])for r in stages],actualBoundary=boundary[0])

def run():
 need(not OUT.exists(),'Fresh immutable native encounter verdict')
 folder=capture.OUT;meta=json.loads((folder/'result.json').read_text())
 pins=json.loads((folder/'input_hashes_before.json').read_text())
 need(meta['passed']and meta['nativeExit']==0 and meta['candidate']==capture.native.NAME and
  meta['physicalSlot']==2 and meta['identity']==18 and meta['fighter']=='sonya'and meta['inputHashes']==pins and
  meta['executableSHA256']==capture.native.EXE_SHA and meta['guestSHA256']==capture.native.GUEST_SHA and
  meta['rawMediaGuestAudioFilesWritten']==meta['newBuilds']==0,'Actual terminal current diagnostic provenance')
 need(all(sha(p)==h for p,h in pins.items()),'All executed controller/compiled inputs intact')
 guest=capture.native.expected();proof=json.loads((folder/'guest_memory_proof.json').read_text())
 need(proof==dict(frame=1,bytes=1048576,sha256=hashlib.sha256(guest).hexdigest().upper(),
  executableSHA256=capture.native.EXE_SHA,payloadSHA256=capture.native.PAYLOAD_SHA,
  captureSourceSHA256=sha(capture.__file__),transportSourceSHA256=sha(ROOT/capture.LUA),
  everyActualByteComparedInRAM=True,guestDumpFilesWritten=0),'Actual every-byte independently reconstructed RAM guest and source provenance')
 need(capture.qualify_payload_metadata_warning((folder/'stderr.log').read_text(),proof)==
  meta['qualifiedTestCandidateMetadataWarning'],'Full source/payload/guest metadata and empty native stderr, no waiver')
 need(not any(p.suffix.lower()in('.png','.wav','.bin')for p in folder.rglob('*')if p.is_file()),
  'No raw buffers or automatic timed-boot PNG')
 process=json.loads((folder/'process.json').read_text());command=process['command']
 need(command[0]==str(ROOT/capture.native.NAME/'mkport_candidate.exe')and command[-1]==str(ROOT/capture.LUA)and
  '-nocheat'in command and command[command.index('-str')+1]=='900','Actual bounded comparison command, not duplicate full campaign')
 raw=gzip.open(folder/'run.log.gz','rb').read();text=raw.decode().replace('\r\n','\n')
 rows=original.parse(text);replay=make_replay();positive=replay(text);native=native_gate(text,guest)
 need(positive['actualNativeOwnRingTasks']>0,'Actual owned native Sonya Ring tasks, not command attempts alone')
 fields=[r for r in rows if r['tag']=='RANGE_FIELD'];f=fields[0];faults=[]
 attack=next(r for r in rows if r['tag']=='INPUT'and r['frame']in{r['frame']for r in fields}and r['button']=='Low_Punch')
 for tag,key,value in [('RANGE_FIELD','human_id',1),('RANGE_FIELD','cpu_id',1),
  ('RANGE_FIELD','human_owner','01000000'),('RANGE_FIELD','cpu_owner','01000000'),
  ('RANGE_FIELD','health','0,161'),('RANGE_FIELD','reset',1-int(f['reset'])),
  ('RANGE_DECISION','reason','fabricated'),('INPUT','button','High_Kick')]:
  frame=attack['frame']if tag=='INPUT'else f['frame'];damaged=original.change(text,tag,frame,key,value)
  need(damaged!=text,'Nonvacuous real input/state fault')
  try:replay(damaged)
  except ValueError as error:faults.append(dict(tag=tag,key=key,rejectedBy=str(error)))
  else:raise ValueError('Actual Ring input/state fault admitted '+key)
 win=next(r for r in rows if r['tag']=='WIN'and r['stage']=='2')
 for key,value in [('pc','FFF00000'),('id',1),('health','0,0')]:
  damaged=original.change(text,'WIN',win['frame'],key,value)
  try:native_gate(damaged,guest)
  except ValueError as error:faults.append(dict(tag='WIN',key=key,rejectedBy=str(error)))
  else:raise ValueError('Actual native winner fault admitted '+key)
 need(replay(text)==positive and native_gate(text,guest)==native,'Complete real input/native positive restored')
 prior=ROOT/'audit_v5633_current_sonya_p2_kitana_prefix_checked/report.json'
 baseline=json.loads(prior.read_text());need(baseline['passed'],'Whole original first physical Leg encounter proof retained')
 for p in[Path(__file__).resolve(),Path(original.__file__).resolve(),prior,*folder.rglob('*')]:
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All source/control/native evidence remains intact')
 return dict(passed=True,physicalSlot=2,trueIdentity=18,trueVictimID=4,native=native,
  actualFullRingSpacingReplay=positive,actualInputStateAndNativeWinnerFaultsRejected=faults,inputHashes=pins,
  priorCompletedLegEncounter=dict(proof=str(prior),actualLegTasks=baseline['actualCompletePhysicalReplay']['actualNativeLegActivations'],
   boundary=baseline['actualCompletedEncounterBoundary']),nativeLogBytes=len(raw),nativeLogSHA256=hashlib.sha256(raw).hexdigest().upper(),
  actualProbeEncounterOnly=True,fullTowerAccepted=False,fullEndingPixelsAccepted=False,completeAudioAccepted=False,fullPortAcceptance=False)

if __name__=='__main__':
 need((capture.OUT/'result.json').is_file(),'Await actual terminal, never restart on observation timeout')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable diagnostic result');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
