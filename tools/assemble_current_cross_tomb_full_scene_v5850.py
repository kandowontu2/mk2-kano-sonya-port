"""Current opposite-character Tomb whole scenes; original full goal remains active.
Derived from the complete5824 matrix, with actual cross IDs/palettes and both
observed unpressed branches. No new game writes, outcome normalization or builds.
"""
import datetime,gzip,hashlib,inspect,json,re,subprocess
from pathlib import Path
import run_current_cross_tomb_render_ram_v5847 as runtime
ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha
OUT=ROOT/'audit_v5851_current_cross_tomb_full_scene_matrix_progress'

# Live CIM observations: names, creation times and complete commands were inspected before polling.
INITIAL_IDENTITIES={
 "kano1": {
  "hostPID": 152820,
  "hostCreated": "2026-10-08T03:39:33.291829-04:00",
  "pid": 148448,
  "created": "2026-10-08T03:39:43.009938-04:00"
 },
 "kano2": {
  "hostPID": 139004,
  "hostCreated": "2026-10-08T03:39:33.458393-04:00",
  "pid": 125384,
  "created": "2026-10-08T03:39:43.179827-04:00"
 },
 "sonya1": {
  "hostPID": 138940,
  "hostCreated": "2026-10-08T03:39:33.404419-04:00",
  "pid": 144032,
  "created": "2026-10-08T03:39:43.077604-04:00"
 },
 "sonya2": {
  "hostPID": 103952,
  "hostCreated": "2026-10-08T03:39:33.458825-04:00",
  "pid": 151988,
  "created": "2026-10-08T03:39:43.179340-04:00"
 }
}

def records(text,tag):
 rows=[]
 for line in text.splitlines():
  if not line.startswith(tag+' '):continue
  pairs=re.findall(r'(\w+)=([^\s]+)',line);row=dict(pairs)
  need(len(row)==len(pairs),'Every actual whole-scene provenance row has unique keys')
  rows.append(row)
 return rows

