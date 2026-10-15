"""Record exact completed audio scope and the same still-live campaign handle."""
import datetime
import gzip
import json
from pathlib import Path
import native_ai_response_context as current
import native_process_census_v6647 as native

ROOT, need, sha = current.ROOT, current.need, current.sha


def main():
    out = ROOT/'audit_native_attract_postending_progress'
    need(not out.exists(), 'Fresh immutable progress journal')
    paths = [ROOT/'audit_native_attract_audible_kano_early/native_audible_square_p2.json',
             ROOT/'audit_native_attract_kano_phase483/finite_muted_roll_route.json',
             ROOT/'audit_native_current_regression_progress_storage/report.json']
    square, muted, core = [json.loads(p.read_text()) for p in paths]
    need(square['passed'] and square['finiteAudibleSonyaP2SquareAccepted'] and
         square['comparison']['differentChannelSamples'] == 0 and square['exactSources']['preciseChannelStates'] == 3584,
         'Actual same-native full speaker/source positive completed')
    need(muted['passed'] and muted['finiteMutedRollSuppressionAccepted'] and not muted['audibleKanoAccepted'] and
         muted['physicalSlot'] == 2 and muted['mutedStartupSourceStates'] == 1028, 'Actual finite muted CPU roll, not audible coverage')
    need(core['passed'] and core['currentSelectionCases'] == 4 and core['currentHumanSpecialCycles'] == 32,
         'Earlier original current UI and special scope retained')
    folder = ROOT/'audit_native_postending_kano_p2_sonya_join'
    identity = json.loads((folder/'native_identity.json').read_text())
    actual = next((r for r in native.census() if r['ProcessId'] == identity['ProcessId']), None)
    need(actual == identity and actual['ParentProcessId'] == 174832 and
         actual['ExecutablePath'] == str(ROOT/current.NAME/'mkport_candidate.exe'), 'Same actual live native PID/parent/creation/command')
    need(current.expected(), 'Full reviewed current guest and compilation identity intact')
    before = json.loads((folder/'input_hashes_before.json').read_text())
    need(all(sha(path) == digest for path,digest in before.items()), 'All actually executing frozen campaign inputs intact')
    stages, losses, selected = set(), 0, 0
    latest = None
    try:
        with gzip.open(folder/'run.log.gz', 'rt', encoding='utf-8') as stream:
            for line in stream:
                if line.startswith('MK2_NAT_CAMPAIGN_STAGE '):
                    stages.add(int(line.split(' stage=')[1].split()[0]))
                if line.startswith('MK2_NAT_CAMPAIGN_LOSS '): losses += 1
                if line.startswith('MK2_NAT_CAMPAIGN_SELECT_ID '): selected += 1
                if line.startswith('MK2_NAT_CAMPAIGN_LIVE '): latest = line.strip()
    except EOFError:
        pass  # The confirmed live writer has not yet emitted its gzip trailer.
    need(stages == {0,1} and losses and selected and latest, 'Actual current campaign progress and physical continues observed')
    launcher = ROOT/'PLAY_MK2_KANO_SONYA.cmd'
    need(sha(launcher) == '90BD99EC729C956A1414D9A544DBA537597A828AE382D323579DF266FB053ACE', 'Public launcher deliberately unchanged')
    result = dict(passed=True, goalStatus='active', fullPortAcceptance=False, fullGoalComplete=False,
                  observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  previousGoalTurnClassification='no progress: status only; same retained RAM host revalidated before work',
                  thisGoalTurnClassification='progress: current true Sonya P2 full audible Square/source EOF qualified, different muted Kano CPU route retained, genuine current earned-campaign/post-ending-join test dispatched and live handle verified',
                  completedSonyaP2Audio=dict(comparedStereoFrames=245760, preciseChannelStates=3584, effectiveFaults=10,
                                            activeCallbacks=47, eofTailCallbacks=209, observedOwnerHP=158),
                  completedMutedKanoP2=dict(sourceStates=1028, audibleAccepted=False, mixedPCMQualified=False),
                  originalRequirements=core['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=core['originalRemainingWorkGroups'],
                  acceptedPriorWorkNotReset=core['acceptedPriorWorkNotReset'],
                  verifiedLiveWait=dict(sessionId=63607, nativeIdentity=actual, observedStages=sorted(stages),
                                        paidContinueLosses=losses, latestNativeOwnedField=latest,
                                        endingReached=False, postEndingJoinAccepted=False,
                                        limitation='Current ordinary zoning controller is repeatedly losing to Subzero8 on stage1. Never count observation time or process liveness as a completed ending/join.'),
                  nextAction='Re-poll the same session63607 and actual native141900; do not restart because observation expires. Qualify the real terminal result and images if the ending/join is reached; otherwise retain the actual bounded failure before changing a physical controller. Audible native Kano demo and remaining integration/final combined CMD/ZIP scope stay open.',
                  newBuilds=0, newROMCopies=0, newZIPs=0, publicBuildPromoted=False,
                  compilerCacheAbsent=not (ROOT/'mame-mkp/build/mingw-gcc').exists(),
                  inputHashes={str(p):sha(p) for p in [*paths, Path(__file__).resolve(), launcher,
                                                      folder/'native_identity.json',folder/'input_hashes_before.json']})
    out.mkdir()
    (out/'report.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(passed=True, audibleSonyaP2Accepted=True, audibleKanoAccepted=False,
                         nativeLive=actual['ProcessId'], campaignStages=sorted(stages), postEndingJoinAccepted=False)), flush=True)


if __name__ == '__main__': main()
