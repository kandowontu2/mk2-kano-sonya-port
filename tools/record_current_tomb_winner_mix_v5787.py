"""Seal actual enabled Tomb winner mixing; keep every original goal group."""
import datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5788_current_enabled_tomb_winner_mix_progress'


def run():
 need(not OUT.exists(),'Fresh immutable enabled-winner checkpoint')
 current.expected()
 parentpath=ROOT/'audit_v5777_current_tomb_native_audio_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and
  parent['actualCurrentBothSlotsHeldAndPressedNativeTombSoundAccepted']and
  parent['fullFourCaseEndingPixelsAndAudioRetained'],'Whole prior current stage, ending, move/UI/campaign evidence and full scope retained')
 pins=dict(parent['newInputHashes']);pins[str(parentpath)]=sha(parentpath)
 phasepath=ROOT/'audit_v5786_current_enabled_tomb_winner_mix_checked/report.json'
 phase=json.loads(phasepath.read_text())
 need(phase['passed']and phase['candidate']==current.NAME and
  phase['actualCurrentBothCharactersBothSidesHeldTombEnabledWinnerMixAccepted']and len(phase['cases'])==4 and
  phase['exactStereoPCMFrames']==3863040 and phase['samplesEnabled']and
  phase['importedWinnerMixedWaveformAccepted']and phase['actualSourceAudioFaultsRejected']==124 and
  phase['actualEarnedStateFaultsRejected']==48 and phase['actualBranchFaultsRejected']==16 and
  not phase['dropLateVictimVoiceAccepted']and not phase['fullStageArtAccepted']and
  not phase['completeStageVictimAudioAccepted']and not phase['fullPortAcceptance']and
  not phase['actualSavedGainSnapshotsAvailable']and not phase['actualMixedRawPCMByteFaultSuiteAccepted'],
  'Actual complete held four-context enabled stereo/channel/window/source faults, no pressed/drop/gain-snapshot/raw-byte-fault overclaim')
 for p,h in phase['inputHashes'].items():
  need(p not in pins or pins[p]==h,'Consistent exact current/source/evidence pins');pins[p]=h
 pins[str(phasepath)]=sha(phasepath);sealed=[phasepath];processes=[];cases=[]
 for case in phase['cases']:
  folder=Path(case['capture']);meta=json.loads((folder/'result.json').read_text())
  live=json.loads((folder/'audio_live_source_model.json').read_text())
  prediction=json.loads((folder/'mixed_waveform_prediction.json').read_text())
  process=json.loads((folder/'process.json').read_text());processes.append(process)
  channels=case['actualWinnerChannelClockAndRetirement'];wave=live['waveform']
  need(case['actualCurrentHeldTombEnabledWaveformVoiceClockAndCleanupAccepted']and
   len(case['actualAudioSourceWindowFaultsRejected'])==31 and len(case['actualNativeBranchFaultsRejected'])==4 and
   channels['passed']and channels['allRepeatedDoublePositionBitsExact']and channels['allOtherChannelsIdle']and
   channels['fullNativeRetirementAccepted']and channels['preciseSourceChannelStates']==14084 and
   channels['videoChannelStates']==15400 and channels['consecutiveActiveCallbacks']==100 and
   channels['sourceOutputSamples']==96001 and not channels['actualSavedGainSnapshotsAvailable']and
   case['actualGeneralCueSourceProof']['passed']and case['actualGeneralCueSourceProof']['actualGeneralCalls']==21,
   'Whole actual winner waveform/native initial voice and exact14channel start/position/retirement/idle tail, every source cue')
  need(meta['exit_code']==0 and meta['samples_enabled']and meta['fighter']==case['fighter']and
   meta['side']==case['physicalSlot']and meta['guestSHA256']==current.GUEST_SHA and
   meta['executable_sha256']==current.EXE_SHA and meta['payload_sha256']==current.PAYLOAD_SHA and
   live['passed']and live['samplesEnabled']and live['importedWinnerMixedWaveformAccepted']and
   prediction==wave and wave['passed']and wave['comparedStereoFrames']==965760 and
   wave['differentChannelSamples']==0 and wave['predictedSHA256']==wave['actualSHA256']==meta['mixedPCMSHA256']and
   wave['sourceWinnerFrequency']==16000 and wave['sourceWinnerLength']==32000 and
   wave['sourceFloat32CompositeGain']==0.21000000834465027 and wave['maximumMixedMagnitude']<1 and
   live['nativeEarnedTombState']['earned_matches']==2 and live['nativeEarnedTombState']['consecutive_fields']==801 and
   len(live['actualEarnedStateFaultsRejected'])==12 and len(live['actualDACFaultsRejected'])==4 and
   len(live['actualSoundROMFaultsRejected'])==8 and len(wave['actualCallbackSourceClocks'])==1006 and
   '-samples'in process['command']and '-nosamples'not in process['command']and '-nocheat'in process['command']and
   (folder/'stderr.log').read_text()==''and not(folder/'audio_failure.json').exists(),
   'Actual current native terminal, complete RAM float mixer equality and full earned/control/source/ROM/DAC gates')
  for p,h in live['mixedWaveformSourceInputHashes'].items():need(sha(p)==h,'Original actual winner source bytes intact');pins[p]=h
  for p in folder.rglob('*'):
   if not p.is_file():continue
   need(p.suffix.lower()not in ('.png','.wav','.bin','.pcm','.rgb','.exe','.zip'),
    'No raw native/source/media or duplicate game/release copies in current capture')
   pins[str(p.resolve())]=sha(p)
   if p.suffix.lower()in ('.json','.cfg','.log','.txt'):sealed.append(p)
  cases.append(dict(fighter=case['fighter'],physicalSlot=case['physicalSlot'],capture=str(folder),
   nativeExit=0,exactStereoPCMFrames=965760,preciseChannelStates=14084,videoChannelStates=15400,
   activeWinnerCallbacks=100,sourceWinnerSample=wave['sourceSelectedWinnerSample'],
   mixedWaveformSHA256=wave['actualSHA256'],sourceMarker=wave['sourceMarker'],
   actualSourceWindowChannelFaults=31,actualEarnedStateFaults=12,actualNativeBranchFaults=4))
 sources=[ROOT/'tools/current_tomb_winner_mix_model_v5778.py',
  ROOT/'mk2ks_current_tomb_winner_mix_observer_v5779.lua',ROOT/'mk2ks_current_tomb_winner_mix_campaign_v5780.lua',
  ROOT/'tools/run_current_tomb_winner_mix_v5781.py',ROOT/'tools/qualify_current_tomb_winner_mix_v5782.py',
  ROOT/'tools/verify_current_tomb_winner_mix_v5785.py',Path(__file__),
  ROOT/'audit_v5783_current_tomb_winner_mix_source_checked/report.json']
 for p in sources:pins[str(p.resolve())]=sha(p);sealed.append(p)
 pids=sorted({p[k]for p in processes for k in ('pid','hostPID')})
 query="Get-CimInstance Win32_Process -Filter '"+' OR '.join(f'ProcessId={p}'for p in pids)+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 output=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(output)if output else []
 if isinstance(jobs,dict):jobs=[jobs]
 for p in processes:
  need(not any(j['ProcessId']==p['pid']and j['Name']=='mkport_candidate.exe'and
   abs(j['createdUnix']-p['startedUnix'])<.05 and
   'mk2ks_current_tomb_winner_mix_campaign_v5780.lua'in (j['CommandLine']or'')for j in jobs),
   'Every exact captured native process is terminal; timeout never means terminal')
  need(not any(j['ProcessId']==p['hostPID']and j['Name']=='python.exe'and
   'run_current_tomb_winner_mix_v5781.py'in (j['CommandLine']or'')for j in jobs),'All exact RAM model/capture hosts terminal')
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 need(all(sha(p)==h for p,h in public.items()),'Public launcher/release ZIP unchanged before full acceptance')
 for p,h in public.items():pins[str(p.resolve())]=h
 current.expected();need(all(sha(p)==h for p,h in pins.items()),'All current, dirty-user-restoration, prior full-scope and native evidence intact')
 sealed=list(dict.fromkeys(p.resolve()for p in sealed));before={str(p):sha(p)for p in sealed}
 for p in sealed:
  need(p.is_relative_to(ROOT.resolve()),'Exact sealed text/source compression only')
  need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0,
   'Lossless bounded immutable text compression')
 need(all(sha(p)==h for p,h in before.items()),'Every full evidence/source byte unchanged')
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  parentAdditiveJournal=str(parentpath),remaining=parent['remaining'],nativePhaseProof=str(phasepath),cases=cases,
  previousGoalTurnClassification=parent['thisGoalTurnClassification'],
  thisGoalTurnClassification='progress: four actual current held Tomb campaigns completed with native sound and original winner samples enabled. Entire unquantized native resampler/cache plus original repeated-double sample interpolation/terminal fill, original stream clock and compiled float gains predict all3,863,040stereo frames exactly. Every14video and precise sound-callback channel state has true winner clip/bit-exact positions/finite retirement and idle tail.31actual source/window/channel faults per case, full earned/held branch/native cue and ROM/DAC faults retained. Full original goal scope stays intact.',
  actualCurrentBothCharactersBothSlotsHeldTombEnabledWinnerMixAccepted=True,exactStereoPCMFrames=3863040,
  preciseSourceChannelStates=56336,videoChannelStates=61600,actualSourceWindowChannelFaultsRejected=124,
  actualEarnedStateFaultsRejected=48,actualNativeHeldBranchFaultsRejected=16,
  effectiveGainSourceQualifiedAndWholeWaveformExact=True,actualSavedGainSnapshotsAvailable=False,
  actualMixedRawPCMByteFaultSuiteAccepted=False,pressedAndRandomDropEnabledWinnerMixAccepted=False,
  allPriorHeldPressedNativeAudioAndEndingPixelsAudioRetained=True,
  broaderPitTombVictimBranchStageArtAccepted=False,completeStageVictimAudioAccepted=False,
  allCinematicsAndIndependentStockChoreographyAccepted=False,fullPortAcceptance=False,
  exactCaptureProcessesStillLive=[],observedOtherOrReusedPIDs=jobs,
  consumedCaptureToolSessions=[24097,62727,40197,19838],consumedPhaseToolSessions=[93866],
  rawGuestRGBPCMFilesWritten=0,newBuilds=0,newDeletedFiles=0,
  publicPlayableChanged=False,publicZIPChanged=False,sealedTextSourcesLosslesslyCompacted=len(sealed),
  newInputHashes=pins,
  next='Do not replay these four completed held enabled-mix campaigns just for status. Continue current pressed/natural random-drop enabled mix and broader native Pit/Tomb victim/branch art/shadow/audio fidelity; strengthen mixed raw-byte fault coverage where a real new capture provides RAM buffers. Retain completed own-ending/campaign/move/UI proofs while finishing all original wider arena/CPU/repeated/KO/overlap, other finisher/victim/morph/secret/cinematic and stock choreography requirements. Final combined selection/ladder/names/audio regression, dependency-aware obsolete-folder cleanup and matching refreshed release ZIP remain required.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(report,indent=2)+'\n')
 digest=sha(path);need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
  'New full-scope checkpoint losslessly compacted')
 print(json.dumps({k:v for k,v in report.items()if k not in ('remaining','newInputHashes','cases')},indent=2),flush=True)


if __name__=='__main__':run()
