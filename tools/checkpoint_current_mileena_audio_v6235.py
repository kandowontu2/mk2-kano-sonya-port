"""Current Mileena source waveform plus full native effect/priority delivery.

Reuse successful initial SonyaP1; preserve three initial host-only failures
and corrected exact lifecycle/source-gate captures. No redundant rerun,
whole parent audit, build copy or raw audio artifact.
"""
import datetime,json,re,subprocess
from pathlib import Path
import current_mileena_audio_routes_v6234 as routes
import checkpoint_current_subzero_audio_v6219 as cleanup
host=routes.host
ROOT,need,sha=host.ROOT,host.need,host.sha
OUT=ROOT/'audit_v6236_current_mileena_source_audio_progress'

def run():
 need(not OUT.exists(),'Fresh finite current native audio journal')
 current=host.prior.original.current;guest=current.expected();routes.source_contract(guest)
 parentpath=host.prior.PARENT;parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,'Original scope preserved')
 pins={str(parentpath):sha(parentpath),str(Path(__file__)):sha(__file__),str(Path(routes.__file__)):sha(routes.__file__),
       str(Path(routes.prior.__file__)):sha(routes.prior.__file__),str(Path(host.__file__)):sha(host.__file__)}
 cases=[];folders=[];stereo=callbacks=channel_rows=state_rows=delivered=actual_faults=0
 for fighter in ('kano','sonya'):
  for side in (1,2):
   version=6231 if(fighter,side)==('sonya',1)else 6233
   folder=ROOT/f'audit_v{version}_current_mileena_{fighter}_p{side}_native_audio';folders.append(folder)
   path=folder/'report.json';r=json.loads(path.read_text());wpath=Path(r['waveformReport']);w=json.loads(wpath.read_text())
   need(r['passed']and r['samplesEnabled']and r['nativeDCSWaveformAccepted']and r['allEnabledImportedSourcesInactive']and
        r['nativeTerminal']['nativeExit']==0 and not r['nativeTerminal']['hostDecodeErrors'],
        'True current native identity/terminal and samples-enabled complete capture')
   need(w['passed']and w['differentChannelSamples']==0 and w['actualSHA256']==w['predictedSHA256']and
        len(w['effectiveActualWholeWaveformFaults'])==4 and len(r['dacFaultsRejected'])==4 and
        len(r['originalSoundROMFaultsRejected'])==8 and len(r['wholeOriginalSoundROM'])==2 and
        all(p['wholeOriginalSoundRegionSourceExact']for p in r['wholeOriginalSoundROM']),
        'All current native PCM samples, normalized DAC/source cursor and both complete12MiB ROM checks;16 real faults')
   need(all(sha(p)==h for p,h in r['inputHashes'].items()),'Every executed/current native input unchanged')
   text=cleanup.read_log(folder/'run.log.gz');state=host.state(text,fighter,side,guest)
   need(state['passed']and state['nativeInterRoundRefill']['actualStores']==81,
        'Whole original global refill then real own stream/disappearance/retirement')
   observed=r['nativeEarnedState']
   need(all(state[k]==v for k,v in observed.items()if k!='nativeInterRoundRefill')and
        all(state['nativeInterRoundRefill'][k]==v for k,v in observed['nativeInterRoundRefill'].items()),
        'All earlier actual state obligations retained; global source adds P2 register-context metadata only')
   channels=cleanup.inactive_channels(text,r['pcmHeaders'])
   need(channels==r['importedChannelsObserved'],'Every real enabled imported channel inactive throughout actual sound callbacks')
   native=routes.native_routes(text,guest,fighter,side);faults=routes.faults(text,guest,fighter,side)
   need(native['nativePacketBytesDelivered']==92 and native['completeNativePCMFrames']==r['comparedStereoFrames']and
        len(native['actualNativeFixedEffects'])==3 and len(faults)==7,
        'Entire original3908 fixed native cues, priority slot, full packet and92actual ADSP bytes')
   for label,tag,key,value in (('actual earned damage','ACTION','damage','321'),
                              ('actual victim owner','ACTION','victim_actor','01000000')):
    line=next(s for s in text.splitlines()if s.startswith('MK2_MILEENA_V3784_'+tag+' '))
    bad,count=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
    need(count==1 and bad!=line,'Actual native state counterexample')
    try:host.state(text.replace(line,bad,1),fighter,side,guest)
    except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
    else:raise ValueError('Accepted native state fault '+label)
    need(host.state(text,fighter,side,guest)==state,'Full actual state restored')
   callbacks+=r['dacProof']['callbacks'];stereo+=r['comparedStereoFrames'];channel_rows+=channels
   state_rows+=state['nativeStateRows'];delivered+=native['nativePacketBytesDelivered'];actual_faults+=16+len(faults)
   pins.update(r['inputHashes']);pins[str(path)]=sha(path);pins[str(wpath)]=sha(wpath)
   reference=Path(state['sourceQualifiedCurrentLifecycle']);pins[str(reference)]=sha(reference)
   cases.append(dict(fighter=fighter,physicalSlot=side,report=str(path),completeNativeState=state,
                     sourceQualifiedNativeEffectsAndADSPDelivery=native,additionalActualSemanticFaultsRejected=faults))
 failures=[]
 for fighter,side in (('kano',1),('kano',2),('sonya',2)):
  folder=ROOT/f'audit_v6231_current_mileena_{fighter}_p{side}_native_audio';folders.append(folder)
  failed=json.loads((folder/'failure.json').read_text());terminal=json.loads((folder/'native_terminal.json').read_text())
  need(not failed['passed']and terminal['nativeExit']==0 and not terminal['hostDecodeErrors'],
       'Original post-native reference/refill checker failures retained; no game interruption')
  failures.append(dict(path=str(folder/'failure.json'),nativeTerminal=str(folder/'native_terminal.json'),
                       cause='Old lifecycle reference selection or obsolete winning-actor assumption in the original global P2 refill'))
  pins[str(folder/'failure.json')]=sha(folder/'failure.json');pins[str(folder/'native_terminal.json')]=sha(folder/'native_terminal.json')
 query="Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'mkport_candidate.exe' -and $_.CommandLine -like '*mk2port*' } | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'Actual empty native census before exact terminal compression')
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C','Current release unchanged')
 files=[p for folder in folders for p in folder.iterdir()if p.is_file()and p.suffix=='.json']
 before={str(p):dict(sha256=sha(p),allocated=cleanup.allocated(p))for p in files}
 for p in files:
  result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True,text=True)
  need(result.returncode==0,'Exact terminal-only evidence compression')
 need(all(sha(p)==v['sha256']for p,v in before.items())and all(sha(p)==h for p,h in pins.items()),
      'All logical source/evidence bytes preserved after compression')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  parentAdditiveJournal=str(parentpath),remaining=parent['remaining'],inputHashes=pins,cases=cases,
  actualCurrentMileenaContexts=4,nativeAudioCallbacks=callbacks,comparedStereoFrames=stereo,
  actualEnabledImportedChannelObservations=channel_rows,exactNativePhysicalStateRows=state_rows,
  collisionEarnedKOs=8,sourceQualifiedNativeGlobalRefillStores=324,actualADSPBytesDelivered=delivered,
  effectiveActualAudioStateAndPacketFaultsRejected=actual_faults,preservedInitialHostFailures=failures,
  currentMileenaWholeSourceAudioAndNativeEffectDeliveryAccepted=True,allFinisherAudioAccepted=False,
  scope='Whole natural stock5 swallowing action through original601-field post-finisher terminal, current true17/18 in both slots; enabled-channel/whole PCM/DAC/ROM proof and unchanged source fixed effects/priority/packed bytes/actual ADSP reads',
  fullPortAcceptance=False,fullGoalComplete=False,currentReleaseZIPUnchanged=True,newBuilds=0,
  newSourceDirectoryCopies=0,rawMediaFilesWritten=0,nativeGamesInterrupted=0,
  exactTerminalJSONFilesCompressed=len(files),allocatedBytesReclaimed=sum(v['allocated']-cleanup.allocated(p)for p,v in before.items()),
  nextActions=['Audit the remaining cinematic/finisher source scopes against actual current evidence, without repeating qualified cases',
               'Broader arena/CPU interaction and final combined selection/ladder/names/moves/audio/release/cleanup verification'])

if __name__=='__main__':
 try:report=run()
 except Exception as error:
  import traceback
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();host.prior.original.save(OUT/'progress.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','remaining','cases')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
