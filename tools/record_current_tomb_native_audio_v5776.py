"""Seal current held/pressed Tomb audio, preserving the complete original goal."""
import ctypes,datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5777_current_tomb_native_audio_progress'


def run():
 need(not OUT.exists(),'Fresh immutable current stage audio receipt')
 current.expected()
 parentpath=ROOT/'audit_v5747_current_four_case_ending_audio_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and
  parent['actualCurrentFourCaseEndingSourceClockAudioAccepted']and len(parent['remaining'])==5,
  'Full original scope and completed four-case own-ending audio/video proof retained')
 pins=dict(parent['inputHashes']);pins[str(parentpath)]=sha(parentpath)
 processes=[];sealed=[];cases=[];matrices=[]
 for pressed,version,capture,key in [
  (False,5756,5754,'actualCurrentBothCharactersBothSidesHeldTombNativeDCSAudioAccepted'),
  (True,5769,5765,'actualCurrentBothCharactersBothSidesPressedTombNativeDCSAudioAccepted')]:
  path=ROOT/(f'audit_v{version}_current_'+('pressed_'if pressed else'')+'tomb_native_source_audio_matrix_checked/report.json')
  matrix=json.loads(path.read_text())
  need(matrix['passed']and matrix[key]and matrix['candidate']==current.NAME and len(matrix['cases'])==4 and
   matrix['exactStereoPCMFrames']==3863040 and matrix['actualSourceAudioFaultsRejected']==76 and
   matrix['actualEarnedStateFaultsRejected']==48 and matrix['actualBranchFaultsRejected']==16 and
   not matrix['samplesEnabled']and not matrix['importedWinnerMixedWaveformAccepted']and
   not matrix['fullStageArtAccepted']and not matrix['completeStageVictimAudioAccepted']and
   not matrix['fullPortAcceptance'],'Whole actual finite current audio matrix and honest remaining scope')
  if pressed:need(matrix['dropLateVictimVoiceAccepted']and matrix['actualLateVictimVoiceFaultsRejected']==32,
   'Actual original source-selected late victim voice in both physical slots, eight actual faults each')
  else:need(not matrix['dropLateVictimVoiceAccepted'],'Held branch does not claim any falling scream')
  for p,h in matrix['inputHashes'].items():
   need(p not in pins or pins[p]==h,'Consistent entire native/source/evidence bytes');pins[p]=h
  pins[str(path)]=sha(path);sealed.append(path);matrices.append(str(path))
  for case in matrix['cases']:
   folder=Path(case['capture']);process=json.loads((folder/'process.json').read_text())
   meta=json.loads((folder/'result.json').read_text());live=json.loads((folder/'audio_live_source_model.json').read_text())
   need(folder.resolve().is_relative_to(ROOT.resolve())and
    meta['exit_code']==0 and meta['candidate']==current.NAME and meta['guestSHA256']==current.GUEST_SHA and
    meta['executable_sha256']==current.EXE_SHA and meta['payload_sha256']==current.PAYLOAD_SHA and
    not meta['samples_enabled']and '-nosamples'in process['command']and '-nocheat'in process['command']and
    live['passed']and live['waveform']['differentChannelSamples']==0 and
    live['waveform']['comparedStereoFrames']==965760 and
    live['nativeEarnedTombState']['earned_matches']==2 and live['nativeEarnedTombState']['consecutive_fields']==801 and
    len(live['actualEarnedStateFaultsRejected'])==12 and len(live['actualDACFaultsRejected'])==4 and
    len(live['actualSoundROMFaultsRejected'])==8 and
    len(live['waveform']['effectiveActualWholeWaveformFaults'])==4 and
    (folder/'stderr.log').read_text()==''and not(folder/'audio_failure.json').exists(),
    'Actual native normal terminal, full source-clock waveform, two earned matches and original cleanup/fault gates')
   files=[p for p in folder.rglob('*')if p.is_file()]
   need(not any(p.suffix.lower()in ('.png','.bin','.wav','.pcm','.rgb','.exe','.zip')for p in files),
    'No native fallback PNG, raw source/media or duplicate build/release files')
   need(meta['rawAudioRasterVRAMROMCopiesWritten']==0 and meta['guest_writes']==0 and meta['assistance']=='none',
    'True-ID physical controls and read-only observer, no game-state assistance')
   for p in files:
    pins[str(p.resolve())]=sha(p)
    if p.suffix.lower()in ('.json','.cfg','.log','.txt'):sealed.append(p)
   processes.append(process)
   cases.append(dict(fighter=case['fighter'],physicalSlot=case['physicalSlot'],branch='pressed'if pressed else'held',
    capture=str(folder),nativeExit=0,exactStereoPCMFrames=965760,actualAudioSourceFaults=19,
    actualEarnedFaults=12,actualBranchFaults=4,actualLateVoiceFaults=8 if pressed else 0,
    nativePCMCallbacks=case['actualPCMCallbacks'],nativeChannelStates=case['actualChannelStates'],
    actualNativePackets=case['actualCompletePackets'],actualPortStores=case['actualFull16BitPortStores'],
    actualADSPReads=case['actualNativeADSPReads']))
 cuepath=ROOT/'audit_v5775_current_tomb_native_cue_source_checked/report.json'
 cues=json.loads(cuepath.read_text())
 need(cues['passed']and len(cues['cases'])==8 and cues['actualGeneralProducerCalls']==132 and
  cues['actualCueSourceFaultsRejected']==180 and cues['allCapturedGeneralCueProducersSourceAccounted']and
  cues['allEmittedGeneralQueueWordsSourceExact']and
  not cues['nativePriorityChoiceAndSuppressionAccepted']and not cues['actualRNGVariantChoiceAccepted']and
  not cues['announcerAndDirectProducersAccepted'],
  'Every actual general cue producer and emitted queue word source bound; no unobserved pre-call priority/RNG or announcer claim')
 for p,h in cues['inputHashes'].items():
  need(p not in pins or pins[p]==h,'Entire current cue/native matrix consistency');pins[p]=h
 pins[str(cuepath)]=sha(cuepath);sealed.append(cuepath)
 # Preserve genuine harness failures; none is concealed as a successful gate.
 failures=[]
 for version,fragment in [(5767,'actualSourceFaultsRejected'),(5771,'WindowsPath'),(5773,'wrong ceiling voice source base')]:
  suffix='current_pressed_tomb_native_source_audio_matrix_checked'if version==5767 else 'current_tomb_native_cue_source_checked'
  path=ROOT/f'audit_v{version}_{suffix}/report.json';failed=json.loads(path.read_text())
  need(not failed['passed']and fragment in failed['error'],'Genuine original checker failure retained')
  pins[str(path)]=sha(path);sealed.append(path);failures.append(dict(path=str(path),error=failed['error']))
 source_names=['current_tomb_source_audio_model_v5748.py','run_current_tomb_source_audio_v5749.py',
  'qualify_current_tomb_source_audio_v5752.py','verify_current_tomb_source_audio_v5755.py',
  'run_current_pressed_tomb_audio_v5758.py','qualify_current_pressed_tomb_audio_v5759.py',
  'qualify_current_pressed_tomb_audio_v5762.py','run_current_pressed_tomb_audio_v5764.py',
  'verify_current_pressed_tomb_audio_v5766.py','verify_current_pressed_tomb_audio_v5768.py',
  'verify_current_tomb_cue_sources_v5770.py','verify_current_tomb_cue_sources_v5772.py',
  'verify_current_tomb_cue_sources_v5774.py']
 sources=[ROOT/'tools'/n for n in source_names]+[Path(__file__),ROOT/'mk2ks_current_tomb_source_audio_observer_v5750.lua',
  ROOT/'mk2ks_current_tomb_source_audio_campaign_v5751.lua',ROOT/'mk2ks_current_pressed_tomb_source_audio_v5757.lua']
 for p in sources:pins[str(p.resolve())]=sha(p);sealed.append(p)
 # All native and model-host handles were consumed; re-used PIDs cannot imply
 # that an old exact executable/control/creation-time combination remains live.
 pids=sorted({p[k]for p in processes for k in ('pid','hostPID')})
 query="Get-CimInstance Win32_Process -Filter '"+' OR '.join(f'ProcessId={p}'for p in pids)+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 output=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(output)if output else []
 if isinstance(jobs,dict):jobs=[jobs]
 for p in processes:
  need(not any(j['ProcessId']==p['pid']and j['Name']=='mkport_candidate.exe'and
   abs(j['createdUnix']-p['startedUnix'])<.05 and
   Path(p['command'][-1]).name in (j['CommandLine']or'')for j in jobs),'Every exact native capture is terminal now')
  need(not any(j['ProcessId']==p['hostPID']and j['Name']=='python.exe'and
   Path(p['hostSource']).name in (j['CommandLine']or'')for j in jobs),'Every exact native audio/model host is terminal now')
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 need(all(sha(p)==h for p,h in public.items()),'Public CMD and release ZIP unchanged until full acceptance')
 for p,h in public.items():pins[str(p.resolve())]=h
 current.expected();need(all(sha(p)==h for p,h in pins.items()),'Every full current/prior/native/cue/harness/public input intact')
 sealed=list(dict.fromkeys(p.resolve()for p in sealed))
 before={str(p):sha(p)for p in sealed}
 for p in sealed:
  need(p.is_relative_to(ROOT.resolve()),'Exact bounded sealed text compression target')
  need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0,
   'Losslessly compact sealed native text/source only')
 need(all(sha(p)==h for p,h in before.items()),'No evidence byte changed by text compression')
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  parentAdditiveJournal=str(parentpath),remaining=parent['remaining'],
  previousGoalTurnClassification='progress: qualified current full earned Tomb observer; all four held native captures and RAM waveform proofs completed, with exact matrix verifier still running',
  thisGoalTurnClassification='progress: terminal held four-case matrix accepted; four current both-Down Tomb campaigns earned naturally and completed. Native128hold/112descent/fall/landing/801cleanup, both true Main-role/female voices, entire DAC-to-stereo waveform and real faults qualified. All132 observed general cue producers and emitted queue words independently bound to original source. Preserve full original scope and prior ending/UI/shadow/move/campaign proofs.',
  candidate=current.NAME,cases=cases,nativeMatrixProofs=matrices,actualCueSourceProof=str(cuepath),
  actualCurrentBothSlotsHeldAndPressedNativeTombSoundAccepted=True,
  exactStereoPCMFrames=7726080,actualGeneralCueProducers=132,actualEmittedGeneralQueueWords=cues['actualEmittedGeneralQueueWords'],
  actualAudioSourceFaultsRejected=152,actualEarnedStateFaultsRejected=96,actualBranchFaultsRejected=32,
  actualLateVoiceFaultsRejected=32,actualCueSourceFaultsRejected=180,
  fullFourCaseEndingPixelsAndAudioRetained=True,
  samplesEnabled=False,importedWinnerMixedWaveformAccepted=False,naturalRandomDropCurrentAudioAccepted=False,
  broaderVictimStageArtAccepted=False,completeStageVictimAudioAccepted=False,
  nativePriorityChoiceAndSuppressionAccepted=False,actualRNGVariantChoiceAccepted=False,
  allCinematicsAndStockChoreographyAccepted=False,fullPortAcceptance=False,
  exactNativeAndHostProcessesStillLive=[],observedOtherOrReusedPIDs=jobs,
  consumedHeldCaptureToolSessions=[44593,22414,2553,59830],consumedHeldGateToolSessions=[90661],
  consumedPressedCaptureToolSessions=[27911,37326,18499,78134],consumedPressedGateToolSessions=[36557],
  consumedCueGateToolSessions=[27934,62630],
  preservedHarnessFailures=failures,preservedInitialPreflightOrderingFailure=str(ROOT/'tools/qualify_current_pressed_tomb_audio_v5759.py'),
  rawGuestRGBPCMFilesWritten=0,newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,publicZIPChanged=False,
  sealedTextSourcesLosslesslyCompacted=len(sealed),newInputHashes=pins,
  next='Do not replay the completed eight held/pressed Tomb native campaigns. Advance current enabled winner native+imported mixed waveform source fidelity, natural unpressed random-drop and broader Pit/Tomb victim/branch/art/shadow fidelity; keep wider move/arena/CPU/repeated/KO/overlap, other finisher/victim/morph/secret/cinematic and independent stock choreography requirements. Finish combined selection/ladder/names/audio regression, dependency-aware obsolete-folder cleanup and matching refreshed release ZIP only after full acceptance.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(report,indent=2)+'\n')
 digest=sha(path);need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
  'New checkpoint compacted without content changes')
 print(json.dumps({k:v for k,v in report.items()if k not in ('newInputHashes','remaining','cases','preservedHarnessFailures')},indent=2),flush=True)


if __name__=='__main__':run()
