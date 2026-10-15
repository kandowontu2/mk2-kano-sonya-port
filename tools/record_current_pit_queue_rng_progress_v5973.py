"""Seal actual native queue/RNG progress and all immutable failed evidence."""
import datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
from record_current_cross_tomb_audio_v5844 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5953_current_subzero_pit_audio_progress/progress.json'
OUT=ROOT/'audit_v5974_current_pit_queue_rng_progress'

def run():
 need(not OUT.exists(),'Fresh immutable additive whole-goal progress')
 current.expected();parent=json.loads(PARENT.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,
      'Previous turn is verified progress; all five original goal groups remain active')
 pins={str(PARENT):sha(PARENT)};sealed=[];proofs={}
 for leaf in('audit_v5963_current_pit_queue_rng_source_checked','audit_v5966_current_pit_queue_rng_mix_checked',
             'audit_v5970_current_pit_queue_rng_checked','audit_v5972_current_pit_queue_rng_owner_checked'):
  path=ROOT/leaf/'report.json';value=json.loads(path.read_text());need(value['passed'],'Completed whole native post-gate '+leaf)
  proofs[leaf]=value;pins[str(path)]=sha(path);sealed.append(path)
  for p,h in value['inputHashes'].items():
   need(p not in pins or pins[p]==h,'Consistent whole compiled/executed/native/prior pins');pins[p]=h
 audio=proofs['audit_v5966_current_pit_queue_rng_mix_checked'];rng=proofs['audit_v5970_current_pit_queue_rng_checked']
 owner=proofs['audit_v5972_current_pit_queue_rng_owner_checked']
 need(audio['exactStereoPCMFrames']==3863040 and audio['actualSourceAudioFaultsRejected']==116 and
      audio['actualEarnedStateFaultsRejected']==48 and audio['actualRawMixedPCMFaultsRejected']==16 and
      audio['actualMixedSourceOperationFaultsRejected']==16 and owner['actualDirectNativeFaultsRejected']==104 and
      rng['actualNativeCoreCalls']==4484 and rng['actualBoundedRNGCalls']==80 and rng['actualSoundVariantSelectors']==32 and
      rng['actualObservedSlotDecisions']==72 and rng['actualNativeRNGPriorityFaultsRejected']==144 and
      rng['allObservedNativeRNGWordsAndChoicesAccepted']and rng['allObservedEmptyReplacementSlotDecisionsAccepted']and
      not rng['nativeSuppressionBranchAccepted']and not rng['nativeSpecial71BranchAccepted']and
      not rng['allNativePitCuePriorityAndRNGAccepted']and not rng['completeStageVictimAudioAccepted']and not rng['fullPortAcceptance'],
      'Every original audio/state/owner/raw/source fault plus144 actual RNG/queue faults retained, finite branches only')
 processes=[];cases=[];failures=[]
 host_creation={('kano',1):'2026-10-08T07:15:51.985661-04:00',('kano',2):'2026-10-08T07:15:52.009752-04:00',
                ('sonya',1):'2026-10-08T07:15:51.986500-04:00',('sonya',2):'2026-10-08T07:15:52.009079-04:00'}
 for fighter in('kano','sonya'):
  for side in(1,2):
   for version in(5959,5964):
    folder=ROOT/f'audit_v{version}_current_pit_queue_rng_{fighter}_p{side}_samples'
    process=json.loads((folder/'process.json').read_text());meta=json.loads((folder/'result.json').read_text())
    processes.append((process,fighter,side,version))
    if version==5959:
     need(meta['exit_code']==3 and 'cannot open mk2ks_native_stage_failure_deadline_v890.lua'in(folder/'stderr.log').read_text(),
          'All actual frame0 failed boots preserved, no accepted gameplay claim')
     failures.append(dict(fighter=fighter,physicalSlot=side,capture=str(folder),nativeExitCode=3,reason='Missing deadline file before gameplay'))
    else:
     ac=next(c for c in audio['cases']if c['fighter']==fighter and c['physicalSlot']==side)
     oc=next(c for c in owner['cases']if c['fighter']==fighter and c['physicalSlot']==side)
     rc=next(c for c in rng['cases']if c['fighter']==fighter and c['physicalSlot']==side)
     old=json.loads((ROOT/f'audit_v5947_current_subzero_pit_mix_{fighter}_p{side}_samples/result.json').read_text())
     need(meta['exit_code']==0 and meta['mixedPCMSHA256']==old['mixedPCMSHA256']and
          meta['fighter']==fighter and meta['side']==side and ac['origin']==oc['origin']and ac['terminal']==oc['terminal']and
          len(ac['actualAudioSourceWindowFaultsRejected'])==29 and len(oc['actualFaultsRejected'])==26 and
          len(rc['actualFaultsRejected'])==36 and process['command'][1]=='mk2ks'and '-samples'in process['command']and
          '-nocheat'in process['command']and process['command'][-1]==str(ROOT/'mk2ks_current_pit_queue_rng_campaign_v5960.lua'),
          'Four corrected true own17/18 versus original8 native terminals, original waveform unchanged under passive observer and every fault matrix agrees')
     cases.append(dict(fighter=fighter,physicalSlot=side,ownID=oc['ownID'],actualOriginalVictimID=8,nativeExitCode=0,
                       earnedMatches=ac['completeNativeEarnedContract']['earned_matches'],origin=oc['origin'],terminal=oc['terminal'],
                       actualWholePCMSHA256=ac['actualWholePCMSHA256'],nativeCoreCalls=rc['nativeCoreCalls'],nativeBoundedRNGCalls=rc['nativeBoundedRNGCalls'],
                       actualPriorityBranches=rc['actualPriorityBranches'],actualSelectedSlots=rc['actualSelectedSlots'],
                       allObservedNativeRNGAndSlotDecisionsAccepted=True,allNativePitCuePriorityAndRNGAccepted=False))
    for path in folder.rglob('*'):
     if not path.is_file():continue
     need(path.suffix.lower()not in('.wav','.pcm','.png','.rgb','.bin','.exe','.zip','.mdata'),'No duplicate/raw native/build/ROM/release artifacts')
     pins[str(path)]=sha(path)
     if path.suffix.lower()in('.json','.log','.txt','.cfg'):sealed.append(path)
 for leaf in('mk2ks_current_pit_queue_rng_v5954.lua','mk2ks_current_pit_queue_rng_campaign_v5955.lua',
             'mk2ks_current_pit_queue_rng_campaign_v5960.lua','tools/run_current_pit_queue_rng_v5956.py',
             'tools/qualify_current_pit_queue_rng_v5957.py','tools/run_current_pit_queue_rng_v5961.py',
             'tools/qualify_current_pit_queue_rng_v5962.py','tools/verify_current_pit_queue_rng_mix_v5965.py',
             'tools/qualify_current_pit_queue_rng_v5967.py','tools/qualify_current_pit_queue_rng_boundary_v5969.py',
             'tools/verify_current_pit_queue_rng_owner_v5971.py','tools/record_current_pit_queue_rng_progress_v5973.py',
             'audit_v5958_current_pit_queue_rng_source_checked/report.json','audit_v5968_current_pit_queue_rng_checked/report.json'):
  path=ROOT/leaf;pins[str(path)]=sha(path);sealed.append(path)
 public={str(ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd'):'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
         str(ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip'):'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 pins.update(public)
 ids=sorted({p[k]for p,f,s,v in processes for k in('pid','hostPID')})
 query="Get-CimInstance Win32_Process -Filter '"+' OR '.join(f'ProcessId={p}'for p in ids)+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 output=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(output)if output else[]
 if isinstance(jobs,dict):jobs=[jobs]
 for p,f,s,v in processes:
  need(not any(j['ProcessId']==p['pid']and j['Name']=='mkport_candidate.exe'and
               abs(j['createdUnix']-p['startedUnix'])<.1 and p['command'][-1]in(j['CommandLine']or'')for j in jobs),
       'Exact captured native PID/name/creation/script command is terminal; no timeout-based restart')
  if v==5964:
   started=datetime.datetime.fromisoformat(host_creation[f,s]).timestamp()
   need(not any(j['ProcessId']==p['hostPID']and j['Name']=='python.exe'and abs(j['createdUnix']-started)<.1 and
                'run_current_pit_queue_rng_v5961.py'in(j['CommandLine']or'')and f'--fighter {f} --side {s}'in(j['CommandLine']or'')for j in jobs),
        'Exact captured corrected Python host identity and command is terminal')
  else:
   need(not any(j['ProcessId']==p['hostPID']and j['Name']=='python.exe'and 'run_current_pit_queue_rng_v5956.py'in(j['CommandLine']or'')for j in jobs),
        'Terminal failed Python host not running')
 current.expected();need(all(sha(p)==h for p,h in pins.items()),'Every compiled/current/user-dirty/executed/failed/native/public/proof byte intact')
 sealed=list(dict.fromkeys(p.resolve()for p in sealed));before=sum(allocated(p)for p in sealed)
 for path in sealed:
  digest=sha(path);done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True)
  need(done.returncode==0 and sha(path)==digest,'Exact bounded completed text losslessly compressed; no copies')
 after=sum(allocated(p)for p in sealed)
 progress=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
               parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],cases=cases,retainedActualFailedBoots=failures,newInputHashes=pins,
               previousGoalTurnClassification='progress:5953 sealed four real stock8 opponent Pit audio/full-source-clock/ADSP/directMain140 cases; complete scope retained',
               thisGoalTurnClassification='progress: four corrected actual cold native seven-match runs qualify all4484 original RNG core words,80 full64bit bounded products/choices,32 sound selectors and72 directly observed empty/replacement queue decisions.144 actual new native/source faults pass with every original audio/state/direct-owner/raw/source suite retained and unchanged whole stereo output. Four frame0 missing-deadline boot failures and one invalid callback-label-only post-gate assumption are preserved; corrected successors pass without guest/build changes. All original five groups remain active.',
               actualNativeCoreCalls=4484,actualBoundedRNGCalls=80,actualSoundVariantSelectors=32,actualObservedSlotDecisions=72,
               actualNativeRNGPriorityFaultsRejected=144,actualAudioSourceWindowFaultsRejected=116,actualEarnedStateFaultsRejected=48,
               actualDirectNativeOwnerFaultsRejected=104,actualRawMixedPCMFaultsRejected=16,actualMixedSourceOperationFaultsRejected=16,
               exactStereoPCMFrames=3863040,allObservedNativeRNGWordsAndChoicesAccepted=True,
               allObservedEmptyReplacementSlotDecisionsAccepted=True,actualWholeMixedPCMUnchangedUnderAdditionalPassiveObserver=True,
               nativeSuppressionBranchAccepted=False,nativeSpecial71BranchAccepted=False,allNativePitCuePriorityAndRNGAccepted=False,
               stockVictimRGBAccepted=False,completeStageVictimAudioAccepted=False,allVictimsArenasMovesCPURepeatedFinishersAccepted=False,
               fullPortAcceptance=False,newNativeBoots=8,successfulNativeBoots=4,failedBeforeGameplayNativeBoots=4,
               newBuilds=0,newRawRecordings=0,newDeletedFiles=0,publicPlayableChanged=False,publicZIPChanged=False,
               exactCapturedNativeProcessesStillLive=[],observedOtherOrReusedPIDs=jobs,
               consumedNativeCaptureSessions=[80581,18766,11408,89924,85783,25476,20417,32548],
               consumedQualifierSessions=[85241,6647,32616],sealedTextFiles=len(sealed),sealedAllocatedBytesBefore=before,
               sealedAllocatedBytesAfter=after,sealedAllocatedBytesReclaimed=before-after,
               next='Continue actual broader native Pit/Tomb victim/cinematic/effect/audio integration and naturally exercised remaining suppression/special71/voice-variant paths; do not inject queue/RNG state or rerun these accepted finite contexts merely for status. Preserve every remaining move/arena/CPU/KO/overlap, other finisher/victim/morph/secret/cinematic, already verified natural campaigns/own endings, final selection/ladder/names/audio/dependency cleanup and matching refreshed release ZIP. No permanently retired raw/build/source-tree regeneration.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(progress,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,'Additive whole-scope journal losslessly sealed')
 print(json.dumps({k:v for k,v in progress.items()if k not in('newInputHashes','remaining','cases','retainedActualFailedBoots')},indent=2),flush=True)

if __name__=='__main__':run()
