"""Preserve full original goal after fresh candidate Friendship audio gate.

Public build, launcher and ZIP remain unchanged. Only bounded latest-candidate
human Friendship audio is newly accepted. Keep all remaining arena, move,
CPU/morph/overlap, finisher, natural boss/ending and final integration work.
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT=assembly.ROOT
PREVIOUS=ROOT/'audit_v2916_blade_allocation_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2924_friendship_audio_full_scope_checkpoint'

def save():
    prior=json.loads(PREVIOUS.read_text())
    assembly.need(prior['goalStatus']=='active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and
                  len(prior['remaining'])==5 and len(prior['currentSourceBoundBossCampaigns'])==70 and
                  prior['currentRealShaoKahnMatchClears']==0 and not prior['actualEndingsAccepted'] and
                  prior['candidateUnderTest']==assembly.NAME and len(prior['candidatePromotionGates'])==2 and
                  prior['candidateUnderTestBladeAllocationAddressProvenanceAccepted'] and
                  not prior['candidateUnderTestAllCPUAccepted'], 'Full original unfinished natural-character scope')
    inherited=dict(prior['inputHashes']);fresh={}
    def pin(path,wanted=None):
        path=Path(path);key=str((path if path.is_absolute() else ROOT/path).resolve())
        actual=assembly.sha(key) if wanted is None else wanted
        assembly.need(key not in fresh or fresh[key]==actual,'Consistent fresh evidence '+key)
        assembly.need(key not in inherited or inherited[key]==actual,'Preserve earlier immutable evidence '+key)
        fresh[key]=actual
    path=ROOT/'audit_v2922_candidate_friendship_audio_checked/report.json'
    proof=json.loads(path.read_text());pin(path)
    assembly.need(proof['passed'] and proof['candidate']==assembly.NAME and proof['actualPhysicalCaptures']==16 and
                  proof['audibleCues']==80 and proof['audibleGroups']==28 and proof['actualAudioCounterexamplesRejected']==56 and
                  proof['originalPCMAndAudibleOverlapAccepted'] and proof['all20OriginalCluckChannelsReconstructed'] and
                  proof['currentWholeGuestAndPayloadReconstructed'] and proof['samplesSettingNeverChangedGameplay'] and
                  proof['originalPhysicalStrategyUnchanged'] and not proof['gameChanged'] and
                  not proof['completeSceneRasterShadowAudioAccepted'] and not proof['allCPUOrMorphsAccepted'] and
                  not proof['fullFinisherAcceptance'] and not proof['fullPortAcceptance'], 'Actual bounded complete original PCM gate')
    for file,wanted in proof['inputHashes'].items():pin(file,wanted)
    cases={}
    for key,value in proof['cases'].items():
        assembly.need(value['finalUnmodifiedControlPassed'] and value['nativeScene']['observedOriginalOwnWinnerDispatches']==2 and
                      value['nativeScene']['actualTrueFighterID']==(17 if key.startswith('kano') else 18) and
                      len(value['baselineCorruptions'])==3 and len(value['cueCorruptions'])==2 and
                      len(value['PCMCorruptions'])==(6 if key.startswith('kano') else 8) and
                      all(.9995<g['correlation']<=1 and g['residual_rms_pcm']<2 and
                          all(abs(offset)<=4 for offset in g['offset_pcm_samples']) and
                          all(.98<gain<1.02 for gain in g['gains'])for g in value['audibleGroups']),
                      'Actual full waveforms, <=4 PCM timing and unchanged strict gain/tail/overlap contracts')
        cases[key]=dict(cues=value['cues'],audibleGroups=len(value['audibleGroups']),
                       nativeSceneRecords=value['wholeNativeRecords'],nativeScene=value['nativeScene'],
                       actualVariants=value['variants'],
                       minimumCorrelation=min(g['correlation']for g in value['audibleGroups']),
                       maximumResidualPCM=max(g['residual_rms_pcm']for g in value['audibleGroups']),
                       PCMCorruptions=value['PCMCorruptions'],cueCorruptions=value['cueCorruptions'],
                       baselineCorruptions=value['baselineCorruptions'],finalUnmodifiedControlPassed=True)
    assembly.need(set(cases)=={'kano_p1','kano_p2','sonya_p1','sonya_p2'} and len(proof['physicalRestrictions'])==8 and
                  all(v['cues']==0 and v['finalUnmodifiedControlPassed'] and len(v['audioCorruptions'])==1
                      for v in proof['physicalRestrictions'].values()), 'Both fighters/slots positive and physical negative captures')
    pin(PREVIOUS);pin(__file__)
    for file,wanted in {
        'PLAY_MK2_KANO_SONYA.cmd':'631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7',
        'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
        'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
        'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
        'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
        'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644',
        'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    }.items():pin(ROOT/file,wanted)
    print('Revalidating fresh relevant audio files:',len(fresh),flush=True)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,wanted),actual in zip(fresh.items(),pool.map(assembly.sha,fresh)):
            assembly.need(actual==wanted,'Changed actual proof dependency '+file)
    inherited.update(fresh)
    prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=prior['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: sixteen fresh cold physical candidate2753 Friendship captures across both fighters/slots, samples-on/off controls and wrong-command/punch-used restrictions completed. Every whole guest/payload independently reconstructed and every native scene record matched between sound settings. All 80 original cues and 28 audible groups passed unchanged <=4 PCM sample timing, .98..1.02 gain, >.9995 correlation and <2 PCM residual gates, with complete original DCS waveform/tails, actual randomized Sonya variants and independent voice overlap. All twenty original cluck channel references reconstructed. Fifty-six actual PCM/cue/baseline/unwanted-audio corruptions rejected. Fresh Friendship audio candidate gate closed, broader CPU/morph/KO/overlap still open. No public playable bytes, CMD or ZIP changed; full original goal remains active.',
        candidateUnderTestFriendshipOriginalPCMAndAudibleOverlapAccepted=True,
        candidateUnderTestFriendshipAudioReport=str(path),candidateUnderTestFriendshipAudioCases=cases,
        candidateUnderTestFriendshipPhysicalAudioRestrictions=proof['physicalRestrictions'],
        candidateUnderTestFriendshipAudioPhysicalCaptures=16,candidateUnderTestFriendshipAudibleCues=80,
        candidateUnderTestFriendshipAudibleGroups=28,candidateUnderTestFriendshipAudioCounterexamplesRejected=56,
        candidateUnderTestFriendshipSamplesNeverChangedNativeGameplay=True,
        candidatePromotionGates=[prior['candidatePromotionGates'][0]],
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
        gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False,oldBuildFoldersDeletedThisTurn=0,
        nativeDifficultyHealthAIPositionStageRNGModified=False,actualEndingsAccepted=False,
        fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
        nextAction='Keep candidate2753 isolated; fresh full captured human Friendship original PCM/tail/overlap and physical audio restrictions are accepted in both slots. Next close broader affected CPU signature-after-pair/subsequent-pair/KO/mirror/morph/ordinary combat/overlapping-effect regressions after shared palette/reset routing changes. Preserve all five remaining original groups: arena/victim/mirror/stage effects/audio/full move phases/grounding/floor shadows/other finishers/morphs/secrets/cinematics/naturally earned full Kintaro and Shao matches/own endings/attract/final integration/obsolete dependency cleanup/refreshed release ZIP. No public promotion or finished release before required gates pass.',
        inputHashes=inherited)
    return prior

if __name__=='__main__':
    assembly.need(not OUT.exists(),'Immutable full-scope Friendship audio checkpoint')
    report=save();OUT.mkdir();path=OUT/'checkpoint.json'
    path.write_text(json.dumps(report,indent=2)+'\n')
    compressed=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    assembly.need(compressed.returncode==0,'Lossless compression of new checkpoint')
    print(json.dumps(dict(goalStatus=report['goalStatus'],candidateUnderTest=report['candidateUnderTest'],
        actualAudioCaptures=16,audibleCues=80,audibleGroups=28,rejectedActualCounterexamples=56,
        remainingCandidateGates=len(report['candidatePromotionGates']),originalRemainingScopeGroups=len(report['remaining']),
        publicLauncherChanged=False,fullPortAcceptance=False,finishedRelease=False,
        revalidatedFreshRelevantFilePins=report['revalidatedFreshRelevantFilePins']),indent=2),flush=True)
