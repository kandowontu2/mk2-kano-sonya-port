"""Finite manually viewed cross-victim frames, not full animation proof."""
import json
from PIL import Image
import verify_native_source_sync as sync


def run(kind):
    sync.verify()
    out=sync.ROOT/f'audit_bounded_cross_{kind}_visuals_checked'
    assert not out.exists()
    reports=[];total=0
    for fighter in ('kano','sonya'):
        case=sync.ROOT/f'audit_bounded_cross_visual_{kind}_{fighter}_p1_runtime'
        old=sync.ROOT/f'audit_bounded_cross_{kind}_finisher_{fighter}_p1_runtime'
        terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert terminal['peakWorkingSetBytes']<=320*1024**2
        lua=sync.ROOT/f'audit_bounded_cross_finisher_visuals_preparation/{kind}.lua'
        assert terminal['observerSha256'].lower()==sync.sha(lua).lower()
        assert not (case/'stderr.log').read_text().strip()
        text=(case/'run.log').read_text()
        prefix='MK2_STOCK_HEAD_V921_'
        actual=[line for line in text.splitlines() if line.startswith(prefix) and not line.startswith(prefix+'VISUAL_SAVED')]
        expected=[line for line in (old/'run.log').read_text().splitlines() if line.startswith(prefix)]
        assert actual==expected
        images=list((case/'snap').rglob('*.png'))
        assert len(images)==4
        samples=[]
        for path in images:
            with Image.open(path) as image: assert image.size==(400,254)
            total+=path.stat().st_size
            samples.append({'path':str(path),'sha256':sync.sha(path),'bytes':path.stat().st_size})
        reports.append({'performer':fighter,'victim':'sonya' if fighter=='kano' else 'kano','side':1,'manualReview':'Expected performer and added victim, own effects/body/name and native winner banner visible; no selection photos over combat. Completed sample remains held fatality scene, not transition clearing.','samples':samples,'terminal':terminal})
    out.mkdir()
    (out/'report.json').write_text(json.dumps({'finiteViewedSamples':8,'totalPngBytes':total,'mechanicsUnchanged':True,'completeAnimationAcceptance':False,'transitionAcceptance':False,'audioAcceptance':False,'releaseAcceptance':False,'cases':reports},indent=2))
    print(f'PASS: eight viewed cross-{kind} P1 samples, {total} PNG bytes; not full art/audio/clearing')


if __name__=='__main__': run('primary')
