"""Seal four actual current Pit movies and grounding; preserve all open scope."""
import copy,datetime,gzip,hashlib,inspect,json,re,subprocess
from decimal import Decimal
from pathlib import Path
import qualify_current_cross_pit_movie_ground_v5912 as qualified
from record_current_cross_tomb_audio_v5844 import allocated
ROOT,need,sha,current=qualified.ROOT,qualified.need,qualified.sha,qualified.previous.current
OUT=ROOT/'audit_v5915_current_cross_pit_movie_ground_progress'
INITIAL={
 'kano1':dict(hostPID=20692,hostCreated='2026-10-08T05:26:10.859217-04:00',pid=151056,created='2026-10-08T05:26:19.792810-04:00'),
 'kano2':dict(hostPID=134172,hostCreated='2026-10-08T05:29:00.908927-04:00',pid=141048,created='2026-10-08T05:29:14.341500-04:00'),
 'sonya1':dict(hostPID=153848,hostCreated='2026-10-08T05:29:00.931902-04:00',pid=73924,created='2026-10-08T05:29:14.410040-04:00'),
 'sonya2':dict(hostPID=149240,hostCreated='2026-10-08T05:29:00.910336-04:00',pid=141040,created='2026-10-08T05:29:14.382939-04:00'),
}

def impact_pair(visual,audio,movie,victim):
 need(movie['actualID']==victim and victim in(17,18),'Actual independent true cinematic victim, no proxy')
 need(len(visual)==len(audio)==4,'Complete paired current native impact and victim high/low bytes')
 actor,main=(f"{movie[k]:08X}"for k in('actualActor','actualMain'))
 for v,a in zip(visual,audio):
  need(v['a8']==a['a8']==actor and v['a13']==a['a13']==main and v['mode']=='9' and
       v['value']==a['word'] and v['pc']==a['pc'] and v['mask']==a['mask']=='FFFF' and
       v['writes']==a['writes']=='0' and v['assistance']==a['assistance']=='none' and
       v['frame']==a['frame']==str(movie['impact']) and
       abs(Decimal(v['seconds'])-Decimal(a['seconds']))<=Decimal('.00000000051'),
       'Every actual current impact port byte/PC/actor/Main/frame/native clock matches independent Main+140 movie capture')
 return dict(passed=True,actualActor=actor,actualMain=main,trueVictim=victim,
             actualPairedImpactPortWords=[v['value']for v in visual],nativeClockMatched=True,
             audioObserverDirectMain140Capture=False,independentlyMatchedCinematicMain140ImpactEvidence=True)

