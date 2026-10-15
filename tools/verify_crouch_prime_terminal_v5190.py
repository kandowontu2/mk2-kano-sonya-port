"""Whole actual5161 native/physical bounded campaign, explicitly no clear."""
import gzip,hashlib,inspect,json,re,traceback
from pathlib import Path
import native_subzero_legs_context_v4993 as native
import run_crouch_prime_sonya_campaign_v5175 as capture
import verify_crouch_prime_prefix_v5179 as prefix
import verify_repaired_campaign_prefix_v5155 as early

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v5191_crouch_prime_terminal_checked'

def run():
 need(not OUT.exists(),'Fresh immutable whole current terminal qualifier')
 result=json.loads((capture.OUT/'result.json').read_text())
 need(result['passed']and result['nativeExit']==0 and result['actualStages']==list(range(13))and
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
 code=inspect.getsource(early.campaign_prefix)
 before='stages==list(range(6))and own>=10 and specials>0';need(code.count(before)==1,'Exact complete native grammar scope extension')
 code=code.replace(before,'stages==list(range(13))and own>=24 and specials>0',1)
 scope=dict(vars(early));exec(compile(code,__file__+'::actual_whole_native_scope0to7','exec'),scope)
 campaign=scope['campaign_prefix'](text,guest)
 physical=prefix.make_replay()(text)
 need(physical['actualCompleteGuardFields']>2277 and physical['actualNativeLegActivations']>6,
  'Complete repeated real Sub-Zero encounters beyond independently qualified first prefix')
 prefixpath=prefix.OUT/'report.json';first=json.loads(prefixpath.read_text())
 need(not first['passed']and 'Actual original HUMAN107 uppercut store must execute'in first['error'],
  'Actual strict first-encounter missing107rejection retained, not silently converted to success')
 firsttext=prefix.completed_prefix();firstphysical=prefix.make_replay()(firsttext)
 need(firstphysical['actualNativeHumanUppercut107Stores']==0 and raw.startswith(firsttext.encode()),
  'Actual complete first failed native encounter remains byte-identical in whole terminal')
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
  actualWholeSubZeroPhysicalReplay=physical,actualKitanaReplay=kitana,actualJaxReplay=jax,actualJaxNativeCallbacks=callbacks,
  actualFinalNativeResult=final,actualOwnSubZeroRoundWins=len(subwins),actualNativeCacheGlobalStores=0,
  originalFirstPrefixMissing107FailurePreserved=True,actualFirstEncounterPhysicalReplay=firstphysical,exactCompiledMetadataWarning=metadata,
  completeUncompressedNativeLogBytes=len(raw),completeUncompressedNativeLogSHA256=hashlib.sha256(raw).hexdigest().upper(),
  inputHashes=pins,actualNaturalTowerClearAccepted=False,deadlineIsNotClear=True,
  fullEndingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullArtAcceptance=False,fullPortAcceptance=False,
  nextAction='Actual whole native anti-air107 stores below remain distinct from the failed first encounter. Native own wins progressed beyond Sub-Zero to stage12; no bosses or ending clear. Continue fresh5186exact-tested timing and5188actual activation; all five scope groups remain.')

if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable actual result');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualJaxNativeCallbacks')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)

