"""Two viewed later-scene frames per cross-victim action, not all fields."""
import json
from PIL import Image
import verify_native_source_sync as sync


def run(kind):
    sync.verify()
    out=sync.ROOT/f'audit_bounded_cross_{kind}_rejoin_visuals_checked'
    assert not out.exists()
    reports=[];total=0
    prefix='MK2_STOCK_HEAD_V921_'
    for fighter in ('kano','sonya'):
        case=sync.ROOT/f'audit_bounded_cross_rejoin_visual_{kind}_{fighter}_p1_runtime'
        baseline=sync.ROOT/f'audit_bounded_cross_rejoin_{kind}_{fighter}_p1_runtime'
        terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert terminal['peakWorkingSetBytes']<=320*1024**2
        assert not (case/'stderr.log').read_text().strip()
        text=(case/'run.log').read_text()
        actual=[line for line in text.splitlines() if line.startswith(prefix) and not line.startswith(prefix+'REJOIN_VISUAL_SAVED')]
        expected=[line for line in (baseline/'run.log').read_text().splitlines() if line.startswith(prefix) and not line.startswith(prefix+'REJOIN_MARKER')]
        assert actual==expected,'Native mechanics changed'
        assert prefix+'REJOIN_TERMINAL' in text and prefix+'REJOIN_FAILED' not in text
        images=list((case/'snap').rglob('*.png'))
        assert len(images)==2
        samples=[]
        for path in images:
            with Image.open(path) as image: assert image.size==(400,254)
            total+=path.stat().st_size
            samples.append({'path':str(path),'sha256':sync.sha(path),'bytes':path.stat().st_size})
        reports.append({'kind':kind,'fighter':fighter,'side':1,'manualReview':'Native selection and new-match frames clear prior fatality body/skeleton/flames/bones/effects/banner; expected added bodies and names in new match, no selection portraits over arena.','samples':samples,'terminal':terminal})
    out.mkdir()
    (out/'report.json').write_text(json.dumps({'finiteViewedSamples':4,'totalPngBytes':total,'mechanicsUnchanged':True,'everyTransitionFrameAcceptance':False,'p2RasterAcceptance':False,'audioAcceptance':False,'releaseAcceptance':False,'cases':reports},indent=2))
    print(f'PASS: four viewed P1 cross-{kind} later-scene samples, {total} PNG bytes')


if __name__=='__main__': run('primary')
