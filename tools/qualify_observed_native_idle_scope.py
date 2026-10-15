"""Reject non-idle direct-reference evidence as a standing parity claim."""
import json
from pathlib import Path
import verify_native_source_sync as sync

ROOT = sync.ROOT

def idle_candidate(references):
    # Membership is necessary here, never sufficient execution/scanout proof.
    return bool(references) and set(references).issubset({0, 64})

def main():
    source = ROOT / 'audit_observed_native_pose_sequences/report.json'
    report = json.loads(source.read_text())
    for path, expected in report['hashes'].items():
        assert sync.sha(Path(path)) == expected, path
    census = report['census']
    categorized = {}
    for fighter, entry in census.items():
        refs = entry['directAnimationReferences']
        categorized[fighter] = {
            'idleCandidates': [pose for pose, ids in refs.items() if idle_candidate(ids)],
            'notIdleEvidence': {pose: ids for pose, ids in refs.items() if not idle_candidate(ids)},
        }
    assert len(categorized['17']['idleCandidates']) == 5
    assert not categorized['18']['idleCandidates']
    assert not categorized['3']['idleCandidates']
    rejected = []
    for name, refs in [('walk', [1]), ('attack', [20]), ('unknown', []),
                       ('mixed_stance_attack', [0, 20]), ('recovery', [18])]:
        assert not idle_candidate(refs), name
        rejected.append(name)
    assert idle_candidate([0, 64]) and idle_candidate([0])
    out = ROOT / 'audit_observed_native_idle_scope_checked'
    out.mkdir(exist_ok=False)
    result = dict(passed=True, categories=categorized, rejectedNonIdleCases=rejected,
                  sourceSha256=sync.sha(source), checkerSha256=sync.sha(Path(__file__)),
                  sourceSync=sync.verify(), nativeIdleExecutionProven=False,
                  standingSoleParityAccepted=False, floorOffsetChangeJustified=False,
                  fullGoalComplete=False,
                  nextEvidence='Normal two-human neutral match; actual stance execution and clipped scanout endpoints')
    (out / 'report.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in
                     ('passed', 'categories', 'rejectedNonIdleCases', 'floorOffsetChangeJustified')}))

if __name__ == '__main__':
    main()
