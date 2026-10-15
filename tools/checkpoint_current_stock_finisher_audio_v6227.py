"""Current four-finisher/both-own-character/both-slot enabled audio evidence.

Whole original PCM/DAC/ROM checks and physical native state are preserved.
Exact terminal-only NTFS compression; no copied builds or raw media.
"""
import datetime,json,re,subprocess
from pathlib import Path
import capture_current_stock_finisher_audio_v6224 as host
import checkpoint_current_subzero_audio_v6219 as original
ROOT,need,sha=host.ROOT,host.need,host.sha
OUT=ROOT/'audit_v6228_current_stock_finisher_audio_progress'
ART={
 'kitana':'audit_v6122_current_kitana_native_scene_progress/progress.json',
 'kung_lao':'audit_v6133_current_kung_lao_native_scene_progress/progress.json',
 'jax_clap':'audit_v6140_current_jax_clap_native_scene_progress/progress.json',
 'jax_arms':'audit_v6152_current_jax_arms_native_scene_progress/progress.json',
}

def run():
 need(not OUT.exists(),'Fresh whole audio journal')
 current=host.prior.original.current;guest=current.expected()
 parentpath=host.prior.PARENT;parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,'Full scope preserved')
 pins={str(parentpath):sha(parentpath),str(Path(__file__)):sha(__file__)}
 cases=[];folders=[];callbacks=stereo=channel_observations=state_rows=actual_faults=0
 for variant in host.CONFIG:
  proofpath=ROOT/ART[variant];art=json.loads(proofpath.read_text())
  need(art['passed']and art['goalStatus']=='active','Previously source-qualified current finisher scene prerequisite')
  pins[str(proofpath)]=sha(proofpath)
  for fighter in ('kano','sonya'):
   for side in (1,2):
    folder=ROOT/f'audit_v6226_current_{variant}_{fighter}_p{side}_native_audio';folders.append(folder)
    path=folder/'report.json';r=json.loads(path.read_text());wpath=Path(r['waveformReport']);w=json.loads(wpath.read_text())
    need(r['passed']and r['variant']==variant and r['samplesEnabled']and r['nativeDCSWaveformAccepted']and
         r['allEnabledImportedSourcesInactive']and r['nativeTerminal']['nativeExit']==0 and
         not r['nativeTerminal']['hostDecodeErrors'],'Actual current true context/release-option native terminal')
    need(w['passed']and w['differentChannelSamples']==0 and w['actualSHA256']==w['predictedSHA256']and
         len(w['effectiveActualWholeWaveformFaults'])==4 and len(r['dacFaultsRejected'])==4 and
         len(r['originalSoundROMFaultsRejected'])==8 and len(r['wholeOriginalSoundROM'])==2 and
         all(p['wholeOriginalSoundRegionSourceExact']for p in r['wholeOriginalSoundROM']),
         'Every original native sample/DAC cursor/normalization and both whole12MiB source ROM checks;16 real faults')
    need(all(sha(p)==h for p,h in r['inputHashes'].items()),'All actual source/compiled/native inputs unchanged')
    text=original.read_log(folder/'run.log.gz');native=host.state(text,fighter,side,variant,guest)
    need(native==r['nativeEarnedState'],'Whole observed state requalifies against current source-qualified native scene')
    channels=original.inactive_channels(text,r['pcmHeaders'])
    need(channels==r['importedChannelsObserved'],'Every enabled imported channel at every native sound callback')
    rejected=[]
    for tag,key,value in (('ACTION','damage','321'),('HEALTH','pc','FFF00000')):
     line=next(s for s in text.splitlines()if s.startswith('MK2_STOCK_HEAD_V921_'+tag+' '))
     changed,count=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
     need(count==1 and changed!=line,'Actual native state byte/field counterexample')
     try:host.state(text.replace(line,changed,1),fighter,side,variant,guest)
     except ValueError as error:rejected.append(dict(kind=tag+'_'+key,rejectedBy=str(error)))
     else:raise ValueError('Accepted changed actual native state '+key)
     need(host.state(text,fighter,side,variant,guest)==native,'Whole original state positive restored')
    line=next(s for s in text.splitlines()if s.startswith('MK2_TOMB_MIX_CHANNEL '))
    for label,bad in (('active_source',text.replace(line,line.replace('sample=4294967295','sample=13',1),1)),
                      ('missing_channel',text.replace(line+'\n','',1)),
                      ('wrong_channel',text.replace(line,line.replace('channel=0','channel=14',1),1))):
     need(bad!=text,'Nonvacuous actual enabled-channel counterexample')
     try:original.inactive_channels(bad,r['pcmHeaders'])
     except ValueError as error:rejected.append(dict(kind=label,rejectedBy=str(error)))
     else:raise ValueError('Accepted actual enabled-channel fault '+label)
     need(original.inactive_channels(text,r['pcmHeaders'])==channels,'Full enabled source positive restored')
    callbacks+=r['dacProof']['callbacks'];stereo+=r['comparedStereoFrames'];channel_observations+=channels
    state_rows+=native['nativeStateRows'];actual_faults+=16+len(rejected)
    pins.update(r['inputHashes']);pins[str(path)]=sha(path);pins[str(wpath)]=sha(wpath)
    source_scene=Path(native['sourceQualifiedCurrentScene']);pins[str(source_scene)]=sha(source_scene)
    cases.append(dict(variant=variant,fighter=fighter,physicalSlot=side,report=str(path),
      audioCallbacks=r['dacProof']['callbacks'],stereoFrames=r['comparedStereoFrames'],
      completeNativePhysicalState=native,additionalActualStateAndChannelFaultsRejected=rejected))
 failed=ROOT/'audit_v6223_current_kitana_kano_p1_native_audio';terminal=json.loads((failed/'native_terminal.json').read_text())
 failure=json.loads((failed/'failure.json').read_text())
 need(terminal['nativeExit']==0 and not terminal['hostDecodeErrors']and not failure['passed']and
      'Whole stock finisher750field'in(failed/'stderr.log').read_text(),
      'Original incorrect observer entry/stop-phase failure retained after native terminal')
 folders.append(failed);pins[str(failed/'failure.json')]=sha(failed/'failure.json')
 query="Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'mkport_candidate.exe' -and $_.CommandLine -like '*mk2port*' } | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'Actual empty current native census before compression')
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C','Current release unmodified')
 files=[p for folder in folders for p in folder.iterdir()if p.is_file()and p.suffix=='.json']
 before={str(p):dict(sha256=sha(p),allocated=original.allocated(p))for p in files}
 for p in files:
  result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True,text=True)
  need(result.returncode==0,'Exact native-terminal JSON compression')
 need(all(sha(p)==v['sha256']for p,v in before.items())and all(sha(p)==h for p,h in pins.items()),
      'Every logical source/evidence byte unchanged after cleanup')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  parentAdditiveJournal=str(parentpath),remaining=parent['remaining'],inputHashes=pins,cases=cases,
  actualCurrentFinisherContexts=len(cases),nativeAudioCallbacks=callbacks,comparedStereoFrames=stereo,
  actualEnabledImportedChannelObservations=channel_observations,exactNativePhysicalStateRows=state_rows,
  nativeCollisionEarnedKOs=2*len(cases),actualOriginalSoundROMChecks=2*len(cases),
  effectiveActualAudioStateAndChannelFaultsRejected=actual_faults,
  sourceExactKitanaKungLaoJaxClapAndArmRipAudioAccepted=True,allFinisherAudioAccepted=False,
  scope='Complete750field stock finisher action/completion/continue windows, all four true Kano/Sonya victim/physical-slot contexts, samples enabled, native stereo/DAC/ROM and full existing current earned-state references',
  preservedInitialObserverFailure=dict(path=str(failed/'failure.json'),nativeExit=0,
      cause='Observer Kitana entry and callback terminal phase; actual normal game completed'),
  fullPortAcceptance=False,fullGoalComplete=False,currentReleaseZIPUnchanged=True,newBuilds=0,
  newSourceDirectoryCopies=0,rawMediaFilesWritten=0,nativeGamesInterrupted=0,
  exactTerminalJSONFilesCompressed=len(files),allocatedBytesReclaimed=sum(v['allocated']-original.allocated(p)for p,v in before.items()),
  nextActions=['Close the remaining Mileena/cinematic audio scope using existing native controllers and source data',
               'Target broader arena/CPU interactions, then final combined selection/ladder/names/moves/audio and release/cleanup audit'])

if __name__=='__main__':
 try:report=run()
 except Exception as error:
  import traceback
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();host.prior.original.save(OUT/'progress.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','remaining','cases')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