def run():
 need(not OUT.exists(),'Fresh additive whole-scope Pit journal')
 current.expected()
 parentpath=ROOT/'audit_v5901_current_cross_pit_audio_progress/progress.json';parent=json.loads(parentpath.read_text())
 need(parent['passed'] and parent['goalStatus']=='active' and len(parent['remaining'])==5 and
      parent['actualCurrentBothCharactersBothSlotsPitWholeMixedAudioAccepted'],
      'Whole earlier current Pit audio and original goal preserved')
 pins={str(parentpath):sha(parentpath)};cases=[];processes=[];sealed=[]
 matrixpath=ROOT/'audit_v5899_current_cross_pit_winner_mix_checked/report.json';matrix=json.loads(matrixpath.read_text())
 need(matrix['passed'] and matrix['exactStereoPCMFrames']==3863040,'Whole independent audio matrix intact')
 for fighter,side in (('kano',1),('kano',2),('sonya',1),('sonya',2)):
  path=ROOT/f'audit_v5913_current_cross_pit_{fighter}_p{side}_movie_ground_checked/report.json'
  proof=json.loads(path.read_text());scene=proof['nativeScene'];movie=scene['movie'];expected=677 if side==1 else 676
  folder=Path(proof['capture']);meta=json.loads((folder/'result.json').read_text())
  need(proof['passed'] and proof['actualCurrentQualifiedNativePitMovieAndGroundingAccepted'] and
       proof['candidate']==current.NAME and proof['fighter']==fighter and proof['physicalSlot']==side and
       proof['retainedLiveExactFields']==meta['modelExactFields']==meta['observedRGBFields']==expected and
       proof['retainedLiveExactRGBPixels']==expected*101600 and meta['modelErrors']==[] and meta['exit_code']==0 and
       proof['retainedLiveActualPixelFaultGateCompleted'] and scene['nativeState']['earned_matches']==7 and
       scene['nativeState']['consecutive_fields']==801 and movie['actualID']==(18 if fighter=='kano'else 17) and
       len(scene['actualMoviePoses'])==len(scene['visiblyRenderedMoviePoses'])==6 and
       movie['fallingGroups']==20 and movie['impactGroups']==movie['initialPreloads']==1 and
       movie['actualMovieAddressRepurposed']==movie['nextScreen']+8 and
       len(scene['actualMovieFaultsRejected'])==31 and len(scene['actualNativePhaseGroundFaultsRejected'])==6 and
       len(scene['actualEarnedFaultsRejected'])==12 and scene['actualNativePhaseGround']['passed'] and
       scene['actualNativePhaseGround']['originalVictimFloorDisplacement']==1024 and
       scene['actualShadowInventory']['checked_copies']==scene['actualShadowInventory']['components']==0 and
       not proof['wholeNativePitShadowPolicyAccepted'] and not proof['completeNativePitSceneAccepted'] and
       not proof['completeStageVictimAudioAccepted'] and not proof['fullPortAcceptance'] and
       proof['newNativeBoots']==proof['newRastersReplayed']==0 and not proof['rawTargetsReconstructed'],
       'Whole actual retained current movie/phase-floor/corruption/cleanup evidence, no shadow/audio scope inflation')
  for p,h in proof['inputHashes'].items():
   need(p not in pins or pins[p]==h,'Consistent immutable native evidence');pins[p]=h
  pins[str(path)]=sha(path);sealed.append(path)
  process=json.loads((folder/'process.json').read_text());processes.append(process);initial=INITIAL[fighter+str(side)]
  need(process['pid']==initial['pid'] and process['hostPID']==initial['hostPID'] and
       abs(process['startedUnix']-datetime.datetime.fromisoformat(initial['created']).timestamp())<.1 and
       '-nocheat'in process['command'] and '-samples'in process['command'] and
       process['command'][-1]==str(ROOT/'mk2ks_current_cross_pit_display_ram_v5904.lua'),
       'Exact independently observed initial native identities and full case command')
  with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
  audio=next(c for c in matrix['cases']if c['fighter']==fighter and c['physicalSlot']==side)
  with gzip.open(Path(audio['capture'])/'run.log.gz','rt')as reader:audio_text=reader.read()
  def rows(t,tag):return [dict(re.findall(r'(\w+)=([^\s]+)',s))for s in t.splitlines()if s.startswith(tag+' ')]
  actor=f"{movie['actualActor']:08X}";frame=str(movie['impact'])
  visual=[r for r in rows(text,'MK2_NAT_CAMPAIGN_FLOOR_SOUND')if r['frame']==frame and r['a8']==actor]
  sounds=[r for r in rows(audio_text,'MK2_MAUDIO_SOUND')if r['frame']==frame and r['a8']==actor]
  pair=impact_pair(visual,sounds,movie,movie['actualID']);faults=[]
  for field,value,label in (('a8','00000000','foreign audio actor'),('a13','00000000','foreign audio Main'),
                            ('word','FF00','changed actual impact byte'),('seconds',str(Decimal(sounds[0]['seconds'])+Decimal('.000000001')),'changed native impact clock')):
   bad=copy.deepcopy(sounds);bad[0][field]=value
   try:impact_pair(visual,bad,movie,movie['actualID'])
   except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
   else:raise ValueError('Altered actual audio/visual impact pairing accepted '+label)
  need(len(faults)==4 and impact_pair(visual,sounds,movie,movie['actualID'])==pair,'Actual impact pairing positive restored')
  for p in folder.rglob('*'):
   if p.is_file()and p.suffix.lower()in('.json','.log','.txt'):sealed.append(p)
  failed=ROOT/f'audit_v5907_current_cross_pit_{fighter}_p{side}_render_checked/report.json'
  pins[str(failed)]=sha(failed);sealed.append(failed)
  cases.append(dict(fighter=fighter,physicalSlot=side,capture=str(folder),report=str(path),wholeLiveRGBFields=expected,
                    wholeLiveRGBPixels=expected*101600,movie=movie,sourceNativeGround=scene['actualNativePhaseGround'],
                    actualMovieFaultsRejected=31,actualGroundFaultsRejected=6,actualEarnedFaultsRejected=12,
                    impactPair=pair,actualImpactPairFaultsRejected=faults,observedShadowCopies=0,
                    wholeNativePitShadowPolicyAccepted=False,completeNativePitSceneAccepted=False))
 for module in (qualified,qualified.previous,qualified.previous.executed,qualified.contract,
                qualified.contract.previous,qualified.previous.model):
  path=Path(module.__file__).resolve();pins[str(path)]=sha(path);sealed.append(path)
 for leaf in ('tools/record_current_cross_pit_movie_ground_v5914.py','mk2ks_current_cross_pit_display_ram_v5904.lua',
              'audit_v5910_current_cross_pit_kano_p1_retained_scene_checked/report.json'):
  path=ROOT/leaf;pins[str(path)]=sha(path);sealed.append(path)
 generated=inspect.getsource(qualified.previous.run).replace(
  "proof=contract.scene_contract(scene,text,guest,payload,fighter,side,Path(ref['capture']),ids)",
  "proof=partial_contract(scene,text,guest,payload,fighter,side,Path(ref['capture']),ids)",1).replace(
  'actualCurrentCrossPitCompleteRetainedNativeSceneAccepted=True,',
  'actualCurrentQualifiedNativePitMovieAndGroundingAccepted=True,wholeNativePitShadowPolicyAccepted=False,completeNativePitSceneAccepted=False,',1)
 need(qualified.run.source==generated,'Whole independently inspected successor binding, no legacy failure rewritten')
 pids=sorted({p[k]for p in processes for k in('pid','hostPID')})
 query="Get-CimInstance Win32_Process -Filter '"+' OR '.join(f'ProcessId={p}'for p in pids)+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 output=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(output)if output else []
 if isinstance(jobs,dict):jobs=[jobs]
 for p in processes:
  need(not any(j['ProcessId']==p['pid'] and j['Name']=='mkport_candidate.exe' and
               'mk2ks_current_cross_pit_display_ram_v5904.lua'in(j['CommandLine']or'') and
               abs(j['createdUnix']-p['startedUnix'])<.1 for j in jobs),'Exact captured native job terminal')
  need(not any(j['ProcessId']==p['hostPID'] and j['Name']=='python.exe' and
               'run_current_cross_pit_render_ram_v5905.py'in(j['CommandLine']or'')for j in jobs),'Exact capture host terminal')
 current.expected();need(all(sha(p)==h for p,h in pins.items()),'All executed/current/compiled/failed/new bytes unchanged')
 sealed=list(dict.fromkeys(p.resolve()for p in sealed));before=sum(allocated(p)for p in sealed)
 for p in sealed:
  need(p.is_relative_to(ROOT)and subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0,
       'Lossless exact sealed text compression, no recovery/build duplicates')
 need(all(sha(p)==h for p,h in pins.items()),'Compression preserves every source/evidence byte')
 after=sum(allocated(p)for p in sealed)
 progress=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  parentAdditiveJournal=str(parentpath),remaining=parent['remaining'],cases=cases,
  previousGoalTurnClassification=parent['thisGoalTurnClassification'],
  thisGoalTurnClassification='progress: four actual current Pit complete one-base live CPU/DMA/shift/VRAM/palette/RGB scenes reached normal exit;2706wholefields274,929,600RGBpixels exact. All native Main+140 true cinematic ancestry/constructor/sixvisiblefall-impactposes/cache/FIFO/projection/gendercommands/shake/exit+30 validated. Correct original Main+200 ADDI400h launched-victim floor phase source-qualified.124actualmovie24floor48earned16impact-pair faults reject. Original wrong-Tomb-floor and zero-shadow failures preserved; native shadow suppression remains explicitly unverified, not waived. Original five full goal groups stay active.',
  actualCurrentBothCharactersBothSlotsPitMovieAndGroundingAccepted=True,
  wholeLiveRGBFields=2706,wholeLiveRGBPixels=274929600,actualMovieFaultsRejected=124,
  actualSourceNativeGroundFaultsRejected=24,actualEarnedFaultsRejected=48,actualImpactPairFaultsRejected=16,
  independentlyMatchedCinematicMain140ImpactEvidence=True,audioObserverDirectMain140Capture=False,
  wholeNativePitShadowPolicyAccepted=False,completeNativePitSceneAccepted=False,
  completeStageVictimAudioAccepted=False,allNativePitCuePriorityAndRNGAccepted=False,
  independentStockChoreographyAccepted=False,fullPortAcceptance=False,
  initialObservedNativeIdentities=INITIAL,exactCaptureProcessesStillLive=[],observedOtherOrReusedPIDs=jobs,
  consumedCaptureToolSessions=[63765,47648,2121,29354],consumedFailedSuccessorSessions=[85029],
  consumedQualifiedSuccessorSessions=[83178,31368,82704,37718],rawGuestRGBPCMFilesWritten=0,
  newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,publicZIPChanged=False,
  sealedTextSourcesLosslesslyCompacted=len(sealed),sealedAllocatedBytesBefore=before,sealedAllocatedBytesAfter=after,
  sealedAllocatedBytesReclaimed=before-after,newInputHashes=pins,
  next='Determine original Pit shadow suppression timing and ordinary arena6 floor-shadow behavior using native source and independent stock control; zero finish-window draws alone are not acceptance. Then broaden Pit/Tomb stock victims/mirrors and native priority/RNG/direct cue and actual audio Main+140 ownership as required. Retain all full move/arena/CPU/repeated/KO/overlap, other finisher/victim/morph/secret/cinematic, already verified natural campaigns/own endings, final UI/ladder/names/audio, dependency-aware cleanup and refreshed release ZIP requirements. Never recreate permanently retired raw/build history.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(progress,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
      'Whole additive journal losslessly compacted')
 print(json.dumps({k:v for k,v in progress.items()if k not in('cases','remaining','newInputHashes','initialObservedNativeIdentities')},indent=2),flush=True)

if __name__=='__main__':run()
