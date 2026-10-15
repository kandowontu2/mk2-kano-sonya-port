"""Additive whole-goal checkpoint: both corrected-build P1 clears, live full video."""
import ast,inspect,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import run_p1_ending_pixels_v5247 as video
import run_p1_ending_pixels_v5243 as unbound
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5228_campaign_and_metadata_progress/progress.json'
OUT=ROOT/'audit_v5252_corrected_campaign_and_p1_ending_progress'

def main():
 need(not OUT.exists(),'Fresh immutable whole-goal additive journal')
 parent=json.loads(PARENT.read_text())
 need(len(parent['remaining'])==5 and all(sha(p)==h for p,h in parent['inputHashes'].items()),
  'All five original unfinished groups and complete source/evidence chain retained')
 pins={str(PARENT):sha(PARENT),str(Path(__file__).resolve()):sha(__file__)}
 campaigns=[]
 for fighter in ('kano','sonya'):
  path=ROOT/f'audit_v5235_{fighter}_corrected_p1_campaign_checked/report.json'
  proof=json.loads(path.read_text())
  need(proof['passed']and proof['actualCorrectedExecutableNaturalTowerOwnEndingAttractAccepted']and
   proof['entirePriorFaultQualifiedNativeChronologyByteIdentical']and proof['physicalSlot']==1 and
   proof['candidate']==current.NAME and proof['executableSHA256']==current.EXE_SHA and
   proof['case']['unassisted_clear_proven']and proof['case']['stages_reached']==list(range(13))+[14,15,16]and
   all(sha(p)==h for p,h in proof['inputHashes'].items()),'Actual new executable full natural own campaign '+fighter)
  pins[str(path)]=sha(path)
  campaigns.append(dict(fighter=fighter,report=str(path),actualNaturalBossesOwnEndingAttractAccepted=True,
   ownRoundWins=proof['case']['native_own_round_wins'],nativeOwnedSpecialEntries=proof['case']['native_owned_special_entries'],
   completeNativeChronologyBytes=proof['completeNativeChronologyBytes'],
   nativeChronologySHA256=proof['completeNativeChronologySHA256'],
   onlyExcludedHostPerformanceTrailer=proof['onlyExcludedHostTrailer'],
   completeNativeEndingPixelsAccepted=False,completeAudioAccepted=False))
 sourcepath=ROOT/'audit_v5249_p1_ending_source_checked/report.json'
 source=json.loads(sourcepath.read_text())
 need(source['passed']and source['sourceOnly']and len(source['sourceFaultsRejected'])==11 and
  source['originalCompleteRendererAndPhysicalPoliciesRetained']and
  all(sha(p)==h for p,h in source['inputHashes'].items()),'Entire original full source/model + explicit P1 map preflight')
 pins[str(sourcepath)]=sha(sourcepath)
 command='Get-CimInstance Win32_Process -Filter "ProcessId=84724 OR ProcessId=140956 OR ProcessId=138968 OR ProcessId=142528" | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress'
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
 need(census.returncode==0,'Fresh exact live native/collector process census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 running=[]
 for fighter,hostpid,nativepid,session in [('kano',138968,84724,41152),('sonya',142528,140956,87441)]:
  folder=ROOT/f'audit_v5250_{fighter}_current_p1_ending_pixels'
  executed=json.loads((folder/'process.json').read_text())
  guest=json.loads((folder/'guest_memory_proof.json').read_text())
  terminal=ROOT/f'audit_v5250_{fighter}_current_p1_ending_pixels_checked/report.json'
  proof=json.loads(terminal.read_text())if terminal.exists()else None
  hosts=[r for r in live if r['ProcessId']==hostpid and 'run_p1_ending_pixels_v5247.py'in r['CommandLine']and f'--fighter {fighter}'in r['CommandLine']]
  natives=[r for r in live if r['ProcessId']==nativepid and r['ParentProcessId']==hostpid and
   current.NAME in r['CommandLine']and str(folder)in r['CommandLine']and video.source.LUA in r['CommandLine']]
  need(proof is not None or(len(hosts)==len(natives)==1),'Pending only with actual currently live exact collector/native '+fighter)
  need(executed['pid']==nativepid and executed['hostPID']==hostpid and
   guest['sha256']==current.GUEST_SHA and guest['everyActualByteComparedInRAM']and
   guest['captureSourceSHA256']==sha(video.__file__)and guest['transportSourceSHA256']==sha(ROOT/video.source.LUA),
   'Actual fresh native full guest and exact executed physical wrapper/capture source')
  for file in ['process.json','guest_memory_proof.json','input_hashes_before.json']:
   pins[str(folder/file)]=sha(folder/file)
  if proof:pins[str(terminal)]=sha(terminal)
  generated=video.collector(fighter);bad=unbound.collector(fighter)
  need('fighter'in bad.__code__.co_names and 'fighter'not in bad.__globals__ and
   generated.__globals__['fighter']==fighter,'Actual old missing global retained; successor binding inspected before launch')
  running.append(dict(fighter=fighter,execSession=session,hostPID=hostpid,nativePID=nativepid,
   actualCurrentlyLiveHost=hosts,actualCurrentlyLiveNative=natives,capture=str(folder),
   actualCurrentWholeGuestComparedInRAM=True,
   completeEndingPixelTerminalPending=proof is None,terminal=proof))
 files=['tools/verify_corrected_campaign_terminal_v5232.py',
  'audit_v5233_kano_corrected_p1_campaign_checked/report.json',
  'tools/verify_corrected_campaign_terminal_v5234.py',
  'tools/run_p1_ending_pixels_v5243.py','tools/qualify_p1_ending_source_v5241.py',
  'audit_v5242_p1_ending_source_checked/report.json','tools/run_p1_ending_pixels_v5247.py',
  'tools/qualify_p1_ending_source_v5248.py','tools/p1_ending_cpu_cycle_model_v5240.py',
  'tools/verify_current_p1_ending_pages_v5253.py',*video.source.EXTRA]
 for name in files:
  p=ROOT/name
  if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
  pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All immutable old/failure/new evidence preserved')
 report=dict(schema=1,parentAdditiveJournal=str(PARENT),goalStatus='active',remaining=parent['remaining'],
  mergeRule='Read with5228 and all prior whole-goal journals. All original scope/evidence/exclusions remain. Both current P1 clears accepted only within actual tested native physical contexts, not all artwork/audio/finisher/cinematic/combat/full-port acceptance.',
  previousGoalTurnClassification='no progress: acknowledgement only; revalidated actual state and took available safe work.',
  thisGoalTurnClassification='progress: consumed same95820 native0 Sonya terminal at347965; full unchanged native/physical verifier accepted corrected5219 both P1 campaigns. Extended complete single-base/native CPU/DMA/shift/IO/source-cycle renderer from actual qualified P2 contexts to P1 by explicit original memory-map scope only, with11actual source faults. Before-boot generated-host check caught missing fighter global; original source retained, fresh successor qualified and both physical native full-video campaigns launched. Each actual full1MiB guest independently compared in RAM; currently live exact process commands checked below. Prepared full original page/photo/font/shadow/background verifier; awaiting actual full video terminals.',
  correctedBuildNaturalP1Campaigns=campaigns,p1EndingSourcePreflight=str(sourcepath),p1EndingVideoProcesses=running,
  failedChecksPreserved=[
   dict(source='tools/verify_corrected_campaign_terminal_v5232.py',report='audit_v5233_kano_corrected_p1_campaign_checked/report.json',
    actualDifference='Exactly one final host Average speed trailer; all146205native/game/RGB chronology lines byte identical. Fresh5234 excludes only that final exact trailer with same1555emulated seconds.'),
   dict(source='tools/run_p1_ending_pixels_v5243.py',nativeLaunchOccurred=False,
    issue='Separate preboot actual generated function check found fighter global required but unbound. Sources/preflight retained;5247/5248exact candidate/physical wrapper/model/fighter bindings qualified before native launches.')],
  newInputHashes=pins,newBuilds=0,newRawROMVRAMImageAudioFilesWritten=0,newDeletedFiles=0,
  publicPlayableChanged=False,refreshedReleaseZIP=False,fullPortAcceptance=False,
  storage='Existing5219 executable reused. Entire text gzip-streamed; native guest/VRAM/RGB remain RAM-only. No additional executable/build tree or raw media copies. Prior cleanup/compression savings not recounted.',
  nextAction='Poll same41152/87441 and actual84724/140956 plus138968/142528 while live. Do not restart on timeout or losses. Consume actual terminal reports5250; if whole native video passes, run5253 --fighter against the same complete actual continuous fields to recheck every original photo/glyph/shadow/background/page fault. If it fails, retain full native terminal/model failure and diagnose actual cause. All five original groups remain verbatim.')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(journal=str(OUT/'progress.json'),goalStatus='active',
  bothCurrentP1NativeBossesOwnEndingsAttractAccepted=True,p1VideoLive=[r['fighter']for r in running if r['actualCurrentlyLiveNative']],
  newBuilds=0,rawMediaCopies=0,publicPlayableChanged=False,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
