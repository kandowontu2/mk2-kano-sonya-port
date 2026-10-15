"""Recursive full-objective checkpoint after native scene/cold campaign proof."""
import hashlib,json,re,subprocess
from pathlib import Path
from PIL import Image
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v3847_native_mileena_fix_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3888_mileena_scene_campaign_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable full-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins={}
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],'Full natural-character scope remains open')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);digest=sha(path)
        need(wanted is None or digest==wanted,'Actual executed evidence unchanged '+key)
        need(key not in pins or pins[key]==digest,'Consistent fresh evidence pin')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Inherited evidence not relabelled')
        pins[key]=digest
    reports={}
    for leaf in('audit_v3868_mileena_native_scene_observed','audit_v3880_mileena_native_scene_matrix_observed','audit_v3871_mileena_fixed_sonya_campaign_checked','audit_v3884_mileena_native_scene_fifo_checked','audit_v3886_mileena_scene_campaign_compression'):
        file=ROOT/leaf/'report.json';value=json.loads(file.read_text());need(value['passed'],'Actual qualified native evidence '+leaf);pin(file);reports[leaf]=value
        for p,h in value.get('inputHashes',{}).items():pin(p,h)
        for case in value.get('cases',[]):
            for p,h in case.get('inputHashes',{}).items():pin(p,h)
    scenes=reports['audit_v3884_mileena_native_scene_fifo_checked'];campaign=reports['audit_v3871_mileena_fixed_sonya_campaign_checked']['cases'][0]
    need(scenes['actualContexts']==4 and scenes['exactFields']==336 and scenes['actualRowFaultsRejected']==40 and scenes['actualNativeVictimArtFIFOProjectionDisplayEraseAccepted'],'Four complete source/FIFO/projection/render/native erase contexts and actual-row counterexamples')
    need(campaign['bounded_campaign_evidence_proven']and not campaign['unassisted_clear_proven']and campaign['stages_reached']==list(range(13))and campaign['actualNativeSwallowingSequences']==2 and campaign['globalCacheOverruns']==0 and campaign['originalPreCorruptionChronologyAccepted'],'Actual long campaign gate remains bounded, not falsely called clear')
    need(not reports['audit_v3871_mileena_fixed_sonya_campaign_checked']['currentBothP2NaturalClearAccepted'],'Unfinished natural Sonya tower still explicit')
    # Bind the four small visual review sheets back to complete actual RGB
    # transfers; cropping here reads a QA artifact and never edits any sprite.
    reviews=[]
    for fighter,side,prefix,reviewdir,filename in(
        ('kano',1,'audit_v3867','art_review_mileena_v3869','kano-native-swallowing-review.png'),
        ('kano',2,'audit_v3878','art_review_mileena_v3879','kano-p2-native-swallowing-review.png'),
        ('sonya',1,'audit_v3878','art_review_mileena_v3879','sonya-p1-native-swallowing-review.png'),
        ('sonya',2,'audit_v3878','art_review_mileena_v3879','sonya-p2-native-swallowing-review.png')):
        folder=ROOT/f'{prefix}_mileena_{fighter}_p{side}_native_scene_ram';visible=json.loads((folder/'visible_digests.json').read_text())
        digests={int(re.search(r'_(\d+)\.png$',r['file'])[1]):r['rgbSHA256']for r in visible}
        observed=reports['audit_v3868_mileena_native_scene_observed']if side==1 and fighter=='kano'else next(c for c in reports['audit_v3880_mileena_native_scene_matrix_observed']['cases']if c['fighter']==fighter and c['side']==side)
        frames=[frame for _,frame in sorted(observed['actualPhaseFrames'].items())]+[max(digests)]
        review=ROOT/reviewdir/filename;image=Image.open(review).convert('RGB')
        for i,frame in enumerate(frames):
            x,y=(i%2)*400,(i//2)*278
            raw=image.crop((x,y+24,x+400,y+278)).tobytes()
            need(hashlib.sha256(raw).hexdigest().upper()==digests[frame],'Every essential native QA panel exactly equals original complete captured RGB')
        pin(review);reviews.append(dict(fighter=fighter,side=side,nativePanels=len(frames),path=str(review),sha256=sha(review),everyPanelEqualsActualRGB=True))
    leaves=('audit_v3851_mileena_fixed_sonya_p2_campaign','audit_v3852_mileena_fixed_sonya_campaign_observed','audit_v3856_mileena_native_scene_observed','audit_v3860_mileena_native_scene_observed','audit_v3864_mileena_native_scene_observed','audit_v3867_mileena_kano_p1_native_scene_ram','audit_v3882_mileena_native_scene_fifo_checked')
    for leaf in leaves:
        for p in(ROOT/leaf).rglob('*'):
            if p.is_file():pin(p)
    for fighter,side in(('kano',2),('sonya',1),('sonya',2)):
        for p in(ROOT/f'audit_v3878_mileena_{fighter}_p{side}_native_scene_ram').rglob('*'):
            if p.is_file():pin(p)
    for file in('mk2ks_mileena_campaign_trace_v3848.lua','mk2ks_mileena_campaign_ram_v3849.lua','tools/run_mileena_fixed_sonya_campaign_v3850.py','mk2ks_mileena_native_scene_ram_v3853.lua','tools/run_mileena_native_scene_ram_v3854.py','tools/run_mileena_native_scene_ram_v3858.py','tools/run_mileena_native_scene_ram_v3862.py','tools/run_mileena_native_scene_ram_v3866.py','tools/verify_mileena_fixed_sonya_campaign_v3870.py','mk2ks_mileena_native_scene_ram_v3872.lua','tools/run_mileena_native_scene_matrix_v3873.py','tools/run_mileena_native_scene_matrix_v3877.py','tools/verify_mileena_native_scene_fifo_v3881.py','tools/verify_mileena_native_scene_fifo_v3883.py','tools/compact_mileena_scene_campaign_v3885.py','tools/save_mileena_scene_campaign_checkpoint_v3887.py'):pin(ROOT/file)
    public={
        'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
        'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
        'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
        'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
        'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
        'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
        'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}
    for p,h in public.items():pin(ROOT/p,h)
    pin(ROOT/state['currentCMD']);pin(PARENT)
    storage=reports['audit_v3886_mileena_scene_campaign_compression'];pids=storage['captureChildrenMissing']
    check=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,pids))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(check.returncode==0 and not check.stdout.strip(),'Exact actual five capture handles missing now; do not interfere with unrelated compiler tasks')
    state['inputHashes']=pins
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=pins[str(PARENT)],mergeRule='Resolve parent recursively; preserve retired/deleted exclusions and agree on shared fresh pins; do not flatten.'),previousCheckpoint=str(PARENT),
        previousGoalTurnClassification='progress: native owned swallowing data/source fix built3836, actual original victim streams/state accepted; next cold campaign was confirmed started. The intervening acknowledgment response made no additional progress.',
        thisGoalTurnClassification='progress: re-polled same live SonyaP2 handle48600 to terminal0 at322771frames; independent unchanged whole native campaign gate passes9actual-row faults and273166pre-corruption original chronology events, two real swallowing sequences complete without global cache stores. No tower clear claimed. Continuous native CPU/DMA/shift/scanout replay passes336fields in four actual earned contexts, source palettes retain true stock5 and actual17/18 identities. Independent FIFO/composite/camera/projection/native disappearance-order gate passes40actual-row faults and proves no later victim body/shadow pixels. Viewed four essential native QA sheets, source-bound every panel to actual RGB. Checker parser/legacy pre-count/within-field ordering failures and syntax source retained honestly. No game/build edits or new playable payload; sealed logs compressed without deleting/relabeling evidence,12.8MiB reclaimed. Full five-group objective stays active.',
        gameSourceAndPlayableBytesChangedThisTurn=False,
        currentDevelopmentNativeMileenaPixelsFIFOProjectionCleanupAccepted=True,
        currentDevelopmentNativeMileenaPixelsReport=str(ROOT/'audit_v3884_mileena_native_scene_fifo_checked/report.json'),
        currentDevelopmentNativeMileenaExactFields=336,currentDevelopmentNativeMileenaExactRGBPixels=336*400*254,currentDevelopmentNativeMileenaPixelRowFaultsRejected=40,
        currentDevelopmentNativeMileenaHumanReview=dict(scope='Normal Dead Pool, physical slots1/2, all7Kano/8Sonya swallowing phases plus native erase. Own black/red and green/black/white costumes retained; observed original mouth clipping/flip/progression. No all-arena/aesthetic/universal-shadow/audio promotion.',panels=reviews,allFourSheetsViewed=True),
        currentDevelopmentBoundedSonyaP2CampaignStateAccepted=True,currentDevelopmentBoundedSonyaP2CampaignReport=str(ROOT/'audit_v3871_mileena_fixed_sonya_campaign_checked/report.json'),
        currentDevelopmentBoundedSonyaP2Campaign=dict(terminalFrame=322771,originalPreCorruptionEvents=273166,stagesReached=list(range(13)),paidContinues=80,nativeRoundWins=35,nativeCollisionDamageStores=4059,trueOwnedRingEntries=1450,actualSwallowingSequences=2,globalCacheOverruns=0,actualRowFaultsRejected=9),
        currentDevelopmentSonyaP2FullTowerClearAccepted=False,currentDevelopmentCampaignRegressionAccepted=False,
        currentDevelopmentMileenaRasterArtShadowAudioAccepted=False,currentDevelopmentWholePortRegressionAccepted=False,
        currentTurnReclaimedAllocatedBytes=storage['reclaimedAllocatedBytes'],currentTurnDeletedFiles=0,currentTurnNewBuilds=0,
        currentTurnActualCaptureRasterFiles=0,currentTurnActualCaptureAudioFiles=0,currentTurnEssentialNativeQAReviewPNGs=4,
        preservedSceneCheckerFailures={'3854':'Legacy parser import-order missing hex entry; no game launched.','3858':'Legacy missing first_source hex; no game launched.','3862':'Retained native chronology contains4pre-pass targets for3snapshots, not old hard-coded3pre. All4source targets replay exact in3866, no omitted/re-anchored buffer.','3873':'Syntax-only failed source, preserved. Fresh3877 executed three actual contexts.','3881':'Same-field final FIFO draw precedes native removal; field-only cutoff wrongly rejected it. Exact line-order proof3883 prohibits every actual publication after removal while preserving original preceding draw.'},
        pendingNativeMileenaCapture=None,pendingNativeMileenaBuild=None,pendingNativeMileenaQualifier=None,pendingSonyaCampaign=None,
        confirmedMissingThisTurnCapturePIDs=pids,
        nextImplementationAction='Continue broader native victim/finisher and audio/floor-shadow fidelity on3836; qualify unchanged combined selection/ladder/lifebar names/audio and all moves/arenas. Improve only physical human test controls to earn natural SonyaP2 Kintaro/Shao tower/own ending, never game/AI/health assists. Re-test affected scopes, dependency-aware obsolete cleanup and release ZIP only after full objective acceptance.',
        fullPortAcceptance=False,finishedRelease=False,goalStatus='active')
    need(state['remaining']==remaining and state['currentCandidate']=='diagnostic_v1836_ball_register_boundary','All original remaining groups and public launch preserved')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compression before write')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n');print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),freshPins=len(pins),goalStatus='active',exactNativeSceneFields=336,naturalSonyaP2Clear=False,fullPortAcceptance=False)))

if __name__=='__main__':main()
