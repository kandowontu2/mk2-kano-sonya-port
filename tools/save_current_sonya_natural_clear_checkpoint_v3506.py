"""Actual current Sonya natural clear/own pages/attract; full port remains open."""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_campaign_shao_ring_retreat_v3491 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
PREVIOUS=ROOT/'audit_v3484_current_guarded_outcomes_ring_pending_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3507_current_sonya_natural_clear_full_scope_checkpoint'
CASE=ROOT/'audit_v3490_current_sonya_natural_ring_retreat_campaign'
def main():
    need(not OUT.exists(),'Immutable full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining'];fresh={}
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance']
       and not state['finishedRelease'],'All original full-port requirements remain')
    def pin(path,digest=None):
        key=str(Path(path).resolve());digest=digest or sha(key)
        need(key not in fresh or fresh[key]==digest,'Consistent fresh evidence')
        need(key not in state['inputHashes'] or state['inputHashes'][key]==digest,'Never relabel parent proof')
        fresh[key]=digest
    def checked(relative):
        path=ROOT/relative;value=json.loads(path.read_text())
        need(value['passed'] and not value['fullPortAcceptance'],'Actual bounded proof, not whole port')
        pin(path)
        for file,digest in value['inputHashes'].items():pin(file,digest)
        return value
    campaign=checked('audit_v3494_current_sonya_ring_campaign_checked/report.json')
    prefix=checked('audit_v3493_current_ring_campaign_prefix_checked/report.json')
    outcome=checked('audit_v3505_current_ring_native_deciding_route_outcomes/report.json')
    exposure=checked('audit_v3498_current_ring_campaign_incoming_exposure/report.json')
    need(campaign['current3172WholeGuestAndCampaignAccepted'] and campaign['unassisted_clear_proven']
       and campaign['player']=='sonya' and campaign['human_slot']==1
       and campaign['ending_starts']==campaign['ending_completions']==1
       and campaign['actualShaoNativeRingEntries']==122 and campaign['native_own_round_wins']==39
       and len(campaign['specificActualInputCounterexamples'])==2,
       'Current true Sonya full ordinary-input campaign/own ending/attract and actual Ring replay faults')
    need(prefix['wholeActualPreShaoRecords']==115802 and prefix['actualFirstShaoField']==100927
       and len(prefix['qualifiedActualChronologyFaults'])==3,'Full ordinary/Kintaro chronology unchanged')
    need(outcome['nativeCampaignClearProven'] and outcome['actualSuccessfulShaoMatch']['actualSuccessfulShaoMatchKOFrames']==[113761,115803]
       and outcome['actualSuccessfulShaoMatch']['firstRoundOwnWinnerTableFrame']==113764
       and outcome['actualSuccessfulShaoMatch']['firstRoundNativeResultTransitionFrame']==113765
       and outcome['actualSuccessfulShaoMatch']['finalNativeBossDeathTransitionFrame']==115806
       and outcome['actualSuccessfulShaoMatch']['finalNativeEndingRetirementFrame']==116091
       and outcome['actualSuccessfulShaoMatch']['finalNativeHealth']=='11,0'
       and len(outcome['actualDecidingRouteQualifiedFaults'])==3 and outcome['samePathDecidingRoutePositiveAccepted'],
       'Two earned boss KOs within one successful paid attempt, actual original next-field WIN boundary and distinct final mode11/retirement')
    need(not outcome['childParentGuardBranchAndFullRingRuntimeContactProven'] and outcome['unclassifiedCollisionDamage']==1468,
       'Do not promote generic collision/temporal proximity to full Ring child ownership/guard proof')
    need(exposure['actualIncomingStores']==20 and exposure['actualIncomingDamage']==816,
       'Ordered own-action incoming exposure remains independent of input guard intent')
    result=json.loads((CASE/'result.json').read_text(encoding='utf-8-sig'))
    need(result['exit_code']==0 and result['raw_audio_files_written']==result['new_builds_or_rom_copies']==0,
       'Original cold campaign handle8660 terminal0; full checker79173 terminal0')
    viewed=['ending_page1_late_117194.png','ending_page2_late_117980.png','ending_return_to_attract.png']
    for name in viewed:pin(CASE/'snap'/name)
    for name in('tools/analyze_current_ring_campaign_outcomes_v3495.py','tools/analyze_current_ring_final_ko_outcomes_v3500.py',
       'tools/analyze_current_ring_deciding_route_v3502.py','mk2ks_campaign_shao_ring_observer_v3499.lua'):pin(ROOT/name)
    for relative in(state['currentCMD'],state['currentPlaytestZIP'],
       'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe','diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        key=str((ROOT/relative).resolve());pin(key,state['inputHashes'][key])
    pin(PREVIOUS);pin(__file__)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for(file,digest),actual in zip(fresh.items(),pool.map(sha,fresh)):need(actual==digest,'Fresh source/capture/manual-frame/public proof bytes unchanged')
    state['inputHashes']=fresh
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),parentCheckpointSHA256=fresh[str(PREVIOUS)],
       mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
       previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=state['thisGoalTurnClassification'],
       thisGoalTurnClassification='progress and verified wait: poll confirmed live8660, native Ring/Shao win observed without early acceptance;8660 terminal0.3494 full independently assembled current guest/compiled inputs/physical replay/native true IDs/health/win/progression/own pages/attract passes79173, unassisted cleartrue,122actual Ring entries39ownwins18paidlosses.3493 whole115802pre-Shao chronology3qualified faults.3505 corrected deciding route proves twoactualoriginalcollisionShaoKOs113761/115803 since last112077paidloss, firstWIN113764→nextSTATE113765, distinct finalbossdeath115806→ownretirement116091health11,0;3qualified actual route faults/same-path positive.3495/3500/3502 failed checker assumptions preserved, not evidence; superseded source-bound original next-field/final-KO handling, no game/capture edits.3498 incoming20stores816damage;97opponentcollisionstores1468damage cannot be attributed to Ring child/parent from existing observer.3499 optional read-only child/guard/scaler observer prepared only, not loaded or accepted. Manually view actual two own Sonya story pages and MKII cast-of-characters attract. Natural Sonya P1 route accepted, not all endings/audio/pixels or full port. All five original groups remain; no public/game/build/WAV changes.',
       pendingCurrentNaturalRingRetreatCampaign={},currentRingRetreatCampaignTerminal=True,allCurrentExecHandlesTerminal=True,
       current3172SonyaNaturalCampaignClearAccepted=True,current3172SonyaNaturalCampaignHumanSlot=1,
       current3172SonyaNaturalCampaignReport=str(ROOT/'audit_v3494_current_sonya_ring_campaign_checked/report.json'),
       current3172SonyaNaturalDecidingRouteReport=str(ROOT/'audit_v3505_current_ring_native_deciding_route_outcomes/report.json'),
       current3172SonyaNaturalCampaignOwnRoundWins=39,current3172SonyaNaturalCampaignPaidContinues=18,
       current3172SonyaNaturalCampaignOwnEndingAndAttractAccepted=True,
       current3172SonyaNaturalCampaignKintaroWinFrames=[98392,100403],
       current3172SonyaNaturalCampaignShaoKOFrames=[113761,115803],
       current3172SonyaNativeOwnStoryPagesManuallyViewed=True,current3172SonyaNativeCastAttractManuallyViewed=True,
       current3172SonyaNaturalEndingManuallyViewedFrames=viewed,
       current3172AllEndingPixelsAudioContextsAccepted=False,actualEndingsAccepted=False,
       currentRingBossCollisionOrVictoryAccepted=False,currentRingBossGenericCollisionAndNativeVictoryAccepted=True,
       currentRingBossChildParentGuardAndFullRuntimeContactAccepted=False,
       currentRingBossObservedOriginalCollisionStores=97,currentRingBossObservedOriginalCollisionDamage=1468,
       currentShaoRingObserverSourcePrepared=str(ROOT/'mk2ks_campaign_shao_ring_observer_v3499.lua'),
       currentShaoRingObserverRuntimeAccepted=False,
       gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
       publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,newExecutableROMOrRawAudioCopiesThisTurn=0,
       inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),historicalPinMapCopiedAgain=False,
       nextAction='Do not rerun completed3490/3494/3493/3505/3498 for continuity. Natural true Sonya P1 campaign/own story/attract now proven on current3172; all-ending audio/pixels/contexts not promoted. Next use source-only Shao projectile pattern as normal Kano D,B,HP input successor, retaining exact accepted3408 zoning ordinary/Kintaro/native observers and true17; full native verifier must explicitly allow only genuine17Knife atstage16. No power/AI/difficulty/health/RNG changes. Alternatively freeze/load prepared3499 read-only observer in a fresh same-policy Sonya campaign to prove actual child/parent/guard/damage/retirement, with control chronology comparison. All five original broader arena/victim/effect/audio, full-move/art/shadow/CPU/repeat/KO/overlap, other finishers/morphs/secrets/cinematics, both natural boss/endings/attract, final combinedUI/audio/cleanup/refreshedZIP groups remain. Use compressed fresh evidence and current build; no new builds/WAVs/retired recoveries or historical pin-map copies.')
    need(state['remaining']==remaining,'Entire original goal remains intact')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless full-scope checkpoint compression')
    print(json.dumps(dict(saved=str(path),goalStatus='active',remainingGroups=5,sonyaNaturalClearAccepted=True,
       ownStoryAndAttractAccepted=True,allHandlesTerminal=True,freshPins=len(fresh),fullPortAcceptance=False),indent=2),flush=True)
if __name__=='__main__':main()
