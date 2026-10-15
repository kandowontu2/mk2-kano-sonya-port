"""Preserve5154 failure; independently qualify actual bounded native terminal.

The collector's checksum predicate failed on exact stale compiled metadata.
This qualifier checks that warning narrowly and does not turn a host deadline
or89paid losses into a campaign clear. Full native/callback chronology retained.
"""
import gzip,hashlib,inspect,json,re,traceback
from pathlib import Path
import native_subzero_legs_context_v4993 as native
import run_repaired_sonya_campaign_v5153 as capture
import run_freeze_guard_sonya_campaign_v5160 as next_capture
import verify_repaired_campaign_prefix_v5155 as early

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v5163_repaired_campaign_terminal_checked'

def run():
 need(not OUT.exists(),'Fresh immutable actual terminal qualifier')
 folder=capture.OUT;resultpath=folder/'result.json';failedpath=folder/'capture_failure.json'
 result=json.loads(resultpath.read_text());failed=json.loads(failedpath.read_text())
 need(not result['passed']and result['nativeExit']==0 and not result['actualNaturalTowerClearAccepted']and
  'Actual terminal current4992 transport and native callbacks'in failed['error'],
  'Actual collector failure preserved, not overwritten or silently relabeled')
 pins=dict(result['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'All actual executed immutable inputs retained')
 with gzip.open(folder/'run.log.gz','rb')as reader:raw=reader.read()
 text=raw.decode();guest=native.expected();proof=json.loads((folder/'guest_memory_proof.json').read_text())
 need(proof['bytes']==1048576 and proof['everyActualByteComparedInRAM']and proof['guestDumpFilesWritten']==0 and
  proof['sha256']==native.GUEST_SHA==hashlib.sha256(guest).hexdigest().upper()and
  proof['captureSourceSHA256']==sha(capture.__file__)and proof['transportSourceSHA256']==sha(ROOT/capture.LUA),
  'Actual whole guest byte comparison and exact source provenance')
 warning=next_capture.qualify_payload_metadata_warning((folder/'stderr.log').read_text(),proof)
 need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',text,re.I),
  'Actual terminal callbacks have no Lua/native errors')
 # Same complete source-derived selection/schedule/winner/special algorithm;
 # only its bounded completed-stage expectation extends from0..5 to0..7.
 code=inspect.getsource(early.campaign_prefix)
 before="stages==list(range(6))and own>=10 and specials>0"
 need(code.count(before)==1,'Exact independent unchanged early native grammar')
 code=code.replace(before,"stages==list(range(8))and own>=14 and specials>0",1)
 scope=dict(vars(early));exec(compile(code,__file__+'::whole_native_early_grammar_through_actual_stage7','exec'),scope)
 actual=scope['campaign_prefix'](text,guest)
 rows=early.kitana.original.parse(text)
 final=[r for r in rows if r['tag']=='RESULT'];need(len(final)==1,'One actual terminal native result')
 final=final[0]
 need(final['frame']==322771 and final['selections']=='90'and final['losses']=='89'and
  final['seen_stages']=='8'and final['ending']==final['ending_completed']=='-1'and
  final['pictures']==final['texts']=='0,0','Actual incomplete native deadline result, never a tower clear')
 deadline=re.findall(r'^MK2_CAMPAIGN_HOST_DEADLINE seconds=([\d.]+) limit=(\d+) assistance=none writes=0$',text,re.M)
 need(len(deadline)==1 and deadline[0][1]=='5900'and 5900<=float(deadline[0][0])<5900.03,
  'Actual finite host deadline observed; no supplied ending/victory')
 cache=[line for line in text.splitlines()if line.startswith('MK2_MILEENA_CAMPAIGN_RESULT ')]
 need(len(cache)==1 and 'global_cache_stores=0'in cache[0]and
  not any(line.startswith('MK2_MILEENA_CAMPAIGN_OVERRUN ')for line in text.splitlines()),
  'Original cache monitor retained through native terminal, zero actual global writes')
 priorpath=early.OUT/'report.json';prior=json.loads(priorpath.read_text())
 need(prior['passed']and hashlib.sha256(raw[:prior['nativeLogUncompressedPrefixBytes']]).hexdigest().upper()==
  prior['nativeLogUncompressedPrefixSHA256'],'Qualified complete early Kitana/Jax replay retained byte-for-byte')
 subwins=[r for r in rows if r['tag']=='WIN'and r['stage']=='7'and r['slot']=='1']
 faults=[]
 for label,tag,key,value in(('wrong_late_human','LIVE','human','1:1'),
  ('wrong_late_winner_pc','WIN','pc','FFF00000')):
  row=next(r for r in rows if r['tag']==tag and r.get('stage')=='7')
  damaged=early.kitana.original.change(text,tag,row['frame'],key,value)
  try:scope['campaign_prefix'](damaged,guest)
  except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Actual late native record fault admitted '+label)
 need(scope['campaign_prefix'](text,guest)==actual,'Actual entire bounded native terminal positive restored')
 scenes=result['actualScenes'];need(len(scenes)==result['actualNativeRGBFrameCallbacks']==371 and
  all(r['width']=='400'and r['height']=='254'and r['bytes']=='406400'for r in scenes),
  'All371actual full RGB field digests retained, not an art-fidelity claim')
 for p in[Path(__file__),Path(early.__file__),Path(next_capture.__file__),priorpath,*folder.rglob('*')]:
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every original source/failure/full terminal byte unchanged')
 return dict(passed=True,nativeExit=0,originalCollectorFailurePreserved=True,
  exactCompiledMetadataWarning=warning,actualBoundedNativeCampaign=actual,
  actualFinalNativeResult=final,actualOwnSubZeroRoundWins=len(subwins),actualOwnSubZeroWins=subwins,
  actualNativeRGBFieldDigests=371,actualFaultsRejected=faults,
  originalEarlyPrefixFaultsRetained=len(prior['actualFaultsRejected']),inputHashes=pins,
  completeUncompressedNativeLogBytes=len(raw),completeUncompressedNativeLogSHA256=hashlib.sha256(raw).hexdigest().upper(),
  actualNaturalTowerClearAccepted=False,deadlineIsNotClear=True,fullEndingPixelsAccepted=False,
  completeCampaignAudioAccepted=False,fullArtAcceptance=False,fullPortAcceptance=False,
  nextAction='Use fresh physical-only freeze guard5159/host5160; preserve89losses and no clear. Correct exact stale payload ROM metadata for a later production build, not a generic checksum waiver.')

if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable evidence');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualOwnSubZeroWins')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
