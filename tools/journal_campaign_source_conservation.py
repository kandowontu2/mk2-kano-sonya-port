"""Keep exact campaign evidence, failed audit attempts and the full port scope."""
import json
import subprocess
from pathlib import Path

import audit_campaign_source_conservation as audit
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated

ROOT, need, sha = audit.ROOT, audit.need, audit.sha


def main():
    out = ROOT / 'audit_campaign_source_conservation_progress_storage'
    need(not out.exists() and not native.census(), 'Fresh journal; no native game running')
    parentpath = ROOT / 'audit_cross_continue_adaptive_progress_storage/report.json'
    parent = json.loads(parentpath.read_text())
    proofpath = ROOT / 'audit_campaign_source_conservation_v3/report.json'
    proof = json.loads(proofpath.read_text())
    need(parent['passed'] and proof['passed'] and len(proof['cases']) == 4,
         'All four whole original retained campaign gates actually completed')
    pins = {str(parentpath): sha(parentpath), str(proofpath): sha(proofpath)}
    for report in (parent, proof):
        for path, digest in report['inputHashes'].items():
            need(sha(path) == digest and (path not in pins or pins[path] == digest),
                 'Every actual prior/current source/evidence pin intact: ' + path)
            pins[path] = digest
    source = json.loads((ROOT / 'audit_campaign_source_conservation_v3/source_conservation.json').read_text())
    need(source['changedGuestBytes'] == 404 and len(source['unchangedWholeSamples']) == 16 and
         source['unchangedWholePayload'] and source['allOldRollInstructionsReconstructedExactly'],
         'Exact reviewed source boundary, not green-report candidate relabeling')
    cases = []
    for declaration in proof['cases']:
        fighter, side = declaration['fighter'], declaration['side']
        path = ROOT / f'audit_campaign_source_conservation_v3/{fighter}_p{side}_retained_gate.json'
        case = json.loads(path.read_text())
        nativecase = case['nativeCase']
        need(case['wholeOriginalGateExecutedAgain'] and not case['currentNativeBootClaim'] and
             nativecase['passed'] and nativecase['unassisted_clear_proven'] and not nativecase['errors'] and
             nativecase['player'] == fighter and nativecase['human_slot'] == side and
             nativecase['stages_reached'] == list(range(13)) + [14, 15, 16],
             'Actual complete original paid-continue/health/boss/own-ending/attract gate')
        cases.append(dict(fighter=fighter, side=side, originalNativeStages=nativecase['stages_reached'],
                          originalOwnRoundWins=nativecase['native_own_round_wins'],
                          originalPaidContinueLosses=nativecase['paid_continue_losses'],
                          reexecutedFaultCount=case['faultCount'], freshCurrentPlaythroughClaim=False))
    failed = []
    for folder, error in [('audit_campaign_source_conservation', 'All sixteen prior samples'),
                          ('audit_campaign_source_conservation_v2', 'All actual old registered samples')]:
        path = ROOT / folder / 'report.json'
        result = json.loads(path.read_text())
        need(not result['passed'] and error in result['error'] and not result['completedCases'],
             'Both pre-runtime audit lookup/parser failures preserved unchanged')
        failed.append(dict(report=str(path), error=result['error'], nativeGameFailure=False))
    files = {Path(__file__), *(ROOT / 'tools').glob('audit_campaign_source_conservation*.py')}
    for name in ('audit_campaign_source_conservation', 'audit_campaign_source_conservation_v2',
                 'audit_campaign_source_conservation_v3'):
        files.update(p for p in (ROOT / name).rglob('*') if p.is_file())
    storage = []
    total = 0
    seen = set()
    for path in sorted(files):
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink() and
             path.suffix.lower() in ('.py', '.json'), 'Bounded proof/source-only compression target')
        digest = sha(path)
        before = allocated(path)
        subprocess.run(['compact.exe', '/C', '/EXE:LZX', '/F', '/I', '/Q', str(path)],
                       capture_output=True, check=True)
        need(sha(path) == digest, 'Exact lossless source/evidence retention')
        after = allocated(path)
        stat = path.stat()
        key = stat.st_dev, stat.st_ino
        if key not in seen:
            total += after
            seen.add(key)
        pins[str(path.resolve())] = digest
        storage.append(dict(path=str(path.resolve()), sha256=digest,
                            beforeAllocatedBytes=before, allocatedBytes=after))
    builds = [p for p in ROOT.iterdir() if p.is_dir() and (p / 'mkport_candidate.exe').is_file()]
    need(len(builds) == 16 and not (ROOT / 'mame-mkp/build/mingw-gcc').exists() and not native.census(),
         'Existing sixteen compiled folders; no compiler cache or newly running game')
    report = dict(passed=True, candidate=audit.current.NAME, goalStatus='active',
                  objective='Kano and Sonya appear as a natural part of the game in all aspects',
                  fullPortAcceptance=False, previousGoalTurnClassification=proof['previousGoalTurnClassification'],
                  thisGoalTurnClassification=proof['thisGoalTurnClassification'],
                  currentCompiledAndGuestSourceConservationAccepted=True,
                  wholeRetainedCampaignGatesRerun=4, retainedCampaignCases=cases,
                  reexecutedNativeFaults=sum(c['reexecutedFaultCount'] for c in cases),
                  currentWholeCampaignRuntimeAccepted=False,
                  originalFourCampaignsNotAnUntouchedWorkGroup=True,
                  originalAuditFailures=failed, remaining=parent['remaining'],
                  nextAction='Check remaining scene-boundary launch-audio exposure during genuine stage advancement, and audit conserved stock-victim/secret/cinematic branch coverage. Do not replay unchanged full towers just for the current executable label. Finish combined current gameplay/visual/audio regression, promote the matching CMD and create the final release ZIP only after the integration gaps are closed.',
                  selectedFileCount=len(files), uniqueSelectedAllocatedBytes=total,
                  retainedCompiledCandidates=16, publicPlayableChanged=False,
                  rootDocumentsChanged=False, newNativeBoots=0, newBuilds=0,
                  newROMCopies=0, newRawMedia=0, newZIPs=0,
                  inputHashes=pins, exactCompressedTargets=storage)
    need(all(sha(path) == digest for path, digest in pins.items()), 'All final immutable pins intact')
    out.mkdir()
    audit.seal(out / 'report.json', report)
    print(json.dumps({key: report[key] for key in ('passed', 'wholeRetainedCampaignGatesRerun',
                                                  'reexecutedNativeFaults', 'selectedFileCount',
                                                  'uniqueSelectedAllocatedBytes', 'newBuilds')}), flush=True)


if __name__ == '__main__':
    main()
