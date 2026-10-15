"""Seal actual missing cross Tomb branch timings without claiming art/audio.

Re-evaluate every entire original earned/unpressed-source contract and every
original actual earned/branch fault from the completed cold-run text. Preserve
all trials, including timings which did not produce the requested branch.
"""
import datetime,gzip,hashlib,json,re,subprocess
from pathlib import Path
import find_current_cross_tomb_native_branches_v5872 as search
from record_current_cross_tomb_audio_v5844 import allocated
ROOT,need,sha=search.ROOT,search.need,search.sha
OUT=ROOT/'audit_v5875_current_cross_tomb_native_timing_progress'
HOST_IDENTITIES={
 122008:'2026-10-08T04:23:58.344656-04:00',85416:'2026-10-08T04:23:58.350613-04:00',
 145204:'2026-10-08T04:23:58.368188-04:00',142156:'2026-10-08T04:23:58.420074-04:00',
 135372:'2026-10-08T04:24:58.530419-04:00',133680:'2026-10-08T04:24:58.561207-04:00',
 146816:'2026-10-08T04:24:58.587674-04:00',
}
SEARCHES=(
 'search_kano_p1_01_01_held.json','search_sonya_p1_01_01_held.json',
 'search_kano_p2_02_02_drop.json','search_sonya_p2_11_11_drop.json',
 'search_kano_p1_02_02_held.json','search_kano_p2_03_18_drop.json',
 'search_sonya_p2_01_10_drop.json',
)
SELECTED={('kano',1):2,('sonya',1):1,('kano',2):11,('sonya',2):8}

