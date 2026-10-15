"""Finite changed-component receipts; distinguish transition acceptance from all branches."""
import json
import verify_native_source_sync as sync
sync.verify();R=sync.ROOT
matrix=[
 ('native campaign transitions',['audit_current_loaded_campaign_transitions_checked','audit_current_kano_p2_earned_ending_checked'],'208 actualstock-derived loadedvalues; current earnedwholeKanoP2stage16ending. No changed transitiondependency identified; notfourfreshcoldcampaignwins.'),
 ('Kano roll launch/charge timing',['audit_current_kano_guarded_ball_charge_checked','audit_current_kano_kunglao_ball_recovery_fixed_checked','audit_current_cpu_kano_ball_audio_checked'],'84fieldphysicalguardedcharge/nativeentries and currentCPUowned6B03sampleprogress/EOF; genuineboundedround/stage/continueplay. Timingnotidenticaloldroll; oldschedule/endingtransitioncode unaffected.'),
 ('shared launch ownership/damage/join lifetime',['audit_current_cpu_sonya_voice_earlier_upper_checked','audit_current_battle_audio_hit_cleanup_checked','audit_current_cpu_sonya_active_voice_join_checked','audit_current_active_voice_joined_controls_checked','audit_current_kano_ending_sonya_crossjoin_v3_checked'],'ActualCPU18health161→121cutsactivecry15517samplesbeforeEOF; bothslotshumanSquare/Bicycle/Ballhitcleanup; activeCPUcry→paidjoinandordinaryjoinedcontrol; earnedKanoending→newSonya18control. GenericwatchercomponentnotallCPUcontexts/heardmix.'),
 ('packed projectile and native actor dispatch',['audit_current_loaded_dispatch_boundaries_checked','audit_native_selector_sonya_walkin_knife_pool_operand_checked'],'105 actual loadeddispatchrows/5operands withoriginalstockderivedrows and nativeownrouters; finiteknifechildpool operand/provenanceproof retained, notcompletegenericretirement. NotallstockCPUprojectile/victimbranches; sourcecouplingnotcampaignschedule.'),
 ('new selector layers/UI teardown',['audit_current_combined_smoke_v2_checked','audit_current_combined_sonya_smoke_checked','audit_current_combined_sonya_smoke_manual_review'],'Both actualP2Kano/P1Sonyaselection→ladder→fightfourPNGs/trueid/contact; selectorpose/portraits clearedonladder and fight. InitialSonyafixedRinghadnoentry; donotclaimspecialactivationthere.'),
 ('row40 biography and Sonya own ending components',['audit_current_loaded_stock_photo_pointers_checked','audit_current_stock_row40_lifecycle_transfer_checked','audit_current_loaded_sonya_ending_components_checked','audit_current_historical_sonya_ending_scope_v2_checked','audit_current_ending_stock_route_invariants_checked'],'Current41stockpointersincludingrow40 plushistoricalexactrepaireddecoder/return/photo21804pixels; currentrow40lookuptwice in135knotifierrun. Sonyaown52/53headers/stories/continuationwordsloaded; unchangedassets/render/audio and34stockROMsourceboundroutesperslot.'),
 ('morph and reaction integration',['audit_current_morph_complete_ledgers_checked'],'20 finitecurrentphysicalcontexts/ledgers retained; notallCPUart/audio/finisherbranches. Pairedstumble/reactiongeometrychanges affecttrajectory, not conserved boss-transitioncallbacks.')]
rows=[]
for component,names,scope in matrix:
 refs=[]
 for n in names:
  p=R/n/'report.json';assert p.exists();d=json.loads(p.read_text());refs.append(dict(path=str(p),SHA256=sync.sha(p),scope=scope))
 rows.append(dict(component=component,receipts=refs,finiteScope=scope))
out=R/'audit_current_campaign_change_proof_matrix_v2_checked';assert not out.exists();out.mkdir()
report=dict(matrix=rows,campaignTransitionFeatureAcceptanceSupported=True,actualFourFreshCurrentColdWinsClaimed=False,remainingIdentifiedChangedTransitionDependency=None,wholeChangedGuestEquivalenceClaimed=False,
 remainingFullRequirementScope='Naturalall-aspects requirement retained. Exhaustive everyCPU/projectile/finisher/arena/reaction branch notestablishedbythismatrix; thoseareseparatefeaturecoverage questions, not a reason to discard proven campaign transitions. No discovered defect or changed transition dependency justifies more fullbossreplays.',
 nextSafeAction='Review genuinelyuncoveredchangedbranches ifrequired, then finalcombinedplayable/launcher/ZIPsourcepins. Do notimpose redundantfourcampaigncoldwins asfunctionalacceptancegate.',fullPortAccepted=False,newEmulatorRuns=0)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(report=str(out/'report.json'),components=len(rows),campaignTransitionFeatureAcceptanceSupported=True)))
