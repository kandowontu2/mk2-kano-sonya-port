"""Native ending mixed-PCM progress; all original port requirements retained."""
import ctypes,json,subprocess
from pathlib import Path
import verify_native_ending_audio_window_v4514 as audio
ROOT,need,sha=audio.ROOT,audio.need,audio.sha
PARENT=ROOT/'audit_v4494_kano_current_p2_tower_ending_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4517_native_ending_audio_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable full-scope progress checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()),'Every inherited original requirement/evidence unchanged')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need((wanted is None or actual==wanted) and (key not in pins or pins[key]==actual),
             'Exact actually executed current and inherited source/evidence bytes')
        pins[key]=actual
    pin(PARENT);pin(__file__)
    path=audio.OUT/'report.json';proof=json.loads(path.read_text());pin(path)
    observation_path=audio.observed.OUT/'report.json';observation=json.loads(observation_path.read_text());pin(observation_path)
    need(proof['passed'] and proof['currentBothP2CompleteEndingAttractMixedPCMNoImportedContributionAccepted'] and
         not proof['independentOriginalDCSWaveformReferenceAccepted'] and not proof['allEndingAudioFidelityAccepted'] and
         not proof['fullEndingTransitionRasterAccepted'] and not proof['fullPortAcceptance'],
         'Complete actual native window/PCM/channel/DCS byte gates pass, original waveform/raster/full-port exclusions retained')
    need(observation['passed'] and observation['actualPairedCaptures']==4 and
         observation['newEndingNativePCMWindowObservationsAccepted'], 'Four real terminal RAM-only sound windows')
    for result in (proof,observation):
        for p,h in result['inputHashes'].items():pin(p,h)
    need({(r['fighter'],r['physicalSlot'],r['identity']) for r in proof['cases']}=={('kano',2,17),('sonya',2,18)} and
         all(len(r['actualAudioWindowFaultsRejected'])==9 and r['consecutiveNativeFields']>3000 and
             r['actualChannelStates']==14*r['consecutiveNativeFields'] and r['nativePCMUpdates']>3000 and
             r['completeActualEndingAttractMixedPCMNoImportedContributionAccepted'] for r in proof['cases']),
         'Both real identities, every audio/14channel/phase field and actual negative controls')
    need(all(r['actualNativePCMExactlyEqual'] and r['allFourteenSampleChannelsInactiveThroughEveryField'] and
             all(r['nativeInventoriesEqual'].values()) and
             r['originalCompleteNativeCampaignAndGuestRGBEventsExactlyUnchanged'] for r in observation['cases']),
         'Every original accepted cold native input/state/guest/RGB event unchanged; whole mixed PCM exactly equal samples on/off')
    query="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_native_ending_audio_campaign_ram_v4511.py|verify_native_ending_audio_window_v4514.py|audit_v4499_' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    live=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(live.returncode==0 and not live.stdout.strip(),'All actual new sound/phase jobs terminal')
    files=[]
    for case in observation['cases']:
        for name in ('capture','baseline'):
            folder=Path(case[name]);files.extend(p for p in folder.rglob('*') if p.is_file())
    for folder in (audio.OUT,audio.observed.OUT,audio.observed.source.OUT):
        files.extend(p for p in folder.rglob('*') if p.is_file())
    alloc=ctypes.windll.kernel32.GetCompressedFileSizeW
    alloc.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];alloc.restype=ctypes.c_uint32
    allocated=0
    for p in files:
        pin(p);hi=ctypes.c_uint32();lo=alloc(str(p),ctypes.byref(hi));need(lo!=0xffffffff,'Exact new evidence allocation')
        allocated+=(hi.value<<32)|lo
    next_action=('Both current3836 P2 native final-KO/ending/attract audio windows are now complete RAM-only '
      'paired observations. Unchanged accepted controllers are reused only to observe formerly missing '
      'sound fields; every original native physical/selection/health/morph/move/boss/ending/guest/RGB event '
      'is exactly equal to accepted cold references. Every mixed stereo PCM update is exactly equal '
      'samples-on/off, non-silent native audio, all fourteen imported channels inactive in every field, '
      'actual original source collision/window/ending/attract PCs/IDs/timing and every native port byte '
      'read by DCS before next write verified; nine actual complete-window faults per context rejected. '
      'samples.cpp deliberately retains inactive old source_len/pos; these are not audio activity. '
      'This is NOT an independent original-stock DCS whole-waveform reference or full ending transition '
      'raster/cinematic/audio/all-P1 acceptance. Do not repeat completed identical P2 mixed-PCM captures '
      'or accepted towers or held/pressed/unpressed Tomb mirrors. Next close the remaining independent '
      'native waveform/ending transition/current-build contexts, broader Pit/Tomb stock victims/branches/'
      'audio and full move-phase/ground/shadow/CPU/repeat/KO/overlap coverage, other finishers/victims/'
      'morphs/secrets/cinematics, final combined selection/ladder/names/audio/dependency cleanup/release. '
      'All five original groups remain unchanged. No new EXE/ROM/raw media or deletion; public1836 still '
      'unchanged playtest, not a finished release; no historical cleanup savings counted again.')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
        mergeRule='All inherited full-goal groups/evidence/exclusions retained; complete actual P2 ending mixed-PCM/channel/DCS delivery windows added.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: new read-only observers capture missing final-KO/ending/attract audio, full paired PCM/14channel/clock/native source/port-to-DSP/cleanup and actual counterexamples pass for both P2 identities without altering original cold native gameplay events.',
      current3836BothP2EndingAttractMixedPCMNoImportedContributionAccepted=True,
      current3836BothP2EndingNativeAudioWindowReport=str(path),current3836BothP2EndingNativeAudioWindowContexts=proof['cases'],
      current3836BothP2EndingIndependentStockDCSWaveformAccepted=False,
      current3836AllEndingTransitionRasterCinematicsAudioContextsAccepted=False,
      currentTurnDiagnosticLogicalBytes=sum(p.stat().st_size for p in files),currentTurnDiagnosticAllocatedBytes=allocated,
      currentTurnNewBuilds=0,currentTurnRawAudioRasterVRAMROMCopies=0,currentTurnDeletedFiles=0,currentTurnReclaimedAllocatedBytes=0,
      cleanupAccounting='Only new compressed source/text/digests; complete PCM/guest/RGB transported and compared in RAM. No deletion or historical saving recounted.',
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      nextAction=next_action,nextImplementationAction=next_action,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'Original full objective and all five groups unchanged')
    need(all(sha(p)==h for p,h in pins.items()),'Every actual inherited/current/public input unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
                    'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),inputPins=len(pins),actualNativeAudioContexts=2,
        actualPairedCaptures=4,currentEvidenceAllocatedBytes=allocated,originalRemainingGroups=5,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
