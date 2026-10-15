"""Close the real Kano spacing defect, retain full natural-character scope."""
import json,subprocess
from pathlib import Path
import native_cpu_finisher_spacing_context as native
import native_process_census_v6647 as census
ROOT,need,sha=native.ROOT,native.need,native.sha
if __name__=='__main__':
    out=ROOT/'audit_native_cpu_finisher_spacing_accepted_progress'
    need(not out.exists(),'Fresh immutable completed finite correction receipt')
    native.expected()
    scope=json.loads((ROOT/'audit_native_guard_campaign_progress/report.json').read_text())
    qualified=ROOT/'audit_native_cpu_finisher_spacing_child_checked/report.json'
    accepted=json.loads(qualified.read_text())
    need(accepted['passed'] and accepted['ownedEntryGap']==79 and
         accepted['continuousFinisherGeometryFields']==231 and accepted['borrowedSkeletonContextFields']==48 and
         accepted['independentChildObjectLinkObserved'] and
         all(sha(p)==h for p,h in accepted['inputHashes'].items()),
         'Complete actual owned native gap/ground/child/teardown correction evidence unchanged')
    runs=[ROOT/'audit_native_cpu_finisher_spacing',ROOT/'audit_native_cpu_finisher_spacing_child']
    meta=[json.loads((r/'result.json').read_text()) for r in runs]
    terminals=[json.loads((r/'native_terminal.json').read_text()) for r in runs]
    need(all(r['nativeExit']==0 and not r['nativeCacheOverrunObserved'] for r in meta) and
         all(r['nativeExit']==0 for r in terminals) and not census.census(),
         'Both actual independent game runs terminal0; both RAM review hosts exited normally')
    need(meta[0]['actualScenes']==meta[1]['actualScenes'] and
         meta[0]['nativeRGBStreamSHA256']==meta[1]['nativeRGBStreamSHA256'],
         'All47 actual native RGB callbacks identical across independent observer replay')
    reviewed=[r for r in accepted['actualNativeRGBScenes']]
    need(len(reviewed)==6 and {r['filename'] for r in reviewed}==
         {f'postjoin_finisher_regression_age{n}.png' for n in (1,30,90,180,330,900)},
         'Six distinct full native frames actually displayed and visually reviewed from both RAM hosts')
    public=ROOT/'PLAY_MK2_KANO_SONYA.cmd'
    need(sha(public)=='90BD99EC729C956A1414D9A544DBA537597A828AE382D323579DF266FB053ACE',
         'Public launcher not prematurely promoted')
    folders=[*runs,ROOT/'audit_native_cpu_finisher_spacing_child_checked',
        ROOT/'audit_native_cpu_finisher_saved_context_checker_failure',
        ROOT/'audit_native_cpu_finisher_spacing_source',ROOT/'source_native_cpu_finisher_spacing']
    files=[p for folder in folders for p in folder.rglob('*') if p.is_file()]
    before={str(p):sha(p) for p in files}
    for p in files:
        need(p.resolve().is_relative_to(ROOT) and not p.is_symlink(),'Only exact local evidence/source compression targets')
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
    need(all(sha(p)==h for p,h in before.items()),'Compression conserved every selected source/evidence byte')
    need(not (ROOT/'mame-mkp/build/mingw-gcc').exists(),'Actual completed compiler cache absent')
    paths=[Path(__file__),qualified,public,ROOT/native.NAME/'build-info.json',
        ROOT/native.NAME/'restoration.json',ROOT/native.NAME/'cache_retirement.json',
        ROOT/'audit_native_cpu_finisher_spacing_progress/report.json',
        ROOT/'audit_native_cpu_finisher_saved_context_checker_failure/report.json']
    report=dict(passed=True,goalStatus='active',fullGoalComplete=False,fullPortAcceptance=False,
        previousGoalTurnClassification='progress: finite corruption repair reviewed; dedicated CPU distance rows source-qualified and actual compiler started.',
        thisGoalTurnClassification='progress: compiled spacing-only private candidate and entire initialized game verified; two actual cold native terminal0 replays, own Kano79pixel entry/231 consecutive grounded actor fields/48 independently linked skeleton context fields/clean native winner-loss-paid-continue. All47 native raster callbacks reproduced, six distinct full frames visually reviewed.',
        originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],acceptedPriorWorkNotReset=scope['acceptedPriorWorkNotReset'],
        candidate=native.NAME,executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,
        actualNativeTerminals=terminals,actualEntryGapBefore=111,actualEntryGapNow=79,
        actualCompleteNativeFinisherFields=231,actualIndependentlyLinkedChildFields=48,
        actualNativeRuntimeFaultsRejected=len(accepted['actualFaultsRejected']),
        sourceOnlySonyaDistanceProfiles=dict(first=128,second=128,runtimeAccepted=False),
        visualReview=dict(actualNativeFrames=reviewed,actualWholeFramesDisplayed=True,
            finiteKanoAgainstSonyaExtractionReachAccepted=True,
            observations=['At ages30/90 Kano reaches Sonya instead of grabbing across the prior wide gap.',
                'Own Sonya victim poses, extracted skeleton phases, Kano winner name and normal native floor anchoring are intact.',
                'No selection portraits or preview pose persists into the inspected finisher/winner frames.',
                'Age900 shows a genuine new paid-continue selection screen, not a character-ID fallback.'],
            completeAllVictimsArenasFinishersRasterAccepted=False),
        audioAcceptance=False,otherPhysicalSlotAndSecondPerformerRuntimeAccepted=False,
        SonyaCPURuntimeAccepted=False,noNewSecondFinisherChoreographyClaim=True,
        allKnownTestProcessesAndRAMHostsTerminal=True,compilerCacheRetired=True,
        sourceEvidenceCompressedFiles=len(files),allCompressedBytesConserved=True,
        newBuildsThisCorrection=1,newGuestROMCopies=0,newRawMediaFiles=0,newZIPs=0,
        retainedRootCandidateExecutables=len(list(ROOT.glob('*/mkport_candidate.exe'))),
        payloadAndSampleHardlinksPreserved=True,publicBuildPromoted=False,
        inputHashes={str(p.resolve()):sha(p) for p in paths},
        nextAction='Use the same verified candidate for genuine CPU Sonya finisher/distance and alternate performer/physical-slot contexts through normal physical selection/ladder RNG, with no memory/HP/RNG/AI writes. Consolidate exact unchanged-source conservation with prior full scope, close real remaining audio/arena/secret/post-ending gaps, then final combined native UI/gameplay/audio acceptance and matching CMD/release ZIP. Do not redo unchanged already accepted cases merely to relabel them.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(out/'report.json')],check=True,capture_output=True)
    print(json.dumps(dict(progress=True,actualNativeRuns=2,bothNativeExit0=True,
        correctedKanoReach=79,continuousNativeFinisherFields=231,independentChildContextFields=48,
        actualFaultsRejected=len(accepted['actualFaultsRejected']),actualViewedNativeFrames=6,
        compilerCacheRemoved=True,publicUnchanged=True,SonyaCPURuntimePending=True,fullGoalComplete=False)))
