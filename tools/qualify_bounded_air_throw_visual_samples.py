"""Exact scalar prefix plus reviewed recovery images; early catch art unproven."""
import json
import re
import qualify_bounded_air_throw_retirement as prior
import verify_native_source_sync as sync

if __name__ == '__main__':
    out = sync.ROOT/'audit_bounded_air_throw_visual_samples_checked'
    assert not out.exists()
    results = {}
    total_bytes = 0
    for fighter in ('kano', 'sonya'):
        folder = sync.ROOT/f'audit_bounded_air_throw_visual_{fighter}_p1_runtime'
        baseline = sync.ROOT/f'audit_bounded_air_throw_retirement_{fighter}_p1_runtime'
        terminal = json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode'] == 0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        lines = [line for line in (folder/'run.log').read_text().splitlines() if line.startswith('MK2_BASIC_')]
        original = [line for line in (baseline/'run.log').read_text().splitlines() if line.startswith('MK2_BASIC_')]
        assert [line for line in lines if not line.startswith('MK2_BASIC_VISUAL_SAVED ')] == original
        rows = {}
        for line in lines:
            rows.setdefault(line.split()[0][10:], []).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        prior.gate(rows, fighter, 1)
        images = sorted((folder/'snap').rglob('*.png'))
        assert len(images) == 4 and len(rows['VISUAL_SAVED']) == 4
        pins = {str(path): sync.sha(path) for path in images}
        size = sum(path.stat().st_size for path in images)
        total_bytes += size
        results[fighter] = dict(imageSHA256=pins, imageBytes=size,
                               exactScalarBaselineRetained=True,
                               recoveredBodiesNamesFloorShadowsVisuallyReviewed=True,
                               activeCatchArtProven=False,
                               reason='Phase24 sample catches early near/above upper screen edge; not enough visible anatomy to qualify choreography.')
    report = dict(passed=True, results=results, pngCount=8, pngBytes=total_bytes,
                  fullVisualAcceptance=False, fullAudioAcceptance=False, fullPortAcceptance=False,
                  scope='Eight bounded reviewed PNGs and identical native scalar traces. Recovery appearance only; active choreography remains unproven.')
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,pngCount=8,pngBytes=total_bytes,fullVisualAcceptance=False)))
