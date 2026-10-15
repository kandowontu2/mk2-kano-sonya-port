"""Full original goal retained; actual native palette fix in an isolated build.
Earlier accepted evidence is for the unchanged public v1836 playtest, not
silently promoted to the new candidate. Whole historical/new dependency graph
is deduplicated and revalidated once. All original unfinished gates remain.
"""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT=assembly.ROOT
PREVIOUS=ROOT/'audit_v2742_current_friendship_palette_router_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2785_native_friendship_palette_full_scope_checkpoint'
need=assembly.need

def save():
    prior=json.loads(PREVIOUS.read_text())
    need(prior['goalStatus']=='active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and
         len(prior['remaining'])==5 and len(prior['currentSourceBoundBossCampaigns'])==70 and
         prior['currentRealShaoKahnMatchClears']==0 and not prior['actualEndingsAccepted'],
         'Original entire unfinished port goal and natural boss/ending requirements preserved')
    pins=dict(prior['inputHashes']);cases={}
    def pin(path,wanted=None):
        path=str(path)
        if wanted is None:wanted=assembly.sha(path)
        need(path not in pins or pins[path]==wanted,'Consistent complete original-goal dependency '+path)
        pins[path]=wanted
    def proof(path):
        value=json.loads(path.read_text());need(value['passed'] and not value['fullPortAcceptance'],'Actual scoped terminal candidate proof '+str(path))
        pin(path)
        for file,wanted in value['inputHashes'].items():pin(file,wanted)
        return value
    pin(PREVIOUS)
    row_path=ROOT/'audit_v2783_native_friendship_palette_shadow_rows_checked/report.json'
    row=proof(row_path)
    need(row['candidate']==assembly.NAME and row['actualConsecutiveScanouts']==6400 and
         row['actualBoundPixels']==650240000 and row['exactNativeDrawingAndContinuousErasurePasses']==6148 and
         row['sourceDerivedNativeShadowRowsAndBlackPenAccepted'] and row['rejectedActualShadowCounterexamples']==24,
         'Actual four-scene complete drawing/erasure, all original shadow rows and black native pen accepted')
    for side in (1,2):
        palette_path=ROOT/f'audit_v2771_native_kano_friendship_palette_p{side}_checked/report.json'
        palette=proof(palette_path)
        need(palette['candidate']==assembly.NAME and palette['actualPaletteTableSource']==0xfffe2800 and
             palette['actualAllocatorEntrySource']==0xfecdf710 and palette['actualConstructorReferenceCount']==1 and
             palette['finalPaletteReferenceCount']==0 and palette['actualNativeBubblePaletteReferenceReclaimed'] and
             palette['actualPaletteOwnershipAndNativeReferenceCleanupAccepted'] and palette['noPrematurePaletteRelease'] and
             palette['actualCompletePaletteSnapshots']==(1525 if side==1 else 1530) and
             palette['actualReplayedTableStores']==330 and palette['actualNativeReferenceReleases']==52 and
             palette['actualNativeReferenceIncrements']==227 and len(palette['rejectedSpecificCounterexamples'])==5,
             'Both actual typed native palette sources and complete reference/store replay accepted')
        need(palette['actualNativeReleaseFrame']==palette['actualSpritePoolResetFrame']==(4420 if side==1 else 4373) and
             palette['actualTaskReturnFrame']==(4412 if side==1 else 4365) and
             palette['actualSpriteAllocatorReuseFrame']==(4436 if side==1 else 4374),
             'Actual source-bound task return, native pool reset and real sprite reuse')
        cases[f'kano_p{side}']=dict(paletteProof=str(palette_path),shadowRows=row['cases'][f'kano_p{side}'],
            nativePaletteAddress='FFFE2800',rawDonorPaletteAddress='FECDF710',finalReferenceCount=0,
            rawPointerIdentityRequired=False,originalSixteenColorRecordCopiedExactly=True,
            nativePaletteReleaseFrame=palette['actualNativeReleaseFrame'],taskReturnFrame=palette['actualTaskReturnFrame'],
            spritePoolResetFrame=palette['actualSpritePoolResetFrame'],spriteReuseFrame=palette['actualSpriteAllocatorReuseFrame'])
        sonya_path=ROOT/f'audit_v2775_native_sonya_friendship_palette_p{side}_render_diagnostic/report.json'
        sonya=proof(sonya_path)
        need(sonya['fighter']=='sonya' and sonya['side']==side and sonya['control']['actualTrueID']==18 and
             sonya['fullDrawingAndContinuousErasureAccepted'] and sonya['actualConsecutiveScanouts']==1600 and
             sonya['typedChronology']['allPhysicalInputsFramesIdentitiesHealthPosesGeometryColorsAndTransitionsUnchanged'] and
             sonya['typedChronology']['nativeCluckSourceAndFirstFreeVoices']['cues']==39 and
             len(sonya['typedChronology']['rejectedNativeAudioCounterexamples'])==3 and
             not sonya['typedChronology']['fullPCMAcceptance'],
             'Both real Sonya scenes, source-native RNG variants/hold/channel allocation and complete rendering accepted')
        cases[f'sonya_p{side}']=dict(renderProof=str(sonya_path),shadowRows=row['cases'][f'sonya_p{side}'],
            trueID=18,sourceNativeRandomCluckAndFirstFreeVoicesChecked=True,actualCluckCues=39,
            fullAudiblePCMRevalidationPending=True,allAuxiliaryEffectCleanupAcceptance=False)
    # Preserve every executed diagnostic failure, rather than rewriting old
    # expectations/captures or confusing stricter harness failures with crashes.
    failed=[]
    for leaf in ('audit_v2761_native_kano_friendship_palette_p1_checked',
                 'audit_v2762_native_kano_friendship_palette_p1_render_diagnostic',
                 'audit_v2766_native_kano_friendship_palette_p1_checked','audit_v2766_native_kano_friendship_palette_p2_checked',
                 'audit_v2769_native_kano_friendship_palette_p1_checked','audit_v2769_native_kano_friendship_palette_p2_checked',
                 'audit_v2776_native_kano_friendship_palette_p1_erase_diagnostic','audit_v2776_native_kano_friendship_palette_p2_erase_diagnostic'):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text())
        need(not value['passed'] and value.get('error'),'Original actual diagnostic failure retained')
        pin(path);failed.append(dict(report=str(path),error=value['error'],accepted=False))
    for version in ('2746','2748','2757','2758','2764','2768','2763','2770','2772','2773','2774','2779','2782'):
        matches=list((ROOT/'tools').glob(f'*_v{version}.py'))
        need(len(matches)==1,'Unambiguous retained executed source version '+version);pin(matches[0])
    for path in (ROOT/'audit_v2747_native_friendship_palette_assembly_failed/report.json',
                 ROOT/'audit_v2749_native_friendship_palette_assembly_checked/report.json',
                 ROOT/'audit_v2755_native_friendship_palette_build_restoration/report.json',
                 ROOT/'audit_v307_current_end_p1_sonya_p2_kano_miss/input_sources/midtunit.h',
                 ROOT/'tools/build_native_friendship_palette_v2744.ps1'):
        pin(path)
    pin(ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp','EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34')
    pin(ROOT/'mame-mkp/src/mame/midway/midtunit.cpp','07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85')
    pin(ROOT/'mame-mkp/src/mame/midway/midtunit.h','256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644')
    pin(ROOT/'mame-mkp/mkport.exe','413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891')
    pin(ROOT/'PLAY_MK2_KANO_SONYA.cmd','631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7')
    pin(ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd','ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E')
    build=json.loads((ROOT/assembly.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    need(build['prior_candidate']==prior['currentCandidate']=='diagnostic_v1836_ball_register_boundary' and
         build['expected_guest_sha256']=='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7',
         'Isolated source-bound candidate; public current playtest deliberately unchanged')
    pin(__file__)
    print('Revalidating complete deduplicated historical/new full-goal graph:',len(pins),'actual files',flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for index,((file,wanted),actual) in enumerate(zip(pins.items(),pool.map(assembly.sha,pins)),1):
            need(actual==wanted,'Changed full original-goal dependency '+file)
            if index%5000==0:print('Verified',index,'actual dependencies',flush=True)
    prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='no progress: status-only reply checked existing checkpoint/build; no implementation or new gameplay evidence',
        thisGoalTurnClassification='progress: independent native assembly exposed/fixed a branch and complemented-immediate bug before execution; isolated native source candidate compiled. Missing old header restore path recovered through exact matching immutable copy; all three canonical sources and installed historical executable restored exactly. Four cold actual physical K/S matches completed in both slots with 2 earned KOs each. Genuine bubble palette now has its own native record/source and native reference decrement/clock at original pool reset; complete 3055 palette snapshots/660 stores and task/sprite return/reuse accepted. 6400 actual complete scanouts, 6148 source-exact draw/erasure passes and source-derived shadow rows/black native pen accepted. Native randomized Sonya cluck variants/first-free voices verified independently, not forced to repeat older RNG sequence. Original failures retained and specific counterexamples rejected. Public launcher/release unchanged; full original goal remains unfinished.',
        candidateUnderTest=assembly.NAME,candidateUnderTestBuildSHA256=build['executable_sha256'],
        candidateUnderTestGuestSHA256=build['expected_guest_sha256'],candidateUnderTestPayloadSHA256=build['payload_sha256'],
        candidateUnderTestNativeFriendshipPaletteOwnershipAndReferenceCleanupBothSlotsAccepted=True,
        candidateUnderTestFourFriendshipRenderAndShadowCases=cases,candidateUnderTestShadowRowsReport=str(row_path),
        candidateUnderTestCompletePaletteSnapshots=3055,candidateUnderTestReplayedPaletteStores=660,
        candidateUnderTestNativeReferenceReleases=104,candidateUnderTestNativeReferenceIncrements=454,
        candidateUnderTestActualCompleteScanouts=6400,candidateUnderTestActualBoundPixels=650240000,
        candidateUnderTestExactDrawingAndContinuousErasurePasses=6148,
        candidateUnderTestEarlierBroadPublicBuildRegressionsNotAutomaticallyPromoted=True,
        candidateUnderTestAllAuxiliaryEffectsAndArenasAccepted=False,candidateUnderTestOriginalPCMRevalidationPending=True,
        candidatePromotionGates=['Repeated natural bubble palette allocation/release across matches and both slots',
            'Fresh affected selection/ladder/portraits/blink/player-number/no-hint/clear/name-shadow regressions',
            'Fresh special/move/morph/ordinary-combat/CPU/KO/overlap regressions after shared allocator/reset routing change',
            'Fresh full original Friendship audible PCM/tail/overlap checks, including actual randomized Sonya variants'],
        candidateUnderTestPreservedDiagnosticFailures=failed,
        candidateUnderTestExistingCpuDescriptorAndNullSentinelProtectionsUnchanged=True,
        candidateUnderTestExactCanonicalSourceRestorationAccepted=True,candidateUnderTestBuildScriptRestorationExitWasNonzero=True,
        candidateUnderTestNaturalBossAndEndingCampaignsNotYetRun=True,
        earlierAcceptedEvidenceRemainsBoundToPublicCandidate='diagnostic_v1836_ball_register_boundary',
        gameSourceAndPlayableBytesChangedThisTurn=True,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
        oldBuildFoldersDeletedThisTurn=0,newProtectedHistoricalHeaderRecovery=str(ROOT/'audit_v307_current_end_p1_sonya_p2_kano_miss/input_sources/midtunit.h'),
        originalRNGCodeUnchangedButExactRandomVariantSequenceNeedNotRepeat=True,
        nativeDifficultyHealthAIPositionStageRNGModified=False,actualEndingsAccepted=False,
        fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
        nextAction='Promote no build yet: finish repeat-match palette ownership/reference reuse and fresh affected special/morph/selection/ladder/portrait/blink/player-number/clear/shaded-name/ordinary-combat/CPU/KO/overlap/audio regressions for isolated v2753 before changing launcher or release. Reconstruct complete source PCM for its actual randomized Sonya cluck variants and capture matched samples-off controls. Future fresh builders must preserve exact canonical backups instead of depending on cleaned-up diagnostic_v1411 header path. Keep true IDs and CPU frame/null-sentinel protections intact. All original stage/victim/mirror/arena/move-phase/grounding/shadow/other-finisher/secret/cinematic/natural full boss match/own ending/final combined integration/dependency-aware cleanup/refreshed-release requirements remain exactly as requested.',
        inputHashes=pins)
    return prior

if __name__=='__main__':
    need(not OUT.exists(),'Immutable full original-scope candidate checkpoint')
    report=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(goalStatus=report['goalStatus'],actualFilePins=len(report['inputHashes']),
        publicCandidate=report['currentCandidate'],candidateUnderTest=report['candidateUnderTest'],
        nativePaletteOwnershipAndReferenceCleanupBothSlotsAccepted=True,actualCompleteScanouts=6400,
        completeSceneRasterShadowAudioAccepted=False,fullPortAcceptance=False,finishedRelease=False,
        originalRemainingGateGroups=len(report['remaining']),publicLauncherChanged=False,actualNaturalShaoMatchClears=0),indent=2),flush=True)
