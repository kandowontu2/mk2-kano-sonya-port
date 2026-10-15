"""Actual unpressed native mirror drops; all original port requirements retained."""
import ctypes,json,subprocess
from pathlib import Path
import run_tomb_mirror_random_drop_render_ram_v4460 as render
ROOT,need,sha=render.ROOT,render.need,render.sha
PARENT=ROOT/'audit_v4451_sonya_p2_native_tower_ending_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4464_tomb_mirror_random_drop_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable full-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()),'Every inherited original requirement/evidence byte unchanged')
    def pin(p,wanted=None):
        p=Path(p).resolve();key=str(p);h=sha(p)
        need((wanted is None or h==wanted) and (key not in pins or pins[key]==h),'Exact shared actual bytes');pins[key]=h
    pin(PARENT);pin(__file__)
    contexts=[]
    for fighter,delay in (('kano',10),('sonya',4)):
        path=ROOT/f'audit_v4459_tomb_mirror_random_drop_checked/{fighter}_p1_delay{delay:02d}/report.json'
        proof=json.loads(path.read_text());pin(path)
        native=proof['nativeBranch']
        need(proof['passed'] and proof['nativeRandomDropStateAndOriginal801CleanupAccepted'] and
             proof['fighter']==fighter and proof['side']==1 and proof['physicalCommandDelay']==delay and
             native['nativeDrop'] and 0<=native['actualNativeRandomValue']<50 and
             native['nativeMotion']['phase']['checkedConsecutiveCallbacks']==269 and
             native['earnedContract']['consecutive_fields']==801 and not proof['fullPortAcceptance'] and
             len(proof['actualOriginalFullEarnedFaultsRejected'])==12 and
             len(proof['actualOriginalBranchPCActorMainIOFaultsRejected'])==4 and
             len(proof['actual269PhaseFaultsRejected'])==4,
             'Both genuine true-mirror P1 rare branches, complete native original contracts and actual faults')
        for p,h in proof['inputHashes'].items():pin(p,h)
        contexts.append(dict(fighter=fighter,side=1,report=str(path),capture=proof['capture'],
                             physicalDelay=delay,nativeBranch=native))
    path=render.OUT/'report.json';scene=json.loads(path.read_text());pin(path)
    need(scene['passed'] and scene['current3836KanoP1RandomDropMirrorNativeTombWholeRenderPaletteShadowEraseAccepted'] and
         scene['nativeBranch']==contexts[0]['nativeBranch'] and scene['nativeScene']['nativeDrop'] and
         scene['sampledFrames']==scene['nativeScene']['retired']-scene['nativeScene']['origin']+30 and
         scene['oneInitialBaseOnly'] and scene['laterTargetsNeverUsedAsAnchors'] and
         scene['nativeMirrorPaletteSelectors']=={'1':[False],'2':[True]} and
         scene['rawImageAudioVRAMROMCopiesWritten']==0 and not scene['completeStageVictimAudioAccepted'] and
         not scene['allMirrorBranchesAndSlotsAccepted'] and not scene['fullPortAcceptance'],
         'Entire original native continuous scene/model/FIFO/owned shadow/erase gates, no broadened acceptance')
    for p,h in scene['inputHashes'].items():pin(p,h)
    for p in render.timing.OUT.rglob('*'):
        if p.is_file():pin(p)
    for name in ('tools/qualify_tomb_mirror_random_drop_v4458.py','tools/find_tomb_mirror_native_random_drop_v4455.py',
                 'mk2ks_tomb_mirror_random_timing_driver_ram_v4453.lua',
                 'mk2ks_tomb_mirror_random_timing_provenance_ram_v4454.lua',
                 'mk2ks_tomb_mirror_random_drop_display_ram_v4457.lua'):pin(ROOT/name)
    query="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'find_tomb_mirror_native_random_drop_v4455.py|qualify_tomb_mirror_random_drop_v4458.py|run_tomb_mirror_random_drop_render_ram_v4460.py|audit_v4456_|audit_v4461_' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    active=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(active.returncode==0 and not active.stdout.strip(),'All actual search/state/render jobs terminal, no observation-timeout restart')
    allocated_api=ctypes.windll.kernel32.GetCompressedFileSizeW
    allocated_api.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];allocated_api.restype=ctypes.c_uint32
    files=[p for folder in (render.CASE,render.OUT,render.timing.OUT,ROOT/'audit_v4459_tomb_mirror_random_drop_checked')
           for p in folder.rglob('*') if p.is_file()]
    allocated=0
    for p in files:
        hi=ctypes.c_uint32();lo=allocated_api(str(p),ctypes.byref(hi));need(lo!=0xffffffff,'Exact allocated current evidence bytes')
        allocated+=(hi.value<<32)|lo
    next_action=('Both added characters now have actual unpressed rare Tomb mirror drop state/phase/801field '
      'cleanup in P1, with native RNG30Kano/41Sonya, unpressed IO, original source-entry PCs, true victim '
      'actor/Main and complete269callback motion. Only ordinary command wait changed10/4fields; no '
      'RNG/health/AI/roster/position/guest writes. Sixteen actual timing trials remain honestly classified '
      'as14held/2drop, not as statistical RNG proof. KanoP1 random-drop whole native scene is now '
      'source-perfect through retirement+30: original continuous CPU/FIFO/DMA/shift/one-base VRAM/RGB/'
      'palette/body/floor/compressed-shadow/erase gates retained; actual P1normal/P2alternate palette, '
      'full physical controls identical to qualified rare-drop reference. Do not rerun this completed '
      'KanoP1 scene or completed held/pressed mirror matrices or accepted SonyaP2 natural tower. Next '
      'use the already qualified SonyaP1 delay4reference for the still missing whole random-drop '
      'render scene, and obtain actual unpressed P2mirror RNG drops for both characters through '
      'fresh ordinary command timing leaves before full render/audio qualification. Preserve whole '
      'original earned gates and all actual pixel/branch/motion counterexamples. Remaining native '
      'stage/victim complete DCS waveform, broader Pit/Tomb stock victims/branches, full move art/'
      'ground/floor shadows/CPU/repeat/KO/overlap across arenas, other finishers/victims/morphs/'
      'secrets/cinematics, complete ending transition/audio/all build contexts and final combined '
      'selection/ladder/names/audio/dependency cleanup/refreshed release all remain. All five original '
      'goal groups stay intact, public1836 unchanged playtest, no new ROM/exe/raw media copies and '
      'no historical cleanup savings counted again.')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
        mergeRule='Every original full-goal requirement/evidence/strict exclusion retained; actual P1 rare Tomb mirror branches and KanoP1 whole scene added.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: ordinary input timing discovers true unpressed RNG30/41 mirror drops for Kano/Sonya P1; complete original native state/phase/cleanup/faults pass, and KanoP1 full native scene art/palette/floor/shadow/erase is verified through retirement+30.',
      current3836P1UnpressedRandomTombMirrorDropStateContexts=contexts,
      current3836KanoP1UnpressedRandomTombMirrorWholeRenderAccepted=True,
      current3836KanoP1UnpressedRandomTombMirrorRenderReport=str(path),
      current3836KanoP1UnpressedRandomTombMirrorNativeShadowCopies=scene['nativeScene']['nativeShadowCopies'],
      current3836SonyaP1UnpressedRandomTombMirrorWholeRenderAccepted=False,
      current3836P2UnpressedRandomTombMirrorCoverageAccepted=False,
      current3836TrueMirrorTombAllDropAndPressedBranchesAccepted=False,
      currentTurnDiagnosticLogicalBytes=sum(p.stat().st_size for p in files),currentTurnDiagnosticAllocatedBytes=allocated,
      currentTurnNewBuilds=0,currentTurnRawAudioRasterVRAMROMCopies=0,currentTurnDeletedFiles=0,
      currentTurnReclaimedAllocatedBytes=0,cleanupAccounting='Only compressed source/text/digest evidence; native guest/scene RAM-only. No deletion and no previous498825626byte cache saving recounted.',
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      nextAction=next_action,nextImplementationAction=next_action,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'All original scope groups intact')
    need(all(sha(p)==h for p,h in pins.items()),'Every inherited/current source/public input unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
                    'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),inputPins=len(pins),
      actualP1RareDropStateContexts=2,KanoP1FullRareDropSceneAccepted=True,
      sampledFields=scene['sampledFrames'],currentEvidenceAllocatedBytes=allocated,
      originalRemainingGroups=5,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