def run():
 need(not OUT.exists(),'Fresh immutable actual timing checkpoint')
 proof=search.preflight();guest=search.current.expected()
 parentpath=ROOT/proof['parentProgress'];parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and
  parent['actualCurrentBothCharactersBothSlotsCrossPressedTombFullSceneGroundShadowEraseAccepted']and
  not parent['fullPortAcceptance'],'Retain all wider original scope and actual preceding state/scene/audio/move/UI/ending/campaign evidence')
 pins=dict(parent['newInputHashes']);pins[str(parentpath)]=sha(parentpath)
 need(all(sha(p)==h for p,h in pins.items()),'Every current and prior source/evidence hash intact')
 seen=set();cases=[];selected=[];processes=[];sealed=[];search_results=[]
 for name in SEARCHES:
  path=search.OUT/name;result=json.loads(path.read_text());pins[str(path)]=sha(path);sealed.append(path)
  need(result['passed']and result['goalStatus']=='active'and
   result['sourcePreflight']==proof and result['allStartedRunsActuallyTerminal']and
   result['requestedNativeBranchObserved']==bool(result['matchingActualBranches'])and
   not result['fullSceneRasterShadowAudioAccepted']and not result['fullPortAcceptance'],
   'Every actual finite search retained as observed, including nonmatching hypotheses')
  actual_found=[t for t in result['actualTrials']if t['nativeBranch']['nativeDrop']==(result['wantedNativeBranch']=='drop')]
  need(actual_found==result['matchingActualBranches'],'No held/drop relabeling in any actual trial')
  search_results.append(dict(report=str(path),wanted=result['wantedNativeBranch'],
   trials=len(result['actualTrials']),matchingActualBranches=len(actual_found)))
  for trial in result['actualTrials']:
   fighter,side,delay=trial['fighter'],trial['side'],trial['physicalDelay']
   key=(fighter,side,delay);need(key not in seen,'Distinct physical timing trial, no duplicate positive');seen.add(key)
   folder=Path(trial['capture']);need(folder==search.OUT/f'{fighter}_p{side}_delay{delay:02d}',
    'Exact current cold timing capture path')
   meta=json.loads((folder/'result.json').read_text());process=json.loads((folder/'process.json').read_text());processes.append(process)
   with gzip.open(folder/'run.log.gz','rt')as reader:log=reader.read()
   need(meta['exit_code']==0 and meta['candidate']==search.NAME and meta['fighter']==fighter and
    meta['side']==side and meta['physicalCommandDelay']==delay and meta['guestSHA256']==search.current.GUEST_SHA and
    meta['assistance']=='none'and meta['guest_writes']==0 and not meta['cheats_enabled']and
    not meta['fullPortAcceptance']and meta['rawRasterAudioROMBuildCopiesWritten']==0 and
    (folder/'stderr.log').read_text()==''and 'hex='not in log and not re.search(
     r'LUA ERROR|Lua error|stack traceback|fatal error|WRONG CHECKSUMS|HOST_DEADLINE',log,re.I),
    'Whole current RAM guest, ordinary input-only native terminal, no raw buffers or deadline acceptance')
   need(process['hostPID']in HOST_IDENTITIES and process['hostSource']==str(Path(search.__file__).resolve())and
    process['startedUnix']>datetime.datetime.fromisoformat(HOST_IDENTITIES[process['hostPID']]).timestamp()and
    process['command'][0]==str(ROOT/search.NAME/'mkport_candidate.exe')and
    process['command'][-1]==str(ROOT/search.OBSERVER)and '-samples'in process['command']and
    '-nocheat'in process['command']and '-nothrottle'in process['command'],
    'Actual inspected cold host and exact candidate/read-only provenance invocation')
   config=[dict(re.findall(r'(\w+)=([^\s]+)',l))for l in log.splitlines()if l.startswith('MK2_TOMB_TIMING_CONFIGURATION ')]
   digest=[dict(re.findall(r'(\w+)=([^\s]+)',l))for l in log.splitlines()if l.startswith('MK2_TOMB_TIMING_GUEST_DIGEST ')]
   need(config==[dict(delay=str(delay),writes='0',assistance='none')]and
    digest==[dict(frame='1',bytes='1048576',sha256=search.current.GUEST_SHA)],
    'Actual declared controller wait and whole initialized RAM guest digest, no prescribed RNG')
   positive=search.native.branch(log,guest,fighter,side)
   earned=search.native.state.actual_faults(log,fighter,side,guest)
   branches=search.native.faults(log,guest,fighter,side)
   identity=17 if fighter=='kano'else 18
   need(trial['passed']and trial['originalEarnedContractPassed']and trial['noForcedNativeState']and
    positive==trial['nativeBranch']and positive['trueVictim']==35-identity and
    positive['earnedContract']['earned_matches']==2 and positive['earnedContract']['consecutive_fields']==801 and
    len(earned)==12 and len(branches)==4 and earned==trial['actualEarnedFaultsRejected']and
    branches==trial['actualBranchFaultsRejected']and
    search.native.branch(log,guest,fighter,side)==positive,
    'Entire native1731/3643/4357 cross contract, all actual earned/source faults and positive restoration')
   need((positive['nativeDrop']and 0<=positive['actualNativeRandomValue']<50 and
     positive['nativeMotion']['phase']['checkedConsecutiveCallbacks']==269)or
    (not positive['nativeDrop']and 50<=positive['actualNativeRandomValue']<1000 and
     positive['nativeMotion']['continuousArena1MotionCallbacks']>400),
    'Actual untouched original random comparison and complete drop or held native victim motion')
   for p,h in meta['input_hashes'].items():
    need((p not in pins or pins[p]==h)and sha(p)==h,'Whole actual compiled/source/assets hash inputs retained');pins[p]=h
   for p in folder.rglob('*'):
    if not p.is_file():continue
    need(p.suffix.lower()not in('.png','.wav','.bin','.pcm','.rgb','.exe','.mdata','.zip'),
     'Bounded gzip and text only, no duplicate build/raw media')
    pins[str(p.resolve())]=sha(p)
    if p.suffix.lower()in('.json','.log','.txt','.cfg'):sealed.append(p)
   row=dict(fighter=fighter,physicalSlot=side,physicalCommandDelay=delay,capture=str(folder),
    nativeBranch=positive,actualEarnedFaultsRejected=12,actualNativeBranchFaultsRejected=4,
    fullSceneRasterShadowAudioAccepted=False)
   cases.append(row)
   if SELECTED.get((fighter,side))==delay:
    need(positive['nativeDrop']==(side==2),'Selected actual missing player-slot branch, never inferred by timing')
    selected.append(row)
 need(len(cases)==25 and len(selected)==4 and {(r['fighter'],r['physicalSlot'])for r in selected}==set(SELECTED),
  'All25 cold trials retained and all four actual missing cross player-slot branches observed')
 pids=sorted({p[k]for p in processes for k in('pid','hostPID')})
 query="Get-CimInstance Win32_Process -Filter '"+' OR '.join(f'ProcessId={p}'for p in pids)+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 output=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(output)if output else []
 if isinstance(jobs,dict):jobs=[jobs]
 for process in processes:
  need(not any(j['ProcessId']==process['pid']and j['Name']=='mkport_candidate.exe'and
   abs(j['createdUnix']-process['startedUnix'])<.05 and search.OBSERVER in(j['CommandLine']or'')for j in jobs),
   'Every exact native trial process terminal, not merely an observation timeout')
  need(not any(j['ProcessId']==process['hostPID']and j['Name']=='python.exe'and
   'find_current_cross_tomb_native_branches_v5872.py'in(j['CommandLine']or'')for j in jobs),
   'All exact inspected cold search hosts terminal')
 for p in (ROOT/search.DRIVER,ROOT/search.OBSERVER,Path(search.__file__),Path(__file__)):
  pins[str(p.resolve())]=sha(p);sealed.append(p)
 search.current.expected();need(all(sha(p)==h for p,h in pins.items()),'Every prior and actual current source/evidence/public hash unchanged')
 sealed=list(dict.fromkeys(p.resolve()for p in sealed));before={str(p):sha(p)for p in sealed}
 before_allocated=sum(allocated(p)for p in sealed)
 for p in sealed:
  need(p.is_relative_to(ROOT.resolve())and subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0,
   'Exact bounded immutable text losslessly compacted')
 after_allocated=sum(allocated(p)for p in sealed)
 need(all(sha(p)==h for p,h in before.items()),'All executed source/evidence bytes unchanged by compression')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  parentAdditiveJournal=str(parentpath),remaining=parent['remaining'],sourcePreflight=proof,
  previousGoalTurnClassification=parent['thisGoalTurnClassification'],
  thisGoalTurnClassification='progress:25 genuine cold current cross Tomb trials with ordinary input timing completed. Both missing P1held and P2random-drop outcomes observed for Kano/Sonya with original RNG untouched. Entire original full-health two-KO/paid-match/select/command/native action/801field/1100cleanup and actual PC/IO/actor/Main/continuous held or269drop source contracts pass;300earned and100native branch counterexamples reject. This is new branch/state evidence, not full raster/audio or all-port acceptance. All wider original goal groups retained.',
  actualTimingTrials=25,cases=cases,searchResults=search_results,selectedActualMissingBranchProfiles=selected,
  actualMissingCrossP1HeldAndP2RandomDropStatesAccepted=True,actualEarnedFaultsRejected=300,actualNativeBranchFaultsRejected=100,
  priorCurrentCrossObservedPressedAudioAndFullScenesAndAllMirrorBranchesRetained=True,
  allCurrentCrossHeldPressedRandomStateContextsAccepted=True,allCurrentCrossHeldPressedRandomFullScenesAccepted=False,
  allCurrentCrossHeldPressedRandomEnabledAudioAccepted=False,fullSceneRasterShadowAudioAccepted=False,
  broaderPitTombVictimsAccepted=False,fullMovePhaseAllArenaCPURepeatedKOOverlapAccepted=False,
  completeStageVictimAudioAccepted=False,independentStockChoreographyAndAllCinematicsAccepted=False,fullPortAcceptance=False,
  rawNativeGuestRGBVRAMPCMFilesWritten=0,newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,publicZIPChanged=False,
  consumedCaptureToolSessions=[42393,82906,55413,69465,88645,53190,58128],exactCaptureProcessesStillLive=[],
  observedOtherOrReusedPIDs=jobs,initialLiveHostIdentities=HOST_IDENTITIES,newInputHashes=pins,
  sealedTextSourcesLosslesslyCompacted=len(sealed),sealedAllocatedBytesBefore=before_allocated,
  sealedAllocatedBytesAfter=after_allocated,sealedAllocatedBytesReclaimed=before_allocated-after_allocated,
  next='Use the four actual selected profiles for complete enabled source audio/channel/voice/cleanup and native one-base full-scene/ground/shadow/retirement checks. Do not repeat the completed timing search or previous finite matrices for status. Continue broader native Pit/Tomb stock victims, exact source audio priority/RNG choices, independent stock choreography, all original move/arena/CPU/repeated/KO/overlap and other finisher/victim/morph/secret/cinematic requirements, retained natural campaigns/endings, final combined UI/ladder/names/audio integration and refreshed release ZIP. Preserve dependency-aware cleanup and never regenerate permanently retired builds/raw recordings.')

if __name__=='__main__':
 report=run();OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(report,indent=2)+'\n')
 digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
  'New original-scope timing checkpoint losslessly compressed')
 print(json.dumps({k:v for k,v in report.items()if k not in('remaining','newInputHashes','cases','selectedActualMissingBranchProfiles','searchResults')},indent=2),flush=True)
