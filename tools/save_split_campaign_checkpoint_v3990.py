"""Recursive full-scope checkpoint: actual split semantics and failed campaign.

Four own victims/two true stock controls in Dead Pool only. This checkpoint
does not promote the development fix or claim universal finisher fidelity.
"""
import hashlib,json,re,subprocess
from pathlib import Path
from PIL import Image
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v3957_kitana_audio_campaign_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3991_split_campaign_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins={}
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],'Full original natural-character objective unchanged')
    def pin(p,wanted=None):
        p=Path(p).resolve();key=str(p);digest=sha(p)
        need(wanted is None or digest==wanted,'Exact executed evidence unchanged '+key)
        need(key not in pins or pins[key]==digest,'Consistent fresh pin')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Inherited evidence not relabelled')
        pins[key]=digest
    reports={}
    for leaf in ('audit_v3949_sonya_close_leg_campaign_observed','audit_v3951_sonya_close_leg_campaign_checked','audit_v3972_kung_lao_split_native_scene_observed','audit_v3999_kung_lao_split_earned_grammar_checked','audit_v3979_terminal_split_campaign_compression','audit_v3995_kung_lao_split_native_fifo_checked','audit_v3989_kung_lao_split_matrix_compression'):
        p=ROOT/leaf/'report.json';r=json.loads(p.read_text());need(r['passed']and not r.get('fullPortAcceptance',False),'Completed bounded qualification '+leaf);reports[leaf]=r;pin(p)
        for path,h in r.get('inputHashes',{}).items():pin(path,h)
        for c in r.get('cases',[]):
            for path,h in c.get('inputHashes',{}).items():pin(path,h)
    campaign=reports['audit_v3951_sonya_close_leg_campaign_checked']['cases'][0]
    need(campaign['bounded_campaign_evidence_proven']and not campaign['unassisted_clear_proven']and campaign['stages_reached']==[0]and campaign['native_own_round_wins']==0 and campaign['paid_continue_losses']==144 and campaign['native_special_moves']=={'leg':312}and len(campaign['actualRowCounterexamplesRejected'])==9,'Closer human test-controller result is zero-win observation, never a clear')
    observed=reports['audit_v3972_kung_lao_split_native_scene_observed'];earned=reports['audit_v3999_kung_lao_split_earned_grammar_checked'];fifo=reports['audit_v3995_kung_lao_split_native_fifo_checked']
    need(len(observed['cases'])==6 and earned['actualContexts']==6 and earned['ownContexts']==4 and earned['stockContexts']==2 and earned['actualRecordFaultsRejected']==84 and earned['stockHeldWinnerPageSemanticsAccepted'],'Six source-bound native contexts and all84 actual state/constructor faults')
    need(fifo['actualContexts']==4 and fifo['exactFields']==2560 and fifo['actualRowFaultsRejected']==64 and fifo['actualNativeVictimArtFIFOProjectionHeldDisplayAccepted'],'Four actual own contexts, every primary/mirrored descriptor/FIFO/camera/DMA/floor field, native compressed shadow rows and64 actual faults')
    reviews=[]
    for c in observed['cases']:
        fighter,side=c['fighter'],c['side'];folder=ROOT/f'audit_v3971_kung_lao_{fighter}_p{side}_native_scene_ram'
        visible=json.loads((folder/'visible_digests.json').read_text());digests={int(re.search(r'_(\d+)\.png$',r['file'])[1]):r['rgbSHA256']for r in visible}
        need(c['exactFields']==len(visible)==640,'Whole continuous actual native scene')
        frames=[f for _,f in sorted(c['actualPhaseFrames'].items())]+[max(digests)]
        review=ROOT/'art_review_split_v3973'/f'{fighter}-p{side}-native-split-review.png';image=Image.open(review).convert('RGB')
        need(image.size==(800,1668)and len(frames)==11,'Eleven essential native QA panels only')
        for i,frame in enumerate(frames):
            x,y=(i%2)*400,(i//2)*278
            need(hashlib.sha256(image.crop((x,y+24,x+400,y+278)).tobytes()).hexdigest().upper()==digests[frame],'Every reviewed panel equals exact original native RGB')
        pin(review);reviews.append(dict(fighter=fighter,side=side,stockReferenceOnly=c['stockReferenceOnly'],path=str(review),sha256=sha(review),nativePanels=11,everyPanelEqualsActualRGB=True))
        for p in folder.rglob('*'):
            if p.is_file():pin(p)
    for leaf in ('audit_v3948_sonya_close_leg_p2_campaign','audit_v3961_kung_lao_kano_p1_native_scene_ram','audit_v3967_kung_lao_kitana_p1_native_scene_ram','audit_v3962_kung_lao_split_native_scene_observed','audit_v3968_kung_lao_split_native_scene_observed'):
        for p in (ROOT/leaf).rglob('*'):
            if p.is_file():pin(p)
    need(not json.loads((ROOT/'audit_v3962_kung_lao_split_native_scene_observed/report.json').read_text())['passed']and not json.loads((ROOT/'audit_v3968_kung_lao_split_native_scene_observed/report.json').read_text())['passed'],'Both initial semantic/palette failures retained as failures')
    for name in ('mk2ks_stock_extended_earned_ram_v3958.lua','mk2ks_split_native_scene_ram_v3959.lua','tools/run_kung_lao_split_native_scene_v3960.py','mk2ks_split_native_scene_ram_v3965.lua','tools/run_kung_lao_split_native_scene_v3966.py','tools/run_kung_lao_split_native_scene_v3970.py','tools/verify_kung_lao_split_earned_grammar_v3974.py','tools/verify_kung_lao_split_earned_grammar_v3976.py','tools/compact_terminal_split_campaign_v3978.py','tools/verify_kung_lao_split_native_fifo_v3980.py','tools/verify_kung_lao_split_native_fifo_v3982.py','tools/verify_kung_lao_split_native_fifo_v3984.py','tools/verify_kung_lao_split_native_fifo_v3986.py','tools/compact_kung_lao_split_matrix_v3988.py','tools/save_split_campaign_checkpoint_v3990.py'):pin(ROOT/name)
    for name in ('tools/verify_kung_lao_split_earned_grammar_v3992.py','tools/verify_kung_lao_split_earned_grammar_v3996.py','tools/verify_kung_lao_split_earned_grammar_v3998.py','tools/verify_kung_lao_split_native_fifo_v3994.py','tools/verify_native_split_grammar_v1100.py'):pin(ROOT/name)
    failed=ROOT/'audit_v3997_kung_lao_split_earned_grammar_checked/report.json'
    need(not json.loads(failed.read_text())['passed'],'Original slot-parity checker failure retained');pin(failed)
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();guest=(ROOT/'audit_v3948_sonya_close_leg_p2_campaign/guest_maincpu.bin').read_bytes()
    lo,hi=(0xff877730-0xff800000)//8,(0xff877800-0xff800000)//8
    need(hashlib.sha256(guest).hexdigest().upper()=='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'and guest[lo:hi]==stock[lo:hi],'Whole actual guest and unchanged original input-parser postincrement word-load/comparison instructions')
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
    storage=[reports['audit_v3979_terminal_split_campaign_compression'],reports['audit_v3989_kung_lao_split_matrix_compression']]
    pids=[p for r in storage for p in r['captureChildrenMissing']]
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,pids))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'Every exact sealed emulator handle missing now; unrelated processes untouched')
    reclaimed=sum(r['reclaimedAllocatedBytes']for r in storage)
    state['inputHashes']=pins
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=pins[str(PARENT)],mergeRule='Resolve parent recursively; preserve retired/deleted exclusions and agree on shared fresh pins; do not flatten.'),previousCheckpoint=str(PARENT),
        previousGoalTurnClassification='progress:3957 four current Kitana native audio contexts/eight captures,76 actual faults,424 source-bound DCS bytes and paired fullPCM; qualified prior leg campaign,6.9MiB reclaimed and exact closer-leg campaign live.',
        thisGoalTurnClassification='progress: reused exact recorded closer-leg capture/qualifier handles to terminal. Actual322771-field campaign has0 own wins,144 paid losses,312 true leg entries,4753 native collision damage stores/stage0 only; nine actual faults qualify bounded stability, not clear. Correctly preserved initial split zero-pixel cleanup assertion failure and stock palette expectation failure. Actual two stock controls independently demonstrate the frozen native WIN page retains victim halves after both physical pointers clear; all four true17/18 contexts match that behavior without new rendering. Full original1021 physical commands/two earned rounds; whole3625 native CPU/DMA/shift/scanout replay3840 fields/390144000 RGB pixels;84 actual state/constructor faults across six contexts and64 independent FIFO/projection/shadow/grounding faults across four own contexts. Original same half stream/mirror/six-field cadence and ordinary MAIN0 constructor seed preserved; native allocator reuse/temporary winner hat MAIN owner are source/lifetime qualified, not proxy exemptions. All six essential eleven-panel QA sheets viewed and each panel bound to actual RGB. No game/build/EXE/payload edits. Nine terminal capture leaves losslessly sealed; full five remaining groups and public1836 unchanged.',
        gameSourceAndPlayableBytesChangedThisTurn=False,
        currentDevelopmentNativeKungLaoSplit=dict(scope='Dead Pool, own17/18 victims in both physical slots; two genuine stock controls KitanaP1/LiuP2. No all-arena, full audio or all-finisher claim.',ownContexts=4,stockReferenceContexts=2,exactOwnFields=2560,exactAllFields=3840,exactOwnRGBPixels=260096000,exactAllRGBPixels=390144000,actualStateConstructorFaultsRejected=84,actualFIFOProjectionShadowFaultsRejected=64,actualOriginalHeldWinnerPageSemanticsAccepted=True,noNewVictimRenderingAfterPointerTeardown=True,sourceSeedIsOrdinaryMain0=True,sameNativeHalfStreamMirrored=True),
        currentDevelopmentNativeKungLaoSplitStateReport=str(ROOT/'audit_v3999_kung_lao_split_earned_grammar_checked/report.json'),currentDevelopmentNativeKungLaoSplitFIFOReport=str(ROOT/'audit_v3995_kung_lao_split_native_fifo_checked/report.json'),
        currentDevelopmentNativeKungLaoSplitHumanReview=dict(allSixSheetsViewed=True,nativePanels=66,scope='Ten native full/half phases plus frozen Fatality page, Dead Pool only. Stock and own controls remain separately labelled; no universal aesthetic acceptance.',panels=reviews),
        completedSonyaCloseLegP2Campaign=dict(terminalFrame=322771,stagesReached=[0],nativeRoundWins=0,paidContinues=144,trueNativeLegEntries=312,nativeCollisionDamageStores=4753,actualRowFaultsRejected=9,towerClear=False,report=str(ROOT/'audit_v3951_sonya_close_leg_campaign_checked/report.json')),
        pendingSonyaCampaign=None,
        preservedSplitCheckerFailures=['3960 incorrectly asserted all physical victim pixels must vanish after pointer teardown. Actual renderer was exact; six fresh own/stock contexts prove unchanged native frozen WIN-page behavior. Original failure remains false.','3966 expected stock normal/alt palette after headless palette activation. Actual native Kitana death palette is FFAE0020. Fresh3970 binds original table/code/pointer/actor and exact queue-event ordering; original failure remains false.'],
        preservedSplitStateCheckerFailure='3996 assumed both native scheduler slots consume the victim table at age76. Actual original stock KitanaP1 is76/first-half166 and LiuP2 is77/first-half167. Fresh3998 enforces exact slot-specific parity for all six contexts; wrong original failure remains false. Earlier immutable preflights also preserved original true-ID MAIN0 table extension, original left/right command tables and A11 postincrement cursor; no live-input data edits.',
        currentTurnReclaimedAllocatedBytes=reclaimed,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnActualCaptureRasterFiles=0,currentTurnActualCaptureAudioFiles=0,currentTurnEssentialNativeQAReviewPNGs=6,currentTurnNativeGuestMemoryDumpFiles=0,retainedEarlierNativeCampaignGuestDumpFiles=1,
        confirmedMissingThisTurnCapturePIDs=pids,currentDevelopmentSonyaP2FullTowerClearAccepted=False,currentDevelopmentCampaignRegressionAccepted=False,currentDevelopmentWholePortRegressionAccepted=False,
        nextImplementationAction='Continue original Kung Lao split complete native victim/effect audio and other finisher/victim/morph/secret/cinematic contexts. Use only genuine physical input plans for the unresolved Sonya P2 tower; gap63 leg trial is poorer, not a clear. Fresh future campaigns must use independently whole-byte-qualified guest RAM transport rather than an ordinary diagnostic dump. Complete full-move/all-arena grounding/floor shadows/cleanup and combined selection/ladder/names/audio regression. Dependency-aware obsolete-folder cleanup and refreshed ZIP remain required after full scope proof.',fullPortAcceptance=False,finishedRelease=False,goalStatus='active')
    need(state['remaining']==remaining and state['currentCandidate']=='diagnostic_v1836_ball_register_boundary','Full original scope and public launch retained')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before write')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n');print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),freshPins=len(pins),ownSplitContexts=4,stockContexts=2,stateFaults=84,fifoFaults=64,reclaimedAllocatedBytes=reclaimed,goalStatus='active',fullPortAcceptance=False)),flush=True)

if __name__=='__main__':main()
