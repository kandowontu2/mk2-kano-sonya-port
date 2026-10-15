"""Actual Sonya CPU finish and current demo audio/rendering; full scope stays active."""
import json,subprocess
from pathlib import Path
import native_cpu_finisher_spacing_context as native
import native_process_census_v6647 as census
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=native.ROOT,native.need,native.sha

if __name__=='__main__':
    out=ROOT/'audit_native_sonya_finisher_current_attract_progress'
    need(not out.exists() and not census.census(),'Both actual original native jobs and RAM hosts terminal, fresh immutable journal')
    sonya_path=ROOT/'audit_native_sonya_cpu_finisher_checked/report.json'
    audio_path=ROOT/'audit_native_attract_kano_spacing_phase484/current_native_audio_source_eof_checked.json'
    sonya=json.loads(sonya_path.read_text());audio=json.loads(audio_path.read_text())
    need(sonya['passed'] and sonya['actualVisualReview']['wholeNativeFramesDisplayed']==10 and
         audio['passed'] and audio['comparedStereoFrames']==778560 and audio['differentChannelSamples']==0 and
         audio['preciseSourceChannels']['preciseChannelStates']==11354 and
         audio['preciseSourceChannels']['realReplacementBetweenSpeakerCallbacks'] and
         len(audio['actualCounterexamplesRejected'])==7 and
         all(sha(p)==h for report in (sonya,audio) for p,h in report['inputHashes'].items()),
         'Every actually accepted current source/input/native RGB/audio/state dependency conserved')
    previous_path=ROOT/'audit_native_ai_response_attract/native_ai_attract_runtime.json'
    previous=json.loads(previous_path.read_text())
    need(previous['passed'] and previous['nativeOwnBiographyPhotosAccepted'],
         'Prior whole native photo raster proof, not merely authored art intentions')
    conserved=[]
    for photo in previous['exactOwnPhotoFrames']:
        current=next(r for r in audio['actualRGBHeaders'] if r['stage']==photo['header']['stage'])
        need(current['sha256']==photo['header']['sha256'] and current['bytes']=='406400' and
             photo['matchedPixels']==21804 and photo['position']==[29,22],
             'Entire current own biography frame identical to independently decoded original-photo native raster')
        conserved.append(dict(identity=photo['identity'],currentNativeHeader=current,
            originalNativeHeader=photo['header'],wholeCurrentRasterIdentical=True,
            inheritedIndependentlyMatchedOriginalPhotoPixels=photo['matchedPixels']))
    scope=json.loads((ROOT/'audit_native_guard_campaign_progress/report.json').read_text())
    run=audio_path.parent;files=[p for p in run.iterdir() if p.is_file()]
    before={str(p):sha(p) for p in files}
    for p in files:
        need(p.resolve().is_relative_to(ROOT) and not p.is_symlink(),'Exact local compression target')
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
    need(all(sha(p)==h for p,h in before.items()),'All original failed/accepted source/evidence bytes preserved after compression')
    public=ROOT/'PLAY_MK2_KANO_SONYA.cmd'
    need(sha(public)=='90BD99EC729C956A1414D9A544DBA537597A828AE382D323579DF266FB053ACE' and
         not (ROOT/'mame-mkp/build/mingw-gcc').exists(),'Public launch path unchanged and generated compiler cache absent')
    report=dict(passed=True,goalStatus='active',fullPortAcceptance=False,fullGoalComplete=False,
        previousGoalTurnClassification='progress: specific original Sonya job terminal0 confirmed with complete initialized guest; visual and independent lifecycle review became eligible.',
        thisGoalTurnClassification='progress: genuine CPU Sonya18 finisher versus human Kano17 is fully observed/reviewed/qualified; fresh same-candidate native demo run and all811 actual PCM/DAC callbacks qualified; all25 native rasters reviewed, original whole own-bio frames conserved. Three observer/checker failures preserved and repaired without game changes or native replay.',
        originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],acceptedPriorWorkNotReset=scope['acceptedPriorWorkNotReset'],
        candidate=native.NAME,executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,
        actualSonyaCPUFinisher=dict(entryGap=127,physicalSlot=1,humanKanoSlot=2,nativePerformerVariant=2,
            continuousFinisherFields=231,continuousActorFieldsUntilTeardown=538,
            independentOrbFields=60,sourceNativeVictimContextFields=116,
            earnedWinningRoundContactHealthStores=14,paidContinues=10,actualVisualFramesReviewed=10,
            actualStateFaultsRejected=22,accepted=True,fullAudioAccepted=False),
        actualCurrentNativeAttract=dict(nativeTerminal=audio['actualNativeTerminal'],
            actualNativeFramesReviewed=25,allWholeFramesActuallyDisplayed=True,
            finiteAudibleSonyaSquareBicycleAndBothNamesAccepted=True,
            exactStereoFrames=778560,exactSourceChannelStates=11354,actualSourceFaultsRejected=7,
            sourceNativeSquareReplacementBetweenCallbacks=True,bothBicycleEOFsAccepted=True,
            wholeCurrentOwnBiographyRasterConservation=conserved,
            audibleKanoDemoLaunchAccepted=False,
            limitation='This finite13-minute ordinary cold boot had genuine Kano P1 and Sonya P1/P2 demos but no native Kano roll cue; cannot count this as audible Kano coverage or full14-biography current runtime.',
            visualObservations=['All25 displayed native fields retain the normal biography frame/name/text layout and clean CPU demo transitions.',
                'Both own biography whole frames are byte-identical to the prior independently original-ROM-decoded native photos; no new palette/color rendering change.',
                'The inspected native demo scenes show genuine Kano/Sonya names and their own animated bodies, with no selector portraits or preview poses.']),
        allFailedExecutedCheckerAndWrapperSourcesRetained=True,newGameRunsForCheckerRepair=0,
        newBuilds=0,newGuestROMCopies=0,newRawMediaFiles=0,newZIPs=0,gameSourceChanged=False,
        compilerCacheAbsent=True,publicPlayableChanged=False,
        completeAllVictimsArenasFinishersOrCampaignsAccepted=False,
        evidenceStorage=dict(files=len(files),logicalBytes=sum(p.stat().st_size for p in files),
            allocatedBytes=sum(allocated(p) for p in files),allBytesConserved=True,
            completeActualPCMAndDACStoredCompressedOnly=True),
        inputHashes={str(p.resolve()):sha(p) for p in (Path(__file__),sonya_path,audio_path,previous_path,
            ROOT/'audit_native_sonya_cpu_finisher_progress/report.json',
            ROOT/'tools/review_native_current_attract_ram.py',public)},
        nextAction='Use the remaining-scope audit and unchanged-source conservation to prioritize real unclosed native behavior: audible CPU Kano demo cue, remaining arena/stock-victim sound priority and secret/post-ending joins; then combined current visual/audio/gameplay acceptance and matching runnable CMD/finished ZIP. Do not rerun accepted unchanged cases just to relabel them or count this finite test as full port completion.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(out/'report.json')],check=True,capture_output=True)
    print(json.dumps(dict(progress=True,SonyaCPUFinisherAccepted=True,actualWholeNativeFramesReviewed=35,
        currentStereoFramesBitExact=778560,preciseChannelStates=11354,
        currentEvidenceAllocatedBytes=report['evidenceStorage']['allocatedBytes'],newBuilds=0,
        audibleKanoDemoLaunchStillOpen=True,publicUnchanged=True,fullGoalComplete=False)))
