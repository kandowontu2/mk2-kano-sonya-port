"""Seal actual current four-case ending audio without narrowing the full goal.

All four complete cold captures, actual source-clock waveform and phase/fault
proofs are required. Preserve previous full ending pixels and original scope.
No new game boot/build, ROM copy, release promotion or all-game audio claim.
"""
import ast,datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5747_current_four_case_ending_audio_progress'


def run():
 need(not OUT.exists(),'Fresh immutable complete four-case audio receipt')
 current.expected()
 parentpath=ROOT/'audit_v5732_current_four_case_ending_pixels_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['actualCurrentFourCaseNaturalEndingPipelineAccepted']and
  parent['allFourConsecutiveVideoFields']==12165,'Actual complete four-case current ending pixels retained')
 pins=dict(parent['sourceInputs']);pins[str(parentpath)]=sha(parentpath)
 cases=[];processes=[];sealed=[]
 for side in (1,2):
  for fighter,identity in [('kano',17),('sonya',18)]:
   path=ROOT/f'audit_v5745_{fighter}_p{side}_ending_audio_window_checked/report.json'
   need(path.exists(),'Await actual full phase gate; never seal missing/unfinished native evidence')
   phase=json.loads(path.read_text());folder=Path(phase['capture'])
   meta=json.loads((folder/'result.json').read_text())
   model=json.loads((folder/'audio_live_source_model.json').read_text())
   process=json.loads((folder/'process.json').read_text());processes.append(process)
   need(phase['passed']and phase['fighter']==fighter and phase['physicalSlot']==side and
    phase['identity']==identity and phase['actualEntireNativeSourceClockAudioAccepted']and
    phase['noPostKOVoiceLoopOrStaleCharacterChannels']and
    phase['terminal']-phase['attract']==300 and
    phase['consecutiveNativeFields']==phase['terminal']-phase['window']and
    phase['actualChannelStates']==phase['consecutiveNativeFields']*14 and
    phase['actualPCMCallbacks']==phase['actualDACCallbacks']and
    phase['exactStereoPCMFrames']==phase['actualPCMCallbacks']*960 and
    phase['actualFull16BitPortStores']==phase['actualNativeADSPReads']==2*phase['actualCompletePackets']and
    phase['wholeSoundROMCheckpoints']==2 and len(phase['actualAudioWindowFaultsRejected'])==19,
    'Actual entire KO/own-ending/300attract waveform/channel/packet/ADSP/ROM scope and all19 real faults')
   need(meta['passed']and meta['nativeExit']==0 and meta['fighter']==fighter and
    meta['physicalSlot']==side and meta['identity']==identity and
    meta['candidate']==current.NAME and meta['executableSHA256']==current.EXE_SHA and
    meta['guestSHA256']==current.GUEST_SHA and meta['rawMediaGuestAudioFilesWritten']==0 and
    meta['newBuilds']==0 and (folder/'stderr.log').read_text()==''and
    model['passed']and model['waveform']['differentChannelSamples']==0 and
    model['waveform']['comparedStereoFrames']==phase['exactStereoPCMFrames']and
    model['waveform']['actualSHA256']==phase['actualFullWaveformSHA256']and
    len(model['actualDACFaultsRejected'])==4 and len(model['actualSoundROMFaultsRejected'])==8 and
    len(model['waveform']['effectiveActualWholeWaveformFaults'])==4,
    'Actual current compiled true-ID native terminal and complete live RAM proof, not source-only acceptance')
   need(not phase['independentStockEndingChoreographyWaveformAccepted']and
    not phase['allEndingAudioContextsAccepted']and not phase['fullPortAcceptance'],
    'Actual source fidelity does not substitute for independent stock choreography or all-game/full-port acceptance')
   need(not any(p.suffix.lower()in('.png','.wav','.bin')for p in folder.rglob('*')if p.is_file()),
    'No timed-stop PNG or raw guest/RGB/PCM/DAC/ROM files in actual capture')
   for p,h in phase['inputHashes'].items():
    need(sha(p)==h and(p not in pins or pins[p]==h),'Every full current/native/source/model/phase input intact')
    pins[p]=h
   pins[str(path)]=sha(path);sealed.append(path)
   sealed.extend(p for p in folder.rglob('*')if p.is_file()and p.suffix in('.json','.log','.cfg'))
   cases.append({k:v for k,v in phase.items()if k not in('inputHashes','actualAudioWindowFaultsRejected')})
   cases[-1].update(phaseProof=str(path),actualAudioWindowFaultsRejected=19,
    actualDACFaultsRejected=4,actualWaveformFaultsRejected=4,actualSoundROMFaultsRejected=8)
 # Preserve both genuine checker failures; their correction does not edit the game.
 old=ROOT/'tools/verify_current_ending_audio_window_v5740.py'
 try:ast.parse(old.read_text())
 except SyntaxError as error:need(error.lineno==27,'Preserved exact original checker parse failure')
 else:raise ValueError('Original failed checker was changed')
 failedpath=ROOT/'audit_v5743_kano_p1_ending_audio_window_checked/report.json'
 failed=json.loads(failedpath.read_text())
 need(not failed['passed']and 'Both original own final boss winner table reads' in failed['error'],
  'Genuine fixed-count checker failure retained, not hidden or called a game failure')
 sources=[old,ROOT/'tools/verify_current_ending_audio_window_v5742.py',
  ROOT/'tools/verify_current_ending_audio_window_v5744.py',Path(__file__),failedpath]
 for p in sources:pins[str(p.resolve())]=sha(p)
 # Process identity includes creation time and full command: reused PIDs are not live captures.
 pids=sorted({p[k]for p in processes for k in('pid','hostPID')})
 query="Get-CimInstance Win32_Process -Filter '"+' OR '.join(f'ProcessId={p}'for p in pids)+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 output=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(output)if output else []
 if isinstance(jobs,dict):jobs=[jobs]
 for p in processes:
  need(not any(j['ProcessId']==p['pid']and j['Name']=='mkport_candidate.exe'and
   abs(j['createdUnix']-p['startedUnix'])<.05 and
   'mk2ks_current_ending_audio_campaign_v5735.lua'in j['CommandLine']for j in jobs),
   'Every exact captured native process terminal; no timeout treated as stop')
  need(not any(j['ProcessId']==p['hostPID']and j['Name']=='python.exe'and
   'run_current_ending_audio_v5736.py'in j['CommandLine']for j in jobs),
   'Every actual capture/model host terminal')
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 need(all(sha(p)==h for p,h in public.items()),'Public launcher and playtest ZIP unchanged pending full acceptance')
 for p,h in public.items():pins[str(p.resolve())]=h
 need(all(sha(p)==h for p,h in pins.items()),'All actual current and prior full-scope evidence stable now')
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  parentAdditiveJournal=str(parentpath),remaining=parent['remaining'],
  previousGoalTurnClassification='progress: current full passive audio observer/source model qualified; actual current P2 campaigns and whole waveform models completed; exact current P1 captures started',
  thisGoalTurnClassification='progress: four actual cold current K/S P1/P2 campaigns completed. Entire final-KO/own-ending/300attract native DAC-to-stereo waveforms matched source exactly; all fourteen channels, original packet/high-low16bit stores, real ADSP reads, loaded sound ROMs and19actual phase faults per case accepted. Current full ending-pixel proofs retained. Original goal scope remains.',
  cases=cases,actualCurrentFourCaseEndingSourceClockAudioAccepted=True,
  exactStereoPCMFrames=sum(c['exactStereoPCMFrames']for c in cases),
  consecutiveNativeFields=sum(c['consecutiveNativeFields']for c in cases),
  actualChannelStates=sum(c['actualChannelStates']for c in cases),
  actualFull16BitPortStores=sum(c['actualFull16BitPortStores']for c in cases),
  actualNativeADSPReads=sum(c['actualNativeADSPReads']for c in cases),
  exactCaptureProcessesStillLive=[],observedOtherOrReusedPIDs=jobs,
  consumedCaptureToolSessions=[18039,83251,97838,22759],
  consumedPhaseToolSessions=[84976,23687,87858,98287,26566,50042,54681],
  actualFourCaseEndingPixelsAcceptanceRetained=True,
  independentStockEndingChoreographyWaveformAccepted=False,allEndingAudioContextsAccepted=False,
  allStageEffectVictimAudioAccepted=False,fullPortAcceptance=False,
  rawGuestRGBPCMFilesWritten=0,newBuilds=0,deletedFiles=0,publicPlayableChanged=False,publicZIPChanged=False,
  inputHashes=pins,
  next='All four current ending audio captures are terminal; do not restart. Continue native Pit/Tomb victim/mirror/branch art and complete effect/victim audio, wider move/arena/shadow/KO coverage, remaining victim/finisher/morph/secret/cinematic fidelity and independent stock choreography. Final combined selection/ladder/names/audio regression, dependency-aware obsolete-folder cleanup and refreshed matching release remain required. Preserve all original work groups; finite actual ending source-clock audio is not whole-port completion.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(report,indent=2)+'\n')
 sealed.extend([path,*sources])
 before={str(p):sha(p)for p in sealed}
 for p in sealed:
  need(p.resolve().is_relative_to(ROOT.resolve()),'Exact bounded immutable text compression')
  need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0,
   'Lossless compression of sealed text only')
 need(all(sha(p)==h for p,h in before.items()),'Every full source/evidence byte preserved; no guessed disk-savings claim')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','remaining','cases')},indent=2),flush=True)


if __name__=='__main__':run()
