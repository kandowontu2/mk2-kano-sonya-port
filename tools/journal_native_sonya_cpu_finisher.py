"""Record actual Sonya CPU completion without shrinking the full port scope."""
import json,subprocess
from pathlib import Path
import native_cpu_finisher_spacing_context as native
import native_process_census_v6647 as census
ROOT,need,sha=native.ROOT,native.need,native.sha

if __name__=='__main__':
    out=ROOT/'audit_native_sonya_cpu_finisher_progress'
    need(not out.exists(),'Fresh immutable full-scope progress receipt')
    qualified=ROOT/'audit_native_sonya_cpu_finisher_checked/report.json'
    accepted=json.loads(qualified.read_text())
    need(accepted['passed'] and accepted['ownedEntryGap']==127 and
         accepted['continuousFinisherFields']==231 and accepted['nativeVictimAnimationContextFields']==116 and
         accepted['independentlyLinkedOrbFields']==60 and
         accepted['actualVisualReview']['wholeNativeFramesDisplayed']==10 and
         all(sha(p)==h for p,h in accepted['inputHashes'].items()),
         'Complete actual Sonya lifecycle, all whole reviewed native frames and unchanged executed inputs')
    terminal=json.loads((ROOT/'audit_native_sonya_cpu_finisher_inventory_checked/native_terminal.json').read_text())
    need(terminal['nativeExit']==0 and not census.census(),'Exact original native child terminal; RAM host exited normally')
    scope=json.loads((ROOT/'audit_native_guard_campaign_progress/report.json').read_text())
    files=[p for folder in ('audit_native_sonya_cpu_finisher','audit_native_sonya_cpu_finisher_inventory_checked',
        'audit_native_sonya_cpu_finisher_checked','audit_native_sonya_cpu_ui_preflight_failure',
        'audit_native_sonya_cpu_inventory_wrapper_preflight_failure') for p in (ROOT/folder).rglob('*') if p.is_file()]
    before={str(p):sha(p) for p in files}
    for p in files:
        need(p.resolve().is_relative_to(ROOT) and not p.is_symlink(),'Exact local byte-conserving compression target')
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
    need(all(sha(p)==h for p,h in before.items()),'Every failed and accepted evidence byte conserved')
    public=ROOT/'PLAY_MK2_KANO_SONYA.cmd'
    need(sha(public)=='90BD99EC729C956A1414D9A544DBA537597A828AE382D323579DF266FB053ACE' and
         not (ROOT/'mame-mkp/build/mingw-gcc').exists(),'Public unpromoted and compiler cache absent')
    report=dict(passed=True,goalStatus='active',fullPortAcceptance=False,fullGoalComplete=False,
        previousGoalTurnClassification='progress: read exact terminal0 Sonya job and recovered complete initialized guest proof; visual/state review became eligible.',
        thisGoalTurnClassification='progress: all ten whole native Sonya kiss/burn/winner/paid-continue frames actually reviewed; complete true-ID lifecycle/health/ground/context/child/teardown qualified against22 actual counterexamples, original28264 trajectory rows and allRGB reproduced exactly.',
        originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],
        acceptedPriorWorkNotReset=scope['acceptedPriorWorkNotReset'],
        candidate=native.NAME,executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,
        actualNativeTerminal=terminal,SonyaCPUPhysicalSlot=1,humanKanoPhysicalSlot=2,
        actualNativePerformerVariant=2,actualSonyaFinisherGap=127,actualFinisherFields=231,
        actualContinuousActorFields=538,actualOrbFields=60,actualVictimContextFields=116,
        actualNativeHealthStoresInWinningRound=14,actualPaidContinues=10,
        actualVisualFramesReviewed=10,actualFaultsRejected=22,
        gameSourceChanged=False,newBuilds=0,newGuestROMCopies=0,newRawMediaFiles=0,newZIPs=0,
        publicPlayableChanged=False,compilerCacheAbsent=True,byteConservingCompressedEvidenceFiles=len(files),
        fullAudioAcceptance=False,otherPhysicalSlotAndFirstPerformerRuntimeAccepted=False,
        noNewSecondFinisherChoreographyClaim=True,
        inputHashes={str(p.resolve()):sha(p) for p in (Path(__file__),qualified,public,
            ROOT/'audit_native_cpu_finisher_spacing_accepted_progress/report.json')},
        nextAction='Close meaningful remaining enabled-demo Kano launch/audio context or remaining arena/post-ending/cinematic integration on the same candidate. Conserve accepted coverage and original14requirements/6groups; final combined native review and matching playable CMD/release still required.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(out/'report.json')],check=True,capture_output=True)
    print(json.dumps(dict(progress=True,SonyaCPUFinisherAccepted=True,actualViewedNativeFrames=10,
        actualFaultsRejected=22,newBuilds=0,publicUnchanged=True,fullGoalComplete=False)))
