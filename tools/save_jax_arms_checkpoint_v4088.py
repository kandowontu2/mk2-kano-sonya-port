"""Preserve complete original scope after bounded normal native arm-rip proofs."""
import json,subprocess
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v4072_jax_native_audio_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4089_jax_arms_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable active-goal checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins={}
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],'Full original natural-character objective remains incomplete')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);digest=sha(path)
        need(wanted is None or digest==wanted,'Exact accepted evidence bytes unchanged '+key)
        need(key not in pins or pins[key]==digest,'Consistent fresh proof pins')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Shared inherited inputs unchanged')
        pins[key]=digest
    pin(PARENT);reports={}
    for leaf in('audit_v4076_jax_arms_native_scene_observed','audit_v4079_jax_arms_earned_checked','audit_v4087_jax_arms_native_fifo_checked',
                'audit_v4083_jax_arms_native_review_panels_checked','audit_v4085_jax_arms_scene_matrix_compression','audit_v4092_jax_arms_stock_corner_observed',
                'audit_v4099_jax_arms_stock_corner_checked','audit_v4101_jax_arms_stock_corner_compression'):
        p=ROOT/leaf/'report.json';r=json.loads(p.read_text());need(r['passed']and not r['fullPortAcceptance'],'Actual complete bounded original proof '+leaf);reports[leaf]=r;pin(p)
        if 'inputHashes'in r:
            for p,h in r['inputHashes'].items():pin(p,h)
        else:
            for case in r['cases']:
                for p,h in case['inputHashes'].items():pin(p,h)
    scene=reports['audit_v4076_jax_arms_native_scene_observed'];earned=reports['audit_v4079_jax_arms_earned_checked'];fifo=reports['audit_v4087_jax_arms_native_fifo_checked']
    review=reports['audit_v4083_jax_arms_native_review_panels_checked'];storage=reports['audit_v4085_jax_arms_scene_matrix_compression']
    need(len(scene['cases'])==4 and sum(c['exactFields']for c in scene['cases'])==2432 and sum(c['exactRGBPixels']for c in scene['cases'])==247091200,'Every actual native body/arm RGB field in four real victim/slot contexts')
    need(earned['actualContexts']==4 and earned['actualNativeStateAndPropFaultsRejected']==52 and earned['originalCompleteEarnedStateAndPropPaletteAlgorithmRetained'],'Complete original1074 command/health/147field/6table/2prop palette algorithm and52 faults')
    need(fifo['actualContexts']==4 and fifo['actualRowFaultsRejected']==60 and not fifo['allArenaFloorShadowsAccepted'],'Complete generic physical FIFO/floor/811 compressed shadow plus actual two-prop source/cadence/DMA proof and60 faults, not all arenas')
    projections=sum(c['nativeFIFO']['sourceBoundProjections']for c in fifo['cases']);prop_draws=sum(c['nativeDetachedProps']['originalPropDMAs']for c in fifo['cases'])
    need(projections==13000 and prop_draws==3912 and all(c['nativeDetachedProps']['sourceBoundPropFIFO']==978 and
         c['nativeDetachedProps']['nativeFourFieldCadenceAccepted']and not c['nativeDetachedProps']['separatePropWorldCameraProjectionAccepted']for c in fifo['cases']),'All native physical projections and3912 actual separate prop FIFO/DMA consumers; prop world transform not falsely claimed')
    need(review['exactNativePanels']==44 and review['exactNativePanelPixels']==4470400 and not review['aestheticAcceptance']and not review['stockVictimCornerPlacementComparisonAccepted'],'44 essential sheets are actual native RGB, not broad art/stock corner acceptance')
    need(storage['captureFolders']==4 and storage['deletedFiles']==storage['newPlayableCopies']==0,'Terminal scene data sealed losslessly without deletion or build copy')
    failed=ROOT/'audit_v4081_jax_arms_native_fifo_checked/report.json';failure=json.loads(failed.read_text())
    need(failure['passed']is False and 'FileNotFoundError'in failure['error']and 'audit_v4079'in failure['traceback'],'Preserve original premature prerequisite failure, never turn it green')
    pin(failed)
    before=(ROOT/'tools/verify_jax_arms_native_fifo_v4080.py').read_text();after=(ROOT/'tools/verify_jax_arms_native_fifo_v4086.py').read_text()
    need(before.replace("OUT=ROOT/'audit_v4081_jax_arms_native_fifo_checked'","OUT=ROOT/'audit_v4087_jax_arms_native_fifo_checked'")==after,'Fresh terminal corrected proof uses identical unweakened algorithm, only unused output leaf changes')
    for name in('mk2ks_jax_arms_native_scene_ram_v4073.lua','tools/run_jax_arms_native_scene_v4074.py','tools/verify_jax_arms_earned_v4078.py',
                 'tools/verify_jax_arms_native_fifo_v4080.py','tools/verify_jax_arms_native_fifo_v4086.py','tools/verify_jax_arms_review_panels_v4082.py',
                 'tools/compact_jax_arms_scene_matrix_v4084.py','tools/save_jax_arms_checkpoint_v4088.py'):pin(ROOT/name)
    stock=reports['audit_v4099_jax_arms_stock_corner_checked'];stock_storage=reports['audit_v4101_jax_arms_stock_corner_compression']
    need(stock['actualStockContexts']==2 and stock['actualAddedCharacterContexts']==0 and stock['actualRowFaultsRejected']==14 and stock['actualNativePanels']==12 and
         stock['actualStockArmlessStandingVictimHeldWINBehaviorObserved']and not stock['ownCornerArtPositionAccepted']and not stock['fullStockSceneReplayAccepted'],'Actual stock held standing-victim behavior,14 faults and12 native panels, not own corner art/universal stock fidelity')
    for leaf in('audit_v4095_jax_arms_stock_corner_checked','audit_v4097_jax_arms_stock_corner_checked'):
        p=ROOT/leaf/'report.json';r=json.loads(p.read_text());need(r['passed']is False,'Preserve focused stock source/slot preflight failures unchanged');pin(p)
    for name in('mk2ks_jax_arms_stock_corner_ram_v4090.lua','tools/run_jax_arms_stock_corner_v4091.py','tools/verify_jax_arms_stock_corner_v4094.py',
                 'tools/verify_jax_arms_stock_corner_v4096.py','tools/verify_jax_arms_stock_corner_v4098.py','tools/compact_jax_arms_stock_corner_v4100.py'):pin(ROOT/name)
    reclaimed=storage['reclaimedAllocatedBytes']+stock_storage['reclaimedAllocatedBytes']
    missing=storage['captureChildrenMissing']+stock_storage['captureChildrenMissing']+[120504]
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,missing))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'All exact native children and original earned-state qualifier terminal/missing now')
    for relative,wanted in {
      'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
      'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
      'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
      'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
      'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
      'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
      'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}.items():pin(ROOT/relative,wanted)
    pin(ROOT/state['currentCMD'])
    state.update(inputHashes=pins,inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='Resolve parent recursively; preserve all retired/deleted exclusions and agree on fresh shared pins; do not flatten.'),previousCheckpoint=str(PARENT),
      previousGoalTurnClassification='progress:4072 complete four native Jax clap audio contexts/eight captures/128 source-bound selectors/280 DCS bytes/120 faults and lossless5.8MiB log seal.',
      thisGoalTurnClassification='progress:4074 original Jax arm-rip physically earned BBBB LP gap96, true17/18 victims/both slots, two actual161HP rounds and original147field completion. Four actual608field native CPU/DMA/shift/scanout scenes exact,2432fields/247091200RGBpixels. All five own body and five own arm sources presented; whole actual3836 guest compared inRAM, no native ROM/RGB/VRAM/PCM dump files. Original1073 only-read-only prop palette taps retained; controlled-alt1063 and retired1046 loader never used. Four essential eleven-panel contact sheets main-agent viewed and44 whole native RGB panels independently bound. Original1074 full earned-state/six table/two real prop normal palette/register/stack algorithm retained,52 actual faults rejected. Complete3994 generic physical FIFO/projection/floor/811 compressed native shadow algorithm plus two actual native prop single-descriptor/cadence/cursor/DMA contracts pass four cases and60 faults.13000 native physical projections and3912 actual detached-prop draws bound. Premature4080 gate failed before validation because original-state report was pending; preserve false4081 and unchanged source. Fresh4086 changes only unused output leaf and runs after original-state terminal report. Four terminal leaves losslessly sealed; no game/build/public bytes changed or new builds/deletions. Corner clipping seen in real QA retained as unaccepted stock-position/aesthetic comparison, not papered over by a pixel-match claim.',
      currentDevelopmentNativeJaxArmsSceneReport=str(ROOT/'audit_v4076_jax_arms_native_scene_observed/report.json'),
      currentDevelopmentNativeJaxArmsStateReport=str(ROOT/'audit_v4079_jax_arms_earned_checked/report.json'),
      currentDevelopmentNativeJaxArmsFIFOReport=str(ROOT/'audit_v4087_jax_arms_native_fifo_checked/report.json'),
      currentDevelopmentNativeJaxArmsQualified=dict(ownVictimContexts=4,actualContinuousNativeRGBFields=2432,exactNativeRGBPixels=247091200,originalEarnedStateAndPropFaults=52,actualFIFOPropFloorFaults=60,
        sourceBoundPhysicalProjections=13000,actualDetachedPropDraws=3912,allTenBodyArmSourcePhasesPresented=True,essentialNativeContactSheets=4,all44PanelsNativeBound=True,mainAgentViewedAllFour=True,
        floorShadowCopyCommands=sum(c['nativeFIFO']['floorShadowCopyCommands']for c in fifo['cases']),actualOwnCompressedShadowCopies=sum(c['nativeFIFO']['actualOwnedCompressedShadowRows']['copies']for c in fifo['cases']),
        scope='Normal Dead Pool original Jax arm-rip, both own victims/slots. Actual corner clipping visible; stock-victim corner positioning/art/aesthetic comparison remains unaccepted. No independent prop world/camera transform, alternate-costume, full audio/all-arena/all-finisher/ending/full-port acceptance.'),
      preservedJaxArmsPrerequisiteFailure=str(failed),pendingJaxArmsQualification=None,currentTurnReclaimedAllocatedBytes=reclaimed,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnNewNativeAudioRasterROMCopies=0,
      currentDevelopmentNativeJaxArmsFocusedStockReport=str(ROOT/'audit_v4099_jax_arms_stock_corner_checked/report.json'),
      currentDevelopmentNativeJaxArmsStockControl=dict(actualStockContexts=2,actualAddedContexts=0,actualTrueStockVictim=4,actualNativePanels=12,actualFaultsRejected=14,mainAgentViewedBoth=True,normalStockStandingArmlessVictimAndHeldWINObserved=True,
        actualNativeStockPosition='000AFF88',actualStockPositionConsumeAgeBySlot={'1':40,'2':41},ownPosition='0005FF70/0004FF70',ownXDisplacementDifferenceFromKitana=24,
        scope='Focused six native RGB epochs per genuine stock Kitana4 victim/slot, actual original command/322HP/147field completion/six stock table rows. Standing armless victim on final WIN page is normal stock behavior. Own closer-to-edge placement needs relevant original stock-profile/full corner facing comparison before any art/position change; no universal stock frame/audio fidelity claim.'),
      nativeJaxArmsStockRow16BoundaryNote=dict(positionRow16='57B009E0',positionTableGuestByteOffset='FBA50',status='Unchanged copied original bytes, instruction-shaped word at original table boundary. This proof only actually consumes own17/18. Do not infer valid secret Jade16 consumption; verify original secret alias/table ABI during remaining native secret/morph matrix before any change.'),
      confirmedMissingThisTurnCapturePIDs=missing,
      nextImplementationAction='Current original Jax arm-rip full native scenes, original earned-state/normal prop palette, physical FIFO/floor/shadow and actual separate prop source/cadence/DMA are qualified in four normal Dead Pool contexts. Before broad natural-position/art acceptance, compare actual stock victim Jax arm-rip corner behavior and true centered/edge facing positions; current QA visibly clips own victim at the edge. Do not infer correct appearance from exact replay alone or alter data merely to make a narrow test green. Full native arm-rip effect/voice/audio and actual normal/alternate branch controls remain needed; never use controlled-alt guest-write observer. Remaining original finisher/victim/morph/secret/cinematic cases, multi-arena complete move-phase/ground/shadow/cleanup, genuine SonyaP2 whole-tower clear/own endings, final combined selection/ladder/names/audio, dependency-aware obsolete-folder cleanup and refreshed ZIP are still required. Natural SonyaP2 next physical policy must respond to actual failing Mileena encounter, not repeat identical startup/strategy or alter AI/health/schedule.',
      gameSourceAndPlayableBytesChangedThisTurn=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active')
    need(state['remaining']==remaining and state['currentCandidate']=='diagnostic_v1836_ball_register_boundary','Original full scope and public playable retained')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),freshPins=len(pins),ownContexts=4,nativeRGBFields=2432,originalStatePropFaults=52,actualFIFOPropFaults=60,actualFocusedStockControls=2,reclaimedAllocatedBytes=reclaimed,goalStatus='active',fullPortAcceptance=False)),flush=True)

if __name__=='__main__':main()
