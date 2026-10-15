"""Seal four real opposite-character Tomb cases; retain complete goal and storage policy."""
import ctypes,datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5845_current_cross_tomb_enabled_audio_progress'

def allocated(path):
 high=ctypes.c_uint32()
 api=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
 api.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32));api.restype=ctypes.c_uint32
 ctypes.set_last_error(0);low=api(str(path),ctypes.byref(high))
 need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual Windows allocated file size '+str(path))
 return low+(high.value<<32)

def run():
 need(not OUT.exists(),'Fresh immutable real cross-character checkpoint')
 current.expected()
 parentpath=ROOT/'audit_v5832_current_pressed_tomb_full_scene_matrix_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and
  parent['actualCurrentHeldPressedAndRandomMirrorFullScenesRetained'],'Whole previous full-scope progress remains intact')
 pins=dict(parent['newInputHashes']);pins[str(parentpath)]=sha(parentpath)
 reportpath=ROOT/'audit_v5843_current_cross_tomb_audio_checked/report.json'
 report=json.loads(reportpath.read_text())
 need(report['passed']and report['candidate']==current.NAME and len(report['cases'])==4 and
  report['actualCurrentBothCharactersBothSidesOppositeTombEnabledWinnerMixAccepted']and
  report['exactStereoPCMFrames']==3863040 and report['actualSourceAudioFaultsRejected']==132 and
  report['actualEarnedStateFaultsRejected']==48 and report['actualOriginalNativeBranchFaultsRejected']==16 and
  report['actualBranchFaultsRejected']==8 and report['actualLateVictimVoiceFaultsRejected']==16 and
  report['actualRawMixedPCMFaultsRejected']==16 and report['actualMixedSourceOperationFaultsRejected']==16 and
  report['actualNativeHeldContexts']==2 and report['actualNativeRandomDropContexts']==2 and
  not report['pairedNOSAMPLESRunAccepted']and not report['actualSavedGainSnapshotsAvailable']and
  not report['fullStageArtAccepted']and not report['completeStageVictimAudioAccepted']and not report['fullPortAcceptance'],
  'Actual complete four-case cross earned/state/window/channel/PCM/source/voice matrix, no inferred missing contexts')
 for p,h in report['inputHashes'].items():
  need(p not in pins or pins[p]==h,'Consistent immutable whole source/evidence pins');pins[p]=h
 pins[str(reportpath)]=sha(reportpath)
 processes=[];cases=[];sealed=[reportpath]
 for case in report['cases']:
  folder=Path(case['capture']);meta=json.loads((folder/'result.json').read_text())
  live=json.loads((folder/'audio_live_source_model.json').read_text())
  prediction=json.loads((folder/'mixed_waveform_prediction.json').read_text())
  process=json.loads((folder/'process.json').read_text());processes.append(process)
  branch=case['sourceQualifiedNativeBranch'];falling=branch['nativeDrop']
  channels=case['actualWinnerChannelClockAndRetirement'];wave=live['waveform']
  identity=17 if case['fighter']=='kano'else 18;victim=18 if identity==17 else 17
  need(case['actualCurrentOppositeCharacterTombEnabledAudioAccepted']and case['identity']==identity and
   case['victimIdentity']==branch['trueVictim']==victim and branch==live['sourceQualifiedNativeBranch']and
   meta['exit_code']==0 and meta['guestSHA256']==current.GUEST_SHA and meta['guest_writes']==0 and
   meta['assistance']=='none'and meta['samples_enabled']and meta['executable_sha256']==current.EXE_SHA and
   meta['payload_sha256']==current.PAYLOAD_SHA and len(case['actualAudioSourceWindowFaultsRejected'])==33 and
   len(case['actualOriginalNativeBranchFaultsRejected'])==4 and len(case['actualNativeBranchFaultsRejected'])==(4 if falling else 0)and
   len(case['actualLateVictimVoiceFaultsRejected'])==(8 if falling else 0)and channels['passed']and
   channels['preciseSourceChannelStates']==14084 and channels['videoChannelStates']==15400 and
   channels['consecutiveActiveCallbacks']==100 and channels['allRepeatedDoublePositionBitsExact']and
   channels['allOtherChannelsIdle']and channels['fullNativeRetirementAccepted']and
   case['actualGeneralCueSourceProof']['actualGeneralCalls']==(12 if falling else 21)and
   prediction==wave and wave['passed']and wave['comparedStereoFrames']==965760 and
   wave['differentChannelSamples']==0 and wave['actualSHA256']==wave['predictedSHA256']==meta['mixedPCMSHA256']and
   wave['actualMixedRawPCMByteFaultSuiteAccepted']and len(wave['actualRawMixedPCMFaultsRejected'])==4 and
   len(wave['actualMixedSourceOperationFaultsRejected'])==4 and
   wave['sourceSelectedWinnerSample']==(2 if identity==17 else 3)and
   wave['sourceWinnerLength']==32000 and wave['sourceWinnerFrequency']==16000 and
   wave['sourceFloat32CompositeGain']==0.21000000834465027 and wave['maximumMixedMagnitude']<1 and
   live['nativeEarnedTombState']['earned_matches']==2 and live['nativeEarnedTombState']['consecutive_fields']==801 and
   len(live['actualEarnedStateFaultsRejected'])==12 and len(live['actualDACFaultsRejected'])==4 and
   len(live['actualSoundROMFaultsRejected'])==8 and len(wave['actualCallbackSourceClocks'])==1006 and
   '-samples'in process['command']and '-nosamples'not in process['command']and '-nocheat'in process['command']and
   (folder/'stderr.log').read_text()==''and not(folder/'audio_failure.json').exists(),
   'Every complete actual native terminal/input/identity/voice/channel/state/waveform proof intact')
  if falling:
   need(branch['nativeMotion']['phase']['checkedConsecutiveCallbacks']==269 and
    live['sourceQualifiedNativeLateVictimVoice']['passed'],'Actual natural269phase and role/female late voice')
  else:need(live['sourceQualifiedNativeLateVictimVoice']is None,'No phantom late voice in held branch')
  for p,h in live['mixedWaveformSourceInputHashes'].items():need(sha(p)==h,'Exact winner source preserved');pins[p]=h
  for p in folder.rglob('*'):
   if not p.is_file():continue
   need(p.suffix.lower()not in('.png','.wav','.bin','.pcm','.rgb','.exe','.zip','.mdata'),
    'No raw recordings or duplicate game builds in actual current capture')
   pins[str(p.resolve())]=sha(p)
   if p.suffix.lower()in('.json','.log','.txt'):sealed.append(p)
  cases.append(dict(fighter=case['fighter'],physicalSlot=case['physicalSlot'],identity=identity,victimIdentity=victim,
   capture=str(folder),nativeDrop=falling,actualNativeRandomValue=branch['actualNativeRandomValue'],
   nativeOrigin=case['origin'],nativeTerminal=case['terminal'],retiredFrame=branch['retiredFrame'],
   exactStereoPCMFrames=965760,actualSourceWindowChannelFaultsRejected=33,
   initialVictimVoice=case['sourceSelectedInitialVictimVoice'],actualVictimRole=case['actualVictimRole']))
 pids=sorted({p[k]for p in processes for k in('pid','hostPID')})
 query="Get-CimInstance Win32_Process -Filter '"+' OR '.join(f'ProcessId={p}'for p in pids)+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 output=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(output)if output else []
 if isinstance(jobs,dict):jobs=[jobs]
 for p in processes:
  need(not any(j['ProcessId']==p['pid']and j['Name']=='mkport_candidate.exe'and
   'mk2ks_current_cross_tomb_campaign_v5835.lua'in(j['CommandLine']or'')and
   abs(j['createdUnix']-p['startedUnix'])<.10 for j in jobs),'Every exact captured native job is terminal')
  need(not any(j['ProcessId']==p['hostPID']and j['Name']=='python.exe'and
   'run_current_cross_tomb_audio_v5838.py'in(j['CommandLine']or'')for j in jobs),'All exact RAM capture/model hosts terminal')
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 need(all(sha(p)==h for p,h in public.items()),'Public playable and release untouched until final acceptance')
 pins.update({str(p.resolve()):h for p,h in public.items()})
 sources=[ROOT/name for name in('mk2ks_current_cross_tomb_driver_v5833.lua',
  'mk2ks_current_cross_tomb_provenance_v5834.lua','mk2ks_current_cross_tomb_campaign_v5835.lua',
  'tools/current_cross_tomb_state_v5836.py','tools/current_cross_tomb_branches_v5837.py',
  'tools/run_current_cross_tomb_audio_v5838.py','tools/qualify_current_cross_tomb_audio_v5839.py',
  'tools/verify_current_cross_tomb_audio_v5842.py','audit_v5840_current_cross_tomb_audio_source_checked/report.json')]+[Path(__file__)]
 for p in sources:pins[str(p.resolve())]=sha(p);sealed.append(p)
 current.expected();need(all(sha(p)==h for p,h in pins.items()),'Every current/source/previous/new evidence byte unchanged')
 sealed=list(dict.fromkeys(p.resolve()for p in sealed));before={str(p):sha(p)for p in sealed}
 before_allocated=sum(allocated(p)for p in sealed)
 for p in sealed:
  need(p.is_relative_to(ROOT.resolve()),'Exact sealed text files within named working folder')
  need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0,
   'Lossless compact bounded text, no new recovery archive')
 need(all(sha(p)==h for p,h in before.items()),'All complete sealed source/evidence bytes preserved')
 after_allocated=sum(allocated(p)for p in sealed)
 progress=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  parentAdditiveJournal=str(parentpath),remaining=parent['remaining'],nativePhaseProof=str(reportpath),cases=cases,
  previousGoalTurnClassification='no progress: intervening acknowledgement only; current mirror checkpoint and sources revalidated before new actual tests',
  thisGoalTurnClassification='progress: four ordinary current Kano-versus-Sonya native Tomb captures completed, actual player-one random drops and player-two held branches. Whole cross earned/identity/action/801cleanup, native PC/IO/actor/Main/RNG/motion, initial and actual late victim voice, original general producers/queues, every precise channel, native DAC/ROM and full source-exact enabled mixed audio qualified.132actual window/channel/RNG faults plus complete original earned/phase/voice and raw PCM/source-operation faults reject. Original wider goal remains active.',
  actualCurrentBothCharactersBothSlotsOppositeTombEnabledAudioAccepted=True,
  actualObservedUnpressedCrossContexts=4,actualHeldCrossContexts=2,actualRandomDropCrossContexts=2,
  allCurrentCrossHeldPressedRandomContextsAccepted=False,
  exactStereoPCMFrames=3863040,actualSourceWindowChannelFaultsRejected=132,actualEarnedStateFaultsRejected=48,
  actualOriginalNativeBranchFaultsRejected=16,actualNativeDropPhaseFaultsRejected=8,actualLateVictimVoiceFaultsRejected=16,
  actualRawMixedPCMFaultsRejected=16,actualMixedSourceOperationFaultsRejected=16,
  allPriorMirrorHeldPressedRandomFullScenesRetained=True,pairedNOSAMPLESCrossContextsAccepted=False,
  actualSavedGainSnapshotsAvailable=False,broaderPitTombVictimBranchStageArtAccepted=False,
  completeStageVictimAudioAccepted=False,fullMovePhaseAllArenaCPURepeatedKOOverlapAccepted=False,
  allCinematicsAndIndependentStockChoreographyAccepted=False,fullPortAcceptance=False,
  exactCaptureProcessesStillLive=[],observedOtherOrReusedPIDs=jobs,
  consumedCaptureToolSessions=[35686,35359,19246,67771],consumedMatrixToolSessions=[80852],
  rawGuestRGBPCMFilesWritten=0,newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,publicZIPChanged=False,
  sealedTextSourcesLosslesslyCompacted=len(sealed),sealedAllocatedBytesBefore=before_allocated,
  sealedAllocatedBytesAfter=after_allocated,sealedAllocatedBytesReclaimed=before_allocated-after_allocated,
  newInputHashes=pins,
  next='Use these actual opposite-character audio/branch records for full native Tomb scene/ground/floor-shadow/cleanup verification. Remaining opposite held/random slots and pressed combinations, broader Pit/Tomb stock victims, source priority/RNG choice and independent choreography remain open. Retain all original arena/move/CPU/repeated/KO/overlap, other finisher/victim/morph/secret/cinematic/campaign/ending, final UI/names/audio integration and refreshed release ZIP requirements. Do not replay completed mirror matrices for status or regenerate permanently retired builds/raw history.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(progress,indent=2)+'\n')
 digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and
  sha(path)==digest,'Full additive checkpoint compacted without content changes')
 print(json.dumps({k:v for k,v in progress.items()if k not in('cases','remaining','newInputHashes')},indent=2),flush=True)

if __name__=='__main__':run()
