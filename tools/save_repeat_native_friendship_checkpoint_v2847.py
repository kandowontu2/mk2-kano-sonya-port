"""Retain the entire native-character goal after repeated palette lifetime proof.
No playable bytes, public launcher, release ZIP or user source changes. The full
historical proof graph remains retained, not revalidated in full this turn.
"""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT=assembly.ROOT
PREVIOUS=ROOT/'audit_v2818_native_blade_blood_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2848_repeat_native_friendship_full_scope_checkpoint'

def save():
    prior=json.loads(PREVIOUS.read_text());inherited=dict(prior['inputHashes']);fresh={}
    assembly.need(prior['goalStatus']=='active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and
        len(prior['remaining'])==5 and len(prior['currentSourceBoundBossCampaigns'])==70 and
        prior['currentRealShaoKahnMatchClears']==0 and not prior['actualEndingsAccepted'] and
        prior['candidateUnderTestAll52CaseEndpointScenesAccepted'] and prior['candidateUnderTestBothChangedBladeRecoveryScenesSourceAccepted'],
        'Retain entire unfinished goal, actual prior evidence and missing full boss clears/endings')
    def pin(path,wanted=None):
        path=Path(path);key=str((path if path.is_absolute() else ROOT/path).absolute())
        if wanted is None:wanted=assembly.sha(key)
        assembly.need(key not in fresh or fresh[key]==wanted,'Consistent fresh evidence '+key)
        assembly.need(key not in inherited or inherited[key]==wanted,'Immutable historical evidence '+key)
        fresh[key]=wanted
    def proof(leaf):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        assembly.need(value['passed'] and not value.get('fullPortAcceptance',False),'Actual bounded terminal proof '+leaf)
        for file,wanted in value['inputHashes'].items():pin(file,wanted)
        return value,str(path)
    cases={}
    for side in (1,2):
        value,path=proof(f'audit_v2842_repeat_native_friendship_p{side}_checked')
        assembly.need(value['candidate']==assembly.NAME and value['side']==side and value['repeatedNativePaletteLifecycleAccepted'] and
            value['wholeActualGuestAndPayloadReconstructed'] and value['noEmulatorResetOrStateInjection'] and
            len(value['matches'])==3 and value['totalEarnedRoundWins']==6 and value['totalEarnedDamage']==966,
            'Three continuous earned two-human matches and actual native Friendships per slot')
        assembly.need([r['paletteIndex'] for r in value['matches']]==[4,6,5] and
            all(r['construction']<r['taskReturn']<r['nativePaletteRelease']<=r['spriteReuse'] and
                r['earnedDamage']==322 and r['earnedRoundWins']==2 for r in value['matches']),
            'All actual palette allocations, task returns, native release and sprite reuse')
        cases[f'p{side}']=dict(report=path,consecutiveNativeFields=value['consecutiveNativeFields'],
            completePaletteSnapshots=value['completePaletteSnapshots'],nativePaletteStores=value['nativePaletteStores'],
            referenceIncrements=value['referenceIncrements'],referenceReleases=value['referenceReleases'],matches=value['matches'])
    units,units_path=proof('audit_v2846_repeat_native_friendship_units')
    assembly.need(units['candidate']==assembly.NAME and units['actualOriginalCounterexamplesRejected']==80 and
        units['actualCaptureFilesUnmodified'],'All actual repeated-match corruptions rejected without modifying captures')
    failures=[]
    for version in (2828,2830,2832,2837):
        for side in (1,2):
            path=ROOT/f'audit_v{version}_repeat_native_friendship_p{side}_checked/report.json'
            value=json.loads(path.read_text());assembly.need(not value['passed'] and value['error'],'Preserved actual observer/verifier failure')
            pin(path);failures.append(dict(report=str(path),error=value['error'],accepted=False))
    unit_fail=ROOT/'audit_v2844_repeat_native_friendship_units/report.json'
    value=json.loads(unit_fail.read_text());assembly.need(not value['passed'] and 'Specific corruption rejected' in value['error'],
        'Earlier expected-error-label diagnostic retained, not gameplay evidence')
    pin(unit_fail);failures.append(dict(report=str(unit_fail),error=value['error'],accepted=False))
    for version in (2819,2824,2833,2838):pin(ROOT/f'mk2ks_repeat_native_friendship_v{version}.lua')
    for file in ('run_repeat_native_friendship_v2820.ps1','run_repeat_native_friendship_v2822.ps1',
        'run_repeat_native_friendship_v2825.ps1','run_repeat_native_friendship_v2834.ps1','run_repeat_native_friendship_v2839.ps1',
        'verify_repeat_native_friendship_v2827.py','verify_repeat_native_friendship_v2829.py',
        'verify_repeat_native_friendship_v2831.py','verify_repeat_native_friendship_v2836.py','verify_repeat_native_friendship_v2841.py',
        'test_repeat_native_friendship_v2843.py','test_repeat_native_friendship_v2845.py'):pin(ROOT/'tools'/file)
    # Retain every actual earlier natural capture, including incomplete observer
    # variants, without promoting those variants as continuous lifecycle proofs.
    for version in (2823,2826,2835):
        for side in (1,2):
            folder=ROOT/f'audit_v{version}_repeat_native_friendship_p{side}'
            result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
            assembly.need(result['exit_code']==0 and result['emulator_resets']==0 and result['guest_writes']==0,
                'Preserved actual earlier terminal physical capture')
            for file in folder.rglob('*'):
                if file.is_file():pin(file)
    pin(PREVIOUS);pin(__file__)
    for path,wanted in {
        'PLAY_MK2_KANO_SONYA.cmd':'631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7',
        'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
        'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
        'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
        'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
        'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644',
        'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    }.items():pin(ROOT/path,wanted)
    print('Revalidating fresh relevant repeated-match proof files:',len(fresh),flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for (file,wanted),actual in zip(fresh.items(),pool.map(assembly.sha,fresh)):
            assembly.need(actual==wanted,'Changed actual fresh proof dependency '+file)
    inherited.update(fresh)
    prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=prior['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: runner automatic-variable collision corrected in fresh source; both slots completed three earned continuous two-human matches and native Kano Friendships with coin/start/reselection only. Fresh read-only stable-field observer covers actual original boot and reset free-pool terminators and old contexts continuously across later activations. Complete 60-cell native palette table replay from boot, all true participant identities, native damage/eligibility/input/action/constructor/task return/reference release/reuse-delay clock/sprite reclaim/reuse independently accepted for all six allocations; 80 specific actual corruptions rejected. Nine earlier diagnostic failures and all earlier terminal captures retained. No playable bytes, public launcher or ZIP changed. Full natural-character scope remains unfinished.',
        candidateUnderTestRepeatedNativeFriendshipAccepted=True,candidateUnderTestRepeatedNativeFriendshipCases=cases,
        candidateUnderTestRepeatedNativeFriendshipNativeFields=sum(r['consecutiveNativeFields'] for r in cases.values()),
        candidateUnderTestRepeatedNativeFriendshipPaletteStores=sum(r['nativePaletteStores'] for r in cases.values()),
        candidateUnderTestRepeatedNativeFriendshipAllocations=6,candidateUnderTestRepeatedNativeFriendshipEarnedRoundWins=12,
        candidateUnderTestRepeatedNativeFriendshipUnitsReport=units_path,candidateUnderTestRepeatedNativeFriendshipSpecificCounterexamples=80,
        preservedRepeatedNativeFriendshipDiagnosticFailures=failures,
        preservedRepeatRunnerFailure='v2820 attempts exited 1 before emulator launch: PowerShell automatic $Matches regex hashtable collided with integer parameter; v2822 and successors use task-specific $MatchCount. Failed source immutable.',
        repeatedNativeFriendshipProofScope='Three continuous earned two-human matches per Kano player slot against true Sonya. Six independent bubble palette allocations, exact release/task/sprite reclamation and reuse; no emulator resets or guest-state injection. Not full rendered Friendship phases/audio, Sonya repeated finisher effects, every victim/arena, or all other auxiliary effects.',
        candidatePromotionGates=[
            'Broader affected move/morph/ordinary-combat/CPU/KO/overlap regressions after shared allocator/reset routing change (fresh native UI, 52 human states, blade blood and repeated native Kano bubble lifetime accepted)',
            'Fresh full original Friendship audible PCM/tail/overlap checks, including actual randomized Sonya variants'],
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
        gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False,oldBuildFoldersDeletedThisTurn=0,
        nativeDifficultyHealthAIPositionStageRNGModified=False,actualEndingsAccepted=False,
        fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
        nextAction='Keep v2753 isolated. Repeated natural Kano bubble palette ownership/release/task/sprite reclaim/reuse in both slots now accepted. Next fresh affected ordinary-combat/morph/CPU/KO/overlap regressions and full original Friendship audible PCM/tail/overlap including matched samples-off controls for actual randomized Sonya variants. Only promote the launcher after remaining candidate gates pass. All five original remaining groups retain arena/victim/mirror/stage effect/audio/move-phase/grounding/floor shadow/other finisher/morph/secret/cinematic/natural Kintaro/Shao match-clear/own-ending/attract/final integration/obsolete dependency cleanup/refreshed release scope.',
        inputHashes=inherited)
    return prior

if __name__=='__main__':
    assembly.need(not OUT.exists(),'Immutable full-scope successor')
    value=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps(dict(goalStatus=value['goalStatus'],publicCandidate=value['currentCandidate'],
        candidateUnderTest=value['candidateUnderTest'],repeatedNativePaletteLifetimeBothSlotsAccepted=True,
        continuousNativeFields=value['candidateUnderTestRepeatedNativeFriendshipNativeFields'],
        actualAllocations=6,earnedRoundWins=12,remainingCandidateGates=len(value['candidatePromotionGates']),
        fullPortAcceptance=False,finishedRelease=False,revalidatedFreshRelevantFilePins=value['revalidatedFreshRelevantFilePins']),indent=2),flush=True)
