"""Full-scope checkpoint: native split audio and actual RAM-only campaign live.

No final-release promotion. Native split proof is Dead Pool only; it does
not prove every finisher, original stock whole-waveform fidelity or endings.
"""
import hashlib,json,subprocess
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current
import verify_sonya_zoning700_campaign_v4015 as campaign
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v3991_split_campaign_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4018_split_audio_ram_campaign_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins={}
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],'Whole original natural-character objective retained')
    def pin(p,wanted=None):
        p=Path(p).resolve();digest=sha(p);key=str(p)
        need(wanted is None or digest==wanted,'Exact actual source/evidence unchanged '+key)
        need(key not in pins or pins[key]==digest,'Consistent evidence pin')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Inherited accepted evidence unchanged')
        pins[key]=digest
    pin(PARENT)
    reports={}
    for leaf in('audit_v4003_kung_lao_native_audio_queue_observed','audit_v4005_kung_lao_native_audio_queue_checked','audit_v4012_kung_lao_audio_compression'):
        p=ROOT/leaf/'report.json';r=json.loads(p.read_text());need(r['passed']and not r['fullPortAcceptance'],'Actual completed bounded native proof '+leaf);reports[leaf]=r;pin(p)
        for f,h in r.get('inputHashes',{}).items():pin(f,h)
    audio=reports['audit_v4005_kung_lao_native_audio_queue_checked'];storage=reports['audit_v4012_kung_lao_audio_compression']
    need(audio['actualContexts']==4 and audio['actualRowCounterexamplesRejected']==80 and audio['actualNativeGeneralCommands']==216 and audio['actualNativeDCSBytesDelivered']==520 and audio['fullNativePCMExactlyUnaffectedBySamples']and audio['actualNativeSplitVoiceGenderAndPacketAccepted']and not audio['stockReferenceWholeWaveformFidelityAccepted']and not audio['allVictimFinisherAudioAccepted'],'All four real added-character victims/slots, full paired PCM and actual native command/packet/ADSP proof; limitations remain explicit')
    for fighter in('kano','sonya'):
        for side in(1,2):
            for mode in('samples','nosamples'):
                folder=ROOT/f'audit_v4002_kung_lao_{fighter}_p{side}_audio_queue_{mode}'
                meta=json.loads((folder/'result.json').read_text());need(meta['exit_code']==0 and meta['fighter']==fighter and meta['side']==side and not meta['stockReferenceOnly']and meta['rawAudioRasterVRAMROMCopiesWritten']==0,'Actual terminal true-ID context, no new native media/guest files')
                for p in folder.rglob('*'):
                    if p.is_file():pin(p)
    for name in('mk2ks_split_audio_queue_ram_v4000.lua','tools/run_kung_lao_native_audio_queue_v4001.py','tools/verify_kung_lao_native_audio_queue_v4004.py','tools/compact_kung_lao_audio_v4011.py','mk2ks_guarded_campaign_guest_ram_v4006.lua','mk2ks_zoning700_campaign_ram_v4007.lua','tools/run_sonya_zoning700_campaign_v4008.py','tools/verify_sonya_zoning700_campaign_v4013.py','tools/verify_sonya_zoning700_campaign_v4015.py','tools/save_split_audio_ram_campaign_checkpoint_v4017.py'):pin(ROOT/name)
    campaign.transport_boundary()
    folder=ROOT/'audit_v4009_sonya_zoning700_p2_campaign'
    before=json.loads((folder/'input_hashes_before.json').read_text());frozen=json.loads((folder/'source_snapshot_paths.json').read_text());process=json.loads((folder/'process.json').read_text());proof=json.loads((folder/'guest_memory_proof.json').read_text())
    need(proof['schema']==1 and proof['frame']==1 and proof['bytes']==1048576 and proof['everyActualByteComparedInRAM']and proof['sha256']=='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'and proof['guestDumpFilesWritten']==0 and proof['captureSourceSHA256']==sha(ROOT/'tools/run_sonya_zoning700_campaign_v4008.py')and proof['transportSourceSHA256']==sha(ROOT/'mk2ks_guarded_campaign_guest_ram_v4006.lua'),'Actual full-byte RAM guest comparator reached before gameplay; source bound, not a fabricated guest file')
    need(not list(folder.rglob('guest*.bin'))and not list(folder.rglob('*.png'))and not list(folder.rglob('*.wav')),'Campaign ordinary native raster/audio/guest files absent')
    for f,h in before.items():pin(f,h)
    for f,dest in frozen.items():pin(dest,before[f])
    for name in('input_hashes_before.json','source_snapshot_paths.json','process.json','guest_memory_proof.json'):pin(folder/name)
    pid=process['pid']
    q=subprocess.run(['powershell.exe','-NoProfile','-Command',f'Get-CimInstance Win32_Process -Filter "ProcessId = {pid}" | Select-Object ProcessId,ExecutablePath,CreationDate | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0 and q.stdout.strip(),'Exact current native campaign handle confirmed live now, no restart')
    live=json.loads(q.stdout);need(live['ProcessId']==pid and Path(live['ExecutablePath']).resolve()==Path(process['command'][0]).resolve(),'Actual live3836 emulator executable and PID')
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,storage['captureChildrenMissing']))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'All eight exact sealed audio children missing now')
    for relative,digest in {
      'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
      'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
      'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
      'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
      'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
      'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
      'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}.items():pin(ROOT/relative,digest)
    pin(ROOT/state['currentCMD'])
    state.update(inputHashes=pins,inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='Resolve parent recursively; preserve retired/deleted exclusions and agree on shared fresh pins; do not flatten.'),previousCheckpoint=str(PARENT),
      previousGoalTurnClassification='no progress: acknowledgement-only user turn; revalidated exact3991 full scope and fresh4003/4005 terminal evidence before taking new safe work.',
      thisGoalTurnClassification='progress: four native Kung Lao split victim/slot audio contexts, eight actual captures, full paired PCM unchanged by samples,216 original table-bound general commands,520 actual delivered DCS bytes and80 actual faults rejected. Original male85/femaleB7 voice grammar and blood-task ownership source bound. Eight terminal leaves losslessly compressed,2834432 allocated bytes reclaimed. Fresh genuine SonyaP2 original zoning Start700 campaign is confirmed live; original game state/schedule/AI/health unchanged. One first-frame1MiB guest read and six original RGB sinks now transport only to RAM, with every actual initialized guest byte independently compared before discard. Full native campaign factory/boss replay constructed with only a qualified guest-sink substitution; terminal qualification pending.',
      currentDevelopmentNativeKungLaoSplitAudioReport=str(ROOT/'audit_v4005_kung_lao_native_audio_queue_checked/report.json'),
      currentDevelopmentNativeKungLaoSplitAudio=dict(ownVictimContexts=4,actualCaptures=8,actualRowFaultsRejected=80,sourceBoundOriginalGeneralCommands=216,actualDCSBytesDelivered=520,completeNativePCMUnaffectedBySamples=True,originalMaleFemaleVictimVoiceAccepted=True,originalStockWholeWaveformFidelityAccepted=False,allFinisherAudioAccepted=False),
      pendingSonyaCampaign=dict(candidate=campaign.NAME,capture=str(folder),pid=pid,execSession=57976,physicalStartFrame=700,strategy='original zoning',humanSlot=2,cpuSlot=1,hostLimitSeconds=5900,gameWrites=0,initializedGuestBytesComparedInRAM=1048576,initializedGuestSHA256=proof['sha256'],nativeGuestDumpFilesWritten=0,liveProcess=live,qualificationSource=str(ROOT/'tools/verify_sonya_zoning700_campaign_v4015.py'),qualificationPending=True,towerClearClaimed=False),
      gameSourceAndPlayableBytesChangedThisTurn=False,currentTurnReclaimedAllocatedBytes=storage['reclaimedAllocatedBytes'],currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnActualCaptureRasterFiles=0,currentTurnActualCaptureAudioFiles=0,currentTurnEssentialNativeQAReviewPNGs=0,currentTurnNativeGuestMemoryDumpFiles=0,
      confirmedMissingThisTurnCapturePIDs=storage['captureChildrenMissing'],
      nextImplementationAction='Poll the same live57976/PID115264 SonyaP2 zoning Start700 campaign to its actual terminal, then run whole retained native campaign qualifier4015 including RAM transport and actual boss input faults. Do not restart on observation timeout, assume a clear, or promote development3836. Continue full original other finisher/victim/morph/secret/cinematic and multi-arena full-move grounding/floor-shadow/cleanup coverage, stock victim/stage sound fidelity and genuine own ending pixel/audio proof. Final combined UI/ladder/names/audio regression, dependency-aware old-folder cleanup and refreshed release ZIP still required.',
      fullPortAcceptance=False,finishedRelease=False,goalStatus='active')
    need(state['remaining']==remaining and state['currentCandidate']=='diagnostic_v1836_ball_register_boundary','No scope shrink or release substitution')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before write')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),freshPins=len(pins),nativeAudioContexts=4,nativeAudioFaultsRejected=80,reclaimedAllocatedBytes=storage['reclaimedAllocatedBytes'],liveNativeCampaignPID=pid,goalStatus='active',fullPortAcceptance=False)),flush=True)

if __name__=='__main__':main()
