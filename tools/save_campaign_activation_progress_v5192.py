"""Preserve whole objective; add natural13stage terminal and actual CPU107."""
import gzip,hashlib,json,re,subprocess
from pathlib import Path
import native_subzero_legs_context_v4993 as native
import run_tested_prime_sonya_campaign_v5186 as current
import verify_tested_prime_prefix_v5188 as checked

ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v5184_tested_prime_progress/progress.json'
OUT=ROOT/'audit_v5193_campaign_activation_progress'

def main():
 need(not OUT.exists(),'Fresh immutable full-goal journal')
 parent=json.loads(PARENT.read_text())
 fullpath=ROOT/'audit_v5191_crouch_prime_terminal_checked/report.json';full=json.loads(fullpath.read_text())
 prefixpath=checked.OUT/'report.json';proof=json.loads(prefixpath.read_text())
 need(full['passed']and full['nativeExit']==0 and full['actualWholeBoundedNativeCampaign']['actualStages']==list(range(13))and
  full['actualWholeSubZeroPhysicalReplay']['actualCompleteGuardFields']==118604 and
  full['actualWholeSubZeroPhysicalReplay']['actualNativeHumanUppercut107Stores']==0 and
  full['originalFirstPrefixMissing107FailurePreserved']and not full['actualNaturalTowerClearAccepted'],
  'Actual complete first prime naturally clears Sub-Zero and reaches stage12, but not bosses/ending/107')
 need(proof['passed']and proof['prefixProofOnly']and proof['actualPhysicalReplay']['actualCompleteGuardFields']==2394 and
  proof['actualPhysicalReplay']['actualNativeHumanUppercut107Stores']==1 and
  proof['actualPhysicalReplay']['actualNativeLegActivations']==5 and len(proof['actualRecordFaultsRejected'])==7,
  'Actual exact-tested physical first CPU encounter, native original107 and5leg entries, not intended commands')
 pins={}
 for report in(full,proof):
  for p,h in report['inputHashes'].items():
   need(p not in pins or pins[p]==h,'All old/new actual native/control source pins agree');pins[p]=h
 for p in[PARENT,fullpath,prefixpath,Path(__file__)]:pins[str(p.resolve())]=sha(p)
 with gzip.open(current.OUT/'run.log.gz','rb')as reader:raw=reader.read(proof['nativeLogPrefixBytes'])
 need(len(raw)==proof['nativeLogPrefixBytes']and hashlib.sha256(raw).hexdigest().upper()==proof['nativeLogPrefixSHA256'],
  'Entire independently qualified actual first encounter retained byte-for-byte')
 witnesses=[]
 for line in raw.decode().splitlines():
  if line.startswith('MK2_NAT_CAMPAIGN_SUBZERO_ACTION ')and ' after=263 'in line:
   r=dict(re.findall(r'(\w+)=([^\s]+)',line));need(r['pc']=='FF83C340'and r['a1']=='00000107'and
    r['actor']==r['owner']==r['a8']and r['main']==r['a13']and r['id']==r['roster']=='18',
    'Actual original HUMAN107 exact setter operand/instruction/true owner')
   witnesses.append(line)
 need(len(witnesses)==1,'One actually executed first encounter HUMAN107 witness')
 command="Get-CimInstance Win32_Process -Filter \"Name='mkport_candidate.exe' OR Name='python.exe'\" | Where-Object { $_.ProcessId -eq 111724 -or $_.ProcessId -eq 134820 } | Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
 need(census.returncode==0,'Fresh exact native/collector census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 resultpath=current.OUT/'result.json';terminal=json.loads(resultpath.read_text())if resultpath.exists()else None
 if terminal is None:
  need(any(r['ProcessId']==111724 and str(current.OUT)in r['CommandLine']for r in live)and
   any(r['ProcessId']==134820 and 'run_tested_prime_sonya_campaign_v5186.py'in r['CommandLine']for r in live),
   'Pending only with both actual currently live exact commands')
 if terminal:
  for p in current.OUT.rglob('*'):
   if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All immutable sources/failed-first-encounter/full terminal/current proof bytes retained')
 report=dict(schema=1,parentAdditiveJournal=str(PARENT),mergeRule='Read with5184and all preceding whole-goal journals. Every original requirement/evidence/exclusion persists. Natural stage12and CPU107activation are progress, not complete tower/boss/ending/all-arena/art/audio/port/release acceptance.',
  goalStatus='active',remaining=parent['remaining'],newInputHashes=pins,
  previousGoalTurnClassification='progress: complete guarded native terminal and source/physical checks accepted; actual first six-field crouch prime rejected, its native transition chronology preserved, exact executed5081Down24/HP10timing reconstructed and prepared.',
  thisGoalTurnClassification='progress: consumed same54519native0terminal at322771frames; Sonya actually beat Sub-Zero and progressed naturally through stage12. Whole native true IDs/schedules/winners/specials and118604Sub physical fields/287native legs/zero107/zero cache-global writes independently checked, preserving failed first encounter. Actual current5186cold boot uses exact tested ordinary Down24/HP10..12, not game-state assistance. Entire actual initialized guest compared in RAM. Strict5188first encounter qualifier now accepts2394real fields,5nativeleg entries and one original owned HUMAN107store,7actual corrupted-record faults; no loss is changed to a win. Exact live/terminal current status below; all original groups remain.',
  actualPreviousPrimeTerminal=dict(report=str(fullpath),execSession=54519,execTerminalConsumed=True,nativeExit=0,
   frames=322771,actualStages=list(range(13)),actualOwnRoundWins=41,actualNativeOwnedSpecialEntries=917,
   subZeroFields=118604,nativeSubZeroLegEntries=287,nativeHuman107Stores=0,actualOwnSubZeroRoundWins=9,
   nativeCacheGlobalStores=0,paidLosses=71,actualNaturalTowerClearAccepted=False),
  actualExactTestedCPUActivation=dict(report=str(prefixpath),ordinaryPhysicalTiming='Down0..23,HP10..12',
   actualFirstEncounterFields=2394,actualNativeLegEntries=5,actualOriginalHuman107Stores=1,
   actualHuman107Witnesses=witnesses,actualOwnSubZeroRoundWins=0,actualFaultsRejected=7,prefixOnly=True),
  currentCampaign=dict(execSession=3931,nativePID=111724,collectorPID=134820,exactLiveProcesses=live,
   nativeTerminal=terminal is not None,nativeExit=terminal['nativeExit']if terminal else None,
   actualTerminalReport=str(resultpath)if terminal else None,compressedTraceBytes=(current.OUT/'run.log.gz').stat().st_size,
   growingLogNotPinnedAsTerminal=terminal is None,actualNaturalTowerClearAccepted=False),
  knownCandidateMetadataReleaseDefect=full['exactCompiledMetadataWarning'],
  publicPlayableChanged=False,newBuilds=0,newlyDeletedFiles=0,rawGuestMediaAudioFilesWritten=0,
  fullPortAcceptance=False,finishedRelease=False,
  nextAction='Poll same3931and exact111724/134820while actual commands are live; consume actual native terminal, never restart solely for loss/timeout. Read full5187run.log.gz and result; use whole native/physical source grammar with exact tested26fielduppercut sequence/HP10..12, not old5179six-field replay. Actual5189is a first encounter and one original107activation, not a natural win/boss/ending. Previous5176full stage0..12accepted in5191; cannot substitute it for current complete campaign. Continue actual Kintaro/ShaoKahn/own endings/300attract and all other five-group broader Pit/Tomb/victim/finisher/art/grounding/shadow/arena/audio/morph/secret/cinematic/selection/ladder/names/cleanup/refreshed-release work. Correct exact stale compiled payload ROM metadata before final production release. No nativeAI/health/RNG/state assistance.',
  storage='All new chronicles losslessly gzip-streamed; no native binaries/ROM/full build tree/raw guest/RGB/PCM copies. Previous32.49GiB/61.46MiBreclamation not recounted.')
 need(len(report['remaining'])==5,'All five original unfinished groups preserved verbatim')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(journal=str(OUT/'progress.json'),actualNaturalStagesPreviouslyAccepted=13,
  actualFirstCPUHuman107Accepted=True,currentCampaign=report['currentCampaign'],
  goalStatus='active',fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
