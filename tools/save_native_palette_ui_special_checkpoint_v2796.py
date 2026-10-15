"""Retain the whole native-character goal after fresh UI and move-state work.

The previous complete historical graph was revalidated at v2787. This successor
retains that entire graph and revalidates every dependency used by this turn's
new proofs, without claiming another full historical-graph validation. Actual
blade endpoint differences remain open; the public playtest is not promoted.
"""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT=assembly.ROOT
PREVIOUS=ROOT/'audit_v2787_native_friendship_palette_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2797_native_palette_ui_special_full_scope_checkpoint'

def save():
    prior=json.loads(PREVIOUS.read_text());fresh={}
    assembly.need(prior['goalStatus']=='active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and
        len(prior['remaining'])==5 and len(prior['currentSourceBoundBossCampaigns'])==70 and
        prior['currentRealShaoKahnMatchClears']==0 and not prior['actualEndingsAccepted'],'Entire original unfinished objective retained')
    inherited=dict(prior['inputHashes'])
    def pin(path,wanted=None):
        path=Path(path)
        key=str((path if path.is_absolute() else ROOT/path).absolute())
        if wanted is None:wanted=assembly.sha(key)
        assembly.need(key not in fresh or fresh[key]==wanted,'Consistent fresh source dependency '+key)
        assembly.need(key not in inherited or inherited[key]==wanted,'Immutable historical dependency '+key)
        fresh[key]=wanted
    def proof(leaf):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        assembly.need(value['passed'] and value['candidate']==assembly.NAME and not value.get('fullPortAccepted',False),'Actual scoped new proof '+leaf)
        for path,wanted in value['inputHashes'].items():pin(path,wanted)
        return value,str(path)
    ui,ui_path=proof('audit_v2789_native_palette_ui_checked')
    ui_units,ui_units_path=proof('audit_v2793_native_palette_ui_units')
    specials,specials_path=proof('audit_v2792_native_palette_special_state_checked')
    special_units,special_units_path=proof('audit_v2795_native_palette_special_state_units')
    assembly.need(ui['currentBothSlotSelectionLadderFirstMatchAccepted'] and len(ui['cases'])==4 and
        all(c['true_id']==(17 if c['fighter']=='kano' else 18) and c['first_match_participant_fields']==362 and
            c['rendered']['blink_colors']>=2 and c['rendered']['native_name_shadow_checks']>=4 for c in ui['cases'].values()),
        'Actual all-four-slot native navigation/blink/number/animation/clear/ladder/identity/shaded-name gate')
    assembly.need(ui_units['methods']==46,'Actual source-bound UI regression rejection suite')
    assembly.need(specials['current52CaseHumanStateMatrixAccepted'] and specials['everyCheckedBuildNativeEventMatched'] and
        specials['positiveCases']==18 and specials['negativeCases']==34 and specials['pairedFields']==46178 and
        specials['nativeEvents']==61250 and specials['exactCheckedBuildEndpointScenes']==154 and
        not specials['allEndpointScenesAccepted'] and len(specials['unresolvedEndpointDifferences'])==2,
        'Actual full native-state matrix and explicit unresolved endpoint differences')
    for value in specials['unresolvedEndpointDifferences']:
        assembly.need(value['case'] in ('audit_v2791_human_blade_p1','audit_v2791_human_blade_p2') and
            value['file']=='special_recovered.png' and not value['differencesMasked'] and
            not value['sourceBoundCauseProven'],'Do not silently accept blood-like scene differences')
    assembly.need(special_units['cases']==52 and special_units['actualSpecificCounterexamplesRejected']==416,
        'Actual every-fixture identity/ownership/field/input/health/recovery corruptions rejected')
    failed_path=ROOT/'audit_v2794_native_palette_special_state_units/report.json'
    failed=json.loads(failed_path.read_text());assembly.need(not failed['passed'] and failed['error'],
        'Executed diagnostic failure retained: fixed wrong-owner constant already equaled P2 owner')
    pin(failed_path);pin(ROOT/'tools/test_native_palette_special_state_v2794.py')
    dispatch_path=ROOT/'audit_v2790_native_palette_special_dispatch/report.json'
    dispatch=json.loads(dispatch_path.read_text());pin(dispatch_path)
    assembly.need(dispatch['allRunnersTerminal'] and dispatch['allRunnerExitsZero'] and len(dispatch['cases'])==52,
        'Every actual cold runner terminal with zero exit')
    pin(PREVIOUS);pin(__file__)
    for path,wanted in {
        'PLAY_MK2_KANO_SONYA.cmd':'631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7',
        'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
        'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
        'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
        'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644',
        'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    }.items():pin(ROOT/path,wanted)
    print('Revalidating fresh relevant proof graph:',len(fresh),'actual files',flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for (file,wanted),actual in zip(fresh.items(),pool.map(assembly.sha,fresh)):
            assembly.need(actual==wanted,'Changed fresh evidence '+file)
    inherited.update(fresh)
    prior.update(previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification='no progress: status-only answer inspected the checkpoint/launcher but did not implement or gather new gameplay evidence',
        thisGoalTurnClassification='progress: four cold physical native UI campaigns and 52 cold physical special/defense/miss cases ran on isolated v2753. All four native selection/animation/blink/player-number/backdrop/teardown/ladder/actual identity/name-shadow contracts passed. Original 46 UI test methods passed; 416 actual state/input corruptions across all 52 fixtures rejected. All 61250 physical native events and 46178 paired fields match public v1836 after bank-only allocation normalization. 154/156 endpoint scenes byte-exact; two blade recovery scenes differ by 804/1068 pixels and remain unaccepted pending original-native-blood source reconstruction. No guest code, public launcher or release changed. Entire original goal remains unfinished.',
        candidateUnderTestFourNativeUIRegressionAccepted=True,candidateUnderTestNativeUIReport=ui_path,
        candidateUnderTestNativeUIRejectionReport=ui_units_path,candidateUnderTestNativeUIUnitMethods=46,
        candidateUnderTestNativeUIFirstMatchParticipantFields=1448,
        candidateUnderTest52CaseHumanStateMatrixAccepted=True,candidateUnderTestHumanStateReport=specials_path,
        candidateUnderTestHumanStateRejectionReport=special_units_path,
        candidateUnderTestHumanStateSpecificCounterexamples=416,candidateUnderTestHumanStatePairedFields=46178,
        candidateUnderTestHumanStateNativeEventsMatched=61250,
        candidateUnderTestExactCheckedBuildEndpointScenes=154,candidateUnderTestAllEndpointScenesAccepted=False,
        candidateUnderTestUnresolvedBladeEndpointDifferences=specials['unresolvedEndpointDifferences'],
        candidateUnderTestBladeBloodCauseInferredNotProven=True,
        candidatePromotionGates=[
            'Repeated natural bubble palette allocation/release across matches and both slots',
            'Source-bound original native blood/full draw/continuous erase for both changed blade recovery scenes; broader move/morph/ordinary-combat/CPU/KO/overlap regressions after shared allocator/reset change (fresh 52-case human states accepted)',
            'Fresh full original Friendship audible PCM/tail/overlap checks, including actual randomized Sonya variants'],
        candidateUnderTestAllOriginalScopeRequirementsStillRetained=True,
        lastCompleteHistoricalGraphValidationCheckpoint=str(PREVIOUS),
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
        gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False,oldBuildFoldersDeletedThisTurn=0,
        nativeDifficultyHealthAIPositionStageRNGModified=False,actualEndingsAccepted=False,
        fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
        nextAction='Keep v2753 isolated. Capture both positive blade scenes with unchanged physical controls plus read-only native full drawing/queue/palette/RNG observation. Independently reconstruct original native blood source/palette/position decisions and complete drawing/continuous erasure, rather than masking changed pixels or forcing old RNG values. Bind captures to independently expected whole guest and the same v2753 endpoint PNGs. Then repeat palette lifetime/reuse across matches, affected move/morph/CPU/KO/overlap and complete original Friendship audio PCM controls. Only after all promotion gates pass update the launcher. All original arena/victim/mirror/stage effects/move-phase/grounding/floor shadows/finishers/secrets/cinematics/full natural boss match clears/own endings/attract/final integration/cleanup/refreshed ZIP requirements remain.',
        inputHashes=inherited)
    return prior

if __name__=='__main__':
    assembly.need(not OUT.exists(),'Immutable entire-goal successor checkpoint')
    report=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(goalStatus=report['goalStatus'],publicCandidate=report['currentCandidate'],
        candidateUnderTest=report['candidateUnderTest'],fourNativeUIAccepted=True,humanStateCases=52,
        nativeEvents=61250,exactEndpointScenes=154,unresolvedEndpointScenes=2,
        fullPortAcceptance=False,finishedRelease=False,freshRevalidatedPins=report['revalidatedFreshRelevantFilePins']),indent=2),flush=True)
