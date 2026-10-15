"""Measured pure-input successor pending; original full objective unchanged."""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_campaign_shao_guarded_highkick_v3461 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
PREVIOUS=ROOT/'audit_v3458_current_sonya_kintaro_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3466_current_guarded_highkick_pending_full_scope_checkpoint'
CASE=ROOT/'audit_v3462_current_sonya_natural_guarded_highkick_campaign'

def main():
    need(not OUT.exists(),'Immutable complete-objective checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining'];fresh={}
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance']
         and not state['finishedRelease'] and not state['actualEndingsAccepted'],'Full unfinished original objective')
    need(state['current3172KanoNaturalKintaroMatchClearAccepted']
         and state['current3172SonyaNaturalKintaroMatchClearAccepted'],'Keep both actual current native Kintaro matches')
    need(not (CASE/'result.json').exists(),'Actually pending campaign, never terminal acceptance')
    def pin(path,digest=None):
        key=str(Path(path).resolve());digest=digest or sha(key)
        need(key not in fresh or fresh[key]==digest,'Consistent fresh relevant pin')
        need(key not in state['inputHashes'] or state['inputHashes'][key]==digest,'Never relabel historical evidence')
        fresh[key]=digest
    sourcepath=ROOT/'audit_v3464_guarded_highkick_source_boundary/report.json'
    source=json.loads(sourcepath.read_text())
    need(source['passed'] and source['exactShaoOnlyGuardThresholdChangeAccepted']
         and (source['previousThreshold'],source['currentThreshold'])==(125,105)
         and source['ordinaryAndKintaroControlsAndObserversUnchanged']
         and source['actualRunnerInputsAndOptionsOtherwiseUnchanged'] and len(source['actualQualifiedSourceFaults'])==4
         and source['samePathSourcePositiveAccepted'] and source['campaignAcceptancePending']
         and not source['controllerImprovementAccepted'] and not source['fullPortAcceptance'],
         'Exact measured input delta and qualified faults, no campaign result yet')
    pin(sourcepath)
    for file,digest in source['inputHashes'].items():pin(file,digest)
    before=json.loads((CASE/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    snapshots=json.loads((CASE/'source_snapshot_paths.json').read_text(encoding='utf-8-sig'))
    for file,digest in before.items():
        pin(file,digest)
        if Path(file).suffix in ('.lua','.ps1','.json'):
            target=Path(snapshots[file]).resolve()
            need(target.is_relative_to((CASE/'input_sources/tree').resolve()),'Exact collision-free capture hierarchy')
            pin(target,digest)
    for name in ('input_hashes_before.json','source_snapshot_paths.json','guest_maincpu.bin'):pin(CASE/name)
    need(sha(CASE/'guest_maincpu.bin')=='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7','Current initialized whole guest')
    for relative in (state['currentCMD'],state['currentPlaytestZIP'],
        'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
        'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        key=str((ROOT/relative).resolve());pin(key,state['inputHashes'][key])
    pin(PREVIOUS);pin(__file__)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,digest),actual in zip(fresh.items(),pool.map(sha,fresh)):
            need(actual==digest,'Fresh actual source/capture/public bytes unchanged')
    state['inputHashes']=fresh
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),
        parentCheckpointSHA256=fresh[str(PREVIOUS)],mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
        previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress and verified wait: inspect current3458 full-five-scope checkpoint/3446 source pins/unchanged dirty source tree. Based on measured330crouch-transition incoming stores and successful contactsmostly98..104, create3459/3460 pure stage16 guard-release threshold125to105. Whole ordinary/Kintaro/selection/health/win/ending source exact after branch inverse; exact whole runner inverse. Four qualified actual source faults rejected3464 with same-path positive. Full current whole guest/verifier construction smoke passed. Start one current3172 Sonya defensive_leg cold campaign3462; live84580 polled, not restarted or accepted. No game/power/difficulty/source/public changes or build/WAV copies. All five original groups preserved.',
        currentGuardedHighkickSourceReport=str(sourcepath),
        pendingCurrentNaturalGuardedHighkickCampaign=dict(capture=str(CASE),execSessionId=84580,
            terminal=False,acceptance=False,candidate='diagnostic_v3172_native_morph_shadow',player='sonya',
            humanSlot=1,strategy='defensive_leg',bootFrame=600,seconds=3900,
            verifier=str(Path(native.__file__).resolve()),previousThreshold=125,currentThreshold=105),
        pendingCampaignLogNotPinnedWhileMutable=True,
        currentGuardedHighkickControllerImprovementAccepted=False,
        gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
        publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,newExecutableROMOrRawAudioCopiesThisTurn=0,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),historicalPinMapCopiedAgain=False,
        nextAction='Poll exact live84580 for3462. Never restart because observation expires. When terminal, execute3461 full campaign verifier to fresh output, compare original normalized pre-Shao trajectory to accepted3426/3446 (only policy labels may differ), then analyze actual stage16 ordered damage/state/guard/HP/wins/ending outcomes against3456. No success from source tests/intended kicks or native stage16 alone. Both current Kintaro matches preserved; Shao/own-ending/attract still unproven. Keep all five original arena/victim/effect/audio, move-phase/ground/shadow/cleanup CPU/repeat/KO/overlap, finisher/morph/secret/cinematic, natural boss/ending/attract, final UI/audio/dependency-cleanup/refreshed-release requirements. Reuse current builds and compressed evidence; no raw audio/build/retired recovery or historical hash flattening.')
    need(state['remaining']==remaining,'Original complete requirement groups intact')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless full-scope checkpoint compression')
    print(json.dumps(dict(saved=str(path),goalStatus='active',remainingGroups=5,pendingCampaign=84580,
        freshPins=len(fresh),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
