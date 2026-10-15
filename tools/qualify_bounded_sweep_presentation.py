"""Bind sampled presented points to independently qualified real sweep trace."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def trace(folder):
    fields=[];hits=[];points=[];ended=False
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line and '_FAILED ' not in line and len(line)<1048576
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if '_FIELD ' in line:fields.append(r)
            elif '_CONTACT_HEALTH ' in line:hits.append(r)
            elif '_IDLE_VRAM_POINT ' in line:points.append(r)
            elif '_IDLE_TERMINAL ' in line:ended=r['fields']=='240'
    assert ended
    return fields,hits,points

def point_gate(points):
    assert len(points)>2000
    for r in points:
        assert r['source_vram']==r['display_vram']
        assert r['vram_rgb']==r['actual'] and r['display_matches']=='1'
        assert int(r['frame'])==int(r['source_frame'])+1

def main():
    out=sync.ROOT/'audit_bounded_sweep_presentation_checked';assert not out.exists()
    previous=sync.ROOT/'audit_bounded_spaced_sweep_checked/report.json'
    report=json.loads(previous.read_text());assert report['passed']
    results={}
    for fighter in ('sonya','kano'):
        baseline=sync.ROOT/f'audit_bounded_{fighter}_spaced_sweep_runtime'
        assert sync.sha(baseline/'run.log')==report['results'][fighter]['logSha256']
        folder=sync.ROOT/f'audit_bounded_{fighter}_sweep_presentation_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        fields,hits,points=trace(folder);oldfields,oldhits,_=trace(baseline)
        assert fields==oldfields and hits==oldhits,'Observer changed qualified actual gameplay'
        point_gate(points)
        bad=[dict(r) for r in points];bad[0]['actual']='WRONG'
        try:point_gate(bad)
        except AssertionError:pass
        else:raise AssertionError('Wrong presentation accepted')
        results[fighter]=dict(identicalQualifiedSweepGameplay=True,presentedPoints=len(points),
            unresolvedAllDrawPredictionPoints=sum(r['source_matches']=='0' for r in points),
            wrongPresentationRejected=True,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    final=dict(passed=True,results=results,sourceSync=sync.verify(),
        priorSweepProofSha256=sync.sha(previous),checkerSha256=sync.sha(Path(__file__)),
        entireRenderedArtAccepted=False,allReactionContextsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(final,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
