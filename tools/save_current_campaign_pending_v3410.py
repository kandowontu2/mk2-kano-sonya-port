"""Keep full goal and exact live handle; pending campaign is never acceptance."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_campaign_shao_lowkick_v3409 as native

ROOT=native.ROOT;need=native.need;sha=native.sha
PREVIOUS=ROOT/'audit_v3404_current_cpu_bicycle_audio_full_scope_checkpoint/checkpoint.json'
FOLDER=ROOT/'audit_v3408_current_kano_natural_lowkick_campaign'
OUT=ROOT/'audit_v3411_current_campaign_pending_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Never overwrite checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining']
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and
         not state['finishedRelease']and not state['actualEndingsAccepted'],'Keep full natural-port requirements')
    native.source_boundary()
    before=json.loads((FOLDER/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    snapshots=json.loads((FOLDER/'source_snapshot_paths.json').read_text(encoding='utf-8-sig'))
    fresh=dict(before)
    for file,digest in before.items():
        if Path(file).suffix in('.lua','.ps1','.json'):
            path=Path(snapshots[file]).resolve()
            need(path.is_relative_to(FOLDER),'Exact snapshot within this evidence leaf')
            fresh[str(path)]=digest
    for path in (PREVIOUS,Path(__file__).resolve(),ROOT/'tools/verify_current_campaign_shao_lowkick_v3409.py',
                 ROOT/'tools/verify_current_boss_shao_cooldown_retreat_v2630.py',
                 ROOT/'audit_v2632_cooldown_retreat_source_boundary_checked/report.json',
                 FOLDER/'input_hashes_before.json',FOLDER/'source_snapshot_paths.json',FOLDER/'guest_maincpu.bin'):
        fresh[str(path.resolve())]=sha(path)
    need(sha(FOLDER/'guest_maincpu.bin')=='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7',
         'Exact actual initialized current guest capture; not full campaign acceptance')
    for relative in (state['currentCMD'],state['currentPlaytestZIP'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        key=str((ROOT/relative).resolve());need(key in state['inputHashes'],'Retained public guard')
        fresh[key]=state['inputHashes'][key]
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,digest),actual in zip(fresh.items(),pool.map(sha,fresh)):
            need(actual==digest,'Immutable relevant source/build/snapshot/public input unchanged')
            need(file not in state['inputHashes']or state['inputHashes'][file]==digest,'No relabeled prior pins')
    state['inputHashes']=fresh
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),
        parentCheckpointSHA256=fresh[str(PREVIOUS)],mergeRule='Resolve parent recursively, preserving its parent graph and retired/deleted exclusions. Fresh inputHashes must agree with inherited keys.'),
        historicalPinMapCopiedAgain=False,previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress and verified wait: launch one current3172 cold ordinary-controls-only Kano campaign with a new Shao crouching-lowkick physical strategy. Full source inverse proves ordinary selection/combat/Kintaro/native health/win/ending observers unchanged. Exact hierarchy input snapshots and current guest captured; no WAV/build copies. Actual runtime progressed through Kintaro into Shao; no success claimed from interim observations. Live exec41305 polled; keep exact handle, never restart because observations expire.',
        pendingCurrentNaturalLowkickCampaign=dict(capture=str(FOLDER),execSessionId=41305,
            candidate='diagnostic_v3172_native_morph_shadow',fighter='kano',humanSlot=1,cpuSlot=2,
            strategy='zoning',bossPolicy='shao_crouch_lowkick',secondsLimit=3900,
            status='Observed running; re-poll exact exec handle before treating as live or terminal.',
            terminalVerificationAccepted=False,fullCampaignOrEndingAcceptance=False,
            verifier=str(ROOT/'tools/verify_current_campaign_shao_lowkick_v3409.py'),
            proposedTerminalReport=str(ROOT/'audit_v3412_current_kano_natural_lowkick_campaign_checked')),
        pendingCampaignLogNotPinnedWhileMutable=True,
        current3172NaturalShaoClearAccepted=False,actualEndingsAccepted=False,
        gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,
        publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
        goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
        nextAction='Poll live exec session41305, never restart its audit_v3408 capture. Observation timeout is not terminal. When authoritative process is terminal, run3409 whole native campaign verifier into fresh3412, inspect actual native losses/wins/lowkick activations/health and own ending/return. Lowkick strategy is not assumed better; interim Shao damage/activation is poor. Retain all five full-port groups and previous bounded proofs; no raw audio/build/archive copies, inherited hash graph remains referenced by parent SHA.')
    need(state['remaining']==remaining,'Full scope unchanged')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless checkpoint compression')
    print(json.dumps(dict(saved=str(path),pendingExecSession=41305,terminalVerificationAccepted=False,
        immutablePinsRehashed=len(fresh),originalRemainingGroups=5,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
