"""Recursive full-objective checkpoint: native queue audio and bounded campaign.

No claim of full finisher waveform fidelity, full tower clear or release.
Preserve all five groups and the public1836 launch while3911 remains live.
"""
import json,subprocess
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v3888_mileena_scene_campaign_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3917_mileena_audio_campaign_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable full-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins={}
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],'Full natural-character objective stays intact')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);digest=sha(path)
        need(wanted is None or wanted==digest,'Actual executed evidence unchanged '+key)
        need(key not in pins or pins[key]==digest,'Consistent current evidence')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'No inherited evidence relabelled')
        pins[key]=digest
    reports={}
    for leaf in('audit_v3891_sonya_defensive_leg_campaign_observed','audit_v3895_mileena_native_audio_matrix_observed','audit_v3903_sonya_defensive_leg_campaign_checked','audit_v3907_mileena_native_audio_queue_observed','audit_v3909_mileena_native_audio_queue_checked','audit_v3915_mileena_audio_campaign_compression'):
        file=ROOT/leaf/'report.json';value=json.loads(file.read_text());need(value['passed'],'Actual completed evidence '+leaf);pin(file);reports[leaf]=value
        for p,h in value.get('inputHashes',{}).items():pin(p,h)
        for case in value.get('cases',[]):
            for p,h in case.get('inputHashes',{}).items():pin(p,h)
    audio=reports['audit_v3909_mileena_native_audio_queue_checked']
    need(audio['actualContexts']==4 and audio['actualRowCounterexamplesRejected']==64 and audio['actualNativeDCSBytesDelivered']==368 and audio['nativeFixedEffectCommandsSourceBound']and audio['fullNativePCMExactlyUnaffectedBySamples']and not audio['stockReferenceWholeWaveformFidelityAccepted'],'Full four-context actual table/priority branch/packet/ADSP/PCM proof remains specifically bounded')
    campaign=reports['audit_v3903_sonya_defensive_leg_campaign_checked']['cases'][0]
    need(campaign['bounded_campaign_evidence_proven']and not campaign['unassisted_clear_proven']and campaign['stages_reached']==[0,1]and campaign['native_special_moves']=={'leg':1100}and len(campaign['actualRowCounterexamplesRejected'])==9,'Actual defensive-leg evidence is not a fabricated tower clear')
    for leaf in('audit_v3890_sonya_defensive_leg_p2_campaign','audit_v3899_mileena_native_audio_delivery_checked','audit_v3901_mileena_native_audio_delivery_checked'):
        for p in(ROOT/leaf).rglob('*'):
            if p.is_file():pin(p)
    for name in('mk2ks_mileena_audio_ram_v3892.lua','mk2ks_mileena_stock_reference_v3896.lua','mk2ks_mileena_stock_audio_ram_v3897.lua','mk2ks_mileena_audio_queue_ram_v3904.lua',
                 'tools/run_sonya_defensive_leg_campaign_v3889.py','tools/run_mileena_native_audio_matrix_v3893.py','tools/verify_mileena_native_audio_delivery_v3898.py','tools/verify_mileena_native_audio_delivery_v3900.py','tools/verify_sonya_defensive_leg_campaign_v3902.py','tools/run_mileena_native_audio_queue_v3905.py','tools/verify_mileena_native_audio_queue_v3908.py','tools/run_sonya_zoning_later_start_v3910.py','tools/compact_mileena_audio_campaign_v3914.py','tools/save_mileena_audio_campaign_checkpoint_v3916.py'):pin(ROOT/name)
    for leaf in('audit_v3899_mileena_native_audio_delivery_checked','audit_v3901_mileena_native_audio_delivery_checked'):
        need(not json.loads((ROOT/leaf/'report.json').read_text())['passed'],'Failed native checker attempts remain failed and retained')
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
    storage=reports['audit_v3915_mileena_audio_campaign_compression'];pids=storage['captureChildrenMissing']
    check=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,pids))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(check.returncode==0 and not check.stdout.strip(),'All exact21 sealed capture handles missing now; no unrelated compiler interference')
    folder=ROOT/'audit_v3911_sonya_zoning_later_start_p2_campaign'
    process=json.loads((folder/'process.json').read_text());before=json.loads((folder/'input_hashes_before.json').read_text())
    need(process['pid']==123820 and not(folder/'result.json').exists(),'Specific new input-only campaign not yet terminal')
    live=subprocess.run(['powershell.exe','-NoProfile','-Command',f'Get-CimInstance Win32_Process -Filter "ProcessId={process["pid"]}" | Select-Object -ExpandProperty ExecutablePath'],capture_output=True,text=True)
    need(live.returncode==0 and live.stdout.strip().lower()==str(ROOT/'diagnostic_v3836_native_mileena_rom_identity/mkport_candidate.exe').lower(),'Specific recorded campaign handle confirmed live now, not inferred from logs/intent')
    for p,h in before.items():pin(p,h)
    for name in('process.json','input_hashes_before.json','source_snapshot_paths.json'):pin(folder/name)
    frozen=json.loads((folder/'source_snapshot_paths.json').read_text())
    for p,dest in frozen.items():pin(dest,before[p])
    state['inputHashes']=pins
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=pins[str(PARENT)],mergeRule='Resolve parent recursively; preserve retired/deleted exclusions and agree on shared fresh pins; do not flatten.'),previousCheckpoint=str(PARENT),
        previousGoalTurnClassification='progress: native scene/campaign proof3888 followed by actual full RAM audio captures3895. The intervening acknowledgment alone made no additional progress.',
        thisGoalTurnClassification='progress: revalidated exact old campaign handle122604 missing/terminal0 at322771fields. Full original campaign algorithm independently passes9actual faults for defensive-leg policy,7native roundwins/1100true leg entries/4021native damage stores/123paid continues, stages0..1 only; not a tower clear. Original audio checker failures retained: inactive sample length/pos are preserved by actual engine stop/completion, not active playback; first table halfword is priority/duration, not packet. Fresh8capture native observer reads original priority-slot/packed-dispatch branches; source-qualified table fields and actual slot increments reach DCS,368bytes in four own slot contexts. Every full streamed PCM update/whole waveform identical sampleson/off;64actual record faults reject. No stock reference renamed as Kano/Sonya, no full original waveform fidelity claim. Compressed21sealed capture logs losslessly,9.5MiB reclaimed. Original zoning controller with genuine later Start900 is confirmed live handle123820, same candidate/no game-state assistance. Public/installed EXE/dirty checkout untouched; all five remaining groups remain active.',
        gameSourceAndPlayableBytesChangedThisTurn=False,
        currentDevelopmentNativeMileenaAudioPacketDeliveryAccepted=True,
        currentDevelopmentNativeMileenaAudioPacketReport=str(ROOT/'audit_v3909_mileena_native_audio_queue_checked/report.json'),
        currentDevelopmentNativeMileenaAudioPacket=dict(actualContexts=4,actualPairedCaptures=8,actualDCSBytesDelivered=368,actualRecordFaultsRejected=64,fixedNativeCommands=[96,201,195],originalPriorityDurationAndBasePacketsBound=True,actualVoiceSlotBranchesObserved=True,fullPCMOnOffIdentical=True,originalStockWaveformFidelityAccepted=False),
        currentDevelopmentDefensiveLegP2CampaignReport=str(ROOT/'audit_v3903_sonya_defensive_leg_campaign_checked/report.json'),
        currentDevelopmentDefensiveLegP2Campaign=dict(terminalFrame=322771,stagesReached=[0,1],nativeRoundWins=7,paidContinues=123,trueNativeLegEntries=1100,nativeCollisionDamageStores=4021,actualRowFaultsRejected=9,towerClear=False),
        preservedAudioCheckerFailures={'3898':'Rejected actual idle metadata differences; actual engine source retains inactive length/pos after clearing playback. Fresh source-qualified3908 still rejects any active sample/loop and changes of retained metadata within window, with every actual PCM byte equal.','3900':'Rejected table-word interpretation; original first word is priority/duration and second word base packet. Fresh actual read-only branch capture3904 proves selected native slot0/1/2 increment before packet emission. No output-derived slot assumption.'},
        currentTurnReclaimedAllocatedBytes=storage['reclaimedAllocatedBytes'],currentTurnDeletedFiles=0,currentTurnNewBuilds=0,
        currentTurnActualCaptureRasterFiles=0,currentTurnActualCaptureAudioFiles=0,currentTurnEssentialNativeQAReviewPNGs=0,
        confirmedMissingThisTurnCapturePIDs=pids,
        pendingSonyaCampaign=dict(folder=str(folder),runner=str(ROOT/'tools/run_sonya_zoning_later_start_v3910.py'),pid=process['pid'],execSessionID=6666,bootFrame=900,strategy='zoning',candidate='diagnostic_v3836_native_mileena_rom_identity',actualCIMLiveConfirmed=True,assistance='none',mutableLogsNotCheckpointPinned=True,action='Re-poll exact exec session6666/PID123820; no restart on observation timeout. At terminal qualify whole3491 campaign algorithm with only declared provenance/start900/strategy differences. Do not compare zoning600 chronology or defensive-leg chronology to this run.'),
        currentDevelopmentSonyaP2FullTowerClearAccepted=False,currentDevelopmentCampaignRegressionAccepted=False,currentDevelopmentMileenaRasterArtShadowAudioAccepted=False,currentDevelopmentWholePortRegressionAccepted=False,
        nextImplementationAction='Finish specific live SonyaP2 campaign and qualify actual outcome, never fake health/AI/schedule or clear. Continue broader stage/victim audio, moves and all-arena floor-shadow/cleanup, other native finishers/secrets/cinematics, full combined current UI/audio regression. Only then dependency-aware obsolete-folder cleanup and refreshed release ZIP.',
        fullPortAcceptance=False,finishedRelease=False,goalStatus='active')
    need(state['remaining']==remaining and state['currentCandidate']=='diagnostic_v1836_ball_register_boundary','Original scope/public launch preserved')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before write')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n');print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),freshPins=len(pins),nativeAudioContexts=4,actualAudioFaults=64,pendingCampaignPID=123820,goalStatus='active',fullPortAcceptance=False)))

if __name__=='__main__':main()
