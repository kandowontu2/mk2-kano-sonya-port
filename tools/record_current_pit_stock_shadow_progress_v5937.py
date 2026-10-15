"""Seal native original Pit scheduling and four current full finite scenes.

Original complete scope remains active. No new builds, raw recordings,
source trees or public promotion; preserve actual failed test post-gates.
"""
import datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
from record_current_cross_tomb_audio_v5844 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5915_current_cross_pit_movie_ground_progress/progress.json'
OUT=ROOT/'audit_v5938_current_pit_stock_shadow_progress'

def run():
 need(not OUT.exists(),'Fresh immutable additive full-scope progress')
 current.expected();parent=json.loads(PARENT.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,
      'Every original group remains in scope, including already qualified campaigns/own endings')
 pins={str(PARENT):sha(PARENT)};sealed=[];cases=[]
 def bind(path):
  value=json.loads(path.read_text());need(value['passed'],'Completed native qualification '+str(path))
  pins[str(path)]=sha(path);sealed.append(path)
  for p,h in value['inputHashes'].items():
   need(p not in pins or pins[p]==h,'Consistent immutable observed/compiled/protected inputs');pins[p]=h
  return value
 ordinary=bind(ROOT/'audit_v5919_original_stock_pit_shadow_inventory_checked/report.json')
 stock=bind(ROOT/'audit_v5928_original_stock_pit_shadow_schedule_checked/report.json')
 need(ordinary['originalDriver']==stock['originalDriver']=='mk2'and stock['genuineFullHealthMatches']==7 and
      stock['genuineCollisionDamage']==2254 and stock['completedFields']==1101 and len(stock['effectiveActualScheduleFaultsRejected'])==14 and
      stock['originalStockPitShadowSchedulingAccepted']and stock['sourceNativeNonFloorFontDraws']['actualOriginalFontCommands']==63110 and
      stock['sourceNativeNonFloorFontDraws']['actualOriginalFontDescriptors']==47,
      'Entire genuine original ordinary/cinematic native scheduling, actual font descriptors and14 effective faults')
 processes=[]
 for leaf in ('audit_v5918_original_stock_pit_shadow_inventory','audit_v5922_original_stock_pit_cinematic_shadow'):
  folder=ROOT/leaf;process=json.loads((folder/'process.json').read_text());terminal=json.loads((folder/'terminal.json').read_text())
  need(terminal['exit_code']==0 and terminal['pid']==process['pid']and '-nocheat'in process['command']and
       process['command'][1]=='mk2'and '-nosamples'in process['command'],'Both actual stock native processes terminal0, true original driver, no cheats or imported voices')
  processes.append(process)
  for p in folder.rglob('*'):
   if not p.is_file():continue
   need(p.suffix.lower()not in('.png','.wav','.pcm','.bin','.rgb','.exe','.zip','.mdata'),
        'No new raw recording/build/ROM/source-tree duplicates')
   pins[str(p)]=sha(p)
   if p.suffix.lower()in('.json','.log','.cfg','.txt'):sealed.append(p)
 for fighter,side in (('kano',1),('kano',2),('sonya',1),('sonya',2)):
  path=ROOT/f'audit_v5936_current_{fighter}_p{side}_pit_stock_shadow_scene_checked/report.json';proof=bind(path)
  scene=proof['nativeScene'];shadow=scene['actualNativePitShadowPolicy'];expected=677 if side==1 else 676
  need(proof['candidate']==current.NAME and proof['fighter']==fighter and proof['physicalSlot']==side and
       proof['actualCurrentCrossPitCompleteRetainedNativeSceneAccepted']and proof['wholeNativePitShadowPolicyAccepted']and
       proof['completeNativePitSceneAccepted']and proof['retainedLiveExactFields']==expected and
       proof['retainedLiveExactRGBPixels']==expected*101600 and proof['retainedLiveExactCPUWrites']==516 and
       proof['retainedLiveActualPixelFaultGateCompleted']and proof['newNativeBoots']==proof['newRastersReplayed']==0 and
       not proof['rawTargetsReconstructed']and shadow['passed']and shadow['currentPitShadowSchedulingMatchesOriginal']and
       shadow['actualCurrentFloorShadowCommands']==scene['nativeShadowCopies']==0 and
       shadow['physicalShadowFlagsRetained']and shadow['ownCinematicNoShadowFlagsMatchOriginal']and
       not shadow['directCurrentShadowEnableVariableObservation']and len(shadow['actualShadowPolicyFaultsRejected'])==5 and
       len(scene['actualMovieFaultsRejected'])==31 and len(scene['actualNativePhaseGroundFaultsRejected'])==6 and
       len(scene['actualEarnedFaultsRejected'])==12 and scene['nativeState']['earned_matches']==7 and
       not proof['completeStageVictimAudioAccepted']and not proof['independentStockChoreographyAccepted']and not proof['fullPortAcceptance'],
       'Whole finite current live-raster/native movie/phase floor/original shadow/font/cleanup/earned proof and every original/new fault preserved')
  cases.append(dict(fighter=fighter,physicalSlot=side,report=str(path),liveExactFields=expected,liveExactRGBPixels=expected*101600,
                    shadowPolicy=shadow,wholeFiniteCurrentPitSceneAccepted=True,completeStageVictimAudioAccepted=False))
 for leaf in ('mk2_stock_pit_shadow_inventory_v5916.lua','tools/capture_stock_pit_shadow_inventory_v5917.py',
              'mk2_stock_pit_cinematic_shadow_v5920.lua','tools/capture_stock_pit_cinematic_shadow_v5921.py',
              'tools/qualify_stock_pit_shadow_schedule_v5925.py','tools/qualify_stock_pit_shadow_schedule_v5927.py',
              'tools/current_pit_shadow_schedule_contract_v5929.py','tools/verify_current_pit_original_shadow_scene_v5930.py',
              'tools/current_pit_shadow_schedule_bindings_v5932.py','tools/verify_current_pit_shadow_bound_scene_v5933.py',
              'tools/verify_current_pit_shadow_namespace_v5935.py','tools/record_current_pit_stock_shadow_progress_v5937.py',
              'audit_v5923_original_stock_pit_cinematic_shadow_checked/report.json',
              'audit_v5924_original_stock_pit_cinematic_shadow_checked/report.json',
              'audit_v5926_original_stock_pit_shadow_schedule_checked/report.json',
              'audit_v5931_current_kano_p1_pit_original_shadow_scene_checked/report.json',
              'audit_v5934_current_kano_p1_pit_native_shadow_scene_checked/report.json'):
  path=ROOT/leaf;pins[str(path)]=sha(path);sealed.append(path)
 pids=sorted({p[k]for p in processes for k in('pid','hostPID')})
 query="Get-CimInstance Win32_Process -Filter '"+' OR '.join(f'ProcessId={p}'for p in pids)+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 output=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(output)if output else []
 if isinstance(jobs,dict):jobs=[jobs]
 for p in processes:
  started=datetime.datetime.fromisoformat(p['startedUTC']).timestamp()
  need(not any(j['ProcessId']==p['pid']and j['Name']=='mkport_candidate.exe'and p['command'][-1]in(j['CommandLine']or'')and
               abs(j['createdUnix']-started)<.1 for j in jobs),'Exact captured native stock job is terminal')
  need(not any(j['ProcessId']==p['hostPID']and j['Name']=='python.exe'and
               ('capture_stock_pit_shadow_inventory_v5917.py'in(j['CommandLine']or'')or'capture_stock_pit_cinematic_shadow_v5921.py'in(j['CommandLine']or''))for j in jobs),
       'Exact captured stock host is terminal, no timeout-based restart')
 current.expected();need(all(sha(p)==h for p,h in pins.items()),'All current/compiled/user-dirty/public/prior/executed/failed/source/evidence bytes unchanged')
 sealed=list(dict.fromkeys(p.resolve()for p in sealed));before=sum(allocated(p)for p in sealed)
 for p in sealed:
  digest=sha(p);done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
  need(done.returncode==0 and sha(p)==digest,'Exact bounded sealed text losslessly compressed, no recovery copy')
 after=sum(allocated(p)for p in sealed)
 progress=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],cases=cases,
  previousGoalTurnClassification='no progress: acknowledgement only; authoritative5915 evidence revalidated before fresh original controls',
  thisGoalTurnClassification='progress: two independent genuine original mk2 physical controls earn the Pit; six preceding arenas provide positive native floor-copy controls,301ordinaryPit fields omit them despite real actor shadow flags. Original full1101field Pit stage/cinematic/nextscreen also makes zero floor-kernel calls;63110mode8commands bind47original1bppfont descriptors. Native typed parserMain versus fighterMain, original retirement-clear phase and14actual schedule/source faults qualify. Four existing current full one-base RGB scenes are now qualified with independent original shadow policy plus20actual new shadow/font/source faults, retaining all124movie24floor48earned faults. All original five goal groups remain active.',
  actualCurrentBothCharactersBothSlotsPitMovieGroundShadowCleanupAccepted=True,wholeFiniteCurrentCrossPitScenesAccepted=True,
  retainedWholeLiveRGBFields=sum(c['liveExactFields']for c in cases),retainedWholeLiveRGBPixels=sum(c['liveExactRGBPixels']for c in cases),
  actualOriginalStockScheduleFaultsRejected=14,actualCurrentShadowPolicyFaultsRejected=20,
  actualMovieFaultsRejected=124,actualSourceNativeGroundFaultsRejected=24,actualEarnedFaultsRejected=48,
  currentNativeFontMode8Commands=sum(c['shadowPolicy']['actualCurrentNativeFontMode8Commands']for c in cases),
  originalReferenceSchedulingOnlyNotStockRGBOrAudio=True,directCurrentShadowEnableVariableObservation=False,
  completeStageVictimAudioAccepted=False,allNativePitCuePriorityAndRNGAccepted=False,
  allVictimsArenasMovesCPURepeatedFinishersAccepted=False,independentStockChoreographyAccepted=False,fullPortAcceptance=False,
  newNativeBoots=2,newBuilds=0,newRawGuestRGBVRAMPCMCopies=0,newDeletedFiles=0,
  publicPlayableChanged=False,publicZIPChanged=False,exactCapturedNativeProcessesStillLive=[],observedOtherOrReusedPIDs=jobs,
  consumedNativeCaptureSessions=[6009,35681],consumedQualifierSessions=[43081,75380,26475,79557,70287,48398,27638],
  sealedTextFiles=len(sealed),sealedAllocatedBytesBefore=before,sealedAllocatedBytesAfter=after,sealedAllocatedBytesReclaimed=before-after,
  newInputHashes=pins,
  next='Proceed to broader real stock victim/current mirror Pit/Tomb integration and remaining native effect/victim audio priority/RNG/direct Main+140 observation where needed; do not re-run these completed finite Pit scenes or add artificial floor shadows to the Pit. Preserve every full move/arena/CPU/repeated/KO/overlap, other finisher/victim/morph/secret/cinematic, verified natural campaigns/own endings, final UI/ladder/names/audio, dependency-aware cleanup and matching refreshed release ZIP requirement. Do not regenerate permanently retired build/raw/source-tree history.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(progress,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
      'Full-scope additive journal losslessly sealed')
 print(json.dumps({k:v for k,v in progress.items()if k not in('newInputHashes','remaining','cases')},indent=2),flush=True)

if __name__=='__main__':run()
