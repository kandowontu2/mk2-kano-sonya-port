"""Recursive bounded native inflation checkpoint; full objective remains active."""
import hashlib,json,re,subprocess
from pathlib import Path
from PIL import Image
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v3917_mileena_audio_campaign_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3938_inflation_campaign_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins={}
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance'] and not state['finishedRelease'],'Full original objective retained')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);digest=sha(path)
        need(wanted is None or digest==wanted,'Actual evidence unchanged '+key)
        need(key not in pins or pins[key]==digest,'Consistent fresh pin')
        need(key not in state['inputHashes'] or state['inputHashes'][key]==digest,'Inherited evidence not relabelled')
        pins[key]=digest
    reports={}
    for leaf in ('audit_v3922_kitana_inflation_native_scene_observed','audit_v3925_kitana_inflation_native_fifo_checked','audit_v3934_kitana_inflation_earned_state_checked','audit_v3929_sonya_later_start_campaign_checked','audit_v3936_inflation_campaign_compression'):
        file=ROOT/leaf/'report.json';value=json.loads(file.read_text());need(value['passed'],'Actual completed qualification '+leaf);pin(file);reports[leaf]=value
        for p,h in value.get('inputHashes',{}).items():pin(p,h)
        for case in value.get('cases',[]):
            for p,h in case.get('inputHashes',{}).items():pin(p,h)
    fifo=reports['audit_v3925_kitana_inflation_native_fifo_checked']
    need(fifo['actualContexts']==4 and fifo['exactFields']==2948 and fifo['actualRowFaultsRejected']==52 and fifo['actualNativeVictimArtFIFOProjectionDisplayEraseAccepted'],'Four source/FIFO/ground/shadow/cleanup contexts')
    earned=reports['audit_v3934_kitana_inflation_earned_state_checked']
    need(earned['passed'],'Native physical earned action/state checker passed')
    campaign=reports['audit_v3929_sonya_later_start_campaign_checked']['cases'][0]
    need(campaign['bounded_campaign_evidence_proven'] and not campaign['unassisted_clear_proven'] and campaign['stages_reached']==[0] and campaign['native_special_moves']=={'ring':1016},'Poor physical-controller campaign outcome is not a tower clear')
    reviews=[]
    for fighter,side in (('kano',1),('kano',2),('sonya',1),('sonya',2)):
        folder=ROOT/f'audit_v3921_kitana_{fighter}_p{side}_native_scene_ram'
        visible=json.loads((folder/'visible_digests.json').read_text())
        digests={int(re.search(r'_(\d+)\.png$',r['file'])[1]):r['rgbSHA256'] for r in visible}
        observed=next(c for c in reports['audit_v3922_kitana_inflation_native_scene_observed']['cases'] if c['fighter']==fighter and c['side']==side)
        frames=[frame for _,frame in sorted(observed['actualPhaseFrames'].items())]+[max(digests)]
        review=ROOT/'art_review_inflation_v3923'/f'{fighter}-p{side}-native-inflation-review.png'
        image=Image.open(review).convert('RGB')
        need(image.size==(800,1112) and len(frames)==7,'Seven essential native panels only')
        for i,frame in enumerate(frames):
            x,y=(i%2)*400,(i//2)*278
            need(hashlib.sha256(image.crop((x,y+24,x+400,y+278)).tobytes()).hexdigest().upper()==digests[frame],'Every QA panel equals complete actual native RGB')
        pin(review);reviews.append(dict(fighter=fighter,side=side,path=str(review),sha256=sha(review),nativePanels=7,everyPanelEqualsActualRGB=True))
        for file in folder.rglob('*'):
            if file.is_file():pin(file)
    for leaf in ('audit_v3911_sonya_zoning_later_start_p2_campaign','audit_v3927_kitana_inflation_earned_state_checked'):
        for file in (ROOT/leaf).rglob('*'):
            if file.is_file():pin(file)
    need(not json.loads((ROOT/'audit_v3927_kitana_inflation_earned_state_checked/report.json').read_text())['passed'],'Initial failed repeated-key parser gate remains failed')
    for name in ('mk2ks_stock_earned_ram_v3918.lua','mk2ks_inflation_native_scene_ram_v3919.lua','tools/run_kitana_inflation_native_scene_v3920.py','tools/verify_kitana_inflation_native_fifo_v3924.py','tools/verify_kitana_inflation_earned_state_v3926.py','tools/verify_sonya_later_start_campaign_v3928.py','tools/run_sonya_leg_later_start_v3930.py','tools/verify_kitana_inflation_earned_state_v3933.py','tools/compact_inflation_campaign_v3935.py','tools/save_inflation_campaign_checkpoint_v3937.py'):pin(ROOT/name)
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
    storage=reports['audit_v3936_inflation_campaign_compression'];pids=storage['captureChildrenMissing']
    check=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,pids))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(check.returncode==0 and not check.stdout.strip(),'Exact sealed capture handles missing; unrelated processes untouched')
    folder=ROOT/'audit_v3931_sonya_leg_later_start_p2_campaign'
    process=json.loads((folder/'process.json').read_text());before=json.loads((folder/'input_hashes_before.json').read_text())
    need(process['pid']==118604 and not (folder/'result.json').exists(),'Specific physical-input campaign still pending')
    live=subprocess.run(['powershell.exe','-NoProfile','-Command',f'Get-CimInstance Win32_Process -Filter "ProcessId={process["pid"]}" | Select-Object -ExpandProperty ExecutablePath'],capture_output=True,text=True)
    need(live.returncode==0 and live.stdout.strip().lower()==str(ROOT/'diagnostic_v3836_native_mileena_rom_identity/mkport_candidate.exe').lower(),'Exact recorded pending capture actually live')
    for p,h in before.items():pin(p,h)
    for name in ('process.json','input_hashes_before.json','source_snapshot_paths.json'):pin(folder/name)
    for p,dest in json.loads((folder/'source_snapshot_paths.json').read_text()).items():pin(dest,before[p])
    state['inputHashes']=pins
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=pins[str(PARENT)],mergeRule='Resolve parent recursively; preserve retired/deleted exclusions and agree on shared fresh pins; do not flatten.'),previousCheckpoint=str(PARENT),
        thisGoalTurnClassification='progress: unchanged3836 real earned Kitana inflation in all four own victim/physical-slot contexts. Full native CPU/DMA/shift/scanout replay2948fields/299516800RGBpixels, true palettes and six poses each. Independent FIFO/projection/grounding/native compressed-shadow rows/retirement52actual faults; original physical commands/collision/healthwriter/parameters/pointer consumers/completion40actual faults. Four essential native QA sheets viewed and all28panels exactly bound to original RGB. Initial repeated victim header/body key parser failure retained; fresh checker preserves both unchanged values. Sonya later Start900 zoning campaign terminal322771 nativefields,8roundwins/85paidcontinues/1016trueRingentries/6298native damage stores; nine actual campaign faults qualify bounded stability, not tower clear. Five sealed leaves LZX-compressed losslessly; no game or playable changes. LaterStart900 defensive-leg physical campaign remains confirmed live; all five groups/public1836 unchanged.',
        gameSourceAndPlayableBytesChangedThisTurn=False,
        currentDevelopmentNativeKitanaInflationPixelsFIFOProjectionCleanupAccepted=True,
        currentDevelopmentNativeKitanaInflationPixelsReport=str(ROOT/'audit_v3925_kitana_inflation_native_fifo_checked/report.json'),
        currentDevelopmentNativeKitanaInflationExactFields=2948,currentDevelopmentNativeKitanaInflationExactRGBPixels=299516800,currentDevelopmentNativeKitanaInflationFIFOShadowFaultsRejected=52,
        currentDevelopmentNativeKitanaInflationEarnedStateReport=str(ROOT/'audit_v3934_kitana_inflation_earned_state_checked/report.json'),currentDevelopmentNativeKitanaInflationEarnedStateFaultsRejected=40,
        currentDevelopmentNativeKitanaInflationHumanReview=dict(scope='Dead Pool only, both true own victims17/18 and slots1/2; six native inflated/burst phases plus held native winner page/blood/bones. Actual native floor-shadow rows/source/quarter-height DMA qualified; not every move/arena or full audio.',allFourSheetsViewed=True,panels=reviews),
        currentDevelopmentLaterStartZoningP2CampaignReport=str(ROOT/'audit_v3929_sonya_later_start_campaign_checked/report.json'),
        currentDevelopmentLaterStartZoningP2Campaign=dict(terminalFrame=322771,stagesReached=[0],nativeRoundWins=8,paidContinues=85,trueRingEntries=1016,nativeCollisionDamageStores=6298,actualRowFaultsRejected=9,towerClear=False),
        preservedInflationCheckerFailure='3926 generic parser overwrote repeated native victim header/body keys. Fresh3933 parses original header separately and retains native victim pointer; no actual input data edits or validation exemption.',
        currentTurnReclaimedAllocatedBytes=storage['reclaimedAllocatedBytes'],currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnActualCaptureRasterFiles=0,currentTurnActualCaptureAudioFiles=0,currentTurnEssentialNativeQAReviewPNGs=4,
        confirmedMissingThisTurnCapturePIDs=pids,
        pendingSonyaCampaign=dict(folder=str(folder),runner=str(ROOT/'tools/run_sonya_leg_later_start_v3930.py'),pid=118604,execSessionID=95590,bootFrame=900,strategy='defensive_leg',candidate='diagnostic_v3836_native_mileena_rom_identity',actualCIMLiveConfirmed=True,assistance='none',mutableLogsNotCheckpointPinned=True,action='Poll exact session95590, no restart on observation timeout. At terminal qualify full3491campaign algorithm with only declared3930 provenance/start900/defensive_leg policy. Never infer tower clear from input attempts.'),
        currentDevelopmentSonyaP2FullTowerClearAccepted=False,currentDevelopmentCampaignRegressionAccepted=False,currentDevelopmentWholePortRegressionAccepted=False,
        nextImplementationAction='Finish and qualify exact pending physical campaign. Continue complete finisher audio and other native finishers/victims/secrets/cinematics, all-move/all-arena art/grounding/floor shadows/cleanup, natural own tower ending and attract, combined UI/name/audio regression. Dependency-aware cleanup/refreshed ZIP only when qualified.',
        fullPortAcceptance=False,finishedRelease=False,goalStatus='active')
    need(state['remaining']==remaining and state['currentCandidate']=='diagnostic_v1836_ball_register_boundary','Original scope and public launch retained')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before write')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),freshPins=len(pins),exactFields=2948,pendingCampaignPID=118604,reclaimedBytes=storage['reclaimedAllocatedBytes'],goalStatus='active',fullPortAcceptance=False)))

if __name__=='__main__':main()
