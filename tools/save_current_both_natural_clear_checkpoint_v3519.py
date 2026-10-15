"""Both current true-character P1 natural clears; full objective remains active."""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_campaign_shao_knife_observer_v3526 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
PREVIOUS=ROOT/'audit_v3507_current_sonya_natural_clear_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3520_current_both_natural_clear_full_scope_checkpoint'
CASE=ROOT/'audit_v3516_current_kano_natural_knife_retreat_campaign'
def main():
    need(not OUT.exists(),'Immutable full objective checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining'];fresh={}
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance']
       and not state['finishedRelease'] and state['current3172SonyaNaturalCampaignClearAccepted'],
       'Full scope and accepted current Sonya route retained')
    def pin(path,digest=None):
        key=str(Path(path).resolve());digest=digest or sha(key)
        need(key not in fresh or fresh[key]==digest,'Consistent current relevant source/evidence')
        need(key not in state['inputHashes'] or state['inputHashes'][key]==digest,'Never relabel parent evidence')
        fresh[key]=digest
    def checked(relative):
        path=ROOT/relative;value=json.loads(path.read_text())
        need(value['passed'] and not value['fullPortAcceptance'],'Actual bounded proof only')
        pin(path)
        for file,digest in value['inputHashes'].items():pin(file,digest)
        return value
    source=checked('audit_v3514_current_shao_knife_source_checked/report.json')
    model=checked('audit_v3518_current_knife_boss_source_checked/report.json')
    gate=checked('audit_v3528_current_frozen_knife_observer_rule_checked/report.json')
    campaign=checked('audit_v3521_current_kano_knife_campaign_checked/report.json')
    prefix=checked('audit_v3523_current_knife_campaign_prefix_checked/report.json')
    outcome=checked('audit_v3525_current_knife_native_deciding_route_outcomes/report.json')
    need(source['ordinaryAndKintaroControlsAndNativeObserversExact'] and len(source['actualQualifiedSourceFaults'])==5
       and gate['originalDynamicCodeAndGuestWriteGateRetained'] and len(gate['actualQualifiedSourceFaults'])==5,
       'Exact stage16 physical Knife delta/read-only observer, original strict control protection')
    need(campaign['current3172WholeGuestAndCampaignAccepted'] and campaign['unassisted_clear_proven']
       and campaign['player']=='kano' and campaign['human_slot']==1
       and campaign['ending_starts']==campaign['ending_completions']==1
       and campaign['actualShaoNativeKnifeEntries']==30 and campaign['native_own_round_wins']==33
       and campaign['paid_continue_losses']==7 and len(campaign['specificActualInputCounterexamples'])==2,
       'Actual current native true17 full cold ordinary-input campaign/own ending/attract')
    need(prefix['wholeActualPreShaoRecords']==134329 and prefix['actualFirstShaoField']==79020
       and len(prefix['qualifiedActualChronologyFaults'])==3,'Entire accepted Kano pre-Shao chronology retained including native fields/inputs/drawing rows')
    need(outcome['nativeCampaignClearProven'] and outcome['actualCurrentKintaroMatchClear']['ownWinFrames']==[76520,78384]
       and outcome['actualSuccessfulShaoMatch']['actualSuccessfulShaoMatchKOFrames']==[80764,81767]
       and outcome['actualSuccessfulShaoMatch']['firstRoundOwnWinnerTableFrame']==80767
       and outcome['actualSuccessfulShaoMatch']['firstRoundNativeResultTransitionFrame']==80768
       and outcome['actualSuccessfulShaoMatch']['finalNativeBossDeathTransitionFrame']==81769
       and outcome['actualSuccessfulShaoMatch']['finalNativeEndingRetirementFrame']==82054
       and outcome['actualSuccessfulShaoMatch']['finalNativeHealth']=='29,0'
       and len(outcome['actualDecidingRouteQualifiedFaults'])==3 and outcome['samePathDecidingRoutePositiveAccepted'],
       'Two real earned boss KOs in successful attempt, correct first-WIN callback/final boss-death/retirement')
    need(outcome['unclassifiedCollisionDamage']==426 and not outcome['childParentGuardBranchAndFullKnifeRuntimeContactProven'],
       'Existing generic ledger does not yet certify separately captured child/parent/guard/scaler')
    result=json.loads((CASE/'result.json').read_text(encoding='utf-8-sig'))
    need(result['exit_code']==0 and result['new_builds_or_rom_copies']==result['raw_audio_files_written']==0,
       'Original65795 terminal0, failed26667 terminal1 preserved, corrected56138 terminal0,15388/46748 terminal0')
    viewed=['ending_page1_late_83157.png','ending_page2_late_83942.png','ending_return_to_attract.png']
    for name in viewed:pin(CASE/'snap'/name)
    for relative in(state['currentCMD'],state['currentPlaytestZIP'],
       'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe','diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        key=str((ROOT/relative).resolve());pin(key,state['inputHashes'][key])
    pin(PREVIOUS);pin(__file__)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for(file,digest),actual in zip(fresh.items(),pool.map(sha,fresh)):need(actual==digest,'Fresh actual source/capture/public/manual-frame bytes unchanged')
    state['inputHashes']=fresh
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),parentCheckpointSHA256=fresh[str(PREVIOUS)],
       mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
       previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=state['thisGoalTurnClassification'],
       thisGoalTurnClassification='progress: inspect accepted3507Sonya clear/3412currentKano proof/current unchanged dirty source.3510/3511 real Kano D,B,HP stage16-only Knife/retreat with3508read-only owner/guard/scaler observer.3514 exact entire ordinary/Kintaro controls and runner otherwise unchanged,5qualified actual source faults.3518 independently rebuilt whole current guest confirms own17Knife descriptors/original donor core/native gate/extraction/health/Shao scaler,4actual faults.3516 cold ordinary-input campaign65795 terminal0.3515 failed26667 only because original blanket dofile ban;3526 permits exactly frozen3508EOFload, retains original write/dynamic gate on every other byte;3528 five qualified loader/guest-write faults/same-path positive.3521 whole current guest/compiled inputs/full native IDs/HP/win/progression/physical replay/own story/attract accepted56138;30actualKnifeentries33ownwins7paidlosses.3523 compares134329wholepre-Shao records,3faults46748;3525 twoactualbossKOs80764/81767, firstWIN80767→STATE80768, finalbossdeath81769→ownretirement82054health29,0;3qualified actual route faults15388. Manually viewed actual two own Kano story pages and MKII cast-of-characters attract. Both current P1 natural clears now proven. Thirty actual child creations/retirements observed, but no detailed child/parent/guard/scaler runtime verifier yet; cannot promote426generic collision damage to child proof. All five original requirement groups preserved, no game/power/difficulty/AI/HP/RNG/public/build/WAV changes.',
       allCurrentExecHandlesTerminal=True,pendingCurrentNaturalKnifeRetreatCampaign={},
       current3172KanoNaturalCampaignClearAccepted=True,current3172KanoNaturalCampaignHumanSlot=1,
       current3172KanoNaturalCampaignReport=str(ROOT/'audit_v3521_current_kano_knife_campaign_checked/report.json'),
       current3172KanoNaturalDecidingRouteReport=str(ROOT/'audit_v3525_current_knife_native_deciding_route_outcomes/report.json'),
       current3172KanoNaturalCampaignOwnRoundWins=33,current3172KanoNaturalCampaignPaidContinues=7,
       current3172KanoNaturalCampaignOwnEndingAndAttractAccepted=True,
       current3172KanoNaturalCampaignKintaroWinFrames=[76520,78384],current3172KanoNaturalCampaignShaoKOFrames=[80764,81767],
       current3172KanoNativeOwnStoryPagesManuallyViewed=True,current3172KanoNativeCastAttractManuallyViewed=True,
       current3172KanoNaturalEndingManuallyViewedFrames=viewed,
       current3172BothTrueCharacterP1NaturalCampaignClearsOwnStoryAndAttractAccepted=True,
       current3172AllEndingPixelsAudioContextsAccepted=False,actualEndingsAccepted=False,
       currentKnifeBossObservedNativeCollisionStores=30,currentKnifeBossObservedNativeCollisionDamage=426,
       currentKnifeBossChildParentGuardAndFullRuntimeContactAccepted=False,
       currentKnifeBossCapturedReadOnlyObserver=str(ROOT/'mk2ks_campaign_shao_knife_observer_v3508.lua'),
       gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
       publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,newExecutableROMOrRawAudioCopiesThisTurn=0,
       inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),historicalPinMapCopiedAgain=False,
       nextAction='All current handles terminal; do not rerun completed3516/3521/3523/3525/3518/3528 for continuity. Both current3172 P1 native campaign/own stories/attract proven with ordinary controls/paid continues. Next independently parse captured MK2_BOSS_KNIFE trace3516; prove30real children and original retirements, true17 parent/child/victim13 linkage, actual branch/extraction/raw6or22→originalShao4or16/clampedHP, exact native health stores against full campaign, first2chips26normal2clampedKOstores426damage; qualify actual parent/scaler/branch/orphan faults and same-path positive. Do not infer anything from planned Block or temporal proximity. Ring3490 lacks child ownership trace; use only fresh frozen read-only companion if needed, no restarts of accepted native clear for continuity. Still need wider stage/victim/effect/audio, full phase/art/ground/shadow/cleanup/CPU/repeat/KO/overlap, other finishers/morphs/secrets/cinematics, ending pixels/audio/contexts, final combinedUI/audio/dependency-cleanup/refreshedZIP. Preserve all five original groups and source/public files, use compressed evidence/current build only; no new build/WAV/retired recovery or broad historical rehash.')
    need(state['remaining']==remaining,'Full original objective retained')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless full-scope checkpoint compression')
    print(json.dumps(dict(saved=str(path),goalStatus='active',remainingGroups=5,bothCurrentP1NaturalClearsAccepted=True,
       ownStoriesAndAttractAccepted=True,allHandlesTerminal=True,freshPins=len(fresh),fullPortAcceptance=False),indent=2),flush=True)
if __name__=='__main__':main()
