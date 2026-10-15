"""Seal four genuine current stock-opponent Pit audio/ownership contexts.

Additive progress only. Preserve whole goal, current protected bytes, every
native/source/fault result and release gap. Bounded text compression only.
"""
import datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
from record_current_cross_tomb_audio_v5844 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5938_current_pit_stock_shadow_progress/progress.json'
OUT=ROOT/'audit_v5953_current_subzero_pit_audio_progress'

def run():
 need(not OUT.exists(),'Fresh immutable additive full-scope progress')
 current.expected();parent=json.loads(PARENT.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,
      'All original goal groups remain in scope, including verified campaigns/own endings')
 pins={str(PARENT):sha(PARENT)};sealed=[];reports={}
 for leaf in('audit_v5946_current_subzero_pit_audio_source_checked',
             'audit_v5949_current_subzero_pit_mix_checked',
             'audit_v5951_current_subzero_pit_owner_checked'):
  path=ROOT/leaf/'report.json';value=json.loads(path.read_text());need(value['passed'],'Completed source/native post-gate '+leaf)
  reports[leaf]=value;pins[str(path)]=sha(path);sealed.append(path)
  for p,h in value['inputHashes'].items():
   need(p not in pins or pins[p]==h,'Consistent immutable executed and qualified inputs');pins[p]=h
 audio=reports['audit_v5949_current_subzero_pit_mix_checked'];owner=reports['audit_v5951_current_subzero_pit_owner_checked']
 need(audio['exactStereoPCMFrames']==3863040 and audio['actualSourceAudioFaultsRejected']==116 and
      audio['actualEarnedStateFaultsRejected']==48 and audio['actualRawMixedPCMFaultsRejected']==16 and
      audio['actualMixedSourceOperationFaultsRejected']==16 and owner['actualDirectNativeFaultsRejected']==104 and
      owner['directlyObservedMain140OwnershipAccepted']and not owner['allNativePitCuePriorityAndRNGAccepted']and
      not owner['stockVictimRGBAccepted']and not owner['completeStageVictimAudioAccepted']and not owner['fullPortAcceptance'],
      'Entire full waveform/source-clock/ADSP/state plus direct cinematic ancestry/owner fault scopes retained without widening')
 processes=[];cases=[]
 host_creations={('kano',1):'2026-10-08T06:51:03.953025-04:00',
                 ('kano',2):'2026-10-08T06:53:28.455983-04:00',
                 ('sonya',1):'2026-10-08T06:53:28.452434-04:00',
                 ('sonya',2):'2026-10-08T06:53:28.451071-04:00'}
 for fighter in('kano','sonya'):
  for side in(1,2):
   folder=ROOT/f'audit_v5947_current_subzero_pit_mix_{fighter}_p{side}_samples'
   process=json.loads((folder/'process.json').read_text());meta=json.loads((folder/'result.json').read_text())
   live=json.loads((folder/'audio_live_source_model.json').read_text())
   ac=next(c for c in audio['cases']if c['fighter']==fighter and c['physicalSlot']==side)
   oc=next(c for c in owner['cases']if c['fighter']==fighter and c['physicalSlot']==side)
   need(meta['exit_code']==0 and meta['fighter']==fighter and meta['side']==side and live['passed']and
        live['nativeEarnedPitState']['earned_matches']==7 and ac['origin']==oc['origin']and ac['terminal']==oc['terminal']and
        len(ac['actualAudioSourceWindowFaultsRejected'])==29 and len(oc['actualFaultsRejected'])==26 and
        process['command'][1]=='mk2ks'and '-samples'in process['command']and '-nocheat'in process['command']and
        process['command'][-1]==str(ROOT/'mk2ks_current_subzero_pit_campaign_v5942.lua'),
        'Each genuine own17/18 versus selected stock8 full-health seven-match terminal agrees across entire native post-gates')
   processes.append((process,fighter,side))
   cases.append(dict(fighter=fighter,physicalSlot=side,ownID=oc['ownID'],actualOriginalVictimID=8,
                     nativeExitCode=0,earnedMatches=7,origin=oc['origin'],terminal=oc['terminal'],
                     exactStereoPCMFrames=ac['exactStereoPCMFrames'],actualWholePCMSHA256=ac['actualWholePCMSHA256'],
                     directCinematicOwnership=oc,fullNativeAudioWindowAccepted=True))
   for path in folder.rglob('*'):
    if not path.is_file():continue
    need(path.suffix.lower()not in('.wav','.pcm','.rgb','.png','.bin','.exe','.zip','.mdata'),
         'No raw native/ROM/raster/PCM or duplicate build/release artifacts')
    pins[str(path)]=sha(path)
    if path.suffix.lower()in('.json','.log','.cfg','.txt'):sealed.append(path)
 for leaf in('mk2ks_current_subzero_pit_driver_v5940.lua','mk2ks_current_subzero_pit_audio_v5941.lua',
             'mk2ks_current_subzero_pit_campaign_v5942.lua','tools/current_subzero_pit_state_v5943.py',
             'tools/qualify_current_subzero_pit_audio_v5944.py','tools/run_current_subzero_pit_audio_v5945.py',
             'tools/verify_current_subzero_pit_mix_v5948.py','tools/qualify_current_subzero_pit_owner_v5950.py',
             'tools/record_current_subzero_pit_progress_v5952.py'):
  path=ROOT/leaf;pins[str(path)]=sha(path);sealed.append(path)
 public={str(ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd'):'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
         str(ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip'):'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 pins.update(public)
 ids=sorted({p[k]for p,f,s in processes for k in('pid','hostPID')})
 query="Get-CimInstance Win32_Process -Filter '"+' OR '.join(f'ProcessId={p}'for p in ids)+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 output=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(output)if output else[]
 if isinstance(jobs,dict):jobs=[jobs]
 for p,f,s in processes:
  host_start=datetime.datetime.fromisoformat(host_creations[f,s]).timestamp()
  need(not any(j['ProcessId']==p['pid']and j['Name']=='mkport_candidate.exe'and
               abs(j['createdUnix']-p['startedUnix'])<.1 and p['command'][-1]in(j['CommandLine']or'')for j in jobs),
       'Exact captured native PID/name/creation/full script command is terminal, not timeout-restarted')
  need(not any(j['ProcessId']==p['hostPID']and j['Name']=='python.exe'and
               abs(j['createdUnix']-host_start)<.1 and 'run_current_subzero_pit_audio_v5945.py'in(j['CommandLine']or'')and
               f'--fighter {f} --side {s}'in(j['CommandLine']or'')for j in jobs),
       'Exact captured host PID/name/creation/command is terminal')
 current.expected();need(all(sha(p)==h for p,h in pins.items()),'All protected/prior/executed/native/public/source bytes intact')
 sealed=list(dict.fromkeys(p.resolve()for p in sealed));before=sum(allocated(p)for p in sealed)
 for path in sealed:
  digest=sha(path);done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True)
  need(done.returncode==0 and sha(path)==digest,'Exact bounded sealed text losslessly compressed without backup copies')
 after=sum(allocated(p)for p in sealed)
 progress=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
               parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],cases=cases,newInputHashes=pins,
               thisGoalTurnClassification='progress: four genuine own17/18 versus physically selected original Sub-Zero8 cold native runs earn seven full-health matches and real Pit actions; whole stereo waveform, original DAC/ROM,14channel source clock, full packet/port/ADSP and all prior actual faults pass. New direct Main140 constructor/movie/impact/voice ownership and104 actual native metadata/source counterexamples pass. Whole original five goal groups remain active.',
               actualCurrentBothCharactersBothSlotsOriginalSubzeroPitAudioAccepted=True,
               exactStereoPCMFrames=3863040,actualAudioSourceWindowFaultsRejected=116,actualEarnedStateFaultsRejected=48,
               actualRawMixedPCMFaultsRejected=16,actualMixedSourceOperationFaultsRejected=16,actualDirectNativeOwnerFaultsRejected=104,
               directlyObservedMain140OwnershipAccepted=True,allNativePitCuePriorityAndRNGAccepted=False,
               stockVictimRGBAccepted=False,completeStageVictimAudioAccepted=False,
               allVictimsArenasMovesCPURepeatedFinishersAccepted=False,fullPortAcceptance=False,
               newNativeBoots=4,newBuilds=0,newRawRecordings=0,newDeletedFiles=0,publicPlayableChanged=False,publicZIPChanged=False,
               exactCapturedNativeProcessesStillLive=[],observedOtherOrReusedPIDs=jobs,
               consumedNativeCaptureSessions=[73206,96857,98725,16231],consumedQualifierSessions=[22377,68148],
               sealedTextFiles=len(sealed),sealedAllocatedBytesBefore=before,sealedAllocatedBytesAfter=after,
               sealedAllocatedBytesReclaimed=before-after,
               next='Continue wider native Pit/Tomb victim/effect/voice integration and genuinely observed audio priority/RNG branches, stock-victim movie raster where missing; preserve remaining move/arena/CPU/KO/overlap, finisher/victim/morph/secret/cinematic, already verified natural campaigns/own endings, final UI/ladder/names/audio/dependency cleanup and matching refreshed release ZIP. Do not re-run completed finite contexts merely for status or regenerate permanently retired raw/build/source history.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(progress,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
      'Additive full-scope journal losslessly sealed')
 print(json.dumps({k:v for k,v in progress.items()if k not in('newInputHashes','remaining','cases')},indent=2),flush=True)

if __name__=='__main__':run()
