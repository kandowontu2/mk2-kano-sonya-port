"""Seal current whole Pit waveform evidence without claiming cinematic audio."""
import datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
from record_current_cross_tomb_audio_v5844 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5901_current_cross_pit_audio_progress'

def run():
 need(not OUT.exists(),'Fresh additive current Pit progress')
 current.expected()
 parentpath=ROOT/'audit_v5890_current_cross_tomb_timing_full_scene_matrix_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed'] and parent['goalStatus']=='active' and len(parent['remaining'])==5,
      'All original goal groups and retained finite Tomb scenes remain intact')
 # Retain the entire previous journal by its own immutable digest. Do not
 # reconstruct permanently retired captures to satisfy obsolete inventories.
 pins={str(parentpath):sha(parentpath),str(Path(__file__).resolve()):sha(__file__)}
 matrixpath=ROOT/'audit_v5899_current_cross_pit_winner_mix_checked/report.json'
 matrix=json.loads(matrixpath.read_text())
 need(matrix['passed'] and matrix['candidate']==current.NAME and len(matrix['cases'])==4 and
      matrix['actualCurrentBothCharactersBothSidesPitEnabledWinnerMixAccepted'] and
      matrix['exactStereoPCMFrames']==3863040 and matrix['actualSourceAudioFaultsRejected']==116 and
      matrix['actualEarnedStateFaultsRejected']==48 and matrix['actualRawMixedPCMFaultsRejected']==16 and
      matrix['actualMixedSourceOperationFaultsRejected']==16 and matrix['actualMixedRawPCMByteFaultSuiteAccepted'] and
      not matrix['cinematicVictimAudioOwnershipAccepted'] and not matrix['allNativePitCuePriorityAndRNGAccepted'] and
      not matrix['fullStageArtAccepted'] and not matrix['completeStageVictimAudioAccepted'] and
      not matrix['fullPortAcceptance'],'Whole exact Pit mixer/window/packet proof, no cinematic/audio scope inflation')
 for p,h in matrix['inputHashes'].items():need(sha(p)==h,'Immutable actual full Pit audio input '+p);pins[p]=h
 pins[str(matrixpath)]=sha(matrixpath)
 cases=[];processes=[];sealed=[matrixpath,Path(__file__).resolve()]
 for case in matrix['cases']:
  folder=Path(case['capture']);meta=json.loads((folder/'result.json').read_text())
  live=json.loads((folder/'audio_live_source_model.json').read_text())
  wave=live['waveform'];channels=case['actualWinnerChannelClockAndRetirement']
  process=json.loads((folder/'process.json').read_text());processes.append(process)
  need(case['passed'] and case['actualCurrentPitEnabledWaveformClockAndCleanupAccepted'] and
       meta['exit_code']==0 and meta['guestSHA256']==current.GUEST_SHA and
       meta['executable_sha256']==current.EXE_SHA and meta['payload_sha256']==current.PAYLOAD_SHA and
       meta['samples_enabled'] and meta['guest_writes']==0 and meta['assistance']=='none' and
       live['nativeEarnedPitState']==case['nativePitPhysicalState'] and
       live['nativeEarnedPitState']['earned_matches']==7 and live['nativeEarnedPitState']['consecutive_fields']==801 and
       len(case['actualAudioSourceWindowFaultsRejected'])==29 and len(case['actualEarnedStateFaultsRejected'])==12 and
       len(live['actualDACFaultsRejected'])==4 and len(live['actualSoundROMFaultsRejected'])==8 and
       channels['passed'] and channels['preciseSourceChannelStates']==14084 and
       channels['videoChannelStates']==15400 and channels['consecutiveActiveCallbacks']==100 and
       channels['allRepeatedDoublePositionBitsExact'] and channels['allOtherChannelsIdle'] and channels['fullNativeRetirementAccepted'] and
       wave==json.loads((folder/'mixed_waveform_prediction.json').read_text()) and wave['passed'] and
       wave['comparedStereoFrames']==965760 and wave['differentChannelSamples']==0 and
       wave['actualSHA256']==wave['predictedSHA256']==meta['mixedPCMSHA256'] and
       len(wave['actualRawMixedPCMFaultsRejected'])==len(wave['actualMixedSourceOperationFaultsRejected'])==4 and
       wave['sourceWinnerLength']==32000 and wave['sourceWinnerFrequency']==16000 and
       wave['sourceFloat32CompositeGain']==0.21000000834465027 and wave['maximumMixedMagnitude']<1 and
       len(wave['actualCallbackSourceClocks'])==1006 and '-samples'in process['command'] and
       '-nocheat'in process['command'] and '-nosamples'not in process['command'] and
       not (folder/'audio_failure.json').exists() and (folder/'stderr.log').read_text()=='',
       'Every actual whole PCM/DAC/ROM/channel/physical terminal and source-fault proof retained')
  for p in folder.rglob('*'):
   if not p.is_file():continue
   need(p.suffix.lower()not in ('.png','.wav','.bin','.pcm','.rgb','.exe','.zip','.mdata'),
        'No raw recording or duplicate build created by current Pit audio')
   pins[str(p)]=sha(p)
   if p.suffix.lower()in ('.json','.log','.txt'):sealed.append(p)
  cases.append(dict(fighter=case['fighter'],physicalSlot=case['physicalSlot'],origin=case['origin'],
                    terminal=case['terminal'],exactStereoPCMFrames=965760,wholePCMSHA256=wave['actualSHA256'],
                    earnedMatches=7,actualSourceWindowFaultsRejected=29,cinematicVictimAudioOwnershipAccepted=False))
 pids=sorted({p[k]for p in processes for k in ('pid','hostPID')}|{150256})
 query="Get-CimInstance Win32_Process -Filter '"+' OR '.join(f'ProcessId={p}'for p in pids)+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 answer=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(answer)if answer else []
 if isinstance(jobs,dict):jobs=[jobs]
 for p in processes:
  need(not any(j['ProcessId']==p['pid'] and j['Name']=='mkport_candidate.exe' and
               'mk2ks_current_pit_winner_mix_campaign_v5892.lua'in(j['CommandLine']or'') and
               abs(j['createdUnix']-p['startedUnix'])<.1 for j in jobs),'Exact native audio job terminal')
  need(not any(j['ProcessId']==p['hostPID'] and j['Name']=='python.exe' and
               'run_current_cross_pit_winner_mix_v5894.py'in(j['CommandLine']or'')for j in jobs),
       'Exact audio capture host terminal')
 need(not any(j['ProcessId']==150256 and j['Name']=='python.exe' and
              'verify_current_cross_pit_winner_mix_v5898.py'in(j['CommandLine']or'')for j in jobs),
      'Independently consumed actual audio matrix is terminal')
 for path,h in {
  ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
 }.items():need(sha(path)==h,'Public launcher/release unchanged');pins[str(path)]=h
 sealed=list(dict.fromkeys(p.resolve()for p in sealed));before=sum(allocated(p)for p in sealed)
 for p in sealed:
  need(p.is_relative_to(ROOT),'Exact sealed text stays in requested working folder')
  need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0,
       'Lossless bounded sealed text compression')
 need(all(sha(p)==h for p,h in pins.items()),'Whole executed/source/public evidence bytes unchanged')
 after=sum(allocated(p)for p in sealed)
 progress=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  parentAdditiveJournal=str(parentpath),remaining=parent['remaining'],nativeAudioProof=str(matrixpath),cases=cases,
  previousGoalTurnClassification='progress: four actual current native cross Pit enabled-audio captures completed; full independent matrix was compiled, not yet executed',
  thisGoalTurnClassification='progress: independent full current Pit source waveform/window/channel/packet/port/ADSP and physical cleanup matrix executed and passed. All3,863,040actual stereo frames exact,116actualwindow48earned16rawPCM16source-operation faults reject. Cinematic ancestry, full render and native cue/priority/RNG source semantics remain separate open work; no broader-port acceptance.',
  actualCurrentBothCharactersBothSlotsPitWholeMixedAudioAccepted=True,exactStereoPCMFrames=3863040,
  actualSourceWindowChannelFaultsRejected=116,actualEarnedStateFaultsRejected=48,
  actualRawMixedPCMFaultsRejected=16,actualMixedSourceOperationFaultsRejected=16,
  cinematicVictimAudioOwnershipAccepted=False,allNativePitCuePriorityAndRNGAccepted=False,
  completeStageVictimAudioAccepted=False,fullStageArtAccepted=False,fullPortAcceptance=False,
  priorAll12CrossTombFullScenesAndAudioRetained=True,exactCaptureProcessesStillLive=[],observedOtherOrReusedPIDs=jobs,
  consumedCaptureToolSessions=[78476,10901,22198,40929],consumedMatrixToolSessions=[66249],
  rawGuestRGBPCMFilesWritten=0,newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,publicZIPChanged=False,
  sealedTextSourcesLosslesslyCompacted=len(sealed),sealedAllocatedBytesBefore=before,sealedAllocatedBytesAfter=after,
  sealedAllocatedBytesReclaimed=before-after,newInputHashes=pins,
  next='Complete actual current Pit cinematic Main+140 identity/ancestry, full original fall/impact/constructor/cache/palette/projection/shake/voice/exit and whole one-base CPU/DMA/shift/VRAM/RGB/shadow/retirement+30 scenes. Retain broader stock victim/mirror/native cue source and independent choreography, all original move/arena/CPU/repeated/KO/overlap/finishers/morph/secret/campaign/ending/UI/audio requirements and final refreshed release ZIP. Never recreate permanently retired raw/build history.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(progress,indent=2)+'\n')
 digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
      'Complete additive progress losslessly compacted')
 print(json.dumps({k:v for k,v in progress.items()if k not in ('cases','remaining','newInputHashes')},indent=2),flush=True)

if __name__=='__main__':run()