def run():
 need(not OUT.exists(),'Fresh immutable current scene matrix')
 guest=runtime.current.expected()
 parentpath=ROOT/'audit_v5845_current_cross_tomb_enabled_audio_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and
  parent['allPriorMirrorHeldPressedRandomFullScenesRetained'],
  'Whole retained actual enabled audio/state/ending/move/UI/campaign evidence and original full objective')
 pins=dict(parent['newInputHashes']);pins[str(parentpath)]=sha(parentpath)
 need(all(sha(p)==h for p,h in pins.items()),'Every parent actual source/evidence retained')
 audio_path=ROOT/'audit_v5843_current_cross_tomb_audio_checked/report.json'
 audio=json.loads(audio_path.read_text())
 need(audio['passed']and len(audio['cases'])==4,'Complete current original unpressed native audio/state matrix')
 pins[str(audio_path)]=sha(audio_path);cases=[];processes=[];sealed=[]
 need(runtime.contract_source==inspect.getsource(runtime.old.scene_contract).replace(
  "old=(reference/'run.log').read_text(encoding='utf-8-sig')",
  "with gzip.open(reference/'run.log.gz','rt')as reader:old=reader.read()",1)and
  runtime.scene_contract.__globals__['model']is runtime.model and
  runtime.scene_contract.__globals__['native']is runtime.native and
  runtime.scene_contract.__globals__['gzip']is gzip,
  'Whole original3648scene/source/FIFO/projection/ground/shadow/retirement contract unchanged except gzip reference IO')
 need(runtime.model.source==inspect.getsource(runtime.model.original.Model).replace(
  'len(self.ids)==2 and set(self.ids)=={17,18}','self.ids in ((17,18),(18,17),(17,17),(18,18))'),
  'Whole continuous native one-base VRAM/CPU/DMA/shift/palette/RGB model retained; only exact mirror tuple admission')
 for fighter,side in (('kano',1),('kano',2),('sonya',1),('sonya',2)):
  folder,output=runtime.paths(fighter,side);path=output/'report.json'
  report=json.loads(path.read_text());meta=json.loads((folder/'result.json').read_text())
  process=json.loads((folder/'process.json').read_text());processes.append(process)
  initial=INITIAL_IDENTITIES[fighter+str(side)]
  need(process['pid']==initial['pid']and process['hostPID']==initial['hostPID']and
   abs(process['startedUnix']-datetime.datetime.fromisoformat(initial['created']).timestamp())<.05,
   'Exact native/host identities independently observed live, not guessed from stale PID')
  ref=next(c for c in audio['cases']if c['fighter']==fighter and c['physicalSlot']==side)
  identity=17 if fighter=='kano'else 18
  need(report['passed']and report['actualCurrentOppositeNativeTombWholeRenderPaletteShadowEraseAccepted']and
   report['candidate']==runtime.current.NAME and report['fighter']==fighter and report['side']==side and
   report['truePhysicalIDs']==[identity if s==side else 35-identity for s in(1,2)]and not report['fullPortAcceptance']and
   not report['allMirrorBranchesAndSlotsAccepted']and not report['completeStageVictimAudioAccepted'],
   'Actual complete current rendered case with exact true slot IDs; broader art/audio acceptance not inferred')
  need(meta['captureCompleted']and meta['exit_code']==0 and not meta['modelErrors']and
   meta['modelExactFields']==meta['observedRGBFields']==report['sampledFrames']and
   meta['guest_writes']==0 and meta['assistance']=='none'and not meta['cheats_enabled']and
   meta['ramGuestSHA256']==runtime.current.GUEST_SHA and meta['executable_sha256']==runtime.current.EXE_SHA and
   meta['payload_sha256']==runtime.current.PAYLOAD_SHA and (folder/'stderr.log').read_text()==''and
   '-samples'in process['command']and '-nocheat'in process['command']and
   process['command'][0]==str(ROOT/runtime.current.NAME/'mkport_candidate.exe'),
   'Current whole guest/executable/payload and real unassisted normal terminal, no proxy/deadline')
  scene,branch=report['nativeScene'],report['nativeBranch']
  need(branch==ref['sourceQualifiedNativeBranch']and branch['trueVictim']==35-identity and
   scene['nativeInputState']==branch['earnedContract']and scene['nativeDrop']==branch['nativeDrop']and
   0<=scene['actualNativeRandomValue']==branch['actualNativeRandomValue']<1000 and
   ((branch['nativeDrop']and scene['nativeMotion']==branch['nativeMotion']['phase']and
      scene['nativeMotion']['checkedConsecutiveCallbacks']==269)or
    (not branch['nativeDrop']and scene['nativeMotion']['ceiling']==branch['nativeMotion']['ceiling']and
      scene['nativeMotion']['heldCallbacks']==branch['nativeMotion']['continuousArena1MotionCallbacks']>400))and
   report['sampledFrames']==scene['retired']-scene['origin']+30>500 and
   report['exactRGBPixels']==report['sampledFrames']*400*254 and
   report['nativeCrossPaletteSelectors']=={'1':[False],'2':[False]}and report['oneInitialBaseOnly']and
   report['laterTargetsNeverUsedAsAnchors']and report['nativeShiftLoads']==report['nativeShiftFills']>0 and
   report['fullPhysicalPaletteChecks']>report['sampledFrames']and scene['nativeShadowCopies']>0 and
   all(int(scene['ownedBodyDispatches'][str(s)])>100 for s in (1,2)),
   'Complete retirement+30 whole scene, every native projection/cache source/mirror palette, original ground/shadow/erase gates')
  need({f['kind']for f in report['actualPixelFaultsRejected']}=={'VRAM target bit','visible RGB bit'}and
   report['sourcePreflight']['observerSHA256']==runtime.controls()and
   report['sourcePreflight']['modelSHA256']==runtime.model.MODEL_SOURCE_SHA256 and
   report['sourcePreflight']['sceneContractSHA256']==hashlib.sha256(runtime.contract_source.encode()).hexdigest().upper(),
   'Actual full raster counterexamples and exact complete observer/model/contract bytes retained')
  with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
  need('MK2_CURRENT_TOMB_RENDER_DEADLINE'not in text and 'hex='not in text,
   'Actual native terminal and RAM-only raw transport; no shortened host deadline')
  need(runtime.branches.branch(text,guest,fighter,side)==branch and
   len(runtime.native.actual_faults(text,fighter,side,guest))==12 and
   len(runtime.branches.faults(text,guest,fighter,side))==4 and
   len(runtime.audio_proof.phase_faults(text,guest,fighter,side)if branch['nativeDrop']else [])==(4 if branch['nativeDrop']else 0)and
   report['sourcePreflight']['earnedContractSHA256']==runtime.native.CONTRACT_SHA256,
   'Independent entire true-ID earned/801cleanup, original unpressed RNG/source/PC/IO/continuous held phase and actual negative gates')
  with gzip.open(Path(ref['capture'])/'run.log.gz','rt')as reader:audio_text=reader.read()
  physical=('MK2_STAGE_BOOT ','MK2_STAGE_INPUT ','MK2_STAGE_DAMAGE ','MK2_STAGE_MATCH ',
   'MK2_STAGE_SELECT ','MK2_STAGE_SELECT_ID ','MK2_STAGE_WINDOW ','MK2_STAGE_COMMAND ','MK2_STAGE_RESULT ')
  need([l for l in text.splitlines()if l.startswith(physical)]==
   [l for l in audio_text.splitlines()if l.startswith(physical)],
   'Every actual physical selection/paid match/damage/command/retirement record agrees with independent current enabled audio capture')
  visible=json.loads((folder/'continuous_scene_records.json').read_text())
  digests=json.loads((folder/'visible_digests.json').read_text())
  need(len(visible)==len(digests)==report['sampledFrames']and
   [r['frame']for r in visible]==list(range(scene['origin']+1,scene['retired']+31))and
   all(r['exactVRAMWords']==512*512 and r['exactRGBPixels']==400*254 and
    r['rgbSHA256']==d['rgbSHA256']and d['file']==f"display_{r['frame']}.png"
    for r,d in zip(visible,digests,strict=True)),
   'Every consecutive full VRAM and actual visible RGB digest through retirement+30, no omitted target field')
  for p,h in report['inputHashes'].items():
   need((p not in pins or pins[p]==h)and sha(p)==h,'Consistent exact native/current source and rendered evidence pins');pins[p]=h
  for p in [path,*folder.rglob('*')]:
   if not p.is_file():continue
   need(p.suffix.lower()not in ('.png','.wav','.bin','.pcm','.rgb','.exe','.zip','.mdata'),
    'No raw scene/audio/guest/GFX or duplicate build/source archive')
   pins[str(p.resolve())]=sha(p)
   if p.suffix.lower()in ('.json','.log','.cfg','.txt'):sealed.append(p)
  cases.append(dict(fighter=fighter,physicalSlot=side,capture=str(folder),report=str(path),
   wholeVisibleFields=report['sampledFrames'],exactVisibleRGBPixels=report['exactRGBPixels'],
   sourceBoundProjections=scene['sourceBoundProjections'],nativeShadowCopies=scene['nativeShadowCopies'],
   nativeShiftTransfers=report['nativeShiftTransfers'],nativeMotion=scene['nativeMotion'],
   actualNativeRandomValue=scene['actualNativeRandomValue'],nativeCrossPaletteSelectors=report['nativeCrossPaletteSelectors'],
   actualEarnedFaultsRejected=12,actualBranchFaultsRejected=4,actualHeldMotionFields=scene['nativeMotion'].get('heldCallbacks',0),nativeDrop=branch['nativeDrop'],actualDropPhaseFaultsRejected=4 if branch['nativeDrop']else 0,actualRasterFaultsRejected=2))
 pids=sorted({p[k]for p in processes for k in ('pid','hostPID')})
 query="Get-CimInstance Win32_Process -Filter '"+' OR '.join(f'ProcessId={p}'for p in pids)+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 raw=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(raw)if raw else []
 if isinstance(jobs,dict):jobs=[jobs]
 for p in processes:
  need(not any(j['ProcessId']==p['pid']and j['Name']=='mkport_candidate.exe'and
   abs(j['createdUnix']-p['startedUnix'])<.05 and 'mk2ks_current_cross_tomb_display_ram_v5846.lua'in(j['CommandLine']or'')
   for j in jobs),'Every exact native rendering process terminal, no timeout inference')
  need(not any(j['ProcessId']==p['hostPID']and j['Name']=='python.exe'and
   'run_current_cross_tomb_render_ram_v5847.py'in(j['CommandLine']or'')for j in jobs),
   'Every exact RAM renderer/model host terminal')
 for p in (Path(__file__),Path(runtime.__file__),runtime.OBSERVER):
  pins[str(p.resolve())]=sha(p);sealed.append(p)
 runtime.current.expected()
 need(all(sha(p)==h for p,h in pins.items()),'Every whole current, dirty-restoration, public launcher/ZIP and retained evidence byte unchanged')
 sealed=list(dict.fromkeys(p.resolve()for p in sealed));before={str(p):sha(p)for p in sealed}
 for p in sealed:
  need(p.is_relative_to(ROOT.resolve())and subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0,
   'Exact bounded immutable text losslessly compacted')
 need(all(sha(p)==h for p,h in before.items()),'Every sealed full evidence/source byte unchanged')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  parentAdditiveJournal=str(parentpath),remaining=parent['remaining'],cases=cases,newInputHashes=pins,
  previousGoalTurnClassification=parent['thisGoalTurnClassification'],
  thisGoalTurnClassification='progress: four actual current opposite-character Tomb whole scenes completed. Both observed player-one native random-drop and player-two held branches match independent current enabled-audio references. Entire one-base CPU/DMA/shift/VRAM/palette/RGB, body/composite/cache/projection/ground/compressed native floor-shadow and retirement+30 gates passed, including real target faults and full earned/PC/IO/actor/Main/branch/phase faults. Full original five-group scope remains active.',
  actualCurrentBothCharactersBothSlotsOppositeTombFullSceneGroundShadowEraseAccepted=True,
  actualCurrentHeldPressedAndRandomMirrorFullScenesRetained=True,
  actualCrossHeldScenes=sum(not c['nativeDrop']for c in cases),actualCrossRandomDropScenes=sum(c['nativeDrop']for c in cases),
  wholeVisibleFields=sum(c['wholeVisibleFields']for c in cases),
  exactVisibleRGBPixels=sum(c['exactVisibleRGBPixels']for c in cases),
  nativeOwnedShadowCopies=sum(c['nativeShadowCopies']for c in cases),
  actualEarnedFaultsRejected=48,actualBranchFaultsRejected=16,actualRasterFaultsRejected=8,
  actualDropPhaseFaultsRejected=sum(c['actualDropPhaseFaultsRejected']for c in cases),
  allCurrentCrossHeldPressedRandomFullScenesAccepted=False,broaderPitTombVictimsAccepted=False,
  fullMovePhaseAllArenaCPURepeatedKOOverlapAccepted=False,completeStageVictimAudioAccepted=False,
  independentStockChoreographyAndAllCinematicsAccepted=False,fullPortAcceptance=False,
  rawNativeGuestRGBVRAMPCMFilesWritten=0,newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,publicZIPChanged=False,
  exactCaptureProcessesStillLive=[],observedOtherOrReusedPIDs=jobs,consumedCaptureToolSessions=[91097,53813,16842,61026],
  sealedTextSourcesLosslesslyCompacted=len(sealed),initialLiveProcessIdentities=INITIAL_IDENTITIES,
  next='Do not rerun completed mirror or these four opposite-character scenes for status. Continue the remaining opposite held/random slots and physical pressed branches, broader native Pit/Tomb stock victims, source audio priority/RNG choice and independent stock choreography. Preserve all original full move/arena/CPU/repeated/KO/overlap, finisher/victim/morph/secret/cinematic, retained natural campaign/endings and final combined selection/ladder/names/audio regression plus dependency-aware cleanup and refreshed release ZIP. Never regenerate permanently retired build/raw history.')

if __name__=='__main__':
 report=run();OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(report,indent=2)+'\n')
 digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
  'New whole-scope evidence journal losslessly compacted')
 print(json.dumps({k:v for k,v in report.items()if k not in ('remaining','newInputHashes','cases')},indent=2),flush=True)
