"""Whole current both-slot Friendship audio and terminal-only bounded storage."""
import datetime,gzip,json,subprocess
from pathlib import Path
import capture_current_friendship_audio_v6255 as capture
import qualify_current_friendship_channels_v6257 as channels
import checkpoint_current_friendship_scenes_v6251 as storage
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
PARENT=capture.PARENT
OUT=ROOT/'audit_v6259_current_friendship_audio_progress'

def run():
 need(not OUT.exists(),'Fresh immutable actual audio matrix journal')
 capture.prior.current.expected()
 parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,
      'Entire original scope and current complete visual proof retained')
 cases=[];pins={};files=[];variants=set();frames=callbacks=states=mixed_faults=native_rows=0
 for fighter in('kano','sonya'):
  for side in(1,2):
   folder=ROOT/f'audit_v6256_current_{fighter}_friendship_audio_p{side}'
   report=json.loads((folder/'report.json').read_text());waveform=json.loads((folder/'waveform.json').read_text())
   terminal=json.loads((folder/'native_terminal.json').read_text())
   need(report['passed']and report['candidate']==capture.prior.current.NAME and report['samplesEnabled']and
        report['importedFriendshipMixAccepted']and report['fighter']==fighter and report['physicalSlot']==side and
        terminal['nativeExit']==0 and not terminal['hostDecodeErrors'],
        'Actual natural native terminal0/full enabled mix/current true character and physical slot')
   need(waveform['passed']and waveform['differentChannelSamples']==0 and
        waveform['actualSHA256']==waveform['predictedSHA256']and waveform['maximumMixedMagnitude']<1 and
        waveform['comparedStereoFrames']==len(report['pcmHeaders'])*960==report['comparedStereoFrames']and
        report['dacProof']['passed']and len(report['dacFaultsRejected'])==4 and
        len(report['originalSoundROMFaultsRejected'])==8 and all(p['wholeOriginalSoundRegionSourceExact']for p in report['wholeOriginalSoundROM']),
        'Whole source waveform equality; complete original DAC/ROM and actual faults, no fit/clipping/trim')
   with gzip.open(folder/'run.log.gz','rt')as log:text=log.read()
   native=capture.state(text,fighter,side,capture.prior.current.expected())
   need(native==report['nativeFriendshipScene']and native['native_kos']==2 and native['damage']==322 and
        native['actualTrueFighterID']==(17 if fighter=='kano'else 18),
        'Entire physical earned/choreography/winner/cleanup positive requalified')
   proof=channels.gate(text,report['pcmHeaders'],waveform);faults=channels.faults(text,report['pcmHeaders'],waveform)
   callback_digest=capture.mix.original.rows(text,'MK2_BBAUDIO_PCM_DIGEST')
   need(callback_digest==report['pcmHeaders']and len(faults)==4,'Every actual callback export and real channel-state faults')
   need(len(waveform['actualWholeMixedFaultsRejected'])==(8 if fighter=='kano'else 10),
        'Whole first/last/missing/source/gain/timing faults actually rejected')
   for p,h in report['inputHashes'].items():
    need(sha(p)==h and (p not in pins or pins[p]==h),'Consistent actual compiled/controller/original-clip inputs')
    pins[p]=h
   for p in folder.rglob('*'):
    if p.is_file():pins[str(p)]=sha(p)
   files.extend(p.resolve()for p in folder.glob('*.json'))
   frames+=waveform['comparedStereoFrames'];callbacks+=len(report['pcmHeaders']);states+=proof['exactSourceChannelStates']
   mixed_faults+=len(waveform['actualWholeMixedFaultsRejected']);native_rows+=native['nativeStateRows']
   variants.update(e['sample']for e in waveform['completeMarkerEvents']if e['sample']>=9)
   cases.append(dict(fighter=fighter,physicalSlot=side,report=str(folder/'report.json'),
       waveform=str(folder/'waveform.json'),nativeScene=native,sourceChannels=proof,actualChannelFaultsRejected=faults,
       wholeMixedFaultsRejected=waveform['actualWholeMixedFaultsRejected']))
 need(variants=={9,10,11,12},'All four original chicken clip variants actually exercised in complete current mix')
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',
   "Get-CimInstance Win32_Process -Filter \"Name='mkport_candidate.exe'\" | Select-Object ProcessId,Name,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"],
   capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'Actual native census empty before lossless terminal compression')
 allocations=[]
 for p in files:
  need(p.parent.parent==ROOT and p.parent.name.startswith('audit_v6256_current_'),'Exact bounded completed capture leaf')
  h=sha(p);before=storage.allocated(p)
  result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True,text=True)
  need(result.returncode==0 and sha(p)==h,'Exact terminal JSON compressed losslessly')
  allocations.append(dict(path=str(p),sha256=h,logicalBytes=p.stat().st_size,
                          allocatedBefore=before,allocatedAfter=storage.allocated(p)))
 for p in(PARENT,Path(__file__).resolve(),Path(channels.__file__),Path(storage.__file__),Path(capture.mix.__file__),
          ROOT/'mame-mkp/src/devices/sound/samples.cpp',ROOT/'mame-mkp/src/emu/disound.cpp',
          ROOT/'mame-mkp/src/emu/speaker.cpp',ROOT/'mame-mkp/src/emu/sound.cpp'):
  pins[str(p)]=sha(p)
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C','Existing portable playtest unchanged')
 pins[str(archive)]=sha(archive)
 need(all(sha(p)==h for p,h in pins.items()),'Whole actual relevant evidence unchanged after qualification/storage')
 result=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
      parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],inputHashes=pins,cases=cases,
      previousGoalTurnClassification=parent['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: all4 real current5219 physical Friendships natural-terminal; entire enabled native DCS/own win/bubble/separate overlapping chicken mix source-clock/sample/float exact; all14callback source positions/finite retirement and actual faults qualified; no raw media/build/rerun, exact terminal JSONs compressed',
      actualCurrentFriendshipAudioContexts=4,nativeAudioCallbacks=callbacks,comparedStereoFrames=frames,
      exactNativePhysicalRows=native_rows,collisionEarnedKOs=8,actualSourceChannelStates=states,
      actualOriginalFriendshipCueEvents=80,actualOwnWinnerAnnouncements=4,
      actualWaveformDACROMAndChannelFaultsRejected=mixed_faults+16+32+16,
      currentBothSlotWholeFriendshipMixAndFiniteChannelRetirementAccepted=True,
      currentBothSlotWholeFriendshipVisualAcceptanceRetained=True,
      allFriendshipVictimMirrorCPUContextsAccepted=False,allFinisherAudioAccepted=False,
      fullPortAcceptance=False,fullGoalComplete=False,currentReleaseZIPUnchanged=True,
      nativeBoots=4,nativeGamesInterrupted=0,nativeGamesRerunForHostError=0,
      newBuilds=0,newSourceDirectoryCopies=0,newRawMedia=0,exactTerminalJSONFilesCompressed=len(allocations),
      compression=allocations,allocatedBytesReclaimed=sum(a['allocatedBefore']-a['allocatedAfter']for a in allocations),
      nextActions=['Audit actual remaining native branches against current evidence, avoiding reruns of completed campaigns and Friendship scenes',
                   'Complete combined normal-launcher gameplay/selection/ladder/move/KO/audio regression and matching final handoff'])
 OUT.mkdir();capture.prior.save(OUT/'progress.json',result)
 print(json.dumps({k:v for k,v in result.items()if k not in('inputHashes','cases','compression')},indent=2),flush=True)

if __name__=='__main__':run()
