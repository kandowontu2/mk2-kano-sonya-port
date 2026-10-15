"""Add full actual campaign failure/progress; retain all five original groups."""
import ast,gzip,hashlib,json,re,subprocess
from pathlib import Path
import native_subzero_legs_context_v4993 as native
import run_freeze_guard_sonya_campaign_v5160 as capture
import run_crouch_prime_sonya_campaign_v5175 as prepared
import verify_freeze_guard_prefix_v5172 as prefix

ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v5158_repaired_campaign_progress/progress.json'
OUT=ROOT/'audit_v5178_campaign_guard_progress'

def main():
 need(not OUT.exists(),'Fresh immutable whole-goal additive journal')
 parent=json.loads(PARENT.read_text())
 fullpath=ROOT/'audit_v5171_repaired_campaign_terminal_checked/report.json'
 full=json.loads(fullpath.read_text());prefixpath=prefix.OUT/'report.json';proof=json.loads(prefixpath.read_text())
 need(full['passed']and full['nativeExit']==0 and full['originalCollectorFailurePreserved']and
  not full['actualNaturalTowerClearAccepted']and full['actualFinalNativeResult']['frame']==322771 and
  full['actualBoundedNativeCampaign']['actualPaidLosses']==89 and full['actualOwnSubZeroRoundWins']==9 and
  full['exactCompiledMetadataWarning']['releaseMetadataCorrectionStillRequired'],
  'Actual bounded terminal and metadata-only collector rejection, no supplied tower victory')
 need(proof['passed']and proof['prefixProofOnly']and proof['actualPhysicalReplay']['actualCompleteGuardFields']==2277 and
  proof['actualPhysicalReplay']['actualNativeLegActivations']==6 and len(proof['actualRecordFaultsRejected'])==7,
  'Real full first Sub-Zero controls and native action/leg entries, not a hypothetical test')
 pins={}
 for report in(full,proof):
  for p,h in report['inputHashes'].items():
   need(p not in pins or pins[p]==h,'All inherited actual executed pins consistent');pins[p]=h
 for p in[PARENT,fullpath,prefixpath,Path(__file__),ROOT/'tools/verify_repaired_campaign_terminal_v5162.py',
  ROOT/'audit_v5163_repaired_campaign_terminal_checked/report.json',
  ROOT/'tools/verify_repaired_campaign_terminal_v5164.py',ROOT/'tools/verify_repaired_campaign_terminal_v5168.py',
  ROOT/'mk2ks_sonya_p1_subzero_crouch_prime_ram_v5174.lua',Path(prepared.__file__),
  ROOT/'tools/verify_crouch_prime_prefix_v5179.py',ROOT/'audit_v5092_move_phase_shadow_progress/progress.json']:
  pins[str(p.resolve())]=sha(p)
 failed_syntax=[]
 for name in('verify_repaired_campaign_terminal_v5164.py','verify_repaired_campaign_terminal_v5168.py'):
  p=ROOT/'tools'/name
  try:ast.parse(p.read_text())
  except SyntaxError as error:failed_syntax.append(dict(source=str(p),error=str(error),failurePreserved=True))
  else:raise ValueError('Executed original malformed correction changed')
 ast.parse(Path(prepared.__file__).read_text())
 future=ROOT/'tools/verify_crouch_prime_prefix_v5179.py';ast.parse(future.read_text())
 with gzip.open(capture.OUT/'run.log.gz','rb')as reader:raw=reader.read(proof['nativeLogPrefixBytes'])
 need(len(raw)==proof['nativeLogPrefixBytes']and hashlib.sha256(raw).hexdigest().upper()==proof['nativeLogPrefixSHA256'],
  'Every independent qualified current first encounter byte retained in compressed log')
 # Compare the unchanged pre-Sub portion across the two actual cold boots.
 early=json.loads((ROOT/'audit_v5156_repaired_sonya_campaign_prefix_checked/report.json').read_text())
 with gzip.open(capture.OUT/'run.log.gz','rb')as reader:before=reader.read(early['nativeLogUncompressedPrefixBytes'])
 need(hashlib.sha256(before).hexdigest().upper()==early['nativeLogUncompressedPrefixSHA256'],
  'Entire actual first0..5 selection/wins/Kitana/Jax/RGB chronology unchanged by new Sub controls')
 command="Get-CimInstance Win32_Process -Filter \"Name='mkport_candidate.exe' OR Name='python.exe'\" | Where-Object { $_.ProcessId -eq 135928 -or $_.ProcessId -eq 132248 } | Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
 need(census.returncode==0,'Fresh authoritative exact native/collector process census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 resultpath=capture.OUT/'result.json';terminal=json.loads(resultpath.read_text())if resultpath.exists()else None
 if terminal is None:
  need(any(r['ProcessId']==135928 and str(capture.OUT)in r['CommandLine']for r in live)and
   any(r['ProcessId']==132248 and 'run_freeze_guard_sonya_campaign_v5160.py'in r['CommandLine']for r in live),
   'Pending only with both specific currently live native and collector commands')
 if terminal:
  for p in capture.OUT.rglob('*'):
   if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every original failure, source, native and qualified evidence byte unchanged')
 report=dict(schema=1,parentAdditiveJournal=str(PARENT),mergeRule='Read with5158 and all previous whole-goal journals. Every original requirement, proof and exclusion persists. Actual test deadline, selected art scenes and guard-input replay are not campaign/ending/all-arena/audio/full-port acceptance.',
  goalStatus='active',remaining=parent['remaining'],newInputHashes=pins,
  previousGoalTurnClassification='progress: real current cold campaign launched, whole guest qualified and complete early native/physical prefix verified; growing replay compressed and exact live jobs recorded.',
  thisGoalTurnClassification='progress: consumed same84815real native0terminal at322771frames/5900s. All actual native identities/schedules/winners/specials and zero cache global writes accepted as bounded observation:30own round wins,1196owned specials,89paid losses,9own Sub-Zero round wins, no clear. Collector failure preserved and exact compiled stale metadata versus fully qualified payload/guest diagnosed.5162CRLF parser rejection and5164/5168host-syntax failures preserved;5170narrow corrected checker passes. Fresh current5160normal freeze guard runs without game-state changes; actual first2277Sub fields,6leg tasks and7faults independently accepted. Entire original0..5cold prefix byte-identical. Older basic-move evidence explains anti-air HP failures as simultaneous Down/HP; fresh normal crouch-prime controller/host/independent actual HUMAN107 qualifier prepared, not yet credited as activated.',
  actualPreviousNativeTerminal=dict(execSession=84815,execTerminalConsumed=True,nativeExit=0,frames=322771,
   fullBoundedProof=str(fullpath),collectorFailurePreserved=True,nativeCacheGlobalStores=0,ownSubZeroRoundWins=9,
   paidLosses=89,nativeOwnedSpecialEntries=1196,naturalTowerClearAccepted=False),
  actualFreezeGuardPrefix=dict(report=str(prefixpath),actualFields=2277,actualLegEntries=6,actualOwnSubZeroRoundWins=0,
   actualNativeHumanUppercut107Stores=0,actualFaultsRejected=7,prefixOnly=True),
  originalEarlyColdPrefixByteIdentical=True,knownCandidateMetadataReleaseDefect=full['exactCompiledMetadataWarning'],
  preservedCheckerSyntaxFailures=failed_syntax,
  currentCampaign=dict(execSession=14420,nativePID=135928,collectorPID=132248,exactLiveProcesses=live,
   nativeTerminal=terminal is not None,nativeExit=terminal['nativeExit']if terminal else None,
   actualTerminalReport=str(resultpath)if terminal else None,compressedTraceBytes=(capture.OUT/'run.log.gz').stat().st_size,
   actualNaturalTowerClearAccepted=False,growingLogNotPinnedAsTerminal=terminal is None),
  preparedNextPhysicalCorrection=dict(lua='mk2ks_sonya_p1_subzero_crouch_prime_ram_v5174.lua',
   host='tools/run_crouch_prime_sonya_campaign_v5175.py',checker='tools/verify_crouch_prime_prefix_v5179.py',
   actualNextNativeBootPerformed=False,actualNewUppercut107Accepted=False,
   basis='Current5092real basic-move matrix: simultaneous Down/HP rejects during crouch transition; Down9fields/HP6..8 activates native uppercut.'),
  publicPlayableChanged=False,newBuilds=0,newlyDeletedFiles=0,rawGuestMediaAudioFilesWritten=0,
  fullPortAcceptance=False,finishedRelease=False,
  nextAction='Poll same14420/exact135928and132248 while commands remain live, never restart on loss/timeout. Only after consuming actual native terminal inspect complete5161run.log.gz/result/errors, preserving any failure. It is not a clear unless actual later native wins, bosses, own ending and300attract all occur. Then launch unused5175/5176normal crouch-prime controller if needed; no nativeAI/health/RNG/state changes. Run prepared5179only once actual completed first Sub encounter exists, requiring actual original HUMAN107 stores rather than crediting intended HP. Continue all five broader Pit/Tomb/victim/finisher/art/grounding/shadow/arena/audio/morph/secret/cinematic/selection/ladder/name/cleanup/refreshed-release groups. Correct exact compiled payload CRC/SHA metadata before final production release; narrowed test warning allowance is not final acceptance.',
  storage='Lossless streaming gzip both captures, no full build trees/native binaries/raw media copies. Old32.49GiB and61.46MiB reclamation not recounted.')
 need(len(report['remaining'])==5,'All five original whole objective groups stay open')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(journal=str(OUT/'progress.json'),oldNativeTerminalAcceptedAsIncomplete=True,
  firstRealFreezeGuardEncounterAccepted=True,currentCampaign=report['currentCampaign'],
  preparedCrouchPrimeUnexecuted=True,goalStatus='active',fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
