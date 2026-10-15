"""Add complete guard terminal and actual rejected prime; preserve whole scope."""
import ast,gzip,hashlib,json,re,subprocess
from pathlib import Path
import native_subzero_legs_context_v4993 as native
import run_crouch_prime_sonya_campaign_v5175 as current
import run_tested_prime_sonya_campaign_v5186 as future

ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v5178_campaign_guard_progress/progress.json'
OUT=ROOT/'audit_v5184_tested_prime_progress'

def main():
 need(not OUT.exists(),'Fresh immutable full-scope journal')
 parent=json.loads(PARENT.read_text())
 fullpath=ROOT/'audit_v5182_freeze_guard_terminal_checked/report.json';full=json.loads(fullpath.read_text())
 failedpath=ROOT/'audit_v5180_crouch_prime_prefix_checked/report.json';failed=json.loads(failedpath.read_text())
 need(full['passed']and full['nativeExit']==0 and not full['actualNaturalTowerClearAccepted']and
  full['actualWholeSubZeroPhysicalReplay']['actualCompleteGuardFields']==130800 and
  full['actualWholeSubZeroPhysicalReplay']['actualNativeLegActivations']==336 and
  full['actualWholeSubZeroPhysicalReplay']['actualNativeHumanUppercut107Stores']==0,
  'Actual complete guard native/physical terminal, no clear or invented anti-air activation')
 need(not failed['passed']and 'Actual original HUMAN107 uppercut store must execute'in failed['error'],
  'Actual strict first prime rejection preserved, never claimed as success')
 pins=dict(full['inputHashes'])
 for p,h in json.loads((current.OUT/'input_hashes_before.json').read_text()).items():
  need(p not in pins or pins[p]==h,'Consistent actual old/new compiled/control inputs');pins[p]=h
 paths=[PARENT,fullpath,failedpath,Path(__file__),current.OUT/'process.json',
  current.OUT/'guest_memory_proof.json',current.OUT/'input_hashes_before.json',Path(future.__file__),
  ROOT/'mk2ks_sonya_p1_subzero_tested_prime_ram_v5185.lua',ROOT/'tools/verify_tested_prime_prefix_v5188.py',
  ROOT/'mk2ks_move_phase_shadow_v5081.lua',ROOT/'tools/verify_move_phase_shadow_v5089.py']
 for p in paths:pins[str(p.resolve())]=sha(p)
 for p in[Path(future.__file__),ROOT/'tools/verify_tested_prime_prefix_v5188.py']:ast.parse(p.read_text())
 proof=json.loads((current.OUT/'guest_memory_proof.json').read_text())
 need(proof['sha256']==native.GUEST_SHA and proof['everyActualByteComparedInRAM']and
  proof['transportSourceSHA256']==sha(ROOT/current.LUA)and proof['captureSourceSHA256']==sha(current.__file__),
  'Actual new prime cold boot complete guest/source provenance')
 lines=[]
 with gzip.open(current.OUT/'run.log.gz','rt',encoding='utf-8',newline='')as reader:
  for line in reader:
   need(line.endswith('\n'),'Complete original first encounter prefix available')
   lines.append(line)
   if line.startswith('MK2_NAT_CAMPAIGN_LOSS ')and ' stage=7'in line:break
 text=''.join(lines);raw=text.encode()
 native_rows=[]
 for line in text.splitlines():
  if not line.startswith('MK2_NAT_CAMPAIGN_'):continue
  row=dict(re.findall(r'(\w+)=([^\s]+)',line));frame=int(row['frame'])
  if 98938<=frame<=98951 and line.startswith(('MK2_NAT_CAMPAIGN_SUBZERO_','MK2_NAT_CAMPAIGN_INPUT ')):
   native_rows.append(line)
 need(any('frame=98944 'in line and 'button=High_Punch'in line for line in native_rows)and
  any('frame=98940 'in line and 'before=1793 after=770 'in line and 'pc=FF83C340'in line for line in native_rows)and
  all('after=263 'not in line for line in native_rows),
  'Real Block701-to-crouch302 chronology, six-field early HP and missing HUMAN107 captured')
 basic=(ROOT/'mk2ks_move_phase_shadow_v5081.lua').read_text()
 for token in("age>=900 and age<924 then press(side,'Down')","age>=910 and age<913 then press(side,'High Punch')"):
  need(token in basic,'Exact actually executed stock/added-fighter uppercut physical timeline')
 command="Get-CimInstance Win32_Process -Filter \"Name='mkport_candidate.exe' OR Name='python.exe'\" | Where-Object { $_.ProcessId -eq 109260 -or $_.ProcessId -eq 79468 } | Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
 need(census.returncode==0,'Fresh actual native/collector command census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 resultpath=current.OUT/'result.json';terminal=json.loads(resultpath.read_text())if resultpath.exists()else None
 if terminal is None:
  need(any(r['ProcessId']==109260 and str(current.OUT)in r['CommandLine']for r in live)and
   any(r['ProcessId']==79468 and 'run_crouch_prime_sonya_campaign_v5175.py'in r['CommandLine']for r in live),
   'Pending only with both actual specific currently live jobs')
 need(all(sha(p)==h for p,h in pins.items()),'Every old terminal, new failure, current source and future prep byte unchanged')
 report=dict(schema=1,parentAdditiveJournal=str(PARENT),mergeRule='Read with5178and all its parents; all original requirements/proofs persist. More bounded native/physical stress is not a natural clear, full art/audio/ending or release acceptance.',
  goalStatus='active',remaining=parent['remaining'],newInputHashes=pins,
  previousGoalTurnClassification='progress: whole old current native terminal verified, real guard encounter replay/source faults accepted, first prime prepared from an earlier misleading9/6comment, scope and exact pending/terminal process status retained.',
  thisGoalTurnClassification='progress: consumed same14420actual guard native0terminal at322771frames,79paid losses/no clear. Independently accepted all130800Sub fields,336actual leg entries,27926own action stores, zero107, plus complete unchanged Kitana/Jax/source schedules/winners/actual guest and zero cache global stores. Fresh current5175prime cold boot selected true18and qualified entire guest. Strict5179actually rejected missing native107; preserved failed proof. Actual98938..98951Block701-to-crouch302/HP trace shows six-field prime still too early. Authoritative executed5081uses Down24/HP10..12, contrary to old comment. Prepared exact-tested input-only5185/5186and independent5188checker; no game patch or source-only activation credited.',
  actualWholeGuardTerminal=dict(report=str(fullpath),execSession=14420,execTerminalConsumed=True,nativeExit=0,
   frames=322771,subZeroFields=130800,actualNativeLegEntries=336,actualHuman107Stores=0,ownSubZeroRoundWins=4,
   nativeCacheGlobalStores=0,paidLosses=79,naturalTowerClearAccepted=False),
  actualRejectedPrime=dict(report=str(failedpath),completedFirstEncounterBoundary=text.splitlines()[-1],
   prefixBytes=len(raw),prefixSHA256=hashlib.sha256(raw).hexdigest().upper(),realNativeAndInputWitnesses=native_rows,
   humanUppercut107Accepted=False,scope='Live first encounter only; complete replay remains pending actual terminal.'),
  currentPrimeCampaign=dict(execSession=54519,nativePID=109260,collectorPID=79468,exactLiveProcesses=live,
   nativeTerminal=terminal is not None,nativeExit=terminal['nativeExit']if terminal else None,
   compressedTraceBytes=(current.OUT/'run.log.gz').stat().st_size,growingLogNotPinnedAsTerminal=terminal is None,
   actualNaturalTowerClearAccepted=False),
  preparedExactTestedCorrection=dict(lua=future.LUA,host=str(Path(future.__file__)),
   checker='tools/verify_tested_prime_prefix_v5188.py',nativeBootPerformed=False,humanUppercut107Accepted=False,
   exactPhysicalTiming='Hold Down0..23, press HP10..12; unchanged leg sequence remains12fields. No actor/health/state/AI/RNG writes.'),
  knownCandidateMetadataReleaseDefect=full['exactCompiledMetadataWarning'],
  publicPlayableChanged=False,newBuilds=0,newlyDeletedFiles=0,rawGuestMediaAudioFilesWritten=0,
  fullPortAcceptance=False,finishedRelease=False,
  nextAction='Poll same54519and exact109260/79468while actual commands are live; consume actual native terminal before another boot.5179strict missing107failure is evidence, not a clear or port-code fault. Preserve whole5176capture and exact checksum-bound test warning. After actual terminal, use unused5186/5187normal exact5081Down24/HP10..12controller if needed, then5188only after real completed Sub encounter, requiring actual original HUMAN107stores. Never weaken activation criterion, force opponents/wins or supply state/health/RNG. Full all-five Pit/Tomb/victim/finisher/art/grounding/shadow/arena/audio/morph/secret/cinematic/selection/ladder/names/cleanup/refreshed-release groups stay open. Correct exact stale compiled payload ROM metadata before production release.',
  storage='Only compressed textual native chronicles and digest/source JSON; no new native build/ROM/guest/RGB/PCM copies. Previous reclamation not recounted.')
 need(len(report['remaining'])==5,'Entire original five-group objective intact')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(journal=str(OUT/'progress.json'),wholeGuardTerminalVerified=True,
  actualPrime107FailurePreserved=True,currentPrimeCampaign=report['currentPrimeCampaign'],
  exactTestedFuturePrimePreparedNotActivated=True,goalStatus='active',fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
