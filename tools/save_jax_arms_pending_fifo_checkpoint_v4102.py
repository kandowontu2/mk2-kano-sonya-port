"""Full-scope progress checkpoint; exact current FIFO qualifier stays live."""
import json,subprocess
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v4072_jax_native_audio_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4103_jax_arms_scene_state_stock_live_fifo_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable active-goal checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins={}
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],'Complete original natural-character objective, not partial-proof release acceptance')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);digest=sha(path)
        need(wanted is None or digest==wanted,'Exact accepted evidence bytes unchanged '+key)
        need(key not in pins or pins[key]==digest,'Consistent current exact pins')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Shared inherited bytes unchanged')
        pins[key]=digest
    pin(PARENT);reports={}
    for leaf in('audit_v4076_jax_arms_native_scene_observed','audit_v4079_jax_arms_earned_checked','audit_v4083_jax_arms_native_review_panels_checked',
                'audit_v4092_jax_arms_stock_corner_observed','audit_v4099_jax_arms_stock_corner_checked','audit_v4101_jax_arms_stock_corner_compression','audit_v4105_jax_arms_terminal_scene_compression'):
        p=ROOT/leaf/'report.json';r=json.loads(p.read_text());need(r['passed']and not r['fullPortAcceptance'],'Actual completed bounded native proof '+leaf);reports[leaf]=r;pin(p)
        if 'inputHashes'in r:
            for p,h in r['inputHashes'].items():pin(p,h)
        else:
            for case in r['cases']:
                for p,h in case['inputHashes'].items():pin(p,h)
    scene=reports['audit_v4076_jax_arms_native_scene_observed'];earned=reports['audit_v4079_jax_arms_earned_checked'];review=reports['audit_v4083_jax_arms_native_review_panels_checked']
    stock=reports['audit_v4099_jax_arms_stock_corner_checked'];storage=reports['audit_v4105_jax_arms_terminal_scene_compression'];stock_storage=reports['audit_v4101_jax_arms_stock_corner_compression']
    need(len(scene['cases'])==4 and sum(c['exactFields']for c in scene['cases'])==2432 and sum(c['exactRGBPixels']for c in scene['cases'])==247091200,'Four complete608field actual native own body/arm scenes, no skipped targets')
    need(earned['actualContexts']==4 and earned['actualNativeStateAndPropFaultsRejected']==52 and earned['originalCompleteEarnedStateAndPropPaletteAlgorithmRetained'],'Entire original1074 physical command/health/147field/6table/2prop normal palette state grammar and52 faults')
    need(review['exactNativePanels']==44 and not review['aestheticAcceptance']and not review['stockVictimCornerPlacementComparisonAccepted'],'All44 essential panels nativeRGB-bound, not universal art/placement approval')
    need(stock['actualStockContexts']==2 and stock['actualAddedCharacterContexts']==0 and stock['actualRowFaultsRejected']==14 and stock['actualNativePanels']==12 and
         stock['actualStockArmlessStandingVictimHeldWINBehaviorObserved']and not stock['ownCornerArtPositionAccepted']and not stock['fullStockSceneReplayAccepted'],'Two actual Kitana4 native reference controls, original held standing-victim semantics, not own relabels or broad fidelity')
    for leaf in('audit_v4081_jax_arms_native_fifo_checked','audit_v4095_jax_arms_stock_corner_checked','audit_v4097_jax_arms_stock_corner_checked'):
        p=ROOT/leaf/'report.json';r=json.loads(p.read_text());need(r['passed']is False,'Original sequencing/table/slot failures preserved, never reclassified green');pin(p)
    need(storage['captureFolders']==4 and stock_storage['captureFolders']==2 and storage['deletedFiles']==stock_storage['deletedFiles']==0,'Six exact terminal capture leaves sealed losslessly, no deletions')
    missing=storage['captureChildrenMissing']+stock_storage['captureChildrenMissing']+[120504]
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,missing))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'Exact native captures and original-state qualifier terminal/missing now')
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process -Filter "ProcessId=137548" | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0 and q.stdout.strip(),'Exact current independent FIFO process confirmed live now')
    live=json.loads(q.stdout);need(live['ProcessId']==137548 and live['Name']=='python.exe'and 'tools/verify_jax_arms_native_fifo_v4086.py'in live['CommandLine'],'Correct exact current FIFO process, not stale PID or unrelated work')
    before=(ROOT/'tools/verify_jax_arms_native_fifo_v4080.py').read_text();after=(ROOT/'tools/verify_jax_arms_native_fifo_v4086.py').read_text()
    need(before.replace("OUT=ROOT/'audit_v4081_jax_arms_native_fifo_checked'","OUT=ROOT/'audit_v4087_jax_arms_native_fifo_checked'")==after,'Fresh current FIFO source is identical unweakened algorithm, only unused output leaf differs')
    for name in('mk2ks_jax_arms_native_scene_ram_v4073.lua','tools/run_jax_arms_native_scene_v4074.py','tools/verify_jax_arms_earned_v4078.py',
                 'tools/verify_jax_arms_native_fifo_v4080.py','tools/verify_jax_arms_native_fifo_v4086.py','tools/verify_jax_arms_review_panels_v4082.py',
                 'tools/compact_jax_arms_scene_matrix_v4084.py','tools/save_jax_arms_checkpoint_v4088.py','mk2ks_jax_arms_stock_corner_ram_v4090.lua',
                 'tools/run_jax_arms_stock_corner_v4091.py','tools/verify_jax_arms_stock_corner_v4094.py','tools/verify_jax_arms_stock_corner_v4096.py',
                 'tools/verify_jax_arms_stock_corner_v4098.py','tools/compact_jax_arms_stock_corner_v4100.py','tools/compact_jax_arms_terminal_scenes_v4104.py','tools/save_jax_arms_pending_fifo_checkpoint_v4102.py'):pin(ROOT/name)
    for relative,wanted in {
      'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
      'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
      'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
      'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
      'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
      'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
      'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}.items():pin(ROOT/relative,wanted)
    pin(ROOT/state['currentCMD']);reclaimed=storage['reclaimedAllocatedBytes']+stock_storage['reclaimedAllocatedBytes']
    state.update(inputHashes=pins,inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='Resolve parent recursively; preserve all retired/deleted exclusions and agree on fresh shared pins; do not flatten.'),previousCheckpoint=str(PARENT),
      previousGoalTurnClassification='progress:4072 full native Jax clap audio four contexts/eight captures,128 original selectors/280 delivered DCS bytes/120 faults and lossless5.8MiB log seal.',
      thisGoalTurnClassification='progress: four complete original earned Jax arm-rip native scenes,2432 consecutive fields/247091200 RGB pixels exact; all ten own body/arm phases. Entire original1074 command/two322HP collision rounds/147field completion/six native tables/two genuine normal prop palette consumers and52 faults accepted. Four essential11-panel native sheets main-agent viewed and all44 actualRGB panels bound. Focused actual stock Kitana4 both-slot controls confirm standing armless victim/final held WIN page is original behavior, not an overlay bug. Six stock native body/arm/position tables and12 native panels accepted with14 actual faults; no original-stock whole-scene/audio or own corner art approval. Own placement row is24pixels farther out than Kitana; relevant stock profiles/full edge positioning remain unaccepted. Native secret row16 boundary is instruction-shaped original bytes; secret consumer ABI not implied valid by own17/18 tests. Complete3994/811 physical FIFO/floor/shadow plus actual separate prop-source/cadence/DMA algorithm preflight passed K1/K2/S1/S2; final60-fault full qualifier137548/exec1558 is confirmed live, not completed. Initial4081 prerequisite sequencing failure and4095 missed-body-table fault/4097 P2draw-parity expectation failures preserved; corrected sources use fresh leaves and stronger full six-table/actual slot-parity checks. Six exact terminal captures losslessly sealed,54194176allocated bytes reclaimed; no game/build/public changes, new builds, native dump files or deletions.',
      currentDevelopmentNativeJaxArmsSceneReport=str(ROOT/'audit_v4076_jax_arms_native_scene_observed/report.json'),
      currentDevelopmentNativeJaxArmsStateReport=str(ROOT/'audit_v4079_jax_arms_earned_checked/report.json'),
      currentDevelopmentNativeJaxArmsSceneQualified=dict(ownContexts=4,fullNativeRGBFields=2432,exactRGBPixels=247091200,allTenBodyArmSourcePhasesPresented=True,actualOriginalStatePropFaultsRejected=52,essentialNativeSheets=4,all44PanelsNativeBound=True,mainAgentViewedAllFour=True,
        scope='Normal Dead Pool own17/18 victims/both slots. Complete original scene/earned-state/normal prop palette; final FIFO/floor/shadow fault qualification still live. No universal art/corner/alternate/audio/all-arena/ending/full-port approval.'),
      currentDevelopmentNativeJaxArmsFocusedStockReport=str(ROOT/'audit_v4099_jax_arms_stock_corner_checked/report.json'),
      currentDevelopmentNativeJaxArmsStockControl=dict(actualStockContexts=2,actualAddedContexts=0,trueStockVictim=4,actualNativePanels=12,actualFaultsRejected=14,mainAgentViewedBoth=True,normalStandingArmlessVictimAndHeldWINObserved=True,
        actualStockPositionRow='000AFF88',actualStockPositionConsumeAgeBySlot={'1':40,'2':41},ownPositionRow='0005FF70/0004FF70',ownXDisplacementDifferenceFromKitana=24,wholeStockSceneReplayAccepted=False,ownCornerArtPositionAccepted=False),
      nativeJaxArmsStockRow16BoundaryNote=dict(positionRow16='57B009E0',positionTableGuestByteOffset='FBA50',status='Unchanged copied original bytes, instruction-shaped word at original table boundary. Actual own17/18 and stock4 are consumed here. Do not infer secret Jade16 validity; verify original secret alias/table ABI in remaining secret/morph cases before any change.'),
      pendingJaxArmsQualification=dict(execSession=1558,pid=137548,liveProcess=live,source=str(ROOT/'tools/verify_jax_arms_native_fifo_v4086.py'),result=str(ROOT/'audit_v4087_jax_arms_native_fifo_checked/report.json'),expectedActualContexts=4,expectedActualFaults=60,completed=False),
      preservedJaxArmsPrerequisiteFailure=str(ROOT/'audit_v4081_jax_arms_native_fifo_checked/report.json'),
      currentTurnReclaimedAllocatedBytes=reclaimed,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnNewNativeAudioRasterROMCopies=0,confirmedMissingThisTurnCapturePIDs=missing,
      nextImplementationAction='Poll exact exec1558/PID137548 final native arm-rip FIFO/floor/811-shadow/prop fault qualifier; it is confirmed live now, do not restart based on elapsed observation. If terminal, inspect actual4087 report/case counts before acceptance. Terminal capture leaves already sealed in4105 and4101; do not double-count their reclaimed space. Final checkpoint must inherit4103, not draft4088 parent4072; use fresh source/output and preserve its52state/14stock faults, live-handle history, storage and failed reports. Continue full original arm-rip victim/effect/audio and relevant native stock-profile/center/edge positioning/facing comparisons; stock Kitana standing/armless held WIN is normal, but different placement is not automatically a bug or art approval. Never use optional controlled-alt guest-write observer or restore retired1046/1071 outputs. Remaining finisher/victim/morph/secret/cinematic/audio fidelity, complete multi-arena moves/ground/shadows/cleanup, actual SonyaP2 whole-tower clear and own ending/attract, final combined selection/ladder/names/audio, dependency-aware obsolete folder cleanup and refreshed ZIP remain required.',
      gameSourceAndPlayableBytesChangedThisTurn=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active')
    need(state['remaining']==remaining and state['currentCandidate']=='diagnostic_v1836_ball_register_boundary','Original full scope and public executable retained')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),freshPins=len(pins),ownContexts=4,nativeRGBFields=2432,actualOriginalStateFaults=52,actualFocusedStockFaults=14,liveNativeFIFOQualifierPID=137548,liveExecSession=1558,reclaimedAllocatedBytes=reclaimed,goalStatus='active',fullPortAcceptance=False)),flush=True)

if __name__=='__main__':main()
