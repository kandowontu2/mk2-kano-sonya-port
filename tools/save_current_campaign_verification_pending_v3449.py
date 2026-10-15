"""Completed selection fault evidence and terminal Sonya capture awaiting live verifier."""
import json,subprocess
from pathlib import Path
import verify_current_campaign_shao_highkick_v3440 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
PREVIOUS=ROOT/'audit_v3443_current_ring_campaign_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3450_current_sonya_verification_pending_full_scope_checkpoint'
CASE=ROOT/'audit_v3426_current_sonya_natural_defensive_leg_highkick_campaign'

def main():
    need(not OUT.exists(),'Immutable full objective checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining']
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance']
         and not state['finishedRelease'] and not state['actualEndingsAccepted'],'All original unfinished requirements')
    meta=json.loads((CASE/'result.json').read_text(encoding='utf-8-sig'))
    need(meta['exit_code']==0 and meta['candidate']=='diagnostic_v3172_native_morph_shadow'
         and meta['player']=='sonya' and meta['strategy']=='defensive_leg' and meta['assistance']=='none'
         and not meta['cheats_enabled'],'Actual terminal unassisted current capture; not verification acceptance')
    report=ROOT/'audit_v3445_current_campaign_selection_counterexamples/report.json'
    proof=json.loads(report.read_text())
    need(proof['passed'] and len(proof['actualSpecificCounterexamples'])==4
         and proof['samePathWholeNativeCampaignPositiveAccepted'] and not proof['actualCaptureOrGameChanged']
         and not proof['fullPortAcceptance'],'Qualified actual confirmation faults and original full-campaign positive')
    pins={}
    def pin(path,digest=None):
        key=str(Path(path).resolve());digest=digest or sha(key)
        need(key not in pins or pins[key]==digest,'Consistent fresh pins')
        need(key not in state['inputHashes'] or state['inputHashes'][key]==digest,'Never relabel parent evidence')
        need(sha(key)==digest,'Actual current relevant bytes unchanged');pins[key]=digest
    pin(PREVIOUS);pin(report);pin(__file__);pin(native.__file__)
    pin(ROOT/'tools/analyze_current_highkick_campaign_v3447.py')
    for file,digest in proof['inputHashes'].items():pin(file,digest)
    for name in ('result.json','run.log','input_hashes_before.json','source_snapshot_paths.json','guest_maincpu.bin'):pin(CASE/name)
    for relative in (state['currentCMD'],state['currentPlaytestZIP'],
        'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
        'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        key=str((ROOT/relative).resolve());pin(key,state['inputHashes'][key])
    state['inputHashes']=pins
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),
        parentCheckpointSHA256=pins[str(PREVIOUS)],mergeRule='Resolve parent recursively, preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
        previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress and verified wait: four actual completed-confirmation/final-time-limit faults reject intended true-ID/due-time invariant; same-path whole native3421 positive passes3445. Existing current Sonya defensive_leg3426 terminal20562 exit0 at213357frames/114756live fields/60selections/59losses/16stages/no ending. Natural Kintaro-to-Shao progression observed, not yet accepted. Exact full3440 verifier73027 confirmed live; no restart on timeout. Ordered native outcome analyzer3447 prepared but not executed or accepted. Ring3432/3439 and whole3421 proof retained. All original five groups remain; no game/public/build/WAV changes.',
        currentCampaignCompletedSelectionFaultReport=str(report),currentCampaignCompletedSelectionQualifiedFaults=4,
        currentSonyaDefensiveLegCampaignTerminal=True,
        pendingCurrentNaturalDefensiveLegHighkickCampaign=dict(capture=str(CASE),terminal=True,
            acceptance=False,independentVerifierExecSessionId=73027,verifier=str(Path(native.__file__).resolve()),
            pendingVerifierReport=str(ROOT/'audit_v3446_current_sonya_defensive_leg_campaign_checked/report.json')),
        pendingCampaignLogNotPinnedWhileMutable=False,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(pins),
        historicalPinMapCopiedAgain=False,
        nextAction='Poll exact live verifier73027, not terminal capture20562. Never restart on observation timeout. If3446 passes, execute3447 ordered Sonya outcomes to fresh3448, then retain exact Kintaro win/advance and Shao damage/activation/control limitations.17561/20562 terminal0; no other live captures remain. Do not rerun completed3432/3439/3441/3445. No ending/whole-port claim from16stages or read-only proofs. Keep all five original requirements, unchanged public1836/dev3172, compressed bounded evidence and cleanup exclusions.')
    need(state['remaining']==remaining,'Full goal intact')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless checkpoint compression')
    print(json.dumps(dict(saved=str(path),goalStatus='active',remainingGroups=5,
        completedSelectionFaults=4,campaignVerifierPending=73027,freshPins=len(pins),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
