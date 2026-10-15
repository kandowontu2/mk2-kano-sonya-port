"""Add current natural campaign work without shrinking the full port goal."""
import gzip,hashlib,json,re,subprocess
from pathlib import Path
import native_subzero_legs_context_v4993 as native
import run_repaired_sonya_campaign_v5153 as capture
import verify_repaired_campaign_prefix_v5155 as checked

ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v5152_shadow_trace_storage_progress/progress.json'
OUT=ROOT/'audit_v5158_repaired_campaign_progress'

def main():
 need(not OUT.exists(),'Fresh immutable full-scope additive journal')
 parent=json.loads(PARENT.read_text());reportpath=checked.OUT/'report.json'
 proof=json.loads(reportpath.read_text())
 need(proof['passed']and proof['prefixProofOnly']and not proof['actualNaturalTowerClearAccepted']and
  proof['actualCampaignPrefix']['actualStages']==list(range(6))and len(proof['actualFaultsRejected'])==10,
  'Actual independent early ladder, exact physical/native checks and honest incomplete campaign')
 pins=dict(proof['inputHashes'])
 for p in[PARENT,reportpath,Path(__file__).resolve()]:pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every immutable source, guest proof and previous playable input unchanged')
 with gzip.open(capture.OUT/'run.log.gz','rb')as reader:
  raw=reader.read(proof['nativeLogUncompressedPrefixBytes'])
 need(len(raw)==proof['nativeLogUncompressedPrefixBytes']and hashlib.sha256(raw).hexdigest().upper()==
  proof['nativeLogUncompressedPrefixSHA256'],'Every qualified actual prefix byte retained in lossless growing gzip')
 command="Get-CimInstance Win32_Process -Filter \"Name='mkport_candidate.exe' OR Name='python.exe'\" | Where-Object { $_.ProcessId -eq 55420 -or $_.ProcessId -eq 137564 } | Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
 need(census.returncode==0,'Fresh authoritative exact native/collector process census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 resultpath=capture.OUT/'result.json'
 terminal=json.loads(resultpath.read_text())if resultpath.exists()else None
 if terminal is None:
  need(any(p['ProcessId']==55420 and str(capture.OUT)in p['CommandLine']and native.NAME in p['CommandLine']for p in live)and
   any(p['ProcessId']==137564 and 'run_repaired_sonya_campaign_v5153.py'in p['CommandLine']for p in live),
   'Pending only after both exact live native and collector commands confirmed')
 observed=[];last=None;prefixbytes=0;prefixhash=hashlib.sha256();cache=False
 with gzip.open(capture.OUT/'run.log.gz','rb')as reader:
  try:
   for line in reader:
    if not line.endswith(b'\n'):break
    prefixbytes+=len(line);prefixhash.update(line)
    if line.startswith(b'MK2_NAT_CAMPAIGN_'):
     row=dict(re.findall(r'(\w+)=([^\s]+)',line.decode()))
     last=row
     if re.match(rb'^MK2_NAT_CAMPAIGN_(STAGE|LOSS|WIN|ENDING_START|ENDING_COMPLETED|RESULT) ',line):
      observed.append(line.decode().rstrip())
    if line.startswith(b'MK2_MILEENA_CAMPAIGN_OVERRUN '):cache=True
  except EOFError:
   need(terminal is None,'Terminal gzip must be completely valid')
 statuses=dict(nativePID=55420,collectorPID=137564,execSession=84815,exactLiveProcesses=live,
  nativeTerminal=terminal is not None,nativeExit=terminal['nativeExit']if terminal else None,
  observedActualStages=[int(re.search(r' stage=(\d+)',line)[1])for line in observed if line.startswith('MK2_NAT_CAMPAIGN_STAGE ')],
  observedPaidLosses=sum(line.startswith('MK2_NAT_CAMPAIGN_LOSS ')for line in observed),
  observedOwnSubZeroRoundWins=sum(line.startswith('MK2_NAT_CAMPAIGN_WIN ')and ' slot=1 stage=7 id=18 'in line for line in observed),
  observedNativeCacheGlobalOverrun=cache,lastObservedNativeRow=last,
  completeObservedPrefixBytes=prefixbytes,completeObservedPrefixSHA256=prefixhash.hexdigest().upper(),
  growingLogNotPinnedAsTerminal=terminal is None,compressedLogBytes=(capture.OUT/'run.log.gz').stat().st_size,
  actualNaturalTowerClearAccepted=False)
 if terminal is not None:
  for p in capture.OUT.rglob('*'):
   if p.is_file():pins[str(p.resolve())]=sha(p)
 scope=parent['remaining'];need(len(scope)==5,'All five unchanged original scope groups retained')
 journal=dict(schema=1,parentAdditiveJournal=str(PARENT),mergeRule='Read with5152 and all its parent journals. Every original requirement and proof persists; bounded current campaign evidence is not all-context, ending, audio, artwork or release acceptance.',
  goalStatus='active',remaining=scope,newInputHashes=pins,
  previousGoalTurnClassification='no progress: acknowledgment of thanks did not perform goal work; revalidated5152, dirty checkout and absence of native jobs before taking the next safe action.',
  thisGoalTurnClassification='progress: inspected actual failed P1 campaign and repaired current candidate; launched one fresh current4992 cold P1 Sonya campaign with unchanged physical4807 policy and zero state assistance. Entire actual guest compared in RAM. Independently qualified source schedules, true selection/live IDs, native winner/advancement,6138Kitana and3234Jax physical fields, actual original Jax callbacks and10captured faults. Complete early campaign to stage5 accepted as prefix only; later actual observations and authoritative live/terminal status recorded separately. Complete textual trace is losslessly gzip-streamed instead of generating another large uncompressed folder.',
  independentlyAcceptedPrefix=dict(report=str(reportpath),actualStages=list(range(6)),
   actualOwnNativeRoundWins=13,actualOwnedNativeSpecialEntries=180,
   actualKitanaFields=6138,actualJaxFields=3234,actualFaultsRejected=10,
   originalNativeJaxCallbacks=proof['actualJaxNativeCallbacks'],prefixOnly=True),
  currentNativeCampaign=statuses,publicPlayableChanged=False,newBuilds=0,newlyDeletedFiles=0,
  rawGuestMediaAudioFilesWritten=0,fullPortAcceptance=False,finishedRelease=False,
  nextAction='Poll the same exec84815 and exact native55420/collector137564 while their actual commands are live; do not restart due repeated losses or an observation timeout. Consume terminal before full campaign qualification. Read run.log.gz losslessly, not an old run.log/guest fixture. Distinguish real own Sub-Zero wins/losses/continues from port failures; preserve actual failed contexts. If host5900 deadline leaves campaign incomplete, use its actual action/damage chronology to improve only ordinary physical controls, not native AI, RNG, health or identities, unless a real native bug is demonstrated. Continue genuine later opponents, Kintaro/ShaoKahn, own endings and attract. All five original broader finisher/stage/art/grounding/shadow/audio/selection/ladder/cleanup/release groups stay open.',
  storage='Fresh complete log uses streaming gzip; no full build tree, executable, ROM, guest, RGB, PCM or raw snapshot copies. Previous32.49GiB and61.46MiB reclamation not recounted.')
 need(all(sha(p)==h for p,h in pins.items()),'All final immutable pins retained; growing log excluded')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(journal,indent=2)+'\n')
 print(json.dumps(dict(journal=str(OUT/'progress.json'),independentEarlyCampaignPrefixPassed=True,
  actualCurrentCampaign=statuses,goalStatus='active',fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
