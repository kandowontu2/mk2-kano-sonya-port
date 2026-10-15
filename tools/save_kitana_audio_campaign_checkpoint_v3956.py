"""Recursive full-scope checkpoint: actual Kitana native audio, physical campaign."""
import json,subprocess
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v3938_inflation_campaign_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3957_kitana_audio_campaign_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable full-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins={}
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance'] and not state['finishedRelease'],'Full natural-character objective unchanged')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);digest=sha(path)
        need(wanted is None or digest==wanted,'Actual executed evidence unchanged '+key)
        need(key not in pins or pins[key]==digest,'Consistent fresh evidence')
        need(key not in state['inputHashes'] or state['inputHashes'][key]==digest,'Inherited evidence not relabelled')
        pins[key]=digest
    reports={}
    for leaf in ('audit_v3932_sonya_leg_later_start_campaign_observed','audit_v3942_kitana_native_audio_queue_observed','audit_v3944_sonya_leg_later_start_campaign_checked','audit_v3953_kitana_native_audio_queue_checked','audit_v3955_kitana_audio_campaign_compression'):
        file=ROOT/leaf/'report.json';value=json.loads(file.read_text());need(value['passed'],'Actual completed report '+leaf);pin(file);reports[leaf]=value
        for p,h in value.get('inputHashes',{}).items():pin(p,h)
        for case in value.get('cases',[]):
            for p,h in case.get('inputHashes',{}).items():pin(p,h)
    audio=reports['audit_v3953_kitana_native_audio_queue_checked']
    need(audio['actualContexts']==4 and audio['actualRowCounterexamplesRejected']==76 and audio['actualNativeDCSBytesDelivered']==424 and audio['actualNativePainVoiceGenderAndPacketAccepted'] and audio['fullNativePCMExactlyUnaffectedBySamples'] and not audio['stockReferenceWholeWaveformFidelityAccepted'],'Four actual native full-window PCM/gender/queue/table/port/ADSP contexts, not universal waveform fidelity')
    need(all(len(c['actualRowCounterexamplesRejected'])==19 and c['nativeAudio']['allDispatchPacketsAndOwnersBound'] for c in audio['cases']),'All76 actual faults and every native packet/owner qualified')
    campaign=reports['audit_v3944_sonya_leg_later_start_campaign_checked']['cases'][0]
    need(campaign['bounded_campaign_evidence_proven'] and not campaign['unassisted_clear_proven'] and campaign['stages_reached']==[0,1] and campaign['native_own_round_wins']==3 and campaign['paid_continue_losses']==126 and campaign['native_special_moves']=={'leg':829} and len(campaign['actualRowCounterexamplesRejected'])==9,'Actual simple-controller loss result remains bounded, never called tower clear')
    for file in (ROOT/'audit_v3931_sonya_leg_later_start_p2_campaign').rglob('*'):
        if file.is_file():pin(file)
    for name in ('mk2ks_kitana_audio_queue_ram_v3939.lua','tools/run_kitana_native_audio_queue_v3940.py','tools/verify_sonya_leg_later_start_campaign_v3943.py','mk2ks_guarded_campaign_close_leg_ram_v3945.lua','mk2ks_close_leg_campaign_ram_v3946.lua','tools/run_sonya_close_leg_campaign_v3947.py','tools/verify_sonya_close_leg_campaign_v3950.py','tools/verify_kitana_native_audio_queue_v3952.py','tools/compact_kitana_audio_campaign_v3954.py','tools/save_kitana_audio_campaign_checkpoint_v3956.py'):pin(ROOT/name)
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
    storage=reports['audit_v3955_kitana_audio_campaign_compression'];pids=storage['captureChildrenMissing']
    check=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,pids))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(check.returncode==0 and not check.stdout.strip(),'All exact nine sealed emulator handles missing, unrelated processes untouched')
    folder=ROOT/'audit_v3948_sonya_close_leg_p2_campaign'
    process=json.loads((folder/'process.json').read_text());before=json.loads((folder/'input_hashes_before.json').read_text())
    need(process['pid']==32644 and not (folder/'result.json').exists(),'Specific closer physical-input campaign pending')
    live=subprocess.run(['powershell.exe','-NoProfile','-Command',f'Get-CimInstance Win32_Process -Filter "ProcessId={process["pid"]}" | Select-Object -ExpandProperty ExecutablePath'],capture_output=True,text=True)
    need(live.returncode==0 and live.stdout.strip().lower()==str(ROOT/'diagnostic_v3836_native_mileena_rom_identity/mkport_candidate.exe').lower(),'Exact pending capture live now')
    for p,h in before.items():pin(p,h)
    for name in ('process.json','input_hashes_before.json','source_snapshot_paths.json'):pin(folder/name)
    for p,dest in json.loads((folder/'source_snapshot_paths.json').read_text()).items():pin(dest,before[p])
    build=json.loads((ROOT/'diagnostic_v3836_native_mileena_rom_identity/build-info.json').read_text(encoding='utf-8-sig'))
    # The inherited campaign controller still writes one native initialized
    # guest-memory dump. Do not mislabel it as a RAM-only guest capture or a
    # new playable ROM. It is immutable frame-one diagnostic evidence.
    guest_dump=folder/'guest_maincpu.bin'
    need(guest_dump.stat().st_size==1048576 and sha(guest_dump)==build['expected_guest_sha256'],'Actual frame-one whole native guest dump, not mutable live log')
    pin(guest_dump)
    state['inputHashes']=pins
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=pins[str(PARENT)],mergeRule='Resolve parent recursively; preserve retired/deleted exclusions and agree on shared fresh pins; do not flatten.'),previousCheckpoint=str(PARENT),
        previousGoalTurnClassification='progress:3938 exact native inflation FIFO/ground/shadow/cleanup and earned-state proof in four actual contexts;63MiB lossless log compression.',
        thisGoalTurnClassification='progress: reused exact recorded3931 live campaign handle to terminal0,322771fields/3native own roundwins/126paidcontinues/829trueLegentries/3524native collisiondamage stores/stages0..1; nine actual faults qualify stability, not naturalclear. Eight actual current native Kitana audio captures retain original physical921controls and true17/18. Full749-field native mixed PCM each is exactly samples-on/off identical; four true gender/player pain routes, original four fixed effect calls plus actual pain command, independently decoded original priority/duration/base packet and actual slot increment delivered through original high/low port/ADSP, all424bytes. Every actual native dispatch packet/owner checked;76actual faults reject with positive restoration. No game/build/EXE/payload edits. Sealed nine capture logs LZX-compressed,6.9MiB reclaimed. Fresh human controller trial walks to gap63 instead85 before original leg command, with native-game/AI/health/schedule/boss controls unchanged; exact actual handle32644 live. Resource audit identified inherited campaigns write one1MiB guest-memory dump per campaign; preserve dependencies honestly and convert future fresh campaigns to qualified RAM guest transport, never relabel current evidence.',
        gameSourceAndPlayableBytesChangedThisTurn=False,
        currentDevelopmentNativeKitanaInflationAudioPacketDeliveryAccepted=True,currentDevelopmentNativeKitanaInflationAudioReport=str(ROOT/'audit_v3953_kitana_native_audio_queue_checked/report.json'),
        currentDevelopmentNativeKitanaInflationAudio=dict(actualContexts=4,pairedCaptures=8,actualDeliveredDCSBytes=424,actualRecordFaultsRejected=76,fullNativePCMExactlyUnaffectedBySamples=True,truePainGenderAndPlayerBranchAccepted=True,originalFixedEffects=[96,163,165,164],originalStockWholeWaveformFidelityAccepted=False,allFinisherAudioAccepted=False),
        currentDevelopmentLaterStartLegP2CampaignReport=str(ROOT/'audit_v3944_sonya_leg_later_start_campaign_checked/report.json'),currentDevelopmentLaterStartLegP2Campaign=dict(terminalFrame=322771,stagesReached=[0,1],nativeRoundWins=3,paidContinues=126,trueNativeLegEntries=829,nativeCollisionDamageStores=3524,actualRowFaultsRejected=9,towerClear=False),
        currentTurnReclaimedAllocatedBytes=storage['reclaimedAllocatedBytes'],currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnActualCaptureRasterFiles=0,currentTurnActualCaptureAudioFiles=0,currentTurnEssentialNativeQAReviewPNGs=0,currentTurnNativeGuestMemoryDumpFiles=1,currentTurnNativeGuestMemoryDumpLogicalBytes=1048576,
        confirmedMissingThisTurnCapturePIDs=pids,
        pendingSonyaCampaign=dict(folder=str(folder),runner=str(ROOT/'tools/run_sonya_close_leg_campaign_v3947.py'),qualifier=str(ROOT/'tools/verify_sonya_close_leg_campaign_v3950.py'),pid=32644,execSessionID=89729,bootFrame=900,strategy='defensive_leg',ordinaryLegAttemptGap=63,candidate='diagnostic_v3836_native_mileena_rom_identity',actualCIMLiveConfirmed=True,assistance='none',mutableLogsNotCheckpointPinned=True,action='Poll exact session89729, no restart on observation timeout. At terminal qualify full3491campaign algorithm, only declared3945closer human attempt and RAM raster sinks/host deadline/provenance. Do not fake health/AI/schedule or tower clear.'),
        currentDevelopmentSonyaP2FullTowerClearAccepted=False,currentDevelopmentCampaignRegressionAccepted=False,currentDevelopmentWholePortRegressionAccepted=False,
        nextImplementationAction='Re-poll exact live closer-leg campaign and independently qualify genuine outcome. Fresh future campaign wrappers should transport actual guest bytes to RAM and retain source-bound whole-byte equality/digests instead of ordinary1MiB dumps. Continue other original finishers (next current Kung Lao vertical split, original1021 F,F,F,LK gap112/native FF8C6040), complete stage/victim audio, all move/arena grounding/shadows/cleanup, natural tower own ending/attract and combined UI/name/audio regression. Dependency-aware cleanup/refreshed release only after full objective proof.',
        fullPortAcceptance=False,finishedRelease=False,goalStatus='active')
    need(state['remaining']==remaining and state['currentCandidate']=='diagnostic_v1836_ball_register_boundary','Original five groups/public launch preserved')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before write')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),freshPins=len(pins),nativeAudioContexts=4,nativeAudioFaults=76,pendingCampaignPID=32644,reclaimedBytes=storage['reclaimedAllocatedBytes'],goalStatus='active',fullPortAcceptance=False)))

if __name__=='__main__':main()
