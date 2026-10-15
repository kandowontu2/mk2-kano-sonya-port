"""Reviewed finite later poses; clipping/full choreography remain unqualified."""
import json
import re
import qualify_bounded_air_throw_retirement as prior
import verify_native_source_sync as sync

if __name__ == '__main__':
    out=sync.ROOT/'audit_bounded_air_throw_later_visuals_checked'
    assert not out.exists()
    results={}
    total=0
    for fighter in ('kano','sonya'):
        folder=sync.ROOT/f'audit_bounded_air_throw_later_visual_{fighter}_p1_runtime'
        baseline=sync.ROOT/f'audit_bounded_air_throw_retirement_{fighter}_p1_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        lines=[line for line in (folder/'run.log').read_text().splitlines() if line.startswith('MK2_BASIC_')]
        original=[line for line in (baseline/'run.log').read_text().splitlines() if line.startswith('MK2_BASIC_')]
        assert [line for line in lines if not line.startswith('MK2_BASIC_VISUAL_SAVED ')]==original
        rows={}
        for line in lines:
            rows.setdefault(line.split()[0][10:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        prior.gate(rows,fighter,1)
        images=sorted((folder/'snap').rglob('*.png'))
        assert len(images)==4
        assert {p.stem for p in images}=={f'air_{cycle}_phase{phase}' for cycle in (1,2) for phase in (40,56)}
        size=sum(p.stat().st_size for p in images)
        total+=size
        results[fighter]=dict(imageSHA256={str(p):sync.sha(p) for p in images},imageBytes=size,
            exactScalarBaselineRetained=True,ownBodiesVisibleInReviewedLaterSamples=True,
            entireChoreographyVerified=False,cameraBoundaryBehaviorVerified=False)
    report=dict(passed=True,results=results,pngCount=8,pngBytes=total,
        fullVisualAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,
        observations='Kano own release; Jax holds Kano/Sonya own victim sprites in sampled stages. Kano released Jax is partly right-edge clipped; requires stock/camera-boundary comparison. Not whole animation acceptance.')
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,pngCount=8,pngBytes=total,fullVisualAcceptance=False)))
