"""Actual completed first P2 Kitana encounter; not whole tower acceptance.

Entire independent4194 Kitana state/ownership/reset/decision/input/action replay
retained with slot2 provenance. Growing log is bounded at the real first loss.
"""
import gzip,hashlib,json,sys,traceback
from pathlib import Path
import verify_current_sonya_p2_campaign_v5630 as whole
ROOT,need,sha=whole.ROOT,whole.need,whole.sha
OUT=ROOT/'audit_v5633_current_sonya_p2_kitana_prefix_checked'

def run():
 need(not OUT.exists(),'Fresh actual completed encounter proof')
 capture=whole.capture;seen=False;lines=[];count=0
 with gzip.open(capture.OUT/'run.log.gz','rt',encoding='utf-8',newline='')as reader:
  for line in reader:
   need(line.endswith('\n'),'Only complete native rows')
   count+=len(line.encode());need(count<=128*1024*1024,'Bounded completed actual encounter')
   lines.append(line)
   if line.startswith('MK2_NAT_CAMPAIGN_KITANA_FIELD '):seen=True
   if seen and ((line.startswith('MK2_NAT_CAMPAIGN_LOSS ')and ' stage=2'in line)or
    (line.startswith('MK2_NAT_CAMPAIGN_STAGE ')and ' stage=3 'in line)):break
  else:raise ValueError('Await actual complete Kitana encounter, never restart live native job')
 text=''.join(lines);module=whole.original.supplemental.kitana
 replay=whole.p2_factory(module.make_replay,module)();positive=replay(text)
 rows=module.original.parse(text);fields=[r for r in rows if r['tag']=='KITANA_FIELD']
 decisions=[r for r in rows if r['tag']=='KITANA_DECISION']
 need(fields and [r['frame']for r in fields]==[r['frame']for r in decisions],
  'Exactly one actual state and physical decision per native Kitana field')
 pins=json.loads((capture.OUT/'input_hashes_before.json').read_text())
 need(all(sha(p)==h for p,h in pins.items()),'All actually executed current compiled/controller inputs intact')
 proof=json.loads((capture.OUT/'guest_memory_proof.json').read_text())
 guest=capture.native.expected()
 need(proof==dict(frame=1,bytes=1048576,sha256=hashlib.sha256(guest).hexdigest().upper(),
  executableSHA256=capture.native.EXE_SHA,payloadSHA256=capture.native.PAYLOAD_SHA,
  captureSourceSHA256=sha(capture.__file__),transportSourceSHA256=sha(ROOT/capture.LUA),
  everyActualByteComparedInRAM=True,guestDumpFilesWritten=0)and proof['sha256']==capture.native.GUEST_SHA,
  'Actual independently reconstructed every-byte current guest and exact capture/Lua provenance')
 capture.source_boundary();f=fields[0];faults=[]
 attack=next(r for r in rows if r['tag']=='INPUT'and r['frame']in{r['frame']for r in fields}and r['button']=='Low_Punch')
 for tag,key,value in [('KITANA_FIELD','human_id',1),('KITANA_FIELD','cpu_id',1),
  ('KITANA_FIELD','human_owner','01000000'),('KITANA_FIELD','cpu_owner','01000000'),
  ('KITANA_FIELD','health','0,161'),('KITANA_FIELD','reset',1-int(f['reset'])),
  ('KITANA_DECISION','reason','fabricated'),('INPUT','button','High_Kick')]:
  frame=attack['frame']if tag=='INPUT'else f['frame']
  damaged=module.original.change(text,tag,frame,key,value)
  need(damaged!=text,'Nonvacuous captured P2 input/state fault')
  try:replay(damaged)
  except ValueError as error:faults.append(dict(tag=tag,key=key,rejectedBy=str(error)))
  else:raise ValueError('Actual P2 Kitana physical fault admitted '+key)
 need(replay(text)==positive,'Full actual physical positive restored')
 for p in[Path(__file__).resolve(),Path(whole.__file__).resolve(),capture.OUT/'guest_memory_proof.json',
           capture.OUT/'input_hashes_before.json',capture.OUT/'process.json']:
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every immutable source/input/proof byte remains intact')
 need('MK2_MILEENA_CAMPAIGN_OVERRUN 'not in text,'No original cache global overwrite in completed encounter')
 return dict(passed=True,physicalSlot=2,humanIdentity=18,cpuIdentity=4,actualCompletePhysicalReplay=positive,
  actualRecordFaultsRejected=faults,inputHashes=pins,actualCompletedEncounterBoundary=lines[-1].strip(),
  actualNativePrefixBytes=len(text.encode()),actualNativePrefixSHA256=hashlib.sha256(text.encode()).hexdigest().upper(),
  growingLogPinnedAsTerminal=False,actualNativeInitializedGuestBytesComparedInRAM=1048576,
  fullTowerAccepted=False,fullEndingPixelsAccepted=False,fullAudioAccepted=False,fullPortAcceptance=False)

if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable real encounter proof');OUT.mkdir()
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
