"""Full objective checkpoint: measured guard failure, genuine Ring trial pending."""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import current_shao_ring_source_v3487 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
PREVIOUS=ROOT/'audit_v3473_current_ring_mirror_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3484_current_guarded_outcomes_ring_pending_full_scope_checkpoint'
CASE=ROOT/'audit_v3490_current_sonya_natural_ring_retreat_campaign'
def main():
    need(not OUT.exists(),'Immutable full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining'];fresh={}
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance']
         and not state['finishedRelease'] and not state['actualEndingsAccepted'],'Entire original goal remains unachieved')
    def pin(path,digest=None):
        key=str(Path(path).resolve());digest=digest or sha(key)
        need(key not in fresh or fresh[key]==digest,'Consistent current evidence')
        need(key not in state['inputHashes'] or state['inputHashes'][key]==digest,'Never relabel parent evidence')
        fresh[key]=digest
    def checked(relative):
        path=ROOT/relative;value=json.loads(path.read_text())
        need(value['passed'] and not value['fullPortAcceptance'],'Bounded actual evidence only')
        pin(path)
        for file,digest in value['inputHashes'].items():pin(file,digest)
        return value
    campaign=checked('audit_v3474_current_sonya_guarded_highkick_campaign_checked/report.json')
    prefix=checked('audit_v3476_current_guarded_highkick_prefix_checked/report.json')
    outcome=checked('audit_v3478_current_guarded_highkick_campaign_outcomes/report.json')
    exposure=checked('audit_v3480_current_guarded_highkick_incoming_exposure/report.json')
    gate=checked('audit_v3482_current_ring_boss_frontgate_checked/report.json')
    source=checked('audit_v3489_current_shao_ring_source_checked/report.json')
    need(campaign['current3172WholeGuestAndCampaignAccepted'] and campaign['bounded_campaign_evidence_proven']
       and not campaign['unassisted_clear_proven'] and not campaign['finalTimeLimitInterruptedSelection'],
       'Actual terminal whole guest/inputs/native state/health/wins/progression verified')
    need(prefix['wholeActualPreShaoRecords']==115802 and prefix['actualFirstShaoField']==100927
       and len(prefix['qualifiedActualChronologyFaults'])==3,'Entire actual pre-Shao chronology exact, not independent Kintaro coverage')
    need(outcome['actualCurrentKintaroMatchClear']['ownWinFrames']==[98392,100403]
       and outcome['actualShaoRoundWins']==outcome['actualEndingEvents']==0
       and outcome['actualNative0113Assignments']==355 and outcome['actualShao0113Damage']==651,
       'Real Kintaro match retained; guard105 did not earn a Shao win or ending')
    need(exposure['actualIncomingDamage']==15456 and exposure['ownActualActionAtIncomingCollision']['0302']['damage']==15031
       and not exposure['controllerImprovementAccepted'],'Ordered incoming exposure, no unsupported controller-improvement claim')
    need(source['ordinaryAndKintaroControlsAndNativeObserversExact'] and len(source['actualQualifiedSourceFaults'])==4
       and source['samePathSourcePositiveAccepted'],'Declared signature-command delta, not game mutation')
    need(not(CASE/'result.json').exists(),'Current Ring campaign remains live/pending, not accepted')
    before=json.loads((CASE/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    snapshots=json.loads((CASE/'source_snapshot_paths.json').read_text(encoding='utf-8-sig'))
    for file,digest in before.items():
        pin(file,digest)
        if Path(file).suffix in('.lua','.ps1','.json'):
            target=Path(snapshots[file]).resolve();need(target.is_relative_to((CASE/'input_sources/tree').resolve()),'Collision-free source hierarchy')
            pin(target,digest)
    for name in('input_hashes_before.json','source_snapshot_paths.json','guest_maincpu.bin'):pin(CASE/name)
    need(sha(CASE/'guest_maincpu.bin')=='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7','Unchanged current guest initialized')
    for relative in(state['currentCMD'],state['currentPlaytestZIP'],
       'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe','diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        key=str((ROOT/relative).resolve());pin(key,state['inputHashes'][key])
    pin(ROOT/'tools/verify_current_campaign_shao_ring_retreat_v3491.py');pin(PREVIOUS);pin(__file__)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for(file,digest),actual in zip(fresh.items(),pool.map(sha,fresh)):need(actual==digest,'Current proof/source/capture/public byte unchanged')
    state['inputHashes']=fresh
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),parentCheckpointSHA256=fresh[str(PREVIOUS)],
       mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
       previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=state['thisGoalTurnClassification'],
       interveningAcknowledgmentClassification='no progress: thanks acknowledgment only; this continuation revalidated authoritative files and completed actual analyses',
       thisGoalTurnClassification='progress and verified wait: terminal3462 and3474 full native acceptance revalidated.3476 compares115802 actual pre-Shao rows including inputs/HP/IDs/drawing rows, with3qualified faults.3478/3480 ordered outcomes prove355actual0113 activations651damage,384incomingstores15456damage, zero Shao wins/endings; no controller improvement.3482 original Ring victim-ID frontgate excludes16, not13, source-only inference not collision proof.3485/3486 genuine D,F,LP/retreat Shao-only physical successor;3489 four qualified source faults/same-path positive.3491 whole current guest/native verifier construction smoke passes; only true native18 Ring stage16 explicitly permitted, original full special instruction/actor/Main and HP/win/progression gates retained. New compressed3490 cold Sonya campaign live8660, no acceptance. No game/build/public/WAV changes; all five original groups preserved.',
       pendingCurrentNaturalGuardedHighkickCampaign={},currentGuardedHighkickCampaignTerminal=True,
       currentGuardedHighkickCampaignCheckedReport=str(ROOT/'audit_v3474_current_sonya_guarded_highkick_campaign_checked/report.json'),
       currentGuardedHighkickActualPrefixReport=str(ROOT/'audit_v3476_current_guarded_highkick_prefix_checked/report.json'),
       currentGuardedHighkickOutcome=outcome['actualCurrentKintaroMatchClear'],
       currentGuardedHighkickActualNative0113Assignments=355,currentGuardedHighkickActualShaoDamage=651,
       currentGuardedHighkickActualIncomingDamage=15456,currentGuardedHighkickActualShaoWins=0,
       currentGuardedHighkickControllerImprovementAccepted=False,
       currentRingBossFrontgateReport=str(ROOT/'audit_v3482_current_ring_boss_frontgate_checked/report.json'),
       currentRingBossFrontgateOnlySourceInference=True,currentRingBossCollisionOrVictoryAccepted=False,
       pendingCurrentNaturalRingRetreatCampaign=dict(capture=str(CASE),execSessionId=8660,terminal=False,acceptance=False,
          candidate='diagnostic_v3172_native_morph_shadow',player='sonya',humanSlot=1,strategy='defensive_leg',bootFrame=600,seconds=3900,
          verifier=str(ROOT/'tools/verify_current_campaign_shao_ring_retreat_v3491.py')),
       pendingCampaignLogNotPinnedWhileMutable=True,
       gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
       publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,newExecutableROMOrRawAudioCopiesThisTurn=0,
       inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),historicalPinMapCopiedAgain=False,
       nextAction='Poll exact live8660 for3490; never restart on timeout. Once terminal run3491 into fresh checked report; compare115802 complete normalized pre-Shao records to accepted3462, labels only. Analyze actual Ring entries separately from native child collision/HP/guard/scaler/lifetime/recovery; do not assume source frontgate or physical command implies hit. Capture future actual child/parent/guard branch details if current log cannot prove them. Preserve both current Kintaro match proofs and Ring CPU hit/mirror art/shadow/erase without expanding all contexts. Actual Shao campaign clear, own ending and return to attract still unproven. All five full-port groups remain; no new build/WAV copies, retired recoveries or broad historical rehash.')
    need(state['remaining']==remaining,'Full original objective intact')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless checkpoint compression')
    print(json.dumps(dict(saved=str(path),goalStatus='active',remainingGroups=5,guardedCampaignVerified=True,
       actualShaoWins=0,pendingRingSession=8660,freshPins=len(fresh),fullPortAcceptance=False),indent=2),flush=True)
if __name__=='__main__':main()
